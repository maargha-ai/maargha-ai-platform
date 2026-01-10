import HoverGrid from "../components/HoverGrid";
import RotatingBadge from "../components/RotatingBadge";
import Pill from "../components/Pill";
import Title from "../components/Title";
import Description from "../components/Description";
import OrchestratorButton from "../components/GetStartedButton";
import "../styles/home.css";

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
    </div>
  );
}
