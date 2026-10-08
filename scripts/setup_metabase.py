#!/usr/bin/env python3
"""Crea o actualiza diez tarjetas SQL y un tablero Metabase local."""
import argparse
import json
import os
import secrets
from pathlib import Path
import requests
from common import ROOT

SPECS = [
 ('01_volume', 'Viajes válidos mensuales', 'trips', 'Viajes',
  'Volumen mensual por tipo. La escala log permite observar green; 2026 es parcial.'),
 ('02_revenue', 'Importe total registrado', 'total_usd', 'USD',
  'Suma de total_amount en viajes válidos. Incluye cargos; no representa utilidad.'),
 ('03_ticket', 'Ticket medio mensual', 'avg_total_usd', 'USD/viaje',
  'Importe medio por viaje válido. Cambios de composición y valores extremos afectan la media.'),
 ('04_distance', 'Distancia típica mensual', 'median_miles', 'Millas',
  'Mediana de distancia en viajes válidos. Comparar con las colas p95/p99 del informe.'),
 ('05_duration', 'Duración típica mensual', 'median_minutes', 'Minutos',
  'Mediana de duración en viajes válidos, limitada a 180 minutos por regla operativa.'),
 ('06_credit', 'Participación de tarjeta', 'credit_pct', '% de viajes',
  'Porcentaje de viajes válidos con payment_type=1. Otros códigos no equivalen automáticamente a efectivo.'),
 ('07_tips', 'Propinas registradas en tarjeta', 'card_tip_pct', '% de tarifa en tarjeta',
  '100 × suma(propina)/suma(tarifa), solo tarjeta y propina no negativa. No mide propinas en efectivo.'),
]


