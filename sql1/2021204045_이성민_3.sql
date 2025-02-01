SET NAMES 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci';
SELECT r.reservation_id, r.passenger_id, r.reservation_date
FROM reservation r
JOIN airports a ON r.departure_code = a.airport_code
WHERE a.airport_country = '미국';