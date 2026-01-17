import { useEffect, useRef, useState } from "react";

export default function QuizSession({ socket, question }) {
  const [answer, setAnswer] = useState("");
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  // 🎥 Start camera
  useEffect(() => {
    let active = true;

    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        if (!active) return;
        streamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch((err) => {
        console.error("Camera access denied:", err);
      });

    return () => {
      active = false;
      // 🛑 Stop camera on unmount
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((t) => t.stop());
      }
    };
  }, []);

  const submitAnswer = () => {
    if (!answer.trim()) return;

    socket.send(
      JSON.stringify({
        type: "quiz_answer",
        answer,
      })
    );
    setAnswer("");
  };

  const stopQuiz = () => {
    socket.send(JSON.stringify({ type: "stop_quiz" }));
  };

  return (
    <div className="quiz-session">
      {/* Camera preview */}
      <video
        ref={videoRef}
        autoPlay
        muted
        playsInline
        className="camera-preview"
      />

      <h3>{question}</h3>

      <textarea
        placeholder="Type your answer..."
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
      />

      <div className="quiz-actions">
        <button onClick={submitAnswer} disabled={!answer.trim()}>
          Next
        </button>
        <button onClick={stopQuiz} className="danger">
          Stop Quiz
        </button>
      </div>
    </div>
  );
}
