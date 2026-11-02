"""Genera 'SUGERENCIAS CAPITULO II - MARCO TEORICO.docx': temas y definiciones sugeridas para el capitulo II."""
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
_txt = open(os.path.join(AQUI, 'generar_doc.py'), encoding='utf-8').read()
exec(_txt[:_txt.index('# ------------------------------------------------------------------ valores')])  # estilos y funciones comunes

SALIDA_CAP2 = r'C:\Users\samue_yffy\Desktop\TRABAJO DE GRADO\SUGERENCIAS CAPITULO II - MARCO TEORICO.docx'


def nota(texto):
    par = doc.add_paragraph()
    r = par.add_run('Importante: ')
    r.bold = True
    r.font.size = Pt(10)
    r2 = par.add_run(texto)
    r2.font.size = Pt(10)
    sombra(par, 'EEF3F8')


def bloque(titulo, intro, filas):
    doc.add_heading(titulo, level=2)
    if intro:
        p(intro)
    cuadro('', ['Tema', 'Qué debe explicar (en lenguaje sencillo)', 'Para qué se necesita en esta tesis', 'Dónde tomarlo'],
           filas, [3.0, 5.6, 4.0, 3.4], fuente='', tam=8)


p('SUGERENCIAS PARA EL CAPÍTULO II', negrita=True, tam=16, centro=True)
p('MARCO TEÓRICO', negrita=True, tam=14, centro=True)
p('Temas, bases teóricas, bases legales y definición de términos', cursiva=True, centro=True)
p('')
p('Este documento propone qué debe contener el capítulo II para que cualquier lector, aunque no sepa de tránsito ni '
  'de simulación, entienda la tesis. Se armó revisando el capítulo II de Estanga y Savignani (2021) y de Assouad y '
  'Peroza (2022), y comparándolo con lo que realmente se hizo en esta investigación. Las tesis anteriores explican bien '
  'el diseño vial y el método del HCM, pero no tratan la simulación, que es el centro de esta tesis: por eso se marcan '
  'como NUEVO los temas que no aparecen en ellas.')
nota('Las dos tesis evaluadas tienen párrafos idénticos en el capítulo II y en las bases legales. Se recomienda no '
     'copiar su texto: usar las mismas fuentes originales (MTC, MINDUR, HCM, Arias, etc.) y redactar con palabras propias, '
     'para evitar problemas de plagio.')

doc.add_heading('1. Estructura sugerida del capítulo', level=1)
p('Según el Manual de la Universidad Santa María (2023), el capítulo II lleva antecedentes nacionales e internacionales, '
  'bases teóricas y bases legales. Ambas tesis evaluadas agregan además una definición de términos, que en esta tesis es '
  'muy útil por la cantidad de términos técnicos. Orden sugerido:')
for t in ['2.1 Antecedentes de la investigación (nacionales e internacionales).',
          '2.2 Bases teóricas: 2.2.1 Vialidad urbana · 2.2.2 Intersecciones · 2.2.3 Control del tránsito · '
          '2.2.4 Características del tránsito · 2.2.5 Capacidad y nivel de servicio · 2.2.6 Proyección del tránsito · '
          '2.2.7 Simulación del tránsito (NUEVO) · 2.2.8 Evaluación de propuestas y costos.',
          '2.3 Bases legales.',
          '2.4 Definición de términos.']:
    vineta(t)

