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
