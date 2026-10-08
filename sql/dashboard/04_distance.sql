-- Mediana de distancia en viajes válidos. Comparar con las colas p95/p99 del informe.
SELECT period, taxi, median_miles AS value FROM monthly ORDER BY period, taxi;
