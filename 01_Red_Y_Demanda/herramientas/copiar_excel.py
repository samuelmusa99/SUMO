"""
Copia un Excel de resultados (.xlsm) cambiando la carpeta de la que leen sus consultas de Power Query.

Las consultas leen los CSV con ruta absoluta (p. ej. EXCEL RESULTADOS\\BASE_2026\\reporte_viajes.csv). Este script copia el
libro y reemplaza esa carpeta en las consultas (DataMashup) y en la ruta guardada del libro. Los datos de la copia son
los del libro original hasta que se actualicen (Datos > Actualizar todo) con los CSV de la nueva carpeta.

Uso: python copiar_excel.py <libro_original.xlsm> <libro_nuevo.xlsm> <carpeta_original> <carpeta_nueva>
  El libro original debe estar cerrado.
"""
import base64
import io
import re
import struct
import sys
import zipfile


def reemplazar_mashup(xml_utf16, viejo, nuevo):
    texto = xml_utf16.decode('utf-16')
    b64 = re.search(r'>([A-Za-z0-9+/=]+)<', texto).group(1)
    datos = base64.b64decode(b64)
    version, largo = struct.unpack('<II', datos[:8])
    paquete, resto = datos[8:8 + largo], datos[8 + largo:]
    entrada, salida = zipfile.ZipFile(io.BytesIO(paquete)), io.BytesIO()
    cambios = 0
    with zipfile.ZipFile(salida, 'w', zipfile.ZIP_DEFLATED) as z:
        for info in entrada.infolist():
            contenido = entrada.read(info.filename)
            if info.filename.endswith('.m'):
                m = contenido.decode('utf-8')
                cambios += m.count(viejo)
                contenido = m.replace(viejo, nuevo).encode('utf-8')
            z.writestr(info, contenido)
    nuevo_paquete = salida.getvalue()
    datos = struct.pack('<II', version, len(nuevo_paquete)) + nuevo_paquete + resto
    texto = texto.replace(b64, base64.b64encode(datos).decode('ascii'))
    return texto.encode('utf-16'), cambios


def main(origen, destino, viejo, nuevo):
    viejo, nuevo = viejo.rstrip('\\') + '\\', nuevo.rstrip('\\') + '\\'
    cambios = 0
    with zipfile.ZipFile(origen) as zin, zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            contenido = zin.read(info.filename)
            if info.filename.startswith('customXml/item') and b'D\x00a\x00t\x00a\x00M\x00a\x00s\x00h\x00u\x00p' in contenido:
                contenido, n = reemplazar_mashup(contenido, viejo, nuevo)
                cambios += n
            elif info.filename == 'xl/workbook.xml':
                contenido = contenido.replace(viejo.encode('utf-8'), nuevo.encode('utf-8'))
            zout.writestr(info, contenido)
    print(f'{destino}: {cambios} rutas de consulta cambiadas a {nuevo}')
    if not cambios:
        sys.exit('ERROR: no se encontro la carpeta original en las consultas')


if __name__ == '__main__':
    main(*sys.argv[1:5])
