# Incongruencias encontradas en las tesis evaluadas

**Uso:** apoyo para el objetivo 3 (recomendaciones a las propuestas originales) y para la comparación con la simulación.
Se va completando a medida que se revisa cada propuesta. Páginas: **impresa** (número al pie) / **PDF** (visor).

**Actualizado:** 04/11/2026

---

## 1. Estanga y Savignani (2021): Costanera, de la Prolongación Av. El Ejército a la Av. Fabricio Ojeda

### 1.1 Datos y cálculo de la situación actual

| # | Incongruencia | Dónde | Efecto |
|---|---|---|---|
| S1 | La Tabla 55 usa **GD3 = 603 veh/h** (acceso Norte, giro a la derecha), pero su propia Tabla 37 da **GD3 = 190 veh/h**. | Tabla 55 y Tabla 56, imp. 215–216 / PDF 241–242; Tabla 37, imp. 191 / PDF 217 | Sobrestima la demanda del acceso Norte de Camino Real. |
| S2 | La Tabla 56 usa **35 % de pesados** en el acceso Norte, mientras la Tabla 37 da **6 %**. | Tabla 56, imp. 216 / PDF 242 | Reduce el flujo de saturación y empeora el nivel de servicio. |
| S3 | **Ciclo de 111 s imposible** (Tabla 54): Norte 40 + 3 + 68, Sur 68 + 3 + 40 y Oeste 37 + 3 + 71. Solo Norte y Sur ya suman 114 s; con tres fases seguidas el ciclo sería de unos 154 s. | Tabla 54, imp. 215 / PDF 241 | El nivel F (121–129 s) de Camino Real se calcula con un semáforo que no puede existir. El semáforo medido en campo en 2026 tiene un ciclo de 82 s. |
| S4 | El nivel **F en los accesos residenciales** (Bissau y Fernández Padilla, demoras de 1.074 a 1.228 s) es un error de cálculo del HCM. Recalculado da unos 28 s (nivel D). | Cap. 4, imp. 205–206 / PDF 231–232 | Justifica la propuesta 2 con un problema exagerado. |
| S5 | Para Camino Real no calculan un horizonte futuro sin proyecto, porque "no se considera necesario" (ya da F). | imp. 220 / PDF 246 | No hay un escenario futuro sin proyecto contra el cual comparar la propuesta. |
| S6 | El aforo se hizo durante la pandemia de COVID-19 y la crisis de combustible. Ellos mismos estiman una caída del 70 al 90 % (o del 75 %) del tránsito y luego suponen un aumento "mínimo del 50 %". | imp. 229–233 / PDF 255–259 | Los volúmenes de diseño son inciertos. En la simulación se aplicó ×1,5 como recuperación post COVID. |
| S22 | **Ancho de la Costanera contradictorio**: los Anexos B y C dicen "dos canales de 8 m" con separador de 1 m, pero las Tablas 25 y 26 dan calzadas de 7,4 m (2 × 3,7 m) con isla de 1,3 m. Además, la Tabla 25 reporta un sentido de la Costanera de 6,3 m como "2 carriles de 3,15 m", mientras que la Fig. 84 muestra que esos 6,3 m son **un solo carril** (el canal de giro libre hacia El Ejército), junto a 2 carriles de 3,7 m. | Tablas 25 y 26, imp. 173 / PDF 199; Fig. 84, imp. 174; Anexos B y C, imp. 270–271 | En la simulación: 2 × 3,70 m por sentido y canal de giro de 6,30 m (según la Fig. 84). |
| S23 | **Prolongación Av. El Ejército contradictoria**: la Tabla 25 da 10,1 m con "2 carriles de 5,05 m" en **ambos** sentidos e isla de 1,8 m; la Fig. 84 muestra 2 × 5,05 m de un lado, isla de 1,3 m y 2 × 3,7 m del otro; el Anexo G da 10,1 m de entrada y 6,3 m de salida. En campo hay 3 carriles de entrada. | Tabla 25, imp. 173; Fig. 84, imp. 174; Anexo G, imp. 279 | Un carril de 5,05 m no es normativo. En la simulación: entrada de 3 × 3,37 m (los 10,1 m de la tesis repartidos en los 3 carriles de campo) y salida de 2 × 3,70 m (Fig. 84). |
| S24 | En la Tabla 26 los carriles de la Costanera son de "2 de 3,75 m" (7,5 m), pero la calzada se reporta en 7,4 m. | Tabla 26, imp. 173 | Detalle de medición. |
| S25 | **Ninguna de las dos tesis reporta radios de giro ni hombrillos** de las intersecciones existentes. Solo dan calzada, carriles, brocal, isla y acera. | Tablas 25 y 26; Perozo, Cuadros 4.1 y 4.2 | El indicador "radios de giro" y "hombrillos" del Cuadro 1.2 no tiene fuente en las tesis. |

