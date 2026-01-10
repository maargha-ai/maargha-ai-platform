export default function StarBackground({ count = 900 }) {
  const stars = Array.from({ length: count });

  return (
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
  );
}
