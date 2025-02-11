import React from "react";
import Dashboard from "./Dashboard";
import TemperatureChart from "./TemperatureChart";
import FAQ from "./FAQ";

function App() {
  return (
    <div style={{ height: "100vh", padding: "20px", textAlign: "center" }}>
      {/* Header */}
      <h1 style={{ marginBottom: "20px" }}>Compost Bin Live Dashboard</h1>

      {/* Main Layout */}
      <div style={{ display: "flex", height: "68vh" }}>
        {/* Left Section: Dashboard */}
        <div style={{
          width: "30%",
          minWidth: "300px",
          padding: "20px",
          borderRight: "2px solid #ddd",
          textAlign: "left",
        }}>
          <Dashboard />
        </div>

        {/* Right Section: Chart */}
        <div style={{ flex: 1, padding: "20px" }}>
          <TemperatureChart />
        </div>
      </div>

      <div>
        <FAQ />
      </div>

    </div>
  );
}

export default App;