import "../styles/dashboard.css";
import "../styles/register.css"; 
import { useNavigate } from "react-router-dom";

const features = [
  { title: "Career Finder", desc: "Discover careers that match your interests and skills.", route: "/career" },
  { title: "AI Roadmap Generator", desc: "Personalized learning paths for your goals.", route: "/roadmap" },
  { title: "AI Tutor", desc: "Ask doubts and learn interactively.", route: "/tutor" },
  { title: "Quiz Generator", desc: "Test yourself with smart quizzes.", route: "/quiz" },
  // { title: "Quiz Evaluation", desc: "Evaluate your answers.", route: "/quiz/evaluation" },
  { title: "Job Search", desc: "AI-powered job discovery.", route: "/jobs" },
  { title: "CV Generation", desc: "AI-powered CV generator.", route: "/cv" },
  { title: "LinkedIn Assistant", desc: "Optimize your profile and posts.", route: "/linkedin" },
  { title: "Networking Events", desc: "Find relevant hackathons & events.", route: "/networking-events" },
  { title: "Emotional Support", desc: "Talk when you need motivation.", route: "/emotional-support" },
  { title: "Music Recommendation", desc: "Mood-based playlists.", route: "/music" },
  { title: "News Digest", desc: "Curated AI & tech updates.", route: "/news" },
];

export default function Dashboard() {
  const navigate = useNavigate();
  const username = "User"; 
  const stars = Array.from({ length: 900 });

  // LOGOUT HANDLER
  const handleLogout = async () => {
    const access = localStorage.getItem("access_token");
    const refresh = localStorage.getItem("refresh_token");

    try {
      await fetch("http://localhost:8000/auth/logout", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${access}`,
        },
        body: JSON.stringify({ refresh }),
      });
    } catch (err) {
      console.error("Logout failed", err);
    } finally {
      // Always clear tokens
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      navigate("/login");
    }
  };

  return (
    <div className="register-wrapper dashboard-wrapper">
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

      <div className="dashboard-content">
        <h1 className="dashboard-title float-text">
          Welcome, {username}
        </h1>

        {/* LOGOUT BUTTON */}
        <button
          className="logout-btn"
          onClick={handleLogout}
        >
          Logout
        </button>

        <div className="feature-grid">
          {features.map((f, i) => {
            const isClickable = Boolean(f.route);

            return (
              <div
                key={i}
                className={`feature-card ${isClickable ? "clickable" : ""}`}
                onClick={() => isClickable && navigate(f.route)}
                role={isClickable ? "button" : "presentation"}
                tabIndex={isClickable ? 0 : -1}
                onKeyDown={(e) => {
                  if (isClickable && (e.key === "Enter" || e.key === " ")) {
                    navigate(f.route);
                  }
                }}
              >
                <h3>{f.title}</h3>
                <p>{f.desc}</p>
              </div>
            );
          })}
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