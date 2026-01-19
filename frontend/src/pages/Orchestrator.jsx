import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { 
  ArrowLeft,
  ArrowRight, 
  User, 
  Bot, 
  Sparkles,
  Mic,
  Send
} from "lucide-react";
import { useTheme } from "../components/ThemeProvider";
import { Button } from "../components/ui/button";
import "../styles/orchestrator.css";
export default function Orchestrator() {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const scrollRef = useRef(null);
  const wsRef = useRef(null);
  const [messages, setMessages] = useState([
    { 
      from: "ai", 
      text: "Welcome to Maargha Orchestrator. I'm your AI career architect. How can I help you shape your future today?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const suggestions = [
    "Analyze my resume quality",
    "Generate a 6-month study plan",
    "Mock interview: React Senior Dev",
    "Find high-paying remote roles"
  ];
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    wsRef.current = new WebSocket(
      `ws://localhost:8000/ws/chat?token=${token}`
    );
    wsRef.current.onmessage = (event) => {
      setIsTyping(false);
      setMessages((prev) => [
        ...prev,
        { 
          from: "ai", 
          text: event.data,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        },
      ]);
    };
    wsRef.current.onerror = () => {
      console.error("WebSocket error");
      setIsTyping(false);
    };
    return () => {
      wsRef.current?.close();
    };
  }, []);
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);
  const sendMessage = () => {
    if (!input.trim()) return;
    const userMessage = { 
      from: "user", 
      text: input,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(input);
    } else {
      setTimeout(() => {
        setIsTyping(false);
        setMessages(prev => [...prev, {
          from: "ai",
          text: "I'm currently disconnected from the neural grid. Please check your connection.",
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }]);
      }, 1500);
    }
  };
  return (
    <div className={`orchestrator-layout ${theme}`}>
      <div className="orch-bg-overlay">
        <div className="orch-gradient-sphere pulse-1"></div>
        <div className="orch-gradient-sphere pulse-2"></div>
      </div>
      <main className="orch-main w-full h-full flex flex-col">
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
        <div className="messages-viewport" ref={scrollRef}>
          <div className="messages-inner">
            {messages.map((m, i) => (
              <div key={i} className={`msg-wrapper ${m.from}`}>
                <div className="msg-avatar">
                   {m.from === "ai" ? <Bot size={20} /> : <User size={20} />}
                </div>
                <div className="msg-content">
                  <div className="msg-bubble">
                    {m.text}
                  </div>
                  <span className="msg-time">{m.timestamp}</span>
                </div>
              </div>
            ))}
            {messages.length === 1 && (
              <div className="suggestions-grid">
                {suggestions.map((s, i) => (
                  <button key={i} className="suggestion-chip" onClick={() => setInput(s)}>
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
                className={`send-btn ${input.trim() ? 'active' : ''}`}
                onClick={sendMessage}
                disabled={!input.trim()}
              >
                <Send size={18} />
              </button>
            </div>
          </div>
          <p className="footer-note">
            Maargha AI may provide inaccurate info. Verify important career steps.
          </p>
        </footer>
      </main>
    </div>
  );
}


