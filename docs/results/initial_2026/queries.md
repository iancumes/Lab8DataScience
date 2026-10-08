# Consultas y resultados: initial_2026

Fuente: Parquet oficiales listados en `metadata.json`. Ninguna consulta requiere importación previa.

Transformación y población: `sql/00_views.sql`; normalización: `scripts/common.py`.

## Esquemas originales

| column | type |
|---|---|
| Airport_fee | double |
| DOLocationID | int32 |
| PULocationID | int32 |
| RatecodeID | int64 |
| VendorID | int32 |
| cbd_congestion_fee | double |
| congestion_surcharge | double |
| ehail_fee | double |
| extra | double |
| fare_amount | double |
| improvement_surcharge | double |
| lpep_dropoff_datetime | timestamp[us] |
| lpep_pickup_datetime | timestamp[us] |
| mta_tax | double |
| passenger_count | int64 |
| payment_type | int64 |
| request_source | large_string |
| store_and_fwd_flag | large_string |
| tip_amount | double |
| tolls_amount | double |
| total_amount | double |
| tpep_dropoff_datetime | timestamp[us] |
| tpep_pickup_datetime | timestamp[us] |
| trip_distance | double |
| trip_type | int64 |

## 01_inventory: Cantidad de archivos y registros

**Objetivo:** Cantidad de archivos y registros.

**Fuentes:** todos los archivos Parquet incluidos en `metadata.json`, con la población indicada en SQL.

```sql
-- Archivos y filas por año/tipo, leyendo Parquet sin importar previamente.
SELECT taxi, source_year, count(DISTINCT source_file) AS files,
       count(*) AS rows, min(pickup) AS earliest_pickup, max(pickup) AS latest_pickup
FROM trips_raw GROUP BY ALL ORDER BY taxi, source_year;
```

**Resultado** (primeras 40 filas; CSV contiene el resultado completo):

| taxi | source_year | files | rows | earliest_pickup | latest_pickup |
|---|---|---|---|---|---|
| green | 2026 | 8 | 337114 | 2008-12-31 17:35:31 | 2026-08-31 23:58:28 |
| yellow | 2026 | 8 | 29703355 | 2001-01-01 09:23:58 | 2026-08-31 23:59:59 |

**Decisión e interpretación:** Se conserva toda fila, incluso fechas fuera de rango; el año de origen viene del nombre del archivo.

## 02_sample: Muestra de registros

**Objetivo:** Muestra de registros.

**Fuentes:** todos los archivos Parquet incluidos en `metadata.json`, con la población indicada en SQL.

```sql
-- Muestra de conveniencia de 10 filas por tipo. No sirve para estimar indicadores.
(SELECT * FROM trips_raw WHERE taxi='yellow' LIMIT 10)
UNION ALL
(SELECT * FROM trips_raw WHERE taxi='green' LIMIT 10);
```

**Resultado** (primeras 40 filas; CSV contiene el resultado completo):

