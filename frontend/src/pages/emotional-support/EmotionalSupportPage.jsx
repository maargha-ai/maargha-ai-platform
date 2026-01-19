import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Mic,
  MicOff,
  LogOut,
  HeartHandshake
} from "lucide-react";
import {
  startMicStream,
  stopMicStream,
  muteMic,
  unmuteMic
} from "./useAudioStream"; // Ensure this path is correct based on folder structure
import "../../styles/emotional-support.css";

export default function EmotionalSupportPage() {
  const [active, setActive] = useState(false);
  const [messages, setMessages] = useState([]);
  const wsRef = useRef(null);
  const navigate = useNavigate();
  const chatEndRef = useRef(null);

  useEffect(() => {
    speechSynthesis.getVoices();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const speak = (text) => {
    muteMic(); // 🔇 STOP MIC

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.pitch = 1.1; // Slightly softer pitch

    const voices = speechSynthesis.getVoices();
    // Try to find a soothing female voice
    const voice = voices.find(v =>
      v.name.includes("Google US English") ||
      v.name.includes("Samantha") ||
      v.name.includes("Zira") ||
      (v.lang.startsWith("en") && v.name.includes("Female"))
    );

    if (voice) utterance.voice = voice;

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
      // Initial greeting
      setMessages([{ role: "agent", text: "Hello. I'm Emily. I'm here to listen. How are you feeling right now?" }]);
      speak("Hello. I'm Emily. I'm here to listen. How are you feeling right now?");
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
    speechSynthesis.cancel();
    navigate("/dashboard");
  };

  return (
    <div className="emotional-layout">
      <div className="emotional-bg"></div>
      
      <div className="emotional-container">
         <div className="avatar-section">
            <div className="avatar-circle">
               <div className={`avatar-pulse ${active ? 'active' : ''}`}></div>
               <HeartHandshake size={64} className="text-primary relative z-30" />
            </div>
            <h1 className="agent-name">Emily</h1>
            <p className="agent-role">Empathetic AI Companion</p>
         </div>

         {messages.length > 0 && (
           <div className="chat-grid">
             {messages.map((m, i) => (
               <div key={i} className={`chat-bubble ${m.role}`}>
                 {m.text}
               </div>
             ))}
             <div ref={chatEndRef} />
           </div>
         )}
         
         <div className="controls-section">
            {!active ? (
              <button className="action-btn start-btn" onClick={startSupport}>
                <Mic size={20} /> Start Session
              </button>
            ) : (
              <div className="flex flex-col items-center gap-2">
                 <button className="action-btn stop-btn" onClick={stopAndExit}>
                   <LogOut size={20} /> End Session
                 </button>
                 <span className="text-xs text-muted-foreground animate-pulse">Listening...</span>
              </div>
            )}
         </div>
      </div>
    </div>
  );
}
