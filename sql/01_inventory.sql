-- Archivos y filas por año/tipo, leyendo Parquet sin importar previamente.
SELECT taxi, source_year, count(DISTINCT source_file) AS files,
       count(*) AS rows, min(pickup) AS earliest_pickup, max(pickup) AS latest_pickup
FROM trips_raw GROUP BY ALL ORDER BY taxi, source_year;
