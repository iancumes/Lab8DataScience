-- Mediana de duración en viajes válidos, limitada a 180 minutos por regla operativa.
SELECT period, taxi, median_minutes AS value FROM monthly ORDER BY period, taxi;
