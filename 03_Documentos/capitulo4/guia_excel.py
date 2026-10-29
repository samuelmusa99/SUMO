"""Genera 'GUIA DEL EXCEL DE RESULTADOS.docx': explicacion hoja por hoja del Excel de la simulacion base."""
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
_txt = open(os.path.join(AQUI, 'generar_doc.py'), encoding='utf-8').read()
exec(_txt[:_txt.index('# ------------------------------------------------------------------ valores')])  # estilos y funciones comunes

def nota(texto):
    par = doc.add_paragraph()
    r = par.add_run('Importante: ')
    r.bold = True
    r.font.size = Pt(10)
    r2 = par.add_run(texto)
    r2.font.size = Pt(10)
    sombra(par, 'EEF3F8')


SALIDA_GUIA = r'C:\Users\samue_yffy\Desktop\EXCEL RESULTADOS\GUIA DEL EXCEL DE RESULTADOS.docx'
I26 = {r['interseccion']: r for r in rep26 if r['nivel'] == 'INTERSECCION'}
R26 = {r['acceso']: r for r in rep26 if r['nivel'] == 'RED'}


def hoja(nombre, que_es, origen, columnas, como_leer, resultado, tutor=None):
    doc.add_heading(nombre, level=2)
    par = doc.add_paragraph()
    par.add_run('Qué es: ').bold = True
    par.add_run(que_es)
    par = doc.add_paragraph()
    par.add_run('De dónde sale: ').bold = True
    par.add_run(origen)
    if columnas:
        cuadro(f'Columnas de la hoja "{nombre}"', ['Columna', 'Significado'], columnas, [4.5, 11.0],
               fuente='', tam=9)
    par = doc.add_paragraph()
    par.add_run('Cómo se lee: ').bold = True
    par.add_run(como_leer)
    par = doc.add_paragraph()
    par.add_run('Qué dice hoy (base 2026): ').bold = True
    par.add_run(resultado)
    if tutor:
        nota(tutor)


# ------------------------------------------------------------------ portada
p('GUÍA DEL EXCEL DE RESULTADOS', negrita=True, tam=16, centro=True)
p('RESULTADOS SIMULACION.xlsm (base 2026) y RESULTADOS SIMULACION 2041.xlsm', tam=12, centro=True)
p('Qué contiene cada hoja, de dónde sale y cómo se interpreta cada resultado', cursiva=True, centro=True)
p('')

doc.add_heading('1. Cómo se produce el Excel', level=1)
p('Todo el Excel se llena automáticamente al ejecutar SIMULACION.bat (o SIMULACION_2041.bat). El proceso es:')
for t in ['Se abre SUMO-GUI y se simula la hora pico con una semilla aleatoria (la "corrida de referencia", la que se ve en pantalla).',
          'Al cerrar SUMO, sus resultados en XML se convierten a CSV (viajes, colas y densidades).',
          'El script resumen_resultados.py calcula, de esa misma corrida, la demora y el nivel de servicio por intersección y por '
          'acceso, y los indicadores de los viajes.',
          'El script replicas.py corre la simulación 5 veces más sin ventana (semillas 1 a 5) y promedia los resultados.',
          'Se abre el Excel y una macro (Workbook_Open → RefreshAll) actualiza todas las consultas de Power Query, que leen esos CSV.']:
    vineta(t)
p('El tiempo simulado se divide en: 0 a 15 min de calentamiento (la red se carga), 15 a 75 min de hora de análisis (lo '
  'único que se mide) y 75 a 90 min de vaciado. Por eso en el Excel las horas van de 00:15 a 01:15.')
nota('Hay dos tipos de hojas y conviene decirlo primero: (1) las hojas "Reporte..." y "Analisis..." y los resúmenes '
     'Resumen Intersecciones y Resumen Viajes salen de UNA sola corrida, la del SUMO-GUI, y sirven para ver el detalle '
     '(cada vehículo, cada tramo, cada segundo); (2) la hoja Resumen Replicas es el promedio de 5 corridas y es la que '
     'se usa en la tesis. Por eso las cifras de una hoja y otra no coinciden exactamente: cada corrida tiene llegadas '
     'aleatorias distintas.')

doc.add_heading('2. Las hojas, una por una', level=1)

