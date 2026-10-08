-- Distribución interpretable de distancias válidas en millas.
SELECT taxi, source_year AS year,
 CASE WHEN trip_distance < 1 THEN '1: <1 mi'
 WHEN trip_distance < 3 THEN '2: 1-3 mi'
 WHEN trip_distance < 10 THEN '3: 3-10 mi'
 WHEN trip_distance < 25 THEN '4: 10-25 mi' ELSE '5: 25-100 mi' END AS distance_bin,
 count(*) AS trips
FROM trips_valid GROUP BY ALL ORDER BY taxi, year, distance_bin;
