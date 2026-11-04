"""Propuesta Assouad y Peroza (2022), Alternativa C: puente sobre la Av. Fuerzas Armadas en Perrokero.

Se aplica sobre la red plana de main (act.*, exportada con netconvert --plain-output-prefix act) y deja mod.*:
- puente de 100 m (cap. V, 5.6 y figuras, imp. 168-170): rampa de 40 m al 15 % + tablero de 20 m a 6,00 m + rampa de
  40 m, centrado en el cruce; 1 carril de 3,70 m por sentido. Solo livianos (los pesados y los carritos, clase bus, a nivel).
- a nivel queda 1 carril por sentido en FFAA (el derecho), como en la figura "Ubicacion del puente": el carril
  izquierdo de campo es el que sube al puente, asi la seccion sigue teniendo 2 carriles por sentido.
- semaforo de 120 s bajo el puente (Cuadro "Ciclo de semaforizacion", imp. 157): una fase por acceso,
  Norte 33, Oeste 20, Sur 25 y Este 30 s de verde + 3 s de amarillo, sin todo rojo.
Uso (en una carpeta de trabajo con act.*):  python propuesta_perozo.py <costanera.net.xml de main>
"""
import math
import os
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.environ.get('SUMO_HOME', r'C:\SUMO'), 'tools'))
import sumolib  # noqa: E402

net = sumolib.net.readNet(sys.argv[1])
tn, tE, tC = (ET.parse(f'act.{x}.xml') for x in ('nod', 'edg', 'con'))
N, E, C = tn.getroot(), tE.getroot(), tC.getroot()
nodos = {n.get('id'): n for n in N.findall('node')}
edges = {e.get('id'): e for e in E.findall('edge')}
CRUCE = 'interseccion_avrio_FA'
CX, CY = net.getNode(CRUCE).getCoord()
H, RAMPA, TABLERO = 6.0, 40.0, 20.0
INICIO = TABLERO / 2 + RAMPA   # la rampa empieza a 50 m del centro del cruce
MARGEN = 8.0                   # los carriles se separan 8 m antes del pie de la rampa (asi el cruce de netconvert no corta la rampa)
ANCHO_PUENTE, VEL = 3.70, 11.11
SOLO_LIVIANOS = 'passenger private taxi evehicle'


def geom(eid):
    e = edges[eid]
    if e.get('shape'):
        return [tuple(map(float, p.split(',')))[:2] for p in e.get('shape').split()]
    a, b = nodos[e.get('from')], nodos[e.get('to')]
    return [(float(a.get('x')), float(a.get('y'))), (float(b.get('x')), float(b.get('y')))]


def acumulado(P):
    L = [0.0]
    for a, b in zip(P, P[1:]):
        L.append(L[-1] + math.dist(a, b))
    return L


def punto(P, s):
    L = acumulado(P)
    for i in range(len(P) - 1):
        if L[i + 1] >= s or i == len(P) - 2:
            t = 0 if L[i + 1] == L[i] else (s - L[i]) / (L[i + 1] - L[i])
            return (P[i][0] + t * (P[i + 1][0] - P[i][0]), P[i][1] + t * (P[i + 1][1] - P[i][1]))


def corte(P, a, b):
    L = acumulado(P)
    return [punto(P, a)] + [p for p, s in zip(P, L) if a < s < b] + [punto(P, b)]


