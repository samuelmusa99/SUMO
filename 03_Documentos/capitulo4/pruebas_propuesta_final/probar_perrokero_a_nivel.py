"""Variante preliminar sin puente, con giro izquierdo protegido al norte."""
import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
from probar_mejoras_locales import SALIDA, aplicar_geometria, expandir, guardar, replicas, xml

ORIGEN = "d816be3a634f82319fef111e9b4023d20aa8a516"
DONANTE = "18e7bfe3f81cfffc98f25cd92011b5153c287c31"
DESTINO = SALIDA.parent / "perrokero_a_nivel"
NODO = "interseccion_avrio_FA"
NORTE, SUR, ESTE, OESTE = "FA_3", "FA_1", "avrio_1", "res_salida"


def version(ruta, revision=ORIGEN):
    return subprocess.check_output(["git", "show", f"{revision}:01_Red_Y_Demanda/{ruta}"])


def construir_red(carpeta):
    base = ET.fromstring(version("costanera.net.xml"))
    aplicar_geometria(base, ET.fromstring(version("costanera.net.xml", DONANTE)))
    camino_real = next(t for t in base.findall("tlLogic") if t.get("id").startswith("cluster_130020"))
    for fase, duracion in zip(camino_real[::3], (28, 20, 22), strict=True):
        fase.set("duration", str(duracion))

    with tempfile.TemporaryDirectory() as temp:
        tmp = Path(temp)
        guardar(base, tmp / "base.net.xml")
        guardar(ET.fromstring(f'<nodes><node id="{NODO}" type="traffic_light"/></nodes>'),
                tmp / "perrokero.nod.xml")
        guardar(ET.fromstring(f'<edges><edge id="{NORTE}" numLanes="3">'
                              '<lane index="2" width="3.0"/></edge></edges>'),
                tmp / "perrokero.edg.xml")
        guardar(ET.fromstring(f'<connections><delete from="{NORTE}" to="avrio_2" '
                              'fromLane="1" toLane="1"/>'
                              f'<connection from="{NORTE}" to="avrio_2" fromLane="2" toLane="1"/>'
                              '</connections>'), tmp / "perrokero.con.xml")
        red = tmp / "nueva.net.xml"
        subprocess.run([
            str(Path(replicas.SUMO).with_name("netconvert.exe")),
            "-s", str(tmp / "base.net.xml"), "-n", str(tmp / "perrokero.nod.xml"),
            "-e", str(tmp / "perrokero.edg.xml"), "-x", str(tmp / "perrokero.con.xml"),
            "-o", str(red), "--tls.rebuild", "true", "--no-turnarounds", "true",
            "--offset.disable-normalization", "true", "--geometry.avoid-overlap", "false",
            "--junctions.corner-detail", "5", "--junctions.limit-turn-speed", "5.5",
            "--internal-junctions.vehicle-width", "3.0", "--rectangular-lane-cut", "false",
        ], check=True)
        nueva = xml(red)

    control = nueva.find(f"tlLogic[@id='{NODO}']")
    cruce = nueva.find(f"junction[@id='{NODO}']")
    conexiones = sorted((c for c in nueva.findall("connection") if c.get("tl") == NODO),
                        key=lambda c: int(c.get("linkIndex")))
    assert [int(c.get("linkIndex")) for c in conexiones] == list(range(len(conexiones)))
    assert [(c.get("fromLane"), c.get("toLane")) for c in conexiones
            if c.get("from") == NORTE and c.get("to") == "avrio_2"] == [("2", "1")]
    assert all(c.get("to") == "avrio_2" for c in conexiones
               if c.get("from") == NORTE and c.get("fromLane") == "2")
    internas = cruce.get("intLanes").split()
    rivales = {int(r.get("index")): r.get("foes")[::-1] for r in cruce.findall("request")}
    for fase in list(control):
        control.remove(fase)
    fases = [
        (24, lambda c: c.get("from") in (NORTE, SUR) and c.get("dir") == "s"),
        (20, lambda c: c.get("from") == NORTE),
        (8, lambda c: c.get("from") == SUR),
        (35, lambda c: c.get("from") == ESTE),
        (13, lambda c: c.get("from") == OESTE),
    ]
    for verde, criterio in fases:
        activas = [c for c in conexiones if criterio(c)]
        for i, a in enumerate(activas):
            for b in activas[i+1:]:
                if a.get("from") != b.get("from"):
                    ia, ib = (internas.index(c.get("via")) for c in (a, b))
                    if rivales[ia][ib] == "1" or rivales[ib][ia] == "1":
                        raise ValueError("La fase propuesta contiene trayectorias en conflicto")
        for duracion, luz in ((verde, "G"), (3, "y"), (1, "r")):
            ET.SubElement(control, "phase", duration=str(duracion),
                          state="".join(luz if c in activas else "r" for c in conexiones))

    # Sólo se cambia el cruce y los tramos directamente afectados.
    incidentes = {e.get("id") for e in base.findall("edge") if NODO in (e.get("from"), e.get("to"))}
    llegadas = {e.get("id") for e in base.findall("edge") if e.get("to") == NODO}
    interno = lambda eid: eid.startswith(f":{NODO}_")
    filtros = [
        ("edge", lambda e: e.get("id") in incidentes or interno(e.get("id"))),
        ("junction", lambda e: e.get("id") == NODO or interno(e.get("id"))),
        ("connection", lambda e: e.get("from") in llegadas or interno(e.get("from"))),
    ]
    for tag, corresponde in filtros:
        antiguos = [e for e in base.findall(tag) if corresponde(e)]
        pos = min(list(base).index(e) for e in antiguos)
        for e in antiguos:
            base.remove(e)
        for e in nueva.findall(tag):
            if corresponde(e):
                base.insert(pos, e)
                pos += 1
    base.insert(list(base).index(camino_real) + 1, control)
    guardar(base, carpeta / "costanera.net.xml")
    return base


