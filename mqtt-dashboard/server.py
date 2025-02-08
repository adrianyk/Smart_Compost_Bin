from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
import paho.mqtt.client as mqtt
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from React

# Directory to store CSV files for each device
CSV_DIRECTORY = "sensor_data"

# MQTT Broker Configuration
MQTT_BROKER = "test.mosquitto.org"
BASE_TOPIC = "IC.embedded/samsungsmartfridge/compost"

# Ensure the sensor data directory exists
def initialize_csv_directory():
    try:
        if not os.path.exists(CSV_DIRECTORY):
            os.makedirs(CSV_DIRECTORY)
    except Exception as e:
        print(f"Error initializing CSV directory: {e}")

# Ensure CSV file exists and is correctly formatted for a given device (MAC address)
def initialize_csv(mac_address):
    try:
        csv_file = os.path.join(CSV_DIRECTORY, f"{mac_address}_sensor_data.csv")
        if os.path.exists(csv_file):
            with open(csv_file, "r+", newline="") as f:
                reader = csv.reader(f)
                headers = next(reader, None)

                # If file is empty or headers are incorrect, reset file
                if headers != ["timestamp", "temperature", "moisture", "CO2", "TVOC"]:
                    print("CSV file format incorrect or empty. Resetting file...")
                    f.seek(0)
                    f.truncate()
                    writer = csv.writer(f)
                    writer.writerow(["timestamp", "temperature", "moisture", "CO2", "TVOC"])
        else:
            with open(csv_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "temperature", "moisture", "CO2", "TVOC"])
    except Exception as e:
        print(f"Error initializing CSV file for {mac_address}: {e}")

# Store new data from POST request (using MAC address to identify the file)
@app.route("/store", methods=["POST"])
def store_data():
    try:
        data = request.json  # Expect JSON format
        mac_address = data.get("device_id")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not mac_address:
            return jsonify({"error": "MAC address required"}), 400
        
        # Initialize CSV file for this device
        initialize_csv(mac_address)

        csv_file = os.path.join(CSV_DIRECTORY, f"{mac_address}_sensor_data.csv")
        with open(csv_file, "a", newline="") as f:
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

# API to get the last 60 readings for a specific device (using MAC address)
@app.route("/data", methods=["GET"])
def get_data():
    try:
        mac_address = request.args.get("device_id")
        csv_file = os.path.join(CSV_DIRECTORY, f"{mac_address}_sensor_data.csv")
        if not os.path.exists(csv_file):
            return jsonify({"error": f"No data found for MAC address {mac_address}"}), 404
        
        with open(csv_file, "r") as f:
            reader = list(csv.reader(f))
            data = reader[-60:] if len(reader) > 1 else []
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"CSV Read Error: {e}"}), 500

# MQTT Callback: When message is received, store in CSV
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        mac_address = payload.get("device_id")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not mac_address:
            print("Error: Missing MAC address in payload.")
            return

        # Initialize CSV file for this device
        initialize_csv(mac_address)
        
        csv_file = os.path.join(CSV_DIRECTORY, f"{mac_address}_sensor_data.csv")
        with open(csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                payload.get("temperature"),
                payload.get("moisture"),
                payload.get("CO2"),
                payload.get("TVOC"),
            ])
        print(f"MQTT Data Saved for {mac_address}: {payload}")
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
        
        # Subscribe to the BASE_TOPIC (which will handle dynamic device subscriptions)
        client.subscribe(f"{BASE_TOPIC}/#")
        client.loop_start()
    except Exception as e:
        print(f"MQTT Setup Error: {e}")

if __name__ == "__main__":
    initialize_csv_directory()  # Ensure the CSV directory exists
    setup_mqtt()  # Start MQTT listener
    app.run(host="0.0.0.0", port=5000)
