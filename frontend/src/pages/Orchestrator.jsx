import "../styles/orchestrator.css";
import { useState,useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

export default function Orchestrator() {
  const navigate = useNavigate();
  const stars = Array.from({ length: 900 });
  const wsRef = useRef(null);

  const [messages, setMessages] = useState([
    { from: "ai", text: "Hi 👋 How can I help you today?" }
  ]);
  const [input, setInput] = useState("");

    useEffect(() => {
      const token = localStorage.getItem("access_token");

      wsRef.current = new WebSocket(
        `ws://localhost:8000/ws/chat?token=${token}`
      );

      wsRef.current.onmessage = (event) => {
        setMessages((prev) => [
          ...prev,
          { from: "ai", text: event.data },
        ]);
      };

      wsRef.current.onerror = () => {
        console.error("WebSocket error");
      };

      return () => {
        wsRef.current?.close();
      };
    }, []);

    const sendMessage = () => {
      if (!input.trim()) return;

      setMessages((prev) => [...prev, { from: "user", text: input }]);

      wsRef.current.send(input);
      setInput("");
    };

  return (
    <div className="orchestrator-wrapper">

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

      <div className="chat-card floating-chat">

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
