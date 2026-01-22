import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Send,
  Bot,
  User,
  Sparkles,
  BookOpen,
  ArrowRight
} from "lucide-react";
import { useTheme } from "../components/ThemeProvider";
import { Button } from "../components/ui/button";

export default function Tutor() {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const wsRef = useRef(null);
  const scrollRef = useRef(null);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hello! I'm your Maargha AI Tutor. I can help you understand complex IT concepts, debug code, or explain system architectures. What are we learning today?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const ws = new WebSocket(`ws://localhost:8000/ws/tutor?token=${token}`);
    wsRef.current = ws;

    ws.onmessage = (e) => {
      setIsTyping(false);
      const msg = JSON.parse(e.data);
      if (msg.type === "tutor_answer") {
        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            text: msg.answer,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }
        ]);
      }
    };

    return () => ws.close();
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const send = () => {
    if (!input.trim()) return;

    const userMsg = {
      role: "user",
      text: input,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setIsTyping(true);

    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: "tutor_question",
        question: input
      }));
    }

    setInput("");
  };

  const topicSuggestions = [
    "Explain React Hooks",
    "How does Docker work?",
    "System Design for Scale",
    "Python Generative AI Basics"
  ];

  return (
    <div className={`flex flex-col h-screen w-full bg-background text-foreground ${theme}`}>
      <div className="fixed inset-0 pointer-events-none opacity-10">
        <div className="absolute top-[20%] right-[-5%] w-[30%] h-[30%] rounded-full bg-primary/30 blur-[100px]" />
        <div className="absolute bottom-[20%] left-[-5%] w-[30%] h-[30%] rounded-full bg-blue-500/20 blur-[100px]" />
      </div>

      <header className="flex h-16 shrink-0 items-center border-b border-border/40 bg-background/80 backdrop-blur-xl px-6 relative z-50">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => navigate("/dashboard")}
          className="rounded-full absolute left-6"
        >
          <ArrowLeft size={20} />
        </Button>
        <div className="flex flex-col items-center flex-1">
          <h1 className="text-xl font-bold leading-none tracking-tight">AI Knowledge Tutor</h1>
          <span className="text-xs text-muted-foreground flex items-center gap-1.5 mt-1.5 uppercase tracking-widest font-bold">Concept Mastery</span>
        </div>
      </header>

      <main className="flex-1 overflow-y-auto relative z-10 scrollbar-thin px-4 py-8" ref={scrollRef}>
        <div className="max-w-3xl mx-auto space-y-8">
          {messages.map((m, i) => (
            <div key={i} className={`flex gap-4 ${m.role === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 border ${m.role === 'assistant' ? 'bg-primary text-primary-foreground border-primary/20' : 'bg-secondary border-border'}`}>
                {m.role === 'assistant' ? <Bot size={18} /> : <User size={18} />}
              </div>
              <div className={`flex flex-col gap-1 max-w-[85%] ${m.role === 'user' ? 'items-end' : ''}`}>
                <div className={`px-5 py-3.5 rounded-2xl text-[15px] leading-relaxed shadow-sm ${m.role === 'assistant' ? 'bg-card border border-border/50 rounded-tl-sm' : 'bg-primary text-primary-foreground rounded-tr-sm'}`}>
                  {m.text}
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
              <div className="bg-card border border-border/50 px-5 py-3.5 rounded-2xl rounded-tl-sm flex items-center gap-2">
                <div className="flex gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce [animation-delay:-0.3s]"></span>
                  <span className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce [animation-delay:-0.15s]"></span>
                  <span className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce"></span>
                </div>
              </div>
            </div>
          )}

          {messages.length === 1 && (
            <div className="pt-8 grid grid-cols-1 sm:grid-cols-2 gap-3">
              {topicSuggestions.map(s => (
                <button
                  key={s}
                  onClick={() => {
                    const userMsg = {
                      role: "user",
                      text: s,
                      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                    };
                    setMessages(prev => [...prev, userMsg]);
                    setIsTyping(true);
                    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
                      wsRef.current.send(JSON.stringify({ type: "tutor_question", question: s }));
                    }
                  }}
                  className="flex items-center justify-between p-4 rounded-2xl bg-secondary/40 border border-border/40 hover:bg-secondary/60 hover:border-primary/30 transition-all text-left group"
                >
                  <span className="text-sm font-medium">{s}</span>
                  <ArrowRight size={14} className="text-muted-foreground group-hover:translate-x-1 transition-transform" />
                </button>
              ))}
            </div>
          )}
        </div>
      </main>

      <footer className="p-4 bg-background/80 backdrop-blur-xl border-t border-border/40 shrink-0 relative z-50">
        <div className="max-w-3xl mx-auto flex items-end gap-3 bg-card border border-border/50 rounded-2xl p-2.5 shadow-lg focus-within:border-primary/50 transition-colors">
          <textarea
            placeholder="Ask anything about software engineering..."
            className="flex-1 bg-transparent border-none outline-none resize-none py-2 px-3 text-sm min-h-[44px] max-h-[120px]"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                send();
              }
            }}
            rows={1}
          />
          <Button
            onClick={send}
            disabled={!input.trim()}
            className="h-10 w-10 rounded-xl shrink-0 p-0"
          >
            <Send size={18} />
          </Button>
        </div>
      </footer>
    </div>
  );
}
