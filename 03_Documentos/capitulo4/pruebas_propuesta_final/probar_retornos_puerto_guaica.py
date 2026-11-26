"""Contrasta la base con demanda local elevada con y sin retornos observados."""
import csv
import io
import sys
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
from probar_sensibilidad_accesos_locales import ajustar_demanda as ajuste_local
from probar_sensibilidad_av_rio import ejecutar

LECHERIA = "costanera_puerto_guaica_hacialecheria"
CAMINO_REAL = "costanera_puerto_guaica_haciacaminoreal"
SENTIDOS = (
    (LECHERIA, "592256719#6", "172344969#4", 120, ("r_L000", "r_L005"), "r_L010"),
    (CAMINO_REAL, "172344969#4", "592256719#6", 60, ("r_L002", "r_L010"), "r_L000"),
)


def volumen(flujo):
    inicio = max(900, float(flujo.get("begin")))
    fin = min(4500, float(flujo.get("end")))
    return float(flujo.get("period")[4:-1]) * max(0, fin - inicio)


def ajustar_retornos(datos, destino):
    buffer = io.BytesIO()
    ajuste_local(datos, buffer)
    red = ET.fromstring(buffer.getvalue())
    rutas = {r.get("id"): r.get("edges").split() for r in red.findall("route")}
    flujos = red.findall("flow")
    demanda_antes = sum(volumen(f) for f in flujos)
    for entrada, salida, recto, objetivo, donantes, referencia in SENTIDOS:
        existente = sum(volumen(f) for f in flujos if
                        (entrada, salida) in zip(rutas[f.get("route")], rutas[f.get("route")][1:]))
        elegibles = [f for f in flujos if f.get("route") in donantes]
        factor = (objetivo - existente) / sum(volumen(f) for f in elegibles)
        assert 0 < factor < 1
        sufijo = rutas[referencia][rutas[referencia].index(salida):]
        for rid in donantes:
            pasos = rutas[rid]
            assert pasos[pasos.index(entrada) + 1] == recto
            nueva = pasos[:pasos.index(entrada) + 1] + sufijo
            red.insert(len(rutas), ET.Element("route", id=rid + "_retorno", edges=" ".join(nueva)))
            rutas[rid + "_retorno"] = nueva
        for f in elegibles:
            tasa = float(f.get("period")[4:-1])
            nueva = ET.Element("flow", f.attrib.copy())
            nueva.attrib.update(id=f.get("id") + "_retorno", route=f.get("route") + "_retorno",
                                period=f"exp({tasa * factor:.10f})")
            f.set("period", f"exp({tasa * (1 - factor):.10f})")
            red.insert(list(red).index(f) + 1, nueva)
        verificacion = sum(volumen(f) for f in red.findall("flow") if
                           (entrada, salida) in zip(rutas[f.get("route")], rutas[f.get("route")][1:]))
        assert abs(verificacion - objetivo) < 0.001
        print(f"{entrada}: {existente:.2f} a {verificacion:.2f} retornos/h", flush=True)
    assert abs(sum(volumen(f) for f in red.findall("flow")) - demanda_antes) < 0.001
    ET.ElementTree(red).write(destino, encoding="utf-8", xml_declaration=True)


def observar(replica, carpeta, salida):
    ejes = {entrada: siguiente for entrada, siguiente, *_ in SENTIDOS}
    ego = {e + "_1": e for e in ejes}
    cuentas = {e: 0 for e in ejes}
    maximos = {e: 0.0 for e in ejes}
    sumas = {e: 0.0 for e in ejes}
    instantes = 0
    for _, elemento in ET.iterparse(carpeta / "reporte_colas.xml", events=["end"]):
        if elemento.tag != "data":
            continue
        if 900 <= float(elemento.get("timestep")) < 4500:
            instantes += 1
            for carril in elemento.iter("lane"):
                eje = ego.get(carril.get("id"))
                if eje:
                    cola = float(carril.get("queueing_length"))
                    sumas[eje] += cola
                    maximos[eje] = max(maximos[eje], cola)
        elemento.clear()
    for v in ET.parse(carpeta / "reporte_rutas.xml").getroot().findall("vehicle"):
        ruta = v.find("route")
        if ruta is None:
            continue
        aristas = ruta.get("edges").split()
        tiempos = ruta.get("exitTimes", "").split()
        for i, (eje, siguiente) in enumerate(zip(aristas, aristas[1:])):
            if ejes.get(eje) == siguiente and i < len(tiempos) and 900 <= float(tiempos[i]) < 4500:
                cuentas[eje] += 1
    ruta_csv = salida / "retornos_y_colas_por_semilla.csv"
    with ruta_csv.open("w" if replica == "replica1" else "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        if replica == "replica1":
            w.writerow(("replica", "acceso", "retornos_atendidos", "cola_media_izquierda_m",
                        "cola_maxima_izquierda_m"))
        for eje in ejes:
            w.writerow((replica, eje, cuentas[eje], round(sumas[eje] / instantes, 2),
                        round(maximos[eje], 2)))


if __name__ == "__main__":
    opcion = sys.argv[1]
    if opcion not in ("control", "retornos"):
        raise ValueError("Use control o retornos")
    ejecutar("base", ajustar=ajuste_local if opcion == "control" else ajustar_retornos,
             carpeta=f"sensibilidad_retornos_puerto_guaica/{opcion}",
             archivo_demanda="demanda.rou.xml", observar=observar)
