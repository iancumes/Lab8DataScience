#!/usr/bin/env python3
"""Interpreta resultados calculados y crea evidencia gráfica estática."""
import json
import math
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import ROOT
from analyze import markdown

COLORS = {'yellow': '#b57900', 'green': '#008477'}
LABELS = {'yellow': 'Amarillo', 'green': 'Verde'}


def load(name, stage='final'):
    return pd.read_csv(ROOT / 'docs/results' / stage / f'{name}.csv')


def observations(stage):
    monthly = load('04_monthly', stage)
    quality = load('03_quality', stage)
    hourly = load('05_hourly', stage)
    text = []
    totals = monthly.groupby('taxi').trips.sum()
    text.append(f'**Escala del servicio.** Se observan {totals["yellow"]:,} viajes válidos amarillos y '
                f'{totals["green"]:,} verdes: razón {totals["yellow"]/totals["green"]:.1f}:1. '
                'Una visualización con escala única lineal ocultaría las variaciones de green.')
    for taxi in ['yellow', 'green']:
        group = monthly[monthly.taxi == taxi]
        ticket = group.total_usd.sum() / group.trips.sum()
        peak = hourly[hourly.taxi == taxi].groupby('hour').trips.sum().idxmax()
        text.append(f'**Ticket y horario ({LABELS[taxi]}).** El importe medio ponderado por viaje es '
                    f'USD {ticket:.2f}; la hora con mayor conteo es {int(peak):02d}:00. '
                    'Es una asociación descriptiva y agrega meses de distinta exposición.')
    excluded = int(quality.excluded.sum())
    rows = int(quality.rows.sum())
    text.append(f'**Calidad.** Se excluyen {excluded:,} de {rows:,} filas ({100*excluded/rows:.2f}%). '
                'Los conteos originales permanecen disponibles y los motivos pueden solaparse. '
                'El análisis describe la población filtrada y no todos los viajes registrados.')
    text.append(f'**Fechas y faltantes.** Se detectan {int(quality.bad_date.sum()):,} filas con pickup fuera del mes/año del archivo o nulo y {int(quality.missing_passengers.sum()):,} filas sin passenger_count. El año analítico proviene del archivo y se valida contra pickup; no se imputan pasajeros.')
    return text


