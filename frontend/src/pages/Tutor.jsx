import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Send,
  Bot,
  User,
  ArrowRight,
  Brain,
  Target
} from "lucide-react";
import { useTheme } from "../components/ThemeProvider";
import { Button } from "../components/ui/button";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import "../index.css";

export default function Tutor() {
  const navigate = useNavigate();
  const { theme } = useTheme();

  const wsRef = useRef(null);
  const scrollRef = useRef(null);

  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hello! I'm your Maargha AI Tutor. I can help you understand complex IT concepts, debug code, or explain system architectures. What are we learning today?",
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    }
  ]);

  /* ===============================
     Stable WebSocket Lifecycle
  =============================== */
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) return;

    const WS = import.meta.env.VITE_WS_BASE_URL;
    const ws = new WebSocket(`${WS}/ws/tutor?token=${token}`);
    wsRef.current = ws;

    ws.onopen = () => console.log("Tutor WS connected");

    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);

      if (msg.type === "tutor_answer") {
        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            text: msg.answer,
            timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
          }
        ]);
        setIsTyping(false);
      }
    };

    ws.onclose = () => console.log("Tutor WS closed");

    // graceful leave instead of force close
    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "leave_tutor" }));
      }
    };
  }, []);

  /* ===============================
     Auto scroll
  =============================== */
  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth"
    });
  }, [messages, isTyping]);

  /* ===============================
     Send Message
  =============================== */
  const send = () => {
    if (!input.trim() || wsRef.current?.readyState !== WebSocket.OPEN) return;

    const text = input;

    setMessages(prev => [
      ...prev,
      {
        role: "user",
        text,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
      }
    ]);

    setInput("");
    setIsTyping(true);

    wsRef.current.send(JSON.stringify({
      type: "tutor_question",
      question: text
    }));
  };

  const topicSuggestions = [
    "Explain React Hooks",
    "How does Docker work?",
    "System Design for Scale",
    "Python Generative AI Basics"
  ];

  /* ===============================
     UI
  =============================== */
  return (
    <div className={`tutor-layout flex flex-col h-screen w-full bg-background text-foreground ${theme}`}>
      <header className="flex h-16 items-center border-b border-border/40 bg-background/80 backdrop-blur-xl px-6">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => navigate("/dashboard")}
          className="rounded-full"
        >
          <ArrowLeft size={20} />
        </Button>

        <div className="flex flex-col items-center flex-1">
          <h1 className="text-xl font-bold">AI Knowledge Tutor</h1>
          <span className="text-xs text-muted-foreground uppercase tracking-widest font-bold">
            Concept Mastery
          </span>
        </div>
      </header>

      <div className="tutor-content-wrapper">
        <aside className="tutor-feature-sidebar">
          <div className="tutor-feature-box">
            <div className="tutor-feature-header">
              <Brain size={24} className="text-pink-500" />
              <h3>Knowledge Mastery Engine</h3>
            </div>
            
            <div className="tutor-feature-content">
              <p className="tutor-feature-description">
                Personalized AI tutoring for deep conceptual understanding and skill mastery.
              </p>
              
              <div className="tutor-feature-sections">
                <div className="tutor-feature-section">
                  <h4 className="feature-title">How It Works</h4>
                  <ul className="tutor-feature-steps">
                    <li>Choose a learning topic</li>
                    <li>Ask complex questions</li>
                    <li>Get structured explanations</li>
                    <li>Master core concepts</li>
                  </ul>
                </div>
              </div>
              
              <div className="tutor-feature-footer">
                <div className="tutor-feature-tip">
                  <Target size={16} className="text-blue-500" />
                  <span>Tip: Ask for examples to better understand!</span>
                </div>
              </div>
            </div>
          </div>
        </aside>

        <div className="tutor-chat-engine">
          <main ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-8 custom-scroll">
            <div className="max-w-3xl mx-auto space-y-8">
              {messages.map((m, i) => (
                <div key={i} className={`flex gap-4 ${m.role === "user" ? "flex-row-reverse" : ""}`}>
                  <div className={`w-9 h-9 rounded-xl flex items-center justify-center border ${m.role === "assistant" ? "bg-primary text-primary-foreground" : "bg-secondary"}`}>
                    {m.role === "assistant" ? <Bot size={18} /> : <User size={18} />}
                  </div>

                  <div className={`max-w-[85%] ${m.role === "user" ? "items-end" : ""}`}>
                    <div className={`px-5 py-4 rounded-2xl text-[15px] leading-7 shadow-sm ${m.role === "assistant" ? "bg-card border rounded-tl-sm" : "bg-primary text-primary-foreground rounded-tr-sm"}`}>
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {m.text}
                      </ReactMarkdown>
                    </div>
                    <span className="text-[10px] text-muted-foreground px-1">{m.timestamp}</span>
                  </div>
                </div>
              ))}

              {isTyping && (
                <div className="flex gap-4">
                  <div className="w-9 h-9 rounded-xl bg-primary text-primary-foreground flex items-center justify-center animate-pulse">
                    <Bot size={18} />
                  </div>
                  <div className="bg-card border px-5 py-3 rounded-2xl">
                    Typing...
                  </div>
                </div>
              )}

              {messages.length === 1 && (
                <div className="pt-8 grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {topicSuggestions.map(s => (
                    <button
                      key={s}
                      onClick={() => {
                        setInput(s);
                        setTimeout(send, 0);
                      }}
                      className="flex items-center justify-between p-4 rounded-2xl bg-secondary/40 border hover:bg-secondary/60 transition-all text-left"
                    >
                      <span className="text-sm font-medium">{s}</span>
                      <ArrowRight size={14} />
                    </button>
                  ))}
                </div>
              )}
            </div>
          </main>

          <footer className="p-4 border-t border-border/40 bg-background">
            <div className="max-w-3xl mx-auto flex items-end gap-3 bg-card border rounded-2xl p-2.5">
              <textarea
                placeholder="Ask anything about software engineering..."
                className="flex-1 bg-transparent outline-none resize-none py-2 px-3 text-sm min-h-[44px]"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    send();
                  }
                }}
              />
              <Button onClick={send} disabled={!input.trim()} className="h-10 w-10 rounded-xl p-0">
                <Send size={18} />
              </Button>
            </div>
          </footer>
        </div>
      </div>
    </div>
  );
}
