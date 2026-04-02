import { useRef, useEffect } from "react";

export default function RoadmapVisualizer({ roadmap }) {
  const pathRef = useRef(null);
  const carRef = useRef(null);
  const cardsRef = useRef([]);

  const steps = roadmap?.steps || [];
  if (steps.length === 0) return null;

  const sceneWidth = 1200;
  const startX = 40;
  const rightPadding = 180;
  const gap = steps.length > 1
    ? (sceneWidth - startX - rightPadding) / (steps.length - 1)
    : 0;
  const sceneHeight = 480;

  const pathD = `
    M ${startX},280
    C ${startX + 200},210 ${startX + 400},210 ${startX + 600},280
    C ${startX + 800},350 ${startX + 1000},350 ${sceneWidth - 160},280
  `;

  useEffect(() => {
    const path = pathRef.current;
    const car = carRef.current;
    const cards = cardsRef.current;

    if (!path || !car) return;

    const length = path.getTotalLength();
    let progress = 0;

    const animate = () => {
      progress += 0.0007;
      if (progress > 1) progress = 0;

      const point = path.getPointAtLength(progress * length);

      car.style.left = `${point.x}px`;
      car.style.top = `${point.y}px`;

      cards.forEach((card) => {
        if (!card) return;
        const cardX = parseFloat(card.style.left);
        if (point.x > cardX - 120) {
          card.classList.add("show");
        }
      });

      requestAnimationFrame(animate);
    };

    animate();

    return () => {
      cards.forEach((card) => card?.classList.remove("show"));
    };
  }, [roadmap]);

  const setCardRef = (el, index) => {
    if (el) cardsRef.current[index] = el;
  };

  return (
    <div className="rv-scene">
      <svg
        width={sceneWidth}
        height={sceneHeight}
        viewBox={`0 0 ${sceneWidth} ${sceneHeight}`}
        preserveAspectRatio="xMidYMid meet"
      >
        <path
          ref={pathRef}
          d={pathD}
          className="rv-road"
        />
      </svg>

      {/* Car – windows are now correctly INSIDE */}
      <div ref={carRef} className="rv-car">
        <div className="rv-windows" />
      </div>

      {steps.map((step, i) => {
        let x = startX + i * gap;
        if (i === steps.length - 1) {
          x -= 40; // safety margin for last card
        }
        const y = i % 2 === 0 ? 60 : 320;

        return (
          <div
            key={i}
            ref={(el) => setCardRef(el, i)}
            className="rv-card"
            style={{ left: `${x}px`, top: `${y}px` }}
          >
            <h3>{step.title}</h3>
            <p>{step.description}</p>
          </div>
        );
      })}
    </div>
  );
}