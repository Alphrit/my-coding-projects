SELECT r.airliner_id, r.passenger_id, r.departure_code, r.arrival_code
FROM reservation r
WHERE r.airliner_id = 'DB409';