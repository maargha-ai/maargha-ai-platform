import "../styles/register.css";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();
  const stars = Array.from({ length: 920 });

  return (
    <div className="register-wrapper">
      {/* STAR BACKGROUND */}
      <div className="stars-layer">
        {stars.map((_, i) => {
          const movement = Math.random() < 0.33 ? 4 : Math.random() < 0.66 ? 8 : 14;

          const style = {
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDuration: `${12 + Math.random() * 18}s`,
            animationDelay: `${Math.random() * -10}s`, // 👈 KEY LINE
            opacity: Math.random(),
            "--drift": `${movement}px`,
          };


          return <span key={i} className="star" style={style} />;
        })}
      </div>

      {/* LOGIN CARD */}
      <div className="register-card">
        <button
          className="home-float-btn"
          onClick={() => navigate("/")}
          aria-label="Go Home"
        >
          ⌂
        </button>
        <h2>Welcome Back</h2>

        <form>
          <input type="email" placeholder="Email" />
          <input type="password" placeholder="Password" />

          <button type="submit">Login</button>
        </form>

        <p className="login-link">
          Don’t have an account?{" "}
          <span onClick={() => navigate("/register")}>Register</span>
        </p>
      </div>
    </div>
  );
}