doc.add_heading('2. Antecedentes sugeridos', level=1)
cuadro('', ['Antecedente', 'Por qué incluirlo', 'Qué resaltar'],
       [['Estanga y Savignani (2021), USM: propuestas para la Av. La Costanera (nacional)',
         'Es una de las tesis que se evalúan', 'Diagnóstico (Camino Real en F, CC Paos en C), propuesta del distribuidor tipo puente y bahías de bus; método HCM.'],
        ['Assouad y Peroza (2022), USM: intersección Av. Fuerzas Armadas con Av. Río (nacional)',
         'Es la otra tesis que se evalúa', 'Diagnóstico de Perrokero (F), puente sobre FFAA y semáforo de 120 s; método HCM.'],
        ['Villalba (2022), Universidad Católica Boliviana: modelación del tránsito en la Av. Busch con SUMO (internacional)',
         'Ya se cita en el capítulo I; usa el mismo software', 'Cómo se construye y valida un modelo en SUMO.'],
        ['Uno o dos trabajos internacionales más que usen SUMO u otro microsimulador para evaluar intersecciones o distribuidores',
         'El manual pide antecedentes internacionales y conviene respaldar el uso de la simulación', 'Buscar en repositorios universitarios o Google Académico ("SUMO microsimulación intersección", "evaluación de distribuidor vial simulación").']],
       [5.0, 4.0, 7.0], fuente='', tam=9)

doc.add_heading('3. Bases teóricas: temas que conviene desarrollar', level=1)
bloque('3.1 Vialidad urbana', None, [
    ['Vía, carretera y vialidad urbana', 'Qué es una vía y en qué se diferencia una vía urbana de una carretera.', 'Ubicar al lector: el eje es urbano.', 'Ambas tesis (2.2.1 y 2.2.3); MINDUR (1981)'],
    ['Red vial y clasificación funcional', 'Tipos de vías según su función: expresa, arterial, colectora, local.', 'La Av. Fuerzas Armadas y la Av. Río son colectoras (Perozo, según el INTT); la Costanera es una vía interurbana principal.', 'Ambas tesis (2.2.2); MINDUR (1981)'],
    ['Sección transversal', 'Partes de la vía: calzada, carril, isla o separador central, brocal y acera.', 'Son los datos del Cuadro 4.2 (anchos de las tesis).', 'Ambas tesis (2.2.4.3 / 2.2.5); MTC (1997)'],
    ['Velocidad de diseño y de operación', 'La velocidad con que se diseña la vía frente a la que realmente llevan los conductores.', 'El modelo usa 40 km/h; las tesis observan de 40 a 50 km/h.', 'Ambas tesis; MTC (1997)'],
    ['Vehículo de diseño', 'El vehículo tipo que se usa para dimensionar la vía (auto, camión, autobús).', 'Explica los tipos de vehículo del modelo y por qué el puente de Savignani se diseña para un camión de 9,1 m.', 'Ambas tesis (2.2.4.2.2); MTC (1997)']])
bloque('3.2 Intersecciones', None, [
    ['Intersección y sus tipos', 'Lugar donde se cruzan dos o más vías. A nivel (en T, en cruz, canalizada) y a desnivel.', 'Las 5 intersecciones del eje son de distintos tipos.', 'Ambas tesis (2.2.7)'],
    ['Intersección a desnivel o distribuidor tipo puente', 'Una vía pasa por encima de la otra para separar los movimientos que se cruzan.', 'Es la propuesta de ambas tesis.', 'Ambas tesis (2.2.7.1.2 y 2.2.9)'],
    ['Elementos del puente', 'Rampa, pendiente, gálibo (altura libre debajo), tablero, curvas verticales.', 'Para describir y criticar las propuestas (rampas al 12,3 % y al 15 %).', 'Ambas tesis (2.2.9); MTC (1997)'],
    ['Carriles de cambio de velocidad', 'Carril de salida (desaceleración) e incorporación (aceleración) para entrar o salir sin frenar la avenida.', 'Propuesta 2 de Savignani en Bissau.', 'Perozo (2.2.8.4)'],
    ['Bahía de autobús', 'Espacio fuera del carril donde el bus se detiene sin bloquear el tránsito.', 'Propuesta 2 de Savignani.', 'Savignani (cap. V); MVDUCT'],
    ['Isla central, separador y retorno', 'Elementos que separan sentidos o permiten dar la vuelta.', 'La propuesta de prolongar la isla de Savignani.', 'Perozo (2.2.8.5)'],
    ['Puntos de conflicto', 'Lugares donde las trayectorias se cruzan, convergen o divergen; explican los choques y demoras.', 'Justifican por qué se proponen puentes y semáforos.', 'Ambas tesis (2.2.8 / 2.2.11)']])