def desplazar(P, d):
    """polilinea paralela a d m a la derecha del sentido de circulacion"""
    Q = []
    for i, p in enumerate(P):
        a, b = P[max(i - 1, 0)], P[min(i + 1, len(P) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        Q.append((p[0] + d * dy / n, p[1] - d * dx / n))
    return Q


def s_a_distancia(P, dist, desde_final=False):
    """abscisa de P donde la distancia en linea recta al centro del cruce es dist"""
    L = acumulado(P)[-1]
    ss = [i * 0.05 for i in range(int(L / 0.05) + 1)]
    if desde_final:
        ss = ss[::-1]
    for s in ss:
        if math.dist(punto(P, s), (CX, CY)) <= dist:
            return s
    raise RuntimeError('no se alcanza la distancia')


def texto(P, z=None):
    return ' '.join(f'{x:.2f},{y:.2f}' + (f',{z(i):.2f}' if z else '') for i, (x, y) in enumerate(P))


def nodo_nuevo(nid, x, y, z=None):
    n = ET.SubElement(N, 'node', id=nid, x=f'{x:.2f}', y=f'{y:.2f}', type='priority')
    if z:
        n.set('z', f'{z:.2f}')
    nodos[nid] = n


def tramo(eid, f, t, P, base=None, carriles=None, z=None, **extra):
    """crea (o rehace) un tramo; base = tramo del que copia atributos"""
    e = edges.get(eid)
    if e is None:
        e = ET.SubElement(E, 'edge', {k: v for k, v in edges[base].attrib.items() if k not in ('id', 'shape')})
        e.set('id', eid)
        edges[eid] = e
    e.set('from', f)
    e.set('to', t)
    e.set('shape', texto(P, z))
    if carriles:
        e.set('numLanes', str(carriles))
        for ln in e.findall('lane'):
            e.remove(ln)
    for k, v in extra.items():
        e.set(k, v)
    return e


# desplazamiento de los centros de carril respecto a la forma de cada tramo (+ = a la derecha del sentido):
# spreadType "right" (FA_2, FA_3): la forma es el eje entre sentidos; "center": la forma es el centro del tramo
w = 3.92
DESPL = {'right': {'izq': w / 2, 'der': 1.5 * w}, 'center': {'izq': -w / 2, 'der': w / 2}}


def carril(eid, cual):
    return desplazar(geom(eid), DESPL[edges[eid].get('spreadType', 'right')][cual])


# ------------------------------------------------------------------ partir los tramos de FFAA a 50 m del cruce
P3 = geom('FA_3')
a3 = s_a_distancia(P3, INICIO + MARGEN)
nodo_nuevo('perozo_rampa_norte', *punto(P3, a3))
P2 = geom('FA_2')
a2 = s_a_distancia(P2, INICIO + MARGEN, desde_final=True)
nodo_nuevo('perozo_bajada_norte', *punto(P2, a2))
Pe = geom('fuerzas_armadas_entrada')
ae = s_a_distancia(Pe, INICIO + MARGEN, desde_final=True)
nodo_nuevo('perozo_bajada_sur', *punto(Pe, ae))

izq3, der3 = carril('FA_3', 'izq'), carril('FA_3', 'der')
izq2, der2 = carril('FA_2', 'izq'), carril('FA_2', 'der')
izqe, dere = carril('fuerzas_armadas_entrada', 'izq'), carril('fuerzas_armadas_entrada', 'der')
izq1, der1 = carril('FA_1', 'izq'), carril('FA_1', 'der')
izqb, derb = carril('bifurcacion_FA_perrokero', 'izq'), carril('bifurcacion_FA_perrokero', 'der')
L3, L2, Le = acumulado(P3)[-1], acumulado(P2)[-1], acumulado(Pe)[-1]

# sentido norte -> sur (desde Camino Real)
tramo('FA_3_antes', '7756816786', 'perozo_rampa_norte', corte(P3, 0, a3), base='FA_3')
tramo('FA_3', 'perozo_rampa_norte', CRUCE, corte(der3, a3, L3), carriles=1, spreadType='center')
tramo('fuerzas_armadas_entrada_nivel', CRUCE, 'perozo_bajada_sur', corte(dere, 0, ae), base='fuerzas_armadas_entrada',
      carriles=1)
tramo('fuerzas_armadas_entrada', 'perozo_bajada_sur', '1835291683', corte(Pe, ae, Le))
# sentido sur -> norte: la bifurcacion hacia la Av. Rio (nodo 8424094388, ~69 m del centro) es un cruce grande que
# recortaria el pie de la rampa; el carril izquierdo se separa un nodo antes (11353318191, ~75 m) y sigue a nivel
# hasta los 50 m, donde empieza a subir. A nivel siguen la bifurcacion y FA_1 con 1 carril (el derecho).
tramo('FA_2_despues', 'perozo_bajada_norte', '7756816786', corte(P2, a2, L2), base='FA_2')
tramo('bifurcacion_FA_perrokero', '11353318191', '8424094388', derb, carriles=1)
tramo('FA_1', '8424094388', CRUCE, der1, carriles=1)
tramo('FA_2', CRUCE, 'perozo_bajada_norte', corte(der2, 0, a2), carriles=1, spreadType='center')


# ------------------------------------------------------------------ puente (eje = carril izquierdo de campo)
def puente(nombre, eje, inicio, fin):
    """eje: polilinea del carril izquierdo; inicio/fin: nodos a nivel donde sale y llega"""
    Lx = acumulado(eje)[-1]
    sc = min((math.dist(punto(eje, s), (CX, CY)), s) for s in [i * 0.05 for i in range(int(Lx / 0.05))])[1]
    s1, s2 = sc - TABLERO / 2, sc + TABLERO / 2
    s0, s3 = max(0.0, s1 - RAMPA), min(Lx, s2 + RAMPA)

    def cota(s):
        if s <= s0 or s >= s3:
            return 0.0
        return min(H, H * (s - s0) / (s1 - s0), H * (s3 - s) / (s3 - s2))

    def con_cota(a, b):
        P = corte(eje, a, b)
        ss = [a] + [s for s in acumulado(eje) if a < s < b] + [b]
        quiebres = sorted(set(ss + [q for q in (s0, s1, s2, s3) if a < q < b]))
        P = [punto(eje, s) for s in quiebres]
        return P, (lambda i: cota(quiebres[i]))

    nodo_nuevo(f'perozo_tablero_{nombre}_1', *punto(eje, s1), H)
    nodo_nuevo(f'perozo_tablero_{nombre}_2', *punto(eje, s2), H)
    attrs = dict(numLanes='1', speed=f'{VEL:.2f}', width=f'{ANCHO_PUENTE:.2f}', spreadType='center',
                 allow=SOLO_LIVIANOS, priority='10', type='highway.tertiary')
    for eid, f, t, a, b in [(f'puente_subida_hacia_{nombre}', inicio, f'perozo_tablero_{nombre}_1', 0, s1),
                            (f'puente_hacia_{nombre}', f'perozo_tablero_{nombre}_1', f'perozo_tablero_{nombre}_2', s1, s2),
                            (f'puente_bajada_hacia_{nombre}', f'perozo_tablero_{nombre}_2', fin, s2, Lx)]:
        P, z = con_cota(a, b)
        e = ET.SubElement(E, 'edge', id=eid, **{'from': f, 'to': t}, **attrs)
        e.set('shape', texto(P, z))
        edges[eid] = e
    return s0, s1, s2, s3, Lx


# FFAA es recta en Perrokero: el eje del puente es la recta entre los puntos donde sale y llega el carril izquierdo
eje_sur = [punto(izq3, a3), punto(izqe, ae)]
eje_norte = [izqb[0], punto(izq2, a2)]
r_sur = puente('sur', eje_sur, 'perozo_rampa_norte', 'perozo_bajada_sur')
r_norte = puente('norte', eje_norte, '11353318191', 'perozo_bajada_norte')

# ------------------------------------------------------------------ conexiones
DESDE = {'FA_1', 'FA_3', 'bifurcacion_FA_perrokero'}
HACIA = {'FA_1', 'FA_2', 'fuerzas_armadas_entrada', 'bifurcacion_FA_perrokero'}
for c in list(C):
    f, t = c.get('from'), c.get('to')
    if f == 'FA_2':                                     # salidas en 7756816786: ahora desde FA_2_despues
        c.set('from', 'FA_2_despues')
    elif t == 'FA_3' and f != 'FA_2':                   # entradas en 7756816786: ahora hacia FA_3_antes
        c.set('to', 'FA_3_antes')
    elif f == 'fuerzas_armadas_entrada':                # el tramo final conserva el id y sus salidas
        continue
    elif f in DESDE or t in HACIA:
        C.remove(c)


def con(f, t, fl, tl, **extra):
    ET.SubElement(C, 'connection', {'from': f, 'to': t, 'fromLane': str(fl), 'toLane': str(tl), **extra})


for f, t, fl, tl in [
        ('FA_3_antes', 'FA_3', 0, 0), ('FA_3_antes', 'puente_subida_hacia_sur', 1, 0),
        ('puente_subida_hacia_sur', 'puente_hacia_sur', 0, 0), ('puente_hacia_sur', 'puente_bajada_hacia_sur', 0, 0),
        ('fuerzas_armadas_entrada_nivel', 'fuerzas_armadas_entrada', 0, 0),
        ('puente_bajada_hacia_sur', 'fuerzas_armadas_entrada', 0, 1),
        ('bifurcacion_FA_perrokero', '172682274', 0, 0), ('bifurcacion_FA_perrokero', 'FA_1', 0, 0),
        ('fuerzas_armadas_salida', 'bifurcacion_FA_perrokero', 0, 0), ('-1223999765#0', 'bifurcacion_FA_perrokero', 0, 0),
        ('fuerzas_armadas_salida', 'puente_subida_hacia_norte', 1, 0),
        ('puente_subida_hacia_norte', 'puente_hacia_norte', 0, 0), ('puente_hacia_norte', 'puente_bajada_hacia_norte', 0, 0),
        ('FA_2', 'FA_2_despues', 0, 0), ('puente_bajada_hacia_norte', 'FA_2_despues', 0, 1)]:
    con(f, t, fl, tl)
# bajo el puente (1 carril de FFAA por sentido): todos los movimientos salen del carril que queda a nivel.
# Los enlaces se numeran por acceso, en el orden de las fases de la tesis: Norte, Oeste, Sur y Este.
ACCESOS = [  # (acceso, tramo, verde s, enlaces)
    ('Norte', 'FA_3', 33, [('res_entrada', 0, 0), ('fuerzas_armadas_entrada_nivel', 0, 0), ('avrio_2', 0, 1)]),
    ('Oeste (Residencias)', 'res_salida', 20, [('fuerzas_armadas_entrada_nivel', 0, 0), ('avrio_2', 0, 0),
                                               ('avrio_2', 1, 1), ('FA_2', 1, 0)]),
    ('Sur', 'FA_1', 25, [('FA_2', 0, 0), ('res_entrada', 0, 1)]),
    ('Este (Av. Rio)', 'avrio_1', 30, [('FA_2', 0, 0), ('res_entrada', 0, 0), ('res_entrada', 1, 1),
                                        ('fuerzas_armadas_entrada_nivel', 1, 0)])]
AMARILLO = 3
nodos[CRUCE].set('type', 'traffic_light')
nodos[CRUCE].set('tl', CRUCE)
T = ET.parse('act.tll.xml').getroot()
for x in [x for x in T if x.get('id') == CRUCE or x.get('tl') == CRUCE]:
    T.remove(x)
logica = ET.SubElement(T, 'tlLogic', id=CRUCE, type='static', programID='0', offset='0')
total = sum(len(enl) for *_, enl in ACCESOS)
i = 0
for k, (_, f, verde, enl) in enumerate(ACCESOS):
    for t, fl, tl in enl:
        con(f, t, fl, tl, keepClear='0')
        ET.SubElement(T, 'connection', {'from': f, 'to': t, 'fromLane': str(fl), 'toLane': str(tl), 'tl': CRUCE,
                                        'linkIndex': str(i + enl.index((t, fl, tl)))})
    for dur, c in ((verde, 'G'), (AMARILLO, 'y')):
        ET.SubElement(logica, 'phase', duration=str(dur), state='r' * i + c * len(enl) + 'r' * (total - i - len(enl)))
    i += len(enl)
print(f'semaforo de Perrokero: ciclo de {sum(v + AMARILLO for _, _, v, _ in ACCESOS)} s')

ET.ElementTree(T).write('mod.tll.xml', encoding='UTF-8', xml_declaration=True)
for t, nombre in ((tn, 'nod'), (tE, 'edg'), (tC, 'con')):
    t.write(f'mod.{nombre}.xml', encoding='UTF-8', xml_declaration=True)
for nombre, (s0, s1, s2, s3, Lx) in (('hacia el sur', r_sur), ('hacia el norte', r_norte)):
    print(f'puente {nombre}: eje de {Lx:.1f} m; rampa {s0:.1f}-{s1:.1f} m ({H / (s1 - s0):.1%}), '
          f'tablero {s1:.1f}-{s2:.1f} m, rampa {s2:.1f}-{s3:.1f} m ({H / (s3 - s2):.1%})')
