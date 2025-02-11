from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
import paho.mqtt.client as mqtt
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from React

CSV_FILE = "sensor_data.csv"
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "IC.embedded/samsungsmartfridge/compost"

# Ensure CSV file exists and is correctly formatted
def initialize_csv():
    if not os.path.exists(CSV_FILE) or os.stat(CSV_FILE).st_size == 0:
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "temperature", "moisture", "CO2", "TVOC"])

# Store new data from POST request
@app.route("/store", methods=["POST"])
def store_data():
    try:
        data = request.json  
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                data.get("temperature"),
                data.get("moisture"),
                data.get("CO2"),
                data.get("TVOC"),
            ])
        return jsonify({"message": "Data saved"}), 200
    except Exception as e:
        return jsonify({"error": f"CSV Write Error: {e}"}), 500

# API to get the latest reading
@app.route("/latest", methods=["GET"])
def get_latest_data():
    try:
        with open(CSV_FILE, "r") as f:
            reader = list(csv.reader(f))
            if len(reader) > 1:
                last_entry = reader[-1]
                return jsonify({
                    "timestamp": last_entry[0],
                    "temperature": float(last_entry[1]),
                    "moisture": float(last_entry[2]),
                    "CO2": float(last_entry[3]),
                    "TVOC": float(last_entry[4])
                }), 200
        return jsonify({"error": "No data available"}), 404
    except Exception as e:
        return jsonify({"error": f"CSV Read Error: {e}"}), 500

# API to get the last 60 readings for historical display
@app.route("/history", methods=["GET"])
def get_history():
    try:
        with open(CSV_FILE, "r") as f:
            reader = list(csv.reader(f))

            if len(reader) > 1:
                header = reader[0]  # Extract header
                if header != ["timestamp", "temperature", "moisture", "CO2", "TVOC"]:
                    print("Warning: CSV header mismatch. Check the CSV file format.")

                data = []
                for row in reader[1:]:  # Skip the first row (header)
                    try:
                        entry = {
                            "timestamp": row[0],
                            "temperature": float(row[1]),
                            "moisture": float(row[2]),
                            "CO2": float(row[3]),
                            "TVOC": float(row[4])
                        }
                        data.append(entry)
                    except ValueError as e:
                        print(f"Skipping invalid row: {row}, Error: {e}")

                print(f"Returning {len(data)} historical entries")  # Debug print
                return jsonify(data), 200

        return jsonify([]), 200
    except Exception as e:
        print(f"Error in /history: {e}")
        return jsonify({"error": f"CSV Read Error: {e}"}), 500


# MQTT Callback: When message is received, store in CSV
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                payload.get("temperature"),
                payload.get("moisture"),
                payload.get("CO2"),
                payload.get("TVOC"),
            ])
        print(f"MQTT Data Saved: {payload}")
    except json.JSONDecodeError:
        print("Error: Received invalid JSON payload.")
    except Exception as e:
        print(f"Error saving MQTT data: {e}")

# Set up MQTT client
def setup_mqtt():
    try:
        client = mqtt.Client()
        client.on_message = on_message
        client.connect(MQTT_BROKER, 1883, 60)
        client.subscribe(MQTT_TOPIC)
        client.loop_start()
    except Exception as e:
        print(f"MQTT Setup Error: {e}")

if __name__ == "__main__":
    initialize_csv()
    setup_mqtt()  # Start MQTT listener
    app.run(host="0.0.0.0", port=5000)
