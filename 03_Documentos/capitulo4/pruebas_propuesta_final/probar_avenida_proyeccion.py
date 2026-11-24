"""Incorpora el cuarto brazo de Camino Real al paquete combinado de 2041."""
import csv
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
from probar_mejoras_locales import SALIDA, adicionales_para_replicas, guardar, replicas, xml

BASE = SALIDA / "2041"
DESTINO = SALIDA.parent / "avenida_proyeccion" / "2041"
NODO = "semaforo_caminoreal"
ENTRADA = "av_proyeccion_salida"
SALIDA_AV = "av_proyeccion_entrada"
ACCESOS = ("semaforo_caminoreal_FA", "semaforo_caminoreal_elejercito",
           "semaforo_caminoreal_costanera", ENTRADA)
DESVIO = 0.30
VERDES = (28, 20, 22, 18)
FRACCION_CAMINO_REAL = None


def extender_red():
    base = xml(BASE / "costanera.net.xml")
    donor = "18e7bfe3f81cfffc98f25cd92011b5153c287c31"

    def archivo_sav(extension):
        ruta = f"01_Red_Y_Demanda/ajustes_red/propuesta_savignani.{extension}.xml"
        datos = subprocess.check_output(["git", "show", f"{donor}:{ruta}"])
        return ET.fromstring(re.sub(rb"<!--.*?-->", b"", datos, flags=re.S))

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        filtros = [
            ("nod", "nodes", "node", lambda e: e.get("id") == "av_proyeccion_extremo"),
            ("edg", "edges", "edge", lambda e: e.get("id") in (ENTRADA, SALIDA_AV)),
            ("con", "connections", "connection", lambda e: e.get("from") == ENTRADA
             or e.get("to") == SALIDA_AV),
        ]
        for ext, tag, hijo, coincide in filtros:
            raiz = ET.Element(tag)
            for e in archivo_sav(ext).findall(hijo):
                if coincide(e):
                    raiz.append(e)
            guardar(raiz, tmp / f"avenida.{ext}.xml")
        red_ampliada = tmp / "ampliada.net.xml"
        netconvert = Path(replicas.SUMO).with_name("netconvert.exe")
        subprocess.run(
            [str(netconvert), "-s", str(BASE / "costanera.net.xml"),
             "-n", str(tmp / "avenida.nod.xml"), "-e", str(tmp / "avenida.edg.xml"),
             "-x", str(tmp / "avenida.con.xml"), "--output-file", str(red_ampliada),
             "--tls.rebuild", "true", "--no-turnarounds", "true",
             "--offset.disable-normalization", "true", "--geometry.avoid-overlap", "false",
             "--junctions.corner-detail", "5", "--junctions.limit-turn-speed", "5.5",
             "--internal-junctions.vehicle-width", "3.0", "--rectangular-lane-cut", "false"],
            check=True,
        )
        nueva = xml(red_ampliada)

    nodos = {NODO, "av_proyeccion_extremo"}
    aristas = {ENTRADA, SALIDA_AV}

    def interno(eid):
        return any(eid.startswith(f":{n}_") for n in nodos)

    def conexiones(red):
        origen = {e.get("id") for e in red.findall("edge") if e.get("to") in nodos}
        return [e for e in red.findall("connection")
                if e.get("from") in origen or interno(e.get("from"))]

    antes, despues = conexiones(base), conexiones(nueva)
    antiguos = [c for c in antes if c.get("tl")]
    controlador, = {c.get("tl") for c in antiguos}
    logica, = base.findall(f"tlLogic[@id='{controlador}']")
    con_nuevas = [c for c in despues if c.get("tl")]
    indices = {int(c.get("linkIndex")): c.get("from") for c in con_nuevas}
    if set(indices.values()) != set(ACCESOS) or set(indices) != set(range(len(con_nuevas))):
        raise ValueError(f"Conexiones semafóricas inesperadas: {indices}")
    movimientos = lambda lista: {(c.get("from"), c.get("to"), c.get("fromLane"), c.get("toLane"))
                                  for c in lista if not c.get("from").startswith(":")}
    if movimientos(antes) - movimientos(despues):
        raise ValueError(f"Se perdieron giros existentes: {movimientos(antes) - movimientos(despues)}")
    for c in con_nuevas:
        c.set("tl", controlador)

    for tag, coincide in (
        ("edge", lambda e: e.get("id") in aristas or interno(e.get("id"))),
        ("junction", lambda e: e.get("id") in nodos or interno(e.get("id"))),
        ("connection", lambda e: e in antes or e in despues),
    ):
        anteriores = [e for e in base.findall(tag) if coincide(e)]
        pos = min(list(base).index(e) for e in anteriores)
        for e in anteriores:
            base.remove(e)
        for e in nueva.findall(tag):
            if coincide(e):
                base.insert(pos, e)
                pos += 1
    for fase in list(logica):
        logica.remove(fase)
    for acceso, verde in zip(ACCESOS, VERDES, strict=True):
        for duracion, luz in ((verde, "G"), (3, "y"), (1, "r")):
            estado = "".join(luz if indices[i] == acceso else "r" for i in range(len(indices)))
            ET.SubElement(logica, "phase", duration=str(duracion), state=estado)
    guardar(base, DESTINO / "costanera.net.xml")


