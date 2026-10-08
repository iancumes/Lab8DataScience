#!/usr/bin/env python3
"""Mismas consultas, mismos datos; caché caliente, orden alternado, resultados validados."""
import argparse
import json
import math
import platform
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
import duckdb
import pandas as pd
from common import ROOT, connect, files, source_sql


def equivalent(a, b):
    if len(a) != len(b):
        return False
    for row_a, row_b in zip(a, b):
        if len(row_a) != len(row_b):
            return False
        for x, y in zip(row_a, row_b):
            if isinstance(x, (float, Decimal)) and isinstance(y, (float, Decimal)):
                if not math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-6):
                    return False
            elif x != y:
                return False
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repeats', type=int, default=3)
    args = parser.parse_args()
    if args.repeats < 2:
        parser.error('Use al menos dos repeticiones')
    out = ROOT / 'docs/benchmarks'
    out.mkdir(parents=True, exist_ok=True)
    all_paths = files()
    current = [p for p in all_paths if p.parent.name == '2026']
    first_month = min(int(p.stem[-2:]) for p in current)
    scales = [('2026_one_month', [p for p in current if int(p.stem[-2:]) == first_month]),
              ('2026', current), ('2024_2026', [p for p in all_paths if p.parent.name != '2025']),
              ('2024_2025_2026', all_paths)]
    timings, builds = [], []
    database = ROOT / 'data/processed/materialized.duckdb'
    for scale, selected in scales:
        # Solo se borran artefactos generados por este script; nunca los Parquet.
        database.unlink(missing_ok=True)
        Path(str(database) + '.wal').unlink(missing_ok=True)
        con = connect(database)
        con.execute('CREATE VIEW parquet_source AS ' + source_sql(selected))
        start = time.perf_counter()
        con.execute('CREATE TABLE trips_materialized AS SELECT * FROM parquet_source')
        con.execute('CHECKPOINT')
        build_seconds = time.perf_counter() - start
        count = con.execute('SELECT count(*) FROM trips_materialized').fetchone()[0]
        builds.append(dict(scale=scale, files=len(selected), rows=count,
                           materialization_seconds=build_seconds, database_bytes=database.stat().st_size,
                           parquet_bytes=sum(p.stat().st_size for p in selected)))
        print(f'{scale}: {count:,} filas; materialización {build_seconds:.2f}s', flush=True)
        for path in sorted((ROOT / 'sql/benchmarks').glob('*.sql')):
            templates = {mode: path.read_text().replace('{source}', source)
                         for mode, source in [('parquet', 'parquet_source'), ('duckdb', 'trips_materialized')]}
            # Calentamiento fuera del cronómetro; materializar no se oculta en el reporte.
            expected = con.execute(templates['parquet']).fetchall()
            actual = con.execute(templates['duckdb']).fetchall()
            if not equivalent(expected, actual):
                raise AssertionError(f'Resultados distintos: {scale}/{path.stem}')
            for repeat in range(args.repeats):
                order = ['parquet', 'duckdb'] if repeat % 2 == 0 else ['duckdb', 'parquet']
                for mode in order:
                    start = time.perf_counter()
                    result = con.execute(templates[mode]).fetchall()
                    seconds = time.perf_counter() - start
                    if not equivalent(expected, result):
                        raise AssertionError(f'Resultado no estable: {scale}/{path.stem}/{mode}')
                    timings.append(dict(scale=scale, files=len(selected), rows=count, query=path.stem,
                                        mode=mode, repeat=repeat+1, seconds=seconds, results_match=True))
            print(f'  {path.stem}: resultados equivalentes', flush=True)
            pd.DataFrame(timings).to_csv(out / 'timings.csv', index=False)
        con.execute('DROP VIEW parquet_source')  # no guardar rutas locales en la tabla materializada
        con.close()
    timing_frame = pd.DataFrame(timings)
    summary = timing_frame.groupby(['scale', 'files', 'rows', 'query', 'mode'], sort=False).seconds.agg(['median', 'min', 'max']).reset_index()
    summary.to_csv(out / 'summary.csv', index=False)
    pd.DataFrame(builds).to_csv(out / 'materialization.csv', index=False)
    (out / 'environment.json').write_text(json.dumps(dict(
        generated_at_utc=datetime.now(timezone.utc).isoformat(), duckdb=duckdb.__version__,
        python=platform.python_version(), platform=platform.platform(), threads=4, memory_limit='3GB',
        repeats=args.repeats, cache='warm; no se vacía caché del sistema operativo',
        methodology='Una conexión por escala; calentamiento de ambas rutas; orden alternado; fetchall incluido; CTAS medido aparte.',
        results_verified=True), indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
