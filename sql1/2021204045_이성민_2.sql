SET NAMES 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci';
SELECT p.pilot_name
FROM pilots p
JOIN airports a ON p.pilot_workplace = a.airport_code
WHERE a.airport_country = '한국';