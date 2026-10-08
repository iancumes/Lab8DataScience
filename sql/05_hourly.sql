-- Perfil horario; usa hora local declarada en el archivo TLC, sin convertir UTC.
SELECT taxi, source_year AS year, hour(pickup) AS hour,
 count(*) AS trips, round(avg(total_amount), 3) AS avg_total_usd
FROM trips_valid GROUP BY ALL ORDER BY taxi, year, hour;
