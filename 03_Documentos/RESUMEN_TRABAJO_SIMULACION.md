# Resumen del trabajo de simulación — Tesis Samuel Mujica (USM, Ing. Civil)

**Actualizado:** 29/10/2026 · **Uso:** compartir este archivo al iniciar un chat nuevo para retomar el trabajo.
**Estado general:** la **simulación base (2026 y 2041) está terminada y revisada**, y la información de los objetivos 1 y 2 ya está lista para la redacción. Lo siguiente son las **propuestas**: terminar Savignani, luego Perozo y luego la propuesta final.

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
    ├── INCONGRUENCIAS_TESIS_EVALUADAS.md   errores de las tesis (S1–S25 Savignani, P1–P8 Perozo), base del objetivo 3
    ├── REVISION_SIMULACION_BASE.md      revisión completa de la base y escenario de sensibilidad
    ├── capitulo4\                       generar_doc.py (documento del cap. IV), guia_excel.py (guía del Excel),
    │                                    replicas_anchos_tesis\2026|2041 (resultados finales), sensibilidad_sin_postcovid\
    └── FLUJO VEHICULAR.xlsx (aforo propio), PDF de validación

Desktop\EXCEL RESULTADOS\
├── BASE_2026\  RESULTADOS SIMULACION.xlsm        FUTURO_2041\  RESULTADOS SIMULACION 2041.xlsm
├── PROPUESTA_SAVIGNANI\2026|2041\  RESULTADOS SAVIGNANI 2026|2041.xlsm
├── PROPUESTA_PEROZO\2026|2041\     RESULTADOS PEROZO 2026|2041.xlsm   (copias del base, 29/10)
├── PROPUESTA_FINAL\2026|2041\      RESULTADOS FINAL 2026|2041.xlsm    (copias del base, 29/10)
├── GUIA DEL EXCEL DE RESULTADOS.docx    explicación hoja por hoja (para el tutor)
└── _RESPALDOS\                     versiones viejas de cada carpeta y Excel
```

**Git (29/10/2026):**
| Rama | Contenido |
|---|---|
| `main` (`6c9a669`) | Simulación base final |
| `propuestaPerozo` (`bd71357`) | Igual a main + sus `.bat` (escriben en `PROPUESTA_PEROZO\2026` y `\2041`). Red todavía sin la propuesta. |
| `propuestaFinal` (`c4b4e5b`) | Igual a main + sus `.bat` (`PROPUESTA_FINAL\2026` y `\2041`). Red todavía sin la propuesta. |
| `propuestaSavignani` (`6f349d3`) | Main fusionado el 29/10 + la propuesta (ver sección 7) |
| `respaldo/propuesta*-2026-10-23` | Versiones viejas, también en GitHub |

- Falta **push normal** (sin force) de `main`, `propuestaPerozo` y `propuestaFinal`.
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

### Excel
- 13 hojas (Reporte Viajes, Analisis Por Vehiculo, Analisis HMD, Reporte Colas, Reporte Densidad, Tramos, Tramos Criticos, Intersecciones, Reporte Densidad Interseccion, Analisis Intersecciones, Resumen Intersecciones, Resumen Viajes y **Resumen Replicas**, que es la que va a la tesis). Una macro actualiza todo al abrir.
- La consulta `resumen_replicas` tiene un paso `TiposNuevas` que convierte a número las columnas nuevas si existen.
- Las hojas "Reporte…/Analisis…", Resumen Intersecciones y Resumen Viajes son de **una corrida** (la del SUMO-GUI); Resumen Replicas es el promedio de 5.
- Explicación completa hoja por hoja: `EXCEL RESULTADOS\GUIA DEL EXCEL DE RESULTADOS.docx`.
- La parada de bus de Puerto Guaica se redacta como "bloquea el carril derecho cerca del 23 % de la hora pico". En 2041, las demoras de miles de segundos en los accesos secundarios se dejan tal cual.

---

## 5. Resultados finales de la base (5 réplicas; red de main)

| Intersección | 2026 | 2041 sin proyecto |
|---|---|---|
| Camino Real | **D** · 43,9 s · V/C 0,95 (FFAA D 53 s; Costanera E 58 s; El Ejército C 27,5 s) | **F** · 190,1 s · 51 % atendida |
| CC Paos | **C** · 21,1 s · V/C 0,73 | **F** · 143,7 s · 37 % |
| Perrokero | **F** · 145,2 s · V/C 1,42 (Av. Río 817 s y 70 % atendida; FFAA norte F 116 s; FFAA sur A) | **F** · 241,3 s · 43 % |
| Bissau | promedio 7,3 s; avenida A; salida residencial F (66 s, 23 veh/h) | **F** · 152,8 s · 47 % |
| Puerto Guaica | promedio 17,0 s (D por la salida residencial); avenida A–C | **F** · 88,5 s · 47 % |
| Red completa | 4.544 viajes; 313 s de viaje; 160 s de demora; **23,3 km/h**; 0 teletransportes | 4.000 viajes; 1.399 s; **4,1 km/h** |

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
- **Falta un documento igual para las propuestas** (objetivos 3 y 4).

---

## 7. Propuesta Savignani (rama `propuestaSavignani`): estado

Lo aplicado en la red (`ajustes_red/propuesta_savignani_fase2.py`; diff respecto a main en `ajustes_red/propuesta_savignani.*`):
- **Distribuidor** Costanera ↔ FFAA: 1 carril de 4 m por sentido; perfil de la tesis (rasante a 7,4 m, rampas de 60 m al 12,3 % y tablero de 30 m). Tramos `puente_subida_hacia_ffaa`, `puente_hacia_ffaa`, `puente_bajada_hacia_ffaa` y sus equivalentes hacia la Costanera.
- **Pesados a nivel:** el puente prohíbe la clase `bus` (coincide con la Alternativa C de la tesis, "canal a nivel para tráfico pesado colectivo").
- **Avenida En Proyección** (`av_proyeccion_entrada/salida`), de 2 carriles por sentido; lleva el **30 % de los viajes de FFAA sur que cruzan Camino Real** (supuesto del usuario, a declarar; rompe a propósito la regla de "misma demanda"). Demanda: `herramientas/demanda_propuesta.py`, que genera `demanda/demanda_savignani_2026|2041.rou.xml` desde la demanda base.
- **Semáforo de Camino Real:** el del usuario, 4 fases separadas (av. en proyección 30 s, El Ejército 40 s, Costanera 20 s y FFAA 20 s, + 3 s de amarillo; **ciclo de 122 s**). El del Anexo B (3 fases 40/40/80 s con ciclos incoherentes de 88/83/113 s) se descartó porque cruza movimientos; pendiente de consultar con el tutor.
- FFAA a nivel con 3,75 m (Anexo G). CC Paos con 3,75 m (traído de main).
- **Bahías de bus** con parada en las 3: Puerto Guaica (sentido Lechería, `bs_0`) y Bissau (sentido Lechería, `bs_bissau`) de 30 m + cuñas de 20 m; Fernández Padilla (sentido Camino Real, `bs_fpadilla`) de 20 m + cuñas de 15 m. Carril de 2,5 m que solo admite buses y carritos.
- **Carriles de 3 m en Bissau** (sentido Lechería): uno de salida y otro de incorporación, de unos 50 m.
- **Isla central NO prolongada:** no hay dónde retornar (Bissau → Camino Real quedaría sin ruta). Pendiente de consultar con el tutor.
- Detectores: `generar_detectores.py` de esta rama tiene `SALIDAS_EXTRA` (salidas del detector al bajar del puente) y `ANTERIOR_FORZADO`.
- **Resultado de prueba 2026** (5 réplicas, semáforo de 122 s): Camino Real F con unos 83 s (El Ejército F 137 s; FFAA a nivel F 269 s); Bissau y Puerto Guaica en A en la Costanera. La red tiene congestión de inserción en El Ejército.
- **Pendientes de Savignani:**
  1. Quedó sin respuesta qué carriles de incorporación faltan: los de Bissau ya están; preguntar si también quiere los de Puerto Guaica y Fernández Padilla, o si los de Bissau no se ven bien en el GUI.
  2. Correr sus `.bat` (2026 y luego 2041) para actualizar `PROPUESTA_SAVIGNANI\2026|2041`: sus datos son de antes del 29/10.
  3. Consultar con el tutor el semáforo de 122 s, la isla central y el 30 % de la avenida en proyección.

---

## 8. Próximos pasos

1. Push normal de `main`, `propuestaPerozo` y `propuestaFinal`.
2. Terminar Savignani (pendientes de la sección 7) y correr sus `.bat`.
3. **Perozo:** su rama ya tiene sus `.bat` y Excel, pero la red no tiene la propuesta. El puente de Perrokero va desde cero (la rama vieja no tenía geometría). Revisar a fondo la tesis de Perozo (planos, perfil y semáforo de 120 s) y agregar sus incongruencias al archivo.
4. **Propuesta final:** con las recomendaciones del usuario.
5. Documento para la amiga de los objetivos 3 y 4 (igual al del capítulo IV de la base), y costos (objetivo 4: cómputos métricos y APU con precios de 2026).

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
