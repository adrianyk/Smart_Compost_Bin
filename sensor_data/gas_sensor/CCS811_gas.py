import time
import smbus2

# CCS811 I2C Address
CCS811_ADDR = 0x5A
STATUS_REG = 0x00
MEAS_MODE_REG = 0x01
ALG_RESULT_DATA = 0x02
APP_START = 0xF4
HW_ID = 0x20

# Initialize I2C
bus = smbus2.SMBus(1)

def initialize_sensor():
    print("Resetting CCS811 sensor...")
    bus.write_byte(CCS811_ADDR, APP_START)
    time.sleep(1)

    # Set mode to read every second
    bus.write_byte_data(CCS811_ADDR, MEAS_MODE_REG, 0x10)
    print("Sensor is ready. Waiting 20s for stabilization...")
    time.sleep(20)

def read_gas_sensor():
    # Reads CO₂ and TVOC values from CCS811, filter out invalid readings
    try:
        status = bus.read_byte_data(CCS811_ADDR, STATUS_REG)
        if status & 0x08:  # Data ready
            data = bus.read_i2c_block_data(CCS811_ADDR, ALG_RESULT_DATA, 8)
            co2 = (data[0] << 8) | (data[1] & 0xFF)
            tvoc = (data[2] << 8) | (data[3] & 0xFF)

            # Ignore unrealistic readings
            if co2 > 5000 or tvoc > 2000:
                print("Unstable reading detected, skipping...")
                return None
            return {"co2": co2, "tvoc": tvoc}

    except Exception as e:
        print(f"⚠️ Sensor error: {e}")

    return None

if __name__ == "__main__":
    initialize_sensor()
    
    while True:
        sensor_data = read_gas_sensor()
        if sensor_data:
            print(f"CO₂: {sensor_data['co2']} ppm, TVOCs: {sensor_data['tvoc']} ppb")
        
        time.sleep(2)
