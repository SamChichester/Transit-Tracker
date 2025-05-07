from kafka import KafkaConsumer
import psycopg2
import json
from datetime import datetime

consumer = KafkaConsumer(
    'gps_data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

conn = psycopg2.connect(dbname='transit', user='Sam')
cursor = conn.cursor()

for message in consumer:
    data = message.value
    print(f"Received: {data}")

    try:
        timestamp = datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        timestamp = datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%S")
    
    timestamp_unix = int(timestamp.timestamp())
    
    cursor.execute("""
        INSERT INTO vehicle_locations (vehicle_id, location, timestamp)
        VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, to_timestamp(%s))
    """, (
        data['vehicle_id'],
        data['longitude'],
        data['latitude'],
        timestamp_unix
    ))
    
    conn.commit()
