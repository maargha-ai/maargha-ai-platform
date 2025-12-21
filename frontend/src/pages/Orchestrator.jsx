import "../styles/orchestrator.css";
import { useState } from "react";

export default function Orchestrator() {
  const [messages, setMessages] = useState([
    { from: "ai", text: "Hi 👋 How can I help you today?" }
  ]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (!input.trim()) return;

    setMessages([...messages, { from: "user", text: input }]);
    setInput("");

    // later → send to orchestrator-service
  };

  return (
    <div className="orchestrator-wrapper">
      <div className="chat-card">
        <div className="chat-messages">
          {messages.map((m, i) => (
            <div
              key={i}
              className={`chat-bubble ${m.from}`}
            >
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