hoja('Reporte Viajes',
     'La lista de todos los vehículos que entraron a la red durante la hora de análisis, uno por fila (4.580 en la corrida de referencia).',
     'Archivo reporte_viajes.xml de SUMO (salida "tripinfo"), de la corrida de referencia.',
     [['ID Vehiculo', 'Nombre del vehículo. La letra indica el tipo (L liviano, P pesado) y el número, la ruta y el cuarto de hora en que salió.'],
      ['Tipo de Vehiculo', 'liviano, pesado o carrito (transporte público).'],
      ['Hora de Entrada / Salida', 'Momento en que entró y salió de la red (reloj de la simulación).'],
      ['Lugar de Entrada / Salida', 'Carril donde empezó y terminó el viaje (bordes de la red).'],
      ['Distancia (m)', 'Largo del recorrido.'],
      ['Tiempo de Viaje (s)', 'Cuánto tardó desde que entró hasta que salió.'],
      ['Velocidad Media (km/h)', 'Distancia dividida entre el tiempo de viaje.'],
      ['Tiempo de Demora (s)', 'Tiempo perdido respecto a hacer el mismo recorrido a la velocidad libre de la vía (por colas, semáforos, cruces y frenadas).'],
      ['Nivel de Servicio (LOS)', 'Letra calculada con la demora del viaje completo y la escala del HCM para una intersección. Solo es orientativa (ver nota).'],
      ['Tiempo Detenido', 'Segundos en que el vehículo estuvo prácticamente parado (menos de 0,1 m/s).'],
      ['N.º de Paradas / Tiempo en Paradas', 'Paradas programadas (buses y carritos en las paradas) y su duración.'],
      ['Minutos', 'Cuarto de hora de la hora de análisis en que salió (para el FHMD).'],
      ['Estado del viaje', 'Completado o En la red al final (vehículo atrapado). En 2026 todos están Completado.']],
     'Cada fila es un viaje. Sirve para ver casos particulares (por ejemplo, cuánto tarda alguien de FFAA a Lechería) y '
     'alimenta las hojas Analisis Por Vehiculo y Analisis HMD.',
     '4.580 viajes, todos completados (ningún vehículo atrapado ni teletransportado).',
     'La columna "Nivel de Servicio (LOS)" de esta hoja NO es el nivel de servicio de la tesis: aplica la escala de una '
     'intersección (10/20/35/55/80 s) a la demora de todo el viaje, que pasa por 2 a 5 intersecciones. Por eso muchos '
     'viajes salen en F. El nivel de servicio oficial está en Resumen Replicas.')

hoja('Analisis Por Vehiculo',
     'Una tabla dinámica con la velocidad media y la demora promedio por tipo de vehículo, un gráfico de barras y la escala de nivel de servicio del HCM 2000.',
     'Tabla dinámica sobre la hoja Reporte Viajes (corrida de referencia).',
     None,
     'Compara cómo les va a livianos, pesados y transporte público en todo su recorrido. La tabla de la derecha es la '
     'escala de nivel de servicio de una intersección semaforizada (A ≤ 10 s; B ≤ 20; C ≤ 35; D ≤ 55; E ≤ 80; F > 80 s).',
     'Livianos 31,5 km/h y 127,5 s de demora; pesados 26,2 km/h y 116,7 s; carritos 29,8 km/h y 133,7 s.',
     'La velocidad de esta hoja (31,2 km/h en total) es el promedio de las velocidades de cada vehículo, por eso es mayor '
     'que la de Resumen Viajes (25,7 km/h), que divide la distancia total entre el tiempo total: los viajes cortos y '
     'rápidos pesan igual que los largos en el primer cálculo. Para la tesis se usa la de Resumen Replicas.')

hoja('Analisis HMD',
     'El cálculo del factor de hora de máxima demanda (FHMD) de la simulación.',
     'Tabla dinámica que cuenta los vehículos de Reporte Viajes por cuarto de hora, y tres fórmulas.',
     [['Intervalo de minutos', 'Cuarto de hora de la hora de análisis (0-14, 15-29, 30-44, 45-59).'],
      ['Cuenta de ID Vehiculo', 'Vehículos que entraron a la red en ese cuarto de hora.'],
      ['Vehículos que ingresan a la red (veh/h)', 'Total de la hora (V).'],
      ['Volumen máximo (V15min)', 'El cuarto de hora más cargado.'],
      ['FHMD', 'V / (4 × V15max). Vale 1 si el tránsito es parejo y baja si se concentra en un cuarto de hora.']],
     'Sirve para comprobar que la simulación reproduce la variación dentro de la hora pico que se usó al generar la demanda (FHMD de diseño 0,90, promedio de las tesis).',
     '1.117, 1.289, 1.111 y 1.063 vehículos por cuarto de hora: V = 4.580 y FHMD = 4.580 / (4 × 1.289) = 0,89. Coincide con el 0,90 de diseño.')

