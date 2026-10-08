-- 100 × suma(propina)/suma(tarifa), solo tarjeta y propina no negativa. No mide propinas en efectivo.
SELECT period, taxi, card_tip_pct AS value FROM monthly ORDER BY period, taxi;
