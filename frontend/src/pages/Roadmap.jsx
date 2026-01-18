import { useState } from "react";
import "../styles/roadmap-dashboard.css";

export default function Roadmap() {
  const [career, setCareer] = useState("");
  const [videoUrl, setVideoUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    if (!career.trim()) return;
    
    setLoading(true);
    setVideoUrl(null);

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
    setLoading(false);
  };

  return (
    <div className="roadmap-page">
      <h2>Career Roadmap Generator</h2>

      <input
        placeholder="Enter career (e.g. Data Scientist)"
        value={career}
        onChange={(e) => setCareer(e.target.value)}
      />

      <button onClick={generate} disabled={loading}>
        {loading ? "Generating roadmap..." : "Generate Roadmap"}
      </button>

      {videoUrl && (
        <div className="roadmap-video-container">
          <video
            src={videoUrl}
            controls
            autoPlay
            style={{ width: "100%", display: "block" }}
          />
        </div>
      )}
    </div>
  );
}