| taxi | source_year | source_month | source_file | vendor_id | pickup | dropoff | passenger_count | trip_distance | pu_location_id | do_location_id | payment_type | ratecode_id | fare_amount | tip_amount | total_amount | tolls_amount | congestion_surcharge | cbd_congestion_fee |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| yellow | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2026/yellow_tripdata_2026-01.parquet | 2 | 2026-01-01 00:54:04 | 2026-01-01 00:59:37 | 1.0 | 0.97 | 239 | 238 | 1 | 1.0 | 7.2 | 3.66 | 15.86 | 0.0 | 2.5 | 0.0 |
| yellow | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2026/yellow_tripdata_2026-01.parquet | 1 | 2026-01-01 00:34:04 | 2026-01-01 00:39:47 | 0.0 | 0.9 | 163 | 162 | 2 | 1.0 | 7.9 | 0.0 | 13.65 | 0.0 | 2.5 | 0.75 |
| yellow | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2026/yellow_tripdata_2026-01.parquet | 1 | 2026-01-01 00:57:06 | 2026-01-01 01:05:59 | 0.0 | 1.4 | 43 | 237 | 1 | 1.0 | 10.7 | 2.5 | 18.95 | 0.0 | 2.5 | 0.75 |
| yellow | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2026/yellow_tripdata_2026-01.parquet | 2 | 2026-01-01 00:15:22 | 2026-01-01 00:58:10 | 4.0 | 5.58 | 142 | 209 | 1 | 1.0 | 38.7 | 11.11 | 55.56 | 0.0 | 2.5 | 0.75 |
| yellow | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2026/yellow_tripdata_2026-01.parquet | 2 | 2026-01-01 00:27:13 | 2026-01-01 00:40:43 | 0.0 | 2.16 | 88 | 144 | 1 | 1.0 | 13.5 | 3.85 | 23.1 | 0.0 | 2.5 | 0.75 |
| yellow | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2026/yellow_tripdata_2026-01.parquet | 2 | 2026-01-01 00:47:11 | 2026-01-01 01:00:47 | 2.0 | 2.33 | 144 | 137 | 1 | 1.0 | 14.2 | 4.99 | 24.94 | 0.0 | 2.5 | 0.75 |
| yellow | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2026/yellow_tripdata_2026-01.parquet | 1 | 2026-01-01 00:17:54 | 2026-01-01 00:28:32 | 1.0 | 1.3 | 142 | 50 | 2 | 1.0 | 11.4 | 0.0 | 17.15 | 0.0 | 2.5 | 0.75 |
| yellow | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2026/yellow_tripdata_2026-01.parquet | 1 | 2026-01-01 00:34:28 | 2026-01-01 00:59:05 | 0.0 | 2.9 | 50 | 234 | 1 | 1.0 | 22.6 | 5.65 | 34.0 | 0.0 | 2.5 | 0.75 |
| yellow | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2026/yellow_tripdata_2026-01.parquet | 2 | 2026-01-01 00:34:14 | 2026-01-01 01:11:58 | 1.0 | 5.34 | 161 | 45 | 1 | 1.0 | 37.3 | 8.61 | 51.66 | 0.0 | 2.5 | 0.75 |
| yellow | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2026/yellow_tripdata_2026-01.parquet | 2 | 2026-01-01 00:41:07 | 2026-01-01 00:50:42 | 3.0 | 1.83 | 237 | 263 | 1 | 1.0 | 10.7 | 2.36 | 18.06 | 0.0 | 2.5 | 0.0 |
| green | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2026/green_tripdata_2026-01.parquet | 1 | 2026-01-01 00:27:58 | 2026-01-01 00:55:16 | 2.0 | 6.2 | 65 | 233 | 1 | 1.0 | 31.7 | 7.5 | 45.2 | 0.0 | 2.75 | 0.75 |
| green | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2026/green_tripdata_2026-01.parquet | 2 | 2026-01-01 00:44:33 | 2026-01-01 01:32:56 | 5.0 | 5.36 | 66 | 188 | 1 | 5.0 | 50.0 | 10.2 | 61.2 | 0.0 | 0.0 | 0.0 |
| green | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2026/green_tripdata_2026-01.parquet | 1 | 2026-01-01 00:23:45 | 2026-01-01 00:45:03 | 4.0 | 10.6 | 65 | 179 | 1 | 1.0 | 41.5 | 2.0 | 46.0 | 0.0 | 0.0 | 0.0 |
| green | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2026/green_tripdata_2026-01.parquet | 1 | 2026-01-01 00:44:33 | 2026-01-01 01:00:45 | 1.0 | 4.2 | 42 | 141 | 2 | 1.0 | 19.8 | 0.0 | 25.05 | 0.0 | 2.75 | 0.0 |
| green | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2026/green_tripdata_2026-01.parquet | 2 | 2026-01-01 00:46:04 | 2026-01-01 01:04:40 | 1.0 | 2.76 | 95 | 82 | 2 | 1.0 | 19.1 | 0.0 | 21.6 | 0.0 | 0.0 | 0.0 |
| green | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2026/green_tripdata_2026-01.parquet | 2 | 2026-01-01 00:16:31 | 2026-01-01 00:33:57 | 1.0 | 2.6 | 66 | 88 | 1 | 1.0 | 19.8 | 0.0 | 25.8 | 0.0 | 2.75 | 0.75 |
| green | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2026/green_tripdata_2026-01.parquet | 2 | 2026-01-01 00:08:25 | 2026-01-01 00:18:15 | 1.0 | 1.35 | 166 | 239 | 1 | 1.0 | 11.4 | 3.33 | 19.98 | 0.0 | 2.75 | 0.0 |
| green | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2026/green_tripdata_2026-01.parquet | 2 | 2026-01-01 00:51:18 | 2026-01-01 00:58:35 | 1.0 | 1.27 | 41 | 42 | 1 | 1.0 | 9.3 | 1.0 | 12.8 | 0.0 | 0.0 | 0.0 |
| green | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2026/green_tripdata_2026-01.parquet | 2 | 2026-01-01 00:53:05 | 2026-01-01 00:56:27 | 1.0 | 0.51 | 92 | 92 | 1 | 5.0 | 15.0 | 0.0 | 16.0 | 0.0 | 0.0 | 0.0 |
| green | 2026 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2026/green_tripdata_2026-01.parquet | 2 | 2026-01-01 00:19:51 | 2026-01-01 00:48:36 | 1.0 | 9.06 | 74 | 211 | 2 | 1.0 | 41.5 | 0.0 | 47.5 | 0.0 | 2.75 | 0.75 |

