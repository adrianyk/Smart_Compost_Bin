# Raspberry Pi Code  

## Overview
This folder contains the **integrated Raspberry Pi script (`main.py`)** used for collecting and transmitting **real-time sensor data** from multiple sensors in the **Smart Compost Bin** project. 

The script is responsible for:
- Reading sensor data (**CO₂, TVOCs, temperature, moisture**)  
- Sending data via **MQTT** to the Flask backend  
- Ensuring **continuous operation** with error handling  
