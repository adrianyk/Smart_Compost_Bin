import React, { useState, useEffect } from "react";
import mqtt from "mqtt";
import Recommendations from "./Recommendations";
import { FaTemperatureHigh, FaSmog, FaCloud } from "react-icons/fa";
import { MdWaterDrop } from "react-icons/md";

const MQTT_BROKER = "wss://test.mosquitto.org:8081";  // WebSocket version of the MQTT broker
const MQTT_TOPIC = "IC.embedded/samsungsmartfridge/compost";

const Dashboard = () => {
  const [temperature, setTemperature] = useState(null);
  const [moisture, setMoisture] = useState(null);
  const [co2, setCO2] = useState(null);
  const [tvoc, setTVOC] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState("Connecting...");

  useEffect(() => {
    console.log("Connecting to MQTT broker...");

    // Connect to the MQTT broker
    const client = mqtt.connect(MQTT_BROKER);

    client.on("connect", () => {
      console.log("Connected to MQTT Broker!");
      setConnectionStatus("Connected");
      client.subscribe(MQTT_TOPIC, (err) => {
        if (!err) {
          console.log(`Subscribed to ${MQTT_TOPIC}`);
        }
      });
    });

    client.on("message", (topic, message) => {
      console.log(`Received message from ${topic}:`, message.toString());

      if (topic === MQTT_TOPIC) {
        try {
          const data = JSON.parse(message.toString());
          setTemperature(data.temperature);
          setMoisture(data.moisture);
          setCO2(data.CO2);
          setTVOC(data.TVOC);
        } catch (error) {
          console.error("Error parsing MQTT message:", error);
        }
      }
    });

    client.on("error", (error) => {
      console.error("MQTT Connection Error:", error);
      setConnectionStatus("Error");
    });

    client.on("offline", () => {
      console.warn("MQTT Client went offline");
      setConnectionStatus("Error");
    });

    client.on("close", () => {
      console.warn("MQTT Client connection closed");
      setConnectionStatus("Error");
    });

    return () => {
      console.log("Disconnecting MQTT client...");
      client.end();
    };
  }, []);

  // Define colors for connection status
  const getStatusColor = () => {
    if (connectionStatus === "Connected") return "green";
    if (connectionStatus === "Error") return "red";
    return "gray";
  };

  return (
    <div style={{ textAlign: "left", padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h2>Live Readings</h2>
      
      {/* Status with only the value colored */}
      <h3>
        Status: <span style={{ color: getStatusColor() }}>{connectionStatus}</span>
      </h3>

      {temperature !== null ? (
        <div>
          <h2 style={{ color: "#ff6600", fontSize: "1.8rem", display: "flex", alignItems: "center" }}>
            <FaTemperatureHigh style={{ marginRight: "10px" }} /> Temperature: {temperature}°C
          </h2>
          <h2 style={{ color: "#008080", fontSize: "1.8rem", display: "flex", alignItems: "center" }}>
            <MdWaterDrop style={{ marginRight: "10px" }} /> Moisture: {moisture}%
          </h2>
          <h2 style={{ color: "#800080", fontSize: "1.8rem", display: "flex", alignItems: "center" }}>
            <FaSmog style={{ marginRight: "10px" }} /> CO₂: {co2} ppm
          </h2>
          <h2 style={{ color: "#ff0000", fontSize: "1.8rem", display: "flex", alignItems: "center" }}>
            <FaCloud style={{ marginRight: "10px" }} /> TVOC: {tvoc} ppm
          </h2>

          {/* Display Recommendations based on data */}
          <Recommendations temperature={temperature} moisture={moisture} tvoc={tvoc} />
        </div>
      ) : (
        <h2>Waiting for data...</h2>
      )}
    </div>
  );
};

export default Dashboard;
