-- Códigos: 0=Flex Fare, 1=crédito, 2=efectivo, 3=sin cargo, 4=disputa,
-- 5=desconocido, 6=anulado. NULL/otros se conservan para auditar.
SELECT taxi, source_year AS year, payment_type, count(*) AS trips,
 round(100.0*count(*) / sum(count(*)) OVER (PARTITION BY taxi, source_year), 3) AS share_pct,
 round(avg(total_amount), 3) AS avg_total_usd
FROM trips_valid GROUP BY taxi, source_year, payment_type ORDER BY taxi, year, payment_type;
