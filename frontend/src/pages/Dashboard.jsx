import "../styles/dashboard.css";
import { useNavigate } from "react-router-dom";

const features = [
  {
    title: "Career Finder",
    desc: "Discover careers that match your interests and skills."
  },
  {
    title: "AI Roadmap Generator",
    desc: "Personalized learning paths for your goals."
  },
  {
    title: "AI Tutor",
    desc: "Ask doubts and learn interactively."
  },
  {
    title: "Quiz Generator",
    desc: "Test yourself with smart quizzes."
  },
  {
    title: "Job Search",
    desc: "AI-powered job discovery."
  },
  {
    title: "CV Generation",
    desc: "AI-powered CV generator."
  },
  {
    title: "LinkedIn Assistant",
    desc: "Optimize your profile and posts."
  },
  {
    title: "Networking Events",
    desc: "Find relevant hackathons & events."
  },
  {
    title: "Emotional Support",
    desc: "Talk when you need motivation."
  },
  {
    title: "Music Recommendation",
    desc: "Mood-based playlists."
  },
  {
    title: "News Digest",
    desc: "Curated AI & tech updates."
  },
  {
    title: "Personal Analytics",
    desc: "Track your growth journey."
  }
];

export default function Dashboard() {
  const navigate = useNavigate();

  // later → get username from JWT / backend
  const username = "Shahan";

  return (
    <div className="dashboard-wrapper">
      <h1 className="dashboard-title">
        Welcome, {username} 👋
      </h1>

      <p className="dashboard-subtitle">
        Your AI-powered personal growth platform
      </p>

      <div className="feature-grid">
        {features.map((f, i) => (
          <div key={i} className="feature-card">
            <h3>{f.title}</h3>
            <p>{f.desc}</p>
          </div>
        ))}
      </div>

      <button
        className="orchestrator-btn"
        onClick={() => navigate("/orchestrator")}
      >
        Start Orchestrator →
      </button>
    </div>
  );
}
