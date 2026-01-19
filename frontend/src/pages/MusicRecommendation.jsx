import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { 
  ArrowLeft, 
  Play, 
  Pause, 
  SkipBack, 
  SkipForward, 
  Sparkles,
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

  // Visualization Logic
  useEffect(() => {
    if (!isPlaying || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    let animationId;

    const renderFrame = () => {
      // Simulate frequency data
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight * 0.7;
      
      const cx = canvas.width / 2;
      const cy = canvas.height / 2;
      
      const bars = 100;
      const baseRadius = Math.min(cx, cy) * 0.35; // Size of the ring
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      const time = Date.now() / 1000;

      // Get theme colors from computed styles for adaptive visualizer
      const style = getComputedStyle(document.body);
      const isDark = document.documentElement.classList.contains("dark");
      
      // Dynamic colors based on theme
      const baseHue = isDark ? 260 : 220; // Purple/Blue for dark, Blue for light
      const saturation = isDark ? "80%" : "70%";
      const lightness = isDark ? "60%" : "50%";

      for (let i = 0; i < bars; i++) {
        // Calculate angle
        const angle = (i / bars) * Math.PI * 2;
        
        // SQUIRCLE / ROUNDED SQUARE LOGIC
        const squareFactor = 0.15; 
        const radiusMod = 1 + Math.cos(angle * 4) * squareFactor; 
        const currentRadius = baseRadius * radiusMod;
        
        // Sound wave simulation
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
    if (!text) return;
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
        setIsPlaying(true); // Auto-play on load
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
      {/* Dynamic Background */}
      <div className="music-bg"></div>
      
      {/* Visualizer Canvas */}
      <canvas ref={canvasRef} className="equalizer-canvas"></canvas>

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
                 onKeyDown={(e) => e.key === 'Enter' && submit()}
               />
               <button className="play-btn" onClick={submit} disabled={loading || !text}>
                 {loading ? <Sparkles size={20} className="animate-spin" /> : <Play size={20} fill="currentColor" />}
                 {loading ? "Composing..." : "Play"}
               </button>
             </div>
          </div>
        ) : (
          <div className="player-container">
            {/* Minimal Player - No Cards */}
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
  );
}
