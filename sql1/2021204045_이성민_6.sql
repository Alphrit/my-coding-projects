SELECT p.passenger_name, p.passenger_age
FROM passengers p
JOIN reservation r ON p.passenger_id = r.passenger_id
GROUP BY p.passenger_id, p.passenger_name, p.passenger_age
HAVING COUNT(r.reservation_id) >= 3
ORDER BY p.passenger_age DESC
LIMIT 1;