hoja('Reporte Colas',
     'La longitud de la cola en cada carril, segundo a segundo, cuando hay vehículos detenidos.',
     'Archivo reporte_colas.xml de SUMO (salida "queue"), corrida de referencia.',
     [['Intervalo de Tiempo', 'Segundo de la simulación.'],
      ['Segmento', 'Carril donde hay cola (tramo_número de carril; el 0 es el de la derecha).'],
      ['Longitud de Cola (m)', 'Largo de la fila de vehículos detenidos en ese carril, medido desde el final del carril.'],
      ['Demora por Cola (s)', 'Tiempo que lleva esperando el vehículo de adelante de la cola.']],
     'Son unas 108.000 filas: se usa filtrando por un tramo para ver cómo crece y se disipa la cola. Las colas por acceso '
     'ya resumidas (promedio y máxima) están en Resumen Replicas.',
     'Las colas más largas y persistentes aparecen en la Av. Río (Perrokero), con unos 160 m y esperas de más de 6 minutos.')

hoja('Reporte Densidad',
     'La densidad y la intensidad del tránsito en cada tramo de la red, cada 100 segundos.',
     'Archivo reporte_densidad.xml de SUMO (medidor "edgeData" de medidores.add.xml), corrida de referencia.',
     [['Tramo', 'Identificador del tramo de vía en la red.'],
      ['Longitud Tramo (m)', 'Largo del tramo.'],
      ['Inicio / Fin', 'Intervalo de medición en segundos (900-1000, 1000-1100, …).'],
      ['Flujo Entrante / Saliente', 'Vehículos que entraron y salieron del tramo en ese intervalo.'],
      ['Tiempo Acumulado', 'Suma de los segundos que pasaron todos los vehículos en el tramo.'],
      ['Densidad (veh/km)', 'Vehículos presentes por kilómetro de tramo (todos los carriles juntos). Se calcula solo en tramos de 20 m o más.'],
      ['Intensidad (veh/h)', 'Flujo que pasa por el tramo, expresado por hora.']],
     'Densidad baja (menos de 20 veh/km por carril) significa circulación libre; cerca de 100 a 130 veh/km por carril, '
     'los vehículos están prácticamente parados en cola.',
     'Alimenta las hojas Tramos Criticos y Reporte Densidad Interseccion.')

hoja('Tramos',
     'La lista de todos los tramos de la red con su largo y velocidad máxima.',
     'El archivo de la red, costanera.net.xml.',
     None, 'Es una tabla de consulta: sirve para saber qué largo tiene un tramo cuando aparece en otra hoja.',
     'Unos 2.000 tramos (incluye calles internas de urbanizaciones que no tienen tránsito en la simulación).')

hoja('Tramos Criticos',
     'Una tabla dinámica que ordena los tramos de mayor a menor densidad media en la hora de análisis.',
     'Tabla dinámica sobre Reporte Densidad.',
     None, 'Los primeros de la lista son los tramos más congestionados de la red: donde se forman las colas.',
     'Los más críticos son las tres llegadas al semáforo de Camino Real (FFAA unos 204 veh/km, El Ejército 194 y '
     'Costanera 131), la llegada de FFAA a Perrokero desde Camino Real (FA_3, 149 veh/km) y la Av. Fuerzas Armadas entre '
     'ambas intersecciones. Coincide con el diagnóstico: los cuellos de botella son Camino Real y Perrokero.')

hoja('Intersecciones',
     'Una tabla de correspondencia: qué tramos de llegada pertenecen a cada intersección.',
     'Tabla escrita a mano (consulta MAPEO_INTERSECCIONES).',
     None, 'Solo sirve para que la hoja siguiente agrupe los tramos por intersección. Incluye los accesos principales de cada intersección.',
     '14 tramos de llegada en las 5 intersecciones.')

