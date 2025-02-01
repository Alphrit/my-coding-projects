SELECT r.airliner_id, AVG(p.passenger_age) AS avg_passenger_age
FROM reservation r
JOIN passengers p ON r.passenger_id = p.passenger_id
GROUP BY r.airliner_id
ORDER BY avg_passenger_age DESC;