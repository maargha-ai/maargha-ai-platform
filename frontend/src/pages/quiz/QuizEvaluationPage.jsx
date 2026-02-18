import { useLocation, useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import { Button } from "../../components/ui/button";
import "../../styles/quiz.css";
export default function QuizEvaluationPage() {
  const { state } = useLocation();
  const navigate = useNavigate();

  const score = state?.score ?? 0;
  const level =
    state?.level ??
    (score >= 85 ? "Expert" : score >= 65 ? "Intermediate" : "Beginner");
  const summary = state?.summary || state?.feedback || "No feedback available.";
  const strengths = Array.isArray(state?.strengths) ? state.strengths : [];
  const weaknesses = Array.isArray(state?.weaknesses) ? state.weaknesses : [];
  const suggestions = Array.isArray(state?.suggestions) ? state.suggestions : [];

  return (
    <div className="quiz-layout">
      <div className="quiz-bg"></div>
      <div className="quiz-container">
        <header className="mb-10 flex items-center justify-between">
           <Button variant="ghost" className="gap-2" onClick={() => navigate("/dashboard")}>
              <ArrowLeft size={18} /> Back to Dashboard
           </Button>
           <div className="flex items-center gap-2 text-primary font-bold">
              Assessment Complete
           </div>
        </header>
        <div className="max-w-4xl mx-auto w-full">
          {state ? (
            <div className="setup-card !max-w-4xl !text-left !block relative overflow-hidden">
              <div className="mb-8">
                <span className="text-xs font-bold uppercase tracking-widest text-primary/60 mb-2 block">Performance Summary</span>
                <h1 className="setup-title !mb-0">Quiz Evaluation</h1>
              </div>
              <div className="flex items-center gap-6 mb-8 p-6 bg-secondary/20 rounded-2xl border border-white/5">
                <div className="flex-1">
                   <div className="text-4xl font-bold text-primary">{score}%</div>
                   <div className="text-sm text-muted-foreground uppercase tracking-tight">Overall Proficiency</div>
                </div>
                <div className="h-12 w-[1px] bg-border/50"></div>
                <div className="flex-1">
                   <div className="text-lg font-semibold">
                     {level}
                   </div>
                   <div className="text-sm text-muted-foreground uppercase tracking-tight">Skill Level</div>
                </div>
              </div>
              <div className="feedback-section eval-content">
                <div className="eval-block">
                  <h3 className="eval-title">Summary</h3>
                  <p className="eval-text">{summary}</p>
                </div>

                <div className="eval-block">
                  <h3 className="eval-title">Strengths</h3>
                  {strengths.length ? (
                    <ul className="eval-list">
                      {strengths.map((item, idx) => (
                        <li key={`s-${idx}`} className="eval-text">{item}</li>
                      ))}
                    </ul>
                  ) : (
                    <p className="eval-muted">No strong areas detected in the provided answers.</p>
                  )}
                </div>

                <div className="eval-block">
                  <h3 className="eval-title">Weaknesses</h3>
                  {weaknesses.length ? (
                    <ul className="eval-list">
                      {weaknesses.map((item, idx) => (
                        <li key={`w-${idx}`} className="eval-text">{item}</li>
                      ))}
                    </ul>
                  ) : (
                    <p className="eval-muted">No specific weaknesses listed.</p>
                  )}
                </div>

                <div className="eval-block">
                  <h3 className="eval-title">Actionable Suggestions</h3>
                  {suggestions.length ? (
                    <ul className="eval-list">
                      {suggestions.map((item, idx) => (
                        <li key={`a-${idx}`} className="eval-text">{item}</li>
                      ))}
                    </ul>
                  ) : (
                    <p className="eval-muted">Keep practicing with concise and concept-driven answers.</p>
                  )}
                </div>
              </div>
              <div className="mt-10 pt-8 border-t border-border/50">
                 <Button className="w-full h-12 rounded-xl text-lg font-bold" onClick={() => navigate("/quiz")}>
                   Try Another Topic
                 </Button>
              </div>
            </div>
          ) : (
            <div className="setup-card">
              <p className="text-muted-foreground py-10">No evaluation data available yet.</p>
              <Button onClick={() => navigate("/dashboard")}>Return to Dashboard</Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}


