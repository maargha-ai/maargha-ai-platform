import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function CareerFinder() {
  const navigate = useNavigate();
  const wsRef = useRef(null);

  const [question, setQuestion] = useState(null);
  const [questionId, setQuestionId] = useState(null);
  const [careers, setCareers] = useState(null);
  const [connected, setConnected] = useState(false);
  const [selectedCareer, setSelectedCareer] = useState(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      navigate("/login");
      return;
    }

    const ws = new WebSocket(
      `ws://localhost:8000/ws/career?token=${token}`
    );

    wsRef.current = ws;

    ws.onopen = () => {
      setConnected(true);
      ws.send(JSON.stringify({ type: "start_career" }));
    };

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);

      if (msg.type === "career_question") {
        setQuestion(msg.question);
        setQuestionId(msg.question_id);
      }

      if (msg.type === "career_result") {
        setCareers(msg.careers);
        setQuestion(null); // stop showing questions
      }

      if (msg.type === "career_saved") {
        setSaved(true);
        setSelectedCareer(msg.career);
        ws.close();
      }
    };

    ws.onerror = (err) => {
      console.error("WebSocket error", err);
    };

    ws.onclose = () => {
      setConnected(false);
    };

    return () => {
      ws.close();
    };
  }, [navigate]);

  const sendAnswer = (answer) => {
    wsRef.current?.send(
      JSON.stringify({
        type: "career_answer",
        answer,
      })
    );
  };

  const selectCareer = (careerTitle) => {
    wsRef.current?.send(
      JSON.stringify({
        type: "select_career",
        career: careerTitle,
      })
    );
  };

  return (
    <div className="career-page">
      <h2>Career Finder</h2>

      {!connected && <p>Connecting...</p>}

      {/* QUESTION VIEW */}
      {question && !careers && (
        <div className="career-question-card">
          <p className="question-text">{question}</p>

          <div className="answer-buttons">
            <button onClick={() => sendAnswer("yes")}>Yes</button>
            <button onClick={() => sendAnswer("no")}>No</button>
          </div>

          <p className="question-progress">
            Question {questionId + 1}
          </p>
        </div>
      )}

      {/* RESULT VIEW */}
      {careers && !saved && (
        <div className="career-result">
          <h3>Recommended Careers</h3>
          <p>Select the career that fits you best:</p>

          {careers.map((career, idx) => (
            <div key={idx} className="career-card">
              <h4>{career.title}</h4>
              <p>{career.reason}</p>

              <div className="skill-tags">
                {career.skills.map((skill, i) => (
                  <span key={i} className="skill-tag">
                    {skill}
                  </span>
                ))}
              </div>

              {/* ✅ EXPLICIT BUTTON */}
              <button
                className="select-btn"
                onClick={() => selectCareer(career.title)}
              >
                Select this career
              </button>
            </div>
          ))}
        </div>
      )}

      {/* CONFIRMATION VIEW */}
      {saved && (
        <div className="career-confirmation">
          <h3>Career Selected 🎉</h3>
          <p>You have chosen:</p>
          <h2>{selectedCareer}</h2>

          <button onClick={() => navigate("/dashboard")}>
            Back to Dashboard
          </button>
        </div>
      )}
    </div>
  );
}
