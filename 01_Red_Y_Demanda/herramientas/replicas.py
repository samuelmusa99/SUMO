"""
Corre la simulacion base N veces con semillas distintas (sin ventana) y resume los resultados por
interseccion y por acceso: promedio, minimo, maximo y desviacion estandar de volumen y demora,
y el nivel de servicio HCM 2000 de la demora promedio.  ->  resumen_replicas.csv

Tambien agrega por acceso: demanda, capacidad (HCM 2000 o medida si esta saturado), V/C y demanda atendida.

Uso: python replicas.py <N> <archivo.sumocfg> <carpeta_xml> <carpeta_csv> [archivo_salida.csv]
"""
import csv
import os
import statistics
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import resumen_resultados as rr  # noqa: E402
import capacidad as cap  # noqa: E402

SUMO = os.path.join(os.environ.get('SUMO_HOME', r'C:\SUMO'), 'bin', 'sumo.exe')


def adicionales_aislados(config, tmp):
    """copia los archivos adicionales que escriben resultados (detectores y medidores) cambiando su
    carpeta de salida por la carpeta temporal; el resto se usa tal cual"""
    import xml.etree.ElementTree as ET
    base = os.path.dirname(os.path.abspath(config))
    lista = ET.parse(config).getroot().find('input/additional-files').get('value').split(',')
    salida = []
    for nombre in lista:
        ruta = os.path.join(base, nombre.strip())
        with open(ruta, encoding='utf-8') as f:
            texto = f.read()
        if '../02_Resultados_Base/' in texto:
            copia = os.path.join(tmp, os.path.basename(ruta))
            with open(copia, 'w', encoding='utf-8') as f:
                f.write(texto.replace('../02_Resultados_Base/', tmp.replace('\\', '/') + '/'))
            salida.append(copia)
        else:
            salida.append(ruta)
    return salida


