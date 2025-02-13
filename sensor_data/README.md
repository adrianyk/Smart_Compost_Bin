# Sensor Data

## Overview
This folder contains the **initial sensor data collection scripts** for the **Smart Compost Bin** project. Each subfolder represents a specific sensor type and contains **Raspberry Pi scripts** for reading and processing data from that sensor.

---

## Sensors Used

| Sensor Type          | Model Used  | Raspberry Pi Interface | Description |
|----------------------|------------|------------------------|-------------|
| **Gas Sensor**      | CCS811      | I2C                    | Measures **CO₂ (ppm)** & **TVOCs (ppb)** |
| **Temperature Sensor** | Si7021  | I2C                    | Measures **temperature (°C)** |
| **Moisture Sensor** | ADS1115 | Analog (via ADC) | Measures **soil moisture level (%)** |

---

## How to Run the Sensor Scripts

Each sensor script is run **independently** on a Raspberry Pi.

📍 **Gas Sensor (CCS811)**
cd gas_sensor
python3 read_gas_sensor.py

📍 **Temperature Sensor (Si7021)**
cd temp_sensor
python3 read_temp_sensor.py

📍 **Moisture Sensor (ADS1115)**
cd moisture_sensor
python3 read_moisture_sensor.py
