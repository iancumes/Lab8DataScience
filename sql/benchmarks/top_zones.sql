SELECT taxi, pu_location_id, count(*) AS trips
FROM {source} WHERE trip_distance > 0 AND total_amount > 0
GROUP BY ALL ORDER BY trips DESC, taxi, pu_location_id LIMIT 20;
