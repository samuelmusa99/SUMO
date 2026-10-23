"""
Demanda de la propuesta Estanga y Savignani (2021) a partir de la demanda base (2026 y 2041).

La demanda de cada horizonte es la misma de la base (demanda/demanda_base.rou.xml y demanda_2041.rou.xml, generadas en
main con generar_demanda.py); solo cambia lo que exige la propuesta:
  1. Rutas: se recalculan sobre la red con el distribuidor. Se conservan los tramos de la ruta base que siguen
     existiendo fuera de Camino Real y se unen por el camino mas corto (asi el transito Costanera <-> FFAA usa el puente).
  2. Avenida en proyeccion: el distribuidor necesita la nueva avenida (av_proyeccion), que recibe el
     PROPORCION_AV_PROYECCION de los viajes con origen o destino en FFAA sur que cruzan Camino Real por FFAA: en esos
     viajes el extremo FFAA sur se cambia por la avenida en proyeccion.
El transporte publico con paradas (costanera.rou.xml) no cambia.

Uso:  python demanda_propuesta.py   (volver a ejecutarlo si cambia la red o la demanda base)
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

SUMO_HOME = os.environ.get('SUMO_HOME', r'C:\SUMO')
sys.path.insert(0, os.path.join(SUMO_HOME, 'tools'))
import sumolib  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
RED = os.path.join(AQUI, '..', 'costanera.net.xml')
DEMANDA = os.path.join(AQUI, '..', 'demanda')
ARCHIVOS = {'demanda_base.rou.xml': 'demanda_savignani_2026.rou.xml',
            'demanda_2041.rou.xml': 'demanda_savignani_2041.rou.xml'}

PROPORCION_AV_PROYECCION = 0.30
FFAA_ORIGEN, FFAA_DESTINO = 'fuerzas_armadas_salida', 'fuerzas_armadas_entrada'
PROY_ORIGEN, PROY_DESTINO = 'av_proyeccion_salida', 'av_proyeccion_entrada'
# tramos de la rama FFAA en Camino Real en la red base: si la ruta base pasa por ellos, el viaje cruza Camino Real por FFAA
FFAA_EN_CAMINO_REAL = {'semaforo_caminoreal_FA', 'semaforocaminorea_haciaperrokero'}
# nodos del distribuidor: los tramos que llegan o salen de ellos se rehacen (no se usan como puntos de paso)
NODOS_DISTRIBUIDOR = {'semaforo_caminoreal', 'distribuidor_lado_costanera', 'distribuidor_lado_ffaa', 'ffaa_nueva_etruria',
                      'puente_tablero_lado_costanera', 'puente_tablero_lado_ffaa'}
# el transito liviano pasante Costanera <-> FFAA cruza por el puente (en la red el puente no admite pesados: van a nivel)
PUENTE = {('semaforo_caminoreal_costanera', 'semaforocaminorea_haciaperrokero'): 'puente_hacia_ffaa',
          ('semaforo_caminoreal_FA', '172344969#0'): 'puente_hacia_costanera'}
VCLASS = {'liviano': 'passenger', 'pesado': 'bus', 'carrito': 'bus'}


def rehacer(net, edges, vclass):
    """une por el camino mas corto los tramos de la ruta base que siguen existiendo fuera del distribuidor"""
    for (a, b), puente in PUENTE.items():
        if vclass == 'passenger' and a in edges and b in edges[edges.index(a):]:
            edges = edges[:edges.index(a)] + [puente] + edges[edges.index(a):]
    paso = [e for i, e in enumerate(edges) if net.hasEdge(e) and (i in (0, len(edges) - 1) or e in PUENTE.values() or
            not {net.getEdge(e).getFromNode().getID(), net.getEdge(e).getToNode().getID()} & NODOS_DISTRIBUIDOR)]
    ruta = [paso[0]]
    for sig in paso[1:]:
        a, b = net.getEdge(ruta[-1]), net.getEdge(sig)
        if b in a.getAllowedOutgoing(vclass):
            ruta.append(sig)
            continue
        camino, _ = net.getShortestPath(a, b, vClass=vclass)
        if not camino:
            raise RuntimeError(f'sin camino de {a.getID()} a {sig} ({vclass})')
        ruta.extend(e.getID() for e in camino[1:])
    return ruta


def main():
    net = sumolib.net.readNet(RED)
    for entrada, salida in ARCHIVOS.items():
        raiz = ET.parse(os.path.join(DEMANDA, entrada)).getroot()
        rutas = {r.get('id'): r.get('edges').split() for r in raiz.iter('route')}
        tipo_ruta = {f.get('route'): f.get('type') for f in raiz.iter('flow')}
        nuevas, desviadas = {}, {}
        for rid, edges in rutas.items():
            vc = VCLASS[tipo_ruta.get(rid, 'liviano')]
            nuevas[rid] = rehacer(net, edges, vc)
            if FFAA_EN_CAMINO_REAL & set(edges) and (edges[0] == FFAA_ORIGEN or edges[-1] == FFAA_DESTINO):
                # la avenida en proyeccion reemplaza todo el recorrido por FFAA hasta Camino Real
                corte = next(i for i, e in enumerate(edges) if e in FFAA_EN_CAMINO_REAL)
                if edges[0] == FFAA_ORIGEN:
                    desvio = [PROY_ORIGEN] + edges[corte + 1:]
                else:
                    desvio = edges[:corte] + [PROY_DESTINO]
                desviadas[rid] = rehacer(net, desvio, vc)
        lineas = ['<?xml version="1.0" encoding="UTF-8"?>',
                  f'<!-- Generado por herramientas/demanda_propuesta.py a partir de {entrada}: misma demanda de la base, rutas sobre '
                  f'la red con el distribuidor y {PROPORCION_AV_PROYECCION:.0%} de los viajes FFAA sur por Camino Real '
                  f'desviados a la avenida en proyeccion. No editar a mano. -->',
                  '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                  'xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">']
        for rid in rutas:
            lineas.append(f'    <route id="{rid}" edges="{" ".join(nuevas[rid])}"/>')
            if rid in desviadas:
                lineas.append(f'    <route id="{rid}_proy" edges="{" ".join(desviadas[rid])}"/>')
        total, movidos = 0.0, 0.0
        for f in raiz.iter('flow'):
            tasa = float(re.fullmatch(r'exp\((.*)\)', f.get('period')).group(1))
            total += tasa
            atr = dict(f.attrib)
            if f.get('route') in desviadas:
                movidos += tasa * PROPORCION_AV_PROYECCION
                atr['period'] = f'exp({tasa * (1 - PROPORCION_AV_PROYECCION):.6f})'
                lineas.append('    <flow ' + ' '.join(f'{k}="{v}"' for k, v in atr.items()) + '/>')
                atr.update(id=f.get('id') + '_proy', route=f.get('route') + '_proy',
                           period=f'exp({tasa * PROPORCION_AV_PROYECCION:.6f})')
            lineas.append('    <flow ' + ' '.join(f'{k}="{v}"' for k, v in atr.items()) + '/>')
        lineas.append('</routes>')
        with open(os.path.join(DEMANDA, salida), 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(lineas) + '\n')
        print(f'{salida}: {len(rutas)} rutas, {len(desviadas)} con desvio a la avenida en proyeccion; '
              f'{movidos / total:.1%} de los vehiculos van por ella')


if __name__ == '__main__':
    main()
