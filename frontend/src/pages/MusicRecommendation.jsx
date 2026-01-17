import { useState } from "react";

export default function MusicRecommendation() {
  const [text, setText] = useState("");
  const [song, setSong] = useState(null);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    setLoading(true);
    setSong(null);

    const res = await fetch("http://localhost:8000/music/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
      body: JSON.stringify({ user_text: text }),
    });

    const data = await res.json();
    setSong(data.song || null);
    setLoading(false);
  };

  return (
    <div className="music-page">
      <h2>Music Recommendation</h2>

      <textarea
        placeholder="How are you feeling today?"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={submit} disabled={loading}>
        {loading ? "Finding music..." : "Recommend"}
      </button>

      {song && (
        <div className="song-card">
          <h3>{song.title}</h3>

          {song.song_emotions && (
            <div className="emotion-tags">
              {song.song_emotions.map((emotion, idx) => (
                <span key={idx} className="emotion-tag">
                  {emotion}
                </span>
              ))}
            </div>
          )}

          <audio src={song.audio_url} controls autoPlay />
        </div>
      )}
    </div>
  );
}