def credentials():
    env_file = ROOT / '.env'
    stored = {}
    if env_file.exists():
        stored = dict(line.split('=',1) for line in env_file.read_text().splitlines() if '=' in line and not line.startswith('#'))
    email = os.environ.get('MB_ADMIN_EMAIL', stored.get('MB_ADMIN_EMAIL', 'lab8@example.com'))
    password = os.environ.get('MB_ADMIN_PASSWORD', stored.get('MB_ADMIN_PASSWORD'))
    if not password:
        password = secrets.token_urlsafe(24) + 'Aa1!'
        env_file.write_text(f'MB_ADMIN_EMAIL={email}\nMB_ADMIN_PASSWORD={password}\n')
        env_file.chmod(0o600)
    return email, password


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://localhost:3000')
    parser.add_argument('--init-only', action='store_true')
    args = parser.parse_args()
    client = requests.Session()
    def api(method, path, **kwargs):
        response = client.request(method, args.url + '/api' + path, timeout=180, **kwargs)
        if not response.ok:
            raise RuntimeError(f'Metabase {method} {path}: {response.status_code} {response.text[:1500]}')
        return response.json() if response.content else None
    email, password = credentials()
    properties = api('GET', '/session/properties')
    if properties.get('setup-token'):
        api('POST', '/setup', json={'token': properties['setup-token'],
            'user': {'first_name':'Equipo', 'last_name':'Lab8', 'email':email, 'password':password},
            'prefs': {'site_name':'Laboratorio 8 - DuckDB', 'allow_tracking':False}})
    session = api('POST', '/session', json={'username':email, 'password':password})
    client.headers.update({'X-Metabase-Session':session['id']})
    if args.init_only:
        print('Metabase inicializado. Credenciales locales en .env (no versionadas).')
        return
    if not (ROOT / 'data/processed/dashboard.duckdb').exists():
        raise FileNotFoundError('Ejecute analyze.py --stage final primero')
    saved_path = ROOT / 'docs/dashboard.json'
    saved = json.loads(saved_path.read_text()) if saved_path.exists() else {}
    databases = api('GET','/database')['data']
    existing = next((d for d in databases if d['name']=='Lab8 DuckDB - indicadores'), None)
    details = dict(database_file='/workspace/data/processed/dashboard.duckdb', read_only=True, memory_limit='1GB')
    if existing:
        db = api('PUT', f'/database/{existing["id"]}', json=dict(name=existing['name'],engine='duckdb',details=details))
    else:
        db = api('POST', '/database', json=dict(name='Lab8 DuckDB - indicadores', engine='duckdb', details=details))
    db_id = db['id']
    specifications = []
    for slug, name, metric, unit, description in SPECS:
        sql = f"SELECT period, taxi, {metric} AS value FROM monthly ORDER BY period, taxi;"
        settings = {'graph.dimensions':['period','taxi'], 'graph.metrics':['value'],
                    'graph.x_axis.title_text':'Mes', 'graph.y_axis.title_text':unit,
                    'graph.colors':['#008477','#b57900']}
        if metric in ('trips','total_usd'):
            settings['graph.y_axis.scale'] = 'log'
            settings['graph.y_axis.auto_range'] = False
            settings['graph.y_axis.min'] = 10000 if metric=='trips' else 500000
            settings['graph.y_axis.max'] = 10000000 if metric=='trips' else 200000000
        specifications.append(dict(slug=slug,name=name,description=description,sql=sql,settings=settings,display='line'))
    specifications += [
        dict(slug='08_hourly',name='Perfil horario por año y tipo',
             description='Participación horaria dentro de cada año/taxi. Normalizar evita confundir meses de exposición con comportamiento horario.',
             sql="SELECT hour, taxi || ' ' || year::VARCHAR AS series, round(100.0*trips/sum(trips) OVER (PARTITION BY taxi,year),3) AS value FROM hourly ORDER BY hour, series;",
             settings={'graph.dimensions':['hour','series'],'graph.metrics':['value'],'graph.x_axis.title_text':'Hora local NYC','graph.y_axis.title_text':'% de viajes por año/tipo','graph.colors':['#48b0a4','#008477','#00594f','#e7be5f','#b57900','#765100']},display='line'),
        dict(slug='09_quality',name='Exclusión por calidad',
             description='Porcentaje de filas que incumplen al menos una regla operativa. Los motivos se solapan; no se suman. No todo viaje excluido es falso.',
             sql='SELECT source_year::VARCHAR AS year, taxi, excluded_pct AS value FROM quality ORDER BY year, taxi;',
             settings={'graph.dimensions':['year','taxi'],'graph.metrics':['value'],'graph.y_axis.title_text':'% de filas originales','graph.colors':['#008477','#b57900']},display='bar'),
        dict(slug='10_evolution',name='Demanda en meses comparables',
             description='Conteo de viajes válidos solo en meses presentes en ambos taxis y todos los años. No extrapola el resto de 2026.',
             sql='SELECT year::VARCHAR AS year, taxi, trips AS value FROM common_months ORDER BY year, taxi;',
             settings={'graph.dimensions':['year','taxi'],'graph.metrics':['value'],'graph.y_axis.scale':'log','graph.y_axis.title_text':'Viajes válidos (log)','graph.colors':['#008477','#b57900'],'graph.y_axis.auto_range':False,'graph.y_axis.min':100000,'graph.y_axis.max':100000000},display='bar')]
    cards = []
    (ROOT / 'sql/dashboard').mkdir(parents=True, exist_ok=True)
    for spec in specifications:
        (ROOT / 'sql/dashboard' / f'{spec["slug"]}.sql').write_text('-- ' + spec['description'] + '\n' + spec['sql'] + '\n')
        dataset = {'database':db_id,'type':'native','native':{'query':spec['sql'],'template-tags':{}}}
        # Comprueba la consulta antes de crear una tarjeta: no basta con que el API acepte guardarla.
        result = api('POST','/dataset',json=dataset)
        if result.get('status') != 'completed' or not result.get('data',{}).get('rows'):
            raise RuntimeError(f'Consulta falló o está vacía: {spec["slug"]}: {result.get("error")}')
        body = dict(name=spec['name'],description=spec['description'],dataset_query=dataset,
                    display=spec['display'],visualization_settings=spec['settings'])
        old = next((c for c in saved.get('cards',[]) if c['slug']==spec['slug']), None)
        if old and client.get(args.url+f'/api/card/{old["id"]}',timeout=30).ok:
            card = api('PUT',f'/card/{old["id"]}',json=body)
        else:
            card = api('POST','/card',json=body)
        cards.append(dict(slug=spec['slug'],id=card['id'],name=spec['name'],sql=spec['sql'],
                          description=spec['description'],verified_rows=len(result['data']['rows'])))
    dashboard_body = dict(name='Lab 8 - NYC TLC | 2024-2026 (2026 parcial)',
        description='10 indicadores DuckDB. 2026 parcial. Viajes válidos según reglas documentadas; USD nominales. Comparación anual con meses comunes.',parameters=[])
    old_id = saved.get('dashboard_id')
    if old_id and client.get(args.url+f'/api/dashboard/{old_id}',timeout=30).ok:
        dashboard = api('PUT',f'/dashboard/{old_id}',json=dashboard_body)
    else:
        dashboard = api('POST','/dashboard',json=dashboard_body)
    dash_id = dashboard['id']
    dashcards = [dict(id=-(i+1),card_id=c['id'],row=(i//2)*5,col=(i%2)*12,size_x=12,size_y=5,
                      parameter_mappings=[],visualization_settings={}) for i,c in enumerate(cards)]
    api('PUT',f'/dashboard/{dash_id}',json={'dashcards':dashcards})
    final = api('GET', f'/dashboard/{dash_id}')
    if len(final.get('dashcards',[])) != len(cards):
        raise AssertionError('El tablero no contiene las diez tarjetas')
    saved_path.write_text(json.dumps(dict(database_id=db_id,dashboard_id=dash_id,
        url=f'{args.url}/dashboard/{dash_id}',cards=cards,read_only=True),indent=2,ensure_ascii=False)+'\n')
    print(f'Tablero verificado: {args.url}/dashboard/{dash_id}; 10 consultas con resultados.')


if __name__ == '__main__':
    main()
