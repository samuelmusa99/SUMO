"""
Demanda, capacidad, relacion volumen/capacidad (V/C) y demanda atendida por acceso.

Demanda (veh/h): vehiculos que quieren pasar por el acceso en la hora de analisis (900-4500 s), segun los
  archivos de demanda del escenario (incluye los que no lograron entrar a la red).
Capacidad (veh/h), metodo HCM 2000 (el mismo enfoque de las tesis evaluadas):
  - acceso semaforizado:            c = s x N x (g / C), s = 1900 x fVP, g = verde + amarillo - 4 s (tiempo perdido)
  - acceso principal sin semaforo:  c = 1900 x fVP x N (flujo libre, sin control)
  - acceso secundario sin semaforo: capacidad potencial HCM 2000 de carril compartido,
        c_m = Vc e^(-Vc tc/3600) / (1 - e^(-Vc tf/3600)), con tc/tf = 7,1/3,5 (izq.), 6,5/4,0 (frente), 6,2/3,3 (der.)
        y Vc = flujo de los accesos principales medido en la simulacion (la mitad para el giro a la derecha);
        c_acceso = suma(v_m) / suma(v_m / c_m)
  fVP = 1 / (1 + %pesados x (2 - 1)) (factor por vehiculos pesados, equivalente 2,0).
  Si en la simulacion el acceso esta saturado (con al menos 50 veh/h: atiende menos del 95 % de su demanda o su demora es de nivel F), la capacidad es el
  flujo que realmente logra descargar (capacidad medida en la simulacion).
"""
import csv
import math
import os
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

SUMO_HOME = os.environ.get('SUMO_HOME', r'C:\SUMO')
sys.path.insert(0, os.path.join(SUMO_HOME, 'tools'))
import sumolib  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
MAPA = os.path.join(AQUI, '..', 'accesos_intersecciones.csv')
INICIO, FIN = 900.0, 4500.0
PERDIDO_POR_FASE = 4.0
TC_TF = {'l': (7.1, 3.5), 'L': (7.1, 3.5), 't': (7.1, 3.5), 's': (6.5, 4.0), 'r': (6.2, 3.3), 'R': (6.2, 3.3)}


def archivos_de_ruta(config):
    raiz = ET.parse(config).getroot()
    base = os.path.dirname(os.path.abspath(config))
    rutas = raiz.find('input/route-files').get('value').split(',')
    red = raiz.find('input/net-file').get('value')
    return os.path.join(base, red), [os.path.join(base, r.strip()) for r in rutas]


def demanda_por_movimiento(net, archivos):
    """(edge, edge siguiente) -> [veh/h totales, veh/h pesados] en la hora de analisis"""
    mov = defaultdict(lambda: [0.0, 0.0])
    tipos_pesados = {'pesado'}
    for archivo in archivos:
        raiz = ET.parse(archivo).getroot()
        rutas = {r.get('id'): r.get('edges').split() for r in raiz.iter('route') if r.get('id')}
        for f in raiz.iter('flow'):
            ini, fin = float(f.get('begin')), float(f.get('end'))
            solape = max(0.0, min(fin, FIN) - max(ini, INICIO))
            if solape <= 0:
                continue
            if f.get('period', '').startswith('exp('):
                vph = float(f.get('period')[4:-1]) * solape
            elif f.get('perHour'):
                vph = float(f.get('perHour')) * solape / 3600.0
            else:
                continue
            if f.get('route'):
                edges = rutas[f.get('route')]
            elif f.find('route') is not None:
                edges = f.find('route').get('edges').split()
            else:
                vclass = 'bus' if f.get('type') in ('pesado', 'carrito') else 'passenger'
                camino, _ = net.getShortestPath(net.getEdge(f.get('from')), net.getEdge(f.get('to')), vClass=vclass)
                edges = [e.getID() for e in camino] if camino else []
            pesado = f.get('type') in tipos_pesados
            for a, b in zip(edges, edges[1:]):
                mov[(a, b)][0] += vph
                if pesado:
                    mov[(a, b)][1] += vph
    return mov