**Decisión e interpretación:** Muestra de conveniencia para inspección; no se usa para estimar indicadores ni se garantiza un orden estable.

## 03_quality: Calidad y exclusiones

**Objetivo:** Calidad y exclusiones.

**Fuentes:** todos los archivos Parquet incluidos en `metadata.json`, con la población indicada en SQL.

```sql
-- Los motivos se solapan: no deben sumarse para obtener el total excluido.
SELECT taxi, source_year, count(*) AS rows,
 count(*) FILTER (WHERE bad_date) AS bad_date,
 count(*) FILTER (WHERE bad_distance) AS bad_distance,
 count(*) FILTER (WHERE bad_duration) AS bad_duration,
 count(*) FILTER (WHERE bad_amount) AS bad_amount,
 count(*) FILTER (WHERE passenger_count IS NULL) AS missing_passengers,
 count(*) FILTER (WHERE passenger_count <= 0 OR passenger_count > 6) AS unusual_passengers,
 count(*) FILTER (WHERE bad_date OR bad_distance OR bad_duration OR bad_amount) AS excluded,
 round(100.0 * count(*) FILTER (WHERE bad_date OR bad_distance OR bad_duration OR bad_amount) / count(*), 3) AS excluded_pct
FROM trips_flagged GROUP BY ALL ORDER BY taxi, source_year;
```

**Resultado** (primeras 40 filas; CSV contiene el resultado completo):

| taxi | source_year | rows | bad_date | bad_distance | bad_duration | bad_amount | missing_passengers | unusual_passengers | excluded | excluded_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| green | 2026 | 337114 | 98 | 12284 | 1521 | 6196 | 48775 | 4626 | 19300 | 5.725 |
| yellow | 2026 | 29703355 | 146 | 953454 | 381810 | 180386 | 7716688 | 91387 | 1484005 | 4.996 |

**Decisión e interpretación:** Los motivos pueden solaparse; excluded cuenta la unión. NULL también se marca explícitamente.

## 04_monthly: Volumen, importes, distancias, duración y propinas

**Objetivo:** Volumen, importes, distancias, duración y propinas.

**Fuentes:** todos los archivos Parquet incluidos en `metadata.json`, con la población indicada en SQL.

```sql
-- Volumen, importe registrado y ticket medio de viajes válidos por mes.
SELECT taxi, source_year AS year, source_month AS month,
 make_date(source_year, source_month, 1) AS period,
 count(*) AS trips, round(sum(total_amount), 2) AS total_usd,
 round(avg(total_amount), 3) AS avg_total_usd,
 round(quantile_cont(trip_distance, 0.5), 3) AS median_miles,
 round(quantile_cont(duration_min, 0.5), 3) AS median_minutes,
 round(100.0 * count(*) FILTER (WHERE payment_type=1) / count(*), 3) AS credit_pct,
 round(100.0 * sum(tip_amount) FILTER (WHERE payment_type=1 AND tip_amount >= 0)
 / nullif(sum(fare_amount) FILTER (WHERE payment_type=1 AND tip_amount >= 0), 0), 3) AS card_tip_pct
FROM trips_valid GROUP BY ALL ORDER BY taxi, year, month;
```

