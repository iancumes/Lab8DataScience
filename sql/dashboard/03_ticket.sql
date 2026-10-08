-- Importe medio por viaje válido. Cambios de composición y valores extremos afectan la media.
SELECT period, taxi, avg_total_usd AS value FROM monthly ORDER BY period, taxi;
