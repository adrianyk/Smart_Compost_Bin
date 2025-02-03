import time
import smbus2

# ADS1115 I2C address (adjust according to your board's ADDR connection)
ADS1115_ADDR = 0x48

# Register addresses
CONVERSION_REG = 0x00
CONFIG_REG = 0x01

# Build a configuration word (16 bits) for a single-shot conversion on A0.
# This value is built by combining the following settings:
#   - OS (bit 15) = 1 to start a conversion
#   - MUX (bits 14:12): For A0 vs. GND, the code is 100.
#   - PGA (bits 11:9): 010 for ±2.048V (default)
#   - MODE (bit 8): 1 for single-shot mode.
#   - DR (bits 7:5): 100 for 128 SPS (default)
#   - Comparator bits (bits 4:0): default (e.g., disable comparator)
#
# As an example, we might use the value 0x8583 (which is close to the datasheet reset value)
# but with the multiplexer bits set for A0 single-ended.
CONFIG = 0x8583

# Create the I2C bus object (bus number 1 is typical on Raspberry Pi Zero)
bus = smbus2.SMBus(1)

# Convert CONFIG to two bytes in big-endian order.
config_bytes = CONFIG.to_bytes(2, byteorder='big')

while True: 
    # Start a single conversion by writing the configuration to the CONFIG_REG.
    bus.write_i2c_block_data(ADS1115_ADDR, CONFIG_REG, list(config_bytes))

    # Wait for the conversion to complete.
    time.sleep(0.1)  # 100ms is safe for 128 SPS; adjust if you change the data rate.

    # Read the conversion result (2 bytes from the conversion register)
    data = bus.read_i2c_block_data(ADS1115_ADDR, CONVERSION_REG, 2)
    adc_value = int.from_bytes(data, byteorder='big', signed=True)

    print("ADC Reading (raw):", adc_value)
    
    # Delay before the next reading (adjust as needed, e.g., 1 minute = 60 seconds)
    # For testing, you might start with a 1-second delay:
    time.sleep(1)