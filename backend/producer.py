from kafka import KafkaProducer
from google.transit import gtfs_realtime_pb2
import requests
import time
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

FEED_URL = "https://api-v3.mbta.com/gtfs/vehicle_positions.pb"

while True:
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(FEED_URL)
    feed.ParseFromString(response.content)

    for entity in feed.entity:
        if entity.HasField('vehicle'):
            v = entity.vehicle
            message = {
                "vehicle_id": v.vehicle.id,
                "route_id": v.trip.route_id,
                "latitude": v.position.latitude,
                "longitude": v.position.longitude,
                "timestamp": v.timestamp
            }

            producer.send("gps_data", message)
    time.sleep(10)
