"""
Genera la demanda de la simulacion base (hora pico 2026) a partir de los volumenes por movimiento
del capitulo 4 de Estanga y Savignani (2021) y Assouad y Peroza (2022) (demanda/conteos_movimientos.csv).

Actualizacion a 2026 (ver FACTOR_2026):
  - crecimiento de 2,5 % anual (INE, el mismo que usa Perozo) durante 5 anos: 1,025^5 = 1,131
  - recuperacion del transito post COVID-19 y crisis de combustible: +50 % (Savignani 2021, cap. 4)

Metodo: muestreo voraz de rutas, el mismo criterio por defecto de la herramienta routeSampler de SUMO.
  1. Se generan rutas candidatas entre todos los bordes de la red (origenes y destinos) que pasan
     por los puntos de conteo.
  2. Se asignan vehiculos uno a uno a rutas que solo pasan por puntos de conteo con demanda pendiente,
     prefiriendo las rutas mas directas, hasta agotar los conteos.
  3. Cada ruta se escribe como un flujo con llegadas de Poisson (period="exp(...)").
El transporte publico (buses y carritos con paradas, en costanera.rou.xml) se descuenta de los conteos.

Uso:  python generar_demanda.py
"""
import csv
import heapq
import itertools
import math
import os
import random
import sys
from collections import defaultdict

SUMO_HOME = os.environ.get('SUMO_HOME', r'C:\SUMO')
sys.path.insert(0, os.path.join(SUMO_HOME, 'tools'))
import sumolib  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
RED = os.path.join(AQUI, '..', 'costanera.net.xml')
CONTEOS = os.path.join(AQUI, '..', 'demanda', 'conteos_movimientos.csv')
TRANSPORTE_PUBLICO = os.path.join(AQUI, '..', 'costanera.rou.xml')

FIN_FLUJOS = 4500        # 15 min de calentamiento + 60 min de analisis
DESVIO_MAX = 800.0       # metros extra permitidos frente a la ruta mas corta del mismo origen-destino
DESVIO_MAX_U = 2000.0    # rutas forzadas por un giro en U contado
SEMILLA = 2026
ESCENARIO_FUENTE = 'tesis2021'          # filas de conteos_movimientos.csv que se usan
FACTOR_2026 = 1.025 ** 5 * 1.5          # = 1,697
# Calles secundarias (salidas de Av. Rio, Residencias y accesos residenciales): solo crecimiento INE.
# La recuperacion post COVID de +50 % (Savignani) corresponde al transito del corredor principal;
# aplicada a Av. Rio daba unos 850 veh/h (Perozo 2021: 559; campo 2026: 180 sin motos).
FACTOR_SECUNDARIAS = 1.025 ** 5             # = 1,131
ACCESOS_SECUNDARIOS = {'avrio_1', 'res_salida', 'salida_bissau_1', 'salida_bissau_2', 'salida:puerto_guaica', '-335982664#1'}
# En Perrokero, las salidas de Av. Rio y Residencias usan el aforo propio 2026 (sin motos): es el flujo que realmente
# logra salir. Esos giros sin semaforo cruzando FFAA tienen una capacidad muy baja (Perozo 2022, tabla 4.8: 93 veh/h),
# por lo que los 559 veh/h de 2021 (o 850 con el factor) no caben fisicamente y generaban colas irreales.
CAMPO_PARA_SECUNDARIAS = {'avrio_1', 'res_salida'}
# Variacion dentro de la hora: un cuarto de hora pico con FHMD = 0,90 (promedio de los FHMD de Savignani 0,87-0,92
# y Perozo 0,83-0,94). Cuarto pico = 1/FHMD = 1,111 veces el promedio; los otros tres = 0,963 (el total horario no cambia).
FHMD = 0.90
PERFIL_15MIN = [(0, 900, None), (900, 1800, None), (1800, 2700, 'pico'), (2700, 3600, None), (3600, 4500, None)]

