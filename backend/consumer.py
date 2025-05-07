from kafka import KafkaConsumer
import psycopg2
import json

consumer = KafkaConsumer(
    'vehicle-locations',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

conn = psycopg2.connect(dbname='transit', user='sam')
cursor = conn.cursor()

for message in consumer:
    data = message.value
    print(f"Received: {data}")
    
    cursor.execute("""
        INSERT INTO vehicle_locations (vehicle_id, location, speed, heading, timestamp)
        VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, %s, %s, to_timestamp(%s))
    """, (
        data['vehicle_id'],
        data['longitude'],
        data['latitude'],
        data['speed'],
        data['heading'],
        data['timestamp']
    ))
    
    conn.commit()