hoja('Reporte Densidad Interseccion y Analisis Intersecciones',
     'La densidad y la intensidad de cada tramo de llegada, agrupadas por intersección (la primera hoja son los datos y la segunda, la tabla dinámica).',
     'Combinación de Reporte Densidad con la hoja Intersecciones.',
     None,
     'En la tabla dinámica, "Promedio de Densidad" es la densidad media de cada llegada y "Suma de Intensidad" el flujo '
     'que llega a la intersección por todos sus accesos principales (veh/h).',
     'Camino Real recibe 2.808 veh/h con 177 veh/km de densidad media en sus llegadas (la más cargada); CC Paos 1.783 '
     'veh/h y 39 veh/km; Perrokero 2.200 veh/h y 73 veh/km; Bissau 2.690 y Puerto Guaica 2.677 veh/h con 38 y 49 veh/km.')

hoja('Resumen Intersecciones',
     'El nivel de servicio de cada intersección y de cada acceso calculado con la corrida de referencia, junto con los valores de las tesis y del conteo de campo.',
     'Script resumen_resultados.py (detectores E3 por intersección y datos por acceso), corrida de referencia.',
     [['volumen_sim_veh_h', 'Vehículos por hora que pasaron por la intersección o el acceso.'],
      ['demora_sim_s', 'Demora de control promedio por vehículo (tiempo perdido al atravesar la intersección).'],
      ['LOS_sim_promedio / LOS_sim_HCM', 'Nivel de servicio con la demora promedio / según el HCM (en intersecciones sin semáforo, el del peor acceso secundario).'],
      ['paradas_por_veh', 'Número promedio de detenciones por vehículo.'],
      ['FHMD_sim', 'Factor de hora de máxima demanda medido en esa intersección.'],
      ['tesis_fuente, tesis_LOS, tesis_demora_s, tesis_volumen_veh_h', 'Lo que obtuvieron Savignani o Perozo para esa intersección (para comparar).'],
      ['campo2026_volumen_veh_h', 'Volumen del conteo de verificación de campo (sin motos).']],
     'Es una "foto" de una sola corrida: útil para verla junto al SUMO-GUI, pero para la tesis se usa Resumen Replicas.',
     'Camino Real D (36 s), CC Paos C (21 s), Perrokero F (99 s), Bissau C, Puerto Guaica C.')

hoja('Resumen Viajes',
     'Los indicadores de todos los viajes de la corrida de referencia, por tipo de vehículo.',
     'Script resumen_resultados.py sobre Reporte Viajes.',
     [['viajes', 'Vehículos que salieron en la hora de análisis.'],
      ['tiempo_viaje_s', 'Tiempo promedio de viaje.'],
      ['demora_s', 'Tiempo perdido promedio por viaje.'],
      ['tiempo_detenido_s', 'Tiempo promedio detenido.'],
      ['velocidad_media_kmh', 'Distancia total entre tiempo total en movimiento.'],
      ['teleports_simulacion', 'Vehículos que SUMO sacó de la red por estar atascados; está desactivado, debe ser 0.']],
     'Mide cómo le va al usuario en todo su recorrido, sin importar cuántas intersecciones cruce.',
     '4.580 viajes; 279 s de viaje y 127 s de demora en promedio; 25,7 km/h; 0 teletransportes.')

