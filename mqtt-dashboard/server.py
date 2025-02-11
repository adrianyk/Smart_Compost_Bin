from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
import paho.mqtt.client as mqtt
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from React

DEVICES_DIR = "mqtt-dashboard/devices"  # Directory to store multiple device data
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "IC.embedded/samsungsmartfridge/compost"

# Ensure devices directory exists
if not os.path.exists(DEVICES_DIR):
    os.makedirs(DEVICES_DIR)

# Get CSV file path for a given device
def get_csv_filename(device_id):
    return os.path.join(DEVICES_DIR, f"{device_id}.csv")

# Ensure CSV file exists with proper headers
def initialize_csv(device_id):
    csv_file = get_csv_filename(device_id)
    if not os.path.exists(csv_file) or os.stat(csv_file).st_size == 0:
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "temperature", "moisture", "CO2", "TVOC"])

# API to get the list of devices (CSV files)
@app.route("/devices", methods=["GET"])
def get_devices():
    device_files = os.listdir(DEVICES_DIR)
    devices = [file.replace(".csv", "") for file in device_files if file.endswith(".csv")]
    return jsonify(devices), 200

# API to get the latest reading for a device
@app.route("/latest/<device_id>", methods=["GET"])
def get_latest_data(device_id):
    csv_file = get_csv_filename(device_id)
    if not os.path.exists(csv_file):
        return jsonify({"error": "Device data not found"}), 404

    with open(csv_file, "r") as f:
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

# API to get historical data for a device
@app.route("/history/<device_id>", methods=["GET"])
def get_history(device_id):
    csv_file = get_csv_filename(device_id)
    if not os.path.exists(csv_file):
        return jsonify({"error": "Device data not found"}), 404

    with open(csv_file, "r") as f:
        reader = list(csv.reader(f))
        if len(reader) > 1:
            data = [
                {"timestamp": row[0], "temperature": float(row[1]), "moisture": float(row[2]),
                 "CO2": float(row[3]), "TVOC": float(row[4])}
                for row in reader[1:]  # Skip header row
            ]
            return jsonify(data[-60:]), 200  # Return last 60 entries
    return jsonify([]), 200

# MQTT Callback: Store incoming messages per device
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        device_id = payload.get("device_id")

        if not device_id:
            print("Received data missing device_id")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        initialize_csv(device_id)  # Ensure CSV file exists

        csv_file = get_csv_filename(device_id)
        with open(csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                payload.get("temperature"),
                payload.get("moisture"),
                payload.get("CO2"),
                payload.get("TVOC"),
            ])
        print(f"Data saved for {device_id}: {payload}")

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
        client.subscribe(f"{MQTT_TOPIC}/+")
        client.loop_start()
    except Exception as e:
        print(f"MQTT Setup Error: {e}")

if __name__ == "__main__":
    setup_mqtt()
    app.run(host="0.0.0.0", port=5000)
