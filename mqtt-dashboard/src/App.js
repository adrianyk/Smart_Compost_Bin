import React, { useState, useEffect } from "react";
import Dashboard from "./Dashboard";
import TemperatureChart from "./TemperatureChart";
import FAQ from "./FAQ";

function App() {
  const [selectedDevice, setSelectedDevice] = useState("");
  const [devices, setDevices] = useState([]);
  const [deviceNames, setDeviceNames] = useState({});
  const [tempDeviceName, setTempDeviceName] = useState(""); // Holds input text before saving

  useEffect(() => {
    const fetchDevices = async () => {
      try {
        const response = await fetch("http://localhost:5000/devices");
        const data = await response.json();
        if (Array.isArray(data)) {
          setDevices(data);
          setSelectedDevice(data[0] || "");

          // Load saved names from localStorage
          const savedNames = JSON.parse(localStorage.getItem("deviceNames")) || {};
          setDeviceNames(savedNames);
        }
      } catch (error) {
        console.error("Error fetching device list:", error);
      }
    };
    fetchDevices();
  }, []);

  // Update and save device name only when "Save Name" is pressed
  const handleSaveDeviceName = () => {
    if (!selectedDevice) return;
    const updatedNames = { ...deviceNames, [selectedDevice]: tempDeviceName.trim() || selectedDevice };
    setDeviceNames(updatedNames);
    localStorage.setItem("deviceNames", JSON.stringify(updatedNames));
    setTempDeviceName(""); // Clear input after saving
  };

  // Reset device name to default (MAC address)
  const handleResetDeviceName = () => {
    if (!selectedDevice) return;
    const updatedNames = { ...deviceNames };
    delete updatedNames[selectedDevice]; // Remove custom name
    setDeviceNames(updatedNames);
    localStorage.setItem("deviceNames", JSON.stringify(updatedNames));
    setTempDeviceName(""); // Clear input
  };

  // Determine button text based on input
  const buttonText =
    deviceNames[selectedDevice] && tempDeviceName.trim() === "" ? "Reset Name" : "Save Name";

  return (
    <div style={{ height: "100vh", padding: "20px", textAlign: "center", backgroundColor: "#white" }}>
      <h1>Compost Bin Live Dashboard</h1>

      {/* Styled Dropdown */}
      <div style={{ position: "relative", display: "inline-block", marginBottom: "20px" }}>
        <label style={{ fontSize: "1.2rem", fontWeight: "bold", display: "block", marginBottom: "5px" }}>
          Select Device:
        </label>
        <div style={{ position: "relative" }}>
          <select
            value={selectedDevice}
            onChange={(e) => setSelectedDevice(e.target.value)}
            style={{
              padding: "12px 40px 12px 16px",
              fontSize: "1rem",
              borderRadius: "8px",
              border: "2px solid #3b82f6",
              backgroundColor: "white",
              cursor: "pointer",
              appearance: "none",
              width: "250px",
              fontWeight: "bold",
              color: "#3b82f6",
            }}
          >
            {devices.map((device) => (
              <option key={device} value={device} style={{ padding: "10px", fontSize: "1rem" }}>
                {deviceNames[device] ? `${deviceNames[device]}` : device}
              </option>
            ))}
          </select>

          {/* Dropdown Arrow */}
          <div
            style={{
              position: "absolute",
              right: "12px",
              top: "50%",
              transform: "translateY(-50%)",
              pointerEvents: "none",
              color: "#3b82f6",
              fontSize: "1.2rem",
            }}
          >
            ▼
          </div>
        </div>
      </div>

      {/* Rename Device Feature */}
      {selectedDevice && (
        <div style={{ marginBottom: "20px" }}>
          <input
            type="text"
            value={tempDeviceName}
            onChange={(e) => setTempDeviceName(e.target.value)}
            placeholder="Enter custom name"
            style={{
              padding: "10px",
              fontSize: "1rem",
              borderRadius: "8px",
              border: "2px solid #3b82f6",
              marginRight: "10px",
              width: "200px",
            }}
          />
          <button
            onClick={buttonText === "Reset Name" ? handleResetDeviceName : handleSaveDeviceName}
            style={{
              padding: "10px 15px",
              fontSize: "1rem",
              borderRadius: "8px",
              border: "none",
              backgroundColor: "#3b82f6",
              color: "white",
              cursor: "pointer",
              fontWeight: "bold",
            }}
          >
            {buttonText}
          </button>
        </div>
      )}

      <div style={{ display: "flex", height: "75vh" }}>
        <div style={{ width: "30%", minWidth: "300px", padding: "20px", borderRight: "2px solid #ddd" }}>
          <Dashboard device={selectedDevice} />
        </div>
        <div style={{ flex: 1, padding: "20px" }}>
          <TemperatureChart device={selectedDevice} />
        </div>
      </div>

      <FAQ />
    </div>
  );
}

export default App;