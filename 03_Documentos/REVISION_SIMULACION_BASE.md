# Revisión completa de la simulación base (29/10/2026)

Revisión de la red, la demanda, los resultados, el Excel y los documentos del escenario sin proyecto (2026 y 2041), antes de entregar la información para la tesis.

## 1. Lo que está bien (verificado)

| Aspecto | Verificación | Resultado |
|---|---|---|
| Red y resultados al día | `main` sin cambios pendientes (commit `02e7a92`); el Excel base 2026 tiene exactamente las mismas réplicas que el documento del capítulo IV | ✔ |
| Calidad de la simulación | Semillas 1 y 3: 0 choques, 0 frenadas de emergencia, 0 teletransportes, 0 vehículos atrapados ni esperando para entrar; demora de inserción de 0,6 s | ✔ |
| Validación de la demanda | GEH < 5 en 60 de 61 movimientos (98 %; criterio ≥ 85 %) | ✔ |
| Variación dentro de la hora | FHMD simulado de 0,89 frente a 0,90 de diseño | ✔ |
| Semáforos | Tiempos de campo: Camino Real 82 s, CC Paos 66 s | ✔ |
| Geometría | Anchos y carriles de las tesis, salvo 3 casos justificados (Cuadro 4.2 y su nota) | ✔ |
| Coherencia de las tesis | Los volúmenes de Savignani cumplen la conservación del flujo: lo que sale de Camino Real hacia Lechería (435 + 385 = 820) coincide con lo que pasa por Bissau y Puerto Guaica (747 y 799) | ✔ |
| Concordancia con las tesis | CC Paos C (tesis C, 22,6 s; simulación 21,1 s); Perrokero F (tesis F); Camino Real D frente a F de la tesis, explicado por los errores S1 a S3 | ✔ |

## 2. Lo que hay que corregir antes de entregar

1. **El Excel de 2041 está desactualizado.** Sus resultados son del 22/10 (red anterior y sin las columnas nuevas). El documento del capítulo IV ya usa los resultados correctos, pero el Excel no. → Correr `SIMULACION_2041.bat` en `main`.
2. **El capítulo III del Word todavía no refleja lo acordado** (es tarea de la redactora):
   - dice "no experimental" y "de campo"; el tutor indicó experimental y documental;
   - mantiene la entrevista informal, los documentos de la Alcaldía y del Ministerio y las normas COVENIN y AASHTO, que no se usaron;
   - la muestra dice "horas pico (mañana, mediodía y tarde) durante días hábiles": no corresponde a los conteos de verificación de corta duración;
   - el procedimiento debe ser la sección 3.9 (después de 3.7 Validez y 3.8 Procesamiento);
   - en el Cuadro 1.2, cambiar "hombrillos" y "radios de giro" por "isla y acera" y "número de carriles";
   - faltan en las referencias: MTC (1997), MINDUR (1981), MVDUCT/INTT (2011), HCM 2000, FHWA Toolbox vol. III y las dos tesis evaluadas.

## 2b. Escenario de sensibilidad: demanda 2026 sin el +50 % post COVID (×1,131)

Misma red, semáforos y método; solo cambia el factor de la demanda del corredor principal (las calles secundarias y la Av. Río no cambian). GEH < 5 en 61 de 61 movimientos; 5 réplicas; 0 teletransportes. Archivos en `03_Documentos/capitulo4/sensibilidad_sin_postcovid`.

| Intersección | Base ×1,697 | Sensibilidad ×1,131 | Tesis |
|---|---|---|---|
| Camino Real | D · 43,9 s · V/C 0,95 | C · 24,9 s · V/C 0,62 | F · 129,3 s |
| CC Paos | C · 21,1 s | B · 16,6 s | C · 22,6 s |
| Perrokero | F · 145,2 s · V/C 1,42 | C · 13,7 s · V/C 1,07 | F |
| Bissau (promedio) | 7,3 s (salida en F) | 3,2 s (salida en C) | F (error de cálculo) |
| Puerto Guaica (promedio) | 17,0 s | 4,9 s | F (error de cálculo) |
| Red: velocidad / tiempo de viaje / demora | 23,3 km/h · 313 s · 160 s | 37,0 km/h · 194 s · 42 s | 40–50 km/h observados |
| Av. Río: vehículos que salen | 122 veh/h (70 %) | 169 veh/h (100 %) | Perozo 93; campo 180 |
| Colas máximas: Costanera en Camino Real / FFAA hacia Perrokero / Av. Río | 155 / 305 / 287 m | 76 / 80 / 33 m | — |

**Lectura:** el diagnóstico depende mucho del factor post COVID.
- Con ×1,697 (base), la simulación reproduce lo que dicen las tesis y el planteamiento del problema: Perrokero en F y Camino Real cerca de su capacidad.
- Con ×1,131, todo funciona entre A y C, la velocidad de la red (37 km/h) se acerca a los 40–50 km/h observados por las tesis, y la Av. Río descarga lo mismo que en el conteo de campo (169 frente a 180 veh/h). Pero contradice el nivel F de Perrokero que reportan ambas tesis.
- **Las dos versiones son extremos razonables de la demanda real**; conviene presentarlas como rango y decir cuál se adopta y por qué.
- **Forma de decidir con evidencia:** medir en los videos de campo, en la hora pico, la cola máxima en la Costanera hacia Camino Real, en FFAA hacia Perrokero y en la Av. Río, y compararla con la tabla. Si se ven colas de 150 a 300 m, la base es la más realista; si son de 30 a 80 m, la demanda real está más cerca de ×1,131.

