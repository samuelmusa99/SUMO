"""
Demanda de la propuesta Assouad y Peroza (2022) a partir de la demanda base (2026 y 2041).

La demanda de cada horizonte es la misma de la base (demanda/demanda_base.rou.xml y demanda_2041.rou.xml, generadas en
main con generar_demanda.py); solo cambian las rutas en Perrokero, donde la propuesta divide FFAA en puente y nivel:
  - los livianos que siguen derecho por FFAA (movimientos MF2 y MF5 de la tesis) cruzan por el puente;
  - los giros, los pesados y los carritos (clase bus, no admitidos en el puente) cruzan a nivel por el semaforo.
El transporte publico con paradas (costanera.rou.xml) no cambia: SUMO le calcula la ruta y no puede usar el puente.

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
ARCHIVOS = {'demanda_base.rou.xml': 'demanda_perozo_2026.rou.xml',
            'demanda_2041.rou.xml': 'demanda_perozo_2041.rou.xml'}
VCLASS = {'liviano': 'passenger', 'pesado': 'bus', 'carrito': 'bus'}
# tramos de la red base -> tramos de la propuesta (a nivel) y recorrido por el puente de los livianos que siguen derecho
NIVEL = {'FA_3': ['FA_3_antes', 'FA_3'], 'fuerzas_armadas_entrada': ['fuerzas_armadas_entrada_nivel', 'fuerzas_armadas_entrada'],
         'FA_2': ['FA_2', 'FA_2_despues']}
PUENTE = {('FA_3', 'fuerzas_armadas_entrada'): (['FA_3_antes', 'puente_subida_hacia_sur', 'puente_hacia_sur',
                                                 'puente_bajada_hacia_sur', 'fuerzas_armadas_entrada'], 'FA_3'),
          ('FA_1', 'FA_2'): (['puente_subida_hacia_norte', 'puente_hacia_norte', 'puente_bajada_hacia_norte',
                              'FA_2_despues'], 'bifurcacion_FA_perrokero')}


def rehacer(edges, vclass):
    ruta, i = [], 0
    while i < len(edges):
        par = tuple(edges[i:i + 2])
        if vclass == 'passenger' and par in PUENTE:
            tramos, previo = PUENTE[par]
            if previo != par[0]:          # sentido sur -> norte: el puente sale antes de la bifurcacion
                ruta.pop()
            ruta.extend(tramos)
            i += 2
            continue
        if edges[i] == 'fuerzas_armadas_entrada' and i == 0:
            raise RuntimeError('ruta que empieza en fuerzas_armadas_entrada')
        ruta.extend(NIVEL.get(edges[i], [edges[i]]))
        i += 1
    return ruta


def revisar(net, ruta, vclass, rid):
    for a, b in zip(ruta, ruta[1:]):
        if net.getEdge(b) not in net.getEdge(a).getAllowedOutgoing(vclass):
            raise RuntimeError(f'{rid} ({vclass}): {a} no conecta con {b}')


def main():
    net = sumolib.net.readNet(RED)
    for entrada, salida in ARCHIVOS.items():
        raiz = ET.parse(os.path.join(DEMANDA, entrada)).getroot()
        rutas = {r.get('id'): r.get('edges').split() for r in raiz.iter('route')}
        tipo_ruta = {f.get('route'): f.get('type') for f in raiz.iter('flow')}
        nuevas = {}
        for rid, edges in rutas.items():
            vc = VCLASS[tipo_ruta.get(rid, 'liviano')]
            nuevas[rid] = rehacer(edges, vc)
            revisar(net, nuevas[rid], vc, rid)
        por_puente = {rid for rid, r in nuevas.items() if any(e.startswith('puente_') for e in r)}
        tasa = {f.get('route'): float(re.fullmatch(r'exp\((.*)\)', f.get('period')).group(1)) * 3600 for f in raiz.iter('flow')}
        lineas = ['<?xml version="1.0" encoding="UTF-8"?>',
                  f'<!-- Generado por herramientas/demanda_propuesta.py a partir de {entrada}: misma demanda de la base, rutas sobre '
                  'la red con el puente de Perrokero (livianos que siguen derecho por FFAA por el puente). No editar a mano. -->',
                  '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                  'xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">']
        lineas += [f'    <route id="{rid}" edges="{" ".join(nuevas[rid])}"/>' for rid in rutas]
        lineas += ['    <flow ' + ' '.join(f'{k}="{v}"' for k, v in f.attrib.items()) + '/>' for f in raiz.iter('flow')]
        lineas.append('</routes>')
        with open(os.path.join(DEMANDA, salida), 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(lineas) + '\n')
        for sentido, tramo in (('hacia el sur', 'puente_hacia_sur'), ('hacia Camino Real', 'puente_hacia_norte')):
            v = sum(tasa.get(r, 0) for r in por_puente if tramo in nuevas[r])
            print(f'{salida}: puente {sentido} {v:.0f} veh/h')


if __name__ == '__main__':
    main()
