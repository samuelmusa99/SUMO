# Resumen del trabajo de simulación — Tesis Samuel Mujica (USM, Ing. Civil)

**Actualizado:** 04/11/2026 (tarde: Perozo aplicada, sección 7b) · **Uso:** compartir este archivo al iniciar un chat nuevo para retomar el trabajo.
**Estado general:** la **simulación base (2026 y 2041) está terminada y revisada**, y la información de los objetivos 1 y 2 ya está lista para la redacción. **Savignani está aplicada y simulada** (2026 y 2041, 5 réplicas; resultados en la sección 7); solo faltan las consultas al tutor y refrescar sus Excel. Lo siguiente es **Perozo** y luego la propuesta final. Lo hecho el 02/11 está en la sección 10.

---

## 1. La tesis

- **Título:** Evaluación de la factibilidad técnica de propuestas para mejorar la circulación vehicular en el eje comprendido desde el cruce de las Avenidas Fabricio Ojeda y La Costanera y el cruce con las Avenidas Fuerzas Armadas y Río. Barcelona, Anzoátegui, 2026.
- **Tutor:** Ing. Wolfgang Bandres. **Documento:** `Desktop\TRABAJO DE GRADO\TESIS SAMUEL MUJICA OCTUBRE.docx`.
- **Reparto del trabajo:** Samuel hace la parte del software (SUMO, red, demanda, simulaciones, Excel) y le pasa la información a una **amiga que redacta la tesis en Word**. No modificar el .docx; entregar la información clara (cuadros, notas, borradores cuando se pidan).
- **Objetivos específicos:**
  1. Parámetros de diseño vial.
  2. Capacidad y nivel de servicio actual y futuro con SUMO.
  3. Recomendaciones a las propuestas originales.
  4. Costos.
