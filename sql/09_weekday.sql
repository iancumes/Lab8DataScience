-- Ajusta por días observados: totales por día de semana pueden confundir exposición.
SELECT taxi, source_year AS year, isodow(pickup) AS weekday,
 count(*) AS trips, count(DISTINCT pickup::DATE) AS observed_days,
 round(count(*)::DOUBLE/count(DISTINCT pickup::DATE), 1) AS trips_per_observed_day
FROM trips_valid GROUP BY ALL ORDER BY taxi, year, weekday;