rr = I26
hoja('Resumen Replicas (la hoja que va a la tesis)',
     'El resultado oficial: el promedio de 5 corridas con semillas distintas, por intersección, por acceso y para toda la red.',
     'Script replicas.py.',
     [['interseccion / nivel / acceso', 'Dónde se mide: INTERSECCION (todos los accesos), ACCESO (cada llegada) o RED (todos los viajes, por tipo de vehículo).'],
      ['replicas', 'Número de corridas promediadas (5).'],
      ['volumen_promedio_veh_h', 'Vehículos por hora que pasaron (en filas RED: número de viajes).'],
      ['demora_promedio_s', 'Demora de control promedio de las 5 corridas (en filas RED: demora por viaje).'],
      ['demora_min_s / demora_max_s', 'La corrida con menos y con más demora: muestran la variabilidad.'],
      ['desviacion_estandar_s', 'Cuánto varía la demora entre corridas.'],
      ['LOS_promedio / LOS_HCM', 'Nivel de servicio de la demora promedio / según el criterio del HCM (sin semáforo: peor acceso secundario).'],
      ['demanda_veh_h', 'Vehículos por hora que quieren pasar (la demanda generada, aunque no logren entrar).'],
      ['capacidad_veh_h y fuente_capacidad', 'Máximo de vehículos por hora que admite el acceso. "HCM 2000": calculada con las fórmulas del HCM; "medida": acceso saturado, se usa lo que realmente descarga; en 2041, "capacidad de la situación actual 2026".'],
      ['VC', 'Relación volumen/capacidad (demanda / capacidad). Mayor que 1 significa que llega más tránsito del que el acceso puede atender.'],
      ['demanda_atendida_pct', 'Porcentaje de la demanda que realmente pasó. Por debajo de 95 % hay vehículos que no logran pasar en la hora.'],
      ['tesis_LOS / tesis_demora_s', 'Resultado de la tesis evaluada para esa intersección.'],
      ['cola_promedio_m / cola_maxima_m', 'Longitud promedio y máxima de la cola del acceso durante la hora, medida desde la línea de detención hacia atrás.'],
      ['cola_llena_el_tramo', '"si" si la cola ocupó todo el tramo medido (unos 300 m o hasta la intersección anterior): la cola real puede ser mayor.'],
      ['velocidad_media_kmh', 'Velocidad media en los tramos del acceso (en filas RED: de todos los viajes).'],
      ['tiempo_viaje_s', 'Solo en filas RED: tiempo de viaje promedio.']],
     'Para cada intersección: primero la letra (LOS_HCM) y la demora; luego la V/C y la demanda atendida dicen si el '
     'problema es de capacidad; las colas y la velocidad dicen hasta dónde llega el efecto. El rango mínimo-máximo indica '
     'qué tan estable es el resultado.',
     f"Camino Real {rr['Camino Real']['LOS_HCM']} ({n(rr['Camino Real']['demora_promedio_s'], 1)} s, V/C {n(rr['Camino Real']['VC'], 2)}); "
     f"CC Paos {rr['CC Paos']['LOS_HCM']} ({n(rr['CC Paos']['demora_promedio_s'], 1)} s); "
     f"Perrokero {rr['Perrokero']['LOS_HCM']} ({n(rr['Perrokero']['demora_promedio_s'], 1)} s, V/C {n(rr['Perrokero']['VC'], 2)}, la Av. Río atiende el "
     f"{fila(rep26, 'Perrokero', 'Este (Av. Rio)')['demanda_atendida_pct']} % de su demanda); Bissau y Puerto Guaica con la "
     f"Costanera fluida y las salidas residenciales con esperas. Toda la red: {n(R26['TOTAL']['volumen_promedio_veh_h'])} viajes, "
     f"{n(R26['TOTAL']['tiempo_viaje_s'])} s de viaje, {n(R26['TOTAL']['demora_promedio_s'])} s de demora y {n(R26['TOTAL']['velocidad_media_kmh'], 1)} km/h.",
     'Las columnas de colas, velocidad y tiempo de viaje se agregaron en octubre de 2026. La consulta de Power Query '
     'las convierte a número solo si el CSV las trae, así que los Excel de corridas anteriores siguen funcionando: '
     'simplemente no muestran esas columnas hasta volver a correr el .bat.')

