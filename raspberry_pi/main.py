import time
import smbus2
import json
import socket
import uuid
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

def read_gas_sensor():
    try:
        status = BUS.read_byte_data(CCS811_ADDR, CCS811_STATUS_REG)
        
        if status & 0x08:   # Data ready
            data = BUS.read_i2c_block_data(CCS811_ADDR, CCS811_ALG_RESULT_DATA, 8)
            co2 = (data[0] << 8) | (data[1] & 0xFF)
            tvoc = (data[2] << 8) | (data[3] & 0xFF)

            # Ignore unrealistic readings
            if co2 > 5000 or tvoc > 2000:
                print("Unstable gas reading detected, skipping...")
                return None
            
            return {"co2": co2, "tvoc": tvoc}
        
    except Exception as e:
        print("Error reading gas sensor:", e)
        
    return None

def main():
    print(f"Device ID: {DEVICE_ID}")
    print(f"MQTT Topic: {MQTT_TOPIC}")
    
    client = setup_mqtt()
    
    initialize_gas_sensor() # Initialize the gas sensor (if needed)
    
    while True:
        temp = read_temperature()
        moisture = read_moisture()
        gas = read_gas_sensor()
        
        CO2, TVOC = (-1.0, -1.0) if gas is None else (gas["co2"], gas["tvoc"])

        # Format data as JSON
        data = {
            "device_id": DEVICE_ID,
            "device_ip": get_ip(),
            "temperature": round(temp, 2) if temp is not None else None,
            "moisture": round(moisture, 2) if moisture is not None else None,
            "CO2": round(CO2, 2),
            "TVOC": round(TVOC, 2)
        }
        
        payload = json.dumps(data)
        client.publish(MQTT_TOPIC, payload)
        print(f"Published to {MQTT_TOPIC}: {payload}\n")

        time.sleep(5) # Read every second
    
if __name__ == "__main__":
    main()
