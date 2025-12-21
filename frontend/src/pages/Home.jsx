import HoverGrid from "../components/HoverGrid";
import RotatingBadge from "../components/RotatingBadge";
import Pill from '../components/Pill';
import Title from '../components/Title';
import Description from '../components/Description';
import OrchestratorButton from '../components/GetStartedButton';
import "../styles/home.css";

export default function Home() {
  return (
    <div className="home-wrapper">
      <section className="hero-outer">
        <div className="hero-inner">
          {/* FULL BACKGROUND GRID */}
          <HoverGrid />

          {/* ROTATING BADGE */}
          <RotatingBadge />

          <div className="content-center">
            <Pill />           {/* Agentic AI */}
            <Title />          {/* MAARGA AI */}
            <Description />    {/* small text */}
            <OrchestratorButton /> {/* black button */}
          </div>

          {/* FLOATING CARD
          <div className="hero-card">
            <p className="hero-subtitle">
              An AI-powered{" "}
              <span className="highlight">Personal Growth Platform</span>{" "}
              inspired by design-driven innovation.
            </p>

            <div className="hero-actions">
              <button className="primary-btn">Get Started</button>
              <button className="secondary-btn">Login</button>
            </div>
          </div> */}

          {/* 👇 ADD MARQUEE HERE */}
          <div className="hero-marquee">
            <div className="marquee-track">
              <span>AI CAREER</span>
              <span>AI ROADMAP</span>
              <span>AI TUTOR</span>
              <span>QUIZ GENERATION</span>
              <span>AI JOBSEARCH</span>
              <span>LINKEDIN ASSISTANT</span>
              <span>NETWORKING EVENTS</span>
              <span>EMOTIONAL SUPPORT</span>
              <span>MUSIC RECOMMENDATION</span>
              <span>DAILY NEWS</span>
            </div>
          </div>
        </div>
      </section>

      {/* BELOW CONTENT */}
      <section className="below-section">
        <h2>About Maargha</h2>
        <p>
          Maargha helps individuals discover, plan, and grow their careers using
          AI-driven guidance.
        </p>
      </section>
    </div>
  );
}
