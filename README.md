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
