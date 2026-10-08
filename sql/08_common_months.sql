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
