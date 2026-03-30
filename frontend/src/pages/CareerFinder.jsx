import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  BrainCircuit,
  Sparkles,
  Target
} from "lucide-react";
import { Button } from "../components/ui/button";
import "../styles/career-finder.css";

export default function CareerFinder() {
  const navigate = useNavigate();
  const wsRef = useRef(null);

  const [question, setQuestion] = useState(null);
  const [questionId, setQuestionId] = useState(null);
  const [careers, setCareers] = useState(null);
  const [connected, setConnected] = useState(false);
  const [selectedCareer, setSelectedCareer] = useState(null);
  const [saved, setSaved] = useState(false);

  /* ===============================
     Connect WebSocket
  =============================== */
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      navigate("/login");
      return;
    }

    const ws = new WebSocket(`ws://localhost:8000/ws/career?token=${token}`);
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
        setQuestion(null);
      }

      // 🔥 DO NOT CLOSE SOCKET HERE
      if (msg.type === "career_saved") {
        setSaved(true);
        setSelectedCareer(msg.career);
      }
    };

    ws.onerror = (err) => {
      console.error("WebSocket error", err);
    };

    ws.onclose = () => {
      setConnected(false);
      wsRef.current = null;
    };

    // 🔥 graceful leave instead of hard close
    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "leave_career" }));
      }
    };
  }, [navigate]);

  /* ===============================
     Send Answer (Safe Send)
  =============================== */
  const sendAnswer = (answer) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(
        JSON.stringify({
          type: "career_answer",
          answer,
        })
      );
    }
  };

  /* ===============================
     Select Career (Safe Send)
  =============================== */
  const selectCareer = (careerTitle) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(
        JSON.stringify({
          type: "select_career",
          career: careerTitle,
        })
      );
    }
  };

  /* ===============================
     UI
  =============================== */
  return (
    <div className="career-layout">
      <main className="career-main">
        {/* Top Header with Back Button */}
        <div className="career-top-header">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => navigate("/dashboard")}
            className="rounded-full"
          >
            <ArrowLeft size={24} />
          </Button>
        </div>

        <div className="career-content-wrapper">
          {/* Sidebar */}
          <aside className="career-feature-sidebar">
            <div className="career-feature-box">
              <div className="career-feature-header">
                <BrainCircuit size={24} className="text-purple-600" />
                <h3>Career Discovery</h3>
              </div>

              <div className="career-feature-content">
                <p className="career-feature-description">
                  AI-powered career analysis to find your perfect professional path.
                </p>
                
                <div className="career-feature-sections">
                  <div className="career-feature-section">
                    <h4>How It Works</h4>
                    <ol className="career-feature-steps">
                      <li>Answer assessment questions</li>
                      <li>AI analyzes responses</li>
                      <li>Get career matches</li>
                      <li>Choose your path</li>
                    </ol>
                  </div>
                </div>
                
                <div className="career-feature-footer">
                  <div className="career-feature-tip">
                    <Target size={16} className="text-blue-500" />
                    <span>Tip: Answer honestly for best results!</span>
                  </div>
                </div>
              </div>
            </div>
          </aside>

          {/* Career Discovery Engine - Right Side */}
          <div className="career-discovery-engine">
            {!saved && (
              <div className="career-header">
                <h1 className="career-title">Career Discovery Engine</h1>
                <p className="career-subtitle">
                  Let AI analyze your aptitudes and map out your perfect path.
                </p>
              </div>
            )}

            {/* Question */}
            {question && !careers && (
              <div className="question-card">
                <p className="question-text">{question}</p>

                <div className="answer-options">
                  <button className="answer-btn yes" onClick={() => sendAnswer("yes")}>
                    Absolutely
                  </button>

                  <button className="answer-btn no" onClick={() => sendAnswer("no")}>
                    Not really
                  </button>
                </div>

                <p className="progress-indicator">
                  Analysis Step {questionId + 1}
                </p>
              </div>
            )}

            {/* Results */}
            {careers && !saved && (
              <div className="results-section">
                <h2 className="text-2xl font-bold mb-6 text-center">
                  <Sparkles /> Analysis Complete: Top Matches
                </h2>

                <div className="results-grid">
                  {careers.map((career, idx) => (
                    <div key={idx} className="result-card">
                      <h4>{career.title}</h4>
                      <p className="result-reason">{career.reason}</p>

                      <div className="skill-pills">
                        {career.skills.map((skill, i) => (
                          <span key={i} className="skill-pill">{skill}</span>
                        ))}
                      </div>

                      <button
                        className="select-career-btn"
                        onClick={() => selectCareer(career.title)}
                      >
                        Select Path
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Saved */}
            {saved && (
              <div className="success-view">
                <h3 className="text-xl font-bold mb-2">Trajectory Locked</h3>
                <p className="text-muted-foreground mb-6">Your professional path has been optimized for:</p>
                <h2 className="text-4xl font-bold text-primary mb-8">{selectedCareer}</h2>
                <Button onClick={() => navigate("/dashboard")}>
                  Return to Dashboard
                </Button>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
