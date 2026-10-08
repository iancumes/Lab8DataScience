SELECT taxi, source_year, source_month, count(*) AS trips,
 sum(total_amount::DECIMAL(18,2)) AS total_usd
FROM {source} GROUP BY ALL ORDER BY taxi, source_year, source_month;
