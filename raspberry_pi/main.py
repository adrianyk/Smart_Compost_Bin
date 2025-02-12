import time
import smbus2
import json
import socket
import uuid
import math
import paho.mqtt.client as mqtt

# Constants for Temperature Sensor (Si7021)
SI7021_ADDR = 0x40
SI7021_TEMP_CMD = 0xF3

# Constants for Moisture Sensor via ADC (ADS1115)
ADS1115_ADDR = 0x48
ADS1115_CONVERSION_REG = 0x00
ADS1115_CONFIG_REG = 0x01
ADS1115_CONFIG = 0x8583

# Constants for Gas Sensor (CCS811)
CCS811_ADDR = 0x5A
CCS811_STATUS_REG = 0x00
CCS811_MEAS_MODE_REG = 0x01
CCS811_ALG_RESULT_DATA = 0x02
CCS811_APP_START = 0xF4
CCS811_HW_ID = 0x20

# Global I2C bus initialization
BUS = smbus2.SMBus(1)

# WiFi Credentials (Handled by Raspberry Pi OS)
SSID = "ImperialWifi"  # No need to manually connect in script
PASSWORD = "imperialwifi1!"

# MQTT Broker Configuration
MQTT_BROKER = "test.mosquitto.org"
BASE_TOPIC = "IC.embedded/samsungsmartfridge/compost"

# Initialize MQTT topic and device ID using last 6 hex characters of MAC
DEVICE_ID = hex(uuid.getnode())[-6:]
MQTT_TOPIC = f"{BASE_TOPIC}/{DEVICE_ID}"

# MQTT Client Setup
def setup_mqtt():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, 1883, 60)
    print(f"Connected to MQTT Broker, publishing to {MQTT_TOPIC}")
    return client

# Get Raspberry Pi's local IP address
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"

def read_temperature():
    try:
        # Set up a command for measuring temperature
        cmd_meas_temp = smbus2.i2c_msg.write(SI7021_ADDR, [SI7021_TEMP_CMD])
        
        # Set up a read command that reads two bytes of data
        read_result = smbus2.i2c_msg.read(SI7021_ADDR, 2)

        BUS.i2c_rdwr(cmd_meas_temp)
        time.sleep(0.1)  # Allow sensor time to measure
        BUS.i2c_rdwr(read_result)

        # Combine bytes
        raw_temp = (read_result.buf[0][0] << 8) | read_result.buf[1][0]
        temp_celcius = (175.72 * raw_temp / 65536) - 46.85  # datasheet

        return temp_celcius

    except Exception as e:
        print("Error reading temperature sensor:", e)
        return None

def read_moisture():
    try:
        # Convert CONFIG to two bytes in big-endian order
        config_bytes = ADS1115_CONFIG.to_bytes(2, byteorder='big')
    
        # Write the configuration to the CONFIG_REG to start a single-shot conversion
        BUS.write_i2c_block_data(ADS1115_ADDR, ADS1115_CONFIG_REG, list(config_bytes))
    
        # Wait for conversion to complete (100ms is sufficient for 128 SPS)
        time.sleep(0.1)
    
        # Read the conversion result (2 bytes from the conversion register)
        data = BUS.read_i2c_block_data(ADS1115_ADDR, ADS1115_CONVERSION_REG, 2)
        adc_value = int.from_bytes(data, byteorder='big', signed=True)
        
        min_moisture = 20700
        max_moisture = 1700
        
        moisture_percent = ((adc_value - min_moisture) / (max_moisture - min_moisture)) * 100
        moisture_percent = max(0, min(100, moisture_percent))  # Clamp to 0-100%
        
        return moisture_percent
    
    except Exception as e:
        print("Error reading moisture sensor:", e)
        return None

def initialize_gas_sensor():
    try:
        print("Resetting CCS811 sensor...")
        
        # Start the application firmware on the CCS811
        BUS.write_byte(CCS811_ADDR, CCS811_APP_START)
        time.sleep(1)  # Allow the sensor to start

        # Set mode to read every second
        BUS.write_byte_data(CCS811_ADDR, CCS811_MEAS_MODE_REG, 0x10)
        print("Gas sensor is ready. Waiting 20 seconds for stabilization...")
        time.sleep(20)
        
    except Exception as e:
        print("Error initializing gas sensor:", e)

