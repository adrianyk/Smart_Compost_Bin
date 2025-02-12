import React from "react";
import { FaTemperatureLow, FaTemperatureHigh, FaWind, FaTint, FaRegCheckCircle, FaExclamationTriangle } from "react-icons/fa";
import { MdWaterDrop } from "react-icons/md";

const Recommendations = ({ chi, aeration }) => {
  const getNotifications = () => {
    let notifications = [];

    const highThreshold = 0.7;
    const mediumThreshold = 0.4;

    // Case 1: Ideal conditions: both CHI and Aeration are high
    if (chi >= highThreshold && aeration >= highThreshold) {
      notifications.push({
        issue: "Optimal Conditions",
        action: "No action needed! Compost conditions are ideal. Decomposition is rapid.",
        icon: (
          <div>
            <FaRegCheckCircle style={{ color: "green", fontSize: "1.5rem" }} />
          </div>
        ),
      });
    }
    
    // Case 2: High CHI but aeration is only medium
    if (chi >= highThreshold && aeration >= mediumThreshold && aeration < highThreshold) {
      notifications.push({
        issue: "Suboptimal Aeration",
        action: "Aeration is slightly reduced. Turn compost to improve oxygen flow and prevent anaerobic pockets. Decomposition is moderate.",
        icon: <FaExclamationTriangle style={{ color: "orange", fontSize: "1.5rem" }} />,
      });
    }

    // Case 3: High CHI but aeration is low
    if (chi >= highThreshold && aeration < mediumThreshold) {
      notifications.push({
        issue: "Poor Aeration",
        action: "Oxygen levels are low. Turn the compost pile immediately to introduce oxygen. Add dry browns to improve structure. Decomposition is slowing due to lack of oxygen.",
        icon: <FaExclamationTriangle style={{ color: "red", fontSize: "1.5rem" }} />,
      });
    }

    // Case 4: Medium CHI and high aeration
    if (chi < highThreshold && chi >= mediumThreshold && aeration >= highThreshold) {
      notifications.push({
        issue: "Moderate Compost Health",
        action: "Decent composting. Check moisture and temperature. If too dry, add water or nitrogen-rich greens; if cooling, turn to aerate. Decomposition is moderate.",
        icon: <FaExclamationTriangle style={{ color: "orange", fontSize: "1.5rem" }} />,
      });
    }

    // Case 5: Medium CHI and medium aeration
    if (chi < highThreshold && chi >= mediumThreshold && aeration < highThreshold && aeration >= mediumThreshold) {
      notifications.push({
        issue: "Suboptimal Conditions",
        action: "Turn compost to aerate and adjust moisture. Add high-nitrogen materials if it's too cold or browns if it's too wet. Decomposition is slowing down.",
        icon: <FaExclamationTriangle style={{ color: "orange", fontSize: "1.5rem" }} />,
      });
    }

    // Case 6: Medium CHI but low aeration
    if (chi < highThreshold && chi >= mediumThreshold && aeration < mediumThreshold) {
      notifications.push({
        issue: "Anaerobic Risk",
        action: "Poor aeration detected. Turn the compost and add dry browns to improve oxygen flow and absorb excess moisture. Decomposition is very slow.",
        icon: <FaExclamationTriangle style={{ color: "red", fontSize: "1.5rem" }} />,
      });
    }

    // Case 7: Low CHI but high aeration.
    if (chi < mediumThreshold && aeration >= highThreshold) {
      notifications.push({
        issue: "Dry & Inactive Compost",
        action: "Compost appears inactive, possibly due to dryness. Add more nitrogen-rich greens or water if moisture is low to restore microbial activity. Decomposition is minimal.",
        icon: <FaExclamationTriangle style={{ color: "red", fontSize: "1.5rem" }} />
      });
    }

    // Case 8: Low CHI and medium aeration.
    if (chi < mediumThreshold && aeration >= mediumThreshold && aeration < highThreshold) {
      notifications.push({
        issue: "Inactive Compost",
        action: "Compost conditions are poor, possibly too cold or dry. Turn the compost, insulate the bin if needed, and add greens. Decomposition is nearly stalled.",
        icon: <FaExclamationTriangle style={{ color: "red", fontSize: "1.5rem" }} />
      });
    }

    // Case 9: Low CHI and low aeration.
    else if (chi < mediumThreshold && aeration < mediumThreshold) {
      notifications.push({
        issue: "Critical Condition",
        action: "Severe anaerobic and inactive conditions detected. Turn compost to introduce oxygen, balance greens and browns. Decomposition stopped, risk of bad odors.",
        icon: <FaExclamationTriangle style={{ color: "red", fontSize: "1.5rem" }} />
      });
    }

    return notifications;
  };

  const notifications = getNotifications();

  return (
    <div style={{ marginTop: "20px", borderRadius: "5px" }}>
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