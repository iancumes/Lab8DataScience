-- Porcentaje de viajes válidos con payment_type=1. Otros códigos no equivalen automáticamente a efectivo.
SELECT period, taxi, credit_pct AS value FROM monthly ORDER BY period, taxi;
