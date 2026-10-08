# Consultas y resultados: final

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
| green | 2024 | 12 | 660218 | 2008-12-31 00:00:00 | 2025-01-01 22:21:15 |
| green | 2025 | 12 | 591375 | 2008-12-31 15:13:04 | 2026-01-01 21:09:39 |
| green | 2026 | 8 | 337114 | 2008-12-31 17:35:31 | 2026-08-31 23:58:28 |
| yellow | 2024 | 12 | 41169720 | 2002-12-31 16:46:07 | 2026-06-26 23:53:12 |
| yellow | 2025 | 12 | 48722602 | 2007-12-05 18:45:00 | 2025-12-31 23:59:59 |
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
| yellow | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2024/yellow_tripdata_2024-01.parquet | 2 | 2024-01-01 00:57:55 | 2024-01-01 01:17:43 | 1.0 | 1.72 | 186 | 79 | 2 | 1.0 | 17.7 | 0.0 | 22.7 | 0.0 | 2.5 | NULL |
| yellow | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2024/yellow_tripdata_2024-01.parquet | 1 | 2024-01-01 00:03:00 | 2024-01-01 00:09:36 | 1.0 | 1.8 | 140 | 236 | 1 | 1.0 | 10.0 | 3.75 | 18.75 | 0.0 | 2.5 | NULL |
| yellow | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2024/yellow_tripdata_2024-01.parquet | 1 | 2024-01-01 00:17:06 | 2024-01-01 00:35:01 | 1.0 | 4.7 | 236 | 79 | 1 | 1.0 | 23.3 | 3.0 | 31.3 | 0.0 | 2.5 | NULL |
| yellow | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2024/yellow_tripdata_2024-01.parquet | 1 | 2024-01-01 00:36:38 | 2024-01-01 00:44:56 | 1.0 | 1.4 | 79 | 211 | 1 | 1.0 | 10.0 | 2.0 | 17.0 | 0.0 | 2.5 | NULL |
| yellow | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2024/yellow_tripdata_2024-01.parquet | 1 | 2024-01-01 00:46:51 | 2024-01-01 00:52:57 | 1.0 | 0.8 | 211 | 148 | 1 | 1.0 | 7.9 | 3.2 | 16.1 | 0.0 | 2.5 | NULL |
| yellow | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2024/yellow_tripdata_2024-01.parquet | 1 | 2024-01-01 00:54:08 | 2024-01-01 01:26:31 | 1.0 | 4.7 | 148 | 141 | 1 | 1.0 | 29.6 | 6.9 | 41.5 | 0.0 | 2.5 | NULL |
| yellow | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2024/yellow_tripdata_2024-01.parquet | 2 | 2024-01-01 00:49:44 | 2024-01-01 01:15:47 | 2.0 | 10.82 | 138 | 181 | 1 | 1.0 | 45.7 | 10.0 | 64.95 | 0.0 | 0.0 | NULL |
| yellow | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2024/yellow_tripdata_2024-01.parquet | 1 | 2024-01-01 00:30:40 | 2024-01-01 00:58:40 | 0.0 | 3.0 | 246 | 231 | 2 | 1.0 | 25.4 | 0.0 | 30.4 | 0.0 | 2.5 | NULL |
| yellow | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2024/yellow_tripdata_2024-01.parquet | 2 | 2024-01-01 00:26:01 | 2024-01-01 00:54:12 | 1.0 | 5.44 | 161 | 261 | 2 | 1.0 | 31.0 | 0.0 | 36.0 | 0.0 | 2.5 | NULL |
| yellow | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/yellow/2024/yellow_tripdata_2024-01.parquet | 2 | 2024-01-01 00:28:08 | 2024-01-01 00:29:16 | 1.0 | 0.04 | 113 | 113 | 2 | 1.0 | 3.0 | 0.0 | 8.0 | 0.0 | 2.5 | NULL |
| green | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2024/green_tripdata_2024-01.parquet | 2 | 2024-01-01 00:46:55 | 2024-01-01 00:58:25 | 1.0 | 1.98 | 236 | 239 | 1 | 1.0 | 12.8 | 3.61 | 21.66 | 0.0 | 2.75 | NULL |
| green | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2024/green_tripdata_2024-01.parquet | 2 | 2024-01-01 00:31:42 | 2024-01-01 00:52:34 | 5.0 | 6.54 | 65 | 170 | 1 | 1.0 | 30.3 | 7.11 | 42.66 | 0.0 | 2.75 | NULL |
| green | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2024/green_tripdata_2024-01.parquet | 2 | 2024-01-01 00:30:21 | 2024-01-01 00:49:23 | 1.0 | 3.08 | 74 | 262 | 1 | 1.0 | 19.8 | 3.0 | 28.05 | 0.0 | 2.75 | NULL |
| green | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2024/green_tripdata_2024-01.parquet | 1 | 2024-01-01 00:30:20 | 2024-01-01 00:42:12 | 1.0 | 2.4 | 74 | 116 | 2 | 1.0 | 14.2 | 0.0 | 16.7 | 0.0 | 0.0 | NULL |
| green | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2024/green_tripdata_2024-01.parquet | 2 | 2024-01-01 00:32:38 | 2024-01-01 00:43:37 | 1.0 | 5.14 | 74 | 243 | 1 | 1.0 | 22.6 | 6.28 | 31.38 | 0.0 | 0.0 | NULL |
| green | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2024/green_tripdata_2024-01.parquet | 1 | 2024-01-01 00:43:41 | 2024-01-01 01:00:23 | 1.0 | 2.0 | 33 | 209 | 1 | 1.0 | 17.0 | 2.0 | 24.25 | 0.0 | 2.75 | NULL |
| green | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2024/green_tripdata_2024-01.parquet | 1 | 2024-01-01 00:31:56 | 2024-01-01 00:48:09 | 2.0 | 3.2 | 74 | 238 | 1 | 1.0 | 18.4 | 4.7 | 28.35 | 0.0 | 2.75 | NULL |
| green | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2024/green_tripdata_2024-01.parquet | 2 | 2024-01-01 00:46:12 | 2024-01-01 00:57:39 | 2.0 | 2.01 | 166 | 239 | 1 | 1.0 | 13.5 | 5.62 | 24.37 | 0.0 | 2.75 | NULL |
| green | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2024/green_tripdata_2024-01.parquet | 2 | 2024-01-01 00:38:07 | 2024-01-01 00:39:23 | 1.0 | 0.31 | 226 | 226 | 2 | 1.0 | 3.7 | 0.0 | 6.2 | 0.0 | 0.0 | NULL |
| green | 2024 | 1 | /Users/javiervalladares/Library/Mobile Documents/com~apple~CloudDocs/Octavo Semestre/Datos/Lab8/data/raw/green/2024/green_tripdata_2024-01.parquet | 2 | 2024-01-01 00:44:24 | 2024-01-01 00:57:47 | 1.0 | 2.32 | 7 | 129 | 1 | 1.0 | 14.9 | 3.48 | 20.88 | 0.0 | 0.0 | NULL |

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
| green | 2024 | 660218 | 164 | 34809 | 3641 | 2667 | 24328 | 6941 | 39512 | 5.985 |
| green | 2025 | 591375 | 248 | 24647 | 4617 | 5000 | 49880 | 8477 | 32964 | 5.574 |
| green | 2026 | 337114 | 98 | 12284 | 1521 | 6196 | 48775 | 4626 | 19300 | 5.725 |
| yellow | 2024 | 41169720 | 420 | 777918 | 38859 | 748345 | 4091232 | 401638 | 1491879 | 3.624 |
| yellow | 2025 | 48722602 | 214 | 1405828 | 564705 | 2870701 | 11611894 | 260208 | 4570673 | 9.381 |
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
| green | 2024 | 1 | 2024-01-01 00:00:00 | 53277 | 1180287.29 | 22.154 | 1.88 | 11.433 | 64.758 | 21.144 |
| green | 2024 | 2 | 2024-02-01 00:00:00 | 50375 | 1131082.36 | 22.453 | 1.89 | 11.45 | 65.941 | 20.926 |
| green | 2024 | 3 | 2024-03-01 00:00:00 | 54069 | 1228381.67 | 22.719 | 1.88 | 11.65 | 66.215 | 20.897 |
| green | 2024 | 4 | 2024-04-01 00:00:00 | 52914 | 1232111.09 | 23.285 | 1.92 | 11.7 | 68.904 | 21.005 |
| green | 2024 | 5 | 2024-05-01 00:00:00 | 57424 | 1404590.25 | 24.46 | 1.98 | 12.417 | 69.205 | 20.551 |
| green | 2024 | 6 | 2024-06-01 00:00:00 | 51649 | 1279349.3 | 24.77 | 2.02 | 12.25 | 69.053 | 20.287 |
| green | 2024 | 7 | 2024-07-01 00:00:00 | 48447 | 1182175.27 | 24.401 | 2.04 | 11.783 | 69.082 | 20.463 |
| green | 2024 | 8 | 2024-08-01 00:00:00 | 48623 | 1255072.84 | 25.812 | 2.1 | 12.0 | 69.34 | 19.93 |
| green | 2024 | 9 | 2024-09-01 00:00:00 | 51205 | 1356612.74 | 26.494 | 2.08 | 12.733 | 70.493 | 19.807 |
| green | 2024 | 10 | 2024-10-01 00:00:00 | 53135 | 1326208.15 | 24.959 | 2.0 | 12.35 | 70.981 | 20.422 |
| green | 2024 | 11 | 2024-11-01 00:00:00 | 49035 | 1173804.97 | 23.938 | 1.94 | 12.133 | 71.32 | 20.656 |
| green | 2024 | 12 | 2024-12-01 00:00:00 | 50553 | 1202370.78 | 23.784 | 1.9 | 11.867 | 70.285 | 20.849 |
| green | 2025 | 1 | 2025-01-01 00:00:00 | 45221 | 1020122.34 | 22.559 | 1.83 | 11.267 | 71.423 | 21.273 |
| green | 2025 | 2 | 2025-02-01 00:00:00 | 43567 | 997853.18 | 22.904 | 1.87 | 11.55 | 71.295 | 20.948 |
| green | 2025 | 3 | 2025-03-01 00:00:00 | 47972 | 1150776.43 | 23.989 | 1.96 | 12.117 | 69.022 | 20.533 |
| green | 2025 | 4 | 2025-04-01 00:00:00 | 48379 | 1187891.1 | 24.554 | 1.99 | 12.383 | 70.915 | 20.663 |
| green | 2025 | 5 | 2025-05-01 00:00:00 | 51844 | 1314126.88 | 25.348 | 2.01 | 12.717 | 71.698 | 20.419 |
| green | 2025 | 6 | 2025-06-01 00:00:00 | 46861 | 1209237.46 | 25.805 | 2.11 | 12.783 | 69.693 | 20.288 |
| green | 2025 | 7 | 2025-07-01 00:00:00 | 46068 | 1184384.57 | 25.709 | 2.17 | 12.85 | 66.866 | 20.286 |
| green | 2025 | 8 | 2025-08-01 00:00:00 | 44212 | 1225516.0 | 27.719 | 2.3 | 13.233 | 66.903 | 19.11 |
| green | 2025 | 9 | 2025-09-01 00:00:00 | 46850 | 1283923.01 | 27.405 | 2.24 | 13.8 | 68.38 | 19.757 |
| green | 2025 | 10 | 2025-10-01 00:00:00 | 47114 | 1216403.15 | 25.818 | 2.16 | 13.367 | 69.686 | 20.645 |
| green | 2025 | 11 | 2025-11-01 00:00:00 | 44620 | 1121079.67 | 25.125 | 2.12 | 13.0 | 68.362 | 20.779 |
| green | 2025 | 12 | 2025-12-01 00:00:00 | 45703 | 1132204.35 | 24.773 | 2.01 | 12.817 | 67.031 | 21.331 |
| green | 2026 | 1 | 2026-01-01 00:00:00 | 38193 | 923369.04 | 24.176 | 2.0 | 13.0 | 66.214 | 21.422 |
| green | 2026 | 2 | 2026-02-01 00:00:00 | 35218 | 854873.24 | 24.274 | 2.01 | 13.433 | 65.827 | 21.414 |
| green | 2026 | 3 | 2026-03-01 00:00:00 | 41774 | 1034525.65 | 24.765 | 2.12 | 13.1 | 66.01 | 21.502 |
| green | 2026 | 4 | 2026-04-01 00:00:00 | 41686 | 1049914.19 | 25.186 | 2.12 | 13.0 | 67.034 | 21.354 |
| green | 2026 | 5 | 2026-05-01 00:00:00 | 42444 | 1092115.84 | 25.731 | 2.13 | 13.383 | 67.979 | 20.751 |
| green | 2026 | 6 | 2026-06-01 00:00:00 | 41656 | 1082407.31 | 25.984 | 2.15 | 13.483 | 66.872 | 20.624 |
| green | 2026 | 7 | 2026-07-01 00:00:00 | 38692 | 1012152.72 | 26.159 | 2.2 | 13.067 | 66.934 | 20.268 |
| green | 2026 | 8 | 2026-08-01 00:00:00 | 38151 | 1006178.37 | 26.374 | 2.24 | 13.167 | 65.505 | 20.39 |
| yellow | 2024 | 1 | 2024-01-01 00:00:00 | 2867591 | 78393609.75 | 27.338 | 1.7 | 11.717 | 80.1 | 22.62 |
| yellow | 2024 | 2 | 2024-02-01 00:00:00 | 2899440 | 78951343.92 | 27.23 | 1.72 | 12.067 | 80.043 | 22.598 |
| yellow | 2024 | 3 | 2024-03-01 00:00:00 | 3437624 | 95754912.24 | 27.855 | 1.8 | 12.55 | 74.882 | 22.398 |
| yellow | 2024 | 4 | 2024-04-01 00:00:00 | 3411748 | 96154036.38 | 28.183 | 1.81 | 12.9 | 74.272 | 22.324 |
| yellow | 2024 | 5 | 2024-05-01 00:00:00 | 3613916 | 104789416.91 | 28.996 | 1.81 | 13.433 | 74.819 | 22.137 |
| yellow | 2024 | 6 | 2024-06-01 00:00:00 | 3425726 | 98251584.8 | 28.681 | 1.82 | 13.067 | 74.332 | 22.012 |
| yellow | 2024 | 7 | 2024-07-01 00:00:00 | 2971649 | 86085233.54 | 28.969 | 1.83 | 12.917 | 75.057 | 21.548 |
| yellow | 2024 | 8 | 2024-08-01 00:00:00 | 2865051 | 83695340.49 | 29.213 | 1.84 | 12.867 | 75.12 | 21.407 |

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
| green | 2024 | 0 | 11145 | 25.803 |
| green | 2024 | 1 | 7657 | 24.932 |
| green | 2024 | 2 | 5425 | 28.206 |
| green | 2024 | 3 | 4064 | 32.935 |
| green | 2024 | 4 | 3326 | 34.267 |
| green | 2024 | 5 | 3289 | 31.242 |
| green | 2024 | 6 | 9376 | 22.499 |
| green | 2024 | 7 | 22115 | 21.999 |
| green | 2024 | 8 | 28693 | 22.87 |
| green | 2024 | 9 | 31821 | 22.997 |
| green | 2024 | 10 | 31700 | 23.284 |
| green | 2024 | 11 | 31939 | 23.893 |
| green | 2024 | 12 | 33388 | 23.481 |
| green | 2024 | 13 | 33992 | 23.582 |
| green | 2024 | 14 | 39573 | 23.681 |
| green | 2024 | 15 | 43290 | 23.438 |
| green | 2024 | 16 | 46940 | 24.957 |
| green | 2024 | 17 | 51202 | 24.425 |
| green | 2024 | 18 | 48982 | 23.645 |
| green | 2024 | 19 | 38801 | 23.079 |
| green | 2024 | 20 | 29787 | 22.991 |
| green | 2024 | 21 | 25996 | 25.679 |
| green | 2024 | 22 | 21392 | 27.135 |
| green | 2024 | 23 | 16813 | 26.01 |
| green | 2025 | 0 | 8689 | 28.416 |
| green | 2025 | 1 | 5779 | 28.149 |
| green | 2025 | 2 | 3979 | 32.408 |
| green | 2025 | 3 | 3089 | 34.631 |
| green | 2025 | 4 | 2922 | 37.992 |
| green | 2025 | 5 | 3681 | 33.148 |
| green | 2025 | 6 | 10128 | 24.818 |
| green | 2025 | 7 | 21861 | 23.735 |
| green | 2025 | 8 | 28359 | 24.236 |
| green | 2025 | 9 | 29833 | 24.446 |
| green | 2025 | 10 | 29620 | 24.373 |
| green | 2025 | 11 | 29410 | 24.988 |
| green | 2025 | 12 | 31534 | 24.361 |
| green | 2025 | 13 | 31809 | 23.954 |
| green | 2025 | 14 | 35285 | 24.348 |
| green | 2025 | 15 | 38591 | 24.037 |

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
| green | 2024 | 1 | 426884 | 68.774 | 25.093 |
| green | 2024 | 2 | 167711 | 27.019 | 20.569 |
| green | 2024 | 3 | 1967 | 0.317 | 15.463 |
| green | 2024 | 4 | 681 | 0.11 | 14.485 |
| green | 2024 | 5 | 21 | 0.003 | 19.39 |
| green | 2024 | NULL | 23442 | 3.777 | 31.987 |
| green | 2025 | 1 | 386997 | 69.303 | 25.775 |
| green | 2025 | 2 | 124465 | 22.289 | 21.193 |
| green | 2025 | 3 | 1564 | 0.28 | 15.713 |
| green | 2025 | 4 | 520 | 0.093 | 15.682 |
| green | 2025 | 5 | 18 | 0.003 | 15.764 |
| green | 2025 | NULL | 44847 | 8.031 | 31.172 |
| green | 2026 | 1 | 211589 | 66.576 | 25.601 |
| green | 2026 | 2 | 62528 | 19.674 | 20.754 |
| green | 2026 | 3 | 723 | 0.227 | 17.694 |
| green | 2026 | 4 | 273 | 0.086 | 19.587 |
| green | 2026 | NULL | 42701 | 13.436 | 30.979 |
| yellow | 2024 | 0 | 3692099 | 9.305 | 25.343 |
| yellow | 2024 | 1 | 30168733 | 76.034 | 29.717 |
| yellow | 2024 | 2 | 5275283 | 13.295 | 24.881 |
| yellow | 2024 | 3 | 155999 | 0.393 | 27.101 |
| yellow | 2024 | 4 | 385727 | 0.972 | 27.856 |
| yellow | 2025 | 0 | 8844223 | 20.031 | 26.317 |
| yellow | 2025 | 1 | 30325274 | 68.684 | 30.089 |
| yellow | 2025 | 2 | 4290434 | 9.717 | 25.354 |
| yellow | 2025 | 3 | 160460 | 0.363 | 26.957 |
| yellow | 2025 | 4 | 531537 | 1.204 | 31.531 |
| yellow | 2025 | 5 | 1 | 0.0 | 71.99 |
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
| green | 2024 | 620706 | 2.934 | 1.97 | 8.62 | 16.25 | 12.0 | 34.3 | 19.25 | 55.25 | 94.13 | 800.0 | 1.324 |
| green | 2025 | 558411 | 3.171 | 2.06 | 9.84 | 17.48 | 12.633 | 38.6 | 20.04 | 57.675 | 97.2 | 991.0 | 1.293 |
| green | 2026 | 317814 | 3.293 | 2.12 | 10.4 | 17.53 | 13.2 | 42.717 | 20.5 | 56.6 | 94.769 | 668.8 | 1.299 |
| yellow | 2024 | 39677841 | 3.422 | 1.8 | 14.5 | 20.06 | 13.083 | 44.05 | 21.2 | 82.69 | 104.88 | 335550.94 | 1.333 |
| yellow | 2025 | 44151929 | 3.489 | 1.89 | 13.21 | 19.65 | 13.533 | 43.95 | 22.03 | 79.03 | 104.3 | 863380.37 | 1.292 |
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
| green | 2024 | 416778 | 8 | 9893050.07 | 23.737 | 2.912 | 14.418 | 67.798 | NULL |
| green | 2025 | 374124 | 8 | 9289907.96 | 24.831 | 3.095 | 15.251 | 69.761 | 0.074 |
| green | 2026 | 317814 | 8 | 8055536.36 | 25.347 | 3.293 | 16.852 | 66.576 | 0.063 |
| yellow | 2024 | 25492745 | 8 | 722075478.03 | 28.325 | 3.422 | 16.387 | 75.939 | NULL |
| yellow | 2025 | 28683362 | 8 | 814054991.63 | 28.381 | 3.451 | 16.456 | 68.729 | 0.547 |
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
| green | 2024 | 1 | 88243 | 53 | 1665.0 |
| green | 2024 | 2 | 92991 | 53 | 1754.5 |
| green | 2024 | 3 | 95893 | 52 | 1844.1 |
| green | 2024 | 4 | 98788 | 52 | 1899.8 |
| green | 2024 | 5 | 93837 | 52 | 1804.6 |
| green | 2024 | 6 | 79515 | 52 | 1529.1 |
| green | 2024 | 7 | 71439 | 52 | 1373.8 |
| green | 2025 | 1 | 80380 | 52 | 1545.8 |
| green | 2025 | 2 | 84170 | 52 | 1618.7 |
| green | 2025 | 3 | 88507 | 53 | 1669.9 |
| green | 2025 | 4 | 88659 | 52 | 1705.0 |
| green | 2025 | 5 | 83267 | 52 | 1601.3 |
| green | 2025 | 6 | 68395 | 52 | 1315.3 |
| green | 2025 | 7 | 65033 | 52 | 1250.6 |
| green | 2026 | 1 | 45220 | 35 | 1292.0 |
| green | 2026 | 2 | 47976 | 34 | 1411.1 |
| green | 2026 | 3 | 49763 | 34 | 1463.6 |
| green | 2026 | 4 | 52520 | 35 | 1500.6 |
| green | 2026 | 5 | 47546 | 35 | 1358.5 |
| green | 2026 | 6 | 38398 | 35 | 1097.1 |
| green | 2026 | 7 | 36391 | 35 | 1039.7 |
| yellow | 2024 | 1 | 4929471 | 53 | 93008.9 |
| yellow | 2024 | 2 | 5695524 | 53 | 107462.7 |
| yellow | 2024 | 3 | 5907726 | 52 | 113610.1 |
| yellow | 2024 | 4 | 6198669 | 52 | 119205.2 |
| yellow | 2024 | 5 | 5864027 | 52 | 112769.8 |
| yellow | 2024 | 6 | 6007741 | 52 | 115533.5 |
| yellow | 2024 | 7 | 5074683 | 52 | 97590.1 |
| yellow | 2025 | 1 | 5405353 | 52 | 103949.1 |
| yellow | 2025 | 2 | 6146652 | 52 | 118204.8 |
| yellow | 2025 | 3 | 6610225 | 53 | 124721.2 |
| yellow | 2025 | 4 | 6734716 | 52 | 129513.8 |
| yellow | 2025 | 5 | 6492994 | 52 | 124865.3 |
| yellow | 2025 | 6 | 6848104 | 52 | 131694.3 |
| yellow | 2025 | 7 | 5913885 | 52 | 113728.6 |
| yellow | 2026 | 1 | 3353808 | 35 | 95823.1 |
| yellow | 2026 | 2 | 3844736 | 34 | 113080.5 |
| yellow | 2026 | 3 | 4098049 | 34 | 120530.9 |
| yellow | 2026 | 4 | 4456770 | 35 | 127336.3 |
| yellow | 2026 | 5 | 4220277 | 35 | 120579.3 |

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
| green | 2024 | 1: <1 mi | 98303 |
| green | 2024 | 2: 1-3 mi | 339107 |
| green | 2024 | 3: 3-10 mi | 161077 |
| green | 2024 | 4: 10-25 mi | 21145 |
| green | 2024 | 5: 25-100 mi | 1074 |
| green | 2025 | 1: <1 mi | 81306 |
| green | 2025 | 2: 1-3 mi | 300361 |
| green | 2025 | 3: 3-10 mi | 149679 |
| green | 2025 | 4: 10-25 mi | 25888 |
| green | 2025 | 5: 25-100 mi | 1177 |
| green | 2026 | 1: <1 mi | 44260 |
| green | 2026 | 2: 1-3 mi | 168488 |
| green | 2026 | 3: 3-10 mi | 87729 |
| green | 2026 | 4: 10-25 mi | 16776 |
| green | 2026 | 5: 25-100 mi | 561 |
| yellow | 2024 | 1: <1 mi | 8694355 |
| yellow | 2024 | 2: 1-3 mi | 19502518 |
| yellow | 2024 | 3: 3-10 mi | 8217383 |
| yellow | 2024 | 4: 10-25 mi | 3152152 |
| yellow | 2024 | 5: 25-100 mi | 111433 |
| yellow | 2025 | 1: <1 mi | 9246125 |
| yellow | 2025 | 2: 1-3 mi | 20996858 |
| yellow | 2025 | 3: 3-10 mi | 10385699 |
| yellow | 2025 | 4: 10-25 mi | 3401475 |
| yellow | 2025 | 5: 25-100 mi | 121772 |
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
| yellow | 2025 | 1 | 2025-01-20 12:07:18 | 2025-01-20 12:12:42 | 1.6 | 5.4 | 863372.12 | 863380.37 | False | False | False | False |
| yellow | 2024 | 11 | 2024-11-01 16:15:08 | 2024-11-01 16:30:32 | 2.0 | 15.4 | 335544.44 | 335550.94 | False | False | False | False |
| yellow | 2024 | 5 | 2024-05-19 22:33:09 | 2024-05-19 22:36:07 | 0.0 | 2.966666666666667 | 334076.32 | 334145.3 | False | True | False | False |
| yellow | 2025 | 6 | 2025-06-11 14:41:03 | 2025-06-11 16:14:37 | 20.6 | 93.56666666666666 | 325478.05 | 325528.45 | False | False | False | False |
| yellow | 2025 | 9 | 2025-09-02 16:01:28 | 2025-09-02 17:31:24 | 11.8 | 89.93333333333334 | 323800.27 | 323820.17 | False | False | False | False |
| yellow | 2025 | 2 | 2025-02-21 17:28:43 | 2025-02-21 17:53:04 | 2.2 | 24.35 | 132531.36 | 132555.41 | False | False | False | False |
| yellow | 2024 | 5 | 2024-05-01 18:11:01 | 2024-05-01 18:11:01 | 0.0 | 0.0 | 50558.68 | 50558.68 | False | True | True | False |
| yellow | 2025 | 3 | 2025-03-09 00:34:23 | 2025-03-09 00:40:49 | 1191.9 | 6.433333333333334 | 46263.88 | 46269.44 | False | True | False | False |
| yellow | 2024 | 6 | 2024-06-17 21:25:59 | 2024-06-17 21:25:59 | 0.0 | 0.0 | 12898.4 | 12903.4 | False | True | True | False |
| yellow | 2024 | 2 | 2024-02-29 07:56:45 | 2024-02-29 08:01:55 | 0.0 | 5.166666666666667 | 9792.0 | 9792.0 | False | True | False | False |
| yellow | 2026 | 6 | 2026-06-07 07:16:20 | 2026-06-07 07:16:20 | 0.01 | 0.0 | 7045.0 | 7053.5 | False | False | True | False |
| yellow | 2026 | 7 | 2026-07-31 09:37:10 | 2026-07-31 09:37:10 | 0.05 | 0.0 | 6466.6 | 6471.35 | False | False | True | False |
| yellow | 2024 | 11 | 2024-11-15 12:13:52 | 2024-11-15 12:22:06 | 0.1 | 8.233333333333333 | 5906.84 | 5910.84 | False | False | False | False |
| yellow | 2026 | 5 | 2026-05-25 07:20:43 | 2026-05-25 07:20:43 | 0.13 | 0.0 | 5525.99 | 5530.74 | False | False | True | False |
| yellow | 2026 | 5 | 2026-05-14 19:44:03 | 2026-05-14 19:44:03 | 0.39 | 0.0 | 5525.99 | 5530.74 | False | False | True | False |
| yellow | 2026 | 8 | 2026-08-01 17:57:35 | 2026-08-01 17:57:35 | 0.0 | 0.0 | 5525.99 | 5530.74 | False | True | True | False |
| yellow | 2026 | 5 | 2026-05-14 19:19:59 | 2026-05-14 19:19:59 | 0.0 | 0.0 | 5525.99 | 5530.74 | False | True | True | False |
| yellow | 2025 | 7 | 2025-07-17 14:30:01 | 2025-07-17 15:01:21 | 8.63 | 31.333333333333332 | 37.3 | 5297.87 | False | False | False | False |
| yellow | 2026 | 8 | 2026-08-29 23:19:18 | 2026-08-29 23:19:18 | 0.0 | 0.0 | 5050.0 | 5054.75 | False | True | True | False |
| yellow | 2026 | 8 | 2026-08-14 13:06:19 | 2026-08-14 13:06:19 | 0.0 | 0.0 | 5000.0 | 5000.0 | False | True | True | False |

**Decisión e interpretación:** No se declara fraude; son ejemplos para revisar, no datos corregidos automáticamente.
