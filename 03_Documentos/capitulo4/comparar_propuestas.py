"""Genera 'COMPARACION DE ESCENARIOS - BASE, SAVIGNANI Y PEROZO.docx': resultados de la simulacion base y de las dos
propuestas evaluadas (2026 y 2041), lado a lado, para la redaccion del objetivo 3."""
import csv
import os

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = r'C:\Users\samue_yffy\Desktop\TRABAJO DE GRADO\COMPARACION DE ESCENARIOS - BASE, SAVIGNANI Y PEROZO.docx'
ESCENARIOS = {'Base': 'replicas_anchos_tesis', 'Savignani': 'replicas_savignani', 'Perozo': 'replicas_perozo'}
NOMBRES = list(ESCENARIOS)
INTERSECCIONES = ['Camino Real', 'CC Paos', 'Perrokero', 'Bissau', 'Puerto Guaica']
TIPOS = [('liviano', 'Livianos'), ('pesado', 'Pesados'), ('carrito', 'Transporte público (carritos)'), ('TOTAL', 'Total')]
COLOR_LOS = {'A': 'C6EFCE', 'B': 'E2F0D9', 'C': 'FFF2CC', 'D': 'FCE4D6', 'E': 'F8CBAD', 'F': 'F4B6B6'}


def leer(ruta):
    return list(csv.DictReader(open(ruta, encoding='utf-8-sig'), delimiter=';'))


DATOS = {anio: {e: leer(os.path.join(AQUI, c, anio, 'resumen_replicas.csv')) for e, c in ESCENARIOS.items()}
         for anio in ('2026', '2041')}


def fila(anio, esc, inter, acceso='(todos)', nivel=None):
    for r in DATOS[anio][esc]:
        if r['interseccion'] == inter and r['acceso'] == acceso and (nivel is None or r['nivel'] == nivel):
            return r
    return None


def n(x, d=0):
    """numero con coma decimal y punto de miles"""
    if x in (None, ''):
        return '-'
    s = f'{float(x):,.{d}f}'
    return s.replace(',', '§').replace('.', ',').replace('§', '.')


def var(nuevo, base):
    """variacion porcentual respecto a la base"""
    if nuevo in (None, '') or base in (None, '') or float(base) == 0:
        return '-'
    v = (float(nuevo) - float(base)) / float(base) * 100
    v = round(v)
    return ('+' if v > 0 else '') + n(v, 0) + ' %'


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


def sombra(par, color):
    ppr = par._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color)
    ppr.append(shd)


def nota(texto):
    par = doc.add_paragraph()
    r = par.add_run('Nota para la redacción: ')
    r.bold = True
    r.font.size = Pt(10)
    r2 = par.add_run(texto)
    r2.font.size = Pt(10)
    sombra(par, 'EEF3F8')


def celda_fondo(celda, color):
    tcpr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color)
    tcpr.append(shd)


