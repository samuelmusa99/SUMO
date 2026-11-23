"""Poligono del puente de Perozo para el SUMO-GUI -> distribuidor.add.xml (igual que en la rama de Savignani).

Sirve solo para ver en el GUI que vehiculos van por el puente y cuales por debajo: un area gris (mismo color y capa que el
de Savignani) que cubre los dos carriles del puente (3,70 m, Cuadro 5.1) y la isla entre ellos, desde el pie de una rampa
hasta el pie de la otra. No cambia la simulacion.
Uso: python poligono_puente_perozo.py   (volver a ejecutarlo si cambia la red)
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.environ.get('SUMO_HOME', r'C:\SUMO'), 'tools'))
import sumolib  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
RED = os.path.join(AQUI, '..', 'costanera.net.xml')
SALIDA = os.path.join(AQUI, '..', 'distribuidor.add.xml')
MEDIO_CARRIL = 3.70 / 2


def eje(net, sentido):
    """centro del carril del puente desde el pie de la rampa de subida hasta el pie de la de bajada (cota > 0)"""
    P = []
    for t in (f'puente_subida_hacia_{sentido}', f'puente_hacia_{sentido}', f'puente_bajada_hacia_{sentido}'):
        for p in net.getEdge(t).getLanes()[0].getShape3D():
            if not P or math.dist(P[-1][:2], p[:2]) > 0.01:
                P.append(p)
    i0 = max(i for i, p in enumerate(P) if p[2] == 0 and i < len(P) // 2)
    i1 = min(i for i, p in enumerate(P) if p[2] == 0 and i > len(P) // 2)
    return [p[:2] for p in P[i0:i1 + 1]]


def desplazar(P, d):
    """polilinea paralela a d m a la derecha del sentido de circulacion"""
    Q = []
    for i, p in enumerate(P):
        a, b = P[max(i - 1, 0)], P[min(i + 1, len(P) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        Q.append((p[0] + d * dy / n, p[1] - d * dx / n))
    return Q


def main():
    net = sumolib.net.readNet(RED)
    sur, norte = eje(net, 'sur'), eje(net, 'norte')
    # cada carril del puente esta en el carril izquierdo de su sentido: el borde exterior de la estructura queda a la
    # derecha de cada carril; la isla central queda entre los dos
    separacion = sum(math.dist(p, q) for p, q in ((sur[0], norte[-1]), (sur[-1], norte[0]))) / 2
    contorno = desplazar(sur, MEDIO_CARRIL) + desplazar(norte, MEDIO_CARRIL)
    forma = ' '.join(f'{x:.2f},{y:.2f}' for x, y in contorno + contorno[:1])
    with open(SALIDA, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<!-- Generado por ajustes_red/poligono_puente_perozo.py: puente de Perozo sobre FFAA en Perrokero (solo para '
                'el SUMO-GUI). -->\n'
                '<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                'xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">\n'
                f'    <poly id="distribuidor" color="131,139,139" fill="1" layer="5.00" shape="{forma}"/>\n'
                '</additional>\n')
    print(f'distribuidor.add.xml: ejes de los carriles a {separacion:.2f} m, ancho {separacion + 2 * MEDIO_CARRIL:.2f} m, '
          f'largo {sum(math.dist(a, b) for a, b in zip(sur, sur[1:])):.1f} m')


if __name__ == '__main__':
    main()
