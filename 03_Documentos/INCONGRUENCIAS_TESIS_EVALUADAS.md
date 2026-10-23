# Incongruencias encontradas en las tesis evaluadas

**Uso:** apoyo para el objetivo 3 (recomendaciones a las propuestas originales) y para la comparación con la simulación.
Se va completando a medida que se revisa cada propuesta. Páginas: **impresa** (número al pie) / **PDF** (visor).

**Actualizado:** 23/10/2026

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

*Pendiente de una revisión detallada al trabajar la rama `propuestaPerozo`. Hallazgos previos:*

| # | Incongruencia | Dónde | Efecto |
|---|---|---|---|
| P1 | La demora de la intersección es de **2.883,7 s** en la Tabla 4.9 y de **1.000,03 s** en las conclusiones. | Tabla 4.9; conclusiones | Resultado principal inconsistente. |
| P2 | En las conclusiones, el costo aparece como **"$ x.xxx.xxx"** (texto de plantilla sin completar). | Conclusiones | Error de edición. |
| P3 | **Longitud de rampas contradictoria**: 40 m en un lugar y 100 m en otro. | Diseño del puente | Geometría no definida. |
| P4 | Rampas al **15 %**, alto para una vía urbana. | Diseño del puente | Problema de seguridad y de operación para los pesados. |
| P5 | La Av. Río se describe con **1 carril de 5 m**; en campo tiene 2 carriles por sentido (confirmado por el usuario). | Cap. 4 | Capacidad del acceso mal representada. |
| P6 | Costos tomados de una tesis extranjera (Quito, 2012). | Costos | No refleja precios locales. |
| P7 | Aforo hecho durante la pandemia y la crisis de combustible. | Cap. 4 | Volúmenes inciertos. |

---

## 3. Comunes a ambas tesis
- Rampas muy empinadas para una vía urbana (12,3 % y 15 %).
- Costos tomados de tesis extranjeras (Bogotá 2017 y Quito 2012).
- Aforos hechos en condiciones atípicas (pandemia y crisis de combustible).