### 1.2 Propuesta 1: distribuidor en Camino Real

| # | Incongruencia | Dónde | Efecto |
|---|---|---|---|
| S7 | **Dos pendientes distintas para las rampas**: el Cuadro 26 y la sección 5.4.1 dan **12,3 %** (7,4 m en 60 m), pero la descripción de las rampas dice **9,83 %**. | Cuadro 26, imp. 240; "Rampas de acceso", imp. 242 / PDF 268; 5.4.1, imp. 245 | En la simulación se usó 12,3 %, que es la que sale de sus dimensiones. Además, 12,3 % es alto para una vía urbana con pesados. |
| S8 | **Curvas verticales más cortas que el mínimo que ellos mismos calculan**: la curva 1 da Lv = 70,92 m y adoptan 50 m; la curva 2 da 148 m y adoptan 100 m; la curva 3 da 70,92 m y adoptan 50 m. | 5.4.1, Tablas 76–78, imp. 246–250 | El perfil no cumple su propio criterio de K·i. |
| S9 | Toman **K = 6 "para una velocidad de diseño de 50 km/h"**, pero la velocidad de diseño de la propuesta es de **40 km/h** (Cuadro 26). | imp. 246 | Criterio inconsistente. |
| S10 | Dicen que entre la rampa y el puente se forman **4 curvas verticales**, luego que usan **3**, y calculan solo 3. Las abscisas de la Tabla 77 son incoherentes: el PIC2 aparece en 0+115 y en 0+155, y el PTV2 en 0+165 y en 0+205. | imp. 245–251 | Perfil longitudinal poco confiable. |
| S11 | **Semáforo de la propuesta con tres ciclos distintos** en la misma intersección (Anexo B): Norte 88 s, Sur 83 s y "Este" 113 s. Además, cada g/C se calcula con su propio ciclo (40/83 = 0,48 y 80/113 = 0,71). | Anexo B, imp. 269 / PDF 295 | El nivel C (35,1 s) es optimista y la tabla no se puede programar. Con los verdes seguidos, el ciclo sería de 169 s. |
| S12 | En el Anexo B, la fase 4 se llama **"Este"**, pero corresponde a **El Ejército (Oeste)**: su g/C de 0,71 es 80/113. | Anexo B, imp. 269 | Error de nombre. |
| S13 | **Las fases no separan los movimientos que se cruzan.** Con cuatro brazos a nivel bajo el puente (Costanera, FFAA, El Ejército y Av. En Proyección), cada acceso necesita su propia fase. El esquema de 3 fases deja movimientos en conflicto y no le da verde a la Av. En Proyección. | Anexo B, imp. 269; Anexo G, imp. 279 | Sin modificar no funciona. En la simulación se usa un semáforo de 4 fases (av. en proyección 30 s, El Ejército 40 s, Costanera 20 s y FFAA 20 s, con 3 s de amarillo; ciclo de 122 s). |
| S14 | **La Av. En Proyección aparece dibujada pero sin tránsito**: está en la Fig. 125 y en el Anexo G, y en la imp. 232 la justifican como la "futura conexión" con la Av. Guzmán Lander. Pero el cálculo del Anexo B no le asigna volumen ni fase. | Fig. 125, imp. 257 / PDF 283; imp. 232 / PDF 258; Anexo B | El nivel C no considera el tránsito que la avenida atraería. En la simulación se supuso que el 30 % de los viajes de FFAA sur que cruzan Camino Real la usan (supuesto propio, a declarar). |
| S15 | La Alternativa C dice que el canal a nivel del acceso Sur es para **"tráfico pesado colectivo"**, pero en el Anexo B ese acceso tiene **fVP = 1,00** (sin pesados) y fB = 0,75. | imp. 232 / PDF 258; Anexo B | La capacidad del acceso FFAA a nivel queda sobrestimada. |
| S16 | El vehículo de diseño del puente es un camión SU de 9,1 m (Cuadro 26), pero el texto de la Alternativa C manda los pesados a nivel. | Cuadro 26, imp. 240; imp. 232 | No queda claro si el puente se diseñó para pesados. En la simulación los pesados cruzan a nivel. |
| S17 | La separación central del puente es de **0,30 m** en el Cuadro 26 y en el texto, y en el Anexo G aparece una "isleta Av" de **1,3 m**. | Cuadro 26; Anexo G, imp. 279 | Detalle de dimensiones. |
| S26 | **El propio cálculo del Anexo B muestra un acceso saturado**: el giro de El Ejército hacia la Costanera (685 veh/h en 1 carril) tiene Xc = **1,04** y 61,4 s (nivel E), aunque la intersección se presenta en nivel C (35,1 s). Debajo del puente, ese giro y el de FFAA sale por **un solo carril** hacia la Costanera. | Anexo B, imp. 269 / PDF 295; Anexo G | La propuesta deja un cuello de botella a nivel. En la simulación, ese carril de salida recibe 897 veh/h (683 de El Ejército) y El Ejército queda en F; la cola bloquea también el acceso al puente. |

