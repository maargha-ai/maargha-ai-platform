import { useLocation, useNavigate } from "react-router-dom";

export default function QuizEvaluationPage() {
  const { state } = useLocation();
  const navigate = useNavigate();

  return (
    <div className="quiz-evaluation-page">
      <h1>Quiz Evaluation</h1>

      {state ? (
        <pre style={{ whiteSpace: "pre-wrap" }}>
          {state}
        </pre>
      ) : (
        <p>No evaluation data available yet.</p>
      )}

      <button onClick={() => navigate("/dashboard")}>
        ← Back to Dashboard
      </button>
    </div>
  );
}
