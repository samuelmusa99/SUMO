"""Prueba un ciclo de 120 s en Camino Real y conserva el plan de Perrokero."""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from probar_camino_real import CARPETA, ejecutar, replicas

# Los 108 s de verde conservan aproximadamente el reparto 28/20/22.
VERDES = (43, 31, 34)
SALIDA = CARPETA / "coordinacion"
adicionales_originales = replicas.adicionales_aislados


def adicionales_para_replicas(config, temporal):
    """Omite la salida de densidad que el resumen de réplicas no consume."""
    return [ruta for ruta in adicionales_originales(config, temporal)
            if Path(ruta).name not in {"medidores.add.xml", "medidores_2041.add.xml"}]


if __name__ == "__main__":
    anio, segundo = sys.argv[1:]
    desfase = int(segundo)
    if not 0 <= desfase < 120:
        raise ValueError("El desfase debe estar entre 0 y 119 s")
    replicas.adicionales_aislados = adicionales_para_replicas
    ejecutar(f"desfase_{desfase:03}", anio, verdes=VERDES, ciclo=120,
             desfase=desfase, carpeta=SALIDA)