def main():
    figures = ROOT / 'docs/figures'
    figures.mkdir(parents=True, exist_ok=True)
    monthly = load('04_monthly')
    monthly['period'] = pd.to_datetime(monthly.period)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'axes.spines.top': False,
                         'axes.spines.right': False, 'font.size': 10})
    fig, axes = plt.subplots(3, 3, figsize=(18, 13), layout='constrained')
    metrics = [('trips', 'Viajes válidos por mes', 'Viajes (log)', True),
               ('total_usd', 'Importe registrado por mes', 'USD (log)', True),
               ('avg_total_usd', 'Ticket medio', 'USD/viaje', False),
               ('median_miles', 'Distancia mediana', 'Millas', False),
               ('median_minutes', 'Duración mediana', 'Minutos', False),
               ('credit_pct', 'Pago con tarjeta', '% de viajes', False),
               ('card_tip_pct', 'Propina registrada en tarjeta', '% de tarifa en tarjeta', False)]
    for ax, (metric, title, ylabel, log) in zip(axes.flat, metrics):
        for taxi, group in monthly.groupby('taxi'):
            ax.plot(group.period, group[metric], color=COLORS[taxi], label=LABELS[taxi], lw=2)
        ax.set(title=title, ylabel=ylabel)
        if log:
            ax.set_yscale('log')
        ax.grid(alpha=0.18)
        ax.tick_params(axis='x', rotation=35, labelsize=8)
        ax.legend(frameon=False, fontsize=8)
    quality = load('03_quality')
    ax = axes.flat[7]
    for i, taxi in enumerate(['yellow', 'green']):
        sub = quality[quality.taxi == taxi]
        ax.bar(sub.source_year + (i-.5)*.3, sub.excluded_pct, width=.3,
               color=COLORS[taxi], label=LABELS[taxi])
    ax.set(title='Filas excluidas por reglas analíticas', ylabel='% de filas originales', xticks=[2024, 2025, 2026])
    ax.legend(frameon=False)
    common = load('08_common_months')
    ax = axes.flat[8]
    for i, taxi in enumerate(['yellow', 'green']):
        sub = common[common.taxi == taxi]
        ax.bar(sub.year + (i-.5)*.3, sub.trips, width=.3, color=COLORS[taxi], label=LABELS[taxi])
    ax.set(title=f'Volumen comparable: {int(common.months.min())} meses/año', ylabel='Viajes (log)',
           xticks=[2024, 2025, 2026], yscale='log')
    ax.legend(frameon=False)
    fig.suptitle('NYC TLC | DuckDB | 2024, 2025 y 2026 parcial\nIndicadores de viajes válidos; USD nominales; escala log donde se indica', fontsize=18)
    fig.savefig(figures / 'indicadores.png', dpi=150)
    plt.close(fig)
    hourly = load('05_hourly')
    fig, axes = plt.subplots(1, 2, figsize=(13, 4), layout='constrained')
    for ax, taxi in zip(axes, ['yellow', 'green']):
        sub = hourly[hourly.taxi == taxi]
        for year, group in sub.groupby('year'):
            # Distribución relativa evita confundir número de meses con horario.
            ax.plot(group.hour, 100*group.trips/group.trips.sum(), label=str(year), lw=2)
        ax.set(title=f'Perfil horario - {LABELS[taxi]}', xlabel='Hora local NYC', ylabel='% del total anual válido', xticks=range(0,24,3))
        ax.legend(frameon=False)
        ax.grid(alpha=.2)
    fig.savefig(figures / 'perfil_horario.png', dpi=150)
    plt.close(fig)
    document = ['# Informe de resultados - Laboratorio 8',
        'Javier Valladares, 23045\n\nIan Cumes, 23236\n\nJavier Cifuentes, 23079',
        'Resultados calculados sobre datos oficiales; fecha exacta, archivos y versiones en los manifiestos y metadata.json. '
        'Las preguntas y reglas están en [metodologia.md](metodologia.md).',
        '## Ejercicios 3 y 4: exploración directa y hallazgos iniciales',
        markdown(load('01_inventory', 'initial_2026')),
        *observations('initial_2026'),
        'Las consultas, objetivos, fuentes, resultados y decisiones de esta etapa están en '
        '[results/initial_2026/queries.md](results/initial_2026/queries.md).',
        '## Ejercicio 5: incorporación de 2024', markdown(load('01_inventory', 'expanded_2024_2026')),
        'Las mismas consultas se ejecutaron sin cambiar su lógica; se amplió únicamente la lista de años. '
        'La normalización tpep/lpep y union_by_name resuelven nombres/columnas diferentes. '
        'El manifiesto expanded muestra los registros de 2026 como existing y los de 2024 como downloaded.',
        '## Ejercicio 6: Parquet versus tabla materializada']
    summary = pd.read_csv(ROOT / 'docs/benchmarks/summary.csv')
    builds = pd.read_csv(ROOT / 'docs/benchmarks/materialization.csv')
    comparison = summary.pivot(index=['scale','query'], columns='mode', values='median').reset_index()
    comparison['speedup_parquet_over_duckdb'] = comparison.parquet / comparison.duckdb
    document += [markdown(builds), markdown(comparison),
        'Un cociente mayor que 1 favorece la tabla DuckDB; menor que 1 favorece Parquet. '
        'Los tiempos son de caché caliente y no incorporan descarga. La materialización sí se mide '
        'por separado. No basta con comparar una sola consulta: CTAS y espacio adicional deben amortizarse.']
    last = comparison[comparison.scale == '2024_2025_2026']
    for row in last.itertuples(index=False):
        document.append(f'Para **{row.query}**, la mediana final fue {row.parquet:.4f}s en Parquet y '
                        f'{row.duckdb:.4f}s en tabla (cociente {row.speedup_parquet_over_duckdb:.2f}).')
    saving = (last.parquet-last.duckdb).sum()
    build = builds[builds.scale=='2024_2025_2026'].materialization_seconds.iloc[0]
    if saving > 0:
        document.append(f'Para una ronda secuencial de estas cuatro consultas, la diferencia observada es '
                        f'{saving:.3f}s; amortizar CTAS requeriría aproximadamente {math.ceil(build/saving)} rondas '
                        'bajo condiciones iguales. Es una estimación local, no una garantía.')
    else:
        document.append('La ronda completa no ahorra tiempo al materializar en esta medición; no hay punto de amortización positivo observado.')
    document += ['Parquet conviene para exploración puntual, archivos que llegan continuamente y evitar otra copia. '
                 'Materializar conviene cuando las consultas repetidas compensan CTAS y se necesita un snapshot estable. '
                 'Una tabla requiere refresco explícito; los Parquet nuevos no aparecen automáticamente en ella.',
        '## Ejercicio 7: indicadores y tablero',
        'Las 13 preguntas y justificaciones están en metodologia.md. Las tarjetas de Metabase usan '
        'sql/dashboard/ y agregados calculados con sql/04..10. El script setup_metabase.py reconstruye '
        'el tablero; docs/dashboard.json registra IDs y consultas. Las interpretaciones están en las '
        'descripciones de las tarjetas y se respaldan con estos resultados.',
        '![Indicadores](figures/indicadores.png)', '![Perfil horario](figures/perfil_horario.png)',
        *observations('final'),
        '## Ejercicio 8: evolución de tres años en meses comparables', markdown(common)]
    document.append('### Interpretación numérica de las siete tarjetas mensuales')
    last_year = int(monthly.year.max())
    last_month = int(monthly[monthly.year==last_year].month.max())
    latest = monthly[(monthly.year==last_year) & (monthly.month==last_month)].set_index('taxi')
    for metric, title, unit, log in metrics:
        unit = {'trips':'viajes', 'total_usd':'USD', 'avg_total_usd':'USD/viaje',
                'median_miles':'millas', 'median_minutes':'minutos', 'credit_pct':'%',
                'card_tip_pct':'% de tarifa en tarjeta'}[metric]
        yellow, green = float(latest.loc['yellow',metric]), float(latest.loc['green',metric])
        document.append(f'**{title} ({last_year}-{last_month:02d}):** amarillo {yellow:,.3f} {unit}; '
                        f'verde {green:,.3f} {unit}. ' +
                        ('El mayor volumen explica parte de la diferencia de importe agregado; no equivale a mayor ingreso por conductor.' if metric in ['trips','total_usd'] else
                         'Se compara la población válida del mismo mes; la diferencia es descriptiva y puede reflejar composición de recorridos y pasajeros.'))
    for taxi in ['yellow','green']:
        sub = common[common.taxi==taxi].set_index('year').sort_index()
        pieces = []
        for a,b in [(2024,2025),(2025,2026)]:
            change = 100*(sub.loc[b,'trips']/sub.loc[a,'trips']-1)
            pieces.append(f'{a}→{b}: {change:+.2f}%')
        document.append(f'**Patrón de volumen ({LABELS[taxi]}):** ' + '; '.join(pieces) +
                        f'. Se usan {int(sub.months.min())} meses comunes; no se extrapola al resto de 2026.')
        ticket_change = 100*(sub.loc[2026,'avg_total_usd']/sub.loc[2024,'avg_total_usd']-1)
        credit_change = sub.loc[2026,'credit_pct']-sub.loc[2024,'credit_pct']
        document.append(f'**Ticket y mezcla ({LABELS[taxi]}):** ticket medio USD '
            f'{sub.loc[2024,"avg_total_usd"]:.2f} → {sub.loc[2025,"avg_total_usd"]:.2f} → '
            f'{sub.loc[2026,"avg_total_usd"]:.2f} ({ticket_change:+.2f}% de 2024 a 2026). '
            f'La proporción de tarjeta cambia {credit_change:+.2f} puntos porcentuales. '
            'La comparación es descriptiva: composición, precios y reglas de registro pueden cambiar simultáneamente.')
    document += ['**Cambio de esquema:** cbd_congestion_fee aparece desde 2025 según TLC. '
        'En 2024 el indicador conserva NULL. El ticket nominal incluye cargos y no mide un cambio causal '
        'atribuible al recargo. La evolución por mes y la distribución aportan contexto adicional.',
        '**Interpretación de pagos:** el código 0 identifica viajes Flex Fare, no un instrumento de pago. Una menor proporción de código 1 no demuestra mayor uso de efectivo. total_amount excluye propinas en efectivo según los diccionarios TLC.',
        '## Ejercicio 9: discusión',
        '**9.1. Características útiles.** Lectura directa de Parquet, SQL analítico (ventanas, cuantiles, '
        'agrupaciones), union_by_name, ejecución en proceso y proyección de columnas. No se necesita '
        'administrar un servidor para el análisis.',
        '**9.2. Parquet.** Evita importar y duplicar todos los datos; conserva el formato original. '
        'La proyección y filtros pueden reducir lectura. Como límites, los archivos requieren gestión de '
        'esquemas/particiones y consultas repetidas pueden volver a decodificar columnas. COUNT puede '
        'aprovechar metadatos, por eso se incluyeron otras consultas en el benchmark.',
        '**9.3. Tablas materializadas.** Ofrecen una copia normalizada estable y pueden acelerar consultas '
        'repetidas según la medición. Cuestan tiempo CTAS y espacio; requieren actualización e invalidación. '
        'Un archivo DuckDB no admite varios procesos escritores simultáneos. Metabase usa otro archivo '
        'de agregados con conexión de solo lectura.',
        '**9.4. Frente a cargar todo en Pandas.** DuckDB procesa y agrega columnas antes de convertir el '
        'resultado a DataFrame y puede ejecutar fuera de memoria con disco temporal. En este trabajo Pandas '
        'recibe tablas pequeñas de resultados. No se midió un benchmark contra Pandas ni se afirma que '
        'DuckDB sea siempre más rápido.',
        '**9.5. Incorporación.** Descubrimiento de rutas, años parametrizados, catálogo oficial, omisión '
        'con validación de archivos existentes, normalización y consultas sin lista fija de meses. La vista '
        'se reconstruye al ejecutar el análisis; la tabla/snapshot se regenera explícitamente.',
        '**9.6. Producción.** Automatizar catálogo, descarga, manifiestos/versionado, validaciones, alertas '
        'de cambios de esquema, ejecución de SQL, refresco del snapshot y pruebas de resultados. Una '
        'planificación debe respetar reintentos, consistencia y bloqueo de lectores/escritores.',
        '**9.7. Reproducibilidad.** Fork y commits por hitos, dependencias directas fijadas, Docker, rutas '
        'relativas al proyecto, SQL versionado, hashes de entradas, manifiestos de etapas, reglas de limpieza '
        'explícitas, metadatos del benchmark y evidencia del tablero. Las dependencias transitivas y '
        'las imágenes base con tag aún pueden cambiar; no se promete reproducción byte a byte.',
        '**9.8. Aprendizaje con escala.** Separar datos de código, medir costo de importar frente a consultar, '
        'reducir columnas antes de mover datos a Python y cuidar espacio temporal se vuelven necesarios. '
        'Las fechas anómalas y esquemas que cambian se hacen visibles al unir muchos archivos. '
        'Medir una consulta pequeña o cargar una muestra no permite inferir el desempeño del conjunto completo.']
    (ROOT / 'docs/informe.md').write_text('\n\n'.join(document) + '\n')


if __name__ == '__main__':
    main()