def instalar_demanda(carpeta, anio, red):
    rutas = "demanda_base.rou.xml" if anio == "2026" else "demanda_2041.rou.xml"
    demanda = ET.fromstring(version(f"demanda/{rutas}"))
    transporte = ET.fromstring(version("costanera.rou.xml"))
    final = xml(SALIDA / anio / f"demanda_perozo_{anio}.rou.xml")
    original = {f.get("id"): f for f in demanda.findall("flow")}
    comparada = {f.get("id"): f for f in final.findall("flow")}
    assert original.keys() == comparada.keys(), "Difieren los flujos de comparación"
    for fid, flujo in original.items():
        assert all(flujo.get(k) == comparada[fid].get(k) for k in
                   ("begin", "end", "period", "type")), fid
    conexiones = {(c.get("from"), c.get("to")) for c in red.findall("connection")}
    for ruta in demanda.findall("route"):
        pasos = expandir(ruta.get("edges")).split()
        assert all((a, b) in conexiones for a, b in zip(pasos, pasos[1:])), ruta.get("id")
        ruta.set("edges", " ".join(pasos))
    guardar(demanda, carpeta / "demanda.rou.xml")
    guardar(transporte, carpeta / "costanera.rou.xml")


def preparar(carpeta, anio):
    red = construir_red(carpeta)
    instalar_demanda(carpeta, anio, red)
    referencia = SALIDA / anio
    config = xml(referencia / "prueba.sumocfg")
    entrada = config.find("input")
    entrada.find("route-files").set("value", "costanera.rou.xml,demanda.rou.xml")
    adicionales = entrada.find("additional-files")
    salida = []
    detector_nombre = ""
    for archivo in adicionales.get("value").split(","):
        nombre = Path(archivo).name
        if nombre.startswith("detectores_intersecciones"):
            detector_nombre = nombre
        elif nombre == "paradas.add.xml":
            (carpeta / nombre).write_bytes((referencia / nombre).read_bytes())
        elif nombre == "distribuidor.add.xml" or nombre.startswith("medidores"):
            continue
        salida.append(archivo)
    adicionales.set("value", ",".join(salida))
    guardar(config, carpeta / "prueba.sumocfg")

    mapa = (referencia / "accesos_intersecciones.csv").read_text(encoding="utf-8-sig")
    perrokero = version("accesos_intersecciones.csv").decode("utf-8-sig").splitlines()
    filas = [f for f in perrokero if f.startswith("Perrokero;")]
    lineas = []
    for f in mapa.splitlines():
        if not f.startswith("Perrokero;"):
            lineas.append(f)
        elif filas:
            lineas.extend(f.replace(";secundario;", ";principal;") for f in filas)
            filas.clear()
    (carpeta / "accesos_intersecciones.csv").write_text("\n".join(lineas) + "\n", encoding="utf-8-sig")
    detectores = xml(referencia / detector_nombre)
    e3 = detectores.find("e3Detector[@id='e3_Perrokero']")
    original = ET.fromstring(version(detector_nombre)).find("e3Detector[@id='e3_Perrokero']")
    for p in list(e3):
        e3.remove(p)
    e3.extend(list(original))
    for p in original.findall("detEntry"):
        if p.get("lane") == "FA_3_1":
            ET.SubElement(e3, "detEntry", {**p.attrib, "lane": "FA_3_2"})
    ids = sorted({t for linea in lineas[1:] for t in linea.split(";")[4].split()})
    detectores.find("edgeData[@id='accesos']").set("edges", " ".join(ids))
    guardar(detectores, carpeta / detector_nombre)


def ejecutar(anio):
    carpeta = DESTINO / anio
    carpeta.mkdir(parents=True, exist_ok=True)
    preparar(carpeta, anio)
    replicas.rr.RED = str(carpeta / "costanera.net.xml")
    replicas.rr.MAPA = replicas.cap.MAPA = str(carpeta / "accesos_intersecciones.csv")
    replicas.rr.TIPOS = str(carpeta / "costanera.rou.xml")
    replicas.rr.PARADAS = str(carpeta / "paradas.add.xml")
    procesar = replicas.rr.main
    with (carpeta / "diagnostico_semillas.csv").open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo, delimiter=";")
        escritor.writerow(("replica", "colisiones", "teletransportes", "en_red_al_cierre",
                           "pendientes_de_ingreso_al_cierre"))

        def registrar(escenario, carpeta_xml, carpeta_csv):
            datos = xml(Path(carpeta_xml) / "estadisticas.xml")
            escritor.writerow((escenario, datos.find("safety").get("collisions"),
                               datos.find("teleports").get("total"),
                               datos.find("vehicles").get("running"),
                               datos.find("vehicles").get("waiting")))
            archivo.flush()
            procesar(escenario, carpeta_xml, carpeta_csv)

        replicas.rr.main = registrar
        referencia = str(DESTINO / "2026" / "resumen_replicas.csv") if anio == "2041" else None
        replicas.main(5, str(carpeta / "prueba.sumocfg"), str(carpeta), str(carpeta),
                      referencia=referencia)


if __name__ == "__main__":
    ejecutar(sys.argv[1])
