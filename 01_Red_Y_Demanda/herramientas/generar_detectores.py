"""
Genera detectores_intersecciones.add.xml y demanda/../accesos_intersecciones.csv.

- Un detector E3 (entrada/salida) por interseccion: entradas a ~300 m aguas arriba de cada acceso
  (sin cruzar otra interseccion principal) y salidas a ~60 m aguas abajo. Mide la demora de control
  (timeLoss) de todos los vehiculos que atraviesan la interseccion.
- Un edgeData sobre los tramos de cada acceso: permite calcular la demora por acceso.
Ambos se agregan cada 900 s (15 min) para obtener tambien el FHMD.

Uso: python generar_detectores.py   (volver a ejecutarlo solo si cambia la red)
"""
import csv
import os
import sys

SUMO_HOME = os.environ.get('SUMO_HOME', r'C:\SUMO')
sys.path.insert(0, os.path.join(SUMO_HOME, 'tools'))
import sumolib  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
RED = os.path.join(AQUI, '..', 'costanera.net.xml')
SALIDA = os.path.join(AQUI, '..', 'detectores_intersecciones.add.xml')
MAPA = os.path.join(AQUI, '..', 'accesos_intersecciones.csv')

INTERSECCIONES = {
    'semaforo_caminoreal': 'Camino Real',
    'semaforo_costanera': 'CC Paos',
    'interseccion_avrio_FA': 'Perrokero',
    'interseccion_bissau': 'Bissau',
    'interseccion_puerto_guaica': 'Puerto Guaica',
}
ACCESOS = {
    'semaforo_caminoreal_FA': 'Sur (FFAA)', 'semaforo_caminoreal_costanera': 'Norte (Costanera)',
    'semaforo_caminoreal_elejercito': 'Oeste (El Ejercito)', 'av_proyeccion_salida': 'Este (Av. Proyeccion)',
    'lecheria_haciacaminoreal': 'Este (Lecheria)', 'madre_vieja_salida': 'Norte (Madre Vieja)',
    'costanera_haciamadrevieja': 'Sur (Costanera)',
    'FA_1': 'Sur (FFAA)', 'FA_3': 'Norte (desde Camino Real)', 'avrio_1': 'Este (Av. Rio)',
    'res_salida': 'Oeste (Residencias)',
    'costanera_bissau_hacialecheria': 'Costanera sentido Lecheria',
    'costanera_bissau_haciacaminoreal': 'Costanera sentido Camino Real',
    'salida_bissau_1': 'Salida Bissau (residencias/CC)', 'salida_bissau_2': 'Salida Bissau (galpones)',
    'costanera_puerto_guaica_hacialecheria': 'Costanera sentido Lecheria',
    'costanera_puerto_guaica_haciacaminoreal': 'Costanera sentido Camino Real',
    'salida:puerto_guaica': 'Salida Puerto Guaica', '-335982664#1': 'Salida Fernandez Padilla',
}
# Propuesta Savignani: los vehiculos que cruzan Camino Real por el distribuidor (puente) salen del detector al bajar
# del puente, asi su demora tambien cuenta en la interseccion.
SALIDAS_EXTRA = {'semaforo_caminoreal': ['puente_bajada_hacia_ffaa', 'puente_bajada_hacia_costanera']}
# Tramo anterior fijado a mano donde la geometria engana al criterio de "seguir derecho" (la Costanera llega al
# distribuidor girando a la izquierda y la calle local de enfrente queda como "recta").
ANTERIOR_FORZADO = {'costanera_hacia_distribuidor': '592256719#7'}
SECUNDARIOS = {'avrio_1', 'res_salida', 'salida_bissau_1', 'salida_bissau_2', 'salida:puerto_guaica', '-335982664#1'}
AGUAS_ARRIBA, AGUAS_ABAJO, PERIODO = 300.0, 60.0, 900


def es_fuente(e):
    return not [p for p in e.getFromNode().getIncoming()
                if p.getFunction() != 'internal' and p.getFromNode() != e.getToNode()]


