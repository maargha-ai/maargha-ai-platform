import { useEffect, useRef, useState } from "react";
import { StopCircle } from "lucide-react";
import "../../styles/quiz.css";

export default function QuizSession({ socket }) {
  const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState("");
  const [warnings, setWarnings] = useState(0);
  const [cameraError, setCameraError] = useState("");
  const [isLoadingNext, setIsLoadingNext] = useState(false);
  const [isTerminating, setIsTerminating] = useState(false);
  const videoRef = useRef(null);
  const loadingRef = useRef(false);
  const terminatingRef = useRef(false);
  const questionRef = useRef(null);

  useEffect(() => {
    loadingRef.current = isLoadingNext;
  }, [isLoadingNext]);

  useEffect(() => {
    terminatingRef.current = isTerminating;
  }, [isTerminating]);

  useEffect(() => {
    questionRef.current = question;
  }, [question]);

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      videoRef.current.srcObject.getTracks().forEach((t) => t.stop());
      videoRef.current.srcObject = null;
    }
  };

  const captureFrame = () => {
    const video = videoRef.current;
    if (!video || video.readyState < 2) return null;
    if (!video.videoWidth || !video.videoHeight) return null;

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    return canvas.toDataURL("image/jpeg", 0.6);
  };

  useEffect(() => {
    if (!socket) return;

    const handler = (e) => {
      const data = JSON.parse(e.data);

      if (data.type === "quiz_question") {
        setQuestion(data.question);
        setIsLoadingNext(false);
        setIsTerminating(false);
      }

      if (data.type === "quiz_warning") {
        setWarnings(data.warnings);
      }

      if (data.type === "quiz_terminated") {
        stopCamera();
        setIsLoadingNext(false);
        setIsTerminating(true);
        alert("Quiz terminated due to malpractice.");
      }

      if (data.type === "quiz_evaluation") {
        stopCamera();
        setIsLoadingNext(false);
        setIsTerminating(false);
      }

      if (data.type === "error") {
        setIsLoadingNext(false);
        setIsTerminating(false);
      }
    };

    socket.addEventListener("message", handler);
    return () => socket.removeEventListener("message", handler);
  }, [socket]);

  useEffect(() => {
    if (!socket) return;

    let stream;
    let interval;
    let healthInterval;
    let stopped = false;

    const startCamera = async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: {
            facingMode: "user",
            width: { ideal: 640 },
            height: { ideal: 480 },
          },
          audio: false,
        });

        let attempts = 0;
        while (!videoRef.current && attempts < 20) {
          await new Promise((resolve) => setTimeout(resolve, 100));
          attempts += 1;
        }
        if (!videoRef.current) {
          setCameraError("Camera UI not ready. Please reload once.");
          return;
        }
        const videoEl = videoRef.current;
        videoEl.srcObject = stream;

        await new Promise((resolve) => {
          videoEl.onloadedmetadata = () => resolve(true);
          setTimeout(() => resolve(true), 1000);
        });

        await videoEl.play();
        setCameraError("");
      } catch (err) {
        console.error("Camera start failed:", err);
        setCameraError("Camera unavailable. Check browser permission.");
        return;
      }

      interval = setInterval(() => {
        if (loadingRef.current || terminatingRef.current || !questionRef.current) return;
        const frame = captureFrame();
        if (!frame) return;

        socket.send(
          JSON.stringify({
            type: "monitor_frame",
            frame,
          })
        );
      }, 1000);

      healthInterval = setInterval(async () => {
        const videoEl = videoRef.current;
        if (!videoEl || stopped) return;
        if (terminatingRef.current) {
          if (videoEl.srcObject) {
            videoEl.srcObject.getTracks().forEach((t) => t.stop());
            videoEl.srcObject = null;
          }
          return;
        }

        const badVideoState =
          !videoEl.srcObject ||
          videoEl.readyState < 2 ||
          !videoEl.videoWidth ||
          videoEl.paused ||
          videoEl.ended;

        if (badVideoState) {
          try {
            if (stream) stream.getTracks().forEach((t) => t.stop());

            stream = await navigator.mediaDevices.getUserMedia({
              video: {
                facingMode: "user",
                width: { ideal: 640 },
                height: { ideal: 480 },
              },
              audio: false,
            });
            videoEl.srcObject = stream;
            await videoEl.play();
            setCameraError("");
          } catch (err) {
            setCameraError("Camera feed interrupted. Trying to recover...");
          }
        }
      }, 3000);
    };

    startCamera();

    return () => {
      stopped = true;
      if (interval) clearInterval(interval);
      if (healthInterval) clearInterval(healthInterval);
      if (stream) stream.getTracks().forEach((t) => t.stop());
    };
  }, [socket]);

  const submitAnswer = () => {
    if (!answer.trim() || isLoadingNext || isTerminating) return;

    socket.send(
      JSON.stringify({
        type: "quiz_answer",
        answer,
      })
    );

    setIsLoadingNext(true);
    setAnswer("");
  };

  const stopQuiz = () => {
    if (isTerminating) return;

    setIsTerminating(true);
    socket.send(
      JSON.stringify({
        type: "stop_quiz",
        answer,
      })
    );
    stopCamera();
  };

  return (
    <div className="quiz-layout">
      <div className="quiz-bg"></div>

      <div className="quiz-container">
        <div className="session-layout">
          <div className="question-panel">
            <div className="question-header">
              <span className="q-badge">Active Assessment</span>
              {warnings > 0 && (
                <span className="warning-chip">
                  Warning {warnings}/3
                </span>
              )}
            </div>

            <h3 className="live-question">{question || "Loading first question..."}</h3>

            <div className="answer-area">
              <textarea
                placeholder="Type your technical response here..."
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                disabled={!question || isLoadingNext || isTerminating}
                autoFocus
              />
            </div>

            {(isLoadingNext || isTerminating) && (
              <div className="pending-row">
                <span className="spinner"></span>
                <span className="pending-text">
                  {isTerminating ? "Finalizing assessment..." : "Loading next question..."}
                </span>
              </div>
            )}

            <div className="session-actions">
              <button
                onClick={stopQuiz}
                disabled={!question || isTerminating}
                className="stop-btn flex items-center gap-2"
              >
                <StopCircle size={18} /> Terminate
              </button>

              <button
                onClick={submitAnswer}
                disabled={!question || !answer.trim() || isLoadingNext || isTerminating}
                className="next-btn flex items-center gap-2"
              >
                Submit Response
              </button>
            </div>
          </div>

          <div className="side-panel">
            <div className="camera-card">
              <video ref={videoRef} autoPlay muted playsInline className="camera-preview" />
              <div className="camera-overlay">
                <div className="rec-dot"></div>
                LIVE PROCTORING
              </div>
              {cameraError && <div className="camera-error">{cameraError}</div>}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
