import { useState } from "react";
import { useNavigate } from "react-router-dom";
import HoverGrid from "../components/HoverGrid";
import RotatingBadge from "../components/RotatingBadge";
import PremiumNavbar from "../components/PremiumNavbar";
import ThinkingProcess from "../components/ThinkingProcess";
import FeaturesGrid from "../components/FeaturesGrid";
import AuthModal from "../components/AuthModal";
import { ArrowRight, Sparkles } from "lucide-react";
import "../styles/home.css";

import { useAuth } from "../context/AuthContext";

export default function Home() {
  const navigate = useNavigate();
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [authDefaultTab, setAuthDefaultTab] = useState("login");
  const { isAuthenticated } = useAuth();

  const openAuthModal = (tab = "login") => {
    if (isAuthenticated) {
      navigate("/dashboard");
      return;
    }
    setAuthDefaultTab(tab);
    setIsAuthModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-background text-foreground overflow-x-hidden selection:bg-primary selection:text-primary-foreground">
      <PremiumNavbar onOpenAuth={() => openAuthModal("login")} onGetStarted={() => openAuthModal("register")} />
      
      <AuthModal 
        isOpen={isAuthModalOpen} 
        onClose={() => setIsAuthModalOpen(false)} 
        defaultTab={authDefaultTab}
      />

      {/* HERO SECTION */}
      <section className="hero-outer pt-20 md:pt-24">
        <div className="hero-inner relative flex flex-col items-center justify-center">
          {/* BACKGROUND ANIMATION */}
          <HoverGrid />

          {/* ROTATING BADGE (Top Right or Center) */}
          <div className="absolute top-8 right-8 z-20 hidden md:block">
            <RotatingBadge />
          </div>

          {/* HERO CONTENT */}
          <div className="content-center z-20 px-4 w-full max-w-4xl mx-auto flex flex-col items-center gap-6">
            
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-background/50 backdrop-blur-md border border-border shadow-sm animate-fade-in-up">
              <Sparkles size={16} className="text-amber-500" />
              <span className="text-sm font-medium tracking-wide uppercase">AI-Powered Career Architect</span>
            </div>

            <h1 className="text-5xl md:text-8xl font-black text-center leading-tight tracking-tighter">
              Build your <br/>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary via-blue-600 to-primary/50">
                Future Self
              </span>
            </h1>

            <p className="text-lg md:text-xl text-muted-foreground text-center max-w-2xl font-light leading-relaxed">
              Maargha AI doesn't just suggest jobs. It analyzes, plans, and mentors you through every 
              step of your career evolution with intelligent, data-driven pathways.
            </p>

            <div className="flex flex-col md:flex-row items-center gap-4 mt-4">
              <button 
                onClick={() => openAuthModal("register")}
                className="group relative px-8 py-4 bg-primary text-primary-foreground text-lg font-bold rounded-full overflow-hidden shadow-xl shadow-primary/20 hover:scale-105 transition-all duration-300"
              >
                <div className="absolute inset-0 bg-white/10 group-hover:translate-x-full transition-transform duration-500 ease-out skew-x-12" />
                <span className="relative flex items-center gap-2">
                  Start Your Journey <ArrowRight size={20} />
                </span>
              </button>
              
              <button 
                onClick={() => openAuthModal("login")}
                className="px-8 py-4 bg-transparent border border-foreground/10 hover:bg-foreground/5 text-foreground text-lg font-medium rounded-full transition-all"
              >
                Login
              </button>
            </div>
          </div>

          <div className="hero-marquee">
            <div className="marquee-track">
              <span>AI CAREER</span>
              <span>PATH FINDER</span>
              <span>SKILL ANALYSIS</span>
              <span>REAL-TIME MARKET DATA</span>
              <span>LINKEDIN OPTIMIZER</span>
              <span>MENTORSHIP</span>
              <span>RESUME BUILDER</span>
              <span>INTERVIEW PREP</span>
              <span>AI CAREER</span>
              <span>PATH FINDER</span>
              <span>SKILL ANALYSIS</span>
            </div>
          </div>
        </div>
      </section>

      {/* NEW SECTIONS */}
      <ThinkingProcess />
      
      <FeaturesGrid />

      {/* FOOTER */}
      <footer className="py-12 border-t border-border mt-20">
        <div className="max-w-7xl mx-auto px-6 text-center md:text-left flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2 font-bold text-xl">
             <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-primary-foreground">M</div>
             <span>MAARGHA.AI</span>
          </div>
          <p className="text-muted-foreground text-sm">
            © {new Date().getFullYear()} Maargha AI. Redefining Career Growth.
          </p>
          <div className="flex gap-6 text-sm font-medium text-muted-foreground">
             <a href="#" className="hover:text-foreground">Privacy</a>
             <a href="#" className="hover:text-foreground">Terms</a>
             <a href="#" className="hover:text-foreground">Twitter</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
