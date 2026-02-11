import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Map,
  Loader2,
  Sparkles
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

      {/* Main content */}
      <div className="roadmap-content" style={{ maxWidth: 'unset', width: '75%' }}>
        <h1 className="roadmap-title">Career Architect</h1>
        <p className="roadmap-subtitle">
          Enter your dream role and watch as we generate a personalized visual roadmap just for you.
        </p>

        {/* Input row – keep compact */}
        <div className="roadmap-input-wrapper" style={{ maxWidth: '600px', margin: '0 auto' }}>  {/* ← fix button/input stretch */}
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

        {/* Roadmap visualization */}
        {roadmap && <RoadmapVisualizer roadmap={roadmap} />}
      </div>
    </div>
  );
}