"""Lectura normalizada: mismo esquema lógico para todos los años y taxis."""
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]


def connect(database=':memory:', read_only=False):
    con = duckdb.connect(str(database), read_only=read_only)
    con.execute("SET threads=4")
    con.execute("SET memory_limit='3GB'")
    con.execute(f"SET temp_directory='{sqlstr(str(ROOT / 'data/processed/tmp'))}'")
    return con


def sqlstr(value):
    return value.replace("'", "''")


def files(years=None, months=None):
    result = sorted((ROOT / 'data/raw').glob('*/*/*.parquet'))
    if years:
        result = [p for p in result if int(p.parent.name) in years]
    if months:
        result = [p for p in result if int(p.stem[-2:]) in months]
    if not result:
        raise FileNotFoundError('Descargue primero los archivos con scripts/download_data.py')
    return result


def source_sql(paths):
    parts = []
    for kind, prefix in [('yellow', 'tpep'), ('green', 'lpep')]:
        selected = [p for p in paths if p.parent.parent.name == kind]
        if not selected:
            continue
        literals = ','.join("'" + sqlstr(str(p)) + "'" for p in selected)
        # union_by_name tolera cambios de columnas entre 2024, 2025 y 2026.
        reader = f'read_parquet([{literals}], union_by_name=true, filename=true)'
        names = {r[0].lower() for r in duckdb.sql(f'DESCRIBE SELECT * FROM {reader}').fetchall()}
        cbd = 'cbd_congestion_fee::DOUBLE' if 'cbd_congestion_fee' in names else 'NULL::DOUBLE'
        parts.append(f"""SELECT '{kind}' AS taxi,
          regexp_extract(filename, '_(\\d{{4}})-', 1)::INTEGER AS source_year,
          regexp_extract(filename, '-(\\d{{2}})\\.parquet', 1)::INTEGER AS source_month,
          filename AS source_file, VendorID::BIGINT AS vendor_id,
          {prefix}_pickup_datetime::TIMESTAMP AS pickup,
          {prefix}_dropoff_datetime::TIMESTAMP AS dropoff,
          passenger_count::DOUBLE AS passenger_count, trip_distance::DOUBLE AS trip_distance,
          PULocationID::INTEGER AS pu_location_id, DOLocationID::INTEGER AS do_location_id,
          payment_type::INTEGER AS payment_type, RatecodeID::DOUBLE AS ratecode_id,
          fare_amount::DOUBLE AS fare_amount, tip_amount::DOUBLE AS tip_amount,
          total_amount::DOUBLE AS total_amount, tolls_amount::DOUBLE AS tolls_amount,
          congestion_surcharge::DOUBLE AS congestion_surcharge, {cbd} AS cbd_congestion_fee
          FROM {reader}""")
    return '\nUNION ALL\n'.join(parts)


def create_views(con, paths=None):
    paths = files() if paths is None else paths
    con.execute('CREATE OR REPLACE VIEW trips_raw AS ' + source_sql(paths))
    con.execute((ROOT / 'sql/00_views.sql').read_text())


def query(name):
    return (ROOT / 'sql' / name).read_text()
