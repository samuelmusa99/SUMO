"""Genera 'INFORMACION CAPITULO IV - ESCENARIO BASE.docx' con los datos de la simulacion base (2026 y 2041)."""
import csv
import json
import os
import subprocess

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

AQUI = os.path.dirname(os.path.abspath(__file__))
X = r'C:\Users\samue_yffy\Desktop\EXCEL RESULTADOS'
SALIDA = r'C:\Users\samue_yffy\Desktop\TRABAJO DE GRADO\INFORMACION CAPITULO IV - ESCENARIO BASE.docx'


def leer(ruta):
    return list(csv.DictReader(open(ruta, encoding='utf-8-sig'), delimiter=';'))


def git_csv(ruta):
    txt = subprocess.run(['git', '-C', r'C:\Users\samue_yffy\Desktop\SUMO', 'show', f'main:{ruta}'],
                         capture_output=True, text=True, encoding='utf-8').stdout
    return list(csv.DictReader(txt.lstrip('\ufeff').splitlines(), delimiter=';'))


REP = os.path.join(AQUI, 'replicas_anchos_tesis')
rep26 = leer(os.path.join(REP, '2026', 'resumen_replicas.csv'))
rep41 = leer(os.path.join(REP, '2041', 'resumen_replicas.csv'))
geh = git_csv('01_Red_Y_Demanda/demanda/ajuste_demanda_base.csv')


def fila(rep, inter, acceso='(todos)'):
    return next(r for r in rep if r['interseccion'] == inter and r['acceso'] == acceso)


def n(x, d=0):
    """numero con coma decimal y punto de miles"""
    if x in (None, ''):
        return '-'
    s = f'{float(x):,.{d}f}'
    return s.replace(',', '§').replace('.', ',').replace('§', '.')


# ------------------------------------------------------------------ documento
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.59), Cm(27.94)
sec.left_margin, sec.right_margin, sec.top_margin, sec.bottom_margin = Cm(3), Cm(2.5), Cm(2.5), Cm(2.5)
st = doc.styles['Normal']
st.font.name = 'Times New Roman'
st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
st.font.size = Pt(12)
st.paragraph_format.space_after = Pt(6)
for h, tam in (('Heading 1', 14), ('Heading 2', 13), ('Heading 3', 12)):
    s = doc.styles[h]
    s.font.name = 'Times New Roman'
    s.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    s.font.size = Pt(tam)
    s.font.bold = True
    s.font.color.rgb = RGBColor(0, 0, 0)
    rf = s.element.rPr.rFonts
    for att in ('w:asciiTheme', 'w:hAnsiTheme', 'w:eastAsiaTheme', 'w:cstheme'):
        if rf.get(qn(att)) is not None:
            del rf.attrib[qn(att)]


def p(texto, negrita=False, cursiva=False, tam=None, centro=False):
    par = doc.add_paragraph()
    r = par.add_run(texto)
    r.bold, r.italic = negrita, cursiva
    if tam:
        r.font.size = Pt(tam)
    if centro:
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return par


def vineta(texto):
    par = doc.add_paragraph(texto, style='List Bullet')
    par.paragraph_format.space_after = Pt(2)
    return par


def nota(texto):
    par = doc.add_paragraph()
    r = par.add_run('Nota para la redacción: ')
    r.bold = True
    r.font.size = Pt(10)
    r2 = par.add_run(texto)
    r2.font.size = Pt(10)
    sombra(par, 'EEF3F8')


def sombra(par, color):
    ppr = par._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color)
    ppr.append(shd)


def celda_fondo(celda, color):
    tcpr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color)
    tcpr.append(shd)


