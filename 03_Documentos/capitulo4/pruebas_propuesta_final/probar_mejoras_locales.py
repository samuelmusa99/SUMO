"""Ensaya los carriles de Bissau y la bahía de Puerto Guaica sobre el plan de 82 s."""
import csv
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
from probar_camino_real import CARPETA, MODELO, replicas
from probar_coordinacion import adicionales_para_replicas

SALIDA = CARPETA / "mejoras_locales"
CADENAS = {
    "172344969#4": ("172344969#4", "172344969#4_bahia", "172344969#4_b",
                   "172344969#4_salida_bissau"),
    "172344969#9": ("172344969#9", "172344969#9_b", "172344969#9_bahia",
                   "172344969#9_c"),
}
ENSANCHADOS = {"172344969#5", "172344969#6", "costanera_bissau_hacialecheria"}


def xml(ruta):
    return ET.parse(ruta).getroot()


def guardar(raiz, ruta):
    ET.ElementTree(raiz).write(ruta, encoding="utf-8", xml_declaration=True)


def aplicar_geometria(base, sav):
    aristas = {e.get("id"): e for e in sav.findall("edge")}
    tramos = ENSANCHADOS | {e for cadena in CADENAS.values() for e in cadena}
    nodos = {aristas[e].get(campo) for e in tramos for campo in ("from", "to")}

    def interno(eid):
        return any(eid.startswith(f":{nodo}_") for nodo in nodos)

    def conexiones(red):
        exteriores = {e.get("id"): e.get("to") for e in red.findall("edge")}
        return [c for c in red.findall("connection")
                if exteriores.get(c.get("from")) in nodos or interno(c.get("from"))]

    def movimientos(red, lista):
        alias = {e: original for original, cadena in CADENAS.items() for e in cadena}
        ids = {e.get("id") for e in red.findall("edge") if not e.get("function")}
        return {(alias.get(f, f), alias.get(t, t)) for c in lista
                for f, t in [(c.get("from"), c.get("to"))]
                if f in ids and t in ids and alias.get(f, f) != alias.get(t, t)}

    viejas, nuevas = conexiones(base), conexiones(sav)
    if movimientos(base, viejas) != movimientos(sav, nuevas):
        raise ValueError(f"Movimientos distintos: {movimientos(base, viejas) ^ movimientos(sav, nuevas)}")
    for etiqueta, seleccion in (
        ("edge", lambda e: e.get("id") in tramos or interno(e.get("id"))),
        ("junction", lambda n: n.get("id") in nodos or interno(n.get("id"))),
        ("connection", lambda c: c in viejas or c in nuevas),
    ):
        originales = [e for e in base.findall(etiqueta) if seleccion(e)]
        posicion = min(list(base).index(e) for e in originales)
        for e in originales:
            base.remove(e)
        for e in sav.findall(etiqueta):
            if seleccion(e):
                base.insert(posicion, e)
                posicion += 1
    # Este ensanche está en la red donante, pero aquí no se habilita una parada en Bissau.
    aristas["172344969#9_bahia"].find("lane").attrib.pop("allow", None)
    aristas["172344969#9_bahia"].find("lane").set("disallow", "all")
    return base