def main(n, config, carpeta_xml, carpeta_csv, archivo_salida='resumen_replicas.csv'):
    n = int(n)
    datos = {}   # (interseccion, nivel, acceso) -> lista de (volumen, demora, tipo)
    orden = []
    teleports = []
    for semilla in range(1, n + 1):
        print(f'  Replica {semilla} de {n} ({os.path.basename(config)})...', flush=True)
        with tempfile.TemporaryDirectory() as tmp:
            # cada replica escribe en su propia carpeta temporal: nunca toca los XML de la corrida en SUMO-GUI
            subprocess.run([SUMO, '-c', config, '--seed', str(semilla), '--no-step-log', '--no-warnings',
                            '-a', ','.join(adicionales_aislados(config, tmp)),
                            '--tripinfo-output', os.path.join(tmp, 'reporte_viajes.xml'),
                            '--queue-output', os.path.join(tmp, 'reporte_colas.xml'),
                            '--statistic-output', os.path.join(tmp, 'estadisticas.xml')],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            sal = sys.stdout
            sys.stdout = open(os.devnull, 'w')
            try:
                rr.main(f'replica{semilla}', tmp, tmp)
            finally:
                sys.stdout.close()
                sys.stdout = sal
            with open(os.path.join(tmp, 'resumen_intersecciones.csv'), encoding='utf-8-sig') as f:
                for r in csv.DictReader(f, delimiter=';'):
                    k = (r['interseccion'], r['nivel'], r['acceso'])
                    if k not in datos:
                        datos[k] = []
                        orden.append(k)
                    datos[k].append((float(r['volumen_sim_veh_h']), float(r['demora_sim_s']), r['tipo']))
            with open(os.path.join(tmp, 'resumen_viajes.csv'), encoding='utf-8-sig') as f:
                for r in csv.DictReader(f, delimiter=';'):
                    if r['tipo_vehiculo'] == 'TOTAL' and r['teleports_simulacion']:
                        teleports.append(int(r['teleports_simulacion']))

    semaf = {nombre: ref[0] == 'semaforizada' for nombre, ref in rr.REFERENCIA.items()}
    atendido = {(k[0], k[2]): statistics.mean(d[0] for d in datos[k]) for k in orden if k[1] == 'ACCESO'}
    capac = cap.calcular(config, atendido)
    referencia = os.path.join(carpeta_csv, 'resumen_replicas.csv')
    if archivo_salida != 'resumen_replicas.csv' and os.path.exists(referencia):
        # La capacidad depende de la via y los semaforos, no de la demanda: en escenarios futuros con la misma red se
        # usa la capacidad de la situacion actual (en un bloqueo, el flujo medido ya no refleja la capacidad del acceso)
        with open(referencia, encoding='utf-8-sig') as f:
            base = {(r['interseccion'], r['acceso']): float(r['capacidad_veh_h'])
                    for r in csv.DictReader(f, delimiter=';') if r['nivel'] == 'ACCESO' and r['capacidad_veh_h']}
        for k, cx in capac.items():
            if k in base and base[k] > 0:
                cx['capacidad'], cx['fuente'] = base[k], 'capacidad de la situacion actual 2026'
                cx['vc'] = cx['demanda'] / base[k]
    filas = []
    for k in orden:
        inter, nivel, acceso = k
        vol = [d[0] for d in datos[k]]
        dem = [d[1] for d in datos[k]]
        dm = statistics.mean(dem)
        los = rr.los(dm, semaf[inter])
        if nivel == 'INTERSECCION' and not semaf[inter]:
            # HCM para intersecciones sin semaforo: nivel del peor acceso secundario
            sec = [statistics.mean(d[1] for d in datos[j]) for j in orden
                   if j[0] == inter and j[1] == 'ACCESO' and datos[j][0][2] == 'secundario' and statistics.mean(d[0] for d in datos[j]) > 0]
            los = rr.los(max(sec), False) if sec else los
        if nivel == 'ACCESO':
            cx = capac[(inter, acceso)]
            demanda, capacidad, fuente, vc, at = cx['demanda'], f"{cx['capacidad']:.0f}", cx['fuente'], cx['vc'], cx['atendida']
        else:
            propios = [v for (i, _), v in capac.items() if i == inter]
            demanda = sum(v['demanda'] for v in propios)
            capacidad, fuente = '', 'V/C del acceso critico'
            vc = max(v['vc'] for v in propios)
            at = min(1.0, statistics.mean(vol) / demanda) if demanda else 1.0
        ref = rr.REFERENCIA[inter]
        filas.append([inter, nivel, acceso, n, f'{statistics.mean(vol):.0f}', f'{dm:.1f}', f'{min(dem):.1f}', f'{max(dem):.1f}',
                      f'{statistics.stdev(dem) if n > 1 else 0:.1f}', rr.los(dm, semaf[inter]), los,
                      f'{demanda:.0f}', capacidad, fuente, f'{vc:.2f}', f'{at * 100:.0f}',
                      ref[2] if nivel == 'INTERSECCION' else '', ref[3] if nivel == 'INTERSECCION' else ''])

    with open(os.path.join(carpeta_csv, archivo_salida), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['interseccion', 'nivel', 'acceso', 'replicas', 'volumen_promedio_veh_h', 'demora_promedio_s',
                    'demora_min_s', 'demora_max_s', 'desviacion_estandar_s', 'LOS_promedio', 'LOS_HCM',
                    'demanda_veh_h', 'capacidad_veh_h', 'fuente_capacidad', 'VC', 'demanda_atendida_pct',
                    'tesis_LOS', 'tesis_demora_s'])
        w.writerows(filas)
    for fila in filas:
        if fila[1] == 'INTERSECCION':
            print(f'  {fila[0]:14s} {fila[4]:>6s} de {fila[11]:>5s} veh/h ({fila[15]} %)  demora {fila[5]:>6s} s ({fila[6]}-{fila[7]})  LOS {fila[10]}  V/C max {fila[14]}  | tesis {fila[16]}')
    print(f'  teleports por replica: {teleports}')


if __name__ == '__main__':
    main(*sys.argv[1:6])
