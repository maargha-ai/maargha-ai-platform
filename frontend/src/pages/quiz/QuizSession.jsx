import { useEffect, useRef, useState } from "react";
import { 
  Clock, 
  Video, 
  Mic, 
  StopCircle, 
  Send
} from "lucide-react";
import "../../styles/quiz.css";

export default function QuizSession({ socket, question, onStop }) {
  const [answer, setAnswer] = useState("");
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  // 🎥 Start camera
  useEffect(() => {
    let active = true;

    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        if (!active) return;
        streamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch((err) => {
        console.error("Camera access denied:", err);
      });

    return () => {
      active = false;
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((t) => t.stop());
      }
    };
  }, []);

  const submitAnswer = () => {
    if (!answer.trim()) return;

    socket.send(
      JSON.stringify({
        type: "quiz_answer",
        answer,
      })
    );
    setAnswer("");
  };

  const stopQuiz = () => {
    socket.send(JSON.stringify({ type: "stop_quiz" }));
    if (onStop) onStop();
  };

  return (
    <div className="quiz-layout">
       <div className="quiz-bg"></div>
       <div className="quiz-container">
         <div className="session-layout">
           {/* Left: Question & Answer */}
           <div className="question-panel">
             <div className="question-header">
               <span className="q-badge">Active Assessment</span>
               <div className="flex items-center gap-2 text-primary font-mono">
                  <Clock size={16} />
                  <span>00:45</span>
               </div>
             </div>

             <h3 className="live-question">{question}</h3>

             <div className="answer-area">
               <textarea
                 placeholder="Type your technical response here..."
                 value={answer}
                 onChange={(e) => setAnswer(e.target.value)}
                 autoFocus
               />
             </div>

             <div className="session-actions">
               <button onClick={stopQuiz} className="stop-btn flex items-center gap-2">
                 <StopCircle size={18} /> Terminate
               </button>
               <button onClick={submitAnswer} disabled={!answer.trim()} className="next-btn flex items-center gap-2">
                 Submit Response <Send size={18} />
               </button>
             </div>
           </div>

           {/* Right: Monitoring Panel */}
           <div className="side-panel">
             <div className="camera-card">
               <video
                 ref={videoRef}
                 autoPlay
                 muted
                 playsInline
                 className="camera-preview"
               />
               <div className="camera-overlay">
                 <div className="rec-dot"></div>
                 LIVE PROCTORING
               </div>
             </div>
             
             <div className="bg-card/50 backdrop-blur p-4 rounded-xl border border-border/50">
                <div className="flex items-center gap-3 mb-2">
                   <div className="p-2 bg-green-500/10 text-green-500 rounded-lg">
                      <Mic size={20} />
                   </div>
                   <div>
                      <div className="text-sm font-bold">Audio Input</div>
                      <div className="text-xs text-muted-foreground">Monitoring active</div>
                   </div>
                </div>
                <div className="h-1 w-full bg-secondary rounded-full overflow-hidden">
                   <div className="h-full bg-green-500 w-[60%] animate-pulse"></div>
                </div>
             </div>
           </div>
         </div>
       </div>
    </div>
  );
}
