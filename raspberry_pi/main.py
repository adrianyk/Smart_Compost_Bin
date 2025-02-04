import time
import smbus2
import json
import socket
import random
import paho.mqtt.client as mqtt

# WiFi Credentials (Handled by Raspberry Pi OS)
SSID = "ImperialWifi"  # No need to manually connect in script
PASSWORD = "imperialwifi1!"

# MQTT Broker Configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "IC.embedded/samsungsmartfridge/compost"

# Temperature Sensor (Si7021)
SI7021_ADDR = 0x40
SI7021_TEMP_CMD = 0xF3

# Moisture Sensor via ADC (ADS1115)
ADS1115_ADDR = 0x48
ADS1115_CONVERSION_REG = 0x00
ADS1115_CONFIG_REG = 0x01
ADS1115_CONFIG = 0x8583
""" The configuration value for a single-shot conversion on A0.
This configuration uses:
 - OS (bit 15) = 1 (start a conversion)
 - MUX (bits 14:12) = 100 for A0 vs. GND
 - PGA (bits 11:9) = 010 for ±2.048V
 - MODE (bit 8) = 1 for single-shot mode
 - DR (bits 7:5) = 100 for 128 SPS
 - Comparator bits (bits 4:0) = default (disabled) """

# Gas Sensor (CCS811)
CCS811_ADDR = 0x5A
CCS811_STATUS_REG = 0x00
CCS811_MEAS_MODE_REG = 0x01
CCS811_ALG_RESULT_DATA = 0x02
CCS811_APP_START = 0xF4
CCS811_HW_ID = 0x20

# Initialize a single I2C bus (bus number 1 is typical on a Raspberry Pi Zero)
bus = smbus2.SMBus(1)

def read_temperature():
    try:
        # Set up a command for measuring temperature
        cmd_meas_temp = smbus2.i2c_msg.write(SI7021_ADDR, [SI7021_TEMP_CMD])
        
        # Set up a read transaction that reads two bytes of data
        read_result = smbus2.i2c_msg.read(SI7021_ADDR, 2)

        bus.i2c_rdwr(cmd_meas_temp)
        time.sleep(0.1)  # Allow sensor time to measure
        bus.i2c_rdwr(read_result)

        # Combine bytes
        raw_temp = (read_result.buf[0][0] << 8) | read_result.buf[1][0]

        # Convert to Celsius
        temp_celcius = (175.72 * raw_temp / 65536) - 46.85

        return round(temp_celcius, 2)

    except Exception as e:
        print("Error reading temperature sensor:", e)
        return None

def read_moisture():
    try:
        # Convert CONFIG to two bytes in big-endian order
        config_bytes = ADS1115_CONFIG.to_bytes(2, byteorder='big')
    
        # Write the configuration to the CONFIG_REG to start a single-shot conversion
        bus.write_i2c_block_data(ADS1115_ADDR, ADS1115_CONFIG_REG, list(config_bytes))
    
        # Wait for conversion to complete (100ms is sufficient for 128 SPS)
        time.sleep(0.1)
    
        # Read the conversion result (2 bytes from the conversion register)
        data = bus.read_i2c_block_data(ADS1115_ADDR, ADS1115_CONVERSION_REG, 2)
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
        bus.write_byte(CCS811_ADDR, CCS811_APP_START)
        time.sleep(1)  # Allow the sensor to start

        # Set mode to read every second
        bus.write_byte_data(CCS811_ADDR, CCS811_MEAS_MODE_REG, 0x10)
        print("Gas sensor is ready. Waiting 20 seconds for stabilization...")
        time.sleep(20)
        
    except Exception as e:
        print("Error initializing gas sensor:", e)

def read_gas_sensor():
    try:
        status = bus.read_byte_data(CCS811_ADDR, CCS811_STATUS_REG)
        
        if status & 0x08:   # Data ready
            data = bus.read_i2c_block_data(CCS811_ADDR, CCS811_ALG_RESULT_DATA, 8)
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

# MQTT Client Setup
client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

print("Connected to MQTT Broker")

def main():
    initialize_gas_sensor() # Initialize the gas sensor (if needed)
    
    while True:
        
        temp = read_temperature()
        moisture = read_moisture()
        gas = read_gas_sensor()
        
        print("\n Sensor Readings:")
        if temp is not None:
            print("Temperature (raw):", temp)
        if moisture is not None:
            print("Moisture ADC (raw):", moisture)
        if gas:
            print(f"Gas - CO₂: {gas['co2']} ppm, TVOC: {gas['tvoc']} ppb")
            CO2 = gas["co2"]
            TVOC = gas["tvoc"]
        else:
            CO2 = -1.0
            TVOC = -1.0

        data = {
            "temperature": round(temp, 2),
            "moisture": round(moisture, 2),
            "CO2": round(CO2, 2),
            "TVOC": round(TVOC, 2),
            "device_ip": get_ip()
        }  # Format data as JSON
        payload = json.dumps(data)

        client.publish(MQTT_TOPIC, payload)
        print(f"Published: {payload}")

        print("")

        time.sleep(5) # Read every second
    
if __name__ == "__main__":
    main()
