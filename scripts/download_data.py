#!/usr/bin/env python3
"""Descarga incremental y verificable de Parquet oficiales de NYC TLC."""
import argparse
import hashlib
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page'
BASE = 'https://d37ci6vzurychx.cloudfront.net/trip-data'


def session():
    client = requests.Session()
    client.headers.update({'User-Agent': 'Mozilla/5.0 (compatible; Lab8-TLC/1.0)'})
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    client.mount('https://', HTTPAdapter(max_retries=retry))
    return client


def inspect_file(path):
    """Verifica el footer; un archivo no vacío también puede estar truncado."""
    metadata = pq.read_metadata(path)
    if metadata.num_rows <= 0:
        raise ValueError(f'Parquet sin registros: {path}')
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return {'bytes': path.stat().st_size, 'rows': metadata.num_rows,
            'sha256': digest.hexdigest()}


def download_one(task):
    kind, year, month, dest = task
    name = f'{kind}_tripdata_{year}-{month:02d}.parquet'
    path = dest / kind / str(year) / name
    record = dict(taxi=kind, year=year, month=month, file=str(path.relative_to(dest)),
                  url=f'{BASE}/{name}')
    if path.exists():
        try:
            record.update(inspect_file(path), status='existing')
        except Exception as exc:
            return dict(record, status='error', error=str(exc))
        print(f'OMITIDO {name}', flush=True)
        return record
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.parquet.part')
    for attempt in range(3):
        try:
            with session() as client, client.get(record['url'], stream=True, timeout=(15, 120)) as response:
                response.raise_for_status()
                expected = response.headers.get('Content-Length')
                with temporary.open('wb') as stream:
                    for block in response.iter_content(1024 * 1024):
                        stream.write(block)
                if expected and temporary.stat().st_size != int(expected):
                    raise ValueError('Content-Length no coincide con bytes descargados')
            record.update(inspect_file(temporary), status='downloaded')
            temporary.replace(path)
            print(f'DESCARGADO {name}: {record["rows"]:,} filas', flush=True)
            return record
        except Exception as exc:
            temporary.unlink(missing_ok=True)
            if attempt == 2:
                return dict(record, status='error', error=str(exc))
            time.sleep(attempt + 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--years', '--anios', nargs='+', type=int, default=[2026])
    parser.add_argument('--taxi', choices=['yellow', 'green', 'all'], default='all')
    parser.add_argument('--months', nargs='+', type=int, default=list(range(1, 13)))
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--dest', type=Path, default=ROOT / 'data/raw')
    parser.add_argument('--manifest', type=Path, default=ROOT / 'docs/download_manifest.json')
    args = parser.parse_args()
    if any(m < 1 or m > 12 for m in args.months) or args.workers < 1:
        parser.error('Meses válidos: 1..12; workers debe ser positivo')
    with session() as client:
        response = client.get(SOURCE, timeout=(15, 90))
        response.raise_for_status()
    # El catálogo oficial define publicación; un timeout/403 no equivale a mes ausente.
    published = set((k, int(y), int(m)) for k, y, m in re.findall(
        r'(yellow|green)_tripdata_(\d{4})-(\d{2})\.parquet', response.text))
    if not published:
        raise RuntimeError('El catálogo oficial está vacío o cambió de formato')
    kinds = ['yellow', 'green'] if args.taxi == 'all' else [args.taxi]
    requested = [(k, y, m) for y in sorted(set(args.years)) for k in kinds for m in sorted(set(args.months))]
    tasks = [(*item, args.dest) for item in requested if item in published]
    unavailable = [dict(taxi=k, year=y, month=m) for k, y, m in requested if (k, y, m) not in published]
    historical_missing = [x for x in unavailable if x['year'] < datetime.now(timezone.utc).year]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        records = list(pool.map(download_one, tasks))
    errors = [r for r in records if r['status'] == 'error']
    report = dict(checked_at_utc=datetime.now(timezone.utc).isoformat(), source=SOURCE,
                  requested_years=args.years, requested_months=args.months,
                  records=records, unpublished=unavailable,
                  complete_for_published=not errors, historical_missing=historical_missing)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(dict(published=len(tasks), downloaded=sum(r['status']=='downloaded' for r in records),
                          existing=sum(r['status']=='existing' for r in records),
                          unpublished=len(unavailable), errors=errors), indent=2))
    return int(bool(errors or historical_missing))


if __name__ == '__main__':
    raise SystemExit(main())
