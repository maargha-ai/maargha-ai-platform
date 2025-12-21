import "../styles/orchestrator.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Orchestrator() {
  const navigate = useNavigate();
  const stars = Array.from({ length: 900 });

  const [messages, setMessages] = useState([
    { from: "ai", text: "Hi 👋 How can I help you today?" }
  ]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (!input.trim()) return;

    setMessages([...messages, { from: "user", text: input }]);
    setInput("");

    // later → connect orchestrator-service
  };

  return (
    <div className="orchestrator-wrapper">

      {/* STAR BACKGROUND */}
      <div className="stars-layer">
        {stars.map((_, i) => {
          const movement =
            Math.random() < 0.33 ? 4 : Math.random() < 0.66 ? 8 : 14;

          return (
            <span
              key={i}
              className="star"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDuration: `${14 + Math.random() * 18}s`,
                animationDelay: `${Math.random() * -20}s`,
                opacity: Math.random(),
                "--drift": `${movement}px`,
              }}
            />
          );
        })}
      </div>

      {/* CHAT CARD */}
      <div className="chat-card floating-chat">

        {/* HOME BUTTON */}
        <button
          className="home-float-btn"
          onClick={() => navigate("/dashboard")}
          aria-label="Go Dashboard"
        >
          ⌂
        </button>

        <div className="chat-messages">
          {messages.map((m, i) => (
            <div key={i} className={`chat-bubble ${m.from}`}>
              {m.text}
            </div>
          ))}
        </div>

        <div className="chat-input">
          <input
            placeholder="Ask anything..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}
