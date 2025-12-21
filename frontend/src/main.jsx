import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import Lenis from "@studio-freight/lenis";

const lenis = new Lenis({
  duration: 0.9,       // 👈 controls scroll speed
  easing: (t) => 1 - Math.pow(1 - t, 3),
  smoothWheel: true,
  smoothTouch: false,
});

function raf(time) {
  lenis.raf(time);
  requestAnimationFrame(raf);
}

requestAnimationFrame(raf);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
