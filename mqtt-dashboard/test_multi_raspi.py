import time
import json
import random
import uuid
import paho.mqtt.client as mqtt

# MQTT Broker Configuration
MQTT_BROKER = "test.mosquitto.org"
BASE_TOPIC = "IC.embedded/samsungsmartfridge/compost"

# Simulated device MAC addresses (last 6 hex characters)
SIMULATED_DEVICES = [
    hex(uuid.getnode())[-6:],
    "a1b2c3",
    "d4e5f6",
    "789abc"
]

# MQTT Client Setup
def setup_mqtt():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, 1883, 60)
    print(f"Connected to MQTT Broker at {MQTT_BROKER}")
    return client

# Generate random sensor data
def generate_sensor_data(device_id):
    return {
        "device_id": device_id,
        "device_ip": f"192.168.0.{random.randint(2, 254)}",
        "temperature": round(random.uniform(15, 35), 2),
        "moisture": round(random.uniform(10, 90), 2),
        "CO2": round(random.uniform(400, 1000), 2),
        "TVOC": round(random.uniform(50, 500), 2),
    }

# Main loop to simulate multiple devices publishing data
def main():
    client = setup_mqtt()

    while True:
        for device_id in SIMULATED_DEVICES:
            topic = f"{BASE_TOPIC}/{device_id}"
            data = generate_sensor_data(device_id)
            payload = json.dumps(data)

            client.publish(topic, payload)
            print(f"Published to {topic}: {payload}")

        time.sleep(5)  # Wait 5 seconds before next round

if __name__ == "__main__":
    main()
