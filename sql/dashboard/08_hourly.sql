-- Participación horaria dentro de cada año/taxi. Normalizar evita confundir meses de exposición con comportamiento horario.
SELECT hour, taxi || ' ' || year::VARCHAR AS series, round(100.0*trips/sum(trips) OVER (PARTITION BY taxi,year),3) AS value FROM hourly ORDER BY hour, series;