**Resultado** (primeras 40 filas; CSV contiene el resultado completo):

| taxi | year | month | period | trips | total_usd | avg_total_usd | median_miles | median_minutes | credit_pct | card_tip_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| green | 2026 | 1 | 2026-01-01 00:00:00 | 38193 | 923369.04 | 24.176 | 2.0 | 13.0 | 66.214 | 21.422 |
| green | 2026 | 2 | 2026-02-01 00:00:00 | 35218 | 854873.24 | 24.274 | 2.01 | 13.433 | 65.827 | 21.414 |
| green | 2026 | 3 | 2026-03-01 00:00:00 | 41774 | 1034525.65 | 24.765 | 2.12 | 13.1 | 66.01 | 21.502 |
| green | 2026 | 4 | 2026-04-01 00:00:00 | 41686 | 1049914.19 | 25.186 | 2.12 | 13.0 | 67.034 | 21.354 |
| green | 2026 | 5 | 2026-05-01 00:00:00 | 42444 | 1092115.84 | 25.731 | 2.13 | 13.383 | 67.979 | 20.751 |
| green | 2026 | 6 | 2026-06-01 00:00:00 | 41656 | 1082407.31 | 25.984 | 2.15 | 13.483 | 66.872 | 20.624 |
| green | 2026 | 7 | 2026-07-01 00:00:00 | 38692 | 1012152.72 | 26.159 | 2.2 | 13.067 | 66.934 | 20.268 |
| green | 2026 | 8 | 2026-08-01 00:00:00 | 38151 | 1006178.37 | 26.374 | 2.24 | 13.167 | 65.505 | 20.39 |
| yellow | 2026 | 1 | 2026-01-01 00:00:00 | 3515209 | 104283604.0 | 29.666 | 1.9 | 13.517 | 62.35 | 21.196 |
| yellow | 2026 | 2 | 2026-02-01 00:00:00 | 3208756 | 97708434.6 | 30.451 | 1.88 | 14.183 | 62.309 | 21.162 |
| yellow | 2026 | 3 | 2026-03-01 00:00:00 | 3761049 | 113818186.75 | 30.262 | 1.9 | 13.45 | 67.686 | 21.118 |
| yellow | 2026 | 4 | 2026-04-01 00:00:00 | 3672435 | 110518342.4 | 30.094 | 1.9 | 14.167 | 70.036 | 21.056 |
| yellow | 2026 | 5 | 2026-05-01 00:00:00 | 3910257 | 119438968.25 | 30.545 | 1.93 | 14.667 | 68.04 | 21.083 |
| yellow | 2026 | 6 | 2026-06-01 00:00:00 | 3644617 | 111522486.74 | 30.599 | 1.9 | 14.283 | 64.952 | 23.049 |
| yellow | 2026 | 7 | 2026-07-01 00:00:00 | 3344740 | 100787574.27 | 30.133 | 2.0 | 14.3 | 63.474 | 22.299 |
| yellow | 2026 | 8 | 2026-08-01 00:00:00 | 3162287 | 95342533.2 | 30.15 | 2.09 | 14.333 | 63.085 | 22.018 |

**Decisión e interpretación:** Importe registrado no equivale a utilidad; mediana reduce influencia de extremos. Propinas solo en tarjeta.

## 05_hourly: Horas de mayor actividad

**Objetivo:** Horas de mayor actividad.

**Fuentes:** todos los archivos Parquet incluidos en `metadata.json`, con la población indicada en SQL.

```sql
-- Perfil horario; usa hora local declarada en el archivo TLC, sin convertir UTC.
SELECT taxi, source_year AS year, hour(pickup) AS hour,
 count(*) AS trips, round(avg(total_amount), 3) AS avg_total_usd
FROM trips_valid GROUP BY ALL ORDER BY taxi, year, hour;
```

**Resultado** (primeras 40 filas; CSV contiene el resultado completo):

