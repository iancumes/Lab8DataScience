-- Porcentaje de filas que incumplen al menos una regla operativa. Los motivos se solapan; no se suman. No todo viaje excluido es falso.
SELECT source_year::VARCHAR AS year, taxi, excluded_pct AS value FROM quality ORDER BY year, taxi;
