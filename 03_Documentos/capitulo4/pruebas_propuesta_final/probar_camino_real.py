"""Pruebas aisladas del reparto de verde de Camino Real sobre Perozo."""
import csv
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
MODELO = CARPETA.parents[2] / "01_Red_Y_Demanda"
sys.path.insert(0, str(MODELO / "herramientas"))
sys.dont_write_bytecode = True
import replicas

PLANES = {
    "control": (25, 25, 20),
    "sur_28": (28, 20, 22),
    "sur_30": (30, 23, 17),
    "sur_32": (32, 20, 18),
}
ACCESOS = ("semaforo_caminoreal_FA", "semaforo_caminoreal_elejercito",
           "semaforo_caminoreal_costanera")


def ejecutar(plan, anio, *, verdes=None, ciclo=82, desfase=0, carpeta=CARPETA):
    salida = carpeta / plan / anio
    salida.mkdir(parents=True, exist_ok=True)
    nombre = {"2026": "tesis_base.sumocfg", "2041": "escenario_2041.sumocfg"}[anio]
    configuracion = ET.parse(MODELO / nombre)
    entrada = configuracion.getroot().find("input")
    red = ET.parse(MODELO / entrada.find("net-file").get("value"))
    conexiones = red.getroot().findall("connection")
    ids = {c.get("tl") for c in conexiones if c.get("from") in ACCESOS and c.get("tl")}
    controlador, = ids
    logica, = red.getroot().findall(f"tlLogic[@id='{controlador}']")
    fases = logica.findall("phase")
    tiempos_verde = PLANES[plan] if verdes is None else verdes
    for indice, acceso, verde in zip((0, 3, 6), ACCESOS, tiempos_verde, strict=True):
        fase = fases[indice]
        activos = {c.get("from") for c in conexiones if c.get("tl") == controlador
                   and fase.get("state")[int(c.get("linkIndex"))] in "Gg"}
        if activos != {acceso}:
            raise ValueError(f"Fase inesperada en {acceso}: {activos}")
        fase.set("duration", str(verde))
    if sum(int(fase.get("duration")) for fase in fases) != ciclo:
        raise ValueError(f"El ciclo debe sumar {ciclo} segundos")
    logica.set("offset", str(desfase))

    ruta_red = salida / "costanera.net.xml"
    red.write(ruta_red, encoding="utf-8", xml_declaration=True)
    entrada.find("net-file").set("value", ruta_red.name)
    for campo in ("route-files", "additional-files"):
        elemento = entrada.find(campo)
        elemento.set("value", ",".join((MODELO / ruta).as_posix()
                                      for ruta in elemento.get("value").split(",")))
    configuracion.getroot().remove(configuracion.getroot().find("gui_only"))
    for elemento in configuracion.getroot().find("output"):
        if elemento.tag.endswith("-output"):
            elemento.set("value", Path(elemento.get("value")).name)
    ruta_config = salida / "prueba.sumocfg"
    configuracion.write(ruta_config, encoding="utf-8", xml_declaration=True)
    replicas.rr.RED = str(ruta_red)
    procesar = replicas.rr.main
    with (salida / "diagnostico_semillas.csv").open("w", encoding="utf-8", newline="") as archivo:
        writer = csv.writer(archivo, delimiter=";")
        writer.writerow(("replica", "colisiones", "teletransportes", "insertados",
                         "en_red_al_cierre", "pendientes_de_ingreso_al_cierre"))

        def registrar(escenario, carpeta_xml, carpeta_csv):
            resumen = ET.parse(Path(carpeta_xml) / "estadisticas.xml").getroot()
            writer.writerow((escenario, resumen.find("safety").get("collisions"),
                             resumen.find("teleports").get("total"),
                             *(resumen.find("vehicles").get(k)
                               for k in ("inserted", "running", "waiting"))))
            archivo.flush()
            procesar(escenario, carpeta_xml, carpeta_csv)

        replicas.rr.main = registrar
        referencia = str(salida.parent / "2026" / "resumen_replicas.csv") if anio == "2041" else None
        replicas.main(5, str(ruta_config), str(salida), str(salida), referencia=referencia)


if __name__ == "__main__":
    ejecutar(*sys.argv[1:])
