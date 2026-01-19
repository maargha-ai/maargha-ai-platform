import "../styles/register.css";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { loginUser } from "../services/authService";
import { useAuth } from "../context/AuthContext";
export default function Login() {
  const navigate = useNavigate();
  const { login, isAuthenticated } = useAuth();
  const stars = Array.from({ length: 920 });
  useEffect(() => {
    if (isAuthenticated) {
      navigate("/dashboard");
    }
  }, [isAuthenticated, navigate]);
  const [form, setForm] = useState({
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const tokens = await loginUser(form);
      login(tokens);
      navigate("/dashboard"); 
    } catch (err) {
      setError(err.message);
    }
  };
  return (
    <div className="register-wrapper">
      {}
      <div className="stars-layer">
        {stars.map((_, i) => {
          const movement = Math.random() < 0.33 ? 4 : Math.random() < 0.66 ? 8 : 14;
          const style = {
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDuration: `${12 + Math.random() * 18}s`,
            animationDelay: `${Math.random() * -10}s`,
            opacity: Math.random(),
            "--drift": `${movement}px`,
          };
          return <span key={i} className="star" style={style} />;
        })}
      </div>
      <div className="register-card">
        <button
          className="home-float-btn"
          onClick={() => navigate("/")}
          aria-label="Go Home"
        >
          ⌂
        </button>
        <h2>Welcome Back</h2>
        <form onSubmit={handleSubmit}>
          <input
            name="email"
            type="email"
            placeholder="Email"
            onChange={handleChange}
            required
          />
          <input
            name="password"
            type="password"
            placeholder="Password"
            onChange={handleChange}
            required
          />
          <button type="submit">Login</button>
        </form>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <p className="login-link">
          Don’t have an account?{" "}
          <span onClick={() => navigate("/register")}>Register</span>
        </p>
      </div>
    </div>
  );
}


