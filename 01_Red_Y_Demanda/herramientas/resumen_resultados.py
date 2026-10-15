"""
Resume la simulacion en dos CSV para el Excel de resultados:
  resumen_intersecciones.csv  volumen, demora de control, nivel de servicio HCM 2000 y FHMD
                              por interseccion y por acceso, junto a los valores de las tesis y del campo 2026
  resumen_viajes.csv          indicadores de red por tipo de vehiculo

Solo se usa la hora de analisis (900-4500 s); los primeros 15 min son de calentamiento.

Uso: python resumen_resultados.py <escenario> <carpeta_xml> <carpeta_csv>
"""
import csv
import os
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

INICIO, FIN = 900.0, 4500.0
AQUI = os.path.dirname(os.path.abspath(__file__))
MAPA = os.path.join(AQUI, '..', 'accesos_intersecciones.csv')

# Valores de referencia (capitulo 4 de las tesis y trabajo de campo 2026 sin motos).
# Volumenes solo de los movimientos que pasan por el semaforo, igual que la medicion:
#   Camino Real sin la curva Costanera -> El Ejercito (Savignani 1765 - 190; campo 1740 - 450)
#   CC Paos sin los giros libres Costanera -> Lecheria y Lecheria -> Madre Vieja (Savignani 1831 - 601 - 169; campo 1300 - 220)
REFERENCIA = {
    'Camino Real': ('semaforizada', 'Savignani 2021, interseccion 1', 'F', '129.3', 1575, 1290),
    'CC Paos': ('semaforizada', 'Savignani 2021, interseccion 2', 'C', '22.6', 1061, 1080),
    'Perrokero': ('no semaforizada', 'Perozo 2022', 'F', '2883.7 (tabla 4.9); 1000.0 en conclusiones', 2349, 800),
    'Bissau': ('no semaforizada', 'Savignani 2021, acceso Bissau', 'F', '1074 a 1228 (HCM recalculado: ~28 s, D)', 1572, 1470),
    'Puerto Guaica': ('no semaforizada', 'Savignani 2021, acceso Fernandez Padilla', 'F', '1074 a 1228', 1637, 1290),
}


def los(demora, semaforizada):
    limites = (10, 20, 35, 55, 80) if semaforizada else (10, 15, 25, 35, 50)
    for letra, lim in zip('ABCDE', limites):
        if demora <= lim:
            return letra
    return 'F'


def en_ventana(iv):
    return float(iv.get('begin')) >= INICIO and float(iv.get('end')) <= FIN


def num(x):
    return f'{x:.2f}'


