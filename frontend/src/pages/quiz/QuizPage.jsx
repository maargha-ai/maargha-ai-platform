import { useState } from "react";
import { useNavigate } from "react-router-dom";
import QuizSetup from "./QuizSetup";
import QuizSession from "./QuizSession";

export default function QuizPage() {
  const [socket, setSocket] = useState(null);
  const navigate = useNavigate();

  const startQuiz = (topic, level) => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("Authentication required");
      return;
    }
    const WS = import.meta.env.VITE_WS_BASE_URL;
    const ws = new WebSocket(
      `${WS}/ws/quiz?token=${token}`
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

      if (data.type === "quiz_evaluation") {
        ws.close();
        setSocket(null);
        navigate("/quiz/evaluation", { state: data.result });
      }

      if (data.type === "quiz_terminated") {
        console.warn("Quiz terminated:", data.reason);
        // Evaluation will still arrive next
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

  return socket ? (
    <QuizSession
      socket={socket}
      onStop={() => {
        socket?.close();
        setSocket(null);
      }}
    />
  ) : (
    <QuizSetup onStart={startQuiz} />
  );
}
