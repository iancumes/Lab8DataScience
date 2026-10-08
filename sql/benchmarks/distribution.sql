SELECT taxi, quantile_cont(total_amount, 0.5) AS median_usd,
 quantile_cont(total_amount, 0.95) AS p95_usd
FROM {source} GROUP BY taxi ORDER BY taxi;