def aguas_arriba(net, edge):
    cadena, dist = [edge], edge.getLength()
    while dist < AGUAS_ARRIBA:
        nodo = cadena[-1].getFromNode()
        if nodo.getID() in INTERSECCIONES or nodo.getType() == 'traffic_light':
            break
        entrantes = [e for e in nodo.getIncoming()
                     if e.getFunction() != 'internal' and e.getFromNode() != cadena[-1].getToNode()]
        rectos = [e for e in entrantes if any(c.getDirection() == 's' for c in e.getConnections(cadena[-1]))]
        cand = rectos if rectos else (entrantes if len(entrantes) == 1 else [])
        forzado = ANTERIOR_FORZADO.get(cadena[-1].getID())
        if forzado and net.hasEdge(forzado):
            cand = [net.getEdge(forzado)]
        if not cand:
            break
        sig = max(cand, key=lambda e: (e.getLaneNumber(), e.getPriority()))
        if sig in cadena:
            break
        cadena.append(sig)
        dist += sig.getLength()
        if es_fuente(sig):
            break
    primero = cadena[-1]
    pos = dist - AGUAS_ARRIBA if dist > AGUAS_ARRIBA else 0.1
    if es_fuente(primero):
        # los vehiculos se insertan al inicio de este tramo: la entrada va despues del punto de insercion
        pos = max(pos, min(15.0, primero.getLength() / 2))
    return cadena, primero, min(max(pos, 0.1), primero.getLength() - 0.1)


def aguas_abajo(edge):
    cadena, dist = [edge], edge.getLength()
    while dist < AGUAS_ABAJO:
        nodo = cadena[-1].getToNode()
        salientes = [e for e in nodo.getOutgoing()
                     if e.getFunction() != 'internal' and e.getToNode() != cadena[-1].getFromNode()]
        if len(salientes) != 1 or nodo.getID() in INTERSECCIONES or nodo.getType() == 'traffic_light':
            break
        cadena.append(salientes[0])
        dist += salientes[0].getLength()
    ultimo = cadena[-1]
    pos = ultimo.getLength() - (dist - AGUAS_ABAJO) if dist > AGUAS_ABAJO else ultimo.getLength() - 0.1
    return ultimo, min(max(pos, 0.1), ultimo.getLength() - 0.1)


def main():
    net = sumolib.net.readNet(RED, withInternal=False)
    lineas = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<!-- Generado por herramientas/generar_detectores.py. Volver a generar si cambia la red. -->',
              '<additional>']
    tramos_acceso = []
    filas = []
    for jid, nombre in INTERSECCIONES.items():
        nodo = net.getNode(jid)
        # solo accesos con algun movimiento permitido (descarta tramos sin conexiones)
        entrantes = [e for e in nodo.getIncoming()
                     if e.getFunction() != 'internal' and any(o.getFromNode() == nodo for o in e.getOutgoing())]
        salientes = [e for e in nodo.getOutgoing() if e.getFunction() != 'internal']
        salientes += [net.getEdge(i) for i in SALIDAS_EXTRA.get(jid, []) if net.hasEdge(i)]
        lineas.append(f'    <e3Detector id="e3_{nombre.replace(" ", "_")}" file="../02_Resultados_Base/reporte_intersecciones.xml" '
                      f'period="{PERIODO}" timeThreshold="2" speedThreshold="1.39">')
        for e in entrantes:
            cadena, primero, pos = aguas_arriba(net, e)
            for ln in primero.getLanes():
                lineas.append(f'        <detEntry lane="{ln.getID()}" pos="{pos:.2f}" friendlyPos="true"/>')
            tramos_acceso.extend(c.getID() for c in cadena)
            filas.append([nombre, ACCESOS.get(e.getID(), e.getID()), 'secundario' if e.getID() in SECUNDARIOS else 'principal',
                          e.getID(), ' '.join(c.getID() for c in cadena), f'{min(sum(c.getLength() for c in cadena), AGUAS_ARRIBA):.0f}'])
        for o in salientes:
            ultimo, pos = aguas_abajo(o)
            for ln in ultimo.getLanes():
                lineas.append(f'        <detExit lane="{ln.getID()}" pos="{pos:.2f}" friendlyPos="true"/>')
        lineas.append('    </e3Detector>')
    lineas.append(f'    <edgeData id="accesos" file="../02_Resultados_Base/reporte_accesos.xml" freq="{PERIODO}" '
                  f'edges="{" ".join(sorted(set(tramos_acceso)))}"/>')
    lineas.append('</additional>')
    with open(SALIDA, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas) + '\n')
    # misma configuracion para el horizonte 2041, con sus resultados en su propia carpeta
    with open(SALIDA.replace('.add.xml', '_2041.add.xml'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas).replace('../02_Resultados_Base/', '../02_Resultados_2041/') + '\n')
    with open(MAPA, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['interseccion', 'acceso', 'tipo', 'tramo_final', 'tramos_del_acceso', 'longitud_m'])
        w.writerows(filas)
    for fila in filas:
        print(f'{fila[0]:14s} {fila[1]:34s} {fila[2]:10s} {fila[5]:>4s} m  ({len(fila[4].split())} tramos)')


if __name__ == '__main__':
    main()
