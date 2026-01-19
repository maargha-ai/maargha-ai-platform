import { useState } from "react";
import { 
  BrainCircuit, 
  Play, 
  ArrowRight,
  Wifi
} from "lucide-react";
import "../../styles/quiz.css";

export default function QuizSetup({ onStart }) {
  const [topic, setTopic] = useState("");
  const [level, setLevel] = useState("easy");

  return (
    <div className="quiz-layout">
       <div className="quiz-bg"></div>
       <div className="quiz-container">
          <div className="setup-card">
            <div className="flex justify-center mb-6">
               <div className="p-4 rounded-2xl bg-primary/10 text-primary">
                 <BrainCircuit size={48} />
               </div>
            </div>
            
            <h2 className="setup-title">Skill Matrix Initiation</h2>
            <p className="setup-subtitle">Configure your technical assessment parameters.</p>

            <div className="text-left">
              <label className="text-sm font-semibold ml-1 mb-2 block">Focus Topic</label>
              <input
                className="input-field"
                placeholder="e.g. React Patterns, Python AsyncIO..."
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
              />

              <label className="text-sm font-semibold ml-1 mb-2 block">Proficiency Level</label>
              <div className="level-selector">
                {['easy', 'medium', 'hard'].map((l) => (
                  <button
                    key={l}
                    className={`level-btn ${level === l ? 'active' : ''}`}
                    onClick={() => setLevel(l)}
                  >
                    {l.charAt(0).toUpperCase() + l.slice(1)}
                  </button>
                ))}
              </div>

              <button 
                className="start-btn"
                onClick={() => onStart(topic, level)}
                disabled={!topic}
              >
                Start Assessment <ArrowRight size={18} />
              </button>
            </div>
          </div>
       </div>
    </div>
  );
}
