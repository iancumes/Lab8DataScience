-- Suma de total_amount en viajes válidos. Incluye cargos; no representa utilidad.
SELECT period, taxi, total_usd AS value FROM monthly ORDER BY period, taxi;
