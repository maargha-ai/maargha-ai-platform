import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Send,
  ArrowLeft,
  Linkedin,
  User,
  Bot,
  Sparkles,
  ArrowRight,
  Zap,
  Layout,
  Share2
} from "lucide-react";
import { useTheme } from "../components/ThemeProvider";
import { Button } from "../components/ui/button";

export default function LinkedInAssistant() {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const wsRef = useRef(null);
  const scrollRef = useRef(null);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Welcome to LinkedIn Growth AI. I'm your personal branding strategist. I can help you craft viral posts, optimize your headline, or draft high-conversion connection requests. How can we boost your professional presence today?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const ws = new WebSocket(`ws://localhost:8000/ws/linkedin?token=${token}`);
    wsRef.current = ws;

    ws.onmessage = (e) => {
      setIsTyping(false);
      const msg = JSON.parse(e.data);
      if (msg.type === "linkedin_reply") {
        setMessages(prev => [...prev, {
          role: "assistant",
          text: msg.message,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }]);
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
        type: "linkedin_message",
        message: input
      }));
    } else {
      setTimeout(() => {
        setIsTyping(false);
        setMessages(prev => [...prev, {
          role: "assistant",
          text: "Neural processing offline. Please check your connection to the strategic engine.",
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }]);
      }, 1500);
    }
    setInput("");
  };

  const suggestions = [
    "Rewrite my LinkedIn headline",
    "Post idea: Switching to AI",
    "Draft a connection request",
    "Analyze profile best practices"
  ];

  return (
    <div className={`flex flex-col h-screen w-full bg-background text-foreground ${theme}`}>
      <div className="fixed inset-0 pointer-events-none opacity-20">
        <div className="absolute top-[-10%] left-[-5%] w-[40%] h-[40%] rounded-full bg-blue-500/10 blur-[120px]" />
        <div className="absolute bottom-[20%] right-[-10%] w-[35%] h-[35%] rounded-full bg-primary/10 blur-[120px]" />
      </div>

      <header className="flex h-16 shrink-0 items-center justify-between border-b border-border/40 bg-background/80 backdrop-blur-xl px-6 relative z-50">
        <div className="flex items-center">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => navigate("/dashboard")}
            className="rounded-full mr-4"
          >
            <ArrowLeft size={20} />
          </Button>
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-[#0a66c2] flex items-center justify-center text-white">
              <Linkedin size={18} />
            </div>
            <div>
              <h1 className="text-lg font-bold leading-none tracking-tight">Growth Strategist</h1>
              <span className="text-[10px] text-muted-foreground uppercase tracking-widest font-bold">Personal Branding AI</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <div className="px-3 py-1 rounded-full bg-green-500/10 border border-green-500/20 flex items-center gap-1.5">
            <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
            <span className="text-[10px] font-bold text-green-500 uppercase tracking-wider">Live</span>
          </div>
        </div>
      </header>

      <main className="flex-1 overflow-y-auto relative z-10 scrollbar-thin px-4 py-8" ref={scrollRef}>
        <div className="max-w-3xl mx-auto space-y-8">
          {messages.map((m, i) => (
            <div key={i} className={`flex gap-4 ${m.role === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 border ${m.role === 'assistant' ? 'bg-[#0a66c2] text-white border-[#0a66c2]/20' : 'bg-secondary border-border'}`}>
                {m.role === 'assistant' ? <Linkedin size={18} /> : <User size={18} />}
              </div>
              <div className={`flex flex-col gap-1 max-w-[85%] ${m.role === 'user' ? 'items-end' : ''}`}>
                <div className={`px-5 py-3.5 rounded-2xl text-[15px] leading-relaxed shadow-sm ${m.role === 'assistant' ? 'bg-card border border-border/50 rounded-tl-sm' : 'bg-[#0a66c2] text-white rounded-tr-sm'}`}>
                  {m.text}
                </div>
                <span className="text-[10px] text-muted-foreground px-1">{m.timestamp}</span>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex gap-4">
              <div className="w-9 h-9 rounded-xl bg-[#0a66c2] text-white flex items-center justify-center animate-pulse">
                <Bot size={18} />
              </div>
              <div className="bg-card border border-border/50 px-5 py-3.5 rounded-2xl rounded-tl-sm flex items-center gap-2">
                <Sparkles size={14} className="animate-spin text-blue-500" />
                <span className="text-sm italic text-muted-foreground">Strategizing...</span>
              </div>
            </div>
          )}

          {messages.length === 1 && (
            <div className="pt-8 grid grid-cols-1 sm:grid-cols-2 gap-3">
              {suggestions.map(s => (
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
                      wsRef.current.send(JSON.stringify({ type: "linkedin_message", message: s }));
                    }
                  }}
                  className="flex items-center justify-between p-4 rounded-2xl bg-secondary/40 border border-border/40 hover:bg-secondary/60 hover:border-blue-500/30 transition-all text-left group"
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
        <div className="max-w-3xl mx-auto">
          <div className="flex items-center gap-4 mb-4 overflow-x-auto pb-2 no-scrollbar">
            {[
              { icon: Layout, label: "Template" },
              { icon: Zap, label: "Neural-Rewrite" },
              { icon: Share2, label: "Viral-Check" }
            ].map(t => (
              <button key={t.label} className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-secondary/50 border border-border/40 text-[10px] font-bold uppercase tracking-widest hover:bg-secondary transition-colors whitespace-nowrap">
                <t.icon size={12} className="text-blue-500" />
                {t.label}
              </button>
            ))}
          </div>

          <div className="flex items-end gap-3 bg-card border border-border/50 rounded-2xl p-2.5 shadow-lg focus-within:border-blue-500/50 transition-colors">
            <textarea
              placeholder="Post ideas, profile tips, connection scripts..."
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
              className="h-10 w-10 rounded-xl shrink-0 p-0 bg-[#0a66c2] hover:bg-[#004182] text-white"
            >
              <Send size={18} />
            </Button>
          </div>
          <p className="text-[10px] text-center text-muted-foreground mt-3 uppercase tracking-tighter">
            LinkedIn Strategic Intelligence • Personalized Branding
          </p>
        </div>
      </footer>
    </div>
  );
}
