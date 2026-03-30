import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { 
  ArrowLeft, 
  Play, 
  Pause, 
  SkipBack, 
  SkipForward, 
  Sparkles,
  Target ,
  Music4
} from "lucide-react";
import { Button } from "../components/ui/button";
import "../styles/music-therapy.css";
export default function MusicRecommendation() {
  const navigate = useNavigate();
  const canvasRef = useRef(null);
  const audioRef = useRef(null);
  const [text, setText] = useState("");
  const [song, setSong] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const MIN_CHARS = 50;
  const charCount = text.trim().length;
  const isValid = charCount >= MIN_CHARS;
  useEffect(() => {
    if (!isPlaying || !canvasRef.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    let animationId;
    const renderFrame = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight * 0.7;
      const cx = canvas.width / 2;
      const cy = canvas.height / 2;
      const bars = 100;
      const baseRadius = Math.min(cx, cy) * 0.35;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const time = Date.now() / 1000;
      const style = getComputedStyle(document.body);
      const isDark = document.documentElement.classList.contains("dark");
      const baseHue = isDark ? 260 : 220;
      const saturation = isDark ? "80%" : "70%";
      const lightness = isDark ? "60%" : "50%";
      for (let i = 0; i < bars; i++) {
        const angle = (i / bars) * Math.PI * 2;
        const squareFactor = 0.15; 
        const radiusMod = 1 + Math.cos(angle * 4) * squareFactor; 
        const currentRadius = baseRadius * radiusMod;
        const soundWave = Math.sin(angle * 10 + time * 5) * Math.cos(angle * 5 - time * 2);
        const barHeight = 20 + Math.abs(soundWave) * 120 * (Math.random() * 0.5 + 0.8);
        const x1 = cx + Math.cos(angle) * currentRadius;
        const y1 = cy + Math.sin(angle) * currentRadius;
        const x2 = cx + Math.cos(angle) * (currentRadius + barHeight);
        const y2 = cy + Math.sin(angle) * (currentRadius + barHeight);
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        const hue = (i / bars) * 60 + baseHue + time * 50; 
        ctx.strokeStyle = `hsla(${hue}, ${saturation}, ${lightness}, 0.8)`;
        ctx.lineWidth = 4;
        ctx.lineCap = "round";
        ctx.stroke();
      }
      animationId = requestAnimationFrame(renderFrame);
    };
    renderFrame();
    return () => cancelAnimationFrame(animationId);
  }, [isPlaying]);
  const submit = async () => {
    if (!isValid) return;
    setLoading(true);
    setSong(null);
    try {
      const res = await fetch("http://localhost:8000/music/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify({ user_text: text }),
      });
      const data = await res.json();
      if (data.song) {
        setSong(data.song);
        setIsPlaying(true);
      }
    } catch (e) {
      console.error("Music fetch error", e);
    } finally {
      setLoading(false);
    }
  };
  const togglePlay = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };
  return (
    <div className="music-layout">
      <div className="music-bg"></div>
      <canvas ref={canvasRef} className="equalizer-canvas"></canvas>
      
      <div className="music-content-wrapper">
        <aside className="music-feature-sidebar">
          <div className="music-feature-box">
            <div className="music-feature-header">
              <Music4 size={24} className="text-indigo-400" />
              <h3>Sonic Therapy</h3>
            </div>
            
            <div className="music-feature-content">
              <p className="music-feature-description">
                AI-curated soundscapes optimized for focus, relaxation, and cognitive performance.
              </p>
              
              <div className="music-feature-sections">
                <div className="music-feature-section">
                  <h4 className="feature-title">How It Works</h4>
                  <ul className="music-feature-steps">
                    <li>Detect your current mood</li>
                    <li>Generate AI playlists</li>
                    <li>Enhance your deep work</li>
                    <li>Achieve mental clarity</li>
                  </ul>
                </div>
              </div>
              
              <div className="music-feature-footer">
                <div className="music-feature-tip">
                  <Target size={16} className="text-blue-500" />
                  <span>Tip: Use headphones for full immersion!</span>
                </div>
              </div>
            </div>
          </div>
        </aside>

        <div className="music-main-engine">
          <button className="back-btn-abs" onClick={() => navigate("/dashboard")}>
            <ArrowLeft size={24} />
          </button>
          
          <div className="music-content">
            {!song ? (
              <div className="emotion-input-container">
                 <div className="flex justify-center mb-6">
                    <div className="w-20 h-20 rounded-full bg-indigo-500/20 flex items-center justify-center animate-pulse">
                       <Music4 size={40} className="text-indigo-400" />
                    </div>
                 </div>
                 <h1 className="music-title">Sonic Therapy</h1>
                 <p className="music-subtitle">Describe your current mood, and let our AI compose your soundscape.</p>
                 <div className="input-box">
                   <input 
                     placeholder="e.g. Feeling stressed about deadlines..." 
                     value={text}
                     onChange={(e) => setText(e.target.value)}
                     onKeyDown={(e) => {
                      if (e.key === "Enter" && isValid) submit();
                    }}
                   />
                     <button
                        className="play-btn"
                        onClick={submit}
                        disabled={loading || !isValid}
                      >
                        <Play size={20} fill="currentColor" />
                        {loading ? "Composing..." : "Play"}
                      </button>
                    </div>

                    <div className={`char-hint ${isValid ? "ok" : "warn"}`}>
                      {charCount}/{MIN_CHARS} characters
                      {!isValid && " — please describe your mood in more detail"}
                    </div>
              </div>
            ) : (
              <div className="player-container">
                <div className="song-info">
                   <h2 className="song-title">{song.title}</h2>
                   <div className="song-tags">
                     {song.song_emotions?.map((tag, i) => (
                       <span key={i} className="tag">{tag}</span>
                     ))}
                   </div>
                </div>
                <audio 
                  ref={audioRef} 
                  src={song.audio_url} 
                  autoPlay 
                  onPlay={() => setIsPlaying(true)}
                  onPause={() => setIsPlaying(false)}
                  onEnded={() => setIsPlaying(false)}
                />
                <div className="controls">
                   <button className="ctrl-btn"><SkipBack size={32} /></button>
                   <button className="ctrl-btn main" onClick={togglePlay}>
                     {isPlaying ? <Pause size={36} fill="currentColor" /> : <Play size={36} fill="currentColor" className="ml-1" />}
                   </button>
                   <button className="ctrl-btn"><SkipForward size={32} /></button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}


