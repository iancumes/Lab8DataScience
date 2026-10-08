# Benchmark: consultas, fuentes y protocolo

El código ejecutable está en `scripts/benchmark.py` y `sql/benchmarks/`.

| Consulta | Pregunta y objetivo | Operaciones |
|---|---|---|
| monthly.sql | ¿Cuántas filas e importe hay por taxi/año/mes? | Agrupación y suma decimal |
| hourly.sql | ¿Cómo se distribuyen los viajes por hora y su distancia media? | Extracción horaria, agrupación, promedio |
| distribution.sql | ¿Cuál es la mediana y el p95 del importe? | Cuantiles exactos, sin filtrar importes extremos |
| top_zones.sql | ¿Cuáles son las principales zonas de recogida con importe/distancia positivos? | Filtro, agrupación, orden y LIMIT |

`{source}` es el único parámetro que cambia: `parquet_source` o
`trips_materialized`. La primera vista usa lectura Parquet y normalización de
`scripts/common.py`; la segunda tabla es `CREATE TABLE ... AS SELECT * FROM
parquet_source`. Por tanto conservan exactamente las mismas filas y columnas.
Los benchmarks usan la población original normalizada, sin aplicar las reglas de
los indicadores, salvo los filtros explícitos que aparezcan en cada consulta.

Las fuentes por escala son: primer mes publicado de 2026 en ambos tipos; todos
los meses 2026; todos los archivos 2024+2026; todos los archivos de los tres años.
El manifiesto final documenta las URLs, tamaños, filas y hashes de las entradas.
La cantidad exacta por escala aparece en materialization.csv y timings.csv.

Se registra CTAS+CHECKPOINT aparte, se calientan ambas rutas, se alterna su orden
y se ejecuta fetchall en el intervalo medido. Son tres repeticiones por ruta y
consulta. Cada resultado se contrasta con la salida inicial Parquet (tolerancia
para flotantes: relativa 1e-9, absoluta 1e-6). No se limpia la caché del sistema
operativo; el experimento mide caché caliente en un único equipo.

Tiempos individuales: timings.csv. Mediana/mínimo/máximo: summary.csv. Costo de
materializar y almacenamiento: materialization.csv. Entorno: environment.json.
Interpretación y decisión Parquet/tabla: ../informe.md, ejercicio 6.

Para reproducir: `docker compose exec lab python scripts/benchmark.py --repeats 3`.
La base materializada final queda en data/processed/materialized.duckdb. No está
versionada y no es la base utilizada por Metabase.
