import "../styles/register.css";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { registerUser } from "../services/authService";
import { useAuth } from "../context/AuthContext";
export default function Register() {
  const stars = Array.from({ length: 920 });
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  useEffect(() => {
    if (isAuthenticated) {
      navigate("/dashboard");
    }
  }, [isAuthenticated, navigate]);
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    password: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await registerUser(form);
      navigate("/login"); 
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="register-wrapper">
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
        <h2>Create Account</h2>
        <form onSubmit={handleSubmit}>
          <input
            name="full_name"
            placeholder="Full Name"
            onChange={handleChange}
            required
          />
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
          <button type="submit" disabled={loading}>
            {loading ? "Creating..." : "Register"}
          </button>
        </form>
         {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
        <p className="login-link">
        Already have an account? <span onClick={() => navigate("/login")}>Login</span>
        </p>
      </div>
    </div>
  );
}