bloque('3.3 Dispositivos de control del tránsito', None, [
    ['Semáforo', 'Dispositivo que asigna el paso por turnos.', 'Camino Real y CC Paos tienen semáforo; Perozo propone uno.', 'Perozo (2.2.17.1); MVDUCT/INTT (2011)'],
    ['Ciclo, fase, verde, amarillo y todo rojo', 'Ciclo: tiempo de una vuelta completa de luces. Fase: parte del ciclo en que un grupo de movimientos tiene verde.', 'Cuadro 4.4 (semáforos de campo) y el análisis del semáforo de Savignani.', 'Ambas tesis; HCM 2000'],
    ['Verde efectivo, tiempo perdido y relación g/C', 'Qué parte del ciclo se aprovecha realmente para pasar.', 'Fórmula de capacidad de los accesos con semáforo.', 'HCM 2000; Savignani (2.2.16.3)'],
    ['Intersección no semaforizada, prioridad y señal de PARE', 'Cómo se reparte el paso sin semáforo: la vía principal tiene prioridad y la secundaria espera.', 'Perrokero, Bissau y Puerto Guaica no tienen semáforo.', 'Ambas tesis (2.2.16.2 / 2.2.15); HCM 2000'],
    ['Brecha (intervalo) y aceptación de brechas', 'El hueco entre vehículos que necesita un conductor de la vía secundaria para cruzar o incorporarse.', 'Explica la cola de la Av. Río en Perrokero.', 'HCM 2000 (brecha crítica tc y tiempo de seguimiento tf)'],
    ['Señalización y demarcación', 'Señales verticales (PARE, velocidad máxima) y marcas en el pavimento.', 'Inventario de señales del Cuadro 4.3.', 'Perozo (2.2.17); MVDUCT/INTT (2011)']])
bloque('3.4 Características del tránsito', None, [
    ['Volumen y tasa de flujo', 'Vehículos que pasan por un punto en un tiempo (veh/h).', 'Es el dato de entrada de todo el estudio.', 'Ambas tesis (2.2.11 / 2.2.13); HCM 2000'],
    ['Demanda frente a volumen', 'Demanda: los que quieren pasar. Volumen: los que logran pasar. Si la vía se satura, son distintos.', 'Explica la "demanda atendida" de los resultados. NUEVO.', 'HCM 2000'],
    ['Movimientos de una intersección', 'Movimiento de frente, giro a la izquierda y giro a la derecha (códigos MF, GI, GD).', 'Los volúmenes del Cuadro 4.8 están por movimiento.', 'Ambas tesis'],
    ['Composición vehicular', 'Livianos, pesados y transporte público; los pesados ocupan más espacio y arrancan más lento.', 'El modelo tiene tres tipos de vehículo (sin motos).', 'HCM 2000 (factor de pesados fVP)'],
    ['Hora pico y factor de hora de máxima demanda (FHMD)', 'La hora más cargada del día y qué tan concentrado está el tránsito dentro de ella.', 'FHMD de diseño 0,90; simulado 0,89.', 'Ambas tesis; HCM 2000'],
    ['Tránsito promedio diario (TPD)', 'Promedio de vehículos por día; las tesis lo usan para pasar del aforo a la hora pico.', 'Explica de dónde salen los volúmenes de las tesis.', 'Ambas tesis'],
    ['Velocidad media', 'Distancia recorrida entre tiempo empleado.', 'Indicador del Cuadro 1.2 y de la red completa.', 'HCM 2000'],
    ['Densidad e intensidad', 'Densidad: vehículos por kilómetro de vía. Intensidad: vehículos por hora que pasan.', 'Hojas de densidad del Excel y tramos críticos.', 'Savignani (2.4); HCM 2000'],
    ['Cola', 'Fila de vehículos detenidos esperando pasar; se mide en metros.', 'Indicador de los Cuadros 4.10 y 4.12.', 'HCM 2000'],
    ['Congestionamiento', 'Cuando la demanda supera la capacidad y aparecen colas y demoras.', 'Planteamiento del problema.', 'Ambas tesis (2.2.9 / 2.2.12)']])