def verde_y_ciclo(net, edge):
    """verde efectivo maximo de los movimientos del acceso y duracion del ciclo (programa activo de la red)"""
    # el semaforo puede tener un id distinto al del nodo (clusters): se busca por las conexiones del acceso
    tls = next(t for t in net.getTrafficLights() if any(c[0].getEdge() == edge for c in t.getConnections()))
    programa = list(tls.getPrograms().values())[0]
    fases = programa.getPhases()
    ciclo = sum(p.duration for p in fases)
    indices = {c[2] for c in tls.getConnections() if c[0].getEdge() == edge}
    verde = 0.0
    for i in indices:
        g = sum(p.duration for p in fases if p.state[i] in 'Gg')
        y = sum(p.duration for p in fases if p.state[i] in 'yY')
        verde = max(verde, g + y - PERDIDO_POR_FASE)
    return max(verde, 0.0), ciclo


def capacidad_potencial(vc, tc, tf):
    if vc <= 0:
        return 1900.0
    return vc * math.exp(-vc * tc / 3600.0) / (1 - math.exp(-vc * tf / 3600.0))


def calcular(config, atendido_por_acceso, demora_por_acceso=None):
    """atendido_por_acceso: (interseccion, acceso) -> veh/h atendidos (promedio de replicas).
    Devuelve (interseccion, acceso) -> dict con demanda, capacidad_hcm, capacidad, fuente, vc, atendida"""
    red, archivos = archivos_de_ruta(config)
    net = sumolib.net.readNet(red, withPrograms=True)
    mov = demanda_por_movimiento(net, archivos)
    with open(MAPA, encoding='utf-8-sig') as f:
        accesos = list(csv.DictReader(f, delimiter=';'))
    principal_vol = defaultdict(float)
    for a in accesos:
        if a['tipo'] == 'principal':
            principal_vol[a['interseccion']] += atendido_por_acceso.get((a['interseccion'], a['acceso']), 0.0)
    salida = {}
    for a in accesos:
        e = net.getEdge(a['tramo_final'])
        movs = {b: v for (x, b), v in mov.items() if x == e.getID()}
        demanda = sum(v[0] for v in movs.values())
        pesados = sum(v[1] for v in movs.values())
        fvp = 1.0 / (1.0 + (pesados / demanda if demanda else 0.0))
        s = 1900.0 * fvp
        n = e.getLaneNumber()
        if e.getToNode().getType() == 'traffic_light':
            g, ciclo = verde_y_ciclo(net, e)
            cap_hcm = s * n * g / ciclo
        elif a['tipo'] == 'principal':
            cap_hcm = s * n
        else:
            vc_total = principal_vol[a['interseccion']]
            suma_v = suma_vc = 0.0
            for b, (v, _) in movs.items():
                conns = e.getOutgoing().get(net.getEdge(b), [])
                d = conns[0].getDirection() if conns else 'l'
                tc, tf = TC_TF.get(d, (7.1, 3.5))
                vc = vc_total * (0.5 if d in ('r', 'R') else 1.0)
                cm = capacidad_potencial(vc, tc, tf) * fvp
                if v > 0:
                    suma_v += v
                    suma_vc += v / cm
            cap_hcm = suma_v / suma_vc if suma_vc else s * n
        atendido = atendido_por_acceso.get((a['interseccion'], a['acceso']), 0.0)
        atendida = atendido / demanda if demanda else 1.0
        # saturado: con una demanda apreciable (con pocos veh/h la diferencia es solo azar), atiende menos del 95 %
        # o su demora ya es de nivel F (cola permanente; p. ej. carril bloqueado por vehiculos que giran a la izquierda)
        semaforizado = e.getToNode().getType() == 'traffic_light'
        demora = (demora_por_acceso or {}).get((a['interseccion'], a['acceso']), 0.0)
        nivel_f = demora > (80.0 if semaforizado else 50.0)
        if demanda >= 50 and (atendida < 0.95 or nivel_f):
            capacidad, fuente = atendido, 'medida (acceso saturado)'
        else:
            capacidad, fuente = cap_hcm, 'HCM 2000'
        salida[(a['interseccion'], a['acceso'])] = {
            'demanda': demanda, 'capacidad_hcm': cap_hcm, 'capacidad': capacidad, 'fuente': fuente,
            'vc': demanda / capacidad if capacidad else 0.0, 'atendida': min(atendida, 1.0)}
    return salida