def main(escenario, carpeta_xml, carpeta_csv):
    # --- intersecciones (detectores E3) ---
    e3 = defaultdict(lambda: {'veh': [], 'perdida': 0.0, 'paradas': 0.0})
    for iv in ET.parse(os.path.join(carpeta_xml, 'reporte_intersecciones.xml')).getroot().iter('interval'):
        if not en_ventana(iv):
            continue
        nombre = iv.get('id')[3:].replace('_', ' ')
        n = float(iv.get('vehicleSum'))
        d = e3[nombre]
        d['veh'].append(n)
        if n > 0:
            d['perdida'] += n * max(0.0, float(iv.get('meanTimeLoss')))
            d['paradas'] += n * max(0.0, float(iv.get('meanHaltsPerVehicle')))

    # --- accesos (edgeData sobre los tramos de cada acceso) ---
    # volumen = vehiculos que salen del ultimo tramo hacia la interseccion; demora = tiempo perdido en el acceso / volumen
    tramos = defaultdict(lambda: {'perdida': 0.0, 'salen': 0.0})
    salen_15min = defaultdict(float)   # (tramo, inicio del intervalo) -> vehiculos
    for iv in ET.parse(os.path.join(carpeta_xml, 'reporte_accesos.xml')).getroot().iter('interval'):
        if not en_ventana(iv):
            continue
        for e in iv.iter('edge'):
            t = tramos[e.get('id')]
            t['perdida'] += float(e.get('timeLoss', 0))
            t['salen'] += float(e.get('left', 0))
            salen_15min[(e.get('id'), iv.get('begin'))] += float(e.get('left', 0))
    accesos = defaultdict(list)
    volumen_15min = defaultdict(lambda: defaultdict(float))   # interseccion -> intervalo -> vehiculos
    with open(MAPA, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f, delimiter=';'):
            perdida = sum(tramos[t]['perdida'] for t in r['tramos_del_acceso'].split())
            veh = tramos[r['tramo_final']]['salen']
            accesos[r['interseccion']].append((r['acceso'], r['tipo'], veh, perdida / veh if veh else 0.0))
            for (tramo, inicio), n in salen_15min.items():
                if tramo == r['tramo_final']:
                    volumen_15min[r['interseccion']][inicio] += n

    horas = (FIN - INICIO) / 3600.0
    filas = []
    for nombre, (tipo, fuente, los_t, demora_t, vol_t, vol_c) in REFERENCIA.items():
        semaf = tipo == 'semaforizada'
        # demora de control: detector E3 (vehiculos que recorren todo el area de la interseccion)
        d = e3.get(nombre, {'veh': [], 'perdida': 0.0, 'paradas': 0.0})
        muestra = sum(d['veh'])
        demora = d['perdida'] / muestra if muestra else 0.0
        # volumen y FHMD: suma de los accesos (incluye vehiculos que se incorporan dentro del area)
        v15 = list(volumen_15min[nombre].values())
        total = sum(v15)
        fhmd = total / (4 * max(v15)) if v15 and max(v15) > 0 else 0.0
        secundarios = [a for a in accesos[nombre] if a[1] == 'secundario' and a[2] > 0]
        if semaf or not secundarios:
            los_hcm = los(demora, semaf)
        else:
            los_hcm = los(max(a[3] for a in secundarios), False)
        filas.append([escenario, nombre, 'INTERSECCION', '(todos)', tipo, num(total / horas), num(demora),
                      los(demora, semaf), los_hcm, num(d['paradas'] / muestra if muestra else 0.0), num(fhmd),
                      fuente, los_t, demora_t, vol_t, vol_c])
        for acceso, rol, veh, dem in accesos[nombre]:
            filas.append([escenario, nombre, 'ACCESO', acceso, rol, num(veh / horas), num(dem),
                          los(dem, semaf), los(dem, semaf), '', '', '', '', '', '', ''])

    os.makedirs(carpeta_csv, exist_ok=True)
    with open(os.path.join(carpeta_csv, 'resumen_intersecciones.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['escenario', 'interseccion', 'nivel', 'acceso', 'tipo', 'volumen_sim_veh_h', 'demora_sim_s',
                    'LOS_sim_promedio', 'LOS_sim_HCM', 'paradas_por_veh', 'FHMD_sim',
                    'tesis_fuente', 'tesis_LOS', 'tesis_demora_s', 'tesis_volumen_veh_h', 'campo2026_volumen_veh_h'])
        w.writerows(filas)

    # --- viajes (tripinfo) ---
    tipos = defaultdict(lambda: [0, 0.0, 0.0, 0.0, 0.0, 0.0])
    for t in ET.parse(os.path.join(carpeta_xml, 'reporte_viajes.xml')).getroot().iter('tripinfo'):
        if not INICIO <= float(t.get('depart')) < FIN:
            continue
        for clave in (t.get('vType'), 'TOTAL'):
            a = tipos[clave]
            a[0] += 1
            a[1] += float(t.get('duration'))
            a[2] += float(t.get('timeLoss'))
            a[3] += float(t.get('waitingTime'))
            a[4] += float(t.get('routeLength'))
            a[5] += float(t.get('stopTime', 0))
    teleports = ''
    estad = os.path.join(carpeta_xml, 'estadisticas.xml')
    if os.path.exists(estad):
        tp = ET.parse(estad).getroot().find('teleports')
        teleports = tp.get('total') if tp is not None else ''
    with open(os.path.join(carpeta_csv, 'resumen_viajes.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['escenario', 'tipo_vehiculo', 'viajes', 'tiempo_viaje_s', 'demora_s', 'tiempo_detenido_s',
                    'velocidad_media_kmh', 'teleports_simulacion'])
        for clave in sorted(tipos, key=lambda k: (k == 'TOTAL', k)):
            n, dur, perd, esp, dist, parada = tipos[clave]
            w.writerow([escenario, clave, n, num(dur / n), num(perd / n), num(esp / n),
                        num(dist / (dur - parada) * 3.6) if dur > parada else '', teleports if clave == 'TOTAL' else ''])

    for fila in filas:
        if fila[2] == 'INTERSECCION':
            print(f'{fila[1]:14s} {fila[5]:>8s} veh/h  demora {fila[6]:>7s} s  LOS {fila[7]} (HCM {fila[8]})  FHMD {fila[10]}'
                  f'  | tesis: LOS {fila[12]}, {fila[13]} s, {fila[14]} veh/h | campo: {fila[15]} veh/h')
        else:
            print(f'     {fila[3]:34s} {fila[4]:10s} {fila[5]:>8s} veh/h  demora {fila[6]:>7s} s  LOS {fila[7]}')
    print(f'teleports: {teleports}')


if __name__ == '__main__':
    main(*sys.argv[1:4])
