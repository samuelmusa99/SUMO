"""Mide llegadas a Camino Real en el plan de referencia de 82 s."""
import csv
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
from probar_camino_real import CARPETA, replicas

DESTINO = "semaforo_caminoreal_FA"
ORIGENES = {"FA_2": "a_nivel", "puente_bajada_hacia_norte": "puente"}


def main():
    config = CARPETA / "sur_28" / "2026" / "prueba.sumocfg"
    with tempfile.TemporaryDirectory() as directorio:
        rutas = Path(directorio) / "rutas.xml"
        adicionales = [a for a in replicas.adicionales_aislados(config, directorio)
                       if Path(a).name in {"paradas.add.xml"}]
        subprocess.run(
            [replicas.SUMO, "-c", str(config), "--seed", "1", "--no-step-log",
             "--no-warnings", "-a", ",".join(adicionales), "--tripinfo-output", "NUL",
             "--queue-output", "NUL", "--statistic-output", "NUL",
             "--vehroute-output", str(rutas), "--vehroute-output.exit-times", "true"],
            check=True,
        )
        grupos = {nombre: [] for nombre in ORIGENES.values()}
        destino = CARPETA / "llegadas_coordinacion_2026_semilla1.csv"
        with destino.open("w", encoding="utf-8", newline="") as archivo:
            writer = csv.writer(archivo, delimiter=";")
            writer.writerow(("vehiculo", "origen", "acceso_perrokero", "salida_perrokero_s",
                             "entrada_acceso_camino_real_s", "recorrido_s"))
            for vehiculo in ET.parse(rutas).getroot().findall("vehicle"):
                ruta = vehiculo.find("route")
                aristas = ruta.get("edges", "").split()
                tiempos = list(map(float, ruta.get("exitTimes", "").split()))
                if DESTINO not in aristas:
                    continue
                llegada = aristas.index(DESTINO)
                for arista, nombre in ORIGENES.items():
                    if arista not in aristas[:llegada] or llegada > len(tiempos):
                        continue
                    partida = tiempos[aristas.index(arista)]
                    entrada = tiempos[llegada - 1]
                    if 900 <= partida <= entrada < 4500:
                        grupos[nombre].append(entrada - partida)
                        origen = aristas.index(arista)
                        acceso = aristas[origen - 1] if origen else ""
                        writer.writerow((vehiculo.get("id"), nombre, acceso, partida, entrada,
                                         round(entrada - partida, 2)))
        for nombre, valores in grupos.items():
            print(nombre, len(valores), statistics.median(valores),
                  statistics.quantiles(valores, n=4))


if __name__ == "__main__":
    main()