| taxi | year | hour | trips | avg_total_usd |
|---|---|---|---|---|
| green | 2026 | 0 | 4754 | 28.835 |
| green | 2026 | 1 | 2930 | 28.346 |
| green | 2026 | 2 | 2114 | 33.897 |
| green | 2026 | 3 | 1741 | 38.542 |
| green | 2026 | 4 | 1734 | 38.965 |
| green | 2026 | 5 | 2357 | 34.57 |
| green | 2026 | 6 | 6389 | 24.53 |
| green | 2026 | 7 | 13591 | 23.668 |
| green | 2026 | 8 | 17100 | 24.624 |
| green | 2026 | 9 | 17936 | 24.423 |
| green | 2026 | 10 | 17301 | 24.851 |
| green | 2026 | 11 | 17102 | 25.155 |
| green | 2026 | 12 | 18508 | 24.856 |
| green | 2026 | 13 | 18250 | 24.473 |
| green | 2026 | 14 | 20458 | 24.889 |
| green | 2026 | 15 | 22229 | 24.44 |
| green | 2026 | 16 | 23945 | 25.471 |
| green | 2026 | 17 | 24820 | 24.829 |
| green | 2026 | 18 | 23529 | 24.042 |
| green | 2026 | 19 | 17690 | 23.497 |
| green | 2026 | 20 | 13559 | 24.111 |
| green | 2026 | 21 | 12045 | 27.458 |
| green | 2026 | 22 | 10348 | 30.394 |
| green | 2026 | 23 | 7384 | 28.591 |
| yellow | 2026 | 0 | 907058 | 31.26 |
| yellow | 2026 | 1 | 602517 | 29.483 |
| yellow | 2026 | 2 | 400976 | 28.392 |
| yellow | 2026 | 3 | 288192 | 29.423 |
| yellow | 2026 | 4 | 235938 | 33.813 |
| yellow | 2026 | 5 | 261316 | 35.53 |
| yellow | 2026 | 6 | 490802 | 31.994 |
| yellow | 2026 | 7 | 856811 | 30.241 |
| yellow | 2026 | 8 | 1150122 | 29.568 |
| yellow | 2026 | 9 | 1204269 | 28.465 |
| yellow | 2026 | 10 | 1219926 | 28.543 |
| yellow | 2026 | 11 | 1316212 | 29.021 |
| yellow | 2026 | 12 | 1423288 | 29.129 |
| yellow | 2026 | 13 | 1489066 | 29.863 |
| yellow | 2026 | 14 | 1614543 | 30.988 |
| yellow | 2026 | 15 | 1668670 | 31.086 |

**Decisión e interpretación:** Se interpreta el horario local TLC; no identifica una causa de los patrones.

## 06_payments: Mezcla de medios de pago

**Objetivo:** Mezcla de medios de pago.

**Fuentes:** todos los archivos Parquet incluidos en `metadata.json`, con la población indicada en SQL.

```sql
-- Códigos: 0=Flex Fare, 1=crédito, 2=efectivo, 3=sin cargo, 4=disputa,
-- 5=desconocido, 6=anulado. NULL/otros se conservan para auditar.
SELECT taxi, source_year AS year, payment_type, count(*) AS trips,
 round(100.0*count(*) / sum(count(*)) OVER (PARTITION BY taxi, source_year), 3) AS share_pct,
 round(avg(total_amount), 3) AS avg_total_usd
FROM trips_valid GROUP BY taxi, source_year, payment_type ORDER BY taxi, year, payment_type;
```

**Resultado** (primeras 40 filas; CSV contiene el resultado completo):

| taxi | year | payment_type | trips | share_pct | avg_total_usd |
|---|---|---|---|---|---|
| green | 2026 | 1 | 211589 | 66.576 | 25.601 |
| green | 2026 | 2 | 62528 | 19.674 | 20.754 |
| green | 2026 | 3 | 723 | 0.227 | 17.694 |
| green | 2026 | 4 | 273 | 0.086 | 19.587 |
| green | 2026 | NULL | 42701 | 13.436 | 30.979 |
| yellow | 2026 | 0 | 7036103 | 24.934 | 32.433 |
| yellow | 2026 | 1 | 18454571 | 65.397 | 30.021 |
| yellow | 2026 | 2 | 2554461 | 9.052 | 26.001 |
| yellow | 2026 | 3 | 56214 | 0.199 | 24.375 |
| yellow | 2026 | 4 | 118001 | 0.418 | 28.829 |

**Decisión e interpretación:** Se mantienen todos los códigos; no se asume que tarjeta + efectivo sumen 100%.

## 07_distributions: Distribución y colas

