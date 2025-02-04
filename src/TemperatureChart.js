import React, { useState, useEffect } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

import { Line } from "react-chartjs-2";

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const PARAMETERS = ["Temperature", "Moisture", "CO2", "TVOC"];

const TemperatureChart = () => {
  const [timestamps, setTimestamps] = useState([]);
  const [dataPoints, setDataPoints] = useState({});
  const [activeParameter, setActiveParameter] = useState("Temperature");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5000/data");
        const jsonData = await response.json();

        if (jsonData.length > 1) {
          const parsedData = jsonData.slice(1); // Remove header row

          const loadedTimestamps = parsedData.map(row => row[0]);
          const loadedData = {
            Temperature: parsedData.map(row => parseFloat(row[1])),
            Moisture: parsedData.map(row => parseFloat(row[2])),
            CO2: parsedData.map(row => parseFloat(row[3])),
            TVOC: parsedData.map(row => parseFloat(row[4])),
          };

          setTimestamps(loadedTimestamps);
          setDataPoints(loadedData);
        }
      } catch (error) {
        console.error("Error fetching CSV data:", error);
      }
    };

    // Fetch data every 5 seconds
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const chartData = {
    labels: timestamps,
    datasets: [
      {
        label: `${activeParameter} Over Time`,
        data: dataPoints[activeParameter] || [],
        borderColor:
          activeParameter === "Temperature"
            ? "orange"
            : activeParameter === "Moisture"
            ? "blue"
            : activeParameter === "CO2"
            ? "green"
            : "purple",
        fill: false,
      },
    ],
  };

  return (
    <div style={{ width: "80%", margin: "auto", textAlign: "center" }}>
      <h2>Historical Data Over Last Hour</h2>
      
      {/* Tab Navigation */}
      <div style={{ marginBottom: "20px" }}>
        {PARAMETERS.map((param) => (
          <button
            key={param}
            onClick={() => setActiveParameter(param)}
            style={{
              margin: "5px",
              padding: "10px",
              cursor: "pointer",
              borderRadius: "5px",
              border: activeParameter === param ? "2px solid black" : "1px solid gray",
              backgroundColor: activeParameter === param ? "#ddd" : "#fff",
            }}
          >
            {param}
          </button>
        ))}
      </div>

      {/* Chart Display */}
      <Line data={chartData} />
    </div>
  );
};

export default TemperatureChart;
