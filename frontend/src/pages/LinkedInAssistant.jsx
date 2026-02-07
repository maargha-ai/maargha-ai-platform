import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { 
  Send, 
  ArrowLeft, 
  Linkedin, 
  User, 
  Bot, 
  Image, 
  Paperclip,
  Sparkles,
  ThumbsUp,
  Share2
} from "lucide-react";
import { useTheme } from "../components/ThemeProvider";
import { Button } from "../components/ui/button";
import "../styles/linkedin.css";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
export default function LinkedInAssistant() {
  const navigate = useNavigate();
  const { theme, setTheme } = useTheme();
  const wsRef = useRef(null);
  const scrollRef = useRef(null);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const ws = new WebSocket(
      `ws://localhost:8000/ws/linkedin?token=${token}`
    );
    wsRef.current = ws;
    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.type === "linkedin_reply") {
        setIsTyping(false);
        setMessages(prev => [...prev, { role: "assistant", text: msg.message }]);
      }
    };
    ws.onerror = () => setIsTyping(false);
    return () => ws.close();
  }, []);
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);
  const send = () => {
    if (!input.trim()) return;
    setMessages(prev => [...prev, { role: "user", text: input }]);
    setIsTyping(true);
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: "linkedin_message",
        message: input
      }));
    } else {
        setTimeout(() => {
            setIsTyping(false);
            setMessages(prev => [...prev, { role: "assistant", text: "I'm simulating a response as the connection seems unstable. In a real scenario, I'd analyze your profile or generate a post now." }]);
        }, 1500);
    }
    setInput("");
  };
  return (
    <div className={`linkedin-layout ${theme}`}>
      <div className="linkedin-bg"></div>
      <main className="li-main">
        {}
        <header className="li-header">
          <div className="flex items-center gap-3">
             <Button variant="ghost" size="icon" onClick={() => navigate("/dashboard")} className="rounded-full">
                <ArrowLeft size={22} />
             </Button>
             <div className="li-brand">
               <div className="li-logo"><Linkedin size={20} /></div>
               <div className="flex flex-col">
                 <h1 className="text-lg font-bold leading-none">LinkedIn Growth AI</h1>
                 <span className="text-xs text-muted-foreground">Personal Branding Expert</span>
               </div>
             </div>
          </div>
        </header>
        {}
        <div className="li-chat-viewport" ref={scrollRef}>
          {messages.length === 0 && (
            <div className="li-welcome">
               <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                 <Linkedin size={32} />
               </div>
               <h2 className="text-2xl font-bold mb-2">Optimize Your Presence</h2>
               <p className="max-w-md mx-auto">
                 I can help you audit your profile, write viral posts, or draft connection requests.
               </p>
               <div className="flex flex-wrap justify-center gap-2 mt-6">
                 {["Review my headline", "Draft a post about AI", "Connection request for clear", "Analyze recent trends"].map(s => (
                   <button 
                     key={s} 
                     className="px-4 py-2 bg-secondary/50 hover:bg-secondary rounded-full text-sm font-medium transition"
                     onClick={() => setInput(s)}
                   >
                     {s}
                   </button>
                 ))}
               </div>
            </div>
          )}
          {messages.map((m, i) => (
            <div key={i} className={`li-message ${m.role}`}>
              <div className="li-avatar">
                {m.role === 'assistant' ? <Bot size={20} /> : <User size={20} />}
              </div>
              <div className="li-bubble markdown">
                <ReactMarkdown remarkPlugins={[remarkGfm]} components={{p: ({ children }) => <p className="mb-2">{children}</p>}}>{m.text}</ReactMarkdown>
              </div>
            </div>
          ))}
          {isTyping && (
             <div className="li-message assistant">
               <div className="li-avatar">
                 <Bot size={20} />
               </div>
               <div className="li-bubble italic text-muted-foreground flex items-center gap-2">
                 <Sparkles size={16} className="animate-spin" />
                 Drafting strategy...
               </div>
             </div>
          )}
        </div>
        {}
        <footer className="li-footer">
          <div className="li-input-box">
            <textarea
              placeholder="Ask for post ideas, profile tips, or networking scripts..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if(e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  send();
                }
              }}
              rows={1}
            />
            <div className="li-input-actions">
              <div className="li-tools">
              </div>
              <button className="li-send-btn" onClick={send} disabled={!input.trim()}>
                Send 
              </button>
            </div>
          </div>
        </footer>
      </main>
    </div>
  );
}


