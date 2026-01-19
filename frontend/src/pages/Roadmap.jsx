import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { 
  ArrowLeft, 
  Map, 
  Play, 
  Loader2,
  Sparkles
} from "lucide-react";
import { useTheme } from "../components/ThemeProvider";
import { ThemeToggle } from "../components/ThemeToggle";
import { Button } from "../components/ui/button";
import "../styles/roadmap-gen.css";

export default function Roadmap() {
  const navigate = useNavigate();
  const { theme, setTheme } = useTheme();
  
  const [career, setCareer] = useState("");
  const [videoUrl, setVideoUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    if (!career.trim()) return;
    
    setLoading(true);
    setVideoUrl(null);

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
      setVideoUrl(data.video_url);
    } catch (error) {
       console.error("Roadmap generation failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`roadmap-layout ${theme}`}>
      <div className="roadmap-bg"></div>
      
      <div className="back-btn">
         <Button variant="ghost" size="icon" onClick={() => navigate("/dashboard")} className="rounded-full">
            <ArrowLeft size={24} />
         </Button>
      </div>

      <div className="absolute top-8 right-8 z-20">
         <ThemeToggle theme={theme} setTheme={setTheme} />
      </div>

      <div className="roadmap-content">
        <h1 className="roadmap-title">Career Architect</h1>
        <p className="roadmap-subtitle">
           Enter your dream role and watch as we generate a personalized visual roadmap just for you.
        </p>

        <div className="roadmap-input-wrapper">
           <Map className="text-muted-foreground mr-4" size={24} />
           <input
             placeholder="What do you want to become? (e.g. AI Engineer)"
             value={career}
             onChange={(e) => setCareer(e.target.value)}
             onKeyDown={(e) => e.key === 'Enter' && generate()}
           />
           <button 
             className="generate-btn" 
             onClick={generate} 
             disabled={loading || !career}
           >
             {loading ? (
                <>
                  <Loader2 size={20} className="animate-spin" />
                  Generating...
                </>
             ) : (
                <>
                  <Sparkles size={20} />
                  Generate
                </>
             )}
           </button>
        </div>

        {videoUrl && (
          <div className="video-card">
            <video
              src={videoUrl}
              controls
              autoPlay
              style={{ width: "100%", display: "block" }}
            />
          </div>
        )}
      </div>
    </div>
  );
}
