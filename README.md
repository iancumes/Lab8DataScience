# Laboratorio 8 DuckDB

CC3084, Universidad del Valle de Guatemala, Ciclo 2 de 2026.
Basado en https://github.com/menene/duckdb.

## Integrantes

- Javier Valladares, 23045
- Ian Cumes, 23236
- Javier Cifuentes, 23079

## Ambiente y descarga

Se usa Docker Compose para levantar JupyterLab y Metabase con DuckDB.
Los datos originales quedan en data/raw y no se incluyen en Git.

```bash
git clone https://github.com/iancumes/Lab8DataScience.git
cd Lab8DataScience
touch .env
docker compose up -d --build
docker compose exec lab python scripts/download_data.py --years 2026 --manifest docs/manifests/initial_2026.json
docker compose exec lab python -m unittest discover -s tests -v
```

JupyterLab abre en http://localhost:8888/lab y Metabase en http://localhost:3000.
El descargador consulta el catálogo oficial, valida los Parquet y conserva los
archivos existentes. El manifiesto inicial registra 16 archivos de enero a agosto
de 2026 y 30,040,469 filas. El año 2026 todavía está incompleto.

## Análisis y benchmark

Las vistas normalizan 19 columnas de yellow y green y conservan las filas
originales. Los indicadores usan reglas de calidad explícitas en sql/00_views.sql.
La comparación anual usa enero a agosto en los tres años.

```bash
docker compose exec lab python scripts/download_data.py --years 2024 2026 --manifest docs/manifests/expanded_2024_2026.json
docker compose exec lab python scripts/analyze.py --years 2026 --stage initial_2026
docker compose exec lab python scripts/analyze.py --years 2024 2026 --stage expanded_2024_2026
docker compose exec lab python scripts/download_data.py --years 2024 2025 2026 --manifest docs/manifests/final.json
docker compose exec lab python scripts/analyze.py --years 2024 2025 2026 --stage final
docker compose exec lab python scripts/benchmark.py --repeats 3
```

Los CSV, esquemas y SQL de cada etapa están en docs/results. Las trece preguntas
y sus decisiones se documentan en docs/metodologia.md. El benchmark incluye
cuatro consultas, cuatro escalas, caché caliente, tres repeticiones y comparación
de resultados entre lectura Parquet y tabla materializada. Los 96 tiempos y
el costo de crear cada tabla se conservan en docs/benchmarks.
