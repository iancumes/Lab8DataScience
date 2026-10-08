#!/usr/bin/env python3
"""Comprueba requisitos con evidencia real y detecta pérdida/alteración de datos."""
import json
import subprocess
import pandas as pd
import nbformat
from common import ROOT
from download_data import inspect_file


def main():
    stages = ['initial_2026','expanded_2024_2026','final','rerun']
    previous = {}
    findings = {}
    for stage in stages:
        report = json.loads((ROOT / f'docs/manifests/{stage}.json').read_text())
        assert report['complete_for_published'] and not report['historical_missing'], stage
        records = report['records']
        current = {r['file']:r for r in records}
        for name, old in previous.items():
            assert name in current and current[name]['sha256']==old['sha256'], (stage,name)
            assert current[name]['status']=='existing', (stage,name,'se volvió a descargar')
        findings[stage] = dict(files=len(records),rows=sum(r['rows'] for r in records),
            downloaded=sum(r['status']=='downloaded' for r in records),existing=sum(r['status']=='existing' for r in records))
        previous = current
    # Verifica la versión en disco frente al último manifiesto, no solo entre JSON.
    for name, record in previous.items():
        actual = inspect_file(ROOT / 'data/raw' / name)
        assert actual['sha256']==record['sha256'] and actual['rows']==record['rows'], name
    inventory = pd.read_csv(ROOT / 'docs/results/final/01_inventory.csv')
    assert int(inventory.rows.sum())==findings['final']['rows']
    quality = pd.read_csv(ROOT / 'docs/results/final/03_quality.csv')
    monthly = pd.read_csv(ROOT / 'docs/results/final/04_monthly.csv')
    assert int(monthly.trips.sum())==int(quality.rows.sum()-quality.excluded.sum())
    timing = pd.read_csv(ROOT / 'docs/benchmarks/timings.csv')
    assert timing.results_match.all() and timing.scale.nunique()==4 and timing['query'].nunique()==4
    assert timing.groupby(['scale','query','mode']).size().min() >= 3
    dash = json.loads((ROOT / 'docs/dashboard.json').read_text())
    assert len(dash['cards'])>=6 and all(c['verified_rows']>0 for c in dash['cards'])
    nb = nbformat.read(ROOT / 'notebooks/lab8_duckdb.ipynb',as_version=4)
    for cell in nb.cells:
        if cell.cell_type=='code':
            assert cell.execution_count is not None
            assert not any(o.output_type=='error' for o in cell.outputs)
    tracked = subprocess.check_output(['git','-c','safe.directory='+str(ROOT),'ls-files'],cwd=ROOT,text=True).splitlines()
    assert not any(p.endswith(('.parquet','.duckdb','.part','.wal')) for p in tracked)
    assert '.env' not in tracked
    (ROOT / 'docs/verification.json').write_text(json.dumps(dict(passed=True,stages=findings,
        raw_hashes_verified=len(previous),benchmark_runs=len(timing),dashboard_cards=len(dash['cards']),
        notebook_executed=True,no_raw_data_in_git=True),indent=2)+'\n')
    print(json.dumps(findings,indent=2))
    print('Verificación completa: datos, etapas, benchmark, indicadores y notebook.')


if __name__=='__main__':
    main()