# Origenes y destinos de la demanda: extremos de las avenidas y puerta de cada acceso residencial.
# (No se usan las calles internas de las urbanizaciones para no generar recorridos artificiales.)
ORIGENES = {
    'lecheria_salida': 'Lecheria', 'madre_vieja_salida': 'Madre Vieja', 'costanera_salida': 'El Ejercito',
    'fuerzas_armadas_salida': 'FFAA sur', 'av_rio_salida': 'Av. Rio', 'res_salida': 'Residencias Perrokero',
    '-495730009#2': 'Bissau residencias/CC', 'bissau_salida': 'Bissau galpones',
    '-1227058160#0': 'Puerto Guaica', '-1088915526': 'Fernandez Padilla',
}
DESTINOS = {
    'lecheria_entrada': 'Lecheria', 'madre_vieja_entrada': 'Madre Vieja', 'costanera_entrada': 'El Ejercito',
    'fuerzas_armadas_entrada': 'FFAA sur', 'av_rio_entrada': 'Av. Rio', 'res_entrada': 'Residencias Perrokero',
    'bissau_entrada': 'Bissau residencias/CC', '-1227058169': 'Bissau galpones',
    'puerto_guaica': 'Puerto Guaica', '1088915526': 'Fernandez Padilla',
}
CLASES = {'livianos': ('liviano', 'passenger', 'L'), 'pesados': ('pesado', 'bus', 'P')}


def construir_grafo(net, vclass):
    suc = {}
    for e in net.getEdges():
        if not e.allows(vclass):
            continue
        suc[e.getID()] = [o.getID() for o, conns in e.getOutgoing().items()
                          if o.allows(vclass) and any(c.getFromLane().allows(vclass) for c in conns)]
    pred = defaultdict(list)
    for a, lst in suc.items():
        for b in lst:
            pred[b].append(a)
    largo = {e.getID(): e.getLength() for e in net.getEdges()}
    return suc, pred, largo


def dijkstra(inicio, vecinos, largo):
    """distancia y predecesor desde 'inicio' (incluye el largo de cada edge recorrido)"""
    dist, prev = {inicio: largo[inicio]}, {inicio: None}
    cola = [(largo[inicio], inicio)]
    while cola:
        d, e = heapq.heappop(cola)
        if d > dist[e]:
            continue
        for n in vecinos.get(e, ()):
            nd = d + largo[n]
            if nd < dist.get(n, math.inf):
                dist[n], prev[n] = nd, e
                heapq.heappush(cola, (nd, n))
    return dist, prev


def camino(prev, fin):
    out = []
    while fin is not None:
        out.append(fin)
        fin = prev[fin]
    return out


def leer_conteos(escenario):
    filas = []
    with open(CONTEOS, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f, delimiter=';'):
            if r['escenario'] == escenario:
                for clase in CLASES:
                    r['original_' + clase] = r[clase]
                    factor = FACTOR_SECUNDARIAS if r['desde'] in ACCESOS_SECUNDARIOS else FACTOR_2026
                    r[clase] = str(float(r[clase]) * factor)
                filas.append(r)
    if not filas:
        sys.exit(f'No hay conteos para el escenario "{escenario}"')
    # reemplazo por el aforo 2026 en las salidas de calles secundarias de Perrokero
    with open(CONTEOS, encoding='utf-8-sig') as f:
        campo = {clave(r): r for r in csv.DictReader(f, delimiter=';') if r['escenario'] == 'campo2026'}
    for r in filas:
        if r['desde'] in CAMPO_PARA_SECUNDARIAS:
            rc = campo.get(clave(r))
            for clase in CLASES:
                r[clase] = rc[clase] if rc else '0'
            r['fuente'] = (rc['fuente'] if rc else 'No contado en campo 2026') + ' (aforo 2026 para calle secundaria)'
    return filas


def clave(fila):
    return (fila['desde'], fila['hacia']) if fila['hacia'] else fila['desde']


def puntos_de_ruta(ruta):
    pts = set(ruta)
    pts.update(zip(ruta, ruta[1:]))
    return pts


def transporte_publico(net, suc_bus, largo):
    """volumen horario de buses y carritos con parada, para descontarlo de los conteos"""
    tp = []
    for f in sumolib.xml.parse(TRANSPORTE_PUBLICO, 'flow'):
        dist, prev = dijkstra(f.attr_from, suc_bus, largo)
        ruta = list(reversed(camino(prev, f.to)))
        clase = 'pesados' if f.type == 'pesado' else 'livianos'   # carritos: contados como livianos en campo
        tp.append((clase, float(f.perHour if f.hasAttribute('perHour') else 3600.0 / float(f.period.strip('exp()') or 1)), ruta))
    return tp


