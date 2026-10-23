"""Fase 2 de la propuesta Savignani sobre la red plana actual (act.*) -> mod.*
- perfil del puente segun la tesis (rasante 7,4 m, rampas de 60 m al 12,3 %, tablero de 30 m centrado en el cruce)
- anchos de FFAA a nivel (3,75 m, Anexo G)
- bahias de bus (Bissau y Puerto Guaica 30 m + cunas de 20 m; Fernandez Padilla 20 m + cunas de 15 m), carril 2,5 m
- carriles de salida e incorporacion de Bissau (3 m x 50 m)
- semaforo de Camino Real: 4 fases del usuario (ciclo 122 s), una por acceso
"""
import math
import xml.etree.ElementTree as ET

tn, tE, tC, tT = (ET.parse(f'act.{x}.xml') for x in ('nod', 'edg', 'con', 'tll'))
N, E, C, T = tn.getroot(), tE.getroot(), tC.getroot(), tT.getroot()
nodos = {n.get('id'): n for n in N.findall('node')}
edges = {e.get('id'): e for e in E.findall('edge')}
TL = 'cluster_13002069148_2322602638_2322679769_3753399808_#2more'


def xy(nid):
    n = nodos[nid]
    return (float(n.get('x')), float(n.get('y')))


def geom(e):
    if e.get('shape'):
        return [tuple(map(float, p.split(',')))[:2] for p in e.get('shape').split()]
    return [xy(e.get('from')), xy(e.get('to'))]


def acumulado(P):
    L = [0.0]
    for a, b in zip(P, P[1:]):
        L.append(L[-1] + math.dist(a, b))
    return L


def punto(P, L, s):
    for i in range(len(P) - 1):
        if L[i + 1] >= s or i == len(P) - 2:
            t = 0 if L[i + 1] == L[i] else (s - L[i]) / (L[i + 1] - L[i])
            return (P[i][0] + t * (P[i + 1][0] - P[i][0]), P[i][1] + t * (P[i + 1][1] - P[i][1]))


def corte(P, a, b, z=None):
    """subpolilinea entre las distancias a y b; z(s) opcional da la cota de cada punto"""
    L = acumulado(P)
    ss = [a] + [s for s in L if a < s < b] + [b]
    if z:
        extra = [s for s in z.quiebres if a < s < b]
        ss = sorted(set(ss + extra))
    pts = []
    for s in ss:
        x, y = punto(P, L, s)
        pts.append(f'{x:.2f},{y:.2f}' + (f',{z(s):.2f}' if z else ''))
    return ' '.join(pts)


def nodo_nuevo(nid, x, y, z=None, tipo='priority'):
    n = ET.SubElement(N, 'node', id=nid, x=f'{x:.2f}', y=f'{y:.2f}', type=tipo)
    if z is not None:
        n.set('z', f'{z:.2f}')
    nodos[nid] = n


def quitar_con(ids):
    for c in list(C):
        if c.get('from') in ids or c.get('to') in ids:
            C.remove(c)


def con(f, t, fl, tl):
    ET.SubElement(C, 'connection', {'from': f, 'to': t, 'fromLane': str(fl), 'toLane': str(tl)})


# ------------------------------------------------------------------ puente
P = geom(edges['puente_subida_hacia_ffaa']) + [xy('puente_centro'), xy('puente_apoyo_1')] + geom(edges['puente_bajada_hacia_ffaa'])
P = [P[0], P[1], P[2], P[3], P[4], P[5]] if len(P) == 6 else P
Lp = acumulado(P)[-1]
# distancia del cruce (centro del semaforo a nivel) sobre el eje del puente
cx, cy = xy('semaforo_caminoreal')
best = min(((math.dist(punto(P, acumulado(P), s), (cx, cy)), s) for s in [i * 0.1 for i in range(int(Lp * 10))]))
S_CRUCE = best[1]
H, RAMPA, TABLERO = 7.4, 60.0, 30.0
s1, s2 = S_CRUCE - TABLERO / 2 - RAMPA, S_CRUCE - TABLERO / 2
s3, s4 = S_CRUCE + TABLERO / 2, S_CRUCE + TABLERO / 2 + RAMPA
assert s1 >= 0 and s4 <= Lp, (s1, s4, Lp)


def cota(s):
    if s <= s1 or s >= s4:
        return 0.0
    if s < s2:
        return H * (s - s1) / RAMPA
    if s <= s3:
        return H
    return H * (s4 - s) / RAMPA


cota.quiebres = [s1, s2, s3, s4]
for nid in ('puente_apoyo_1', 'puente_apoyo_2', 'puente_apoyo_3', 'puente_centro'):
    N.remove(nodos.pop(nid))
