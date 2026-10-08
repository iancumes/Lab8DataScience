-- Conserva todos los registros; flags auditables antes de filtrar indicadores.
CREATE OR REPLACE VIEW trips_flagged AS
SELECT *, date_diff('second', pickup, dropoff) / 60.0 AS duration_min,
  coalesce(year(pickup) <> source_year OR month(pickup) <> source_month, true) AS bad_date,
  coalesce(trip_distance <= 0 OR trip_distance > 100, true) AS bad_distance,
  coalesce(date_diff('second', pickup, dropoff) <= 0
    OR date_diff('second', pickup, dropoff) > 10800, true) AS bad_duration,
  coalesce(total_amount <= 0 OR fare_amount <= 0, true) AS bad_amount
FROM trips_raw;

-- Población analítica explícita: mes correcto, 0-100 millas, 0-180 minutos,
-- tarifa e importe positivos. Los valores excluidos siguen disponibles arriba.
CREATE OR REPLACE VIEW trips_valid AS
SELECT * FROM trips_flagged
WHERE NOT (bad_date OR bad_distance OR bad_duration OR bad_amount);