def read_gas_sensor(num_samples=5):
    co2_readings = []
    tvoc_readings = []
    
    for i in range(num_samples):
        print(i)
        try:
            status = BUS.read_byte_data(CCS811_ADDR, CCS811_STATUS_REG)
            
            if status & 0x08:   # Data ready
                data = BUS.read_i2c_block_data(CCS811_ADDR, CCS811_ALG_RESULT_DATA, 8)
                co2 = (data[0] << 8) | (data[1] & 0xFF)
                tvoc = (data[2] << 8) | (data[3] & 0xFF)
                print(f"CO2: {co2}, TVOC: {tvoc}")

                if 0 <= co2 <= 10000 and 0 <= tvoc <= 3000:
                    co2_readings.append(co2)
                    tvoc_readings.append(tvoc)
                    print(f"Valid readings collected: co2 {co2_readings}, tvoc {tvoc_readings}")
                else:
                    # Ignore unrealistic readings
                    print("Unstable gas reading detected, skipping...")
            
        except Exception as e:
            print("Error reading gas sensor:", e)

        time.sleep(0.5)
        
    # Compute average if we have valid readings, otherwise return None
    if co2_readings and tvoc_readings:
        print(f"len(co2_readings): {len(co2_readings)}, len(tvoc_readings): {len(tvoc_readings)}")
        avg_co2 = sum(co2_readings) / len(co2_readings)
        avg_tvoc = sum(tvoc_readings) / len(tvoc_readings)
        return {"co2": avg_co2, "tvoc": avg_tvoc}
    
    return None

def temperature_score(temp):
    optimal_temp = 55
    acceptable_range = 15
    
    # Linear peak function: calcs temp score where ideal temp (55°C) gets highest score
    score = 1 - abs((temp - optimal_temp) / acceptable_range)
    return max(0, score)

def moisture_score(moisture):
    optimal_moisture = 55
    acceptable_range = 15
    
    # Linear peak function: calcs moisture score where ideal range (50-60%) gets highest score
    score = 1 - abs((moisture - optimal_moisture) / acceptable_range)
    return max(0, score)

def aeration_score(co2, tvoc):
    # Bell-shaped curve: calcs aeration score where ideal range CO2 & TVOC gets highest score
    optimal_co2 = 1200              # Around 1000-1500 ppm is ideal
    acceptable_co2_range = 1000     # Spread of ideal range (500-2500)
    co2_score = math.exp(-((co2 - optimal_co2) / acceptable_co2_range) ** 2)
    
    optimal_tvoc = 300              # Around 200-400 ppb is ideal
    acceptable_tvoc_range = 300     # Spread of ideal range (0-600)
    tvoc_score = math.exp(-((tvoc - optimal_tvoc) / acceptable_tvoc_range) ** 2)
    
    return (co2_score + tvoc_score) / 2

def chi_score(temp, moisture, co2, tvoc):
    # Calcs CHI score as weighted sum
    temp_score = temperature_score(temp)
    moist_score = moisture_score(moisture)
    gas_score = aeration_score(co2, tvoc)
    
    return (0.4 * temp_score) + (0.4 * moist_score) + (0.2 * gas_score)

def main():
    print(f"Device ID: {DEVICE_ID}")
    print(f"MQTT Topic: {MQTT_TOPIC}")
    
    client = setup_mqtt()
    
    initialize_gas_sensor() # Initialize the gas sensor (if needed)
    
    while True:
        start_time = time.time()
        
        temp = read_temperature()
        moisture = read_moisture()
        gas = read_gas_sensor(num_samples=5)
        
        co2, tvoc = (-1.0, -1.0) if gas is None else (gas["co2"], gas["tvoc"])

        chi = chi_score(temp, moisture, co2, tvoc)
        if co2 == -1:
            aeration = -1
        else:
            aeration = aeration_score(co2, tvoc)
        
        # Format data as JSON
        data = {
            "device_id": DEVICE_ID,
            "device_ip": get_ip(),
            "temperature": round(temp, 2) if temp is not None else None,
            "moisture": round(moisture, 2) if moisture is not None else None,
            "CO2": round(co2, 2),
            "TVOC": round(tvoc, 2),
            "aeration_score": round(aeration, 2),
            "chi_score": round(chi, 2)
        }
        
        payload = json.dumps(data)
        client.publish(MQTT_TOPIC, payload)
        print(f"Published to {MQTT_TOPIC}: {payload}\n")
        
        end_time = time.time()
        elapsed_time = end_time - start_time

        time.sleep(5 - elapsed_time) # Read every second
    
if __name__ == "__main__":
    main()