viejos = ['puente_hacia_ffaa_1', 'puente_hacia_ffaa_2', 'puente_hacia_ffaa_3',
          'puente_hacia_costanera_1', 'puente_hacia_costanera_2', 'puente_hacia_costanera_3']
for i in viejos:
    E.remove(edges.pop(i))
quitar_con(set(viejos) | {'puente_subida_hacia_ffaa', 'puente_bajada_hacia_ffaa',
                          'puente_subida_hacia_costanera', 'puente_bajada_hacia_costanera'})
nodo_nuevo('puente_tablero_lado_costanera', *punto(P, acumulado(P), s2), H)
nodo_nuevo('puente_tablero_lado_ffaa', *punto(P, acumulado(P), s3), H)
R = P[::-1]
cota_r = lambda s: cota(Lp - s)  # noqa: E731
cota_r.quiebres = [Lp - q for q in cota.quiebres]
plantilla = edges['puente_bajada_hacia_ffaa']


def tramo_puente(eid, f, t, shape):
    e = edges.get(eid)
    if e is None:
        e = ET.SubElement(E, 'edge', {k: v for k, v in plantilla.attrib.items() if k not in ('id', 'from', 'to', 'shape')})
        e.set('id', eid)
        edges[eid] = e
    e.set('from', f)
    e.set('to', t)
    e.set('shape', shape)


tramo_puente('puente_subida_hacia_ffaa', 'distribuidor_lado_costanera', 'puente_tablero_lado_costanera', corte(P, 0, s2, cota))
tramo_puente('puente_hacia_ffaa', 'puente_tablero_lado_costanera', 'puente_tablero_lado_ffaa', corte(P, s2, s3, cota))
tramo_puente('puente_bajada_hacia_ffaa', 'puente_tablero_lado_ffaa', 'distribuidor_lado_ffaa', corte(P, s3, Lp, cota))
tramo_puente('puente_subida_hacia_costanera', 'distribuidor_lado_ffaa', 'puente_tablero_lado_ffaa', corte(R, 0, Lp - s3, cota_r))
tramo_puente('puente_hacia_costanera', 'puente_tablero_lado_ffaa', 'puente_tablero_lado_costanera', corte(R, Lp - s3, Lp - s2, cota_r))
tramo_puente('puente_bajada_hacia_costanera', 'puente_tablero_lado_costanera', 'distribuidor_lado_costanera', corte(R, Lp - s2, Lp, cota_r))
for a, b in [('puente_subida_hacia_ffaa', 'puente_hacia_ffaa'), ('puente_hacia_ffaa', 'puente_bajada_hacia_ffaa'),
             ('puente_subida_hacia_costanera', 'puente_hacia_costanera'), ('puente_hacia_costanera', 'puente_bajada_hacia_costanera')]:
    con(a, b, 0, 0)
# conexiones de entrada y salida del puente (estaban en los tramos que se conservan con el mismo id)
_, C0 = None, ET.parse('act.con.xml').getroot()
for c in C0.findall('connection'):
    f, t = c.get('from'), c.get('to')
    if (t in ('puente_subida_hacia_ffaa', 'puente_subida_hacia_costanera') and f not in viejos) or \
            (f in ('puente_bajada_hacia_ffaa', 'puente_bajada_hacia_costanera') and t not in viejos):
        C.append(c)

# ------------------------------------------------------------------ anchos FFAA a nivel (Anexo G: 3,75 m)
for i in ('ffaa_hacia_semaforo', 'semaforo_caminoreal_FA', 'semaforocaminorea_haciaperrokero'):
    edges[i].set('width', '3.75')


# ------------------------------------------------------------------ bahias y carriles auxiliares
def dividir(eid, tramos):
    """tramos: [(fin_m, id, carril_extra)] en orden; carril_extra = None o (ancho, allow). El primero conserva el id."""
    e = edges[eid]
    Pg = geom(e)
    Lg = acumulado(Pg)[-1]
    inicio, desde = 0.0, e.get('from')
    hasta_final = e.get('to')
    E.remove(e)
    del edges[eid]
    for k, (fin, nid, extra) in enumerate(tramos):
        fin = Lg if fin is None else fin
        hasta = hasta_final if k == len(tramos) - 1 else f'{eid}_km{fin:.0f}'
        if hasta not in nodos:
            nodo_nuevo(hasta, *punto(Pg, acumulado(Pg), fin))
        s = ET.SubElement(E, 'edge', {a: v for a, v in e.attrib.items() if a not in ('id', 'from', 'to', 'shape')})
        s.set('id', nid)
        s.set('from', desde)
        s.set('to', hasta)
        s.set('shape', corte(Pg, inicio, fin))
        n0 = int(e.get('numLanes'))
        dx = 1 if extra else 0
        s.set('numLanes', str(n0 + dx))
        for ln in e.findall('lane'):
            l2 = ET.SubElement(s, 'lane', dict(ln.attrib))
            l2.set('index', str(int(ln.get('index')) + dx))
        if extra:
            ancho, allow = extra
            l0 = ET.SubElement(s, 'lane', index='0', width=f'{ancho:.2f}')
            vel = next((ln.get('speed') for ln in e.findall('lane') if ln.get('speed')), None)
            if vel:
                l0.set('speed', vel)
            if allow:
                l0.set('allow', allow)
            s[:] = sorted(s, key=lambda x: int(x.get('index')))
        edges[nid] = s
        inicio, desde = fin, hasta


