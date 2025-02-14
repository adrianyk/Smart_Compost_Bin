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

| Name          | Air Quality Sensor | Temperature Sensor | Moisture Sensor | Flask Backend & API | MQTT Integration | React Frontend | Documentation |
| ------------- | ------------------ | ------------------ | --------------- | ------------------- | ---------------- | -------------- | ------------- |
| **[Adrian]**  |                    |                    | ✅               |                     | ✅                | ✅              | ✅             |
| **[Keegan]**  |                    | ✅                  |                 | ✅                   |                  | ✅              | ✅             |
| **[Jungwon]** | ✅                  |                    | ✅               |                     |                  | ✅              | ✅             |

---
## Marketing Website

https://jungwon0518.wixsite.com/smart-compost-bin


## Accomplishments
### Core functional specifications
1. Functional prototype of an Internet-of-Things product ✅
2. The prototype includes a standalone hardware module that incorporates 3 I2C sensors: temperature, moisture, gas ✅
3. The prototype sends data to a remote client using MQTT, and displayed on a user interface ✅
4. The prototype process and formats sensor data for presentation to a uses ✅
5. Data is sampled at once every 5 seconds (configurable) ✅
### Non-functional specifications
 1. The concept has potential for development into a commercial product ✅
 2. Data presentation to the user is relevant and easy to understand ✅
 3. Code is appropriately structured. The point of entry for code on the Raspberry Pi is `main.py` ✅
 4. The system is scalable to support multiple users and sensor nodes, with multiple sensor nodes per user ✅
 5. The interface to the sensor is implemented using byte-level communication over the I2C bus ✅
### Documentation specifications
 1. There is a marketing website, which uses text, data and graphics to illustrate the beneficial features of the product to a prospective customer ✅
 2. There is a marketing video ✅
 3. The marketing website and video is viewable online with a web browser ✅
### Advanced functionality
1. Data from multiple sensors is fused to provide high-level metrics ✅
2. A webpage is implemented for user interaction ✅
3. Functionality is implemented on a backend server ✅
4. The system is designed to remain functional when data connectivity is lost ✅
5. Machine learning may be used to process sensor data (being developed)

## Launching Frontend Dashboard

Part of the project includes a dashboard which displays both live and historic data from the composting bins. Due to versions conflicts with React, please follow the steps below to launch:

1. Using `Command Prompt`, `cd` into the directory `mqtt-dashboard` by running `cd mqtt-dashboard`
2. Ensure that `node_modules` and `package-lock.js` are not present in this directory
3. Run `npm install webpack@4.44.2 webpack-dev-server@3.11.1 --legacy-peer-deps`
4. Run `set NODE_OPTIONS=--openssl-legacy-provider`
5. Run `npm start` which should launch the dashboard in your browser

These installation instructions are meant to ensure that there are no conflicts due to the use of specific packages which are only compatible with older versions of React and its associated libraries

