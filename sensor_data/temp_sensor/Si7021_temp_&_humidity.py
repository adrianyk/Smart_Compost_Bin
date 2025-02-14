import time
import smbus2

si7021_ADD = 0x40
si7021_READ_TEMPERATURE = 0xF3

bus = smbus2.SMBus(1)

# Set up write transaction that sends command to measure temp
cmd_meas_temp = smbus2.i2c_msg.write(si7021_ADD,[si7021_READ_TEMPERATURE])

# Set up read transaction that reads two bytes of data
read_result = smbus2.i2c_msg.read(si7021_ADD,2)

# Execute both commands
bus.i2c_rdwr(cmd_meas_temp)
time.sleep(0.1)
bus.i2c_rdwr(read_result)

# Convert result to int
temperature = int.from_bytes(read_result.buf[0]+read_result.buf[1],'big')
print(temperature)