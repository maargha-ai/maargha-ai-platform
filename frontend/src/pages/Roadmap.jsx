import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Map,
  Loader2,
  Sparkles,
  Route,
  Target
} from "lucide-react";

import { useTheme } from "../components/ThemeProvider";
import { ThemeToggle } from "../components/ThemeToggle";
import { Button } from "../components/ui/button";
import RoadmapVisualizer from "../components/RoadmapVisualizer";

import "../styles/roadmap-gen.css";

export default function Roadmap() {
  const navigate = useNavigate();
  const { theme, setTheme } = useTheme();

  const [career, setCareer] = useState("");
  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    if (!career.trim()) return;

    setLoading(true);
    setRoadmap(null);

    try {
      const res = await fetch("http://localhost:8000/roadmap/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify({ career }),
      });

      const data = await res.json();
      setRoadmap(data);
    } catch (error) {
      console.error("Roadmap generation failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`roadmap-layout ${theme}`}>
      <div className="roadmap-bg" />

      {/* Back button */}
      <div className="back-btn">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => navigate("/dashboard")}
          className="rounded-full"
        >
          <ArrowLeft size={24} />
        </Button>
      </div>

      {/* Theme toggle */}
      <div className="absolute top-8 right-8 z-20">
        <ThemeToggle theme={theme} setTheme={setTheme} />
      </div>

      <div className="roadmap-content-wrapper">
        <div className="roadmap-container">
          {/* Feature Box - Hide when roadmap is generated */}
          {!roadmap && (
            <aside className="roadmap-feature-sidebar">
              <div className="roadmap-feature-box">
                <div className="roadmap-feature-header">
                  <Route size={24} className="text-green-500" />
                  <h3>Career Path Intelligence</h3>
                </div>
                
                <div className="roadmap-feature-content">
                  <p className="roadmap-feature-description">
                    AI-powered personalized learning paths to achieve your career goals efficiently.
                  </p>
                  
                  <div className="roadmap-feature-sections">
                    <div className="roadmap-feature-section">
                      <h4 className="feature-title">How It Works</h4>

                      <div className="roadmap-steps">
                        <div className="step">
                          <span className="step-number">1</span>
                          <p>Enter your dream career role</p>
                        </div>

                        <div className="step">
                          <span className="step-number">2</span>
                          <p>AI analyzes required skills</p>
                        </div>

                        <div className="step">
                          <span className="step-number">3</span>
                          <p>Generate visual roadmap</p>
                        </div>

                        <div className="step">
                          <span className="step-number">4</span>
                          <p>Follow step-by-step path</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="roadmap-feature-footer">
                    <div className="roadmap-feature-tip">
                      <Target size={16} className="text-blue-500" />
                      <span>Tip: Be specific about your career goals for better roadmaps!</span>
                    </div>
                  </div>
                </div>
              </div>
            </aside>
          )}

          {/* Main Content */}
          <div className={`roadmap-main-engine ${roadmap ? 'roadmap-generated' : ''}`}>
            <h1 className="roadmap-title">Career Architect</h1>
            <p className="roadmap-subtitle">
              {roadmap ? "Generation for this role is complete! Your personalized career path is ready to explore." : "Enter your dream role and watch as we generate a personalized visual roadmap just for you."}
            </p>

            {/* Input row – keep compact */}
            {!roadmap && (
              <div className="roadmap-input-wrapper">
                <Map className="text-muted-foreground mr-4" size={24} />

                <input
                  placeholder="What do you want to become?"
                  value={career}
                  onChange={(e) => setCareer(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && generate()}
                />

                <button
                  className="generate-btn"
                  onClick={generate}
                  disabled={loading || !career}
                >
                  {loading ? (
                    <>
                      <Loader2 size={16} className="animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Sparkles size={16} />
                      Generate
                    </>
                  )}
                </button>
              </div>
            )}

            {/* Roadmap visualization */}
            {roadmap && <RoadmapVisualizer roadmap={roadmap} />}
          </div>
        </div>
      </div>
    </div>
  );
}