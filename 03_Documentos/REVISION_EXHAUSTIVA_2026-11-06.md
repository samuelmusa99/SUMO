# Revisión exhaustiva antes del objetivo 3 (06/11/2026)

Revisión de las tres simulaciones (base, Savignani y Perozo; 2026 y 2041), de los datos de entrada frente a las tesis evaluadas y de la solidez estadística de los resultados. Sirve para decidir qué corregir antes de las recomendaciones.

## Veredicto

- **Lo que está sólido:** la geometría sale de las tesis y cada decisión está documentada (incongruencias S1–S26 y P1–P19). Los modelos corren sin teletransportes y casi sin choques, todo se reproduce con scripts, y las propuestas están simuladas como las escriben sus autores, corrigiendo solo lo que no funciona y declarándolo.
- **Lo que un jurado puede atacar:** (1) la **demanda**, sobre todo en Perrokero, y el factor post COVID; (2) que el GEH se presente como **validación**, cuando solo verifica la asignación; (3) varias diferencias entre escenarios **no son estadísticamente significativas con 5 réplicas**.
- Ninguno invalida el trabajo, pero los tres conviene resolverlos **antes** de las recomendaciones, porque las recomendaciones se apoyan en esas diferencias.

---

## 1. Puntos críticos

### 1.1 El +50 % post COVID no es un dato de Savignani sobre el tránsito existente
- Savignani usa el +50 % solo como hipótesis para chequear su propia propuesta: "esta estima un incremento mínimo del 50 %, para lo cual el tiempo de demora será de 35,1 seg" (imp. 233 / PDF 259). Su escenario actual y su proyección a 2036 usan solo el 2,5 % anual del INE (imp. 195–196).
- Perozo **no aplica** ningún factor post COVID: solo el 2,5 % anual (imp. 135–136).
- El modelo base usa ×1,5 sobre los volúmenes de ambas tesis (factor total ×1,697). Es un supuesto del autor inspirado en Savignani, y debe presentarse así, no como dato de la tesis.
- El escenario de sensibilidad (×1,131, `REVISION_SIMULACION_BASE.md` 2b) cambia el diagnóstico: Perrokero pasa de F 145 s a C 13,7 s y la red de 23 a 37 km/h.

### 1.2 En Perrokero, el modelo tiene de 3 a 10 veces lo contado en campo

| Movimiento | Tesis 2021 | Modelo 2026 (×1,697) | Campo 2026 | Modelo / campo |
|---|---|---|---|---|
| FFAA sur → Camino Real (MF2) | 519 | 881 | 260 | 3,4 |
| FFAA sur → Av. Río (GD3) | 275 | 467 | 60 | 7,8 |
| **Camino Real → Av. Río (GI4)** | 225 | **382** | **40** | **9,5** |
| Camino Real → FFAA sur (MF5) | 568 | 964 | 180 | 5,4 |

- En Camino Real y CC Paos el modelo y el campo coinciden razonablemente (0,7 a 1,6), pero en Perrokero no.
- Además, en Perrokero se mezclan fuentes: la FFAA usa tesis ×1,697 y la Av. Río usa el conteo propio (180 veh/h). Así la avenida principal queda muy cargada frente a una secundaria contada en campo. Esto explica que la Av. Río del modelo base solo descargue 122 veh/h, cuando en campo salen 180.
- **Consecuencia para Perozo:** el problema principal que se le detectó, la cola del acceso norte que tapa la entrada al puente, depende del giro GI4 de 382 veh/h, que en campo es de 40. Si el giro real se parece más al campo, ese problema desaparece.
- **Causa probable:** el conteo de campo fue de 2 a 3 minutos por intersección, multiplicado por 20 o 30. Con muestras tan cortas el error es enorme, sobre todo en giros de poco volumen.

