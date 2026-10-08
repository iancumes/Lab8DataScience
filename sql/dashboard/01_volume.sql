-- Volumen mensual por tipo. La escala log permite observar green; 2026 es parcial.
SELECT period, taxi, trips AS value FROM monthly ORDER BY period, taxi;
