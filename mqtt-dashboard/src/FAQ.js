import React, { useState } from "react";

const FAQ = () => {
  const faqs = [
    {
      question: "🔥 My compost bin temperature is too high! What should I do?",
      answer: "Add more dry browns (leaves, cardboard) to balance nitrogen levels and turn the compost to release excess heat.",
    },
    {
      question: "❄️ My compost is too cold. How do I warm it up?",
      answer: "Add more greens (food scraps, grass clippings) and turn the compost to activate microbial activity.",
    },
    {
      question: "💦 My compost is too wet! What can I do?",
      answer: "Mix in dry browns like shredded paper or sawdust to absorb excess moisture.",
    },
    {
      question: "🌱 My compost is too dry! How do I fix it?",
      answer: "Add a small amount of water and mix in wet greens to increase moisture levels.",
    },
    {
      question: "💨 My CO₂ levels are too high! What does this mean?",
      answer: "This indicates anaerobic conditions. Turn the compost to improve airflow and balance the moisture levels.",
    },
    {
      question: "🤢 My compost smells bad! What should I do?",
      answer: "Bad odors mean too much moisture or lack of aeration. Turn the compost and add dry browns to neutralize odors.",
    },
  ];

  const [openIndex, setOpenIndex] = useState(null);

  const toggleFAQ = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div style={{ marginTop: "30px", padding: "20px", backgroundColor: "#f9f9f9", borderRadius: "8px" }}>
      <h2>❓ Frequently Asked Questions</h2>
      {faqs.map((faq, index) => (
        <div key={index} style={{ marginBottom: "10px" }}>
          <button
            onClick={() => toggleFAQ(index)}
            style={{
              width: "100%",
              textAlign: "left",
              padding: "10px",
              fontSize: "1.1rem",
              fontWeight: "bold",
              backgroundColor: openIndex === index ? "#ddd" : "#eee",
              border: "none",
              cursor: "pointer",
            }}
          >
            {faq.question}
          </button>
          {openIndex === index && (
            <div style={{ padding: "10px", backgroundColor: "#fff", borderRadius: "4px", border: "1px solid #ddd" }}>
              {faq.answer}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default FAQ;
