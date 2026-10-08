-- Muestra de conveniencia de 10 filas por tipo. No sirve para estimar indicadores.
(SELECT * FROM trips_raw WHERE taxi='yellow' LIMIT 10)
UNION ALL
(SELECT * FROM trips_raw WHERE taxi='green' LIMIT 10);
