# ♻️ Smart Compost Bin

As part of the **Embedded Systems module**, we designed and implemented a functional Smart Compost Bin that monitors and optimizes composting conditions using real-time sensor data and intelligent recommendations. 

---
## System Architecture
The **Smart Compost Bin System** consists of:  
- **Two Raspberry Pis** that collects sensor data (**temperature, moisture, CO₂, and TVOCs**)
- **MQTT protocol** for wireless data transmission
- **Flask backend** to process and store sensor readings
- **React frontend** to visualize data and provide real-time composting recommendations  

**Data Flow:**  
Sensor Data →  MQTT Broker → Flask Backend → React UI

---

## 📝 Contributors

| Name            | Air Quality Sensor | Temperature Sensor | Moisture Sensor | Flask Backend & API | MQTT Integration | React Frontend | Documentation |
|----------------|------------------|-------------------|------------------|----------------|----------------|---------------|---------------|
| **[Adrian]**   |                  |                   | ✅                    |               | ✅              | ✅            | ✅
| **[Keegan]**   |                  | ✅                |                     | ✅              |                | ✅            | ✅
| **[Jungwon]**  | ✅               |                   | ✅                   |               |                | ✅            | ✅

---
## Marketing Website

https://jungwon0518.wixsite.com/smart-compost-bin

## Launching Frontend Dashboard

Part of the project includes a dashboard which displays both live and historic data from the composting bins. Due to versions conflicts with React, please follow the steps below to launch:

1. Using `Command Prompt`, `cd` into the directory `mqtt-dashboard` by running `cd mqtt-dashboard`
2. Ensure that `node_modules` and `package-lock.js` are not present in this directory
3. Run `npm install webpack@4.44.2 webpack-dev-server@3.11.1 --legacy-peer-deps`
4. Run `set NODE_OPTIONS=--openssl-legacy-provider
5. Run `npm start` which should launch the dashboard in your browser

These installation instructions are meant to ensure that there are no conflicts due to the use of specific packages which are only compatible with older versions of React and its associated libraries

