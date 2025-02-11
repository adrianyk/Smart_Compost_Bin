import React, { useState, useEffect } from "react";
import Recommendations from "./Recommendations";
import { FaTemperatureHigh, FaSmog, FaCloud } from "react-icons/fa";
import { MdWaterDrop } from "react-icons/md";

const Dashboard = ({ device }) => {
  const [data, setData] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState("Fetching data...");

  useEffect(() => {
    if (!device) return;

    const fetchLatestData = async () => {
      try {
        const response = await fetch(`http://localhost:5000/latest/${device}`);
        const jsonData = await response.json();
        if (jsonData.error) {
          setConnectionStatus("No data available");
          setData(null);
        } else {
          setData(jsonData);
          setConnectionStatus("Connected");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        setConnectionStatus("Error fetching data");
      }
    };

    fetchLatestData();
    const interval = setInterval(fetchLatestData, 5000);
    return () => clearInterval(interval);
  }, [device]);

  return (
    <div style={{ padding: "15px", fontFamily: "Arial, sans-serif", textAlign: "left" }}>
      <h2>Live Readings</h2>
      <h3>Status: <span style={{ color: connectionStatus === "Connected" ? "green" : "red" }}>{connectionStatus}</span></h3>

      {data ? (
        <div>
          <h2 style={{ color: "orange" }}>
            <FaTemperatureHigh /> Temperature: {data.temperature}°C
          </h2>
          <h2 style={{ color: "blue" }}>
            <MdWaterDrop /> Moisture: {data.moisture}%
          </h2>
          <h2 style={{ color: "green" }}>
            <FaSmog /> CO<sub>2</sub>: {data.CO2} ppm
          </h2>
          <h2 style={{ color: "purple" }}>
            <FaCloud /> TVOC: {data.TVOC} ppm
          </h2>
          <Recommendations temperature={data.temperature} moisture={data.moisture} tvoc={data.TVOC} />
        </div>
      ) : (
        <h2>Waiting for data...</h2>
      )}
    </div>
  );
};

export default Dashboard;
