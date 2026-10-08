-- Conteo de viajes válidos solo en meses presentes en ambos taxis y todos los años. No extrapola el resto de 2026.
SELECT year::VARCHAR AS year, taxi, trips AS value FROM common_months ORDER BY year, taxi;
