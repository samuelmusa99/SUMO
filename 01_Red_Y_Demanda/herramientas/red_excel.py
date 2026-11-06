"""
Hace que un Excel de resultados (.xlsm) lea la red desde su propia carpeta y no desde 01_Red_Y_Demanda.

La consulta "costanera net" (hoja Tramos, longitudes para la densidad) leia 01_Red_Y_Demanda\\costanera.net.xml, que es
la red de la rama de git que este activa: al abrir el Excel de una propuesta con otra rama, la macro lo refrescaba con
la red equivocada. Con este cambio lee <carpeta del Excel>\\costanera.net.xml, que el .bat copia en cada corrida.

Uso: python red_excel.py <libro.xlsm>   (el libro debe estar cerrado; la red debe estar ya en su carpeta)
"""
import os
import shutil
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from copiar_excel import reemplazar_mashup  # noqa: E402

RED_COMPARTIDA = r'C:\Users\samue_yffy\Desktop\SUMO\01_Red_Y_Demanda\costanera.net.xml'


def main(libro):
    libro = os.path.abspath(libro)
    carpeta = os.path.dirname(libro)
    nueva = os.path.join(carpeta, 'costanera.net.xml')
    if not os.path.exists(nueva):
        sys.exit(f'ERROR: falta {nueva} (copiar primero la red de la propuesta)')
    temporal = libro + '.tmp'
    cambios = 0
    with zipfile.ZipFile(libro) as zin, zipfile.ZipFile(temporal, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            contenido = zin.read(info.filename)
            if info.filename.startswith('customXml/item') and b'D\x00a\x00t\x00a\x00M\x00a\x00s\x00h\x00u\x00p' in contenido:
                contenido, n = reemplazar_mashup(contenido, RED_COMPARTIDA, nueva)
                cambios += n
            zout.writestr(info, contenido)
    if not cambios:
        os.remove(temporal)
        sys.exit(f'{libro}: la consulta ya no lee la red compartida (sin cambios)')
    shutil.move(temporal, libro)
    print(f'{libro}: la red se lee ahora desde {nueva}')


if __name__ == '__main__':
    main(sys.argv[1])
