import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  startMicStream,
  stopMicStream,
  muteMic,
  unmuteMic
} from "../pages/emotional-support/useAudioStream";

/* ---------------------------
   INLINE TTS
--------------------------- */
function speakText(text, onEnd) {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";
  utterance.rate = 1;
  utterance.pitch = 1;

  utterance.onend = onEnd;
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utterance);
}

export default function OrchestratorChat({ onClose }) {
  const navigate = useNavigate();

  const chatWsRef = useRef(null);   // TEXT WS
  const liveWsRef = useRef(null);   // AUDIO WS

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [connected, setConnected] = useState(false);
  const [liveMode, setLiveMode] = useState(false);
  const [status, setStatus] = useState(""); // "Listening...", "Thinking...", etc.

  /* TEXT CHAT WS */
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const ws = new WebSocket(`ws://localhost:8000/ws/chat?token=${token}`);
    chatWsRef.current = ws;

    ws.onopen = () => {
      console.log("[CHAT WS] Connected");
      setConnected(true);
    };

    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.navigate) {
        handleNavigation(data.navigate);
        return;
      }
      if (data.type === "CHAT") {
        setMessages(p => [...p, { role: "assistant", content: data.content }]);
      }
    };

    ws.onclose = () => setConnected(false);

    return () => ws.close();
  }, []);

  /* TOGGLE LIVE MODE */
  const toggleLiveMode = () => {
    const token = localStorage.getItem("access_token");

    if (!liveMode) {
      console.log("[LIVE MODE] START");
      setStatus("Connecting...");

      const ws = new WebSocket(`ws://localhost:8000/ws/chat/live?token=${token}`);

      ws.onopen = () => {
        console.log("[LIVE WS] Connected");
        startMicStream(ws);
        setStatus("Listening...");
      };

      ws.onmessage = (e) => {
        const data = JSON.parse(e.data);

        if (data.type === "USER_TRANSCRIPT") {
          setMessages(p => [...p, { role: "user", content: data.content }]);
          setStatus("Thinking...");
        }

        if (data.type === "CHAT") {
          setMessages(p => [...p, { role: "assistant", content: data.content }]);
          muteMic();
          setStatus("Speaking...");
          speakText(data.content, () => {
            unmuteMic();
            setStatus("Listening...");
            console.log("[TTS] Finished – mic unmuted, listening resumed");
          });
        }
      };

      ws.onclose = () => {
        console.log("[LIVE WS] Closed");
        setStatus("");
        setLiveMode(false);
      };

      liveWsRef.current = ws;
      setLiveMode(true);

    } else {
      console.log("[LIVE MODE] STOP");
      setStatus("Stopping...");

      if (liveWsRef.current?.readyState === WebSocket.OPEN) {
        liveWsRef.current.send("STOP");
      }

      // Give a moment for STOP to be processed
      setTimeout(() => {
        stopMicStream();
        liveWsRef.current?.close();
        liveWsRef.current = null;
        setLiveMode(false);
        setStatus("");
      }, 400);
    }
  };

  /* SEND TEXT MESSAGE */
  const sendMessage = () => {
    if (!input.trim()) return;
    chatWsRef.current.send(input);
    setMessages(p => [...p, { role: "user", content: input }]);
    setInput("");
  };

  const handleNavigation = ({ tool, payload }) => {
    const routes = {
      CareerPredictor: "/career",
      RoadmapGenerator: "/roadmap",
      JobSearch: "/jobs",
      LinkedInAssistant: "/linkedin",
      QuizGenerator: "/quiz",
      TechNews: "/news",
      MusicRecommender: "/news",
      NetworkingEvents: "/news",
      CVGeneration: "/news",
      EmotionalSupport: "/emotional-support"
    };
    if (routes[tool]) navigate(routes[tool], payload ? { state: payload } : {});
  };

  /* UI */
  return (
    <div className="orchestrator-chat">
      <div className="header">
        <span>🧠 MAARGHA Orchestrator</span>
        <button onClick={onClose}>✕</button>
      </div>

      <button
        className={`live-btn ${liveMode ? "active" : ""}`}
        onClick={toggleLiveMode}
      >
        🎤 {liveMode ? "Live Mode ON" : "Live Mode"}
      </button>

      {liveMode && status && (
        <div className="status-bar" style={{ textAlign: "center", padding: "8px", color: "#666" }}>
          {status}
        </div>
      )}

      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            {m.content}
          </div>
        ))}
        {!connected && <div className="msg system">Connecting…</div>}
      </div>

      <div className="input-bar">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Talk to the orchestrator..."
          disabled={liveMode} // optional: disable text input during voice mode
        />
        <button onClick={sendMessage} disabled={liveMode}>Send</button>
      </div>
    </div>
  );
}