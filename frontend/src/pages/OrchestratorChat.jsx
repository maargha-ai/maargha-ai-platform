import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  User,
  Bot,
  Mic,
  Send,
  Cpu,
  Target
} from "lucide-react";
import { useTheme } from "../components/ThemeProvider";
import { Button } from "../components/ui/button";
import VoiceModal from "../components/VoiceModal";
import {
  startMicStream,
  stopMicStream,
  muteMic,
  unmuteMic
} from "../pages/emotional-support/useAudioStream";

import "../styles/orchestrator.css";
import "../index.css";
/*INLINE TTS*/
function speakText(text, onEnd) {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";
  utterance.rate = 1;
  utterance.pitch = 1;

  utterance.onend = onEnd;
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utterance);
}

export default function OrchestratorChat() {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const scrollRef = useRef(null);

  const chatWsRef = useRef(null);   // TEXT WS
  const liveWsRef = useRef(null);   // AUDIO WS

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Welcome to Maargha Orchestrator. I'm your AI career architect. How can I help you shape your future today?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [liveMode, setLiveMode] = useState(false);
  const [status, setStatus] = useState(""); // "Listening...", "Thinking...", etc.
  const [volume, setVolume] = useState(0);

  const suggestions = [
    "I need someone to listen to my feelings",
    "Generate a 6-month study plan",
    "Show me latest events",
    "Find me jobs that matches my profile"
  ];

  /* TEXT CHAT WS */
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const ws = new WebSocket(`ws://localhost:8000/ws/chat?token=${token}`);
    chatWsRef.current = ws;

    ws.onopen = () => {
      console.log("[CHAT WS] Connected");
    };

    ws.onmessage = (e) => {
      setIsTyping(false);
      const data = JSON.parse(e.data);
      if (data.navigate) {
        handleNavigation(data.navigate);
        return;
      }
      if (data.type === "CHAT") {
        setMessages(p => [...p, {
          role: "assistant",
          content: data.content,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }]);
      }
    };

    ws.onclose = () => {
      console.log("[CHAT WS] Closed");
    };

    return () => ws.close();
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  /* TOGGLE LIVE MODE */
  const toggleLiveMode = () => {
    const token = localStorage.getItem("access_token");

    if (!liveMode) {
      console.log("[LIVE MODE] START");
      setStatus("Connecting...");

      const ws = new WebSocket(`ws://localhost:8000/ws/chat/live?token=${token}`);

      ws.onopen = () => {
        console.log("[LIVE WS] Connected");
        startMicStream(ws, (v) => setVolume(v));
        setStatus("Listening...");
      };

      ws.onmessage = (e) => {
        const data = JSON.parse(e.data);

        if (data.type === "USER_TRANSCRIPT") {
          setMessages(p => [...p, {
            role: "user",
            content: data.content,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }]);
          setStatus("Thinking...");
        }

        if (data.type === "CHAT") {
          setMessages(p => [...p, {
            role: "assistant",
            content: data.content,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }]);
          muteMic();
          setStatus("Speaking...");
          speakText(data.content, () => {
            unmuteMic();
            setStatus("Listening...");
            console.log("[TTS] Finished – mic unmuted, listening resumed");
          });
        }

        // Handle navigation from live chat
        if (data.navigate) {
          handleNavigation(data.navigate);
          closeLiveMode();
          return;
        }
      };

      ws.onclose = () => {
        console.log("[LIVE WS] Closed");
        setStatus("");
        setLiveMode(false);
        setVolume(0);
      };

      liveWsRef.current = ws;
      setLiveMode(true);

    } else {
      console.log("[LIVE MODE] STOP");
      closeLiveMode();
    }
  };

  const closeLiveMode = () => {
    setStatus("Stopping...");
    if (liveWsRef.current?.readyState === WebSocket.OPEN) {
      liveWsRef.current.send("STOP");
    }
    setTimeout(() => {
      stopMicStream();
      liveWsRef.current?.close();
      liveWsRef.current = null;
      setLiveMode(false);
      setStatus("");
      setVolume(0);
    }, 400);
  };

  /* SEND TEXT MESSAGE */
  const sendMessage = () => {
    if (!input.trim()) return;

    if (chatWsRef.current && chatWsRef.current.readyState === WebSocket.OPEN) {
      chatWsRef.current.send(input);
      setMessages(p => [...p, {
        role: "user",
        content: input,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
      setInput("");
      setIsTyping(true);
    } else {
      setMessages(p => [...p, {
        role: "assistant",
        content: "I'm currently disconnected. Please check your connection.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    }
  };

  const handleNavigation = ({ tool, payload }) => {
    const routes = {
      CareerPredictor: "/career",
      RoadmapGenerator: "/roadmap",
      JobSearch: "/jobs",
      LinkedInAssistant: "/linkedin",
      QuizGenerator: "/quiz",
      TechNews: "/news",
      MusicRecommender: "/music",
      NetworkingEvents: "/networking-events",
      CVGeneration: "/cv",
      EmotionalSupport: "/emotional-support",
      AITutor: "/tutor",
      ResumeParser: "/resume-parser"
    };
    if (routes[tool]) navigate(routes[tool], payload ? { state: payload } : {});
  };

  return (
    <div className={`orchestrator-layout ${theme}`}>
      <div className="orch-bg-overlay">
        <div className="orch-gradient-sphere pulse-1"></div>
        <div className="orch-gradient-sphere pulse-2"></div>
      </div>

      <main className="orch-main">
        <header className="orch-header border-b border-border/40 backdrop-blur-md bg-background/50">
          <div className="flex items-center justify-between w-full px-6">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => navigate("/dashboard")}
              className="rounded-full hover:bg-primary/10"
            >
              <ArrowLeft size={20} />
            </Button>
            <div className="flex flex-col items-center flex-1">
              <h1 className="text-xl font-bold leading-none tracking-tight">Maargha Orchestrator</h1>
              <span className="text-xs text-muted-foreground flex items-center gap-1.5 mt-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                Online
              </span>
            </div>
            <div className="w-10" />
          </div>
        </header>

        <div className="orchestrator-content-wrapper">
          <aside className="orchestrator-feature-sidebar">
            <div className="orchestrator-feature-box">
              <div className="orchestrator-feature-header">
                <Cpu size={24} className="text-indigo-500" />
                <h3>Maargha Orchestrator</h3>
              </div>
              
              <div className="orchestrator-feature-content">
                <p className="orchestrator-feature-description">
                  Your central AI command center for seamless career management and multi-agent coordination.
                </p>
                
                <div className="orchestrator-feature-sections">
                  <div className="orchestrator-feature-section">
                    <h4 className="feature-title">How It Works</h4>
                    <ul className="orchestrator-feature-steps">
                      <li>Ask any career question</li>
                      <li>Coordinate between AI agents</li>
                      <li>Get real-time data & insights</li>
                      <li>Execute strategic plans</li>
                    </ul>
                  </div>
                </div>
                
                <div className="orchestrator-feature-footer">
                  <div className="orchestrator-feature-tip">
                    <Target size={16} className="text-blue-500" />
                    <span>Tip: Use natural language for best results!</span>
                  </div>
                </div>
              </div>
            </div>
          </aside>

          <div className="orchestrator-chat-engine">
            <div className="orchestrator-chat-full">
              <div className="messages-area" ref={scrollRef}>
                {messages.map((m, i) => (
                  <div key={i} className={`msg-wrapper ${m.role === 'assistant' ? 'ai' : 'user'}`}>
                    <div className="msg-avatar">
                      {m.role === "assistant" ? <Bot size={20} /> : <User size={20} />}
                    </div>
                    <div className="msg-content">
                      <div className="msg-bubble">
                        {m.content}
                      </div>
                      <span className="msg-time">{m.timestamp}</span>
                    </div>
                  </div>
                ))}

                {messages.length === 1 && (
                  <div className="suggestions-grid">
                    {suggestions.map((s, i) => (
                      <button
                        key={i}
                        className="suggestion-chip"
                        onClick={() => {
                          if (chatWsRef.current?.readyState === WebSocket.OPEN) {
                            chatWsRef.current.send(s);
                            setMessages(p => [...p, { role: "user", content: s, timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }]);
                            setIsTyping(true);
                          }
                        }}
                      >
                        {s}
                        <ArrowRight size={14} />
                      </button>
                    ))}
                  </div>
                )}

                {isTyping && (
                  <div className="msg-wrapper ai">
                    <div className="msg-avatar">
                      <Bot size={20} />
                    </div>
                    <div className="msg-content">
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <footer className="orch-footer">
                <div className="input-container glass-morphism">
                  <textarea
                    placeholder="Message Maargha Orchestrator..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" && !e.shiftKey) {
                        e.preventDefault();
                        sendMessage();
                      }
                    }}
                    rows={1}
                  />
                  <div className="input-actions flex items-center gap-2">
                    <button
                      className={`mic-btn ${liveMode ? 'active' : ''}`}
                      onClick={toggleLiveMode}
                      title="Voice Mode"
                    >
                      <Mic size={18} />
                    </button>
                    <button
                      className={`send-btn ${input.trim() ? 'active' : ''}`}
                      onClick={sendMessage}
                      disabled={!input.trim()}
                    >
                      <Send size={18} />
                    </button>
                  </div>
                </div>
              </footer>
            </div>
          </div>
        </div>
      </main>

      <VoiceModal
        isOpen={liveMode}
        onClose={closeLiveMode}
        status={status}
        volume={volume}
      />
    </div>
  );
}