**Objetivo:** Distribución y colas.

**Fuentes:** todos los archivos Parquet incluidos en `metadata.json`, con la población indicada en SQL.

```sql
-- Medianas y colas permiten detectar asimetría sin depender solo del promedio.
SELECT taxi, source_year AS year, count(*) AS trips,
 round(avg(trip_distance), 3) AS avg_miles,
 round(quantile_cont(trip_distance, 0.5), 3) AS median_miles,
 round(quantile_cont(trip_distance, 0.95), 3) AS p95_miles,
 round(quantile_cont(trip_distance, 0.99), 3) AS p99_miles,
 round(quantile_cont(duration_min, 0.5), 3) AS median_minutes,
 round(quantile_cont(duration_min, 0.95), 3) AS p95_minutes,
 round(quantile_cont(total_amount, 0.5), 3) AS median_total_usd,
 round(quantile_cont(total_amount, 0.95), 3) AS p95_total_usd,
 round(quantile_cont(total_amount, 0.99), 3) AS p99_total_usd,
 max(total_amount) AS max_total_usd,
 round(avg(passenger_count), 3) AS avg_reported_passengers
FROM trips_valid GROUP BY ALL ORDER BY taxi, year;
```

**Resultado** (primeras 40 filas; CSV contiene el resultado completo):

| taxi | year | trips | avg_miles | median_miles | p95_miles | p99_miles | median_minutes | p95_minutes | median_total_usd | p95_total_usd | p99_total_usd | max_total_usd | avg_reported_passengers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| green | 2026 | 317814 | 3.293 | 2.12 | 10.4 | 17.53 | 13.2 | 42.717 | 20.5 | 56.6 | 94.769 | 668.8 | 1.299 |
| yellow | 2026 | 28219350 | 3.515 | 1.93 | 12.55 | 19.55 | 14.1 | 44.0 | 23.58 | 77.27 | 104.96 | 1065.72 | 1.248 |

**Decisión e interpretación:** Se reportan mediana, p95 y p99. Los filtros operativos no eliminan necesariamente todos los errores.

## 08_common_months: Evolución en meses comparables

**Objetivo:** Evolución en meses comparables.

**Fuentes:** todos los archivos Parquet incluidos en `metadata.json`, con la población indicada en SQL.

```sql
-- Compara solamente meses con archivos en TODOS los años y ambos tipos.
-- Evita comparar doce meses de 2024/25 con un año 2026 incompleto.
WITH coverage AS (
 SELECT DISTINCT taxi, source_year, source_month FROM trips_raw
), common AS (
 SELECT source_month FROM coverage GROUP BY source_month
 HAVING count(*) = (SELECT count(DISTINCT source_year) FROM coverage) * 2
)
SELECT taxi, source_year AS year, count(*) AS trips,
 count(DISTINCT source_month) AS months,
 round(sum(total_amount), 2) AS total_usd,
 round(avg(total_amount), 3) AS avg_total_usd,
 round(avg(trip_distance), 3) AS avg_miles,
 round(avg(duration_min), 3) AS avg_minutes,
 round(100.0*count(*) FILTER (WHERE payment_type=1)/count(*), 3) AS credit_pct,
 round(avg(cbd_congestion_fee), 3) AS avg_cbd_fee_usd
FROM trips_valid WHERE source_month IN (SELECT source_month FROM common)
GROUP BY taxi, source_year ORDER BY taxi, year;
```

**Resultado** (primeras 40 filas; CSV contiene el resultado completo):

| taxi | year | trips | months | total_usd | avg_total_usd | avg_miles | avg_minutes | credit_pct | avg_cbd_fee_usd |
|---|---|---|---|---|---|---|---|---|---|
| green | 2026 | 317814 | 8 | 8055536.36 | 25.347 | 3.293 | 16.852 | 66.576 | 0.063 |
| yellow | 2026 | 28219350 | 8 | 853420130.21 | 30.242 | 3.515 | 17.661 | 65.397 | 0.543 |

**Decisión e interpretación:** Solo meses presentes en ambos taxis y todos los años seleccionados; evita sesgo de año parcial.

## 09_weekday: Actividad por día de semana

**Objetivo:** Actividad por día de semana.

**Fuentes:** todos los archivos Parquet incluidos en `metadata.json`, con la población indicada en SQL.

