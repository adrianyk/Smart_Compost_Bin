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
