import { useEffect, useState, useRef } from "react";
import "../styles/scrollGrid.css";

const COLORS = ["#E8FFC1", "#C7FF5E", "#4F6DFF", "#000000"];

export default function ScrollGrid() {
  const [activeCount, setActiveCount] = useState(0);
  const gridRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          const ratio = entry.intersectionRatio;
          setActiveCount(Math.floor(ratio * 12));
        }
      },
      { threshold: Array.from({ length: 12 }, (_, i) => i / 12) }
    );

    if (gridRef.current) observer.observe(gridRef.current);

    return () => observer.disconnect();
  }, []);

  return (
    <div className="grid-wrapper" ref={gridRef}>
      {Array.from({ length: 12 }).map((_, i) => (
        <div
          key={i}
          className="grid-box"
          style={{
            backgroundColor:
              i < activeCount ? COLORS[i % COLORS.length] : "#f2f2f2",
          }}
        />
      ))}
    </div>
  );
}