```sql
-- Ajusta por días observados: totales por día de semana pueden confundir exposición.
SELECT taxi, source_year AS year, isodow(pickup) AS weekday,
 count(*) AS trips, count(DISTINCT pickup::DATE) AS observed_days,
 round(count(*)::DOUBLE/count(DISTINCT pickup::DATE), 1) AS trips_per_observed_day
FROM trips_valid GROUP BY ALL ORDER BY taxi, year, weekday;
```

**Resultado** (primeras 40 filas; CSV contiene el resultado completo):

| taxi | year | weekday | trips | observed_days | trips_per_observed_day |
|---|---|---|---|---|---|
| green | 2026 | 1 | 45220 | 35 | 1292.0 |
| green | 2026 | 2 | 47976 | 34 | 1411.1 |
| green | 2026 | 3 | 49763 | 34 | 1463.6 |
| green | 2026 | 4 | 52520 | 35 | 1500.6 |
| green | 2026 | 5 | 47546 | 35 | 1358.5 |
| green | 2026 | 6 | 38398 | 35 | 1097.1 |
| green | 2026 | 7 | 36391 | 35 | 1039.7 |
| yellow | 2026 | 1 | 3353808 | 35 | 95823.1 |
| yellow | 2026 | 2 | 3844736 | 34 | 113080.5 |
| yellow | 2026 | 3 | 4098049 | 34 | 120530.9 |
| yellow | 2026 | 4 | 4456770 | 35 | 127336.3 |
| yellow | 2026 | 5 | 4220277 | 35 | 120579.3 |
| yellow | 2026 | 6 | 4501154 | 35 | 128604.4 |
| yellow | 2026 | 7 | 3744556 | 35 | 106987.3 |

**Decisión e interpretación:** Se divide por los días observados con viajes válidos; no demuestra cobertura de días sin viajes.

## 10_distance_bins: Composición de distancias

**Objetivo:** Composición de distancias.

**Fuentes:** todos los archivos Parquet incluidos en `metadata.json`, con la población indicada en SQL.

```sql
-- Distribución interpretable de distancias válidas en millas.
SELECT taxi, source_year AS year,
 CASE WHEN trip_distance < 1 THEN '1: <1 mi'
 WHEN trip_distance < 3 THEN '2: 1-3 mi'
 WHEN trip_distance < 10 THEN '3: 3-10 mi'
 WHEN trip_distance < 25 THEN '4: 10-25 mi' ELSE '5: 25-100 mi' END AS distance_bin,
 count(*) AS trips
FROM trips_valid GROUP BY ALL ORDER BY taxi, year, distance_bin;
```

**Resultado** (primeras 40 filas; CSV contiene el resultado completo):

| taxi | year | distance_bin | trips |
|---|---|---|---|
| green | 2026 | 1: <1 mi | 44260 |
| green | 2026 | 2: 1-3 mi | 168488 |
| green | 2026 | 3: 3-10 mi | 87729 |
| green | 2026 | 4: 10-25 mi | 16776 |
| green | 2026 | 5: 25-100 mi | 561 |
| yellow | 2026 | 1: <1 mi | 5915837 |
| yellow | 2026 | 2: 1-3 mi | 12976372 |
| yellow | 2026 | 3: 3-10 mi | 7163685 |
| yellow | 2026 | 4: 10-25 mi | 2083254 |
| yellow | 2026 | 5: 25-100 mi | 80202 |

**Decisión e interpretación:** Las bandas usan millas y provienen de viajes válidos.

## 11_outliers: Casos extremos sin filtrar

**Objetivo:** Casos extremos sin filtrar.

**Fuentes:** todos los archivos Parquet incluidos en `metadata.json`, con la población indicada en SQL.

```sql
-- Ejemplos de importes extremos SIN filtrar; se conservan para auditoría.
SELECT taxi, source_year, source_month, pickup, dropoff, trip_distance,
 duration_min, fare_amount, total_amount, bad_date, bad_distance, bad_duration, bad_amount
FROM trips_flagged ORDER BY total_amount DESC NULLS LAST LIMIT 20;
```

**Resultado** (primeras 40 filas; CSV contiene el resultado completo):

