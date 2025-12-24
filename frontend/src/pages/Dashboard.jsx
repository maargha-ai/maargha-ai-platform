import "../styles/dashboard.css";
import "../styles/register.css"; 
import { useNavigate } from "react-router-dom";

const features = [
  { title: "Career Finder", desc: "Discover careers that match your interests and skills." },
  { title: "AI Roadmap Generator", desc: "Personalized learning paths for your goals." },
  { title: "AI Tutor", desc: "Ask doubts and learn interactively." },
  { title: "Quiz Generator", desc: "Test yourself with smart quizzes." },
  { title: "Quiz Evaluation", desc: "Evaluate your answers." },
  { title: "Job Search", desc: "AI-powered job discovery." },
  { title: "CV Generation", desc: "AI-powered CV generator." },
  { title: "LinkedIn Assistant", desc: "Optimize your profile and posts." },
  { title: "Networking Events", desc: "Find relevant hackathons & events." },
  { title: "Emotional Support", desc: "Talk when you need motivation." },
  { title: "Music Recommendation", desc: "Mood-based playlists." },
  { title: "News Digest", desc: "Curated AI & tech updates." },
  // { title: "Personal Analytics", desc: "Track your growth journey." },
];

export default function Dashboard() {
  const navigate = useNavigate();
  const username = "User"; // later from backend/JWT
  const stars = Array.from({ length: 900 });

  return (
    <div className="register-wrapper dashboard-wrapper">
      {/* ⭐ STAR BACKGROUND */}
      <div className="stars-layer">
        {stars.map((_, i) => {
          const movement = Math.random() < 0.33 ? 4 : Math.random() < 0.66 ? 8 : 14;

          const style = {
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDuration: `${14 + Math.random() * 18}s`,
            animationDelay: `${Math.random() * -10}s`,
            opacity: Math.random(),
            "--drift": `${movement}px`,
          };

          return <span key={i} className="star" style={style} />;
        })}
      </div>

      {/* 🌌 CONTENT */}
      <div className="dashboard-content">
        <h1 className="dashboard-title float-text">
          Welcome, {username}
        </h1>

        <div className="feature-grid">
          {features.map((f, i) => (
            <div key={i} className="feature-card">
              <h3>{f.title}</h3>
              <p>{f.desc}</p>
            </div>
          ))}
        </div>

          <button
            className="orchestrator-btn floating-btn"
            onClick={() => navigate("/orchestrator")}
          >
            Start Orchestrator →
          </button>
      </div>
    </div>
  );
}
