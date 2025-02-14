import time
import smbus2

# ADS1115 I2C address (adjust according to ADC's ADDR connection)
ADS1115_ADDR = 0x48

# Register addresses
CONVERSION_REG = 0x00
CONFIG_REG = 0x01

# Config word for single-shot conversion on channel A0
CONFIG = 0x8583

# I2C bus object
bus = smbus2.SMBus(1)

config_bytes = CONFIG.to_bytes(2, byteorder='big')

while True: 
    # Start single conversion by writing configuration to CONFIG_REG
    bus.write_i2c_block_data(ADS1115_ADDR, CONFIG_REG, list(config_bytes))

    time.sleep(0.1)

    # Read conversion result (2 bytes from conversion reg)
    data = bus.read_i2c_block_data(ADS1115_ADDR, CONVERSION_REG, 2)
    adc_value = int.from_bytes(data, byteorder='big', signed=True)

    print("ADC Reading (raw):", adc_value)

    time.sleep(1)