BAHIA, AUX = (2.5, 'bus'), (3.0, None)
MOD = ['172344969#4', '172344969#5', '172344969#6', 'costanera_bissau_hacialecheria', '172344969#9', '592256719#7']
quitar_con(set(MOD))
L4 = acumulado(geom(edges['172344969#4']))[-1]
# Puerto Guaica (sentido Lecheria): bahia de 20 + 30 + 20 m a 10 m del acceso; al final, inicio del carril de salida de Bissau
dividir('172344969#4', [(10, '172344969#4', None), (80, '172344969#4_bahia', BAHIA),
                        (L4 - 18, '172344969#4_b', None), (None, '172344969#4_salida_bissau', AUX)])
# carril de salida de Bissau (18 m mas para compensar lo que ocupan los cruces): ultimos 18 m de 172344969#4 + 172344969#5 + 172344969#6 + costanera_bissau_hacialecheria = 50 m
dividir('172344969#5', [(None, '172344969#5', AUX)])
dividir('172344969#6', [(None, '172344969#6', AUX)])
dividir('costanera_bissau_hacialecheria', [(None, 'costanera_bissau_hacialecheria', AUX)])
# Bissau (sentido Lecheria): carril de incorporacion de 50 m y despues la bahia de 20 + 30 + 20 m
dividir('172344969#9', [(58, '172344969#9', AUX), (65, '172344969#9_b', None), (135, '172344969#9_bahia', BAHIA),
                        (None, '172344969#9_c', None)])
# Fernandez Padilla (sentido Camino Real): bahia de 15 + 20 + 15 m a 10 m del acceso
dividir('592256719#7', [(10, '592256719#7', None), (60, '592256719#7_bahia', BAHIA), (None, '592256719#7_b', None)])