doc.add_heading('3. Glosario de los resultados', level=1)
cuadro('Términos que aparecen en el Excel',
       ['Término', 'Qué significa', 'Cómo se interpreta'],
       [['Demanda (veh/h)', 'Vehículos que quieren usar la vía en la hora pico.', 'Sale de los volúmenes de las tesis actualizados a 2026.'],
        ['Volumen (veh/h)', 'Vehículos que realmente pasaron.', 'Si es menor que la demanda, la vía no alcanza.'],
        ['Demanda atendida (%)', 'Volumen / demanda.', '100 % = todos pasan; menos de 95 % = la vía está saturada.'],
        ['Demora (s/veh)', 'Tiempo perdido por vehículo frente a circular libre.', 'Es lo que define el nivel de servicio.'],
        ['Nivel de servicio (LOS)', 'Letra de A (libre) a F (colapso) según la demora, HCM 2000.', 'Con semáforo: 10/20/35/55/80 s; sin semáforo: 10/15/25/35/50 s.'],
        ['Capacidad (veh/h)', 'Máximo de vehículos que admite el acceso en una hora.', 'Depende de carriles, semáforo y pesados, no de la demanda.'],
        ['V/C', 'Demanda / capacidad.', 'Menor que 0,85 holgado; 0,85-1 cerca del límite; mayor que 1 saturado.'],
        ['Cola (m)', 'Largo de la fila de vehículos detenidos.', 'Muestra hasta dónde llega el efecto de la intersección.'],
        ['Velocidad media (km/h)', 'Distancia / tiempo.', 'Las tesis observaron 40 a 50 km/h en el corredor.'],
        ['Densidad (veh/km)', 'Vehículos por kilómetro de vía.', 'Alta densidad con baja intensidad = cola.'],
        ['Intensidad (veh/h)', 'Flujo que pasa por un punto.', 'Igual que volumen, pero medido en un tramo.'],
        ['FHMD', 'Volumen horario / (4 × cuarto de hora más cargado).', 'Diseño 0,90; medido en la simulación 0,89.'],
        ['Réplica', 'Una corrida con una semilla aleatoria distinta.', 'Se promedian 5 para que el resultado no dependa del azar.'],
        ['Teletransporte', 'Vehículo que SUMO saca de la red si se atasca demasiado.', 'Desactivado: siempre debe ser 0.']],
       [3.2, 6.0, 6.3], fuente='')

doc.add_heading('4. El Excel de 2041', level=1)
p('RESULTADOS SIMULACION 2041.xlsm tiene exactamente las mismas hojas. Cambian dos cosas: la demanda es la de 2026 '
  'multiplicada por 1,448 (15 años al 2,5 % anual), y en Resumen Replicas la capacidad de cada acceso es la de 2026 '
  '(fuente "capacidad de la situación actual 2026"), porque la vía y los semáforos no cambian. En 2041 aparecen '
  'vehículos "En la red al final" (atrapados) en Reporte Viajes, y las demandas atendidas bajan a 37-51 %: la red '
  'colapsa empezando por Perrokero.')

doc.add_heading('5. Preguntas que puede hacer el tutor', level=1)
for preg, resp in [
    ('¿Por qué no coinciden Resumen Intersecciones y Resumen Replicas?',
     'La primera es una sola corrida (la del SUMO-GUI); la segunda es el promedio de 5. La de la tesis es Resumen Replicas.'),
    ('¿Por qué 5 réplicas?',
     'Con 3 réplicas el margen de la demora de Camino Real era de ±27 s; con 5 baja a ±13 s. Es el equilibrio entre precisión y tiempo de cálculo.'),
    ('¿Cómo se calcula la demora de una intersección?',
     'Con un detector que registra a cada vehículo desde unos 300 m antes de la intersección hasta unos 60 m después, y mide el tiempo que perdió frente a circular libre (demora de control, como en el HCM).'),
    ('¿Por qué Bissau sale en E o F si la demora es de pocos segundos?',
     'En intersecciones sin semáforo el HCM asigna a la intersección el nivel del peor acceso secundario (la salida de la residencia), aunque la avenida circule fluida.'),
    ('¿Qué significa una V/C mayor que 1?',
     'Que llega más tránsito del que el acceso puede atender: se forman colas que crecen y parte de la demanda no logra pasar en la hora (por eso la demanda atendida baja de 100 %).'),
    ('¿Cómo sé que el modelo es válido?',
     'Por el GEH: 60 de 61 movimientos tienen GEH < 5 (criterio ≥ 85 %), por el FHMD de 0,89 frente a 0,90 de diseño, y porque CC Paos (C) y Perrokero (F) coinciden con las tesis.'),
    ('¿Por qué el nivel de servicio por vehículo de Reporte Viajes sale casi todo F?',
     'Porque aplica la escala de una intersección a la demora de todo el viaje, que cruza varias. Es solo una referencia; el nivel de servicio oficial es por intersección.')]:
    par = doc.add_paragraph(style='List Bullet')
    par.add_run(preg + ' ').bold = True
    par.add_run(resp)

doc.save(SALIDA_GUIA)
print('guardado', SALIDA_GUIA)
