import { useEffect, useRef, useState } from "react";
import { Clock, Mic, StopCircle } from "lucide-react";
import "../../styles/quiz.css";

export default function QuizSession({ socket, onStop }) {
  const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState("");
  const [warnings, setWarnings] = useState(0);
  const videoRef = useRef(null);

  /* ===============================
     Camera helpers
     =============================== */
  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(t => t.stop());
      videoRef.current.srcObject = null;
    }
  };

  const captureFrame = () => {
    const video = videoRef.current;
    if (!video || video.readyState < 2) return null;

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    return canvas.toDataURL("image/jpeg", 0.6);
  };

  /* ===============================
     1️⃣ WebSocket listener
     =============================== */
  useEffect(() => {
    if (!socket) return;

    const handler = (e) => {
      const data = JSON.parse(e.data);

      if (data.type === "quiz_question") {
        setQuestion(data.question); // 🔥 KEY FIX
      }

      if (data.type === "quiz_warning") {
        setWarnings(data.warnings);
      }

      if (data.type === "quiz_terminated") {
        stopCamera();
        alert("Quiz terminated due to malpractice.");
        onStop?.();
      }

      if (data.type === "quiz_evaluation") {
        stopCamera();
      }
    };

    socket.addEventListener("message", handler);
    return () => socket.removeEventListener("message", handler);
  }, [socket, onStop]);

  /* ===============================
     2️⃣ Camera + monitoring
     =============================== */
  useEffect(() => {
    if (!socket) return;

    let stream;
    let interval;

    async function startCamera() {
      stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;

      interval = setInterval(() => {
        const frame = captureFrame();
        if (!frame) return;

        socket.send(
          JSON.stringify({
            type: "monitor_frame",
            frame,
          })
        );
      }, 1500); // 1.5 FPS
    }

    startCamera();

    return () => {
      if (interval) clearInterval(interval);
      if (stream) stream.getTracks().forEach(t => t.stop());
    };
  }, [socket]);

  /* ===============================
     3️⃣ Quiz actions
     =============================== */
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
    stopCamera();
    onStop?.();
  };

  /* ===============================
     Loading state
     =============================== */
  if (!question) {
    return <div className="loading">Loading question...</div>;
  }

  /* ===============================
     UI
     =============================== */
  return (
    <div className="quiz-layout">
      <div className="quiz-bg"></div>

      <div className="quiz-container">
        <div className="session-layout">

          {warnings > 0 && (
            <div className="warning-banner">
              ⚠️ Attention warning {warnings}/3 — please focus on the screen
            </div>
          )}

          <div className="question-panel">
            <div className="question-header">
              <span className="q-badge">Active Assessment</span>
              <div className="flex items-center gap-2 text-primary font-mono">
                <Clock size={16} />
                <span>00:45</span>
              </div>
            </div>

            <h3 className="live-question">{question}</h3>

            <div className="answer-area">
              <textarea
                placeholder="Type your technical response here..."
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                autoFocus
              />
            </div>

            <div className="session-actions">
              <button
                onClick={stopQuiz}
                className="stop-btn flex items-center gap-2"
              >
                <StopCircle size={18} /> Terminate
              </button>

              <button
                onClick={submitAnswer}
                disabled={!answer.trim()}
                className="next-btn flex items-center gap-2"
              >
                Submit Response
              </button>
            </div>
          </div>

          <div className="side-panel">
            <div className="camera-card">
              <video
                ref={videoRef}
                autoPlay
                muted
                playsInline
                className="camera-video"
              />
              <div className="camera-overlay">
                <div className="rec-dot"></div>
                LIVE PROCTORING
              </div>
            </div>

            <div className="bg-card/50 backdrop-blur p-4 rounded-xl border border-border/50">
              <div className="flex items-center gap-3 mb-2">
                <div className="p-2 bg-green-500/10 text-green-500 rounded-lg">
                  <Mic size={20} />
                </div>
                <div>
                  <div className="text-sm font-bold">Audio Input</div>
                  <div className="text-xs text-muted-foreground">
                    Monitoring active
                  </div>
                </div>
              </div>

              <div className="h-1 w-full bg-secondary rounded-full overflow-hidden">
                <div className="h-full bg-green-500 w-[60%] animate-pulse"></div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
