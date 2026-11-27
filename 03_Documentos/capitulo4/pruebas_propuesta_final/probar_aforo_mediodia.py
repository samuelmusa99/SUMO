"""Contraste aislado del aforo manual del 27 de noviembre de 2026."""
import csv
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
import probar_retornos_puerto_guaica as retornos
from probar_sensibilidad_av_rio import ejecutar

OBJETIVOS = {
    "entrada:bissau:1": 192, "salida_bissau_1": 108,
    "entrada_puerto_guaica": 72, "salida:puerto_guaica": 36,
    "fernandez_padilla": 84, "-335982664#1": 12, "salida_bissau_2": 48,
}
PASOS = {
    "Bissau recto hacia Barcelona": ("costanera_bissau_haciacaminoreal", "592256719#4"),
    "Bissau recto hacia Lecheria": ("costanera_bissau_hacialecheria", "172344969#9"),
    "Puerto Guaica recto hacia Barcelona": ("costanera_puerto_guaica_haciacaminoreal", "592256719#6"),
    "Puerto Guaica recto hacia Lecheria": ("costanera_puerto_guaica_hacialecheria", "172344969#4"),
}


def copiar(datos, destino):
    Path(destino).write_bytes(datos)


def ajustar_accesos(datos, destino):
    red = ET.fromstring(datos)
    rutas = {r.get("id"): r.get("edges").split() for r in red.findall("route")}
    ruta_galpones = rutas["r_L037"]
    pasos = ["salida_bissau_2", *ruta_galpones[ruta_galpones.index("592256719#4"):]]
    red.insert(len(rutas), ET.Element("route", id="campo_galpones", edges=" ".join(pasos)))
    rutas["campo_galpones"] = pasos
    flujos = red.findall("flow")
    origen = next(f for f in flujos if f.get("route") == "r_L037")
    nuevo = ET.Element("flow", origen.attrib.copy())
    nuevo.set("id", "campo_galpones")
    nuevo.set("route", "campo_galpones")
    nuevo.set("begin", "0")
    nuevo.set("end", "4500")
    nuevo.set("period", "exp(0.01)")
    red.insert(list(red).index(origen) + 1, nuevo)
    flujos = red.findall("flow")

    for acceso, meta in OBJETIVOS.items():
        variables = []
        fijo = 0.0
        for f in flujos:
            asociados = OBJETIVOS.keys() & set(rutas[f.get("route")])
            if asociados == {acceso}:
                variables.append(f)
            elif acceso in asociados:
                fijo += retornos.volumen(f)
        subtotal = sum(map(retornos.volumen, variables))
        assert subtotal > 0 and meta > fijo, (acceso, subtotal, fijo)
        factor = (meta - fijo) / subtotal
        for f in variables:
            tasa = float(f.get("period")[4:-1])
            f.set("period", f"exp({tasa * factor:.12f})")
        assert abs(fijo + sum(map(retornos.volumen, variables)) - meta) < 0.001
        print(f"{acceso}: {fijo + subtotal:.2f} -> {meta} veh/h", flush=True)

    ET.ElementTree(red).write(destino, encoding="utf-8", xml_declaration=True)


def ajustar_con_retornos(datos, destino):
    retornos.ajuste_local = ajustar_accesos
    retornos.SENTIDOS = tuple((*sentido[:3], 36, *sentido[4:]) for sentido in retornos.SENTIDOS)
    retornos.ajustar_retornos(datos, destino)


def observar(replica, carpeta, salida):
    retornos.observar(replica, carpeta, salida)
    mediciones = {e: 0 for e in OBJETIVOS}
    mediciones.update(dict.fromkeys(PASOS, 0))
    nombres_pasos = {paso: nombre for nombre, paso in PASOS.items()}
    for vehiculo in ET.parse(carpeta / "reporte_rutas.xml").getroot().findall("vehicle"):
        ruta = vehiculo.find("route")
        if ruta is None:
            continue
        edges = ruta.get("edges").split()
        for i, tiempo in enumerate(ruta.get("exitTimes", "").split()):
            if tiempo == "-1" or not 900 <= float(tiempo) < 4500:
                continue
            actual = edges[i]
            if actual in OBJETIVOS:
                mediciones[actual] += 1
            if i + 1 < len(edges):
                nombre = nombres_pasos.get((actual, edges[i + 1]))
                if nombre:
                    mediciones[nombre] += 1
    archivo = salida / "movimientos_atendidos_por_semilla.csv"
    con_cabecera = replica == "replica1"
    with archivo.open("w" if con_cabecera else "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        if con_cabecera:
            writer.writerow(("replica", "movimiento", "vehiculos_atendidos"))
        writer.writerows((replica, e, n) for e, n in mediciones.items())


if __name__ == "__main__":
    opcion = sys.argv[1]
    ajustes = {"control": copiar, "accesos": ajustar_accesos, "accesos_y_retornos": ajustar_con_retornos}
    ejecutar("base", ajustar=ajustes[opcion], carpeta=f"aforo_mediodia_2026-11-27/{opcion}",
             archivo_demanda="demanda.rou.xml", observar=observar)
