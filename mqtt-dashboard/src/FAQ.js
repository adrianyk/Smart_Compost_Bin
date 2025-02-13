import React, { useState, useRef, useEffect } from "react";
import { FaChevronDown, FaChevronUp } from "react-icons/fa";

const FAQ = () => {
  const faqs = [
    {
      question: "My compost is too hot! How do I cool it down?",
      answer: "Add more dry browns (leaves, cardboard) to balance nitrogen levels and turn the compost to release excess heat.",
    },
    {
      question: "My compost is too cold! How do I warm it up?",
      answer: "Add more greens (food scraps, grass clippings) and turn the compost to activate microbial activity.",
    },
    {
      question: "My compost is too wet! What can I do?",
      answer: "Mix in dry browns like shredded paper or sawdust to absorb excess moisture.",
    },
    {
      question: "My compost is too dry! How do I fix it?",
      answer: "Add a small amount of water and mix in wet greens to increase moisture levels.",
    },
    {
      question: "My CO₂ levels are too high! What does this mean?",
      answer: "This indicates anaerobic conditions. Turn the compost to improve airflow and balance the moisture levels.",
    },
    {
      question: "My CO₂ levels are too low! What should I do?",
      answer: "Add more moisture, ensure there's enough organic matter, and turn the compost.",
    },
    {
      question: "My compost smells bad! What should I do?",
      answer: "Bad odors mean too much moisture or lack of aeration. Turn the compost and add dry browns to neutralize odors.",
    },
    {
      question: "What does CHI score mean?",
      answer: "Compost Health Index (CHI) combines key composting parameters into a single score (0-1) to indicate overall composting efficiency."
    },
    {
      question: "What does Aeration score mean?",
      answer: "Aeration meaasures the oxygen availability in the compost."
    },
    {
      question: "What are Dry Browns?",
      answer: "Dry Browns refers to carbon-rich materials that provide energy for microbes and help balance moisture. (i.e. dry leaves, shredded paper/cardboard, sawdust, straw/hay and wood chips)"
    },
    {
      question: "What are Greens?",
      answer: "Greens are fresh, moist, nitrogen-rich materials that help microbes grow and reproduce. (i.e. Fruit & vegetable scraps, grass clippings, coffee grounds, tea leaves, fresh leaves)"
    },
    {
      question: "What materials are bad for compost?",
      answer: "Avoid Meat, dairy, oily foods, pet waste and plastics"
    },
  ];

  const [openIndexes, setOpenIndexes] = useState([]);

  const toggleFAQ = (index) => {
    setOpenIndexes((prevIndexes) =>
      prevIndexes.includes(index)
        ? prevIndexes.filter((i) => i !== index)
        : [...prevIndexes, index]
    );
  };

  return (
    <div style={{ marginTop: "30px", padding: "20px", margin: "auto" }}>
      <h2 style={{ fontSize: "1.8rem", fontWeight: "bold", marginBottom: "20px" }}>Frequently Asked Questions</h2>
      {faqs.map((faq, index) => (
        <div key={index} style={{ marginBottom: "0px", borderBottom: "2px solid #add8e6" }}>
          <button
            onClick={() => toggleFAQ(index)}
            style={{
              width: "100%",
              textAlign: "left",
              padding: "15px",
              fontSize: "1.1rem",
              fontWeight: "bold",
              backgroundColor: "transparent",
              border: "none",
              cursor: "pointer",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            {faq.question}
            {openIndexes.includes(index) ? <FaChevronUp /> : <FaChevronDown />}
          </button>
          <ExpandableAnswer isOpen={openIndexes.includes(index)}>{faq.answer}</ExpandableAnswer>
        </div>
      ))}
    </div>
  );
};

const ExpandableAnswer = ({ isOpen, children }) => {
  const contentRef = useRef(null);
  const [height, setHeight] = useState("0px");
  const [opacity, setOpacity] = useState(0);

  useEffect(() => {
    if (isOpen) {
      setHeight(`${contentRef.current.scrollHeight}px`);
      setOpacity(1);
    } else {
      setHeight("0px");
      setOpacity(0);
    }
  }, [isOpen]);

  return (
    <div
      ref={contentRef}
      style={{
        height,
        opacity,
        overflow: "hidden",
        transition: "height 0.6s ease-in-out, opacity 0.4s ease-in-out",
        textAlign: "left",
        padding: isOpen ? "5px 10px" : "0px 10px",
        fontSize: "1rem",
        color: "#333",
        marginBottom: isOpen ? "3px" : "0px",
      }}
    >
      {children}
    </div>
  );
};


export default FAQ;