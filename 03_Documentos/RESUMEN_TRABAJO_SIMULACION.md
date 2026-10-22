# Resumen del trabajo de simulación — Tesis Samuel Mujica (USM, Ing. Civil)

**Actualizado:** 22/10/2026 · **Uso:** compartir este archivo al iniciar un chat nuevo para retomar el trabajo.

---

## 1. La tesis

- **Título:** Evaluación de la factibilidad técnica de propuestas para mejorar la circulación vehicular en el eje comprendido desde el cruce de las Avenidas Fabricio Ojeda y La Costanera y el cruce con las Avenidas Fuerzas Armadas y Río. Barcelona, Anzoátegui, 2026.
- **Tutor:** Ing. Wolfgang Bandres. **Documento:** `Desktop\TRABAJO DE GRADO\TESIS SAMUEL MUJICA OCTUBRE.docx`.
- **Objetivos específicos:**
  1. Parámetros de diseño vial.
  2. Capacidad y nivel de servicio actual y futuro con SUMO.
  3. Recomendaciones a las propuestas originales.
  4. Costos.
- **Propuestas evaluadas** (PDF en `Desktop\TRABAJO DE GRADO\`):
  - **Assouad y Peroza (2022)**, en Perrokero (Av. Fuerzas Armadas × Av. Río): puente elevado de 100 m sobre FFAA, 1 carril por sentido de 3,70 m, gálibo de 6 m, rampas al 15 %, solo livianos (los pesados a nivel); debajo, semáforo de 120 s (verdes N 33 / S 25 / E 30 / O 20 s). Costo: $3.605.643,54.
  - **Estanga y Savignani (2021)**, en Camino Real (Costanera × Prolongación El Ejército/FFAA, su "intersección 1"): distribuidor tipo puente de 30 m, 1 carril por sentido de 4 m, rampas de 60 m al 12,3 %. Además: carriles de incorporación y bahías de bus en Bissau, Puerto Guaica y Fernández Padilla; eliminar el giro a la izquierda en Fernández Padilla; ajustar el semáforo en CC Paos (su "intersección 2"). Costo: $3.487.520,41.
- **Plan de simulaciones (definido por el usuario):** base actual → propuesta Savignani → propuesta Perozo → propuesta final con las recomendaciones del usuario. Cada una con horizonte actual (2026) y futuro (2041).
- **Las motos se excluyen** del estudio por indicación del tutor (solo livianos, pesados y carritos/por puestos). No volver a proponerlas.

---

## 2. Organización de carpetas (reorganizada el 22/10/2026)

```
Desktop\SUMO\                            repositorio git (GitKraken). Ramas: main, propuestaSavignani, propuestaPerozo, propuestaFinal
├── 01_Red_Y_Demanda\
│   ├── SIMULACION.bat                   base 2026: abre SUMO, convierte a CSV, resume y corre 5 réplicas
│   ├── SIMULACION_2041.bat              horizonte 2041: igual, con sus propias carpetas
│   ├── tesis_base.sumocfg / escenario_2041.sumocfg
│   ├── costanera.net.xml                red (ya ajustada)
│   ├── costanera.rou.xml                tipos de vehículo y transporte público con paradas
│   ├── paradas.add.xml, medidores(_2041).add.xml, detectores_intersecciones(_2041).add.xml, vista.xml, mapa_fondo.poly.xml
│   ├── accesos_intersecciones.csv       tramos de cada acceso (lo generan los scripts)
│   ├── demanda\                         conteos_movimientos.csv, demanda_base.rou.xml, demanda_2041.rou.xml, ajuste_demanda_base.csv
│   ├── herramientas\                    generar_demanda.py, generar_detectores.py, resumen_resultados.py, replicas.py, capacidad.py
│   ├── ajustes_red\                     cambios aplicados a la red con netconvert (documentación)
│   └── fuentes\                         red_vial.osm, polygonTypes.txt
├── 02_Resultados_Base\  02_Resultados_2041\   XML de SUMO (ignorados por git; se regeneran)
└── 03_Documentos\                       FLUJO VEHICULAR.xlsx (aforo propio), PDF de validación, este resumen

Desktop\EXCEL RESULTADOS\
├── BASE_2026\    RESULTADOS SIMULACION.xlsm + CSV
├── FUTURO_2041\  RESULTADOS SIMULACION 2041.xlsm + CSV
├── PROPUESTA_SAVIGNANI\ PROPUESTA_PEROZO\ PROPUESTA_FINAL\   (estructura vieja, por actualizar)
└── _RESPALDOS\   el respaldo más reciente de cada Excel
```

**Pendiente:** la reorganización y los últimos ajustes están en `main`, **pendientes de commit** (el usuario hace sus commits en GitKraken).

---

## 3. Simulación base 2026: decisiones tomadas

### Demanda (hora pico 2026)
- **Fuente:** volúmenes por movimiento del capítulo 4 de ambas tesis (Savignani, tablas 37 y 38 y cuadros 21 y 23; Perozo, tabla 4.3), cargados en `demanda\conteos_movimientos.csv` (filas `tesis2021`).
- **Actualización:** V₂₀₂₆ = V₂₀₂₁ × 1,025⁵ (INE, 2,5 % anual, la misma tasa de Perozo) × 1,5 (recuperación post-COVID, estimación de Savignani) = **×1,697** en el corredor principal.
- **Calles secundarias** (salidas de Bissau, Puerto Guaica y Fernández Padilla): solo ×1,131 (INE).
- **Av. Río y Residencias en Perrokero:** se usa el **aforo propio 2026** sin motos (180 y 80 veh/h). Con el factor daba unos 850 veh/h, físicamente imposibles: Perozo calcula una capacidad de unos 93 veh/h para el giro (tabla 4.8), y quedaba una cola irreal de 300 vehículos.
- **Pico de 15 minutos:** FHMD = 0,90 (promedio de las tesis).
- **Rutas:** se generan con un muestreo voraz más mínimos cuadrados ponderados (equivalente a routeSampler, sin numpy). Orígenes y destinos solo en los extremos de las avenidas y en las puertas de los accesos residenciales; **no se usan calles laterales como comodín** (por ejemplo, la 1106623985 junto al CIVO).
- **Ajuste:** 60 de 61 movimientos con GEH < 5.
- El giro FFAA sur → Av. Río va por el carril de giro previo al cruce (`172682274`). El usuario quitó la conexión `FA_1` → `avrio_2`.

### Cómo redactar el aforo en la tesis ("opción A")
- Los volúmenes vienen de las tesis, actualizados a 2026.
- El aforo propio (07/04/2026, en las 5 intersecciones) se presenta como **"conteos de verificación de corta duración"**, usados en las calles secundarias.
- No decir que se contó varios días ni en horas pico.

### Red y geometría (verificadas contra las tesis y fotos del usuario)
- **Perrokero:** FFAA y Av. Río a 40 km/h (antes estaban a 19,8). Sin giro a la izquierda desde el carril derecho de FFAA. Red regenerada con `--internal-junctions.vehicle-width 3.0` (los choques bajaron de 237 a unos 5 por hora).
- **El Ejército en Camino Real:** 3 carriles (1 hacia FFAA y 2 hacia Lechería, confirmado por el usuario), de **3,37 m** (calzada de 10,1 m según Savignani).
- **Av. Río:** 2 carriles por sentido (confirmado por el usuario; Perozo dice 1 de 5 m).
- **CC Paos:** carril de giro libre Fabricio Ojeda → Madre Vieja, de 1 carril de 5,5 m.
- **Tramos de entrada** de Lechería y FFAA sur: 60 km/h (antes 80).
- **FFAA:** 3,92 m por carril (calzada de 7,85 m según Perozo). Costanera: 3,70 m.
- **Semáforos:** los medidos en campo. Camino Real ciclo de 82 s (25/25/20 s con amarillo de 3 s y 1 s de todo rojo); CC Paos ciclo de 66 s.

### Vehículos (`costanera.rou.xml`)
- Sin `jmIgnoreFoeProb`, que hacía que los vehículos se atravesaran.
- **Livianos y carritos:** speedFactor de 1,10 (unos 44 km/h en zonas de 40; las tesis observan 40–50 km/h).
- **Pesados:** aceleración 1,0 (antes 0,4), prefieren el carril derecho y casi no cambian de carril para adelantar.
- Impaciencia de 0,5. Se probó un tipo agresivo solo para Av. Río y se descartó: empeoraba FFAA, aumentaba los choques y la variabilidad.

### Simulación y medición
- **Tiempo:** 0–900 s de calentamiento, 900–4500 s de hora de análisis, 4500–5400 s de vaciado.
- `time-to-teleport = -1` (sin teletransportes) y `tripinfo-output.write-unfinished = true` (registra también a los atrapados).
- **Medición:** un detector E3 por intersección más edgeData por acceso. La demora por acceso reparte la pérdida de tiempo de los tramos compartidos.
- **Nivel de servicio:** HCM 2000. Con semáforo: 10/20/35/55/80 s. Sin semáforo: 10/15/25/35/50 s, y la intersección toma el nivel del peor acceso secundario.
- **V/C y capacidad (HCM 2000):**
  - Con semáforo: c = 1900·fVP·N·g/C.
  - Principal sin semáforo: 1900·fVP·N.
  - Secundario: capacidad potencial de carril compartido.
  - Si el acceso está saturado (demanda ≥ 50 y atendida < 95 %, o demora de nivel F), se usa el flujo medido.
  - En 2041 se usa la capacidad de 2026 (la capacidad es propiedad de la vía).
- **Réplicas:** 5 con semillas 1 a 5. Con 3 el margen sería de ±27 s en Camino Real; con 5 es de ±13 s. Cada réplica corre en una carpeta temporal y nunca pisa los XML de la corrida en GUI.

### Excel
- Hojas originales del usuario, corregidas:
  - densidad calculada sobre el intervalo de 100 s, solo tramos de 20 m o más y solo la hora de análisis;
  - tramos sin duplicar;
  - viajes filtrados a 00:15–01:15, con la columna "Estado del viaje";
  - en la tabla dinámica de intersecciones, la intensidad se suma.
- Hojas nuevas: **Resumen Intersecciones**, **Resumen Viajes** y **Resumen Replicas**. Esta última es la que se usa en la tesis: demanda, capacidad, V/C, demanda atendida, demora con mínimo y máximo, y nivel de servicio.
- La "cola" de unos 384 m en la parada de bus de Puerto Guaica se deja tal cual por decisión del usuario, porque es un problema real. Se redacta como **"la parada bloquea el carril derecho el 23 % de la hora pico"** (el largo es un artefacto de cómo mide SUMO).
- En 2041, las demoras de miles de segundos en los accesos secundarios se dejan tal cual (decisión del usuario).

---

## 4. Resultados actuales (5 réplicas, 22/10/2026)

| Intersección | Base 2026 | 2041 sin proyecto |
|---|---|---|
| Camino Real | **D** · 42 s · V/C 0,95 (Costanera E, FFAA D) | **F** · 46 % atendida · V/C 1,37 |
| CC Paos | **C** · 23 s · V/C 0,73 | **F** · 33 % · V/C 1,03 (bloqueada por las colas de abajo) |
| Perrokero | **F** · 151 s · V/C 1,36 (Av. Río 734 s, 74 % atendida; FFAA norte F, V/C 1,05; FFAA sur A) | **F** · 40 % · V/C 1,97 |
| Bissau | Avenida A; salida residencial E (45 s) | **F** · 42 % |
| Puerto Guaica | **C** · 16 s | **F** · 43 % (bloqueada por Camino Real) |
| Red | 23,5 km/h, 0 teletransportes, 0 atrapados, FHMD 0,90 | 4,5 km/h, unos 1.560 atrapados, FHMD 0,67 (efecto del bloqueo) |

**Hallazgo clave:** en 2041 el colapso empieza en **Perrokero** (FFAA norte, 13 % atendida) y se propaga a Camino Real → Puerto Guaica → Bissau → CC Paos. Por eso conviene evaluar las propuestas en conjunto.

### Comparación con las tesis
- **Perrokero:** coincide (F hoy y F en el futuro).
- **CC Paos actual:** coincide (C, 22,6 s frente a 23,3 s).
- **Camino Real actual:** las tesis dan F (129 s) y la simulación D (V/C 0,95). Savignani usa 35 % de pesados (su tabla 37 dice 6 %), 1 carril de giro y un ciclo de 111 s. En 2041 la simulación también da F.
- **CC Paos futuro:** la tesis da C (2036) y la simulación F, por el efecto de red que el HCM aislado no capta.
- **Bissau y Fernández Padilla:** el F de Savignani es un error de cálculo del HCM (recalculado: unos 28 s, D).

### Errores encontrados en las tesis (útiles para el objetivo 3)
- **Savignani:** la tabla 55 usa GD3 = 603 en lugar de 190; la tabla 56 usa 35 % de pesados frente al 6 % de la tabla 37; el F de los accesos residenciales es un error de cálculo.
- **Perozo:** la demora es de 2.883,7 s en la tabla 4.9 y de 1.000,03 s en las conclusiones; en las conclusiones el costo quedó como "$ x.xxx.xxx"; las longitudes de rampa son contradictorias (40 frente a 100 m).
- **Ambas:** rampas al 15 % y al 12,3 % (altas para vía urbana); costos tomados de tesis extranjeras (Quito 2012, Bogotá 2017); los dos aforos se hicieron durante la pandemia y la crisis de combustible.

---

## 5. Acuerdos sobre la redacción de la tesis (capítulos 1 y 3)
- **Tipo de investigación:** de campo con apoyo documental (mixta). Nivel sugerido: descriptivo-evaluativo. Modalidad: proyecto factible.
- **Quitar** las entrevistas informales y los documentos de la Alcaldía (no se hicieron); el uso de las tesis va en la revisión documental.
- **Agregar la sección 3.7 Validez y confiabilidad:**
  - GEH < 5 en 60 de 61 movimientos, con criterio ≥ 85 % (DMRB y FHWA, *Traffic Analysis Toolbox*, vol. III);
  - comparación con las tesis;
  - 5 réplicas.
- **Cuadro 1.2:** mantener la V/C y agregar la demanda atendida.
- **Normas unificadas:** MTC 1997, MINDUR 1981, MVDUCT/INTT 2011 y HCM 2000. Quitar COVENIN.
- **Horizonte futuro 2041:** ×1,025¹⁵ = 1,448.
- **Supuestos a declarar:** +50 % post-COVID, aforo 2026 en calles secundarias, FHMD 0,90, 5 réplicas y capacidad HCM o medida.
- **Detalles de forma:**
  - citas sin referencia: Aragón, Baray, Sabino, Hernández y otros;
  - Arias 2016: el título correcto es *El proyecto de investigación*, de Editorial Episteme;
  - URLs dañadas por un reemplazo Rio → Río;
  - numeración CAPITULO 1 / CAPÍTULO III;
  - suavizar "SUMO es el software más utilizado".
- **Pendiente ofrecido:** redactar 3.7 Validez y confiabilidad y 3.8 Procedimiento listos para pegar. Ya se entregaron el texto de la actualización del aforo y el de la parada de bus.

---

## 6. Próximos pasos
1. **Commit en `main`** (GitKraken) de todos los cambios y la reorganización.
2. **Propuestas:** NO fusionar `main` con las ramas viejas, porque `costanera.net.xml` daría conflicto. Crear cada propuesta **desde el `main` actual** (rama nueva o rama vieja reiniciada) y volver a aplicar su geometría.
3. Cada propuesta usa **la misma demanda** (2026 y 2041) y las mismas herramientas; solo cambian la red y los semáforos. Después: regenerar los detectores (`python herramientas\generar_detectores.py`), adaptar su `.bat` (`CSV_DIR` = `EXCEL RESULTADOS\PROPUESTA_X`) y su Excel (copia del base con las rutas cambiadas).
4. Orden sugerido: Savignani (distribuidor en Camino Real, bahías de bus, carriles de incorporación) → Perozo (puente en Perrokero y semáforo debajo) → propuesta final con las recomendaciones.
5. Al actualizar cada propuesta, borrar los `xml2csv.py` viejos de `EXCEL RESULTADOS\PROPUESTA_*`.
6. Redactar las secciones 3.7 y 3.8. Objetivo 4: costos.

## 7. Reglas de trabajo importantes
- Si se cambia la red en netedit, correr `python herramientas\generar_detectores.py` y `python herramientas\generar_demanda.py`. Si un movimiento contado cambia de camino, ajustar su fila en `conteos_movimientos.csv`.
- Los `.bat` deben tener saltos de línea CRLF (con LF, cmd corta los comandos).
- Antes de modificar un Excel por script, debe estar cerrado (si no, se abre en solo lectura). Siempre hacer respaldo.
- No correr simulaciones en `02_Resultados_*` con SUMO-GUI abierto (se pisan los XML).
- Revisar siempre el realismo: choques, colas, teletransportes y volúmenes por calle. El usuario valora el realismo por encima de cuadrar cifras.