def preparar(anio, carpeta):
    referencia = CARPETA / "sur_28" / anio
    config = xml(referencia / "prueba.sumocfg")
    base = xml(referencia / "costanera.net.xml")
    datos = subprocess.check_output(
        ["git", "-C", str(MODELO.parent), "show",
         "18e7bfe3f81cfffc98f25cd92011b5153c287c31:01_Red_Y_Demanda/costanera.net.xml"]
    )
    guardar(aplicar_geometria(base, ET.fromstring(datos)), carpeta / "costanera.net.xml")
    entrada = config.find("input")
    rutas = entrada.find("route-files")
    fuentes = rutas.get("value").split(",")
    for fuente in fuentes:
        original = Path(fuente)
        raiz = xml(original)
        for ruta in raiz.iter("route"):
            if ruta.get("edges"):
                ruta.set("edges", expandir(ruta.get("edges")))
        guardar(raiz, carpeta / original.name)
    rutas.set("value", ",".join(Path(f).name for f in fuentes))

    adicionales = entrada.find("additional-files")
    nuevos = []
    for fuente in map(Path, adicionales.get("value").split(",")):
        if fuente.name == "paradas.add.xml":
            raiz = xml(fuente)
            parada = raiz.find("busStop[@id='bs_0']")
            parada.attrib.update(lane="172344969#4_bahia_0", startPos="16", endPos="46")
        elif fuente.name.startswith("detectores_intersecciones"):
            raiz = xml(fuente)
            for detector in raiz.findall("e3Detector"):
                for punto in list(detector):
                    lane = punto.get("lane", "")
                    eid, _, indice = lane.rpartition("_")
                    if eid == "172344969#4":
                        pos = float(punto.get("pos"))
                        receptor = "172344969#4_b" if pos >= 80 else "172344969#4_bahia"
                        punto.attrib.update(lane=f"{receptor}_{int(indice) + (pos < 80)}",
                                            pos=str(pos - (80 if pos >= 80 else 10)))
                        if pos < 80 and indice == "0":
                            ET.SubElement(detector, punto.tag,
                                          {**punto.attrib, "lane": f"{receptor}_0"})
                    elif eid == "172344969#9":
                        punto.attrib.update(lane=f"{eid}_b_{indice}", pos="2")
                    elif eid in ENSANCHADOS:
                        punto.set("lane", f"{eid}_{int(indice) + 1}")
            for detector in raiz.findall("edgeData"):
                detector.set("edges", expandir(detector.get("edges")))
        else:
            nuevos.append(fuente.as_posix())
            continue
        guardar(raiz, carpeta / fuente.name)
        nuevos.append(fuente.name)
    adicionales.set("value", ",".join(nuevos))
    guardar(config, carpeta / "prueba.sumocfg")

    with (MODELO / "accesos_intersecciones.csv").open(encoding="utf-8-sig") as f:
        lector = csv.DictReader(f, delimiter=";")
        with (carpeta / "accesos_intersecciones.csv").open(
                "w", encoding="utf-8-sig", newline="") as destino:
            escritor = csv.DictWriter(destino, fieldnames=lector.fieldnames, delimiter=";")
            escritor.writeheader()
            for fila in lector:
                fila["tramos_del_acceso"] = " ".join(
                    t for eid in fila["tramos_del_acceso"].split()
                    for t in reversed(CADENAS.get(eid, (eid,)))
                )
                escritor.writerow(fila)


def expandir(cadena):
    return " ".join(t for eid in cadena.split() for t in CADENAS.get(eid, (eid,)))


def ejecutar(anio):
    carpeta = SALIDA / anio
    carpeta.mkdir(parents=True, exist_ok=True)
    preparar(anio, carpeta)
    replicas.rr.RED = str(carpeta / "costanera.net.xml")
    replicas.rr.MAPA = replicas.cap.MAPA = str(carpeta / "accesos_intersecciones.csv")
    replicas.adicionales_aislados = adicionales_para_replicas
    referencia = str(SALIDA / "2026" / "resumen_replicas.csv") if anio == "2041" else None
    procesar = replicas.rr.main
    with (carpeta / "diagnostico_semillas.csv").open("w", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f, delimiter=";")
        escritor.writerow(("replica", "colisiones", "teletransportes", "en_red_al_cierre",
                           "pendientes_de_ingreso_al_cierre"))

        def registrar(escenario, carpeta_xml, carpeta_csv):
            datos = xml(Path(carpeta_xml) / "estadisticas.xml")
            escritor.writerow((escenario, datos.find("safety").get("collisions"),
                               datos.find("teleports").get("total"),
                               datos.find("vehicles").get("running"),
                               datos.find("vehicles").get("waiting")))
            f.flush()
            procesar(escenario, carpeta_xml, carpeta_csv)

        replicas.rr.main = registrar
        replicas.main(5, str(carpeta / "prueba.sumocfg"), str(carpeta), str(carpeta),
                      referencia=referencia)


if __name__ == "__main__":
    ejecutar(sys.argv[1])
