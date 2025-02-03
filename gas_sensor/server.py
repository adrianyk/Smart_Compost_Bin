from flask import Flask, jsonify, render_template
import time
import smbus2

app = Flask(__name__)

# CCS811 I2C Address
CCS811_ADDR = 0x5A
STATUS_REG = 0x00
MEAS_MODE_REG = 0x01
ALG_RESULT_DATA = 0x02
APP_START = 0xF4
HW_ID = 0x20
RESET_REG = 0xFF  # Reset register

# Software reset sequence (as per CCS811 datasheet)
RESET_COMMAND = [0x11, 0xE5, 0x72, 0x8A]

# Initialize I2C
bus = smbus2.SMBus(1)

# Store last valid sensor values to prevent missing data
last_valid_co2 = 400  # Default safe CO₂ value
last_valid_tvoc = 0  # Default safe TVOC value

# 🛠 Step 1: Reset the sensor before starting
print("🔄 Resetting CCS811 sensor...")
bus.write_i2c_block_data(CCS811_ADDR, RESET_REG, RESET_COMMAND)
time.sleep(2)  # Wait 2 seconds for reset

# 🛠 Step 2: Check if the sensor is connected
try:
    hw_id = bus.read_byte_data(CCS811_ADDR, HW_ID)
    if hw_id != 0x81:
        print("❌ Error: CCS811 not detected! Check wiring.")
        exit()
except OSError:
    print("⚠️ I2C communication error! Sensor may not be connected properly.")
    exit()

print("✅ CCS811 detected successfully!")

# 🛠 Step 3: Start the sensor application
bus.write_byte(CCS811_ADDR, APP_START)
time.sleep(1)  # Allow sensor to start

# Set mode to read every second
bus.write_byte_data(CCS811_ADDR, MEAS_MODE_REG, 0x10)

# 🛠 Step 4: Allow the sensor to warm up
print("⏳ Waiting 10 seconds for sensor stabilization...")
time.sleep(10)

def read_sensor():
    """ Reads CO₂ and TVOC values from the CCS811 sensor, filtering out invalid readings. """
    global last_valid_co2, last_valid_tvoc

    try:
        status = bus.read_byte_data(CCS811_ADDR, STATUS_REG)
        if status & 0x08:  # Data ready
            data = bus.read_i2c_block_data(CCS811_ADDR, ALG_RESULT_DATA, 8)
            co2 = (data[0] << 8) | (data[1] & 0xFF)
            tvoc = (data[2] << 8) | (data[3] & 0xFF)

            # Ignore unrealistic readings
            if co2 > 5000 or tvoc > 2000:
                print("⚠️ Unstable reading detected, using last valid values...")
                return {"co2": last_valid_co2, "tvoc": last_valid_tvoc}
            
            # Update last valid readings
            last_valid_co2 = co2
            last_valid_tvoc = tvoc
            return {"co2": co2, "tvoc": tvoc}
    
    except Exception as e:
        print(f"⚠️ Sensor error: {e}")

    # Return last valid values if there's an error
    return {"co2": last_valid_co2, "tvoc": last_valid_tvoc}

# Import the Compost Recommendation Algorithm
from compost_algorithm import compost_recommendation  # Ensure this script exists

@app.route("/")
def index():
    """ Serves the main web page. """
    return render_template("dashboard.html")

@app.route("/sensor")
def sensor_data():
    """ Provides sensor data as a JSON API with recommendations. """
    air_quality = read_sensor()
    temperature = 100  # Dummy value for now
    moisture = 50  # Dummy value for now

    # Ensure recommendations always exist
    recommendations = {"compact_summary": "No recommendations available."}

    if air_quality["co2"] is not None and air_quality["tvoc"] is not None:
        recommendations = compost_recommendation(
            air_quality["co2"], air_quality["tvoc"], temperature, moisture
        )

        print(f"📌 Debug - API Response: {recommendations}")  # ✅ Debugging log

    return jsonify({
        "co2": air_quality["co2"],
        "tvoc": air_quality["tvoc"],
        "temperature": temperature,
        "moisture": moisture,
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)