def preparar_demanda(origen):
    demanda = xml(origen)
    desvios = {}
    for ruta in demanda.findall("route"):
        tramos = ruta.get("edges").split()
        nueva = None
        if tramos[0] == "fuerzas_armadas_salida" and ACCESOS[0] in tramos:
            nueva = [ENTRADA] + tramos[tramos.index(ACCESOS[0]) + 1:]
        elif tramos[-1] == "fuerzas_armadas_entrada" and "semaforocaminorea_haciaperrokero" in tramos:
            nueva = tramos[:tramos.index("semaforocaminorea_haciaperrokero")] + [SALIDA_AV]
        if nueva:
            rid = ruta.get("id")
            desvios[rid] = rid + "_proy"
            demanda.insert(list(demanda).index(ruta) + 1,
                           ET.Element("route", id=desvios[rid], edges=" ".join(nueva)))
    total = elegible = 0.0
    flujos_elegibles = []
    for flujo in demanda.findall("flow"):
        tasa = float(re.fullmatch(r"exp\(([^)]+)\)", flujo.get("period"))[1])
        segundos_hmd = max(0, min(4500, float(flujo.get("end")))
                           - max(900, float(flujo.get("begin"))))
        total += tasa * segundos_hmd
        rid = flujo.get("route")
        if rid in desvios:
            elegible += tasa * segundos_hmd
            flujos_elegibles.append((flujo, rid, tasa))
    desvio = DESVIO
    if FRACCION_CAMINO_REAL is not None:
        with (BASE / "resumen_replicas.csv").open(encoding="utf-8-sig") as archivo:
            fila, = (fila for fila in csv.DictReader(archivo, delimiter=";")
                     if fila["interseccion"] == "Camino Real"
                     and fila["nivel"] == "INTERSECCION")
        objetivo = FRACCION_CAMINO_REAL * float(fila["demanda_veh_h"])
        desvio = objetivo / elegible
        if not 0 < desvio <= 1:
            raise ValueError("La demanda elegible no permite alcanzar el objetivo")
    for flujo, rid, tasa in flujos_elegibles:
        derivado = ET.Element("flow", flujo.attrib.copy())
        derivado.attrib.update(id=flujo.get("id") + "_proy", route=desvios[rid],
                              period=f"exp({tasa * desvio:.10f})")
        flujo.set("period", f"exp({tasa * (1 - desvio):.10f})")
        demanda.insert(list(demanda).index(flujo) + 1, derivado)
    print(f"En la hora de análisis: demanda vial elegible {elegible:.1f} veh/h, "
          f"desviada {elegible * desvio:.1f} veh/h ({desvio:.1%} de elegibles), "
          f"total {total:.1f} veh/h", flush=True)
    guardar(demanda, DESTINO / origen.name)


def preparar_configuracion():
    config = xml(BASE / "prueba.sumocfg")
    entrada = config.find("input")
    rutas = entrada.find("route-files")
    transporte, demanda = rutas.get("value").split(",")
    preparar_demanda(BASE / demanda)
    rutas.set("value", f"{(BASE / transporte).as_posix()},{demanda}")
    adicionales = entrada.find("additional-files")
    nuevos = []
    for origen in map(Path, adicionales.get("value").split(",")):
        if origen.name.startswith("detectores_intersecciones"):
            detectores = xml(BASE / origen)
            e3 = detectores.find("e3Detector[@id='e3_Camino_Real']")
            red = xml(DESTINO / "costanera.net.xml")
            for tag, eid, pos in (("detEntry", ENTRADA, -299), ("detExit", SALIDA_AV, 60)):
                for carril in red.find(f"edge[@id='{eid}']").findall("lane"):
                    ET.SubElement(e3, tag, lane=carril.get("id"), pos=str(pos), friendlyPos="true")
            d = detectores.find("edgeData[@id='accesos']")
            d.set("edges", d.get("edges") + f" {ENTRADA}")
            guardar(detectores, DESTINO / origen.name)
            nuevos.append(origen.name)
        else:
            nuevos.append((BASE / origen).as_posix())
    adicionales.set("value", ",".join(nuevos))
    guardar(config, DESTINO / "prueba.sumocfg")

    mapa = (BASE / "accesos_intersecciones.csv").read_text(encoding="utf-8-sig")
    with (DESTINO / "accesos_intersecciones.csv").open("w", encoding="utf-8-sig") as f:
        f.write(mapa + f"Camino Real;Este (Av. En Proyeccion);principal;{ENTRADA};{ENTRADA};300\n")


def ejecutar():
    DESTINO.mkdir(parents=True, exist_ok=True)
    extender_red()
    preparar_configuracion()
    replicas.rr.RED = str(DESTINO / "costanera.net.xml")
    replicas.rr.MAPA = replicas.cap.MAPA = str(DESTINO / "accesos_intersecciones.csv")
    replicas.adicionales_aislados = adicionales_para_replicas
    procesar = replicas.rr.main
    with (DESTINO / "diagnostico_semillas.csv").open("w", encoding="utf-8", newline="") as f:
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
        replicas.main(5, str(DESTINO / "prueba.sumocfg"), str(DESTINO), str(DESTINO))


if __name__ == "__main__":
    opcion = sys.argv[1] if len(sys.argv) > 1 else "30"
    if opcion == "15":
        DESVIO = 0.15
        DESTINO = SALIDA.parent / "avenida_proyeccion_15" / "2041"
    elif opcion in ("camino_real", "camino_real_reparto"):
        FRACCION_CAMINO_REAL = 0.30
        nombre = "avenida_proyeccion_30_camino_real"
        if opcion == "camino_real_reparto":
            VERDES = (22, 24, 28, 14)
            nombre += "_reparto"
        DESTINO = SALIDA.parent / nombre / "2041"
    elif opcion != "30":
        raise ValueError("Indique 15, 30, camino_real o camino_real_reparto")
    ejecutar()
