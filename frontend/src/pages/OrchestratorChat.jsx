import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

/**
 * OrchestratorChat
 * ----------------
 * - Opens WebSocket to gateway (/ws/chat?token=...)
 * - Handles general chat + navigation instructions
 */
export default function OrchestratorChat({ onClose }) {
  const navigate = useNavigate();
  const wsRef = useRef(null);

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [connected, setConnected] = useState(false);

  /* -------------------------------
     WebSocket connection
  -------------------------------- */
  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      console.error("No access token found");
      return;
    }

    const ws = new WebSocket(
      `ws://localhost:8000/ws/chat?token=${token}`
    );

    wsRef.current = ws;

    ws.onopen = () => {
      console.log("[WS] Orchestrator connected");
      setConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        // 🔁 Navigation instruction
        if (data.navigate) {
          handleNavigation(data.navigate);
          return;
        }

        // 💬 Normal chat message
        if (data.type === "CHAT") {
          setMessages((prev) => [
            ...prev,
            { role: "assistant", content: data.content }
          ]);
        }
      } catch {
        // Fallback: plain string
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: event.data }
        ]);
      }
    };

    ws.onclose = () => {
      console.log("[WS] Orchestrator disconnected");
      setConnected(false);
    };

    ws.onerror = (err) => {
      console.error("[WS] Error", err);
    };

    return () => {
      ws.close();
    };
  }, []);

  /* -------------------------------
     Send message
  -------------------------------- */
  const sendMessage = () => {
    if (!input.trim() || !wsRef.current) return;

    wsRef.current.send(input);

    setMessages((prev) => [
      ...prev,
      { role: "user", content: input }
    ]);

    setInput("");
  };

  /* -------------------------------
     Handle ENTER key
  -------------------------------- */
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  /* -------------------------------
     Navigation handler
  -------------------------------- */
  const handleNavigation = ({ tool, payload }) => {
    console.log("[NAVIGATE]", tool, payload);

    if (onClose) onClose();

    switch (tool) {
      case "CareerPredictor":
        navigate("/career");
        break;

      case "RoadmapGenerator":
        navigate("/roadmap", { state: payload });
        break;

      case "JobSearch":
        navigate("/jobs");
        break;

      case "LinkedInAssistant":
        navigate("/linkedin");
        break;

      case "QuizGenerator":
        navigate("/quiz");
        break;

      case "TechNews":
        navigate("/news");
        break;

      case "EmotionalSupport":
        navigate("/emotional-support");
        break;

      default:
        console.warn("Unknown tool:", tool);
    }
  };

  /* -------------------------------
     UI
  -------------------------------- */
  return (
    <div className="orchestrator-chat">
      <div className="header">
        <span>🧠 MAARGHA Orchestrator</span>
        <button onClick={onClose}>✕</button>
      </div>

      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            {m.content}
          </div>
        ))}

        {!connected && (
          <div className="msg system">Connecting...</div>
        )}
      </div>

      <div className="input-bar">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Talk to the orchestrator..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}
