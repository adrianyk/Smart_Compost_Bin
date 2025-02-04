import React from "react";
import { FaTemperatureLow, FaTemperatureHigh, FaWind, FaTint, FaRegCheckCircle } from "react-icons/fa";
import { MdWaterDrop } from "react-icons/md";

const Recommendations = ({ temperature, moisture, tvoc }) => {
  const getNotifications = () => {
    let notifications = [];

    if (temperature < 40) {
      notifications.push({
        issue: "Temperature Too Low",
        action: "Turn to aerate, add more nitrogen.",
        icon: <FaTemperatureLow style={{ color: "blue", fontSize: "1.5rem" }} />,
      });
    }
    if (temperature > 70) {
      notifications.push({
        issue: "Temperature Too High",
        action: "Turn to release heat, add more carbon.",
        icon: <FaTemperatureHigh style={{ color: "red", fontSize: "1.5rem" }} />,
      });
    }
    if (tvoc > 500) {
      notifications.push({
        issue: "Strong Odor Detected",
        action: "Turn to improve aeration, add dry carbon materials.",
        icon: <FaWind style={{ color: "gray", fontSize: "1.5rem" }} />,
      });
    }
    if (moisture > 70) {
      notifications.push({
        issue: "Compost Too Wet",
        action: "Mix in dry materials and turn.",
        icon: <MdWaterDrop style={{ color: "blue", fontSize: "1.5rem" }} />,
      });
    }
    if (moisture < 30) {
      notifications.push({
        issue: "Compost Too Dry",
        action: "Add water and turn.",
        icon: <FaTint style={{ color: "brown", fontSize: "1.5rem" }} />,
      });
    }

    return notifications;
  };

  const notifications = getNotifications();

  return (
    <div style={{ marginTop: "20px", padding: "15px", borderRadius: "5px" }}>
      <h3>Alerts & Recommendations</h3>
      {notifications.length > 0 ? (
        notifications.map((notif, index) => (
          <div key={index} style={{ 
            display: "flex", 
            alignItems: "center",
            backgroundColor: "#ffcccc", 
            padding: "10px", 
            borderRadius: "5px", 
            marginBottom: "10px", 
            borderLeft: "5px solid red"
          }}>
            {notif.icon}
            <div style={{ marginLeft: "10px" }}>
              <strong>{notif.issue}</strong>
              <p>{notif.action}</p>
            </div>
          </div>
        ))
      ) : (
        <div style={{ 
          display: "flex", 
          alignItems: "center",
          backgroundColor: "#ccffcc", 
          padding: "10px", 
          borderRadius: "5px", 
          borderLeft: "5px solid green"
        }}>
          <FaRegCheckCircle style={{ color: "green", fontSize: "1.5rem" }} />
          <div style={{ marginLeft: "10px" }}>
            Conditions are optimal! No action needed.
          </div>
        </div>
      )}
    </div>
  );
};

export default Recommendations;