def optimizar(rutas, objetivo, inicial, bloqueados, iteraciones=4000, penal_desvio=0.05, minimo=0.05):
    """Mejora la solucion voraz: minimos cuadrados no negativos entre conteos y demanda asignada
    (equivalente a la opcion --optimize de routeSampler), con una pequena penalizacion por metro
    de desvio para preferir rutas directas. Las rutas que pasan por un movimiento contado en 0 se excluyen.
    Cada conteo se pondera por 1/conteo (error relativo, como el GEH) para que los accesos pequenos
    no queden en cero frente a los movimientos grandes de la avenida."""
    usables = [(r, pts, desvio) for r, (pts, desvio) in rutas if not any(k in bloqueados for k in pts)]
    peso = {k: 1.0 / max(v, 5.0) for k, v in objetivo.items()}
    x = [inicial.get(r, 0) + 0.5 for r, _, _ in usables]
    for _ in range(iteraciones):
        sim = defaultdict(float)
        for xi, (_, pts, _) in zip(x, usables):
            for k in pts:
                sim[k] += xi
        for i, (_, pts, desvio) in enumerate(usables):
            num = sum(peso[k] * objetivo[k] for k in pts)
            den = sum(peso[k] * sim[k] for k in pts) + penal_desvio * desvio / 100.0 + 1e-9
            x[i] *= num / den
    return {r: xi for xi, (r, _, _) in zip(x, usables) if xi >= minimo}


