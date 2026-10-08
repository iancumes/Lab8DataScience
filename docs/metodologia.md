# Preguntas, indicadores y decisiones

Se trabaja con los datos publicados por NYC TLC para taxis yellow y green. El año
2026 está incompleto: se debe leer el manifiesto para conocer el corte real. Los
análisis temporales usan el año y mes del archivo y exigen que el pickup coincida
con ellos. Las fechas de TLC se interpretan como hora local de Nueva York.

## Preguntas e indicadores (ejercicios 4 y 7)

| # | Pregunta | Indicador y unidad | Justificación | Consulta |
|---|---|---|---|---|
| 1 | ¿Cómo cambia la demanda mensual de cada taxi? | Conteo de viajes válidos/mes | Identifica estacionalidad y diferencia de escala | 04_monthly |
| 2 | ¿Cómo cambia el importe registrado mensual? | Suma de total_amount, USD | Aproxima actividad económica; no es beneficio neto | 04_monthly |
| 3 | ¿Cuánto paga en promedio un viaje? | Media de total_amount, USD/viaje | Compara ticket; sensible a extremos y composición | 04_monthly |
| 4 | ¿Qué tan largos son los viajes típicos? | Mediana de trip_distance, millas | Resume distancias asimétricas con robustez | 04_monthly y 07_distributions |
| 5 | ¿Cuánto dura un viaje típico? | Mediana de duración, minutos | Resume uso operativo y permite comparar tipos | 04_monthly y 07_distributions |
| 6 | ¿Cuándo se concentra la actividad? | Conteo por hora y tipo | Describe franjas de demanda | 05_hourly |
| 7 | ¿Cómo cambia la mezcla de pagos? | Porcentaje por payment_type | Evita asumir que todos los pagos son efectivo o tarjeta | 06_payments |
| 8 | ¿Qué proporción de tarifa se registra como propina en tarjeta? | 100 × suma(propina)/suma(tarifa), solo tarjeta y propina no negativa | La propina en efectivo no está observada: no se equiparan ambos medios | 04_monthly |
| 9 | ¿Qué fracción queda fuera de las reglas analíticas? | 100 × filas excluidas/filas originales | Expone sensibilidad y problemas de calidad | 03_quality |
| 10 | ¿Cómo evoluciona la demanda en meses comparables? | Viajes por tipo/año, mismos meses | Evita confundir cobertura parcial con descenso | 08_common_months |
| 11 | ¿Qué días tienen mayor actividad ajustada por exposición? | Viajes/día observado por día de semana | Corrige distinta cantidad de lunes, martes, etc. | 09_weekday |
| 12 | ¿Cómo se distribuyen distancias e importes? | Bandas, mediana, p95, p99 | Identifica colas y cambios de composición | 07_distributions y 10_distance_bins |
| 13 | ¿Qué valores extremos deben revisarse? | Top 20 importes originales y flags | Separa observación de corrección automática | 11_outliers |

El tablero Metabase muestra 10 visualizaciones: volumen, importe total, ticket,
distancia mediana, duración mediana, proporción de tarjeta, propinas en tarjeta,
perfil horario, exclusión por calidad y evolución comparable. Cada tarjeta incluye
su interpretación y SQL. Los gráficos estáticos son evidencia complementaria.

## Transformaciones registradas

1. `scripts/common.py` descubre archivos por año/tipo, extrae año/mes de su nombre,
   normaliza tpep/lpep a pickup/dropoff y aplica casts explícitos a columnas comunes.
2. `read_parquet(..., union_by_name=true)` alinea columnas por nombre. Se conserva
   el esquema completo original en schemas.csv. `cbd_congestion_fee` se representa
   como NULL cuando no existe; nunca se sustituye por cero. La tabla normalizada
   proyecta 19 columnas para el análisis; no pretende conservar todas las variables
   exclusivas de los esquemas yellow/green.
3. `sql/00_views.sql` calcula duración en minutos y flags de calidad. La población
   principal requiere pickup en el mes/año de su archivo, distancia >0 y <=100
   millas, duración >0 y <=180 minutos, tarifa e importe positivos.