**Sugerencia (la más importante de esta revisión):** contar con los videos de campo, en la hora pico, al menos 15 minutos por intersección (ideal una hora, en períodos de 15 minutos), empezando por Perrokero y por una sección de la Costanera. Con eso:
1. se decide con evidencia entre ×1,697 y ×1,131 (o un valor intermedio);
2. se puede validar con datos independientes (ver 1.3);
3. se cierra la pregunta "¿por qué su modelo tiene 5 veces lo que usted contó?".

Si no es posible, hay que presentar los dos escenarios de demanda como rango (alto y bajo) y decir cuál se adopta y por qué.

### 1.3 El GEH no es una validación del modelo
- El GEH < 5 en 60 de 61 movimientos compara el modelo con los volúmenes que se le impusieron (tesis × factor). Demuestra que la asignación de rutas reproduce la demanda objetivo, pero **no** que el modelo represente la realidad. Un evaluador con experiencia en simulación lo va a notar.
- **Redacción sugerida:** "verificación de la asignación de la demanda (GEH)". La "validación" debe hacerse con datos independientes que el modelo no recibió: colas máximas medidas en video, tiempo de recorrido del eje (con un vehículo de prueba o con los videos) o el flujo de descarga de la Av. Río (campo 180 veh/h).

---

## 2. Puntos importantes

### 2.1 Cinco réplicas no alcanzan para todas las conclusiones
Prueba t de Welch (95 %) entre cada propuesta y la base, sobre la demora media:

| Comparación | Base | Propuesta | ¿Significativa? |
|---|---|---|---|
| 2026 red completa, Savignani | 159,8 s | 115,4 s | Sí |
| **2026 red completa, Perozo** | 159,8 s | 117,2 s | **No** (t = 2,2) |
| 2026 Camino Real, Savignani | 43,9 s | 81,7 s | Sí |
| 2026 Perrokero, Savignani / Perozo | 145,2 s | 40,2 / 62,3 s | Sí / Sí |
| 2026 CC Paos, Bissau (ambas) | — | — | No |
| 2026 Puerto Guaica, Savignani | 17,0 s | 4,9 s | Sí |
| 2041 red completa, Savignani | 1.280 s | 1.217 s | No |
| 2041 red completa, Perozo | 1.280 s | 754 s | Sí |
| 2041 Perrokero, Perozo | 241 s | 77 s | Sí |

- Con 5 réplicas, el intervalo de confianza del 95 % de varias demoras es de ±20 a ±75 %. Algunos ejemplos: Perrokero de Perozo, ±55 %; puente hacia el sur, ±69 %; Av. Río de Savignani, ±153 %.
- **Sugerencia:** correr **10 a 20 réplicas** en los seis escenarios. En SUMO esto tarda unos minutos y no cambia ningún dato. Además:
  - justificar el número de réplicas en la metodología con n = (t·s/E)²; los evaluadores suelen preguntarlo;
  - reportar el intervalo de confianza y decir qué diferencias son significativas.
- El documento de comparación dice que Perozo mejora la red en 2026; con 5 réplicas esa mejora todavía no es significativa.

### 2.2 Las demoras de 2041 no deben citarse como cifras exactas
- Hay demoras de 2.934 s, 5.960 s y 8.158 s. En una red sobresaturada, la demora depende del largo de la simulación y de cuántos vehículos quedan atrapados. Como número no tiene sentido físico.
- **Sugerencia:** en 2041 reportar sobre todo el nivel F, el porcentaje de demanda atendida, los viajes completados y la velocidad de la red. Las demoras de más de 300 s pueden ir como "> 300 s (F)".

### 2.3 Perozo: el semáforo de la tesis se diseñó para otra demanda
- Perozo reparte el verde (Norte 33, Oeste 20, Sur 25 y Este 30 s) pensando en una Av. Río de unos 963 veh/h en 2041. En el modelo, la Av. Río tiene 172 veh/h (conteo propio), así que sus 30 s de verde se desperdician mientras el acceso norte, con el giro GI4, queda corto.
- Evaluar la propuesta "tal cual" es correcto. Pero para el objetivo 3 es una recomendación natural: retemporizar el semáforo (Webster o HCM) con la demanda real. Debe ir como recomendación, no como corrección de la propuesta.
- **P10:** el modelo deja 1 carril a nivel por sentido, como la figura; el cálculo HCM de la tesis supone 2. Está bien documentado y debe consultarse con el tutor, porque cambia mucho la capacidad a nivel.