bloque('3.5 Capacidad y nivel de servicio', None, [
    ['Capacidad', 'Máximo de vehículos por hora que puede atender un acceso o una vía.', 'Base del diagnóstico.', 'Ambas tesis (2.2.15); HCM 2000'],
    ['Flujo de saturación', 'Vehículos por hora de verde que pasan cuando hay cola.', 'Fórmula de capacidad con semáforo: c = s · g/C.', 'HCM 2000; Savignani'],
    ['Relación volumen/capacidad (V/C)', 'Qué tan cerca está un acceso de su límite: mayor que 1 significa saturado.', 'Indicador del Cuadro 1.2.', 'HCM 2000'],
    ['Demora (demora de control)', 'Tiempo que pierde un vehículo por la intersección frente a circular libre.', 'Es la medida que define el nivel de servicio.', 'HCM 2000; ambas tesis'],
    ['Nivel de servicio (NDS o LOS)', 'Letra de A (flujo libre) a F (colapso) según la demora. Incluir las dos tablas del HCM 2000: con semáforo (10/20/35/55/80 s) y sin semáforo (10/15/25/35/50 s).', 'Es el resultado principal de la tesis.', 'HCM 2000; ambas tesis (2.2.16)'],
    ['Método del HCM 2000', 'Cómo se calcula el NDS a mano (lo que hicieron las tesis) y su limitación: analiza cada intersección aislada.', 'Explica por qué la simulación capta efectos de red que el HCM no ve.', 'HCM 2000; ambas tesis']])
bloque('3.6 Proyección del tránsito', None, [
    ['Crecimiento del tránsito y tasa de crecimiento', 'El tránsito aumenta cada año; se proyecta con una tasa (2,5 % anual según el INE).', 'Paso de 2021 a 2026 (×1,131) y de 2026 a 2041 (×1,448).', 'Ambas tesis (2.2.12-2.2.14)'],
    ['Período o horizonte de diseño', 'Años para los que se evalúa una obra (15 años en esta tesis).', 'Escenario 2041.', 'Ambas tesis'],
    ['Recuperación del tránsito post COVID-19', 'Por qué los aforos de 2020-2021 subestiman el tránsito normal (pandemia y crisis de combustible).', 'Supuesto del +50 % (×1,5) tomado de Savignani. NUEVO como tema.', 'Savignani (cap. IV)']])