4. Son umbrales operativos elegidos para este análisis, no una afirmación de que
   todo viaje excluido sea falso. Viajes con reembolsos, ajustes o recorridos largos
   pueden ser reales. No se eliminan del Parquet ni de trips_raw/trips_flagged.
5. No se imputa passenger_count ni se exige que esté entre 1 y 6. Se reportan sus
   faltantes y valores inusuales. No se deduplican filas: dos viajes iguales pueden
   ser reales y no hay identificador universal con el cual probar un duplicado.
6. total_amount excluye propinas en efectivo según el diccionario TLC. El código de
   pago 0 identifica viajes Flex Fare, no un instrumento de pago; no se deduce un
   aumento de efectivo a partir de un descenso del código 1.
   Los importes se reportan en USD nominales, sin ajuste por inflación. Un aumento
   del ticket no prueba aumento de tarifas: también cambia la composición de viajes.
7. Los indicadores mensuales usan viajes válidos; inventario y calidad usan todas
   las filas. Los benchmarks usan TODAS las filas normalizadas con SQL equivalente.
8. El tablero consulta un snapshot de agregados producido por DuckDB. Permite
   reproducir los resultados sin escanear millones de filas en cada interacción.
   Debe regenerarse al incorporar nuevos archivos.

## Descarga completa e incremental

El script base ya implementaba yellow/green, omisión de archivos existentes y
renombrado atómico, pero fijaba ANIO=2026. También convertía cualquier error de HEAD
en "no publicado", lo que podía ocultar fallos de red. Se generalizó a `--years` y
`--months`, se usa el catálogo enlazado en la página oficial, se añadieron reintentos,
validación de longitud/footer, hash SHA-256 y manifiesto JSON. Un error HTTP o un
archivo local corrupto produce un estado de error y código de salida distinto de 0.

Completo significa: todos los enlaces yellow/green de los años/meses solicitados
en el catálogo oficial tienen archivo local legible y no vacío. No significa que
se haya probado la integridad de la recolección original TLC. Para años pasados se
exigen los 12 meses por tipo; para el año en curso se registran meses no publicados.
El hash fija qué versión se analizó, pero no es una firma oficial ni detecta una
revisión remota futura: por requisito, los archivos existentes no se redescargan.

Los manifiestos initial, expanded y final permiten comprobar que la incorporación
2024 y 2025 conservó hashes, bytes y filas de los años ya descargados. Una segunda
corrida final registra todos como existing; verificar este resultado forma parte
de `scripts/verify.py`.

## Benchmark válido

Cuatro escalas: primer mes de 2026 (ambos taxis), todos los meses de 2026,
2024+2026 y 2024+2025+2026. Cuatro consultas: agrupación mensual con suma decimal,
perfil horario, cuantiles exactos de importe y zonas principales con filtro.

Las dos rutas usan el mismo conjunto de archivos y el mismo esquema normalizado.
La materialización CTAS incluye todas las filas y se mide aparte junto con el
CHECKPOINT. Cada consulta se calienta en ambas rutas y se repite tres veces con
orden alternado. El tiempo incluye ejecución y fetchall; no incluye creación de la
vista ni descarga. Las tablas resumen reportan mediana/mínimo/máximo. Se valida la
igualdad de resultados de todas las repeticiones: exacta para enteros/texto y con
tolerancia rel=1e-9, abs=1e-6 para flotantes/decimales.

Se usa caché caliente: no se controla la caché del sistema operativo ni se afirma
medir I/O frío. Un único equipo, 4 threads y memory_limit=3GB. Las operaciones de
arranque de Docker/descarga deben finalizar antes de medir. No es una comparación
universal de motores. La tabla materializada final se conserva para inspección;
las escalas previas se reemplazan para limitar disco.

## Fuentes

- [Repositorio base](https://github.com/menene/duckdb)
- [TLC: catálogo y advertencias de calidad](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [Diccionario Yellow TLC](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)
- [Diccionario Green TLC](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf)
- [DuckDB: lectura Parquet y pushdown](https://duckdb.org/docs/stable/data/parquet/overview)
- [DuckDB: concurrencia](https://duckdb.org/docs/stable/connect/concurrency)
- [Driver DuckDB para Metabase](https://github.com/motherduckdb/metabase_duckdb_driver)