### 1.3 Propuesta 2: accesos residenciales y bahías

| # | Incongruencia | Dónde | Efecto |
|---|---|---|---|
| S18 | **Prolongar la isla central sin definir dónde retornan** los vehículos: se eliminan los giros a la izquierda y los retornos en Bissau y en Puerto Guaica / Fernández Padilla, pero no se indica otro punto de retorno. En la red, Bissau → Camino Real queda sin ruta posible y otros movimientos dan rodeos de unos 2 km. | 5.1, imp. 237–238 / PDF 263; 5.8, imp. 256–257 | Sin un retorno, la propuesta deja movimientos sin solución. **Pendiente: consulta con el tutor**; por ahora no se aplica en la simulación. |
| S19 | No hay planos de la isla prolongada ni de los carriles. Las Fig. 118 y 119 son fotos satelitales con marcas, y solo se dan dimensiones generales: carriles de 3 × 50 m y bahías de 30 (20) × 2,5 m con cuñas de 20 (15) m. | 5.5, imp. 251–252 / PDF 277–278 | La ubicación exacta la tuvo que definir el modelador. |

### 1.4 Propuesta 3: CC Paos

| # | Incongruencia | Dónde | Efecto |
|---|---|---|---|
| S20 | Proponen **"solo la mejora del ciclo de semaforización"**, pero no dan un ciclo nuevo: la Tabla 68 (15 años) es idéntica a la actual (Tabla 61). Además, sus fases tienen ciclos de 108, 99 y 109 s dentro de la misma intersección. | 5.1; Tablas 61 y 68, imp. 220 y 224 | La propuesta 3 no se puede evaluar tal como está escrita. En la simulación se mantiene el ciclo de campo (66 s). |

### 1.5 Costos

| # | Incongruencia | Dónde | Efecto |
|---|---|---|---|
| S21 | El costo ($3.487.520,41) se toma de un trabajo de grado extranjero (Universidad Católica de Colombia, Bogotá, 2017) sobre otros puentes. | 5.9, imp. 258–259 | No refleja precios de Venezuela en 2026 (objetivo 4). |

---

## 2. Assouad y Peroza (2022): Av. Fuerzas Armadas × Av. Río (Perrokero)