def cuadro(titulo, encabezado, filas, anchos, fuente='Fuente: El autor (2026), a partir de la simulación en SUMO.',
           tam=9, columnas_los=(), grupos=None):
    """grupos: fila de encabezado superior [(texto, n_columnas), ...]"""
    t = p(titulo, negrita=True, tam=11)
    t.paragraph_format.keep_with_next = True
    tab = doc.add_table(rows=0, cols=len(encabezado))
    tab.style = 'Table Grid'
    tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    filas_enc = []
    if grupos:
        celdas = tab.add_row().cells
        i = 0
        for texto, k in grupos:
            c = celdas[i].merge(celdas[i + k - 1]) if k > 1 else celdas[i]
            c.text = ''
            r = c.paragraphs[0].add_run(texto)
            r.bold = True
            r.font.size = Pt(tam)
            c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            celda_fondo(c, 'C5D3E2')
            i += k
        filas_enc.append(tab.rows[-1])
    celdas = tab.add_row().cells
    for i, h in enumerate(encabezado):
        celdas[i].text = ''
        r = celdas[i].paragraphs[0].add_run(h)
        r.bold = True
        r.font.size = Pt(tam)
        celdas[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        celda_fondo(celdas[i], 'D9E2EC')
    filas_enc.append(tab.rows[-1])
    for fe in filas_enc:   # repetir encabezado en cada pagina
        trpr = fe._tr.get_or_add_trPr()
        th = OxmlElement('w:tblHeader')
        th.set(qn('w:val'), 'true')
        trpr.append(th)
    for f in filas:
        negrita = isinstance(f, tuple)
        celdas = tab.add_row().cells
        for i, v in enumerate(f):
            celdas[i].text = ''
            r = celdas[i].paragraphs[0].add_run(str(v))
            r.font.size = Pt(tam)
            r.bold = negrita
            celdas[i].paragraphs[0].paragraph_format.space_after = Pt(0)
            if i > 0 and len(str(v)) <= 14:
                celdas[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            if i in columnas_los and str(v) in COLOR_LOS:
                celda_fondo(celdas[i], COLOR_LOS[str(v)])
    for fr in tab.rows:
        for i, a in enumerate(anchos):
            fr.cells[i].width = Cm(a)
    f = p(fuente, cursiva=True, tam=9)
    f.paragraph_format.space_after = Pt(12)
    return tab


def horizontal():
    s = doc.add_section()
    s.orientation = WD_ORIENT.LANDSCAPE
    s.page_width, s.page_height = Cm(27.94), Cm(21.59)
    s.left_margin, s.right_margin, s.top_margin, s.bottom_margin = Cm(2.5), Cm(2.5), Cm(3), Cm(2.5)


def vertical():
    s = doc.add_section()
    s.orientation = WD_ORIENT.PORTRAIT
    s.page_width, s.page_height = Cm(21.59), Cm(27.94)
    s.left_margin, s.right_margin, s.top_margin, s.bottom_margin = Cm(3), Cm(2.5), Cm(2.5), Cm(2.5)


NUM = [15]


def num():
    NUM[0] += 1
    return f'4.{NUM[0] - 1}'


def accesos(inter):
    """accesos de una interseccion en el orden de la base y luego los propios de cada propuesta"""
    vistos = []
    for e in NOMBRES:
        for r in DATOS['2026'][e]:
            if r['interseccion'] == inter and r['nivel'] in ('ACCESO',) and r['acceso'] not in vistos:
                vistos.append(r['acceso'])
    return vistos


# ------------------------------------------------------------------ portada
p('INFORMACIÓN PARA EL CAPÍTULO IV', negrita=True, tam=16, centro=True)
p('COMPARACIÓN DE ESCENARIOS', negrita=True, tam=14, centro=True)
p('Escenario base (sin proyecto) frente a las propuestas de Estanga y Savignani (2021) y de Assouad y Peroza (2022)',
  tam=12, centro=True)
p('Situación 2026 y horizonte 2041 · Objetivo específico 3', cursiva=True, centro=True)
p('')
p('Este documento reúne, lado a lado, los resultados de la simulación en SUMO de los tres escenarios evaluados: el '
  'escenario base (control) y las dos propuestas originales (tratamientos), cada uno en la hora pico de 2026 y en el '
  'horizonte 2041. Sirve de base para el análisis del objetivo 3 (recomendaciones a las propuestas). Los cuadros '
  'continúan la numeración del documento del escenario base (que llega al Cuadro 4.14); los recuadros sombreados son '
  'notas para la redacción y no forman parte del texto de la tesis.')
p('Fuente de los datos: simulación en SUMO 1.26; todos los resultados son el promedio de 5 réplicas (semillas 1 a 5). '
  'Nivel de servicio según el HCM 2000. Cifras con coma decimal.', cursiva=True, tam=10)

# ------------------------------------------------------------------ 1. escenarios
doc.add_heading('1. Escenarios comparados', level=1)
cuadro(f'Cuadro {num()} Descripción de los escenarios simulados',
       ['Elemento', 'Base (sin proyecto)', 'Estanga y Savignani (2021)', 'Assouad y Peroza (2022)'],
       [['Intersección intervenida', '-', 'Camino Real (Costanera × FFAA × El Ejército)', 'Perrokero (FFAA × Av. Río)'],
        ['Obra principal', '-', 'Distribuidor tipo puente Costanera ↔ FFAA: 1 carril de 4 m por sentido; tablero de 30 m a 7,4 m; '
         'rampas de 60 m al 12,3 %', 'Puente sobre FFAA: 1 carril de 3,70 m por sentido; tablero de 20 m a 6,0 m; rampas de 40 m al 15 % '
         '(100 m en total)'],
        ['Tránsito por el puente', '-', 'Livianos y carritos (pesados a nivel)', 'Livianos y carritos (pesados a nivel)'],
        ['Control a nivel', 'Semáforo de 82 s (Camino Real); Perrokero sin semáforo',
         'Semáforo de 4 fases, ciclo de 122 s (una fase por acceso)', 'Semáforo de 4 fases, ciclo de 120 s (Norte 33, Oeste 20, Sur 25 '
         'y Este 30 s)'],
        ['Carriles a nivel', 'Los de campo', 'FFAA con 1 carril a nivel; salida a la Costanera de 1 carril',
         'FFAA con 1 carril a nivel por sentido (el izquierdo sube al puente)'],
        ['Otras obras', '-', 'Av. En Proyección (2 carriles por sentido); bahías de bus en Puerto Guaica, Bissau y Fernández '
         'Padilla; carriles de salida e incorporación en Bissau', '-'],
        ['Demanda', 'Tesis × 1,697 (2026) y × 1,448 adicional (2041)', 'La misma de la base; el 30 % de los viajes de FFAA sur '
         'por Camino Real usa la Av. En Proyección', 'La misma de la base'],
        ],
       [3.0, 3.6, 4.7, 4.7], tam=8)
nota('Los carritos (taxis y por puestos) se modelan como automóviles con paradas de 15 s; como no son vehículos pesados, en ambas '
     'propuestas pueden usar el puente (criterio del autor). Los pesados, incluidos los buses, cruzan siempre a nivel.')
nota('El 30 % de la Av. En Proyección lo indicó el tutor como criterio de experto (la tesis no le asigna volumen) y debe declararse así. Por esa razón '
     'la red de Savignani recibe algo menos de tránsito en FFAA, lo que la favorece levemente en la comparación. La capacidad de '
     'cada acceso en 2041 se toma de la de 2026 del mismo escenario.')


# ------------------------------------------------------------------ cuadros por horizonte
def bloque(anio):
    doc.add_heading(f'{"2" if anio == "2026" else "3"}. Resultados {anio}', level=1)
    # intersecciones
    filas = []
    for inter in INTERSECCIONES:
        f = [inter]
        for e in NOMBRES:
            r = fila(anio, e, inter, nivel='INTERSECCION')
            f += [n(r['demora_promedio_s'], 1), r['LOS_HCM'], n(r['VC'], 2), n(r['demanda_atendida_pct'], 0)]
        filas.append(f)
    cuadro(f'Cuadro {num()} Demora y nivel de servicio por intersección, {anio}',
           ['Intersección'] + ['Demora (s)', 'NS', 'V/C', 'Atendida (%)'] * 3, filas,
           [2.6] + [1.45, 0.8, 1.05, 1.5] * 3, tam=8, columnas_los=(2, 6, 10),
           grupos=[('', 1), ('Base', 4), ('Savignani', 4), ('Perozo', 4)])
    filas = []
    for inter, nombre in (('Camino Real', 'Camino Real (Savignani)'), ('Perrokero', 'Perrokero (Perozo)')):
        e = 'Savignani' if inter == 'Camino Real' else 'Perozo'
        r = fila(anio, e, inter, '(sin puente)')
        filas.append([nombre, n(r['volumen_promedio_veh_h']), n(r['demora_promedio_s'], 1), r['LOS_HCM'],
                      n(r['demanda_atendida_pct'], 0)])
    cuadro(f'Cuadro {num()} Intersección intervenida: solo los accesos a nivel (sin el puente), {anio}',
           ['Intersección', 'Volumen (veh/h)', 'Demora (s)', 'NS', 'Atendida (%)'], filas, [5.0, 2.6, 2.4, 1.4, 2.4],
           tam=9, columnas_los=(3,))
    horizontal()
    filas = []
    for inter in INTERSECCIONES:
        filas.append((inter,) + ('',) * 15)
        for acc in accesos(inter):
            f = ['   ' + acc]
            for e in NOMBRES:
                r = fila(anio, e, inter, acc)
                f += ([n(r['volumen_promedio_veh_h']), n(r['demora_promedio_s'], 1), r['LOS_HCM'],
                       n(r['cola_promedio_m']) + ' / ' + n(r['cola_maxima_m']), n(r['velocidad_media_kmh'], 1)]
                      if r else ['—', '—', '—', '—', '—'])
            filas.append(f)
    cuadro(f'Cuadro {num()} Resultados por acceso, {anio}',
           ['Acceso'] + ['Vol. (veh/h)', 'Demora (s)', 'NS', 'Cola prom./máx. (m)', 'Vel. (km/h)'] * 3, filas,
           [4.4] + [1.15, 1.25, 0.65, 1.55, 1.1] * 3, tam=7, columnas_los=(3, 8, 13),
           grupos=[('', 1), ('Base', 5), ('Savignani', 5), ('Perozo', 5)])
    nota('Los accesos tipo "Puente" son el tránsito que cruza la intersección por el puente; su demora incluye la cola que '
         'encuentra antes de subir. Los vehículos del puente también cuentan en la fila de la intersección completa. '
         '"—": el acceso no existe en ese escenario.')
    vertical()
    filas = []
    for clave, nombre in TIPOS:
        f = [nombre]
        for e in NOMBRES:
            r = fila(anio, e, 'Red completa', clave)
            f += [n(r['volumen_promedio_veh_h']), n(r['tiempo_viaje_s']), n(r['demora_promedio_s']),
                  n(r['velocidad_media_kmh'], 1)]
        filas.append(tuple(f) if clave == 'TOTAL' else f)
    cuadro(f'Cuadro {num()} Indicadores de la red completa por tipo de vehículo, {anio}',
           ['Tipo'] + ['Viajes', 'T. viaje (s)', 'Demora (s)', 'Vel. (km/h)'] * 3, filas,
           [2.6] + [1.15, 1.25, 1.2, 1.2] * 3, tam=8,
           grupos=[('', 1), ('Base', 4), ('Savignani', 4), ('Perozo', 4)])
    nota('"Viajes" son los vehículos que completaron su recorrido en la simulación. En la red completa, la demora (timeLoss '
         'de SUMO) no incluye el tiempo detenido en las paradas de bus; el tiempo de viaje sí lo incluye.')


bloque('2026')
bloque('2041')

# ------------------------------------------------------------------ 4. variaciones
doc.add_heading('4. Variación de cada propuesta respecto al escenario base', level=1)
filas = []
for anio in ('2026', '2041'):
    filas.append((f'Año {anio}',) + ('',) * 5)
    for etiqueta, inter, acc, col, d in [
            ('Red: viajes completados', 'Red completa', 'TOTAL', 'volumen_promedio_veh_h', 0),
            ('Red: tiempo de viaje (s)', 'Red completa', 'TOTAL', 'tiempo_viaje_s', 0),
            ('Red: demora media (s)', 'Red completa', 'TOTAL', 'demora_promedio_s', 0),
            ('Red: velocidad media (km/h)', 'Red completa', 'TOTAL', 'velocidad_media_kmh', 1),
            ('Carritos: demora (s)', 'Red completa', 'carrito', 'demora_promedio_s', 0),
            ('Pesados: demora (s)', 'Red completa', 'pesado', 'demora_promedio_s', 0)] + [
            (f'{i}: demora (s)', i, '(todos)', 'demora_promedio_s', 1) for i in INTERSECCIONES]:
        b = fila(anio, 'Base', inter, acc)[col]
        s = fila(anio, 'Savignani', inter, acc)[col]
        pz = fila(anio, 'Perozo', inter, acc)[col]
        filas.append(['   ' + etiqueta, n(b, d), n(s, d), var(s, b), n(pz, d), var(pz, b)])
cuadro(f'Cuadro {num()} Variación respecto al escenario base',
       ['Indicador', 'Base', 'Savignani', 'Var. Sav.', 'Perozo', 'Var. Per.'], filas,
       [5.0, 1.8, 1.8, 1.8, 1.8, 1.8], tam=8)
nota('En 2041 una demora menor no siempre significa un mejor funcionamiento: si la intersección solo atiende una parte de la '
     'demanda (columna "Atendida" de los cuadros por intersección), los vehículos que no llegan no suman demora. Por eso en 2041 '
     'conviene leer la demora junto con la demanda atendida y el número de viajes completados.')

# ------------------------------------------------------------------ 5. analisis
I = {(a, e): {i: fila(a, e, i, nivel='INTERSECCION') for i in INTERSECCIONES} for a in DATOS for e in NOMBRES}
R = {(a, e): fila(a, e, 'Red completa', 'TOTAL') for a in DATOS for e in NOMBRES}


def ds(a, e, i, acc='(todos)'):
    r = fila(a, e, i, acc)
    return f"{r['LOS_HCM']}, {n(r['demora_promedio_s'], 1)} s"


doc.add_heading('5. Análisis de los resultados', level=1)
doc.add_heading('5.1 Propuesta de Estanga y Savignani (2021)', level=2)
vineta(f'Camino Real empeora: pasa de {ds("2026", "Base", "Camino Real")} a {ds("2026", "Savignani", "Camino Real")} en 2026. '
       f'El puente hacia FFAA funciona bien ({ds("2026", "Savignani", "Camino Real", "Puente hacia FFAA")}), pero el puente hacia '
       f'la Costanera queda en {ds("2026", "Savignani", "Camino Real", "Puente hacia Costanera")}.')
vineta(f'La causa es la geometría a nivel bajo el puente: El Ejército y la bajada del puente salen hacia la Costanera por un solo '
       f'carril, que se satura (El Ejército pasa de {ds("2026", "Base", "Camino Real", "Oeste (El Ejercito)")} a '
       f'{ds("2026", "Savignani", "Camino Real", "Oeste (El Ejercito)")}), y FFAA a nivel, con un solo carril y 20 s de verde, pasa de '
       f'{ds("2026", "Base", "Camino Real", "Sur (FFAA)")} a {ds("2026", "Savignani", "Camino Real", "Sur (FFAA)")}. El propio Anexo B '
       'de la tesis muestra ese giro con Xc = 1,04 (incongruencia S26): el distribuidor traslada el cuello de botella a la salida '
       'hacia la Costanera.')
vineta(f'Transporte público: los carritos usan el distribuidor y su demora baja de '
       f'{n(fila("2026", "Base", "Red completa", "carrito")["demora_promedio_s"])} s a '
       f'{n(fila("2026", "Savignani", "Red completa", "carrito")["demora_promedio_s"])} s; los buses y demás pesados no pueden '
       f'subir y cruzan por FFAA a nivel, que queda saturada: su demora sube de '
       f'{n(fila("2026", "Base", "Red completa", "pesado")["demora_promedio_s"])} s a '
       f'{n(fila("2026", "Savignani", "Red completa", "pesado")["demora_promedio_s"])} s.')
vineta(f'Puerto Guaica pasa de {n(I["2026", "Base"]["Puerto Guaica"]["demora_promedio_s"], 1)} a '
       f'{n(I["2026", "Savignani"]["Puerto Guaica"]["demora_promedio_s"], 1)} s (Bissau: {n(I["2026", "Base"]["Bissau"]["demora_promedio_s"], 1)} → '
       f'{n(I["2026", "Savignani"]["Bissau"]["demora_promedio_s"], 1)} s), por las bahías de bus y porque llega algo menos de tránsito: parte queda '
       'retenida en Camino Real (por eso el sentido Lechería aparece con V/C mayor que 1 y buen nivel a la vez).')
vineta(f'Perrokero también mejora ({ds("2026", "Base", "Perrokero")} → {ds("2026", "Savignani", "Perrokero")}) sin intervenirlo: recibe menos '
       'tránsito por la FFAA, porque el 30 % de los viajes de FFAA sur se desvía por la Av. En Proyección y otra parte queda retenida en Camino Real.')
vineta(f'En la red completa la demora baja de {n(R["2026", "Base"]["demora_promedio_s"])} a {n(R["2026", "Savignani"]["demora_promedio_s"])} s '
       f'y la velocidad sube de {n(R["2026", "Base"]["velocidad_media_kmh"], 1)} a {n(R["2026", "Savignani"]["velocidad_media_kmh"], 1)} km/h, '
       f'con menos viajes completados ({n(R["2026", "Savignani"]["volumen_promedio_veh_h"])} frente a {n(R["2026", "Base"]["volumen_promedio_veh_h"])}).')
vineta(f'En 2041 es el escenario que mejor responde: la red circula a {n(R["2041", "Savignani"]["velocidad_media_kmh"], 1)} km/h '
       f'(base {n(R["2041", "Base"]["velocidad_media_kmh"], 1)} km/h) y completa {n(R["2041", "Savignani"]["volumen_promedio_veh_h"])} viajes '
       f'(base {n(R["2041", "Base"]["volumen_promedio_veh_h"])}); Camino Real sigue en F pero atiende el '
       f'{n(I["2041", "Savignani"]["Camino Real"]["demanda_atendida_pct"])} % de su demanda (base '
       f'{n(I["2041", "Base"]["Camino Real"]["demanda_atendida_pct"])} %). Buena parte de esa mejora viene de la Av. En Proyección, que '
       'saca el 30 % de los viajes de FFAA sur del eje: el resultado depende de que esa avenida se construya.')

doc.add_heading('5.2 Propuesta de Assouad y Peroza (2022)', level=2)
vineta(f'Perrokero mejora: pasa de {ds("2026", "Base", "Perrokero")} a {ds("2026", "Perozo", "Perrokero")} en 2026, con la misma '
       f'demanda. La Av. Río, que era el acceso crítico, pasa de {ds("2026", "Base", "Perrokero", "Este (Av. Rio)")} a '
       f'{ds("2026", "Perozo", "Perrokero", "Este (Av. Rio)")}, gracias al semáforo bajo el puente.')
vineta(f'Solo los accesos a nivel dan {ds("2026", "Perozo", "Perrokero", "(sin puente)")} y {ds("2041", "Perozo", "Perrokero", "(sin puente)")} '
       'en 2041; la propia tesis obtiene E, 65,6 s para 2041 (Alternativa C), pero con una Av. Río mucho más cargada que la del modelo.')
vineta(f'El acceso norte a nivel, con un solo carril para el giro a la izquierda hacia la Av. Río, los pesados y el giro a la derecha, '
       f'queda en {ds("2026", "Perozo", "Perrokero", "Norte (desde Camino Real)")} (cola máxima de '
       f'{n(fila("2026", "Perozo", "Perrokero", "Norte (desde Camino Real)")["cola_maxima_m"])} m), sin bloquear la entrada al puente: el puente '
       f'hacia el sur queda en {ds("2026", "Perozo", "Perrokero", "Puente hacia el sur (FFAA)")} y el puente hacia Camino Real en '
       f'{ds("2026", "Perozo", "Perrokero", "Puente hacia Camino Real")}.')
vineta(f'No perjudica al resto del eje: Camino Real ({ds("2026", "Perozo", "Camino Real")}), CC Paos ({ds("2026", "Perozo", "CC Paos")}), '
       'Bissau y Puerto Guaica quedan prácticamente como en la base.')
vineta(f'En la red completa la demora baja de {n(R["2026", "Base"]["demora_promedio_s"])} a {n(R["2026", "Perozo"]["demora_promedio_s"])} s '
       f'y la velocidad sube de {n(R["2026", "Base"]["velocidad_media_kmh"], 1)} a {n(R["2026", "Perozo"]["velocidad_media_kmh"], 1)} km/h, '
       f'completando los mismos viajes ({n(R["2026", "Perozo"]["volumen_promedio_veh_h"])}).')
vineta(f'En 2041 Perrokero sigue funcionando ({ds("2041", "Perozo", "Perrokero")}, con el '
       f'{n(I["2041", "Perozo"]["Perrokero"]["demanda_atendida_pct"])} % de la demanda atendida), pero el resto del eje colapsa casi como sin '
       f'proyecto: la red circula a {n(R["2041", "Perozo"]["velocidad_media_kmh"], 1)} km/h (base {n(R["2041", "Base"]["velocidad_media_kmh"], 1)} km/h) '
       f'y completa {n(R["2041", "Perozo"]["volumen_promedio_veh_h"])} viajes (base {n(R["2041", "Base"]["volumen_promedio_veh_h"])}). '
       'El colapso pasa a Camino Real y CC Paos.')

doc.add_heading('5.3 Síntesis', level=2)
cuadro(f'Cuadro {num()} Síntesis de la comparación',
       ['Criterio', 'Estanga y Savignani (2021)', 'Assouad y Peroza (2022)'],
       [['Efecto en la intersección intervenida (2026)', f'Empeora ({ds("2026", "Base", "Camino Real")} → {ds("2026", "Savignani", "Camino Real")})',
         f'Mejora ({ds("2026", "Base", "Perrokero")} → {ds("2026", "Perozo", "Perrokero")})'],
        ['Efecto en el resto del eje (2026)', 'Mejoran Perrokero y Puerto Guaica (menos tránsito y bahías de bus)', 'Sin cambios apreciables'],
        ['Red completa 2026', f'{n(R["2026", "Savignani"]["velocidad_media_kmh"], 1)} km/h; menos viajes completados',
         f'{n(R["2026", "Perozo"]["velocidad_media_kmh"], 1)} km/h; los mismos viajes'],
        ['Transporte público (2026)',
         f'Carritos mejoran (usan el puente: {n(fila("2026", "Savignani", "Red completa", "carrito")["demora_promedio_s"])} s); '
         f'pesados empeoran ({n(fila("2026", "Savignani", "Red completa", "pesado")["demora_promedio_s"])} s; FFAA a nivel saturada)',
         f'Carritos y pesados casi sin cambio ({n(fila("2026", "Perozo", "Red completa", "carrito")["demora_promedio_s"])} y '
         f'{n(fila("2026", "Perozo", "Red completa", "pesado")["demora_promedio_s"])} s; base: '
         f'{n(fila("2026", "Base", "Red completa", "carrito")["demora_promedio_s"])} y {n(fila("2026", "Base", "Red completa", "pesado")["demora_promedio_s"])} s)'],
        ['Horizonte 2041', f'El que mejor responde: {n(R["2041", "Savignani"]["velocidad_media_kmh"], 1)} km/h y '
         f'{n(R["2041", "Savignani"]["volumen_promedio_veh_h"])} viajes (base {n(R["2041", "Base"]["velocidad_media_kmh"], 1)} km/h); '
         'depende de la Av. En Proyección',
         f'Perrokero en {ds("2041", "Perozo", "Perrokero")}, pero el resto del eje colapsa '
         f'({n(R["2041", "Perozo"]["velocidad_media_kmh"], 1)} km/h)'],
        ['Problema principal detectado', 'Salida de un carril hacia la Costanera bajo el puente (S26)',
         'Semáforo repartido para una Av. Río mucho más cargada que la real; un solo carril a nivel en el acceso norte (P10)']],
       [4.2, 5.4, 5.4], tam=9)

doc.add_heading('6. Elementos para las recomendaciones (objetivo 3)', level=1)
vineta('Ninguna de las dos propuestas, por sí sola, mantiene un nivel de servicio aceptable en 2041: la solución del eje requiere '
       'intervenir más de una intersección. Savignani resiste mejor porque la Av. En Proyección saca tránsito de la FFAA.')
vineta('Perozo: resuelve Perrokero, pero su semáforo de 120 s se repartió para una Av. Río mucho más cargada que la real; conviene '
       'reprogramarlo con la demanda actual. Revisar la pendiente del 15 % (P4, P9).')
vineta('Savignani: el distribuidor necesita una salida de dos carriles hacia la Costanera bajo el puente; sin ella traslada el '
       'cuello de botella. Las bahías de bus y los carriles de incorporación sí aportan y pueden conservarse en la propuesta final.')
vineta('Los buses y demás pesados no pueden usar los puentes: necesitan un carril a nivel que no quede saturado (en Savignani, '
       'FFAA a nivel con un carril y 20 s de verde).')
nota('Estas ideas son el punto de partida para la propuesta final, que se simulará con la misma metodología; sus resultados se '
     'agregarán a este mismo formato. Las incongruencias de cada tesis citadas (S26, P4, P9, P10) están en '
     'INCONGRUENCIAS_TESIS_EVALUADAS.md.')

doc.save(SALIDA)
print('guardado', SALIDA)