### 2.4 Savignani: el 30 % de la Av. En Proyección influye en el resultado
- Es un supuesto propio y le quita tránsito a la FFAA. Para que no lo cuestionen, conviene correr una sensibilidad con 0 % (avenida sin tránsito, como el cálculo del Anexo B) y quizás con 15 %. Así se muestra que la conclusión (Camino Real empeora por la salida de un carril, S26) no depende de ese número.

---

## 3. Detalles menores

- **Carritos en el puente de Perozo:** Perozo prohíbe solo los "vehículos pesados" (imp. 155–156). Los carritos (por puestos) son automóviles. En Savignani está bien dejarlos a nivel, porque su Alternativa C habla de "tráfico pesado colectivo". En Perozo lo estricto sería permitirles subir al puente. El efecto es chico (pocos carritos cruzan Perrokero), pero es coherente con la tesis.
- **Pendiente de las rampas:** los livianos suben y bajan los puentes a unos 37–40 km/h, casi a la velocidad máxima, así que en la simulación la pendiente (12,3 y 15 %) prácticamente no penaliza. Para livianos en rampas cortas es aceptable, pero en la tesis conviene decir que la operación en las rampas es la de flujo libre, sin efecto de la pendiente.
- **Distinto criterio de nivel de servicio en Perrokero:** la base y Savignani usan el criterio sin semáforo (el peor acceso secundario); Perozo usa el criterio con semáforo. Para comparar entre escenarios conviene usar la demora (con su intervalo) además de la letra.
- **Velocidad de la red:** la base da 23,3 km/h y las tesis reportan 40–50 km/h observados. Sirve como chequeo de realismo; con ×1,131 da 37 km/h. Es otro argumento para medir en video.
- **Bissau y Puerto Guaica con Savignani:** mejoran en parte porque llega menos tránsito (queda retenido en Camino Real). Ya está explicado; mantenerlo en la redacción.

---

## 4. Lo que está bien y se puede defender

- Geometría solo de las tesis, número de carriles de campo y anchos documentados (incluidos los que no se aplicaron y por qué).
- Semáforos de la base medidos en campo; los de las propuestas son los de las tesis, salvo el de Savignani, que no se puede programar (S11 a S13) y está justificado.
- Cada propuesta está simulada como la plantea su autor, y cada desviación está documentada: la isla de Savignani, el 30 % de la Av. En Proyección y el carril a nivel de Perozo.
- 0 teletransportes; calentamiento de 15 minutos; hora de análisis de 900 a 4.500 s; FHMD simulado de 0,89 frente a 0,90 de las tesis.
- Las comparaciones con las tesis están explicadas: los errores de cálculo de Savignani (S1 a S4) y las incongruencias de Perozo (P1, P13 y P17).
- Las conclusiones principales son significativas con 5 réplicas: Savignani empeora Camino Real; Perozo mejora Perrokero en 2026 y 2041; Perozo mejora la red en 2041.

---

## 5. Orden sugerido antes de las recomendaciones

1. **Contar en los videos** (Perrokero y una sección de la Costanera; colas máximas en Camino Real, FFAA y Av. Río). Es lo que más fortalece la tesis.
2. Con eso, **decidir el factor de demanda** (o presentar el rango) y, si cambia, regenerar la demanda y volver a correr los escenarios. Los scripts ya existen.
3. **Subir a 10 réplicas o más** en los seis escenarios y agregar el intervalo de confianza y la significancia a los cuadros.
4. **Sensibilidad de Savignani** con 0 % en la Av. En Proyección.
5. Llevar al tutor: el factor post COVID, el GEH como verificación, P10 (carriles a nivel de Perozo), el semáforo de 122 s de Savignani y la isla.
6. Recién entonces, las recomendaciones del objetivo 3 y la propuesta final.
