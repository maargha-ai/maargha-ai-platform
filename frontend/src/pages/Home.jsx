import { useState } from "react";
import { useNavigate } from "react-router-dom";
import HoverGrid from "../components/HoverGrid";
import RotatingBadge from "../components/RotatingBadge";
import Pill from "../components/Pill";
import Title from "../components/Title";
import Description from "../components/Description";
import OrchestratorButton from "../components/GetStartedButton";
import "../styles/home.css";

import { useAuth } from "../context/AuthContext";

export default function Home() {
  const stars = Array.from({ length: 900 });

  return (
    <div className="home-wrapper">
      <section className="hero-outer">
        <div className="hero-inner">

          {/* ⭐ STAR BACKGROUND (SAME AS REGISTER) */}
          <div className="stars-layer">
            {stars.map((_, i) => {
              const movement =
                Math.random() < 0.33 ? 4 : Math.random() < 0.66 ? 8 : 14;

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

          {/* GRID */}
          <HoverGrid />

          {/* BADGE */}
          <RotatingBadge />

          {/* CENTER CONTENT */}
          <div className="content-center">
            <Pill />
            <Title />
            <Description />
            <OrchestratorButton />
          </div>

          {/* MARQUEE */}
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
    </div>
  );
}
