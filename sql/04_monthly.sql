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
