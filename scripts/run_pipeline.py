#!/usr/bin/env python3
"""Reproduce el orden pedagógico: 2026 -> +2024 -> +2025, luego benchmarks."""
import argparse
import subprocess
import sys
from common import ROOT


def run(*arguments):
    subprocess.run([sys.executable, *arguments], cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-download', action='store_true')
    parser.add_argument('--skip-benchmark', action='store_true')
    args = parser.parse_args()
    for stage, years in [('initial_2026', [2026]), ('expanded_2024_2026', [2024, 2026]), ('final', [2024, 2025, 2026])]:
        if not args.skip_download:
            run('scripts/download_data.py', '--years', *map(str, years), '--manifest', f'docs/manifests/{stage}.json')
        run('scripts/analyze.py', '--years', *map(str, years), '--stage', stage)
    if not args.skip_benchmark:
        run('scripts/benchmark.py')
    run('scripts/report.py')
    run('scripts/create_notebook.py')


if __name__ == '__main__':
    main()