def cuadro(titulo, encabezado, filas, anchos, fuente='Fuente: El autor (2026), a partir de la simulación en SUMO.', tam=9):
    t = p(titulo, negrita=True, tam=11)
    t.paragraph_format.keep_with_next = True
    tab = doc.add_table(rows=1, cols=len(encabezado))
    tab.style = 'Table Grid'
    tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(encabezado):
        c = tab.rows[0].cells[i]
        c.text = ''
        r = c.paragraphs[0].add_run(h)
        r.bold = True
        r.font.size = Pt(tam)
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        celda_fondo(c, 'D9E2EC')
    # repetir encabezado en cada pagina
    trpr = tab.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement('w:tblHeader')
    th.set(qn('w:val'), 'true')
    trpr.append(th)
    for fila in filas:
        celdas = tab.add_row().cells
        for i, v in enumerate(fila):
            celdas[i].text = ''
            r = celdas[i].paragraphs[0].add_run(str(v))
            r.font.size = Pt(tam)
            celdas[i].paragraphs[0].paragraph_format.space_after = Pt(0)
            if i > 0 and len(str(v)) <= 12:
                celdas[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for fila in tab.rows:
        for i, a in enumerate(anchos):
            fila.cells[i].width = Cm(a)
    f = p(fuente, cursiva=True, tam=9)
    f.paragraph_format.space_after = Pt(12)
    return tab



# ------------------------------------------------------------------ valores que se citan en el texto
I26 = {r['interseccion']: r for r in rep26 if r['nivel'] == 'INTERSECCION'}
I41 = {r['interseccion']: r for r in rep41 if r['nivel'] == 'INTERSECCION'}
R26 = {r['acceso']: r for r in rep26 if r['nivel'] == 'RED'}
R41 = {r['acceso']: r for r in rep41 if r['nivel'] == 'RED'}


def d(rep, inter, acceso='(todos)'):
    r = fila(rep, inter, acceso)
    return f"{r['LOS_HCM']}, {n(r['demora_promedio_s'], 1)} s"


# ------------------------------------------------------------------ portada
p('INFORMACIÓN PARA EL CAPÍTULO IV', negrita=True, tam=16, centro=True)
p('PRESENTACIÓN Y ANÁLISIS DE RESULTADOS', negrita=True, tam=14, centro=True)
p('Escenario base (sin proyecto): situación actual 2026 y horizonte futuro 2041', tam=12, centro=True)
p('Objetivos específicos 1 y 2', cursiva=True, centro=True)
p('')
p('Este documento reúne los datos, cuadros y resultados de la simulación en SUMO del escenario sin proyecto, '
  'organizados según los indicadores del Cuadro 1.2 (Operacionalización de las variables), siguiendo la estructura '
  'del capítulo IV de Estanga y Savignani (2021) y de Assouad y Peroza (2022). Los cuadros pueden copiarse tal cual; '
  'los recuadros sombreados son notas para la redacción y no forman parte del texto de la tesis. '
  'Los resultados de las propuestas (objetivos 3 y 4) se entregarán en un documento aparte.')
p('Fuente de los datos: simulación en SUMO 1.26 (todos los resultados son el promedio de 5 réplicas), trabajo de campo '
  'del 07/04/2026 y capítulo IV de las tesis evaluadas. Cifras con coma decimal.', cursiva=True, tam=10)

# ------------------------------------------------------------------ resumen de indicadores
doc.add_heading('Resumen: indicadores del Cuadro 1.2 y dónde se presentan', level=1)
vcs = [float(r['VC']) for r in I26.values()]
cuadro('Cuadro 4.0 Indicadores de los objetivos 1 y 2 en el escenario base',
       ['Variable', 'Dimensión', 'Indicador', 'Resultado principal', 'Cuadro'],
       [['Parámetros y variables de diseño vial', 'Características geométricas y de control', 'Ancho de calzada, carriles, isla y acera (m)',
         'Carriles de 3,00 a 3,92 m; calzadas de 6,0 a 10,1 m por sentido', '4.2'],
        ['', '', 'Número de carriles', '1 a 3 carriles por acceso', '4.2'],
        ['', '', 'Ubicación de señalización vial', 'Inventario de señales, pasos peatonales y paradas por intersección', '4.3'],
        ['', '', 'Tiempos de ciclos y fases semafóricas (s)', 'Camino Real: ciclo de 82 s (3 fases); CC Paos: ciclo de 66 s (3 fases)', '4.4'],
        ['Desempeño operativo del tránsito', 'Calidad del flujo vehicular', 'Volumen vehicular',
         f"Demanda 2026 de {n(sum(float(r['demanda_veh_h']) for r in I26.values()))} veh/h en las 5 intersecciones", '4.7 a 4.9'],
        ['', '', 'Capacidad vial y relación V/C', f"V/C crítica 2026: de {n(min(vcs), 2)} a {n(max(vcs), 2)}", '4.10 y 4.12'],
        ['', '', 'Velocidad media de circulación', f"Red: {n(R26['TOTAL']['velocidad_media_kmh'], 1)} km/h (2026) y {n(R41['TOTAL']['velocidad_media_kmh'], 1)} km/h (2041)", '4.10, 4.12 y 4.13'],
        ['', '', 'Demora promedio por vehículo', f"Perrokero {d(rep26, 'Perrokero')}; Camino Real {d(rep26, 'Camino Real')}; CC Paos {d(rep26, 'CC Paos')}", '4.9 a 4.12'],
        ['', '', 'Longitud de cola promedio y máxima (m)', 'Por acceso, 2026 y 2041', '4.10 y 4.12']],
       [3.2, 3.0, 3.6, 5.3, 1.4])
nota('Las tesis evaluadas no reportan radios de giro ni hombrillos (son avenidas urbanas con brocal); solo dan calzada, '
     'carriles, brocal, isla y acera. Por eso, en el Cuadro 1.2 conviene cambiar el indicador "Ancho de calzada, carriles '
     'y hombrillos" por "Ancho de calzada, carriles, isla y acera", y "Radios de giro y número de carriles" por "Número '
     'de carriles".')

# ------------------------------------------------------------------ 4.1
doc.add_heading('4.1 Parámetros y variables de diseño vial (objetivo específico 1)', level=1)
doc.add_heading('4.1.1 Área de estudio e intersecciones que intervienen', level=2)
p('El eje en estudio está formado por la Av. La Costanera, desde el cruce con la Av. Fabricio Ojeda (CC Paos) hasta el '
  'cruce con la Prolongación Av. El Ejército y la Av. Fuerzas Armadas (Camino Real), y por la Av. Fuerzas Armadas hasta '
  'su cruce con la Av. Río (Perrokero). Sobre la Costanera se encuentran además los accesos a la Residencia Bissau y a '
  'la Residencia Puerto Guaica - sector Fernández Padilla. En la red simulada, el recorrido por la Costanera desde CC Paos '
  'hasta Camino Real mide 1.387 m y el tramo de la Av. Fuerzas Armadas entre Camino Real y Perrokero, 618 m.')
cuadro('Cuadro 4.1 Intersecciones del eje en estudio',
       ['Intersección', 'Vías que se cruzan', 'Tipo', 'Control', 'Accesos'],
       [['Camino Real', 'Av. La Costanera, Prolong. Av. El Ejército y Av. Fuerzas Armadas', 'T con giro libre (curva Costanera - El Ejército)', 'Semáforo (3 fases)', '3'],
        ['CC Paos', 'Av. La Costanera y Av. Fabricio Ojeda', 'T con giros libres', 'Semáforo (3 fases)', '3'],
        ['Perrokero', 'Av. Fuerzas Armadas y Av. Río (con acceso residencial)', 'Cruz', 'Sin semáforo (prioridad FFAA)', '4'],
        ['Bissau', 'Av. La Costanera y accesos Residencia Bissau / galpones', 'Acceso con abertura en la isla central', 'Sin semáforo', '4'],
        ['Puerto Guaica', 'Av. La Costanera, Residencia Puerto Guaica y sector Fernández Padilla', 'Cruz (abertura en la isla central)', 'Sin semáforo', '4']],
       [2.4, 5.0, 3.6, 2.8, 1.5], fuente='Fuente: El autor (2026), a partir de la inspección de campo y la red vial modelada.')

doc.add_heading('4.1.2 Características geométricas', level=2)
p('El Cuadro 4.2 resume la sección transversal de cada vía tal como se representó en el modelo. Los anchos se tomaron '
  'de las tesis evaluadas: Estanga y Savignani (2021), Tablas 25 y 26 y Fig. 84, para Camino Real y CC Paos; y Assouad '
  'y Peroza (2022), Cuadros 4.1 y 4.2, para Perrokero. El número de carriles es el observado en campo.')
geo = [
    ['Camino Real', 'Av. La Costanera, llegada', '2', '3,70', '7,40', '1,30', '2,04', 'Savignani, T. 25 y Fig. 84'],
    ['', 'Av. La Costanera, salida', '2', '3,70', '7,40', '1,30', '2,25', 'Savignani, Fig. 84'],
    ['', 'Canal de giro libre Costanera - El Ejército', '1', '6,30', '6,30', '-', '-', 'Savignani, Fig. 84'],
    ['', 'Av. Fuerzas Armadas, llegada', '2', '3,75', '7,50', 'No dividida', '2,25', 'Savignani, T. 25 y Fig. 84'],
    ['', 'Av. Fuerzas Armadas, salida', '3 (*)', '3,75', '11,25', 'No dividida', '1,50', 'Savignani: 2 de 3,75 m'],
    ['', 'Prolong. Av. El Ejército, llegada', '3 (*)', '3,37', '10,10', '1,30', '2,60', 'Savignani: 2 de 5,05 m'],
    ['', 'Prolong. Av. El Ejército, salida', '2', '3,70', '7,40', '1,30', '2,60', 'Savignani, Fig. 84'],
    ['CC Paos', 'Av. La Costanera (ambos sentidos)', '2', '3,75', '7,50', '1,30', '2,60', 'Savignani, T. 26'],
    ['', 'Av. Fabricio Ojeda, llegada', '2', '3,70', '7,40', '1,70', '2,60', 'Savignani, T. 26'],
    ['', 'Giro libre Fabricio Ojeda - Costanera norte', '1', '5,50', '5,50', '-', '2,60', 'Savignani, T. 26'],
    ['Perrokero', 'Av. Fuerzas Armadas, acceso sur', '2', '3,92', '7,85', '1,10', '2,00', 'Perozo, C. 4.1'],
    ['', 'Av. Fuerzas Armadas, acceso norte', '2', '3,92', '7,85', 'No dividida', '2,00', 'Perozo, C. 4.1'],
    ['', 'Av. Río', '2 (*)', '3,00', '6,00', 'No dividida', '2,00', 'Perozo, C. 4.2: 1 carril de 5,0 m'],
    ['', 'Acceso residencial', '2 (*)', '3,00', '6,00', 'No dividida', '2,00', 'Perozo, C. 4.2: 1 carril de 5,0 m'],
    ['Bissau y Puerto Guaica', 'Av. La Costanera (ambos sentidos)', '2', '3,70', '7,40', '1,30', '-', 'Sección de la Costanera, Savignani T. 25'],
    ['', 'Salidas residenciales', '1', '3,20 - 3,70', '-', '-', '-', 'No reportadas en las tesis'],
]
cuadro('Cuadro 4.2 Sección transversal por vía (sentido de circulación)',
       ['Intersección', 'Vía', 'N.º carriles', 'Ancho de carril (m)', 'Calzada (m)', 'Isla (m)', 'Acera (m)', 'Fuente'],
       geo, [2.0, 4.0, 1.3, 1.5, 1.4, 1.5, 1.2, 3.3], tam=8,
       fuente='Fuente: El autor (2026), a partir de Estanga y Savignani (2021), Assouad y Peroza (2022) e inspección de campo. '
              '(*) Número de carriles observado en campo, distinto al de la tesis.')
nota('Donde la tesis reporta menos carriles que los observados en campo (*), se conservaron los carriles de campo. En El '
     'Ejército se repartió el ancho de calzada de la tesis (10,1 m) entre los 3 carriles. En la Av. Río y el acceso '
     'residencial de Perrokero, la tesis da 1 carril de 5,0 m; repartirlo en 2 carriles de 2,5 m provocaba bloqueos '
     'artificiales en la simulación, por lo que se mantuvieron 2 carriles de 3,0 m. La velocidad máxima es de 40 km/h en '
     'todo el eje (señal observada en campo), salvo en las salidas residenciales (20 a 30 km/h). Las Tablas 25 y 26 y la '
     'Fig. 84 de Savignani se contradicen en algunos anchos (ver INCONGRUENCIAS_TESIS_EVALUADAS, S22 a S24); se usó la '
     'Fig. 84, que es la más detallada.')

doc.add_heading('4.1.3 Señalización vial', level=2)
p('Durante la inspección de campo se registraron fotográficamente los siguientes dispositivos de control:')
cuadro('Cuadro 4.3 Inventario de señalización observada en campo (07/04/2026)',
       ['Intersección / tramo', 'Dispositivo', 'Ubicación / sentido'],
       [['Camino Real', 'Señal de PARE', 'Sentido Barcelona - Perrokero'],
        ['', 'Señales de semáforo', 'Sentido Lechería - Barcelona y sentido Perrokero - Lechería/Barcelona'],
        ['', 'Restricción de altura (2 señales)', 'En la intersección y junto al semáforo'],
        ['', 'Delineadores de curva', 'Curva Costanera - El Ejército'],
        ['', 'Paso peatonal', 'Intersección'],
        ['', 'Parada de transporte público', 'Intersección'],
        ['CC Paos (semáforo Costanera)', 'Señal de PARE', 'Sentido Lechería - Barcelona y sentido Madre Vieja - Barcelona'],
        ['', 'Señales de semáforo', 'Sentido Lechería - Barcelona y sentido Barcelona - Lechería'],
        ['', 'Velocidad máxima 40 y 60 km/h', 'Sentido Barcelona - Lechería'],
        ['Puerto Guaica', 'Parada de transporte público', 'Sentido Lechería'],
        ['', 'Velocidad máxima 40 km/h', 'Antes del cruce de Costa Guaica'],
        ['Perrokero', 'Señal de PARE', 'Sentido Perrokero - Lechería'],
        ['', 'Paso peatonal', 'Intersección'],
        ['Nueva Etruria', 'Paso peatonal', 'Av. Fuerzas Armadas'],
        ['Corredor', 'Señal informativa de corredor vial', 'Av. La Costanera']],
       [3.8, 5.0, 6.7], fuente='Fuente: El autor (2026), registro fotográfico de campo.')
nota('El inventario sale de los nombres de las fotos de la carpeta TRABAJO DE CAMPO\\SEÑALIZACION. Conviene revisar '
     'cada foto para confirmar la ubicación y agregar el estado de cada señal (bueno, regular, deteriorado), como hacen '
     'las tesis evaluadas en sus secciones de pavimento, demarcación, señalización e iluminación.')

doc.add_heading('4.1.4 Sistema semaforizado', level=2)
p('Los tiempos de los semáforos se midieron con cronómetro en campo y se programaron tal cual en el modelo. En ambos '
  'semáforos el amarillo es de 3 s. En Camino Real hay además 1 s de todo rojo entre fases.')
cuadro('Cuadro 4.4 Programas semafóricos medidos en campo',
       ['Intersección', 'Fase', 'Movimientos con verde', 'Verde (s)', 'Amarillo (s)', 'Todo rojo (s)', 'Ciclo (s)'],
       [['Camino Real', '1', 'Prolong. Av. El Ejército hacia Lechería o Perrokero', '25', '3', '1', '82'],
        ['', '2', 'Lechería (Costanera) hacia Perrokero o El Ejército', '25', '3', '1', ''],
        ['', '3', 'Perrokero (FFAA) hacia El Ejército o Lechería', '20', '3', '1', ''],
        ['CC Paos', '1', 'Madre Vieja hacia Barcelona (inicio de su verde)', '10', '3', '-', '66'],
        ['', '2', 'Madre Vieja hacia Barcelona y Barcelona hacia Madre Vieja', '20', '3', '-', ''],
        ['', '3', 'Lechería hacia Barcelona', '27', '3', '-', '']],
       [2.2, 1.0, 6.2, 1.4, 1.6, 1.6, 1.4], fuente='Fuente: El autor (2026), medición en campo.')
nota('En CC Paos el semáforo de Madre Vieja tiene 33 s de verde: los 10 s de la fase 1, más 3 s de amarillo y los 20 s de '
     'la fase 2, que comparte con el sentido Barcelona - Madre Vieja (así quedó anotado en campo). Comparación con las tesis: '
     'Savignani (2021) reporta en Camino Real un ciclo de 111 s (Tabla 54), cuyos tiempos no suman el ciclo; y en CC Paos, '
     'fases con ciclos de 108, 99 y 109 s (Tabla 61). Ver el archivo INCONGRUENCIAS_TESIS_EVALUADAS.')

# ------------------------------------------------------------------ 4.2
doc.add_heading('4.2 Desempeño operativo del tránsito (objetivo específico 2)', level=1)
doc.add_heading('4.2.1 Modelo de simulación', level=2)
p('El eje se modeló en el software SUMO (Simulation of Urban Mobility), versión 1.26, a partir de la cartografía de '
  'OpenStreetMap, ajustada con la geometría y los semáforos descritos en la sección 4.1. El Cuadro 4.5 resume los '
  'parámetros principales del modelo.')
cuadro('Cuadro 4.5 Parámetros del modelo de simulación',
       ['Parámetro', 'Valor adoptado', 'Justificación'],
       [['Período simulado', '0-15 min calentamiento; 15-75 min hora de análisis; 75-90 min vaciado', 'Se mide solo la hora pico con la red ya cargada'],
        ['Réplicas', '5 corridas con semillas 1 a 5; se reporta el promedio', 'Con 3 réplicas el margen en Camino Real era de ±27 s; con 5, de ±13 s'],
        ['Teletransportes', 'Desactivados', 'Un vehículo detenido sigue esperando, como en la realidad'],
        ['Tipos de vehículo', 'Livianos, pesados y transporte público (carritos/por puestos)', 'Motocicletas excluidas por indicación del tutor'],
        ['Liviano', 'Largo 5,0 m; acel. 2,6 m/s²; vel. deseada 110 % del límite', 'Las tesis observan de 40 a 50 km/h en zonas de 40 km/h'],
        ['Pesado', 'Largo 12,0 m; acel. 1,0 m/s²; vel. máx. 50 km/h; carril derecho', 'Comportamiento de buses y camiones observado'],
        ['Carrito', 'Largo 5,0 m; acel. 2,8 m/s²; paradas de 15 s', 'Transporte público con paradas'],
        ['Factor de hora de máxima demanda', '0,90', 'Promedio de las tesis (0,83 a 0,94)'],
        ['Medición', 'Detector E3 por intersección y datos por tramo de cada acceso (unos 300 m aguas arriba)', 'Demora de control según HCM 2000'],
        ['Nivel de servicio', 'HCM 2000. Con semáforo: 10/20/35/55/80 s; sin semáforo: 10/15/25/35/50 s', 'Mismo método de las tesis evaluadas']],
       [3.6, 6.2, 5.7])

doc.add_heading('4.2.2 Volúmenes de tránsito', level=2)
p('Los volúmenes horarios por movimiento se tomaron del capítulo IV de ambas tesis: Estanga y Savignani (2021), '
  'Tablas 37 y 38 y Cuadros 21 y 23; y Assouad y Peroza (2022), Tabla 4.3. Se actualizaron al año 2026 con los '
  'factores del Cuadro 4.6.')
cuadro('Cuadro 4.6 Factores de actualización y proyección de la demanda',
       ['Factor', 'Valor', 'Aplicación', 'Fuente'],
       [['Crecimiento anual', '2,5 %', 'Todos los movimientos', 'INE; mismo valor usado por Assouad y Peroza (2022)'],
        ['Crecimiento 2021 - 2026', '1,025⁵ = 1,131', 'Calles secundarias (salidas residenciales)', 'INE'],
        ['Recuperación post COVID-19', '1,50', 'Corredor principal', 'Estanga y Savignani (2021)'],
        ['Factor 2026 corredor principal', '1,131 × 1,50 = 1,697', 'Costanera, FFAA, El Ejército, Fabricio Ojeda', 'El autor'],
        ['Av. Río y Residencias (Perrokero)', 'Conteo de campo 2026', '180 y 80 veh/h (sin motos)', 'Trabajo de campo; capacidad del giro 93 veh/h (Perozo, Tabla 4.8)'],
        ['Horizonte futuro 2026 - 2041', '1,025¹⁵ = 1,448', 'Toda la demanda 2026', 'INE (15 años)']],
       [3.8, 3.0, 4.4, 4.3])
nota('La Av. Río no usa el factor 1,697 porque daba unos 850 veh/h, físicamente imposibles para un giro sin semáforo '
     'con capacidad de unos 93 veh/h (Perozo, Tabla 4.8): generaba una cola irreal de 300 vehículos. Se usó el conteo de campo.')

camp = [['Camino Real', 'El Ejército → Costanera', '540', '60', '600'], ['', 'Costanera → El Ejército (curva)', '420', '30', '450'],
        ['', 'El Ejército → FFAA', '270', '0', '270'], ['', 'FFAA → Costanera', '330', '90', '420'],
        ['CC Paos', 'Lechería → Costanera', '460', '20', '480'], ['', 'Costanera → Madre Vieja', '280', '20', '300'],
        ['', 'Madre Vieja → Costanera', '260', '40', '300'], ['', 'Lechería → Madre Vieja', '220', '0', '220'],
        ['Bissau', 'Costanera → Lechería', '540', '60', '600'], ['', 'Costanera → Camino Real', '420', '30', '450'],
        ['', 'Entradas/salidas residencias y CC', '180', '0', '180'], ['', 'Entrada a galpones', '120', '30', '150'],
        ['Puerto Guaica', 'Costanera → Lechería', '450', '30', '480'], ['', 'Costanera → Camino Real', '360', '60', '420'],
        ['', 'Entrada Puerto Guaica', '120', '0', '120'], ['', 'Salida Puerto Guaica', '90', '0', '90'],
        ['Perrokero', 'FFAA → Camino Real', '240', '20', '260'], ['', 'Camino Real → FFAA', '180', '0', '180'],
        ['', 'Av. Río → Camino Real', '100', '0', '100'], ['', 'Av. Río → FFAA', '80', '0', '80'],
        ['', 'FFAA → Av. Río', '60', '0', '60'], ['', 'Residencias → FFAA / Camino Real / Av. Río', '80', '0', '80'],
        ['', 'Camino Real → Av. Río', '40', '0', '40']]
cuadro('Cuadro 4.7 Conteos de verificación de corta duración en campo, sin motocicletas (veh/h)',
       ['Intersección', 'Movimiento', 'Livianos', 'Pesados', 'Total'], camp, [2.6, 6.6, 2.0, 2.0, 2.0],
       fuente='Fuente: El autor (2026), conteos de 2 a 3 minutos expandidos a la hora (07/04/2026).')
nota('Según lo acordado, los conteos propios se presentan como "conteos de verificación de corta duración" y se usan '
     'para contrastar los volúmenes de las tesis y para las calles secundarias. No decir que se contó varios días ni en '
     'varias horas pico.')

doc.add_heading('4.2.3 Validación del modelo (estadístico GEH)', level=2)
ok = sum(1 for g in geh if float(g['GEH']) < 5)
p(f'Para verificar que el modelo reproduce los volúmenes de diseño se calculó el estadístico GEH de cada movimiento, '
  f'comparando el volumen objetivo 2026 con el volumen generado en la simulación. El criterio de aceptación es que al '
  f'menos el 85 % de los movimientos tenga GEH < 5 (FHWA, Traffic Analysis Toolbox, vol. III). Se obtuvo GEH < 5 en '
  f'{ok} de {len(geh)} movimientos ({n(100 * ok / len(geh), 1)} %), por lo que el modelo se considera validado. El único '
  f'movimiento por encima del límite es Costanera → FFAA (livianos) en Camino Real, con GEH = 5,22.')
cuadro('Cuadro 4.8 Volúmenes por movimiento y validación GEH (hora pico)',
       ['Intersección', 'Código', 'Movimiento', 'Clase', 'Tesis 2021 (veh/h)', 'Objetivo 2026 (veh/h)', 'Simulado (veh/h)', 'GEH'],
       [[g['interseccion'], g['codigo'], g['descripcion'].replace('->', '→'), g['clase'], g['tesis 2021 (veh/h)'],
         g['objetivo 2026 (veh/h)'], g['demanda generada (veh/h)'], n(g['GEH'], 2)] for g in geh],
       [2.0, 1.1, 4.6, 1.5, 1.6, 1.7, 1.6, 1.2], tam=8,
       fuente='Fuente: El autor (2026), a partir de Estanga y Savignani (2021), Assouad y Peroza (2022) y la simulación.')


# ------------------------------------------------------------------ resultados
def bloque_resultados(rep, num_int, num_acc, anio):
    filas_i = [[r['interseccion'], n(r['demanda_veh_h']), n(r['volumen_promedio_veh_h']), r['demanda_atendida_pct'] + ' %',
                n(r['demora_promedio_s'], 1), f"{n(r['demora_min_s'], 1)} - {n(r['demora_max_s'], 1)}", n(r['VC'], 2), r['LOS_HCM']]
               for r in rep if r['nivel'] == 'INTERSECCION']
    cuadro(f'Cuadro {num_int} Desempeño por intersección, escenario {anio} (promedio de 5 réplicas)',
           ['Intersección', 'Demanda (veh/h)', 'Volumen atendido (veh/h)', 'Demanda atendida', 'Demora (s/veh)',
            'Rango 5 réplicas (s)', 'V/C crítica', 'Nivel de servicio'],
           filas_i, [2.3, 1.7, 1.9, 1.7, 1.7, 2.2, 1.5, 1.6])
    filas_a = []
    ant = None
    for r in rep:
        if r['nivel'] != 'ACCESO':
            continue
        filas_a.append([r['interseccion'] if r['interseccion'] != ant else '', r['acceso'], n(r['demanda_veh_h']),
                        n(r['capacidad_veh_h']) if r['capacidad_veh_h'] else '-', n(r['VC'], 2), r['demanda_atendida_pct'] + ' %',
                        n(r['demora_promedio_s'], 1), r['LOS_HCM'], n(r['cola_promedio_m']),
                        ('≥ ' if r['cola_llena_el_tramo'] == 'si' else '') + n(r['cola_maxima_m']),
                        n(r['velocidad_media_kmh'], 1) if r['velocidad_media_kmh'] else '-'])
        ant = r['interseccion']
    cuadro(f'Cuadro {num_acc} Desempeño por acceso, escenario {anio} (promedio de 5 réplicas)',
           ['Intersección', 'Acceso', 'Demanda (veh/h)', 'Capacidad (veh/h)', 'V/C', 'Atendida', 'Demora (s/veh)', 'NDS',
            'Cola prom. (m)', 'Cola máx. (m)', 'Vel. media (km/h)'],
           filas_a, [1.7, 2.9, 1.2, 1.3, 1.0, 1.2, 1.2, 0.8, 1.2, 1.3, 1.2], tam=8)


doc.add_heading('4.2.4 Capacidad y nivel de servicio actual (2026)', level=2)
p('Los Cuadros 4.9 y 4.10 presentan los resultados de la situación actual. La capacidad se calculó con el método del '
  'HCM 2000: con semáforo, c = 1.900 · fVP · N · g/C; en el acceso principal sin semáforo, c = 1.900 · fVP · N; y en '
  'el acceso secundario, la capacidad potencial de carril compartido. Cuando un acceso está saturado (atiende menos '
  'del 95 % de su demanda o tiene demora de nivel F), se usa como capacidad el flujo que realmente descarga en la '
  'simulación. La cola se mide desde la línea de detención hacia atrás, a lo largo de los tramos de cada acceso (unos '
  '300 m, o hasta la intersección anterior); cuando la cola llena todos esos tramos se indica con "≥".')
bloque_resultados(rep26, '4.9', '4.10', '2026')
nota('En las intersecciones sin semáforo (Perrokero, Bissau y Puerto Guaica), el HCM 2000 asigna a la intersección el '
     'nivel de servicio de su peor acceso secundario, aunque la demora promedio de todos los vehículos sea menor. La '
     'demora de la intersección es el promedio de todos los vehículos que la cruzan.')
cr, cp_, pk = I26['Camino Real'], I26['CC Paos'], I26['Perrokero']
nota(f"Hallazgos 2026: Camino Real funciona en nivel {cr['LOS_HCM']} ({n(cr['demora_promedio_s'], 1)} s, V/C {n(cr['VC'], 2)}); "
     f"su acceso más cargado es la Costanera ({d(rep26, 'Camino Real', 'Norte (Costanera)')}). CC Paos opera en "
     f"{cp_['LOS_HCM']} ({n(cp_['demora_promedio_s'], 1)} s). Perrokero es el punto crítico: nivel {pk['LOS_HCM']} "
     f"({n(pk['demora_promedio_s'], 1)} s), con la Av. Río saturada ({d(rep26, 'Perrokero', 'Este (Av. Rio)')}; atiende el "
     f"{fila(rep26, 'Perrokero', 'Este (Av. Rio)')['demanda_atendida_pct']} % de su demanda). En Puerto Guaica, sentido "
     f"Camino Real, la parada de bus ocupa el carril derecho cerca del 23 % de la hora pico: redactarlo así, porque la "
     f"longitud de cola de ese acceso es un efecto de cómo mide SUMO.")

doc.add_heading('4.2.5 Nivel de servicio futuro (2041, sin proyecto)', level=2)
p('Para el horizonte 2041 se multiplicó toda la demanda 2026 por 1,448 y se mantuvieron la red y los semáforos actuales. '
  'Como capacidad de cada acceso se usa la de 2026, porque es una propiedad de la vía y no de la demanda. Las colas que '
  'llenan todo el tramo medido se indican con "≥".')
bloque_resultados(rep41, '4.11', '4.12', '2041')
at41 = [int(r['demanda_atendida_pct']) for r in I41.values()]
nota(f"Hallazgos 2041: todas las intersecciones pasan a nivel F y atienden solo entre el {min(at41)} % y el {max(at41)} % "
     f"de la demanda. El colapso empieza en Perrokero: el acceso FFAA norte atiende el "
     f"{fila(rep41, 'Perrokero', 'Norte (desde Camino Real)')['demanda_atendida_pct']} % de su demanda. La cola se propaga "
     f"hacia Camino Real, luego a Puerto Guaica y Bissau, y llega hasta CC Paos. Por eso conviene evaluar las propuestas "
     f"en conjunto. Las demoras de miles de segundos en los accesos secundarios se dejan tal cual (decisión del autor): "
     f"indican vehículos que prácticamente no logran salir.")

doc.add_heading('4.2.6 Indicadores de la red completa', level=2)
p('Los cuadros anteriores evalúan cada intersección por separado. El Cuadro 4.13 evalúa el viaje completo de cada '
  'vehículo que entra al eje durante la hora pico, desde su origen hasta su destino, sin importar cuántas intersecciones '
  'cruce: cuántos viajes se realizaron, cuánto tardaron, cuánto tiempo perdieron respecto a circular a la velocidad '
  'libre de la vía (demora) y a qué velocidad media circularon.')
nombres = {'carrito': 'Transporte público', 'liviano': 'Livianos', 'pesado': 'Pesados', 'TOTAL': 'Total'}
filas_v = []
for tipo in ('liviano', 'pesado', 'carrito', 'TOTAL'):
    a, b = R26[tipo], R41[tipo]
    filas_v.append([nombres[tipo], n(a['volumen_promedio_veh_h']), n(a['tiempo_viaje_s']), n(a['demora_promedio_s']),
                     n(a['velocidad_media_kmh'], 1), n(b['volumen_promedio_veh_h']), n(b['tiempo_viaje_s']),
                     n(b['demora_promedio_s']), n(b['velocidad_media_kmh'], 1)])
cuadro('Cuadro 4.13 Indicadores de los viajes en la hora pico (todo el eje, promedio de 5 réplicas)',
       ['Tipo de vehículo', 'Viajes 2026', 'Tiempo de viaje 2026 (s)', 'Demora 2026 (s)', 'Velocidad 2026 (km/h)',
        'Viajes 2041', 'Tiempo de viaje 2041 (s)', 'Demora 2041 (s)', 'Velocidad 2041 (km/h)'],
       filas_v, [2.2, 1.5, 1.8, 1.6, 1.7, 1.5, 1.8, 1.6, 1.7],
       fuente='Fuente: El autor (2026), a partir de la simulación en SUMO (viajes que salen entre los minutos 15 y 75).')
t26, t41 = R26['TOTAL'], R41['TOTAL']
nota(f"En 2026 un viaje promedio dura {n(t26['tiempo_viaje_s'])} s, de los cuales {n(t26['demora_promedio_s'])} s se pierden "
     f"en colas, semáforos y cruces; la velocidad media es de {n(t26['velocidad_media_kmh'], 1)} km/h. En 2041 el viaje "
     f"dura {n(t41['tiempo_viaje_s'])} s y la velocidad cae a {n(t41['velocidad_media_kmh'], 1)} km/h. Estos indicadores "
     f"son los que se usarán para comparar cada propuesta con el escenario sin proyecto (porcentaje de reducción del "
     f"tiempo de viaje y de la demora, e incremento de la velocidad).")

doc.add_heading('4.2.7 Comparación con las tesis evaluadas', level=2)
tes = []
for r in I26.values():
    tes.append([r['interseccion'], r['tesis_LOS'], r['tesis_demora_s'].replace('.', ','), r['LOS_HCM'], n(r['demora_promedio_s'], 1)])
cuadro('Cuadro 4.14 Nivel de servicio actual: tesis evaluadas frente a la simulación',
       ['Intersección', 'NDS tesis', 'Demora tesis (s)', 'NDS simulación 2026', 'Demora simulación (s)'],
       tes, [2.6, 1.6, 5.3, 2.4, 2.4], fuente='Fuente: El autor (2026), a partir de Estanga y Savignani (2021), Assouad y Peroza (2022) y la simulación.')
for t in [f"Perrokero: coincide con Perozo (F hoy y F en el futuro).",
          f"CC Paos: la tesis da C (22,6 s) y la simulación {cp_['LOS_HCM']} ({n(cp_['demora_promedio_s'], 1)} s).",
          f"Camino Real: la tesis da F (129 s) y la simulación {cr['LOS_HCM']} ({n(cr['demora_promedio_s'], 1)} s). Savignani usa "
          '35 % de pesados (su Tabla 37 dice 6 %), un GD3 de 603 veh/h (su Tabla 37 dice 190), un solo carril de giro y un '
          'ciclo de 111 s cuyos tiempos no cuadran. En 2041 la simulación también da F.',
          'Bissau y Fernández Padilla: el F de Savignani (1.074 a 1.228 s) es un error de cálculo del HCM; recalculado da '
          'unos 28 s (D).',
          'CC Paos futuro: la tesis da C (2036) y la simulación F (2041), por el efecto de red (colas que vienen de las '
          'otras intersecciones), que el HCM aislado no capta.']:
    vineta(t)

doc.save(SALIDA)
print('guardado', SALIDA)
