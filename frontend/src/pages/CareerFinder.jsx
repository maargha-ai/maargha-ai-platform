import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { 
  ArrowLeft, 
  CheckCircle2, 
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
        setQuestion(null);
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
    <div className="career-layout">
      <div className="p-6">
         <Button variant="ghost" size="icon" onClick={() => navigate("/dashboard")} className="rounded-full">
            <ArrowLeft size={24} />
         </Button>
      </div>
      <div className="career-container">
        {!saved && (
          <div className="career-header">
            <h1 className="career-title">Career Discovery Engine</h1>
            <p className="career-subtitle">Let AI analyze your aptitudes and map out your perfect path.</p>
            {connected ? (
               <span className="status-badge flex items-center gap-2 w-fit mx-auto">
                 <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                 Neural Link Active
               </span>
            ) : (
               <span className="status-badge text-muted-foreground">Connecting to Neural Net...</span>
            )}
          </div>
        )}
        {}
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
        {}
        {careers && !saved && (
          <div className="results-section">
             <h2 className="text-2xl font-bold mb-6 text-center flex items-center justify-center gap-2">
               <Sparkles className="text-primary" /> Analysis Complete: Top Matches
             </h2>
             <div className="results-grid">
              {careers.map((career, idx) => (
                <div key={idx} className="result-card">
                  <h4>{career.title}</h4>
                  <p className="result-reason">{career.reason}</p>
                  <div className="skill-pills">
                    {career.skills.map((skill, i) => (
                      <span key={i} className="skill-pill">
                        {skill}
                      </span>
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
        {}
        {saved && (
          <div className="success-view">
            <h3 className="text-xl font-bold mb-2">Trajectory Locked</h3>
            <p className="text-muted-foreground mb-6">Your professional path has been optimized for:</p>
            <h2 className="text-4xl font-bold text-primary mb-8">{selectedCareer}</h2>
            <Button onClick={() => navigate("/dashboard")} className="rounded-full px-8">
              Return to Dashboard
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}


