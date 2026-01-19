import { useLocation, useNavigate } from "react-router-dom";
import { ArrowLeft, Trophy, CheckCircle2 } from "lucide-react";
import { Button } from "../../components/ui/button";
import "../../styles/quiz.css";
export default function QuizEvaluationPage() {
  const { state } = useLocation();
  const navigate = useNavigate();
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
        <div className="max-w-2xl mx-auto w-full">
          {state ? (
            <div className="setup-card !text-left !block relative overflow-hidden">
              <div className="mb-8">
                <span className="text-xs font-bold uppercase tracking-widest text-primary/60 mb-2 block">Performance Summary</span>
                <h1 className="setup-title !mb-0">Quiz Evaluation</h1>
              </div>
              <div className="flex items-center gap-6 mb-8 p-6 bg-secondary/20 rounded-2xl border border-white/5">
                <div className="flex-1">
                   <div className="text-4xl font-bold text-primary">{state.score}%</div>
                   <div className="text-sm text-muted-foreground uppercase tracking-tight">Overall Proficiency</div>
                </div>
                <div className="h-12 w-[1px] bg-border/50"></div>
                <div className="flex-1">
                   <div className="text-lg font-semibold">
                     {state.score >= 80 ? "Expert" : state.score >= 50 ? "Intermediate" : "Beginner"}
                   </div>
                   <div className="text-sm text-muted-foreground uppercase tracking-tight">Skill Level</div>
                </div>
              </div>
              <div className="feedback-section">
                 <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
                   Detailed Feedback
                 </h3>
                 <p className="text-muted-foreground leading-relaxed text-lg italic">
                   "{state.feedback}"
                 </p>
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