bloque('3.7 Simulación del tránsito (NUEVO: no está en las tesis evaluadas)',
       'Es el bloque más importante para que se entienda esta tesis, porque es su herramienta principal.', [
    ['Modelo y simulación de tránsito', 'Representar en computadora el movimiento de los vehículos para probar cambios antes de construirlos.', 'Justifica el uso de SUMO.', 'Villalba (2022); Lopez y otros (2018)'],
    ['Niveles de modelación', 'Macroscópico (flujos), mesoscópico y microscópico (cada vehículo por separado).', 'SUMO es microscópico.', 'FHWA, Traffic Analysis Toolbox vol. III'],
    ['SUMO (Simulation of Urban Mobility)', 'Software libre desarrollado por el Centro Aeroespacial Alemán (DLR); qué hace y para qué se usa.', 'Herramienta de la tesis.', 'Lopez y otros (2018); documentación oficial de SUMO'],
    ['Red de simulación', 'Cómo se representa la vía: nodos (cruces), tramos (edges), carriles y conexiones. Se importó de OpenStreetMap con netconvert y se ajustó con netedit.', 'Fase III del procedimiento.', 'Documentación de SUMO'],
    ['Demanda de simulación', 'Rutas y flujos de vehículos que entran a la red; generación de rutas a partir de conteos (muestreo de rutas).', 'Cómo se cargaron los volúmenes de las tesis.', 'Documentación de SUMO (routeSampler)'],
    ['Modelo de seguimiento vehicular', 'Cómo decide cada conductor su velocidad según el vehículo de adelante (modelo de Krauss).', 'Explica parámetros como aceleración, tiempo de reacción e imperfección.', 'Krauss (1998); documentación de SUMO'],
    ['Modelo de cambio de carril', 'Cómo decide un vehículo cambiar de carril (por ruta, por velocidad o para cooperar).', 'Comportamiento en accesos y bahías.', 'Documentación de SUMO (LC2013)'],
    ['Parámetros de comportamiento', 'Aceleración, desaceleración, factor de velocidad, imperfección (sigma), impaciencia.', 'Cuadro 4.5 (parámetros del modelo).', 'Documentación de SUMO'],
    ['Detectores de simulación', 'Medidores virtuales: el detector E3 mide la demora de los vehículos que atraviesan una intersección.', 'De ahí salen las demoras y colas.', 'Documentación de SUMO'],
    ['Calentamiento, período de análisis y vaciado', 'La red empieza vacía: se simulan 15 min antes de medir y se deja vaciar al final.', 'Configuración de las corridas.', 'FHWA, Traffic Analysis Toolbox vol. III'],
    ['Aleatoriedad, semilla y réplicas', 'Cada corrida tiene llegadas al azar; se repite con distintas semillas y se promedia.', 'Las 5 réplicas.', 'FHWA, Traffic Analysis Toolbox vol. III'],
    ['Calibración y validación', 'Ajustar el modelo y comprobar que reproduce la realidad.', 'Validez del modelo.', 'FHWA, Traffic Analysis Toolbox vol. III'],
    ['Estadístico GEH', 'Medida para comparar volúmenes simulados con observados: GEH < 5 se considera buen ajuste; se exige en al menos el 85 % de los casos.', '60 de 61 movimientos cumplen.', 'FHWA, Traffic Analysis Toolbox vol. III'],
    ['Teletransporte (y por qué se desactivó)', 'SUMO puede sacar de la red a un vehículo atascado; aquí se desactivó para que las colas sean reales.', 'Explicación de los resultados de 2041.', 'Documentación de SUMO']])
bloque('3.8 Evaluación de propuestas y costos', None, [
    ['Factibilidad técnica', 'Si una obra funciona técnicamente: mejora la circulación y cumple las normas.', 'Es el objetivo general.', 'Manual USM; literatura de proyectos'],
    ['Escenario sin proyecto y con proyecto', 'Comparar la situación sin hacer nada con cada propuesta, con la misma demanda.', 'Diseño experimental de la tesis.', 'FHWA, Traffic Analysis Toolbox vol. III'],
    ['Indicadores de efectividad', 'Reducción de la demora y del tiempo de viaje, aumento de la velocidad, cambio de nivel de servicio.', 'Indicadores del Cuadro 1.2.', 'HCM 2000'],
    ['Presupuesto: cómputos métricos y análisis de precios unitarios (APU)', 'Cómo se calcula el costo de una obra: cantidades por partida por su precio unitario.', 'Objetivo 4.', 'Normas venezolanas de presupuesto; Savignani (5.9)']])

doc.add_heading('4. Bases legales sugeridas', level=1)
p('Las dos tesis usan la misma base legal; conviene mantenerla, actualizarla y redactarla con palabras propias:')
for t in ['Constitución de la República Bolivariana de Venezuela (1999): competencias en vialidad y obras públicas.',
          'Ley Orgánica del Poder Público Municipal: competencias del municipio en vialidad urbana y tránsito.',
          'Ley de Transporte Terrestre (G.O. 38.985, 2008) y su reglamento.',
          'Normas técnicas: Normas para el Proyecto de Carreteras del MTC (1997), Manual de Vialidad Urbana del MINDUR (1981) '
          'y Manual Venezolano de Dispositivos Uniformes para el Control del Tránsito (MVDUCT/INTT, 2011). '
          'El HCM 2000 es una referencia técnica internacional, no una norma legal: va en las bases teóricas.']:
    vineta(t)

