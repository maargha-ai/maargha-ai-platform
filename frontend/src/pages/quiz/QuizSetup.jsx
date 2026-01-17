import { useState } from "react";

export default function QuizSetup({ onStart }) {
  const [topic, setTopic] = useState("");
  const [level, setLevel] = useState("easy");

  return (
    <div className="quiz-setup">
      <h2>Start Quiz</h2>

      <input
        placeholder="Enter quiz topic (e.g. Machine Learning)"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
      />

      <select value={level} onChange={(e) => setLevel(e.target.value)}>
        <option value="easy">Easy</option>
        <option value="medium">Medium</option>
        <option value="hard">Hard</option>
      </select>

      <button onClick={() => onStart(topic, level)}>
        Start Quiz
      </button>
    </div>
  );
}
