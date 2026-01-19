import { useState } from "react";
import { useNavigate } from "react-router-dom";
import QuizSetup from "./QuizSetup";
import QuizSession from "./QuizSession";
export default function QuizPage() {
  const [socket, setSocket] = useState(null);
  const [question, setQuestion] = useState(null);
  const navigate = useNavigate();
  const startQuiz = (topic, level) => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("Authentication required");
      return;
    }
    const ws = new WebSocket(
      `ws://localhost:8000/ws/quiz?token=${token}`
    );
    ws.onopen = () => {
      console.log("Quiz WS connected");
      ws.send(
        JSON.stringify({
          type: "start_quiz",
          topic,
          level,
        })
      );
    };
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      console.log("Quiz WS:", data);
      if (data.type === "quiz_question") {
        setQuestion(data.question);
      }
      if (data.type === "quiz_evaluation") {
        ws.close();
        navigate("/quiz/evaluation", { state: data.result });
      }
      if (data.type === "error") {
        alert(data.message);
      }
    };
    ws.onerror = (err) => {
      console.error("Quiz WS error", err);
      alert("WebSocket error occurred");
    };
    ws.onclose = () => {
      console.log("Quiz WS closed");
    };
    setSocket(ws);
  };
  if (!question) {
    return <QuizSetup onStart={startQuiz} />;
  }
  return (
    <QuizSession
      socket={socket}
      question={question}
      onStop={() => {
        socket?.close();
        setQuestion(null);
      }}
    />
  );
}


