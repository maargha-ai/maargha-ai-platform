import { useState } from "react";
import { BrainCircuit, ArrowRight, Target } from "lucide-react";
import "../../styles/quiz.css";

export default function QuizSetup({ onStart }) {
  const [topic, setTopic] = useState("");
  const [level, setLevel] = useState("easy");

  return (
    <div className="quiz-layout">
      <div className="quiz-bg"></div>
      
      <div className="quiz-content-wrapper">
        <aside className="quiz-feature-sidebar">
          <div className="quiz-feature-box">
            <div className="quiz-feature-header">
              <BrainCircuit size={24} className="text-purple-600" />
              <h3>Technical Assessment</h3>
            </div>
            
            <div className="quiz-feature-content">
              <p className="quiz-feature-description">
                AI-powered technical skill evaluation and knowledge testing platform.
              </p>
              
              <div className="quiz-feature-sections">
                <div className="quiz-feature-section">
                  <h4>How It Works</h4>
                  <ol className="quiz-feature-steps">
                    <li>Choose your technical topic</li>
                    <li>Select difficulty level</li>
                    <li>Answer skill-based questions</li>
                    <li>Get detailed evaluation</li>
                  </ol>
                </div>
              </div>
              
              <div className="quiz-feature-footer">
                <div className="quiz-feature-tip">
                  <Target size={16} className="text-blue-500" />
                  <span>Tip: Start with easier levels to build confidence!</span>
                </div>
              </div>
            </div>
          </div>
        </aside>

        <div className="quiz-setup-engine">
          <div className="setup-card">
            <h2 className="setup-title">Skill Matrix Initiation</h2>
            <p className="setup-subtitle">Configure your technical assessment parameters.</p>
            
            <div className="text-left">
              <label className="text-sm font-semibold ml-1 mb-2 block">
                Focus Topic
              </label>
              
              <input
                className="input-field"
                placeholder="e.g. React Patterns, Python AsyncIO..."
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
              />

              <label className="text-sm font-semibold ml-1 mb-2 block">
                Proficiency Level
              </label>
              
              <div className="level-selector">
                {["easy", "medium", "hard"].map((l) => (
                  <button
                    key={l}
                    type="button"
                    className={`level-btn ${level === l ? "active" : ""}`}
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
    </div>
  );
}
