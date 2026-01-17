import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  startMicStream,
  stopMicStream,
  muteMic,
  unmuteMic
} from "./useAudioStream";

export default function EmotionalSupportPage() {
  const [active, setActive] = useState(false);
  const [messages, setMessages] = useState([]);
  const wsRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    speechSynthesis.getVoices();
  }, []);

  const speak = (text) => {
    muteMic(); // 🔇 STOP MIC

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.pitch = 1.2;

    const voices = speechSynthesis.getVoices();
    const female = voices.find(v =>
      v.name.toLowerCase().includes("zira") ||
      v.name.toLowerCase().includes("female") ||
      v.name.toLowerCase().includes("samantha")
    );

    if (female) utterance.voice = female;

    utterance.onend = () => {
      setTimeout(() => {
        unmuteMic();  // 🎤 RESUME MIC AFTER SPEECH
      }, 500); // small buffer
    };

    speechSynthesis.speak(utterance);
  };


  const startSupport = () => {
    const token = localStorage.getItem("access_token");

    const ws = new WebSocket(
      `ws://localhost:8000/ws/emotional-support?token=${token}`
    );

    ws.onopen = () => {
      startMicStream(ws);
      setActive(true);
    };

    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);

      if (data.type === "user_text") {
        setMessages(prev => [...prev, { role: "user", text: data.text }]);
      }

      if (data.type === "agent_reply") {
        setMessages(prev => [...prev, { role: "agent", text: data.text }]);
        speak(data.text);
      }
    };

    wsRef.current = ws;
  };

  const stopAndExit = () => {
    stopMicStream();

    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    navigate("/dashboard");
  };

  return (
    <div style={{ padding: 40, background: "white", color: "black" }}>
      <h1>Emily 💙</h1>
      <h3>Your emotional support companion</h3>

      {!active && (
        <button onClick={startSupport}>Start</button>
      )}

      <button style={{ marginLeft: 20 }} onClick={stopAndExit}>
        Stop
      </button>

      <div style={{ marginTop: 30, maxWidth: 600 }}>
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              background: m.role === "user" ? "#e6f2ff" : "#f2f2f2",
              padding: 10,
              borderRadius: 6,
              marginBottom: 10
            }}
          >
            <strong>{m.role === "user" ? "You" : "Emily"}:</strong> {m.text}
          </div>
        ))}
      </div>
    </div>
  );
}