## 3. Puntos que hay que explicar bien (posibles preguntas del jurado)

### 3.1 La demanda del modelo es mayor que el conteo de campo en la avenida
| Movimiento | Tesis 2021 | Modelo 2026 | Campo 2026 | Modelo / campo |
|---|---|---|---|---|
| Camino Real: El Ejército → Costanera | 435 | 738 | 600 | 1,23 |
| Camino Real: FFAA → Costanera | 385 | 653 | 420 | 1,55 |
| CC Paos: Lechería → Costanera | 625 | 1.061 | 480 | 2,21 |
| Bissau: Costanera → Camino Real | 774 | 1.313 | 450 | 2,92 |
| Puerto Guaica: Costanera → Camino Real | 810 | 1.375 | 420 | 3,27 |
| Perrokero: Camino Real → FFAA sur | 568 | 964 | 180 | 5,36 |

- En los **giros de las intersecciones**, modelo y campo son parecidos (0,7 a 1,5 veces).
- En el **tránsito directo de la avenida**, el modelo tiene de 2 a 5 veces lo contado, e incluso la tesis de 2021 (en pandemia) es mayor que el conteo de 2026.
- **El conteo de campo no cumple la conservación del flujo:** de Camino Real salen hacia Lechería 600 + 420 = 1.020 veh/h, pero 300 m más adelante, en Puerto Guaica, se contaron 480 (entre ambos puntos no hay salidas importantes). Lo mismo en sentido contrario. Lo más probable es que, en la avenida, el conteo de 2 a 3 minutos no haya captado todos los carriles o haya caído en un momento sin pelotón.
- **Conclusión para la tesis:** los conteos propios sirven para verificar los giros y las calles secundarias, pero no para reemplazar los volúmenes de las tesis en la avenida. Conviene decirlo así en el capítulo IV.
- **Recomendación:** correr un **escenario de sensibilidad** sin el +50 % post COVID (solo ×1,131) para mostrar que las conclusiones se mantienen aunque la demanda sea menor.

### 3.2 Av. Río (Perrokero)
- En la simulación, la Av. Río logra salir a 122 veh/h (75 % de su demanda) con 817 s de demora.
- Perozo calcula una capacidad del giro de 93 veh/h (Tabla 4.8); en el conteo de campo salieron 180 veh/h.
- La simulación queda entre los dos. Es un resultado defendible, pero el conteo es de solo 3 minutos (14 vehículos), con un margen de ±25 %. Si se quiere afinar, se puede ajustar la aceptación de brechas en ese acceso para que descargue unos 150 a 180 veh/h.

### 3.3 Nivel de servicio de las intersecciones sin semáforo
- El HCM 2000 no define un nivel de servicio global para intersecciones con PARE en los accesos secundarios: lo define por movimiento o acceso secundario.
- En el modelo se asigna a la intersección el nivel del peor acceso secundario. Por eso Bissau sale en F aunque su demora promedio es de 7,3 s: la salida de la residencia (23 veh/h) tiene 66 s, con un rango de 19 a 168 s entre réplicas. Con tan pocos vehículos, unas pocas esperas largas cambian la letra.
- **Recomendación:** en la tesis, reportar en estas intersecciones el nivel de la avenida y el de cada salida por separado, con su volumen, en lugar de una sola letra.

### 3.4 Velocidades
- Las tesis observan de 40 a 50 km/h en el corredor. En la simulación, la Costanera entre intersecciones circula a 30–38 km/h y la red completa a 23,3 km/h, porque incluye las esperas en los semáforos y en Perrokero. Es coherente: la velocidad de 40 a 50 km/h es la de circulación libre entre intersecciones.

## 4. Detalles menores del modelo (no afectan los resultados)
- En CC Paos, el carril derecho de la salida Madre Vieja → Lechería no recibe conexiones (todos entran por el izquierdo). El movimiento es de 195 veh/h y no se satura.
- Hay avisos de geometría en calles internas de urbanizaciones sin tránsito simulado.

## 5. Recomendaciones para fortalecer la tesis
1. **Escenario de sensibilidad de la demanda** (sin el +50 %): responde de antemano la pregunta más probable del jurado.
2. **Tabla de conservación del flujo** para justificar por qué se usan los volúmenes de las tesis y no el conteo corto.
3. **Reportar las intersecciones sin semáforo por acceso**, no con una sola letra.
4. **Mencionar las limitaciones:** conteo corto, demanda basada en datos de 2021 y factor post COVID estimado por Savignani, y el modelo no incluye motos ni peatones.
5. **Usar las incongruencias de las tesis** (archivo INCONGRUENCIAS_TESIS_EVALUADAS, 25 puntos de Savignani y 8 de Perozo) como base del objetivo 3.
