SELECT taxi, hour(pickup) AS hour, count(*) AS trips,
 avg(trip_distance) AS avg_miles
FROM {source} GROUP BY ALL ORDER BY taxi, hour;
