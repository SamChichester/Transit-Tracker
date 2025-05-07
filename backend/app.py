from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

conn = psycopg2.connect(
    dbname="transit",
    user="Sam",
    host="localhost"
)
cursor = conn.cursor()

@app.route('/locations', methods=['GET'])
def get_locations():
    cursor.execute("""
        SELECT vehicle_id, ST_X(location::geometry), ST_Y(location::geometry),
               speed, heading, timestamp
        FROM (
            SELECT DISTINCT ON (vehicle_id) * 
            FROM vehicle_locations
            ORDER BY vehicle_id, timestamp DESC
        ) AS latest
    """)

    rows = cursor.fetchall()

    data = [{
        'vehicle_id': r[0],
        'longitude': r[1],
        'latitude': r[2],
        'speed': r[3],
        'heading': r[4],
        'timestamp': r[5].isoformat()
    } for r in rows]

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)