doc.add_heading('5. Definición de términos sugerida', level=1)
p('Lista en orden alfabético con una definición sencilla de referencia. Cada definición debe redactarse con su fuente '
  '(HCM 2000, MINDUR, MVDUCT, documentación de SUMO o las tesis).')
terminos = [
    ['Acceso', 'Cada una de las vías por las que los vehículos llegan a una intersección.'],
    ['Aforo vehicular', 'Conteo de los vehículos que pasan por un punto, por tipo y movimiento.'],
    ['Bahía de autobús', 'Ensanche de la vía donde el autobús se detiene fuera del carril de circulación.'],
    ['Brecha (intervalo)', 'Tiempo entre el paso de dos vehículos consecutivos; el conductor de la vía secundaria espera una brecha suficiente para cruzar.'],
    ['Calibración', 'Ajuste de los parámetros del modelo para que reproduzca lo observado.'],
    ['Calzada', 'Parte de la vía destinada a la circulación de vehículos.'],
    ['Capacidad', 'Número máximo de vehículos por hora que puede atender un acceso o una vía en condiciones dadas.'],
    ['Carril', 'Franja de la calzada por la que circula una fila de vehículos.'],
    ['Carril de incorporación / de salida', 'Carril auxiliar que permite acelerar para entrar a la avenida o desacelerar para salir de ella.'],
    ['Ciclo semafórico', 'Tiempo que tarda el semáforo en completar la secuencia de todas sus fases.'],
    ['Cola', 'Fila de vehículos detenidos o casi detenidos esperando pasar.'],
    ['Demanda', 'Número de vehículos que quieren usar una vía en un período, aunque no todos logren pasar.'],
    ['Demanda atendida', 'Porcentaje de la demanda que realmente logra pasar en la hora.'],
    ['Demora', 'Tiempo adicional que tarda un vehículo respecto a circular a la velocidad libre.'],
    ['Densidad', 'Número de vehículos por kilómetro de vía.'],
    ['Detector', 'En la simulación, medidor virtual que registra el paso, la velocidad o la demora de los vehículos.'],
    ['Distribuidor a desnivel', 'Obra en la que una vía pasa por encima o por debajo de otra para separar movimientos.'],
    ['Escenario', 'Conjunto de condiciones simuladas (red, semáforos y demanda): base 2026, futuro 2041 o con propuesta.'],
    ['Factor de hora de máxima demanda (FHMD)', 'Relación entre el volumen de la hora pico y cuatro veces el volumen del cuarto de hora más cargado.'],
    ['Fase semafórica', 'Parte del ciclo en la que un grupo de movimientos tiene luz verde al mismo tiempo.'],
    ['Flujo de saturación', 'Máximo de vehículos por hora de verde que pasan por un acceso cuando hay cola.'],
    ['Gálibo', 'Altura libre bajo un puente.'],
    ['GEH', 'Estadístico que compara un volumen simulado con uno observado; valores menores que 5 indican buen ajuste.'],
    ['Hora pico', 'Período de una hora con el mayor volumen de tránsito del día.'],
    ['Intersección', 'Área donde se cruzan o se unen dos o más vías.'],
    ['Intersección no semaforizada', 'Intersección sin semáforo, donde la vía secundaria cede el paso a la principal.'],
    ['Isla o separador central', 'Elemento físico que separa los dos sentidos de circulación.'],
    ['Microsimulación', 'Simulación que representa el movimiento de cada vehículo por separado.'],
    ['Movimiento direccional', 'Trayectoria de un vehículo en una intersección: de frente, giro a la izquierda o giro a la derecha.'],
    ['Nivel de servicio (NDS)', 'Medida de la calidad de operación, de A (excelente) a F (colapso), según la demora.'],
    ['Pesado (vehículo)', 'Camión o autobús; ocupa más espacio y acelera más lento que un auto.'],
    ['Punto de conflicto', 'Lugar donde se cruzan, unen o separan trayectorias de vehículos.'],
    ['Rampa', 'Tramo inclinado que conecta el nivel de la calle con el puente.'],
    ['Red vial', 'Conjunto de vías conectadas de una zona.'],
    ['Réplica', 'Repetición de una simulación con una semilla aleatoria distinta.'],
    ['Semilla aleatoria', 'Número que inicia la secuencia de azar de una simulación; cambiarla cambia las llegadas de vehículos.'],
    ['Sección transversal', 'Corte de la vía que muestra sus partes y anchos: calzada, carriles, isla, brocal y acera.'],
    ['SUMO', 'Simulation of Urban Mobility: software libre de microsimulación de tránsito del Centro Aeroespacial Alemán (DLR).'],
    ['Tasa de crecimiento', 'Porcentaje anual en que aumenta el tránsito.'],
    ['Tiempo de viaje', 'Tiempo que tarda un vehículo desde su origen hasta su destino.'],
    ['Tránsito promedio diario (TPD)', 'Promedio de vehículos que pasan por un punto en un día.'],
    ['Validación', 'Comprobación de que el modelo reproduce la realidad con un error aceptable.'],
    ['Velocidad de diseño', 'Velocidad que se usa para dimensionar los elementos de la vía.'],
    ['Velocidad media', 'Distancia recorrida dividida entre el tiempo empleado.'],
    ['Volumen de tránsito', 'Número de vehículos que pasan por un punto en un período.'],
    ['Volumen/capacidad (V/C)', 'Relación entre la demanda y la capacidad; mayor que 1 indica saturación.'],
]
cuadro('', ['Término', 'Definición de referencia'], terminos, [4.5, 11.5], fuente='', tam=9)