| taxi | source_year | source_month | pickup | dropoff | trip_distance | duration_min | fare_amount | total_amount | bad_date | bad_distance | bad_duration | bad_amount |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| yellow | 2026 | 6 | 2026-06-07 07:16:20 | 2026-06-07 07:16:20 | 0.01 | 0.0 | 7045.0 | 7053.5 | False | False | True | False |
| yellow | 2026 | 7 | 2026-07-31 09:37:10 | 2026-07-31 09:37:10 | 0.05 | 0.0 | 6466.6 | 6471.35 | False | False | True | False |
| yellow | 2026 | 5 | 2026-05-25 07:20:43 | 2026-05-25 07:20:43 | 0.13 | 0.0 | 5525.99 | 5530.74 | False | False | True | False |
| yellow | 2026 | 5 | 2026-05-14 19:19:59 | 2026-05-14 19:19:59 | 0.0 | 0.0 | 5525.99 | 5530.74 | False | True | True | False |
| yellow | 2026 | 8 | 2026-08-01 17:57:35 | 2026-08-01 17:57:35 | 0.0 | 0.0 | 5525.99 | 5530.74 | False | True | True | False |
| yellow | 2026 | 5 | 2026-05-14 19:44:03 | 2026-05-14 19:44:03 | 0.39 | 0.0 | 5525.99 | 5530.74 | False | False | True | False |
| yellow | 2026 | 8 | 2026-08-29 23:19:18 | 2026-08-29 23:19:18 | 0.0 | 0.0 | 5050.0 | 5054.75 | False | True | True | False |
| yellow | 2026 | 8 | 2026-08-14 13:06:19 | 2026-08-14 13:06:19 | 0.0 | 0.0 | 5000.0 | 5000.0 | False | True | True | False |
| yellow | 2026 | 8 | 2026-08-10 13:21:33 | 2026-08-10 13:21:33 | 0.0 | 0.0 | 4385.0 | 4385.0 | False | True | True | False |
| yellow | 2026 | 7 | 2026-07-22 05:30:01 | 2026-07-25 06:07:59 | 19.28 | 4357.966666666666 | 3062.0 | 3067.75 | False | False | True | False |
| yellow | 2026 | 1 | 2026-01-25 00:43:10 | 2026-01-27 11:28:52 | 48.65 | 3525.7 | 2555.2 | 2560.2 | False | False | True | False |
| yellow | 2026 | 5 | 2026-05-14 17:53:53 | 2026-05-14 17:53:53 | 0.07 | 0.0 | 2552.59 | 2554.09 | False | False | True | False |
| yellow | 2026 | 1 | 2026-01-15 13:56:22 | 2026-01-15 13:56:22 | 0.0 | 0.0 | 2500.0 | 2500.0 | False | True | True | False |
| yellow | 2026 | 2 | 2026-02-22 19:31:11 | 2026-02-24 19:19:42 | 41.62 | 2868.516666666667 | 2084.1 | 2088.85 | False | False | True | False |
| yellow | 2026 | 6 | 2026-06-25 19:20:13 | 2026-06-25 19:20:13 | 0.05 | 0.0 | 2000.0 | 2004.75 | False | False | True | False |
| yellow | 2026 | 7 | 2026-07-23 13:36:51 | 2026-07-23 13:36:51 | 0.0 | 0.0 | 2000.0 | 2000.0 | False | True | True | False |
| yellow | 2026 | 8 | 2026-08-06 11:47:42 | 2026-08-06 17:08:32 | 272.2 | 320.8333333333333 | 1860.8 | 1884.55 | False | True | True | False |
| yellow | 2026 | 8 | 2026-08-28 02:36:52 | 2026-08-28 07:06:10 | 274.35 | 269.3 | 1849.6 | 1866.89 | False | True | True | False |
| yellow | 2026 | 3 | 2026-03-05 17:15:25 | 2026-03-07 05:50:52 | 205.86 | 2195.45 | 1843.3 | 1850.55 | False | True | True | False |
| yellow | 2026 | 6 | 2026-06-20 04:21:56 | 2026-06-21 12:47:22 | 185.55 | 1945.4333333333334 | 1825.1 | 1830.1 | False | True | True | False |

**Decisión e interpretación:** No se declara fraude; son ejemplos para revisar, no datos corregidos automáticamente.
