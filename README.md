# Lab 8 - DuckDB | NYC TLC

Laboratorio CC3084, UVG, Ciclo 2 de 2026. Basado en el
[repositorio base](https://github.com/menene/duckdb).

## Integrantes

- Javier Valladares, 23045
- Ian Cumes, 23236
- Javier Cifuentes, 23079

Descarga incremental de yellow/green: 2026, luego 2024 y después 2025. Incluye
consultas directas Parquet, calidad, indicadores, benchmark contra tablas DuckDB,
notebook ejecutado y tablero Metabase con 10 visualizaciones.

- [Informe, hallazgos y discusión 9.1-9.8](docs/informe.md).
- [Informe en Word](output/docx/Laboratorio_8_DuckDB.docx).
- [13 preguntas, indicadores y decisiones metodológicas](docs/metodologia.md).
- [Consultas y resultados iniciales](docs/results/initial_2026/queries.md).
- [Consultas y resultados 2024+2026](docs/results/expanded_2024_2026/queries.md).
- [Consultas y resultados finales](docs/results/final/queries.md).
- [Verificación del ambiente](docs/ambiente.md).
- [Evidencia del tablero Metabase](docs/tablero.md).

## Estructura y propósito

| Ruta | Propósito |
|---|---|
| data/raw/tipo/año/ | Parquet originales, excluidos de Git |
| data/processed/ | Tabla materializada, snapshot para Metabase y temporales, fuera de Git |
| scripts/ | Descarga, análisis, benchmark, informe, notebook, tablero y verificación |
| sql/ | Vistas de calidad y consultas analíticas versionadas |
| sql/benchmarks/ | Cuatro consultas parametrizadas equivalentes |
| sql/dashboard/ | SQL de cada tarjeta |
| notebooks/ | Notebook ejecutado con consultas directas |
| docs/manifests/ | URL, bytes, filas, SHA-256 y estado de cada etapa |
| docs/results/ | CSV pequeños, esquemas, metadatos y documentación SQL |
| docs/benchmarks/ | Tiempos individuales, resumen, CTAS y entorno |
| docs/figures/ | Evidencia gráfica |
| Dockerfile | Python, DuckDB, JupyterLab, Pandas, PyArrow, Matplotlib, Requests |
| metabase.Dockerfile | Java 21, Metabase y driver DuckDB sobre glibc |
| docker-compose.yml | Servicios, puertos locales y volúmenes persistentes |

## Cómo levantar el ambiente (ejercicio 1)

Requisitos: Git, Docker Desktop iniciado y Docker Compose. Se recomiendan al menos
10 GB libres y memoria suficiente para DuckDB (límite 3 GB), Jupyter y Metabase.
En macOS, conviene mantener descargada la carpeta si reside en iCloud Drive para
evitar que el sistema retire archivos durante el análisis.

```bash
git clone https://github.com/iancumes/Lab8DataScience.git
cd Lab8DataScience
touch .env
docker compose up -d --build
docker compose ps
curl -f http://localhost:8888/api/status
curl -f http://localhost:3000/api/health
docker compose exec lab python -c "import duckdb, pandas, pyarrow; print(duckdb.__version__)"
```

Abra [JupyterLab](http://localhost:8888/lab) y [Metabase](http://localhost:3000).
Los servicios escuchan solo en 127.0.0.1. Jupyter conserva la configuración local
sin token del repositorio base. El proyecto vive en `/workspace` dentro de los
contenedores y data se monta en `/workspace/data`. Los scripts resuelven las rutas
respecto a su ubicación. `docker compose down` detiene los servicios y conserva
los datos y el volumen Metabase.

Docker y versiones directas fijadas reducen diferencias entre equipos. SQL,
reglas, manifiestos y hashes permiten identificar los datos y transformaciones
que produjeron los resultados. No se garantiza reproducción bit a bit si cambian
imágenes base, dependencias transitivas o archivos originales de TLC.

## Cómo descargar los datos (ejercicios 2, 5 y 8)

```bash
# Pasaporte: meses publicados de ambos tipos en 2026.
docker compose exec lab python scripts/download_data.py --years 2026 --manifest docs/manifests/initial_2026.json
# Añadir 2024 conservando 2026.
docker compose exec lab python scripts/download_data.py --years 2024 2026 --manifest docs/manifests/expanded_2024_2026.json
# Añadir 2025 conservando los anteriores.
docker compose exec lab python scripts/download_data.py --years 2024 2025 2026 --manifest docs/manifests/final.json
# Segunda ejecución: todos deben aparecer como existing.
docker compose exec lab python scripts/download_data.py --years 2024 2025 2026 --manifest docs/manifests/rerun.json
```

Opciones: `--taxi yellow|green|all`, `--months 1 2 ...`, `--workers 4`. El valor por
defecto es ambos taxis y todos los meses publicados de 2026. Se consulta el
catálogo oficial, se reintentan fallos transitorios y se verifica longitud/footer
Parquet antes del renombrado atómico desde `.part`. Un archivo existente se valida
y omite; uno corrupto produce error y no se sobrescribe automáticamente.

Completo significa obtener todos los enlaces oficiales de los años/meses
solicitados con archivos locales legibles y no vacíos. No significa probar que
TLC haya recogido todos los viajes reales. Los meses no publicados quedan en el
manifiesto; los hashes permiten comprobar que las etapas preservaron las entradas.
El hash no es una firma oficial ni detecta revisiones futuras en el servidor.

## Cómo ejecutar el análisis

```bash
# Reproduce las tres etapas en el orden del enunciado; incluye benchmark e informe.
docker compose exec lab python scripts/run_pipeline.py
```

El pipeline no configura Metabase; ese paso está abajo. Para pasos independientes:

```bash
docker compose exec lab python scripts/analyze.py --years 2026 --stage initial_2026
docker compose exec lab python scripts/analyze.py --years 2024 2026 --stage expanded_2024_2026
docker compose exec lab python scripts/analyze.py --years 2024 2025 2026 --stage final
```

`run_pipeline.py --skip-download` reutiliza entradas y `--skip-benchmark` conserva
las mediciones existentes (requiere haber ejecutado benchmark previamente).
Las consultas leen Parquet con union_by_name y normalización tpep/lpep. El esquema
de cada archivo está en schemas.csv. queries.md contiene SQL, objetivo, fuentes,
resultado y decisión de cada consulta. Calidad usa todas las filas; indicadores
usan la población válida definida en sql/00_views.sql. Se conservan los originales.

## Cómo reproducir los benchmarks (ejercicio 6)

```bash
docker compose exec lab python scripts/benchmark.py --repeats 3
```

Cuatro escalas: un mes 2026, todo 2026, 2024+2026 y los tres años. Cuatro consultas,
calentamiento de ambas rutas, tres repeticiones con orden alternado y validación
de equivalencia de todos los resultados. El tiempo incluye fetchall y excluye la
descarga. CTAS+CHECKPOINT se mide aparte. Caché caliente: no se afirma medir I/O frío.

- timings.csv: cada ejecución, filas, archivos y coincidencia de resultados.
- summary.csv: mediana, mínimo y máximo por consulta/ruta/escala.
- materialization.csv: tiempo CTAS y bytes en disco.
- environment.json: equipo, versiones, threads y metodología.

Se reconstruye data/processed/materialized.duckdb y queda con el conjunto final.
Metabase consulta otra base de agregados, sin bloquear la base del benchmark.

## Cómo generar resultados principales y tablero (ejercicios 7-9)

```bash
docker compose exec lab python scripts/report.py
docker compose exec lab python scripts/create_notebook.py
# Espere hasta que /api/health responda antes del setup.
docker compose exec lab python scripts/setup_metabase.py --url http://metabase:3000
```

La primera configuración crea un usuario local con contraseña aleatoria y guarda
el acceso en `.env`, ignorado por Git. Consulte ese archivo local para iniciar
sesión; no se publican credenciales. Para una cuenta ya configurada pueden usarse
las variables MB_ADMIN_EMAIL y MB_ADMIN_PASSWORD. El script comprueba las consultas
y crea/actualiza 10 tarjetas con SQL e interpretación y su tablero.

La conexión DuckDB es de solo lectura: `/workspace/data/processed/dashboard.duckdb`.
IDs y SQL quedan en docs/dashboard.json. Abra Metabase en localhost:3000 y la ruta
`/dashboard/<id>` indicada ahí. El hostname `metabase` pertenece a la red Docker.
El informe incluye figuras estáticas complementarias, hallazgos numéricos y las
respuestas de discusión. El notebook se genera y ejecuta sin errores.

Para actualizar datos, detenga Metabase antes de reescribir su snapshot:

```bash
docker compose stop metabase
docker compose exec lab python scripts/run_pipeline.py
docker compose start metabase
# Espere a que /api/health responda.
docker compose exec lab python scripts/setup_metabase.py --url http://metabase:3000
```

La tabla y snapshot se refrescan explícitamente. Las vistas se reconstruyen al
analizar y descubren archivos nuevos. La comparación anual usa meses comunes;
no compara doce meses de un año con un año 2026 parcial.

## Verificación final

```bash
docker compose exec lab python scripts/download_data.py --years 2024 2025 2026 --manifest docs/manifests/rerun.json
docker compose exec lab python scripts/verify.py
```

Comprueba conservación de hashes, omisión de archivos anteriores, conteos de
inventario/calidad/indicadores, benchmark en cuatro escalas, tarjetas con datos,
notebook ejecutado y ausencia de Parquet, bases y credenciales en Git. El resultado
está en docs/verification.json. La verificación de salud está en docs/ambiente.md.

## Alternativa Python local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_pipeline.py
python scripts/setup_metabase.py --url http://localhost:3000
```

Los metadatos de benchmark indican dónde se midió. No mezclar tiempos macOS y
contenedor sin reportarlo. Los datos siguen fuera de Git en ambas modalidades.

## Informe en Word

El documento incluye a los tres integrantes y los nueve ejercicios, con tablas
resumidas, figuras y respuestas de discusión. Para regenerarlo a partir de los
resultados guardados, se usa la dependencia opcional python-docx:

```bash
pip install -r requirements-report.txt
python scripts/create_word_report.py
```

## Entregables

Ejercicios 1-2: ambiente y manifiesto inicial. Ejercicios 3-5: SQL y resultados por
etapa. Ejercicio 6: script y tablas de benchmark. Ejercicio 7: 13 preguntas, 10
indicadores visualizados y tablero. Ejercicios 8-9: evolución de tres años y
respuestas 9.1-9.8. Se incluyen notebook ejecutado, figuras y verificaciones.
La entrega está en https://github.com/iancumes/Lab8DataScience. Se organiza en tres
commits sobre el README inicial: ambiente y descarga, análisis y benchmarks, e
informe con notebook, tablero y Word. Los commits usan las fechas reales.