doc.add_heading('6. Recomendaciones de forma', level=1)
for t in ['Ir de lo general a lo particular: primero la vía y la intersección, luego el tránsito, después la capacidad y el nivel de servicio, y al final la simulación.',
          'Usar en el capítulo II los mismos nombres que en el capítulo IV (por ejemplo, "demora de control", "nivel de servicio", "demanda atendida", "réplica"), para que el lector los reconozca.',
          'Incluir figuras sencillas: tipos de intersección, partes de la sección transversal, puntos de conflicto, un esquema de fases de semáforo, la tabla de nivel de servicio del HCM y una captura de la red en SUMO.',
          'Explicar en un párrafo por qué se simula en vez de solo calcular con el HCM: la simulación ve cómo la cola de una intersección afecta a las demás (efecto de red), que es lo que pasa en 2041.',
          'Revisar que toda cita tenga su referencia en la lista final (en el capítulo I hay citas de Aragón, Baray, Sabino y Hernández sin referencia).']:
    vineta(t)
doc.add_heading('Fuentes sugeridas', level=2)
for t in ['Transportation Research Board (2000). Highway Capacity Manual (HCM 2000). Washington, D.C.',
          'Dowling, R., Skabardonis, A. y Alexiadis, V. (2004). Traffic Analysis Toolbox Volume III: Guidelines for Applying Traffic Microsimulation Modeling Software. FHWA.',
          'Lopez, P. A. y otros (2018). Microscopic Traffic Simulation using SUMO. IEEE Intelligent Transportation Systems Conference (ITSC).',
          'Krauss, S. (1998). Microscopic Modeling of Traffic Flow: Investigation of Collision Free Vehicle Dynamics. Tesis doctoral, DLR / Universidad de Colonia.',
          'Ministerio de Transporte y Comunicaciones (1997). Normas para el Proyecto de Carreteras.',
          'MINDUR (1981). Manual de Vialidad Urbana.',
          'INTT (2011). Manual Venezolano de Dispositivos Uniformes para el Control del Tránsito.',
          'Documentación oficial de SUMO: sumo.dlr.de/docs.']:
    vineta(t)

doc.save(SALIDA_CAP2)
print('guardado', SALIDA_CAP2)
