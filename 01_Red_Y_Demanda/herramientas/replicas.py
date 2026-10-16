"""
Corre la simulacion base N veces con semillas distintas (sin ventana) y resume los resultados por
interseccion y por acceso: promedio, minimo, maximo y desviacion estandar de volumen y demora,
y el nivel de servicio HCM 2000 de la demora promedio.  ->  resumen_replicas.csv

Uso: python replicas.py <N> <archivo.sumocfg> <carpeta_xml> <carpeta_csv>
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

SUMO = os.path.join(os.environ.get('SUMO_HOME', r'C:\SUMO'), 'bin', 'sumo.exe')


def main(n, config, carpeta_xml, carpeta_csv):
    n = int(n)
    datos = {}   # (interseccion, nivel, acceso) -> lista de (volumen, demora, tipo)
    orden = []
    teleports = []
    for semilla in range(1, n + 1):
        print(f'  Replica {semilla} de {n}...', flush=True)
        subprocess.run([SUMO, '-c', config, '--seed', str(semilla), '--no-step-log', '--no-warnings'],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with tempfile.TemporaryDirectory() as tmp:
            sal = sys.stdout
            sys.stdout = open(os.devnull, 'w')
            try:
                rr.main(f'replica{semilla}', carpeta_xml, tmp)
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
        ref = rr.REFERENCIA[inter]
        filas.append([inter, nivel, acceso, n, f'{statistics.mean(vol):.0f}', f'{dm:.1f}', f'{min(dem):.1f}', f'{max(dem):.1f}',
                      f'{statistics.stdev(dem) if n > 1 else 0:.1f}', rr.los(dm, semaf[inter]), los,
                      ref[2] if nivel == 'INTERSECCION' else '', ref[3] if nivel == 'INTERSECCION' else ''])

    with open(os.path.join(carpeta_csv, 'resumen_replicas.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['interseccion', 'nivel', 'acceso', 'replicas', 'volumen_promedio_veh_h', 'demora_promedio_s',
                    'demora_min_s', 'demora_max_s', 'desviacion_estandar_s', 'LOS_promedio', 'LOS_HCM',
                    'tesis_LOS', 'tesis_demora_s'])
        w.writerows(filas)
    for fila in filas:
        if fila[1] == 'INTERSECCION':
            print(f'  {fila[0]:14s} {fila[4]:>6s} veh/h  demora {fila[5]:>6s} s ({fila[6]}-{fila[7]})  LOS {fila[10]}  | tesis {fila[11]}')
    print(f'  teleports por replica: {teleports}')


if __name__ == '__main__':
    main(*sys.argv[1:5])
