-- Ejemplos de importes extremos SIN filtrar; se conservan para auditoría.
SELECT taxi, source_year, source_month, pickup, dropoff, trip_distance,
 duration_min, fare_amount, total_amount, bad_date, bad_distance, bad_duration, bad_amount
FROM trips_flagged ORDER BY total_amount DESC NULLS LAST LIMIT 20;
