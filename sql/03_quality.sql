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