*Revisión del capítulo IV (alternativas) y del capítulo V (diseño) hecha el 04/11/2026 en la rama `propuestaPerozo` (P9–P19).*

| # | Incongruencia | Dónde | Efecto |
|---|---|---|---|
| P1 | La demora de la intersección es de **2.883,7 s** en la Tabla 4.9 y de **1.000,03 s** en las conclusiones. | Tabla 4.9; conclusiones | Resultado principal inconsistente. |
| P2 | En las conclusiones, el costo aparece como **"$ x.xxx.xxx"** (texto de plantilla sin completar). | Conclusiones | Error de edición. |
| P3 | **Longitud de rampas contradictoria**: el Cuadro 5.1 da una "distancia horizontal de la rampa" de **100 m**, pero el texto de 5.6, la Fig. "Dimensiones del puente y rampas" y el perfil dan **rampas de 40 m + tablero de 20 m + rampa de 40 m = 100 m** de longitud total. El Cuadro 5.1 confunde la longitud total con la de la rampa. | Cuadro 5.1, imp. 167 / PDF 189; 5.6 y figuras, imp. 168–170 / PDF 190–192 | Resuelto con las figuras: en la simulación, rampas de 40 m al 15 % y tablero de 20 m centrado en el cruce. |
| P4 | Rampas al **15 %**, alto para una vía urbana. | Diseño del puente | Problema de seguridad y de operación para los pesados. |
| P5 | La Av. Río se describe con **1 carril de 5 m**; en campo tiene 2 carriles por sentido (confirmado por el usuario). | Cap. 4 | Capacidad del acceso mal representada. |
| P6 | Costos tomados de una tesis extranjera (Quito, 2012). | Costos | No refleja precios locales. |
| P7 | Aforo hecho durante la pandemia y la crisis de combustible. | Cap. 4 | Volúmenes inciertos. |
| P8 | **Ancho de carril de FFAA contradictorio**: el Cuadro 4.1 da calzadas de 7,85 m por sentido (2 carriles, 3,92 m c/u), pero el cálculo HCM usa carriles de 3,60 y 3,70 m. | Cuadro 4.1, imp. 127 / PDF 149; tabla de capacidad del cap. 4 | Capacidad calculada con un ancho distinto al medido. En la simulación: 3,92 m. |
| P9 | **El gálibo se usa como altura de la rasante**: la pendiente sale de H = 6,00 m (gálibo) / 40 m = 15 %, pero la sección transversal dibuja vigas bajo el tablero. Con un peralte de vigas de 1,2 a 1,4 m (Savignani usa 1,4 m), o el gálibo real queda en unos 4,6 m o la rasante sube a unos 7,4 m y la rampa a unos **18,5 %**. | 5.6, imp. 170 / PDF 192 | El perfil no cumple a la vez el gálibo de 6 m y la pendiente del 15 %. En la simulación se usa la rasante a 6,00 m de la tesis (15 %). |
| P10 | **Número de carriles a nivel contradictorio**: la Fig. "Ubicación del puente" y el texto de 5.6 dejan **un solo carril de 3,70 m a nivel** a cada lado del puente ("para el flujo de vehículos pesados y para el cruce a la derecha"), pero el cálculo HCM de la intersección bajo el puente usa **2 carriles a nivel por acceso** (GI 3,60 m + MF 3,70 m). El texto también se contradice: "dos carriles por sentido" (imp. 154) y "dos carriles, uno por sentido" (imp. 155). | Figuras y 5.6, imp. 168–169; Cuadro de anchos, imp. 156–157; imp. 154–155 / PDF 176–179 | La capacidad a nivel en FFAA queda sobrestimada (el giro a la izquierda, los pesados y el giro a la derecha comparten en realidad un carril). En la simulación se sigue la figura: el carril izquierdo de FFAA sube al puente y el derecho queda a nivel (se mantienen los 2 carriles de campo). |
| P11 | **Volúmenes 2041 distintos en dos cuadros seguidos**: el cuadro de volúmenes futuros da Norte MF5 = **36** y Oeste GD12 = **86** veh/h, y la tabla de ajuste usa **82** y **98** veh/h. | imp. 156–158 / PDF 178–180 | Detalle de cálculo; el MF5 a nivel debería ser solo de pesados (36). |
| P12 | **Los giros a la derecha no entran en el análisis de capacidad** bajo el puente: GD3 (451 veh/h), GD9 (Av. Río, **425 veh/h**), GD6 y GD12 quedan fuera de los grupos de carriles (solo se calculan GI y MF), sin aclarar si todos funcionan como giros libres canalizados. | imp. 157–159 / PDF 179–181 | La demora de los accesos Este y Sur queda subestimada. |
| P13 | **Niveles de servicio mal asignados por movimiento** (tabla bajo el puente): Norte GI 124,8 s marcado "D" (es F), Norte MF 32,8 s "B" (es C), Sur MF 38,3 s "C" (es D) y Oeste GI 43,8 s "E" (es D). Además, el grado de saturación global se da en **0,87** ("funcionará al 87 %") con dos giros críticos sobresaturados (Norte GI Xc 1,13 y Este GI Xc 1,23). | imp. 159–160 / PDF 181–182 | El resultado de la propuesta se presenta mejor de lo que da su propio cálculo. |
| P14 | **La conclusión no corresponde al cálculo**: bajo el puente la intersección queda en **E (65,6 s)** con giros en F en 2041, pero se presenta como "solución factible a largo plazo", y el capítulo V dice que "eliminará todos los puntos de conflicto al permitir el tráfico fluido en todos los sentidos" y el "libre flujo de los 3.850 veh/h", aunque el semáforo a nivel se mantiene. La demora a nivel es casi igual a la de la Alternativa B sin puente (64,7 s, E). | imp. 160, 164–165 / PDF 182, 186–187; Alternativa B, imp. 148–154 | La ventaja del puente se limita al tránsito directo de FFAA; los giros siguen en F. |
| P15 | **Alternativa B con dos demoras y horizontes mezclados**: el texto da 67,9 s y la tabla 64,7 s (ambos E); la Alternativa A se evalúa a 2042, la B a 15 años (2036) y la C a 2041. | imp. 147–148 y 154 / PDF 169–170 y 176 | Las alternativas no se comparan en el mismo horizonte. |
| P16 | **¿La intersección actual tiene semáforo?** El capítulo V propone "la eliminación de la actual intersección semaforizada", pero la Alternativa B propone "colocar un sistema de semáforos", y la situación actual se analiza como intersección sin semáforo (capacidad media de 450 veh/h, 2.883,7 s). En campo (2026) no hay semáforo. | imp. 146–148 y 165 / PDF 168–170 y 187 | Descripción contradictoria del estado actual. En la simulación base, Perrokero es un cruce sin semáforo. |
| P17 | **El volumen futuro es menor que el actual**: "actualmente para un volumen de 3.850 veh/h… dentro de 20 años para un volumen de 3.403 veh/h". | 4.3.4.6, imp. 146 / PDF 168 | Error en la proyección o en la suma de volúmenes. |
| P18 | **Vehículo de diseño del puente: bus de 12,1 m** (Cuadro 5.1), pero "por restricciones de peso los vehículos pesados no pueden transitar por el puente". | Cuadro 5.1, imp. 167; imp. 155–156 | Igual que S16 en Savignani. En la simulación los pesados cruzan a nivel. |
| P19 | **"Calzada 9,50 m"** en la sección del puente, pero 3,70 + 0,60 + 3,70 = 8,00 m (el Cuadro 5.1 da "ancho de la rampa 8,00 m"); los 9,50 m incluyen las defensas de 0,75 m. | Sección transversal, imp. 170; Cuadro 5.1, imp. 167 | Detalle de rotulado; afecta los cómputos del objetivo 4. |

---

## 3. Comunes a ambas tesis
- Rampas muy empinadas para una vía urbana (12,3 % y 15 %).
- Costos tomados de tesis extranjeras (Bogotá 2017 y Quito 2012).
- Aforos hechos en condiciones atípicas (pandemia y crisis de combustible).
