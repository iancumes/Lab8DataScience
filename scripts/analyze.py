#!/usr/bin/env python3
"""Ejecuta SQL directamente sobre Parquet y exporta resultados pequeños auditables."""
import argparse
import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path
import duckdb
import pandas as pd
import pyarrow.parquet as pq
from common import ROOT, connect, files, create_views, sqlstr


def markdown(frame, limit=40):
    frame = frame.head(limit).astype(object).fillna('NULL')
    def escape(x):
        return str(x).replace('|', '\\|').replace('\n', ' ')
    return '\n'.join(['| ' + ' | '.join(map(escape, frame.columns)) + ' |',
        '|' + '|'.join(['---'] * len(frame.columns)) + '|'] +
        ['| ' + ' | '.join(map(escape, row)) + ' |' for row in frame.itertuples(index=False, name=None)])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--years', nargs='+', type=int)
    parser.add_argument('--stage', default='final')
    args = parser.parse_args()
    selected = files(args.years)
    out = ROOT / 'docs/results' / args.stage
    out.mkdir(parents=True, exist_ok=True)
    con = connect()
    create_views(con, selected)
    # Esquemas originales de CADA archivo (incluye columnas específicas del taxi).
    schema_rows = []
    for path in selected:
        for field in pq.read_schema(path):
            schema_rows.append(dict(file=str(path.relative_to(ROOT)), column=field.name, type=str(field.type)))
    schemas = pd.DataFrame(schema_rows)
    schemas.to_csv(out / 'schemas.csv', index=False)
    unique = schemas[['column', 'type']].drop_duplicates().sort_values(['column', 'type'])
    unique.to_csv(out / 'schema_types.csv', index=False)
    con.sql('DESCRIBE trips_raw').df().to_csv(out / 'normalized_schema.csv', index=False)
    metadata = dict(stage=args.stage, years=sorted({int(p.parent.name) for p in selected}),
        generated_at_utc=datetime.now(timezone.utc).isoformat(), duckdb=duckdb.__version__,
        python=platform.python_version(), platform=platform.platform(),
        files=[str(p.relative_to(ROOT)) for p in selected], queries={})
    descriptions = {
        '01_inventory': ('Cantidad de archivos y registros', 'Se conserva toda fila, incluso fechas fuera de rango; el año de origen viene del nombre del archivo.'),
        '02_sample': ('Muestra de registros', 'Muestra de conveniencia para inspección; no se usa para estimar indicadores ni se garantiza un orden estable.'),
        '03_quality': ('Calidad y exclusiones', 'Los motivos pueden solaparse; excluded cuenta la unión. NULL también se marca explícitamente.'),
        '04_monthly': ('Volumen, importes, distancias, duración y propinas', 'Importe registrado no equivale a utilidad; mediana reduce influencia de extremos. Propinas solo en tarjeta.'),
        '05_hourly': ('Horas de mayor actividad', 'Se interpreta el horario local TLC; no identifica una causa de los patrones.'),
        '06_payments': ('Mezcla de medios de pago', 'Se mantienen todos los códigos; no se asume que tarjeta + efectivo sumen 100%.'),
        '07_distributions': ('Distribución y colas', 'Se reportan mediana, p95 y p99. Los filtros operativos no eliminan necesariamente todos los errores.'),
        '08_common_months': ('Evolución en meses comparables', 'Solo meses presentes en ambos taxis y todos los años seleccionados; evita sesgo de año parcial.'),
        '09_weekday': ('Actividad por día de semana', 'Se divide por los días observados con viajes válidos; no demuestra cobertura de días sin viajes.'),
        '10_distance_bins': ('Composición de distancias', 'Las bandas usan millas y provienen de viajes válidos.'),
        '11_outliers': ('Casos extremos sin filtrar', 'No se declara fraude; son ejemplos para revisar, no datos corregidos automáticamente.')}
    document = [f'# Consultas y resultados: {args.stage}',
        'Fuente: Parquet oficiales listados en `metadata.json`. Ninguna consulta requiere importación previa.',
        'Transformación y población: `sql/00_views.sql`; normalización: `scripts/common.py`.',
        '## Esquemas originales', markdown(unique, 80)]
    for path in sorted((ROOT / 'sql').glob('[0-9][0-9]_*.sql')):
        if path.name == '00_views.sql':
            continue
        print(f'{args.stage}: {path.name}', flush=True)
        start = time.perf_counter()
        result = con.sql(path.read_text()).df()
        elapsed = time.perf_counter() - start
        result.to_csv(out / f'{path.stem}.csv', index=False)
        title, decision = descriptions[path.stem]
        metadata['queries'][path.name] = dict(seconds=elapsed, result_rows=len(result))
        document += [f'## {path.stem}: {title}', f'**Objetivo:** {title}.',
            '**Fuentes:** todos los archivos Parquet incluidos en `metadata.json`, con la población indicada en SQL.',
            '```sql\n' + path.read_text().strip() + '\n```',
            '**Resultado** (primeras 40 filas; CSV contiene el resultado completo):', markdown(result),
            '**Decisión e interpretación:** ' + decision]
    (out / 'metadata.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + '\n')
    (out / 'queries.md').write_text('\n\n'.join(document) + '\n')
    # Snapshot de lectura para Metabase: tablas pequeñas, sin bloqueo del DB de benchmark.
    if args.stage == 'final':
        db = ROOT / 'data/processed/dashboard.duckdb'
        with connect(db) as dash:
            for path in sorted(out.glob('[0-9][0-9]_*.csv')):
                name = path.stem.split('_', 1)[1]
                dash.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM read_csv_auto('{sqlstr(str(path))}', sample_size=-1)")
            dash.execute('CHECKPOINT')
    con.close()
    print(f'Resultados: {out}', flush=True)


if __name__ == '__main__':
    main()
