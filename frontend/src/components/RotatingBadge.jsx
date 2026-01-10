import "../styles/rotatingBadge.css";

export default function RotatingBadge() {
  return (
    <div className="badge-wrapper">
      <svg
        className="badge-svg"
        viewBox="0 0 120 120"
      >
        <defs>
          <path
            id="text-circle"
            d="M 60,60 m -46,0 a 46,46 0 1,1 92,0 a 46,46 0 1,1 -92,0"
          />
        </defs>

        <text className="badge-text">
          <textPath href="#text-circle">
            PERSONAL • GROWTH • PLATFORM •
          </textPath>
        </text>
      </svg>

      <div className="badge-center">
        <span>#10</span>
      </div>
    </div>
  );
}