def generar(escenario):
    net = sumolib.net.readNet(RED, withInternal=False)
    filas = leer_conteos(escenario)
    random.seed(SEMILLA)
    salida_rutas = []
    informe = []
    tp = None

    for clase, (vtype, vclass, prefijo) in CLASES.items():
        suc, pred, largo = construir_grafo(net, vclass)
        if tp is None:
            suc_bus, _, _ = construir_grafo(net, 'bus')
            tp = transporte_publico(net, suc_bus, largo)
        fuentes = [e for e in ORIGENES if e in suc]
        sumideros = [e for e in DESTINOS if e in suc]
        nodos = {e.getID(): (e.getFromNode().getID(), e.getToNode().getID()) for e in net.getEdges()}
        giros_u = set()
        for r in filas:
            if r['hacia']:
                conns = net.getEdge(r['desde']).getOutgoing().get(net.getEdge(r['hacia']), [])
                if any(c.getDirection() in ('t', 'T') for c in conns):
                    giros_u.add(clave(r))

        objetivo = defaultdict(float)
        for r in filas:
            objetivo[clave(r)] += float(r[clase])
        for c, vol, ruta in tp:
            if c == clase:
                pts = puntos_de_ruta(ruta)
                for k in objetivo:
                    if k in pts:
                        objetivo[k] = max(0.0, objetivo[k] - vol)
        pendiente = {k: int(round(v)) for k, v in objetivo.items()}

        adelante = {s: dijkstra(s, suc, largo) for s in fuentes}
        atras = {t: dijkstra(t, pred, largo) for t in sumideros}

        candidatas = {}
        def agregar(ruta, s, t):
            if ORIGENES[s] == DESTINOS[t]:
                return
            pts = [k for k in pendiente if k in puntos_de_ruta(ruta)]
            con_u = any(k in giros_u for k in pts)
            recorrido = [nodos[ruta[0]][0]] + [nodos[e][1] for e in ruta]
            if not con_u and len(set(recorrido)) != len(recorrido):   # sin bucles ni vueltas por calles internas
                return
            directo = adelante[s][0].get(t)
            if directo is None:
                return
            l = sum(largo[e] for e in ruta)
            limite = DESVIO_MAX_U if con_u else DESVIO_MAX
            if pts and l <= directo + limite:
                candidatas[tuple(ruta)] = (pts, l - directo)

        for s in fuentes:
            dist, prev = adelante[s]
            for t in sumideros:
                if t in dist and t != s:
                    agregar(list(reversed(camino(prev, t))), s, t)
        # rutas forzadas por cada punto de conteo (giros en U, accesos secundarios)
        for k in pendiente:
            a, b = k if isinstance(k, tuple) else (k, k)
            for s in fuentes:
                ds, ps = adelante[s]
                if a not in ds:
                    continue
                ida = list(reversed(camino(ps, a)))
                for t in sumideros:
                    dt, pt = atras[t]
                    if b not in dt:
                        continue
                    vuelta = camino(pt, b)
                    ruta = ida + (vuelta if a != b else vuelta[1:])
                    agregar(ruta, s, t)

        rutas = sorted(candidatas.items())
        volumen = defaultdict(int)
        utiles = None
        while True:
            if utiles is None:
                utiles = [(r, pts, desvio) for r, (pts, desvio) in rutas if all(pendiente[k] > 0 for k in pts)]
                if not utiles:
                    break
                acumulado = list(itertools.accumulate(
                    len(pts) * math.exp(-desvio / 200.0) for _, pts, desvio in utiles))
            r, pts, _ = random.choices(utiles, cum_weights=acumulado)[0]
            volumen[r] += 1
            for k in pts:
                pendiente[k] -= 1
                if pendiente[k] == 0:
                    utiles = None

        # un conteo observado en 0 (para este tipo de vehiculo) prohibe ese movimiento
        bloqueados = {clave(r) for r in filas if float(r[clase]) == 0}
        volumen = optimizar(rutas, objetivo, volumen, bloqueados)
        for i, (r, v) in enumerate(sorted(volumen.items(), key=lambda x: -x[1])):
            salida_rutas.append((f'{prefijo}{i:03d}', vtype, v, r))

        # informe de ajuste (incluye el transporte publico)
        simulado = defaultdict(float)
        for r, v in volumen.items():
            for k in puntos_de_ruta(list(r)):
                simulado[k] += v
        for c, vol, ruta in tp:
            if c == clase:
                for k in puntos_de_ruta(ruta):
                    simulado[k] += vol
        for r in filas:
            k = clave(r)
            informe.append((r['interseccion'], r['codigo'], r['descripcion'], clase, float(r['original_' + clase]), float(r[clase]), simulado[k]))

    nombre = 'demanda_base'
    ruta_xml = os.path.join(AQUI, '..', 'demanda', nombre + '.rou.xml')
    with open(ruta_xml, 'w', encoding='utf-8') as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<!-- Generado por herramientas/generar_demanda.py (hora pico 2026 = volumenes de las tesis x {FACTOR_2026:.3f}). No editar a mano: modificar demanda/conteos_movimientos.csv y volver a generar. -->\n')
        f.write('<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n')
        pico = 1.0 / FHMD
        resto = (4 - pico) / 3
        for fid, vtype, v, r in salida_rutas:
            f.write(f'    <route id="r_{fid}" edges="{" ".join(r)}"/>\n')
        # SUMO exige los flujos ordenados por hora de inicio: primero todos los del cuarto 0, luego los del 1, etc.
        for q, (ini, fin, tipo) in enumerate(PERFIL_15MIN):
            for fid, vtype, v, r in salida_rutas:
                tasa = v * (pico if tipo == 'pico' else resto) / 3600.0
                f.write(f'    <flow id="{fid}_q{q}" type="{vtype}" route="r_{fid}" begin="{ini}" end="{fin}" period="exp({tasa:.6f})" departLane="best" departSpeed="max"/>\n')
        f.write('</routes>\n')

    ruta_inf = os.path.join(AQUI, '..', 'demanda', 'ajuste_demanda_base.csv')
    with open(ruta_inf, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['interseccion', 'codigo', 'descripcion', 'clase', 'tesis 2021 (veh/h)', 'objetivo 2026 (veh/h)', 'demanda generada (veh/h)', 'GEH'])
        geh_ok = n = 0
        for inter, cod, desc, clase, orig, obj, sim in informe:
            if obj == 0 and sim == 0:
                continue
            geh = math.sqrt(2 * (sim - obj) ** 2 / (sim + obj)) if sim + obj > 0 else 0.0
            n += 1
            geh_ok += geh < 5
            w.writerow([inter, cod, desc, clase, f'{orig:.0f}', f'{obj:.0f}', f'{sim:.0f}', f'{geh:.2f}'])
    total = sum(v for _, _, v, _ in salida_rutas)
    print(f'Demanda base hora pico 2026: {len(salida_rutas)} rutas, {total:.0f} veh/h (sin transporte publico); GEH<5 en {geh_ok} de {n} conteos')
    print(f'  -> {os.path.normpath(ruta_xml)}\n  -> {os.path.normpath(ruta_inf)}')


if __name__ == '__main__':
    generar(ESCENARIO_FUENTE)
