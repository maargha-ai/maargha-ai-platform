import { useEffect, useState } from "react";
import "../styles/hoverGrid.css";

const ROWS = 9;
const COLS = 19;
const COLORS = ["#235CD9","#142A5B", "#0F172A","#F6EEFE", "#b28ade"];

export default function HoverGrid() {
  const [tiles, setTiles] = useState(
    Array.from({ length: ROWS * COLS }, () => ({
      color: null,
      activeAt: null,
    }))
  );

  const activateTile = (index) => {
    const now = Date.now();

    setTiles((prev) =>
      prev.map((tile, i) =>
        i === index
          ? {
              color: COLORS[Math.floor(Math.random() * COLORS.length)],
              activeAt: now,
            }
          : tile
      )
    );
  };

  // DECAY LOOP — this was missing / incorrect earlier
  useEffect(() => {
    const interval = setInterval(() => {
      setTiles((prev) =>
        prev.map((tile) => {
          if (!tile.activeAt) return tile;

          const elapsed = Date.now() - tile.activeAt;

          if (elapsed > 500) {
            // RESET TO DEFAULT
            return { color: null, activeAt: null };
          }

          return tile;
        })
      );
    }, 100);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="hover-grid">
      {tiles.map((tile, i) => (
        <div
          key={i}
          className="grid-tile"
          style={tile.color ? { backgroundColor: tile.color } : {}}
          onMouseEnter={() => activateTile(i)}
        />
      ))}
    </div>
  );
}
