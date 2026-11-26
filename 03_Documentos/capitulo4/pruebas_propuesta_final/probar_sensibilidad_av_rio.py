"""Sensibilidad 2026 con 863 veh/h programados en el acceso de Av. Río."""

import csv
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
from probar_camino_real import CARPETA, MODELO, replicas

BASE = "d816be3a634f82319fef111e9b4023d20aa8a516"
OBJETIVO = 863.0
ACCESO = "avrio_1"


def de_base(ruta):
    return subprocess.check_output(
        ["git", "-C", str(MODELO.parent), "show", f"{BASE}:01_Red_Y_Demanda/{ruta}"]
    )


def preparar_demanda(datos, destino):
    demanda = ET.fromstring(datos)
    rutas = {r.get("id") for r in demanda.findall("route")
             if ACCESO in r.get("edges").split()}
    flujos = []
    total = 0
    for flujo in demanda.findall("flow"):
        if flujo.get("route") in rutas:
            tasa = float(re.fullmatch(r"exp\(([^)]+)\)", flujo.get("period"))[1])
            inicio = max(900, float(flujo.get("begin")))
            fin = min(4500, float(flujo.get("end")))
            total += tasa * max(0, fin - inicio)
            flujos.append((flujo, tasa))
    if round(total) != 619:
        raise ValueError(f"Se esperaba una demanda de referencia de 619 veh/h y se obtuvo {total:.2f}")
    factor = OBJETIVO / total
    for flujo, tasa in flujos:
        flujo.set("period", f"exp({tasa * factor:.10f})")
    ET.ElementTree(demanda).write(destino, encoding="utf-8", xml_declaration=True)
    print(f"Av. Río: de {total:.2f} a {OBJETIVO:.0f} veh/h, factor {factor:.6f}", flush=True)


def preparar_configuracion(escenario, temporal, salida, ajustar, archivo_demanda):
    es_base = escenario == "base"
    config_archivo = "tesis_base.sumocfg" if es_base else "propuesta_final_2026.sumocfg"
    config = ET.fromstring(de_base(config_archivo) if es_base
                           else (MODELO / config_archivo).read_bytes())
    entrada = config.find("input")
    mapa = temporal / "accesos_intersecciones.csv"
    modelo_final = MODELO / "propuesta_final"
    mapa.write_bytes(de_base(mapa.name) if es_base else (modelo_final / mapa.name).read_bytes())
    replicas.rr.MAPA = replicas.cap.MAPA = str(mapa)
    for campo in entrada:
        archivos = []
        for nombre in campo.get("value").split(","):
            if nombre.startswith("medidores") or nombre == "vista.xml":
                continue
            destino = temporal / Path(nombre).name
            datos = de_base(nombre) if es_base else (MODELO / nombre).read_bytes()
            if Path(nombre).name.startswith("demanda_"):
                destino = salida / archivo_demanda
                ajustar(datos, destino)
            else:
                destino.write_bytes(datos)
            archivos.append(destino.as_posix())
        campo.set("value", ",".join(archivos))
    config.remove(config.find("gui_only"))
    for e in config.find("output"):
        if e.tag.endswith("-output"):
            e.set("value", (temporal / Path(e.get("value")).name).as_posix())
    destino = temporal / "prueba.sumocfg"
    ET.ElementTree(config).write(destino, encoding="utf-8", xml_declaration=True)
    replicas.rr.RED = str(temporal / "costanera.net.xml")
    replicas.rr.TIPOS = str(temporal / "costanera.rou.xml")
    replicas.rr.PARADAS = str(temporal / "paradas.add.xml")
    if es_base:
        replicas.rr.REFERENCIA["Perrokero"] = (
            "no semaforizada", "Perozo 2022", "F",
            "2883.7 (tabla 4.9); 1000.0 en conclusiones", 2349, 800,
        )
    return destino


def ejecutar(escenario, *, ajustar=preparar_demanda, carpeta="sensibilidad_av_rio_863",
            archivo_demanda="demanda_av_rio_863.rou.xml", observar=None):
    if escenario not in ("base", "propuesta_final"):
        raise ValueError("Use base o propuesta_final")
    salida = CARPETA / carpeta / escenario / "2026"
    salida.mkdir(parents=True, exist_ok=True)
    procesar = replicas.rr.main
    with tempfile.TemporaryDirectory() as tmp, (salida / "diagnostico_semillas.csv").open(
            "w", encoding="utf-8", newline="") as archivo:
        config = preparar_configuracion(escenario, Path(tmp), salida, ajustar, archivo_demanda)
        writer = csv.writer(archivo, delimiter=";")
        writer.writerow(("replica", "colisiones", "teletransportes", "en_red_al_cierre",
                         "pendientes_de_ingreso_al_cierre"))

        def registrar(nombre, carpeta_xml, carpeta_csv):
            datos = ET.parse(Path(carpeta_xml) / "estadisticas.xml").getroot()
            writer.writerow((nombre, datos.find("safety").get("collisions"),
                             datos.find("teleports").get("total"),
                             datos.find("vehicles").get("running"),
                             datos.find("vehicles").get("waiting")))
            archivo.flush()
            if observar is not None:
                observar(nombre, Path(carpeta_xml), salida)
            procesar(nombre, carpeta_xml, carpeta_csv)

        replicas.rr.main = registrar
        replicas.main(5, str(config), tmp, str(salida))


if __name__ == "__main__":
    ejecutar(sys.argv[1])
