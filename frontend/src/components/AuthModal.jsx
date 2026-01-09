import { useState, useEffect } from "react";
import {
  X,
  Mail,
  Lock,
  User,
  ArrowRight,
  Loader2,
  Github,
  Sparkles,
} from "lucide-react";
import { loginUser, registerUser } from "../services/authService";
import { useNavigate } from "react-router-dom";
import "../index.css";

export default function AuthModal({ isOpen, onClose, defaultTab = "login" }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (isOpen) {
      setActiveTab(defaultTab);
      setError("");
      setForm({ full_name: "", email: "", password: "" });
    }
  }, [isOpen, defaultTab]);

  const [form, setForm] = useState({
    full_name: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      if (activeTab === "login") {
        const tokens = await loginUser({
          email: form.email,
          password: form.password,
        });
        localStorage.setItem("access_token", tokens.access);
        localStorage.setItem("refresh_token", tokens.refresh);
        onClose();
        navigate("/dashboard");
      } else {
        await registerUser(form);
        setActiveTab("login");
        setError("Account created! Please login.");
      }
    } catch (err) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
      <div
        className="absolute inset-0 bg-background/60 backdrop-blur-md transition-opacity duration-300"
        onClick={onClose}
      />

      <div className="relative w-full max-w-md bg-card border border-border/50 rounded-3xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-300">
        <div className="p-8 pb-0 text-center relative z-10">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-primary/10 text-primary mb-4">
            <User size={24} />
          </div>
          <h2 className="text-2xl font-bold tracking-tight">
            {activeTab === "login" ? "Welcome Back" : "Start Your Journey"}
          </h2>
          <p className="text-sm text-muted-foreground mt-2">
            {activeTab === "login"
              ? "Access your personalized career roadmap."
              : "Join Maargha AI to build your future self."}
          </p>
        </div>

        <div className="flex p-2 bg-secondary/50 m-6 mb-0 rounded-xl relative">
          <div
            className={`absolute inset-y-2 w-[calc(50%-8px)] bg-background border border-border/50 shadow-sm rounded-lg transition-transform duration-300 ease-spring ${
              activeTab === "login"
                ? "left-2 translate-x-0"
                : "left-2 translate-x-full"
            }`}
          />
          <button
            type="button"
            onClick={() => setActiveTab("login")}
            className={`flex-1 relative z-10 py-2 text-sm font-medium transition-colors duration-200 ${
              activeTab === "login"
                ? "text-foreground"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Log In
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("register")}
            className={`flex-1 relative z-10 py-2 text-sm font-medium transition-colors duration-200 ${
              activeTab === "register"
                ? "text-foreground"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Register
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-8 pt-6 space-y-4">
          {activeTab === "register" && (
            <div className="space-y-2 animate-in slide-in-from-left-4 fade-in duration-300">
              <div className="relative">
                <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <input
                  name="full_name"
                  placeholder="Full Name"
                  value={form.full_name}
                  onChange={handleChange}
                  required
                  className="w-full h-10 pl-9 pr-4 rounded-lg border border-input bg-transparent text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
                />
              </div>
            </div>
          )}

          <div className="space-y-2">
            <div className="relative">
              <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <input
                name="email"
                type="email"
                placeholder="Email Address"
                value={form.email}
                onChange={handleChange}
                required
                className="w-full h-10 pl-9 pr-4 rounded-lg border border-input bg-transparent text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
              />
            </div>
          </div>

          <div className="space-y-2">
            <div className="relative">
              <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <input
                name="password"
                type="password"
                placeholder="Password"
                value={form.password}
                onChange={handleChange}
                required
                className="w-full h-10 pl-9 pr-4 rounded-lg border border-input bg-transparent text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
              />
            </div>
          </div>

          {error && (
            <div
              className={`text-xs p-3 rounded-lg ${
                error.includes("Account created")
                  ? "text-green-600 bg-green-500/10"
                  : "text-destructive bg-destructive/10"
              }`}
            >
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full h-11 mt-2 bg-primary text-primary-foreground font-bold rounded-xl shadow-lg shadow-primary/20 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2 group"
          >
            {loading ? (
              <Loader2 className="animate-spin h-5 w-5" />
            ) : (
              <>
                {activeTab === "login" ? "Sign In" : "Create Account"}
                <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </>
            )}
          </button>
        </form>

        <div className="p-6 pt-0 text-center">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t border-border/50"></span>
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-card px-3 text-muted-foreground">
                Why Maargha AI?
              </span>
            </div>
          </div>

          <div className="mt-4 p-4 rounded-lg bg-gradient-to-br from-primary/10 to-blue-500/10 border border-primary/20">
            <div className="flex items-center justify-center gap-2 mb-2">
              <span className="font-semibold text-sm">
                AI-Powered Career Intelligence
              </span>
            </div>
            <p className="text-xs text-muted-foreground">
              Personalized pathways, real-time insights & smart optimization
            </p>
          </div>
        </div>

        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 text-muted-foreground hover:text-foreground transition-colors rounded-full hover:bg-secondary"
        >
          <X size={20} />
        </button>

        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-primary to-transparent opacity-50" />
        <div className="absolute -top-[100px] -right-[100px] w-[200px] h-[200px] bg-primary/5 blur-[80px] rounded-full pointer-events-none" />
        <div className="absolute -bottom-[100px] -left-[100px] w-[200px] h-[200px] bg-blue-500/5 blur-[80px] rounded-full pointer-events-none" />
      </div>
    </div>
  );
}
