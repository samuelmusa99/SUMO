"""Sensibilidad 2026 de entradas y salidas de Bissau y Puerto Guaica."""
from collections import defaultdict
import re
import sys
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
from probar_sensibilidad_av_rio import ejecutar

OBJETIVO = {
    "entrada:bissau:1": 90,
    "salida_bissau_1": 90,
    "entrada_puerto_guaica": 120,
    "salida:puerto_guaica": 90,
}
ACCESOS_FIJOS = {"avrio_1", "fernandez_padilla", "-335982664#1",
                "entrada_bissau_2", "salida_bissau_2"}
RETORNOS_FIJOS = {
    ("costanera_puerto_guaica_hacialecheria", "592256719#6"),
    ("costanera_puerto_guaica_haciacaminoreal", "172344969#4"),
}


def ajustar_demanda(datos, destino):
    raiz = ET.fromstring(datos)
    rutas = {r.get("id"): r.get("edges").split() for r in raiz.findall("route")}
    total = defaultdict(float)
    fijo = defaultdict(float)
    flujos = defaultdict(list)
    for flujo in raiz.findall("flow"):
        ruta = rutas[flujo.get("route")]
        conjunto = OBJETIVO.keys() & set(ruta)
        if not conjunto:
            continue
        tasa = float(re.fullmatch(r"exp\(([^)]+)\)", flujo.get("period"))[1])
        duracion = max(0.0, min(4500, float(flujo.get("end"))) -
                       max(900, float(flujo.get("begin"))))
        for acceso in conjunto:
            total[acceso] += tasa * duracion
            if (len(conjunto) > 1 or ACCESOS_FIJOS.intersection(ruta)
                    or RETORNOS_FIJOS.intersection(zip(ruta, ruta[1:]))):
                fijo[acceso] += tasa * duracion
            else:
                flujos[acceso].append((flujo, tasa, duracion))
    for acceso, meta in OBJETIVO.items():
        factor = (meta - fijo[acceso]) / (total[acceso] - fijo[acceso])
        resultado = fijo[acceso]
        for flujo, tasa, duracion in flujos[acceso]:
            nueva_tasa = f"{tasa * factor:.10f}"
            flujo.set("period", f"exp({nueva_tasa})")
            resultado += float(nueva_tasa) * duracion
        assert abs(resultado - meta) < 0.001, (acceso, resultado)
        print(f"{acceso}: de {total[acceso]:.2f} a {resultado:.2f} veh/h", flush=True)
    ET.ElementTree(raiz).write(destino, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    ejecutar(sys.argv[1], ajustar=ajustar_demanda, carpeta="sensibilidad_accesos_locales_aislada",
             archivo_demanda="demanda_accesos_locales.rou.xml")
