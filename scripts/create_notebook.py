#!/usr/bin/env python3
"""Crea y ejecuta un notebook con consultas directas y resultados del laboratorio."""
import os
import sys
import json
import nbformat as nbf
from nbclient import NotebookClient
from common import ROOT


def main():
    nb = nbf.v4.new_notebook()
    md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
    nb.cells = [md('# Laboratorio 8 - DuckDB\n\n'
        'Javier Valladares, 23045\n\nIan Cumes, 23236\n\nJavier Cifuentes, 23079\n\n'
        'Análisis reproducible NYC TLC. '
        'Ejecute primero `scripts/run_pipeline.py`. Los datos originales permanecen en Parquet. '
        'El informe y las reglas de calidad están en `docs/`.'),
        code("from pathlib import Path\nimport sys\nROOT = Path.cwd()\nif ROOT.name == 'notebooks':\n    ROOT = ROOT.parent\nsys.path.insert(0, str(ROOT / 'scripts'))\nfrom common import connect, create_views, query\nimport pandas as pd\nfrom IPython.display import display, Image\ncon = connect()\ncreate_views(con)"),
        md('## Ejercicio 3: archivos, filas, columnas y muestra'),
        code("display(con.sql(query('01_inventory.sql')).df())\ndisplay(con.sql('DESCRIBE trips_raw').df())\ndisplay(con.sql(query('02_sample.sql')).df())"),
        md('## Calidad de datos\nLos motivos se solapan; `excluded` es la unión. Las filas originales se conservan.'),
        code("display(con.sql(query('03_quality.sql')).df())"),
        md('## Ejercicios 4, 7 y 8: indicadores y evolución\nLas 13 preguntas justificadas están en `docs/metodologia.md`. '
           'La comparación anual usa meses comunes, pues 2026 es parcial.'),
        code("monthly = con.sql(query('04_monthly.sql')).df()\ndisplay(monthly.head(12))\ndisplay(con.sql(query('08_common_months.sql')).df())"),
        code("display(Image(filename=str(ROOT / 'docs/figures/indicadores.png')))\ndisplay(Image(filename=str(ROOT / 'docs/figures/perfil_horario.png')))"),
        md('## Ejercicio 6: benchmark medido\nMisma proyección y SQL, caché caliente, tres repeticiones. '
           'Resultados equivalentes verificados en cada repetición. CTAS reportado aparte.'),
        code("display(pd.read_csv(ROOT / 'docs/benchmarks/materialization.csv'))\ndisplay(pd.read_csv(ROOT / 'docs/benchmarks/summary.csv'))"),
        md('## Discusión\nConsulte `docs/informe.md` para los hallazgos numéricos y respuestas 9.1 a 9.8. '
           'El tablero interactivo se reconstruye con `scripts/setup_metabase.py`.'), code('con.close()')]
    # Kernel temporal apunta al intérprete que generó el notebook, sin instalar globalmente.
    kernel = ROOT / 'tmp/jupyter/kernels/lab8'
    kernel.mkdir(parents=True, exist_ok=True)
    (kernel / 'kernel.json').write_text(json.dumps(dict(argv=[sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
        display_name='Lab8', language='python')))
    os.environ['JUPYTER_PATH'] = str(ROOT / 'tmp/jupyter') + os.pathsep + os.environ.get('JUPYTER_PATH', '')
    NotebookClient(nb, timeout=1200, kernel_name='lab8', resources={'metadata': {'path': str(ROOT)}}).execute()
    nb.metadata.kernelspec = dict(name='python3', display_name='Python 3', language='python')
    nbf.write(nb, ROOT / 'notebooks/lab8_duckdb.ipynb')
    print('Notebook ejecutado sin errores', flush=True)


if __name__ == '__main__':
    main()
