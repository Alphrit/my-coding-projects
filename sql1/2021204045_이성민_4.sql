SELECT a.airliner_capacity
FROM airliners a
JOIN reservation r ON a.airlinder_id = r.airliner_id
WHERE r.reservation_date = (SELECT MAX(reservation_date) FROM reservation);