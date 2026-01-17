import { useEffect, useRef, useState } from "react";

export default function LinkedInAssistant() {
  const wsRef = useRef(null);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const ws = new WebSocket(
      `ws://localhost:8000/ws/linkedin?token=${token}`
    );

    wsRef.current = ws;

    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.type === "linkedin_reply") {
        setMessages(prev => [...prev, { role: "assistant", text: msg.message }]);
      }
    };

    return () => ws.close();
  }, []);

  const send = () => {
    if (!input.trim()) return;

    setMessages(prev => [...prev, { role: "user", text: input }]);

    wsRef.current.send(JSON.stringify({
      type: "linkedin_message",
      message: input
    }));

    setInput("");
  };

  return (
    <div className="linkedin-page">
      <h2>LinkedIn Assistant</h2>

      <div className="chat-box">
        {messages.map((m, i) => (
          <div key={i} className={`chat ${m.role}`}>
            {m.text}
          </div>
        ))}
      </div>

      <textarea
        placeholder="Ask about LinkedIn profile, posts, growth..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      <button onClick={send}>Send</button>
    </div>
  );
}