for f, t, fl, tl in [
    # entradas a 172344969#4 (sin cambios de carril)
    ('-335982664#1', '172344969#4', 0, 1), ('costanera_puerto_guaica_haciacaminoreal', '172344969#4', 1, 1),
    ('costanera_puerto_guaica_hacialecheria', '172344969#4', 0, 0), ('costanera_puerto_guaica_hacialecheria', '172344969#4', 1, 1),
    ('salida:puerto_guaica', '172344969#4', 0, 0),
    # bahia Puerto Guaica
    ('172344969#4', '172344969#4_bahia', 0, 0), ('172344969#4', '172344969#4_bahia', 0, 1), ('172344969#4', '172344969#4_bahia', 1, 2),
    ('172344969#4_bahia', '172344969#4_b', 0, 0), ('172344969#4_bahia', '172344969#4_b', 1, 0), ('172344969#4_bahia', '172344969#4_b', 2, 1),
    # carril de salida de Bissau (3 carriles hasta el acceso)
    ('172344969#4_b', '172344969#4_salida_bissau', 0, 0), ('172344969#4_b', '172344969#4_salida_bissau', 0, 1),
    ('172344969#4_b', '172344969#4_salida_bissau', 1, 2),
    ('172344969#4_salida_bissau', '1223987566#0', 0, 0), ('172344969#4_salida_bissau', '172344969#5', 0, 0),
    ('172344969#4_salida_bissau', '172344969#5', 1, 1), ('172344969#4_salida_bissau', '172344969#5', 2, 2),
    ('-1223987566#0', '172344969#5', 0, 1),
    ('172344969#5', '1201018455#0', 0, 0), ('172344969#5', '172344969#6', 0, 0), ('172344969#5', '172344969#6', 1, 1),
    ('172344969#5', '172344969#6', 2, 2), ('-1201018455#0', '172344969#6', 0, 1),
    ('172344969#6', '1227058166#0', 0, 0), ('172344969#6', 'costanera_bissau_hacialecheria', 0, 0),
    ('172344969#6', 'costanera_bissau_hacialecheria', 1, 1), ('172344969#6', 'costanera_bissau_hacialecheria', 2, 2),
    ('-1227058166#0', 'costanera_bissau_hacialecheria', 0, 1),
    ('costanera_bissau_hacialecheria', 'entrada:bissau:1', 0, 0), ('costanera_bissau_hacialecheria', 'entrada_bissau_2', 0, 0),
    ('costanera_bissau_hacialecheria', '172344969#9', 1, 1), ('costanera_bissau_hacialecheria', '172344969#9', 2, 2),
    # carril de incorporacion de Bissau y bahia
    ('salida_bissau_1', '172344969#9', 0, 0), ('salida_bissau_2', '172344969#9', 0, 0),
    ('172344969#9', '172344969#9_b', 0, 0), ('172344969#9', '172344969#9_b', 1, 0), ('172344969#9', '172344969#9_b', 2, 1),
    ('172344969#9_b', '172344969#9_bahia', 0, 0), ('172344969#9_b', '172344969#9_bahia', 0, 1), ('172344969#9_b', '172344969#9_bahia', 1, 2),
    ('172344969#9_bahia', '172344969#9_c', 0, 0), ('172344969#9_bahia', '172344969#9_c', 1, 0), ('172344969#9_bahia', '172344969#9_c', 2, 1),
    ('172344969#9_c', '1223987567', 0, 0), ('172344969#9_c', '172344969#10', 0, 0), ('172344969#9_c', '172344969#10', 1, 1),
    # bahia Fernandez Padilla
    ('-335982661#0', '592256719#7', 0, 0), ('592256719#6', '592256719#7', 0, 0), ('592256719#6', '592256719#7', 1, 1),
    ('592256719#7', '592256719#7_bahia', 0, 0), ('592256719#7', '592256719#7_bahia', 0, 1), ('592256719#7', '592256719#7_bahia', 1, 2),
    ('592256719#7_bahia', '592256719#7_b', 0, 0), ('592256719#7_bahia', '592256719#7_b', 1, 0), ('592256719#7_bahia', '592256719#7_b', 2, 1),
    ('592256719#7_b', '1223688133#0', 0, 0), ('592256719#7_b', 'curva_caminoreal', 0, 0),
    ('592256719#7_b', 'costanera_hacia_distribuidor', 0, 0), ('592256719#7_b', 'costanera_hacia_distribuidor', 1, 1),
]:
    con(f, t, fl, tl)

# las salidas de Bissau con giro a la izquierda se conservan (la isla central no se prolonga por ahora)
for c in ET.parse('act.con.xml').getroot().findall('connection'):
    if c.get('from') in ('salida_bissau_1', 'salida_bissau_2') and c.get('to') == '592256719#4':
        C.append(c)

# ------------------------------------------------------------------ semaforo de Camino Real
# Se mantiene el semaforo de 4 fases del usuario (una por acceso; ciclo 122 s). El de la tesis (Anexo B: 3 fases,
# verdes 40/40/80 s con ciclos de 88, 83 y 113 s) no separa los movimientos que se cruzan ni da verde a la avenida en proyeccion.
# indices: 0-3 av. proyeccion | 4-6 FFAA a nivel | 7-10 El Ejercito | 11 sin uso | 12-14 Costanera a nivel
logica = next(x for x in T.findall('tlLogic') if x.get('id') == TL)
for ph in list(logica):
    logica.remove(ph)
for dur, estado in [(30, 'GGGGrrrrrrrrrrr'), (3, 'yyyyrrrrrrrrrrr'),     # av. en proyeccion
                    (40, 'rrrrrrrGGGGrrrr'), (3, 'rrrrrrryyyyrrrr'),     # El Ejercito
                    (20, 'rrrrrrrrrrrGGGG'), (3, 'rrrrrrrrrrryyyy'),     # Costanera a nivel
                    (20, 'rrrrGGGrrrrrrrr'), (3, 'rrrryyyrrrrrrrr')]:    # FFAA a nivel
    ET.SubElement(logica, 'phase', duration=str(dur), state=estado)

for t, nombre in ((tn, 'nod'), (tE, 'edg'), (tC, 'con'), (tT, 'tll')):
    t.write(f'mod.{nombre}.xml', encoding='UTF-8', xml_declaration=True)
print(f'cruce sobre el eje del puente: s = {S_CRUCE:.1f} m de {Lp:.1f} m; rampas {s1:.1f}-{s2:.1f} y {s3:.1f}-{s4:.1f}')