- **Propuestas evaluadas** (PDF en `Desktop\TRABAJO DE GRADO\`):
  - **Estanga y Savignani (2021)**, en Camino Real (su "intersección 1"): distribuidor tipo puente Costanera ↔ FFAA, 1 carril de 4 m por sentido, luz de 30 m, rasante a 7,4 m (gálibo 6 m + vigas 1,4 m), rampas de 60 m al 12,3 %, que empiezan a 75 m del cruce. Incluye la **Avenida En Proyección** (futura conexión con la Av. Guzmán Lander; Fig. 125 y Anexo G). Además: bahías de bus en Bissau, Puerto Guaica y Fernández Padilla; carriles de salida e incorporación de 3 × 50 m; prolongar la isla central; "mejorar el ciclo" en CC Paos. Costo: $3.487.520,41.
  - **Assouad y Peroza (2022)**, en Perrokero (Av. Fuerzas Armadas × Av. Río): puente de 100 m sobre FFAA, 1 carril por sentido de 3,70 m, gálibo de 6 m, rampas al 15 %, solo livianos (los pesados a nivel); debajo, semáforo de 120 s (verdes N 33 / S 25 / E 30 / O 20 s). Costo: $3.605.643,54.
- **Plan de simulaciones:** base → Savignani → Perozo → propuesta final con las recomendaciones del usuario. Cada una en 2026 y 2041.
- **Las motos se excluyen** por indicación del tutor (solo livianos, pesados y carritos/por puestos). No volver a proponerlas.

---

## 2. Metodología (indicaciones del tutor, 27/10/2026)

- **Diseño experimental** (en SUMO se modifica el diseño vial y se mide su efecto: el escenario sin proyecto es el control y cada propuesta un tratamiento). **Tipo documental** (parte de las tesis ya hechas), con validación de algunos datos en campo.
- **Población:** los vehículos que circulan por el eje. **Muestra:** los vehículos del conteo.
- **Confiabilidad:** juicio de expertos que validan el procedimiento (el manual USM pide 3, 5 o 7 expertos, con validación metodológica, gramatical y de contenido).
- **Manual USM (2023):** el capítulo III lleva 3.7 Validez y confiabilidad, 3.8 Técnicas de procesamiento y 3.9 Procedimiento.
- **Regla de datos:** todos los datos geométricos salen de las tesis evaluadas (Savignani: Tablas 25 y 26 y Fig. 84; Perozo: Cuadros 4.1 y 4.2). **Si las tesis no tienen un dato, no se usa** (no reportan radios de giro ni hombrillos). **No se cambia el número de carriles** del modelo, porque está confirmado en campo.

---

## 3. Organización de carpetas y git

```
Desktop\SUMO\                            repositorio git (GitKraken)
├── 01_Red_Y_Demanda\
│   ├── SIMULACION.bat / SIMULACION_2041.bat   abren SUMO-GUI, convierten a CSV, resumen y corren 5 réplicas (CRLF)
│   ├── tesis_base.sumocfg / escenario_2041.sumocfg
│   ├── costanera.net.xml                red
│   ├── costanera.rou.xml                tipos de vehículo y transporte público con paradas
│   ├── paradas.add.xml, medidores(_2041).add.xml, detectores_intersecciones(_2041).add.xml, vista.xml, mapa_fondo.poly.xml
│   ├── accesos_intersecciones.csv       tramos de cada acceso (lo genera generar_detectores.py)
│   ├── demanda\                         conteos_movimientos.csv, demanda_base.rou.xml, demanda_2041.rou.xml, ajuste_demanda_base.csv (GEH)
│   ├── herramientas\                    generar_demanda.py, generar_detectores.py, resumen_resultados.py, replicas.py, capacidad.py, copiar_excel.py
│   ├── ajustes_red\                     parches de netconvert (documentación); anchos_tesis.edg.xml
│   └── fuentes\                         red_vial.osm
├── 02_Resultados_Base\ 02_Resultados_2041\   XML de SUMO (ignorados por git)
└── 03_Documentos\
    ├── RESUMEN_TRABAJO_SIMULACION.md    este archivo
    ├── INCONGRUENCIAS_TESIS_EVALUADAS.md   errores de las tesis (S1–S26 Savignani, P1–P8 Perozo), base del objetivo 3
    ├── REVISION_SIMULACION_BASE.md      revisión completa de la base y escenario de sensibilidad
    ├── capitulo4\                       generar_doc.py (documento del cap. IV), guia_excel.py (guía del Excel),
    │                                    sugerencias_cap2.py (sugerencias del marco teórico),
    │                                    replicas_anchos_tesis\2026|2041 (resultados finales de la base), sensibilidad_sin_postcovid\,
    │                                    replicas_savignani\2026|2041 (resultados de Savignani del 02/11)
    └── FLUJO VEHICULAR.xlsx (aforo propio), PDF de validación

Desktop\EXCEL RESULTADOS\
├── BASE_2026\  RESULTADOS SIMULACION.xlsm        FUTURO_2041\  RESULTADOS SIMULACION 2041.xlsm
├── PROPUESTA_SAVIGNANI\2026|2041\  RESULTADOS SAVIGNANI 2026|2041.xlsm
├── PROPUESTA_PEROZO\2026|2041\     RESULTADOS PEROZO 2026|2041.xlsm   (copias del base, 29/10)
├── PROPUESTA_FINAL\2026|2041\      RESULTADOS FINAL 2026|2041.xlsm    (copias del base, 29/10)
├── GUIA DEL EXCEL DE RESULTADOS.docx    explicación hoja por hoja (para el tutor)
└── _RESPALDOS\                     versiones viejas de cada carpeta y Excel
```

**Git (02/11/2026):**
| Rama | Contenido |
|---|---|
| `main` (`744747c` + este resumen) | Simulación base final + reporte de puentes y tiempo en paradas (sin efecto en la base) |
| `propuestaPerozo` (`bdbdedb`) | Igual a main + sus `.bat` (escriben en `PROPUESTA_PEROZO\2026` y `\2041`). Red todavía sin la propuesta. |
| `propuestaFinal` (`d350840`) | Igual a main + sus `.bat` (`PROPUESTA_FINAL\2026` y `\2041`). Red todavía sin la propuesta. |
| `propuestaSavignani` (`4e8ec59` + este resumen) | Main fusionado el 02/11 + la propuesta (ver sección 7) |
| `respaldo/propuesta*-2026-10-23` | Versiones viejas, también en GitHub |

- Falta **push normal** (sin force) de las 4 ramas: los commits del 02/11 son locales.
- El usuario hace commit y push en GitKraken. **No hacer Pull/Sync** en una rama reiniciada, porque mezcla la versión vieja de GitHub (si pasa: `git merge --abort`).
- Para llevar cambios de main a una propuesta: fusionar main en la rama. En `costanera.net.xml` conservar la red de la propuesta y aplicarle el parche que cambió en main con `netconvert -s ... -e <parche>`; luego regenerar los detectores.

---

## 4. Simulación base: decisiones tomadas

### Demanda (hora pico)
- **Fuente:** volúmenes por movimiento del capítulo 4 de ambas tesis (Savignani: Tablas 37 y 38 y Cuadros 21 y 23; Perozo: Tabla 4.3), en `demanda\conteos_movimientos.csv` (filas `tesis2021`).
- **2026:** ×1,025⁵ (INE, 2,5 % anual) × 1,5 (recuperación post COVID estimada por Savignani) = **×1,697** en el corredor principal. Calles secundarias: solo ×1,131.
- **Av. Río y Residencias (Perrokero):** conteo propio 2026 sin motos (180 y 80 veh/h). Con el factor daban unos 850 veh/h, imposibles para un giro con capacidad de unos 93 veh/h (Perozo, Tabla 4.8).
- **2041:** demanda 2026 × 1,025¹⁵ = **1,448**.
- **FHMD = 0,90** (promedio de las tesis). Simulado: 0,89.
- **Rutas:** muestreo voraz + mínimos cuadrados (equivalente a routeSampler). Orígenes y destinos solo en los extremos de las avenidas y en las puertas de los accesos residenciales.
- **Validación:** **GEH < 5 en 60 de 61 movimientos** (98 %; criterio ≥ 85 %). El único que no cumple es Costanera → FFAA (livianos) en Camino Real, con 5,22.
- **Cómo redactar el aforo ("opción A"):** los volúmenes vienen de las tesis actualizados a 2026; el conteo propio (07/04/2026, 2 a 3 min por intersección) se presenta como **"conteos de verificación de corta duración"** y se usa en las calles secundarias. No decir que se contó varios días ni en horas pico.
- **Conteo frente a modelo:** en los giros de las intersecciones coinciden bastante (0,7 a 1,5 veces). En el tránsito directo de la avenida, el modelo tiene de 2 a 5 veces lo contado, pero **el conteo no cumple la conservación del flujo** (de Camino Real salen 1.020 veh/h hacia Lechería y en Puerto Guaica se contaron 480), mientras que las tesis sí la cumplen. Eso justifica usar los volúmenes de las tesis.

### Red y geometría
- **Carriles (confirmados en campo):** El Ejército con 3 carriles de entrada (10,1 m de la tesis repartidos en 3,37 m); Av. Río y Residencias con 2 por sentido de 3,0 m; FFAA saliendo de Camino Real hacia Perrokero con 3 carriles.
- **Anchos (de las tesis):** Costanera 3,70 m; Costanera en CC Paos **3,75 m** (Tabla 26, aplicado con `ajustes_red/anchos_tesis.edg.xml`); FFAA en Perrokero 3,92 m (Perozo, 7,85 m); giro libre Fabricio Ojeda → Costanera norte en CC Paos de 5,50 m; salida de El Ejército 2 × 3,70 m.
- **Anchos de la tesis que NO se aplicaron en el modelo** (documentado en `anchos_tesis.edg.xml` y en el Cuadro 4.2 con (**)):
  - Camino Real: canal de giro Costanera → El Ejército de 6,30 m (Fig. 84) → se dejó en 3,70 m; y FFAA de 3,75 m → se dejó en 3,20 m. Con los anchos de la tesis, SUMO agranda el polígono del cruce (de 782 a 1.137 m²), alarga los recorridos internos y **baja** la capacidad, al revés del HCM (un carril más ancho tiene más capacidad); la cola llegaba hasta Puerto Guaica (Camino Real pasaba de 43,9 a 53,3 s y Puerto Guaica de 17,0 a 43,2 s).
  - Perrokero: la tesis da 1 carril de 5,0 m; repartirlo en 2 carriles de 2,5 m trancaba el cruce en 1 de cada 3 réplicas → se dejaron 3,0 m.
- **Perrokero:** FFAA y Av. Río a 40 km/h; sin giro a la izquierda desde el carril derecho de FFAA; red regenerada con `--internal-junctions.vehicle-width 3.0` (choques de 237 a unos 0–5). El giro FFAA sur → Av. Río va por el carril previo al cruce (`172682274`); se quitó la conexión `FA_1 → avrio_2`.
- **Semáforos medidos en campo:** Camino Real, ciclo de 82 s (25/25/20 s de verde, 3 s de amarillo y 1 s de todo rojo); CC Paos, ciclo de 66 s (10 + 3, 20 + 3 y 27 + 3 s; Madre Vieja tiene 33 s de verde).
- **Opciones de netconvert** para reconstruir la red: `--offset.disable-normalization true --geometry.min-radius.fix.railways false --geometry.avoid-overlap false --geometry.max-grade.fix false --no-turnarounds true --junctions.corner-detail 5 --junctions.limit-turn-speed 5.5 --internal-junctions.vehicle-width 3.0 --rectangular-lane-cut false --walkingareas false`.

### Vehículos (`costanera.rou.xml`)
- Sin `jmIgnoreFoeProb`. Livianos y carritos con speedFactor de 1,10 (unos 44 km/h en zonas de 40). Pesados con aceleración de 1,0, prefieren el carril derecho. Impaciencia de 0,5.

### Simulación y medición
- 0–900 s de calentamiento, 900–4500 s de hora de análisis y 4500–5400 s de vaciado. `time-to-teleport = -1`; `tripinfo-output.write-unfinished = true`.
- Un detector E3 por intersección (desde unos 300 m antes hasta unos 60 m después) y edgeData por acceso.
- **Nivel de servicio HCM 2000:** con semáforo 10/20/35/55/80 s; sin semáforo 10/15/25/35/50 s, y la intersección toma el nivel del peor acceso secundario. (Ojo: el HCM no define un nivel global para cruces con PARE; se recomienda reportar en la tesis la avenida y cada salida por separado.)
- **Capacidad:** con semáforo, c = 1900·fVP·N·g/C; principal sin semáforo, 1900·fVP·N; secundario, capacidad potencial. Si el acceso está saturado, se usa el flujo medido. En 2041 se usa la capacidad de 2026.
- **5 réplicas** (semillas 1 a 5); cada una en una carpeta temporal.
- **`replicas.py` (desde el 27/10)** agrega a `resumen_replicas.csv`: `cola_promedio_m`, `cola_maxima_m`, `cola_llena_el_tramo`, `velocidad_media_kmh`, `tiempo_viaje_s`, y filas `nivel=RED` ("Red completa", por tipo de vehículo y TOTAL). Todo es el promedio de 5 réplicas.
- **Desde el 02/11** (24 columnas): columna `tiempo_en_paradas_s` (tiempo detenido en paradas de bus; la demora `timeLoss` de SUMO no lo incluye, el tiempo de viaje sí), también en `resumen_viajes.csv`. En las propuestas con puente: cada rampa de bajada es un acceso tipo `puente` de la intersección que cruza (flujo libre en `capacidad.py`), y se agrega la fila `INTERSECCION_A_NIVEL` / `(sin puente)` con la demora ponderada solo de los accesos a nivel. La fila `INTERSECCION` sigue siendo el detector E3 completo (a nivel + puente), que es la que se compara con la base.

### Excel
- 13 hojas (Reporte Viajes, Analisis Por Vehiculo, Analisis HMD, Reporte Colas, Reporte Densidad, Tramos, Tramos Criticos, Intersecciones, Reporte Densidad Interseccion, Analisis Intersecciones, Resumen Intersecciones, Resumen Viajes y **Resumen Replicas**, que es la que va a la tesis). Una macro actualiza todo al abrir.
- La consulta `resumen_replicas` tiene un paso `TiposNuevas` que convierte a número las columnas nuevas si existen (desde el 02/11 incluye `tiempo_en_paradas_s`); `resumen_viajes` tiene el mismo paso para `tiempo_en_paradas_s`. Aplicado en los 8 Excel (respaldo en `_RESPALDOS\antes_paradas_2026-11-02`).
- Las hojas "Reporte…/Analisis…", Resumen Intersecciones y Resumen Viajes son de **una corrida** (la del SUMO-GUI); Resumen Replicas es el promedio de 5.
- Explicación completa hoja por hoja: `EXCEL RESULTADOS\GUIA DEL EXCEL DE RESULTADOS.docx`.
- La parada de bus de Puerto Guaica se redacta como "bloquea el carril derecho cerca del 23 % de la hora pico". En 2041, las demoras de miles de segundos en los accesos secundarios se dejan tal cual.

---

## 5. Resultados finales de la base (5 réplicas; red de main con keepClear y cesión del giro libre en Perrokero, 06/11/2026)

| Intersección | 2026 | 2041 sin proyecto |
|---|---|---|
| Camino Real | **D** · 41,9 s (Costanera D 53,5 s) | **F** · 178,2 s · 68 % atendida |
| CC Paos | **C** · 21,5 s | **F** · 220,4 s · 50 % |
| Perrokero | **F** · 95,8 s (Av. Río F 507 s, descarga 139 de 172 veh/h, campo 180; FFAA norte F 67 s; Residencias D 27 s; FFAA sur A) | **F** · 195,9 s · 71 % |
| Bissau | promedio 4,3 s (D por la salida residencial) | **F** · 177,3 s · 56 % |
| Puerto Guaica | promedio 12,7 s (D) | **F** · 95,3 s · 58 % |
| Red completa | 4.545 viajes; 281 s de viaje; 127 s de demora; **26,0 km/h**; 0 teletransportes | 4.887 viajes; 824 s de demora; **6,6 km/h** |

- **Valores anteriores (keepClear=0, hasta el 06/11):** Camino Real D 43,9 s; Perrokero F 145 s (Av. Río 817 s); red 23,3 km/h; 2041 red 4,1 km/h. Se cambiaron porque Perrokero se bloqueaba en ~30 % de las semillas (ver bitácora del 06/11).
- En 2041 el colapso empieza en Perrokero (FFAA norte) y se propaga a Camino Real, Puerto Guaica, Bissau y CC Paos.
- **Comparación con las tesis:** Perrokero coincide (F). CC Paos coincide (C; 22,6 s frente a 21,1 s). Camino Real: tesis F (129 s) frente a D, explicado por sus errores (GD3 = 603 frente a 190; 35 % de pesados frente a 6 %; ciclo de 111 s imposible). Bissau y Fernández Padilla: el F de Savignani es un error de cálculo (recalculado, unos 28 s, D).
- **Escenario de sensibilidad** (sin el +50 % post COVID, ×1,131): Camino Real C 24,9 s, CC Paos B 16,6 s, Perrokero C 13,7 s, red 37 km/h, Av. Río sale 169 veh/h (campo 180). **El diagnóstico depende del factor post COVID.** Está en `REVISION_SIMULACION_BASE.md` (sección 2b) y en `capitulo4\sensibilidad_sin_postcovid`. **No se agregó al documento del capítulo IV**: el usuario lo consultará con el tutor y medirá las colas en los videos de campo (si hay colas de 150 a 300 m, la base es la más realista; si son de 30 a 80 m, se parece más a ×1,131).

---

## 6. Entregado para la redacción (a la amiga)

1. `TRABAJO DE GRADO\INFORMACION CAPITULO IV - ESCENARIO BASE.docx`: cuadros 4.0 a 4.14 de los objetivos 1 y 2 (geometría con isla y acera, señalización, semáforos, volúmenes y GEH, resultados 2026 y 2041 por intersección y acceso con colas y velocidades, red completa y comparación con las tesis), con notas para la redacción. Se regenera con `03_Documentos\capitulo4\generar_doc.py`.
2. `TRABAJO DE GRADO\BORRADOR 3.7 PROCEDIMIENTO.txt` (5 fases; editado por el usuario).
3. Correcciones pendientes del capítulo III del Word (sección 2 de `REVISION_SIMULACION_BASE.md`):
   - pasar de "no experimental" y "de campo" a experimental y documental;
   - quitar la entrevista informal, los documentos de la Alcaldía y del Ministerio, y COVENIN/AASHTO;
   - corregir la descripción de la muestra (no fue "horas pico de días hábiles");
   - procedimiento como 3.9;
   - en el Cuadro 1.2, cambiar "hombrillos" y "radios de giro" por "isla y acera" y "número de carriles";
   - agregar las referencias: MTC 1997, MINDUR 1981, MVDUCT/INTT 2011, HCM 2000, FHWA Toolbox vol. III y las dos tesis.
4. Apoyo: `INCONGRUENCIAS_TESIS_EVALUADAS.md` y la sección 3 de la revisión.
5. `TRABAJO DE GRADO\SUGERENCIAS CAPITULO II - MARCO TEORICO.docx` (estructura, antecedentes, 8 bloques teóricos incluido el de simulación, bases legales, 46 términos y fuentes). Se regenera con `capitulo4\sugerencias_cap2.py`.
6. **Antecedentes del capítulo II (04/11/2026).** El tutor pide solo los trabajos que de verdad se usaron (3 a 5, sin mínimo de nacionales o internacionales). Quedaron así (verificados en los PDF; el usuario debe leer al menos el resumen, la metodología y las conclusiones de los nuevos):
   1. Estanga y Savignani (2021), USM. Nacional.
   2. Assouad y Peroza (2022), USM. Nacional.
   3. Villalba, C. (2022). *Modelación del tránsito vehicular al tramo Avenida Busch entre segundo y cuarto anillo, Santa Cruz de la Sierra* [Tesis de grado, Universidad Católica Boliviana "San Pablo"]. https://www.tesis.ucb.edu.bo/scz/ucb_civ/2022/villalba_c/ — SUMO (NetEdit + SUMO-GUI), HCM 2010, conteos en 4 nodos, proyección a 2, 5 y 10 años y 3 alternativas; sin intervención las esperas se duplican en 5 años y el sistema colapsa a los 10. Ya se cita en el capítulo I. Se entregó un borrador del antecedente con su "aporte a la investigación".
   4. Molina Toledo, D. A. (2024). *Análisis de niveles de servicio mediante la aplicación del método HCM: Estudio de caso Megamaxi Cuenca*. Universidad de Cuenca (Ecuador). SUMO + HCM 2000, matrices O-D, fases semafóricas. https://dspace-test.ucuenca.edu.ec/bitstream/123456789/45467/4/Trabajo-de-Titulaci%C3%B3n.pdf
   5. Opcional: Gómez Arias, J. A. (2017). *Modelación y calibración de tránsito usando el software PTV VISSIM…* Universidade do Minho / UIS. Respalda la calibración con GEH.
   - La tesis de Valentina Marcano (riego, 2025) **no** sirve como antecedente. Lopez y otros (2018) es un artículo: va en bases teóricas.
- **Falta un documento igual para las propuestas** (objetivos 3 y 4).

---

## 7. Propuesta Savignani (rama `propuestaSavignani`): estado

Lo aplicado en la red (`ajustes_red/propuesta_savignani_fase2.py`; diff respecto a main en `ajustes_red/propuesta_savignani.*`):
- **Distribuidor** Costanera ↔ FFAA: 1 carril de 4 m por sentido; perfil de la tesis (rasante a 7,4 m, rampas de 60 m al 12,3 % y tablero de 30 m). Tramos `puente_subida_hacia_ffaa`, `puente_hacia_ffaa`, `puente_bajada_hacia_ffaa` y sus equivalentes hacia la Costanera.
- **Pesados a nivel:** el puente prohíbe la clase `bus` (coincide con la Alternativa C de la tesis, "canal a nivel para tráfico pesado colectivo").
- **Avenida En Proyección** (`av_proyeccion_entrada/salida`), de 2 carriles por sentido; lleva el **30 % de los viajes de FFAA sur que cruzan Camino Real** (porcentaje indicado por el tutor, 06/11/2026: se declara como criterio de experto; rompe a propósito la regla de "misma demanda"). Demanda: `herramientas/demanda_propuesta.py`, que genera `demanda/demanda_savignani_2026|2041.rou.xml` desde la demanda base.
- **Semáforo de Camino Real:** el del usuario, 4 fases separadas (av. en proyección 30 s, El Ejército 40 s, Costanera 20 s y FFAA 20 s, + 3 s de amarillo; **ciclo de 122 s**). El del Anexo B (3 fases 40/40/80 s con ciclos incoherentes de 88/83/113 s) se descartó porque cruza movimientos; pendiente de consultar con el tutor.
- FFAA a nivel con 3,75 m (Anexo G). CC Paos con 3,75 m (traído de main).
- **Bahías de bus** con parada en las 3: Puerto Guaica (sentido Lechería, `bs_0`) y Bissau (sentido Lechería, `bs_bissau`) de 30 m + cuñas de 20 m; Fernández Padilla (sentido Camino Real, `bs_fpadilla`) de 20 m + cuñas de 15 m. Carril de 2,5 m que solo admite buses y carritos.
- **Carriles de 3 m en Bissau** (sentido Lechería): uno de salida y otro de incorporación, de unos 50 m. **Es el único lugar donde la tesis los propone** (4.4.1, p. 233 impresa: "canales de acceso e incorporación… sentido Sur-Norte (Acceso a Residencia Bissau)"; Fig. 118 Bissau; la Fig. 119 muestra solo bahías en Puerto Guaica y Fernández Padilla). Agregarlos en Puerto Guaica y Fernández Padilla puede ir como **recomendación propia** (objetivo 3 / propuesta final).
- **Isla central NO prolongada:** no hay dónde retornar (Bissau → Camino Real quedaría sin ruta). Pendiente de consultar con el tutor.
- Detectores: `generar_detectores.py` (ahora igual en main y en todas las ramas) tiene `SALIDAS_EXTRA` (salidas del E3 al bajar del puente), `ANTERIOR_FORZADO` y `PUENTES` (filas "Puente hacia FFAA", 272 m, y "Puente hacia Costanera", 300 m).

**Resultados finales de Savignani (02/11, 5 réplicas; en `capitulo4\replicas_savignani\2026|2041`):**

| 2026 | Base | Savignani |
|---|---|---|
| Camino Real completa (a nivel + puente) | D · 43,9 s · V/C 0,95 | **F · 81,7 s** · V/C 1,25 · 94 % atendida |
| Camino Real solo a nivel | — | F · 130,4 s · 89 % |
| Puente hacia FFAA | — | A · 5,0 s · 648 veh/h |
| Puente hacia Costanera | — | **F · 117,6 s** · 434 veh/h |
| FFAA a nivel | D · 53 s · 942 veh/h | F · 259 s · 214 veh/h (1 carril, 20 s de verde) |
| Costanera a nivel | E · 58 s | E · 56 s |
| El Ejército | C · 27,5 s | **F · 137 s** · 87 % atendida |
| Av. En Proyección | — | D · 40 s · 216 veh/h |
| CC Paos | C · 21,1 s | C · 29,0 s (Madre Vieja 67 s: es azar, ver abajo) |
| Perrokero | F · 145 s (Av. Río 817 s) | F · 40 s (Av. Río 109 s; FFAA norte D 31 s) |
| Bissau / Puerto Guaica | 7,3 s / 17,0 s | 4,3 s (C) / 4,9 s (B) |
| Red completa | 4.544 viajes · 160 s demora · 23,3 km/h | 4.418 viajes · 115 s · 26,7 km/h |
| Buses (`carrito`) | 127 s demora · 28,4 km/h | **367 s** demora (+28 s en paradas, aparte) · 15,8 km/h |
| Pesados | 132 s | 225 s |

- **2041:** la red colapsa igual que la base (4,1 km/h en ambos; demora 1.217 frente a 1.280 s). Camino Real F 110 s con 42 % atendida (base 190 s y 51 %); el distribuidor no resuelve el horizonte 2041.
- **Cuello de botella en El Ejército / salida a la Costanera:** la salida a nivel hacia la Costanera es de 1 carril y recibe El Ejército + la bajada del puente (~900 veh/h). Por eso el puente hacia FFAA va en A pero el puente hacia la Costanera queda en F. Registrado como **S26** (Anexo B de la tesis: El Ejército → Costanera 685 veh/h en 1 carril, Xc 1,04, 61,4 s (E), pero la intersección se presenta como C). **Idea para la tesis:** quizá el distribuidor no es la mejor propuesta, porque traslada el cuello de botella a la salida hacia la Costanera.
- **Buses:** el atraso es real, no efecto de las paradas: el puente prohíbe buses, así que cruzan por FFAA a nivel, que queda saturado (FFAA → Lechería: 873–916 s frente a 210–237 s en la base).
- **Madre Vieja (CC Paos):** con 5 semillas parecía empeorar (67 frente a 33 s), pero con 10 semillas da base 39,8 s y Savignani 33,3 s → variabilidad aleatoria (carril compartido con giro a la izquierda permisivo), no efecto de la propuesta.
- **Bissau y Puerto Guaica sentido Lechería** salen con V/C 1,15 y nivel A a la vez: no están saturados, sino que llega menos tráfico porque se queda atrapado en Camino Real (la "capacidad medida" es lo que llega). Explicarlo así en la tesis.

**Pendientes de Savignani:**
1. Correr sus `.bat` (2026 y luego 2041) para refrescar `PROPUESTA_SAVIGNANI\2026|2041` (sus Excel tienen datos del 23/10). Los resultados deben parecerse a los de la tabla.
2. Consultar con el tutor: semáforo de 122 s frente al del Anexo B, isla central y los carriles de incorporación de Puerto Guaica y Fernández Padilla como recomendación.

---

## 7b. Propuesta Perozo (rama `propuestaPerozo`): estado al 04/11/2026

Lo aplicado en la red con `ajustes_red/propuesta_perozo.py` (se corre sobre la red plana de main; diff en `ajustes_red/propuesta_perozo.*`):
- **Puente sobre FFAA** (cap. V, 5.6 y figuras, imp. 168–170): rampa de 40 m al 15 % + tablero de 20 m a 6,00 m + rampa de 40 m (100 m en total), centrado en el cruce; 1 carril de 3,70 m por sentido; 40 km/h. Tramos `puente_subida_hacia_sur`, `puente_hacia_sur`, `puente_bajada_hacia_sur` y los equivalentes `..._hacia_norte`.
- **Solo livianos** en el puente (`allow` passenger); pesados y carritos (clase bus) a nivel, igual que en Savignani.
- **A nivel queda 1 carril por sentido en FFAA** (el derecho), como en la figura de la tesis: el carril izquierdo de campo es el que sube al puente (la sección sigue con 2 carriles por sentido). Por eso los giros a la izquierda salen del carril derecho. El cálculo HCM de la tesis supone 2 carriles a nivel (incongruencia **P10**).
- Los carriles se separan 8 m antes del pie de la rampa (58 m del centro) para que netconvert no corte la rampa. En el sentido sur → norte, el carril izquierdo se separa en el nodo `11353318191` (~75 m), antes de la bifurcación hacia la Av. Río, y sigue a nivel hasta los 50 m.
- **Semáforo de 120 s** bajo el puente, una fase por acceso: Norte 33, Oeste (Residencias) 20, Sur 25 y Este (Av. Río) 30 s + 3 s de amarillo, sin todo rojo (tal cual la tesis).
- Tramos nuevos a nivel: `FA_3_antes`, `FA_3` (1 carril), `fuerzas_armadas_entrada_nivel`, `FA_2` (1 carril), `FA_2_despues`; `bifurcacion_FA_perrokero` y `FA_1` con 1 carril. El giro libre FFAA sur → Av. Río (`172682274`) se mantiene.
- Demanda: `herramientas/demanda_propuesta.py` → `demanda/demanda_perozo_2026|2041.rou.xml` (misma demanda de la base; los livianos que siguen derecho por FFAA van por el puente: 753 y 726 veh/h en 2026). Las `.sumocfg` de la rama apuntan a esos archivos.
- `resumen_resultados.py` de la rama: Perrokero pasa a `semaforizada` (umbrales HCM con semáforo) y la referencia de la tesis es la Alternativa C (E, 65,6 s). `generar_detectores.py`: filas `puente` "Puente hacia el sur (FFAA)" y "Puente hacia Camino Real" (también sirven en main, están protegidas con `hasEdge`).

**Resultados (5 réplicas; `capitulo4\replicas_perozo\2026|2041`; 0 teletransportes):**

| 2026 | Base | Perozo |
|---|---|---|
| Perrokero completa (a nivel + puente) | F · 145,2 s · V/C 1,42 | **E · 62,3 s** · V/C 1,08 · 98 % atendida |
| Perrokero solo a nivel | — | E · 67,2 s (tesis, 2041: E · 65,6 s) |
| FFAA norte (desde Camino Real) a nivel | F · 116,5 s · 1.128 veh/h | **F · 93,1 s** · 372 veh/h · cola 76 m (máx. 258 m) |
| FFAA sur a nivel | A · 4,7 s | D · 43,9 s · 133 veh/h |
| Av. Río | F · 817 s · 70 % atendida | **D · 37,9 s** · 97 % |
| Residencias | F · 51,4 s | D · 42,4 s |
| Puente hacia el sur | — | D · 43,6 s · 767 veh/h |
| Puente hacia Camino Real | — | A · 3,4 s · 761 veh/h |
| Camino Real / CC Paos | D 43,9 s / C 21,1 s | D 40,7 s / C 21,6 s |
| Red completa | 4.544 viajes · 160 s demora · 313 s viaje · 23,3 km/h | 4.547 viajes · **117 s** · 271 s · **27,0 km/h** |

- **Hallazgo:** el puente hacia el sur tiene 43,6 s de demora aunque el tablero va libre: la cola del acceso norte a nivel (1 carril, 33 s de verde, con el giro a la izquierda GI4 hacia la Av. Río) pasa de los 50 m de separación y **bloquea la entrada al puente**. Es una recomendación natural para el objetivo 3 (alargar la separación de carriles o dar más verde al acceso norte). Hacia Camino Real no pasa, porque el acceso sur tiene poco giro.
- **2041:** Perrokero E · 77,0 s (71 % atendida; a nivel 72,8 s), pero la red sigue colapsada (7,1 km/h frente a 4,1 de la base; demora 754 frente a 1.280 s); el colapso pasa a Camino Real (FFAA a nivel 227 s), CC Paos y Bissau.

- **Polígono del puente en el GUI:** `distribuidor.add.xml` (mismo id, color gris 131,139,139 y capa 5 que el de Savignani), generado con `ajustes_red/poligono_puente_perozo.py` sobre los dos carriles del puente (100 m × 8,67 m); cargado en las dos `.sumocfg`. No cambia la simulación.
- **Excel (04/11):** los de Perozo se rehicieron como copia de los de Savignani con `copiar_excel.py` (misma estructura) y se refrescaron con los CSV de Perozo; los anteriores están en `_RESPALDOS\PROPUESTA_PEROZO_antes_igualar_2026-11-04`.
- **Mapeo de intersecciones (hoja "Intersecciones", tabla `MAPEO_INTERSECCIONES`), 04/11:** en los 4 Excel de propuestas (Savignani y Perozo, 2026 y 2041) se agregaron las mismas 6 filas: `puente_subida_hacia_sur` y `puente_subida_hacia_norte` (Perrokero), `puente_subida_hacia_ffaa`, `puente_subida_hacia_costanera`, `ffaa_hacia_semaforo` y `av_proyeccion_salida` (Camino Real). Así "Analisis Intersecciones" y "Reporte Densidad Interseccion" cuentan también el puente (Perrokero Perozo 2026: de 778 a 2.356 veh/h; Camino Real Savignani 2026: de 1.106 a 2.546 veh/h). `ffaa_hacia_semaforo` reemplaza en Savignani a `semaforo_caminoreal_FA`, que mide 18 m y la consulta descarta (< 20 m). Respaldo en `_RESPALDOS\antes_mapeo_puentes_2026-11-04`.
- **Red propia de cada Excel (04/11):** la consulta "costanera net" leía `01_Red_Y_Demanda\costanera.net.xml`, o sea, la red de la rama activa, y la macro refresca al abrir. Ahora los 8 Excel (base, 2041, Savignani, Perozo y Final) leen `costanera.net.xml` **de su propia carpeta** (`herramientas/red_excel.py`; respaldo en `_RESPALDOS\antes_red_propia_2026-11-04`). Se copiaron: red de main en BASE_2026 y FUTURO_2041, la de cada rama en su propuesta (Final = main por ahora). Los `.bat` de Perozo copian la red en cada corrida (`copy /Y "%RED_DIR%\costanera.net.xml" "%CSV_DIR%\costanera.net.xml"`). **Falta agregar esa misma línea a los `.bat` de main, Savignani y Final** cuando se trabaje en cada rama (mientras tanto sus Excel usan la copia de hoy, que está bien mientras no cambie su red).

- **Cambios del 06/11/2026 (rama Perozo):** (1) `carFollowModel="KraussPS"` en los tres tipos de vehículo (la pendiente reduce la aceleración en subida); en la red plana da resultados idénticos a Krauss (verificado con la base, semilla 1), así que solo afecta los puentes. Los livianos (aceleración 2,6 m/s²) mantienen unos 40 km/h en el 15 % porque la gravedad les resta 1,46 m/s²: el efecto se nota al arrancar en cola sobre la rampa, no a velocidad constante. (2) Carritos con clase `taxi` (taxis y por puestos; Perozo solo prohíbe pesados): el flujo `ffaa_lech_C` tiene ruta fija por el puente. Réplicas rehechas: 2026 Perrokero E 61,1 s, red 112 s y 27,4 km/h; carritos de 161 a 137 s de demora; 2041 Perrokero F 87,5 s (antes E 77 s: está en el límite y dentro de la variabilidad), red 7,0 km/h. **Falta aplicar KraussPS a Savignani** (su puente tiene pendiente; ahí los carritos siguen a nivel porque su tesis habla de "tráfico pesado colectivo"). **Ojo al llevar `costanera.rou.xml` a main o a Savignani:** la clase `taxi` de los carritos es solo de Perozo (las bahías de Savignani admiten solo `bus`).
- **30 % de la Av. En Proyección:** lo indicó el tutor; se declara como criterio de experto (06/11).

**Pendientes de Perozo:**
1. Revisar en el SUMO-GUI la geometría del puente y la cola del acceso norte (los `.bat` ya se corrieron el 04/11).
2. Commit y push de la rama (el merge de main del 04/11, `859d9fe`, también es local).
3. Llevar a main el resumen, `INCONGRUENCIAS_TESIS_EVALUADAS.md` (P9–P19) y `generar_detectores.py`.

---

## 8. Próximos pasos

*(Actualizado el 04/11/2026.)*
1. **Commit y push de `propuestaPerozo`** (todo lo del 04/11 está sin commit, salvo el merge `859d9fe`). Después, llevar a main el resumen, `INCONGRUENCIAS_TESIS_EVALUADAS.md` (P9–P19), `generar_detectores.py` y `herramientas/red_excel.py`, y agregar la línea `copy /Y` de la red a los `.bat` de main, Savignani y Final.
2. **Revisar Perozo en el SUMO-GUI** (geometría del puente y cola del acceso norte que bloquea la entrada al puente hacia el sur).
3. **Consultas al tutor:** Savignani (semáforo de 122 s, isla central, carriles de incorporación), Perozo (1 carril a nivel según la figura frente a los 2 del cálculo HCM, P10) y el factor post COVID (escenario de sensibilidad).
4. **Objetivo 3, recomendaciones:** comparar base, Savignani y Perozo (2026 y 2041) y decidir la propuesta final. Hallazgos ya disponibles: el distribuidor de Savignani lleva el cuello de botella a la salida de 1 carril hacia la Costanera (S26); en Perozo la cola a nivel del acceso norte tapa la entrada al puente; ninguna resuelve 2041.
5. **Propuesta final** en `propuestaFinal`, con las recomendaciones del usuario. Su Excel se hace copiando el de Savignani (`copiar_excel.py` + `red_excel.py`).
6. **Documento para la amiga de los objetivos 3 y 4** (como el del capítulo IV de la base), con las tablas de las secciones 7 y 7b.
7. **Objetivo 4, costos:** cómputos métricos y APU con precios de 2026 (las dos tesis copian costos de trabajos extranjeros, S21 y P6).

---

## 9. Reglas de trabajo importantes

- **Responder siempre en español.**
- Los datos geométricos salen solo de las tesis; no agregar indicadores que no tienen. No cambiar el número de carriles. Si un cambio puede alterar los resultados, decir cuánto.
- Ir registrando cada incongruencia nueva de las tesis en `03_Documentos/INCONGRUENCIAS_TESIS_EVALUADAS.md` (con página impresa/PDF y efecto).
- Si se cambia la red: correr `python herramientas\generar_detectores.py` (y `generar_demanda.py` en main, o `demanda_propuesta.py` en Savignani). Si un movimiento contado cambia de camino, ajustar su fila en `conteos_movimientos.csv`.
- Para cada propuesta: carpetas `EXCEL RESULTADOS\PROPUESTA_X\2026|2041`; el Excel se copia con `herramientas\copiar_excel.py` (cambia las rutas de Power Query); el `.bat` 2041 toma la capacidad del `resumen_replicas.csv` 2026 de la misma propuesta.
- Los `.bat` deben tener CRLF.
- Antes de modificar un Excel por script, debe estar cerrado. Siempre hacer respaldo en `_RESPALDOS`.
- `netdiff.py` deja archivos planos (`costanera.con.xml`, etc.) junto a la red de entrada: borrarlos si aparecen en `01_Red_Y_Demanda`.
- No correr simulaciones en `02_Resultados_*` con SUMO-GUI abierto.
- Revisar siempre el realismo (choques, colas, bloqueos, volúmenes por calle). El usuario valora el realismo por encima de cuadrar cifras. Desconfiar de cambios de geometría que alteran el dibujo de los cruces en SUMO (probar con varias semillas).
- Si un acceso cambia mucho entre escenarios sin una causa clara, correr 10 semillas antes de concluir (caso Madre Vieja).

---

## 10. Bitácora del 02/11/2026

1. **Revisión de lo que faltaba en Savignani** (rama `propuestaSavignani`): diagnóstico con 5 réplicas 2026 (Camino Real F, El Ejército F, FFAA a nivel F, buses muy demorados).
2. **Incongruencia S26** agregada (salida a la Costanera de 1 carril; Anexo B con Xc 1,04).
3. **Carriles de incorporación:** confirmado en la tesis que solo los propone en Bissau; los de Puerto Guaica y Fernández Padilla quedan como posible recomendación propia.
4. **Madre Vieja:** probado con 10 semillas; es azar.
5. **Reporte para comparar con la base** (commit `744747c` en main, fusionado en las 3 ramas): accesos tipo `puente`, fila `INTERSECCION_A_NIVEL`, columna `tiempo_en_paradas_s` en `resumen_viajes.csv` y `resumen_replicas.csv` (`resumen_resultados.py`, `replicas.py`, `capacidad.py`, `generar_detectores.py`). En la base no cambia nada (verificado).
6. **Los 8 Excel** (base, 2041, Savignani, Perozo y Final) actualizados para tipar la columna nueva; se probó el refresco de una copia sin errores.
7. **Réplicas finales de Savignani 2026 y 2041** con el reporte nuevo (sección 7), guardadas en `capitulo4\replicas_savignani`.
8. Este resumen e `INCONGRUENCIAS_TESIS_EVALUADAS.md` (con S26) llevados también a main.

---

## 11. Bitácora del 06/11/2026

1. **Revisión exhaustiva** (`REVISION_EXHAUSTIVA_2026-11-06.md`). Puntos críticos: la demanda de Perrokero es de 3 a 10 veces el conteo de campo; el +50 % post COVID es un supuesto propio (Savignani solo lo usa para su propuesta, imp. 233); el GEH es verificación de la carga, no validación; con 5 réplicas, "Perozo mejora la red en 2026" no es significativo.
2. **Decisiones del usuario:** recontar Perrokero (5 minutos en la hora pico durante 3 días), filmar la cola de la FFAA y recorrer el eje para medir la velocidad; quedarse con 5 réplicas y reportar el intervalo de confianza; el 30 % de la Av. En Proyección lo indicó el tutor (no hay sensibilidad con 0 %); en 2041 se reportan los mismos indicadores que en 2026, más la demanda atendida.
3. **Pendiente de las rampas:** `carFollowModel="KraussPS"` en `propuestaPerozo` (`c66a9a4`) y en `propuestaSavignani` (`7c59139`). En la red plana da lo mismo que Krauss (verificado), así que la base no se volvió a correr y `main` sigue con Krauss.
4. **Carritos en el puente de Perozo** (clase `taxi`, solo en esa rama).
5. **Réplicas rehechas:**
   - Perozo 2026: Perrokero E 61,1 s; red 112 s y 27,4 km/h.
   - Perozo 2041: Perrokero F 87,5 s, en el límite de 80 s.
   - Savignani 2026: Camino Real F 84,2 s; red 118 s y 26,4 km/h.
   - Savignani 2041: red 4,2 km/h.
   - Las conclusiones no cambian.
6. **Consolidado en main:** documentos, `comparar_propuestas.py`, las réplicas de las tres simulaciones, `generar_detectores.py` y `red_excel.py`. Se regeneró el Word `COMPARACION DE ESCENARIOS - BASE, SAVIGNANI Y PEROZO.docx`. Los `.bat` de la base copian la red a su carpeta de Excel.
7. **Carritos como taxi en las tres ramas** (decisión del usuario: se detienen en las paradas y, como no son pesados, usan los puentes). En main no cambia nada (verificado). En Savignani: bahías con `allow="bus taxi"`, ruta fija del carrito FFAA → Lechería por el distribuidor y **corrección de permisos**: antes solo `puente_subida_hacia_ffaa` prohibía `bus`; ningún pesado usó el puente (verificado) y ahora los 6 tramos lo prohíben (`ajustes_red/propuesta_savignani_permisos.edg.xml`). Réplicas nuevas de Savignani 2026: carritos de 391 a 49 s de demora; Camino Real E 76,6 s (en el límite de 80 s; la base está en D 43,9 s); red 106 s y 27,8 km/h. En 2041 no cambia.
8. Se fusionó main en `propuestaSavignani` (`8581717`). Main tiene las réplicas definitivas de las tres simulaciones y el Word de comparación regenerado, con los textos sobre transporte público corregidos.
9. **Bloqueo de Perrokero:** una corrida del `.bat` dio FHMD 0,58 porque Perrokero quedó bloqueado desde los 30 minutos. Con 10 semillas, 3 se bloqueaban. La causa era `keepClear="0"` en sus 15 conexiones (desde los primeros commits): los que giraban hacia la Av. Río (salida `avrio_2` de 7,5 m que se une al canal de giro libre) quedaban dentro del cruce y lo bloqueaban en círculo. Se aplicó `keepClear="1"` ("no bloquear el cruce", `ajustes_red/keepclear_perrokero.con.xml`) y, como solo con eso la salida `avrio_2` de 7,5 m frenaba el cruce, también la **cesión de paso del canal de giro libre** `172682274` al incorporarse a la Av. Río (`ajustes_red/cesion_giro_libre_perrokero.edg.xml`, priority=1). Resultado: 0 bloqueos y 0 choques en 10 semillas (6 a 15), sin teletransportes. Base rehecha (tabla de la sección 5). Se regeneró `INFORMACION CAPITULO IV - ESCENARIO BASE.docx`. **Falta:** aplicarlo en Savignani y en Perozo (en Perozo también en `propuesta_perozo.py`, que ponía `keepClear='0'`), volver a correr sus réplicas, regenerar el Word de comparación y rehacer el escenario de sensibilidad (×1,131), que se corrió con la red anterior.
10. **Falta:** la línea `copy /Y` de la red en los `.bat` de Final (Savignani ya la tiene por la fusión); correr los `.bat` de Savignani y Perozo para refrescar sus Excel con KraussPS; fusionar main en las tres ramas (en Perozo, conservar su `resumen_resultados.py` y su `costanera.rou.xml`).
