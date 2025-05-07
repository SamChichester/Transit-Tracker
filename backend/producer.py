from kafka import KafkaProducer
import requests
import time
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

FEED_URL = f"https://developer.trimet.org/ws/v2/vehicles?appID={os.environ.get('API_ID')}"

while True:
    response = requests.get(FEED_URL)

    if response.status_code == 200:
        data = response.json()
        vehicles = data.get("resultSet", {}).get("vehicle", [])
        for vehicle in vehicles:
            timestamp_seconds = vehicle.get("time") / 1000.0
            timestamp_dt = datetime.utcfromtimestamp(timestamp_seconds)
            timestamp_iso = timestamp_dt.isoformat()

            message = {
                "vehicle_id": vehicle.get("vehicleID"),
                "route_id": vehicle.get("routeNumber"),
                "latitude": vehicle.get("latitude"),
                "longitude": vehicle.get("longitude"),
                "timestamp": timestamp_iso
            }

            producer.send("gps_data", message)
        
    time.sleep(3)
