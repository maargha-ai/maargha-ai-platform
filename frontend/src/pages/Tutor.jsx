import { useEffect, useRef, useState } from "react";

export default function Tutor() {
  const wsRef = useRef(null);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const ws = new WebSocket(
      `ws://localhost:8000/ws/tutor?token=${token}`
    );

    wsRef.current = ws;

    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.type === "tutor_answer") {
        setMessages(prev => [
          ...prev,
          { role: "assistant", text: msg.answer }
        ]);
      }
    };

    return () => ws.close();
  }, []);

  const send = () => {
    if (!input.trim()) return;

    setMessages(prev => [...prev, { role: "user", text: input }]);

    wsRef.current.send(JSON.stringify({
      type: "tutor_question",
      question: input
    }));

    setInput("");
  };

  return (
    <div className="tutor-page">
      <h2>AI Tutor</h2>

      <div className="chat-box">
        {messages.map((m, i) => (
          <div key={i} className={`chat ${m.role}`}>
            {m.text}
          </div>
        ))}
      </div>

      <textarea
        placeholder="Ask any IT concept..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      <button onClick={send}>Ask Tutor</button>
    </div>
  );
}
