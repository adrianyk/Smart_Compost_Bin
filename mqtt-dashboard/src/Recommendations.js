import React from "react";
import { FaTemperatureLow, FaTemperatureHigh, FaSmog, FaWind, FaTint, FaRegCheckCircle, FaExclamationTriangle } from "react-icons/fa";
import { MdWaterDrop } from "react-icons/md";

const Recommendations = ({ temperature, moisture, co2, tvoc, chi, aeration }) => {
  const getNotifications = () => {
    let chiAerationWarnings = [];
    let generalWarnings = [];

    const highThreshold = 0.7;
    const mediumThreshold = 0.4;

    // General Warnings
    if (temperature < 40) {
      generalWarnings.push({
        issue: "Temperature Too Low",
        icon: <FaTemperatureLow style={{ color: "blue", fontSize: "1.5rem" }} />,
      });
    }

    if (temperature > 70) {
      generalWarnings.push({
        issue: "Temperature Too High",
        icon: <FaTemperatureHigh style={{ color: "red", fontSize: "1.5rem" }} />,
      });
    }

    if (moisture < 30) {
      generalWarnings.push({
        issue: "Compost Too Dry",
        icon: <FaTint style={{ color: "brown", fontSize: "1.5rem" }} />,
      });
    }

    if (moisture > 70) {
      generalWarnings.push({
        issue: "Compost Too Wet",
        icon: <MdWaterDrop style={{ color: "blue", fontSize: "1.5rem" }} />,
      });
    }

    if (co2 < 400) {
      generalWarnings.push({
        issue: "CO₂ Levels Too Low",
        icon: <FaSmog style={{ color: "gray", fontSize: "1.5rem" }} />,
      });
    }

    if (co2 > 5000) {
      generalWarnings.push({
        issue: "CO₂ Levels Too High",
        icon: <FaSmog style={{ color: "gray", fontSize: "1.5rem" }} />,
      });
    }

    if (tvoc > 500) {
      generalWarnings.push({
        issue: "Strong Odor Detected",
        icon: <FaWind style={{ color: "gray", fontSize: "1.5rem" }} />,
      });
    }

    // CHI & Aeration Warnings
    if (chi < mediumThreshold || aeration < mediumThreshold) {
      chiAerationWarnings.push({
        issue: "Critical Condition",
        action: "Severe anaerobic and inactive conditions detected. Turn compost to introduce oxygen, balance greens and browns.",
        icon: <FaExclamationTriangle style={{ color: "red", fontSize: "1.5rem" }} />,
      });
    } else if (chi < highThreshold || aeration < highThreshold) {
      chiAerationWarnings.push({
        issue: "Suboptimal Conditions",
        action: "Turn compost to aerate and adjust moisture. Add high-nitrogen materials if too cold or browns if too wet.",
        icon: <FaExclamationTriangle style={{ color: "orange", fontSize: "1.5rem" }} />,
      });
    } else {
      chiAerationWarnings.push({
        issue: "Optimal Conditions",
        action: "No action needed! Compost conditions are ideal. Decomposition is rapid.",
        icon: <FaRegCheckCircle style={{ color: "green", fontSize: "1.5rem" }} />,
      });
    }

    return { chiAerationWarnings, generalWarnings };
  };

  const { chiAerationWarnings, generalWarnings } = getNotifications();

  return (
    <div style={{ marginTop: "20px", borderRadius: "5px" }}>
      <h3>Compost Status</h3>
      {chiAerationWarnings.map((notif, index) => (
        <div key={index} style={{
          display: "flex",
          alignItems: "center",
          backgroundColor: notif.issue.includes("Optimal") ? "#ccffcc" : "#ffcccc",
          padding: "10px",
          borderRadius: "5px",
          marginBottom: "10px",
          borderLeft: `5px solid ${notif.issue.includes("Optimal") ? "green" : "red"}`
        }}>
          {notif.icon}
          <div style={{ marginLeft: "10px" }}>
            <strong>{notif.issue}</strong>
            <p>{notif.action}</p>
          </div>
        </div>
      ))}

      {/* Separator Section */}
      {generalWarnings.length > 0 && (
        <>
          <h3 style={{ marginTop: "20px" }}>Warnings</h3>
          {generalWarnings.map((notif, index) => (
            <div key={index} style={{
              display: "flex",
              alignItems: "center",
              backgroundColor: "#ffe5cc",
              padding: "10px",
              borderRadius: "5px",
              marginBottom: "10px",
              borderLeft: "5px solid orange"
            }}>
              {notif.icon}
              <div style={{ marginLeft: "10px" }}>
                <strong>{notif.issue}</strong>
              </div>
            </div>
          ))}
        </>
      )}
    </div>
  );
};

export default Recommendations;
