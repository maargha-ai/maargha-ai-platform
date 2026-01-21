import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import OrchestratorChat from "./pages/OrchestratorChat";
import NetworkingEvents from "./pages/NetworkingEvents";
import QuizPage from "./pages/quiz/QuizPage";
import QuizEvaluationPage from "./pages/quiz/QuizEvaluationPage";
import EmotionalSupportPage from "./pages/emotional-support/EmotionalSupportPage";
import MusicRecommendation from "./pages/MusicRecommendation";
import CareerFinder from "./pages/CareerFinder";
import Roadmap from "./pages/Roadmap";
import JobSearch from "./pages/JobSearch";
import LinkedInAssistant from "./pages/LinkedInAssistant";
import NewsDigest from "./pages/NewsDigest";
import Tutor from "./pages/Tutor";
import CVGeneration from "./pages/CVGeneration";
import ResumeParser from "./pages/ResumeParser";

import "./styles/stars.css";
import ProtectedRoute from "./components/ProtectedRoute";
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/networking-events" element={<NetworkingEvents />} />
        <Route path="/quiz" element={<QuizPage />} />
        <Route path="/quiz/evaluation" element={<QuizEvaluationPage />} />
        <Route path="/emotional-support" element={<EmotionalSupportPage />} />
        <Route path="/music" element={<MusicRecommendation />} />
        <Route path="/career" element={<CareerFinder />} />
        <Route path="/roadmap" element={<Roadmap />} />
        <Route path="/jobs" element={<JobSearch />} />
        <Route path="/linkedin" element={<LinkedInAssistant />} />
        <Route path="/news" element={<NewsDigest />} />
        <Route path="/tutor" element={<Tutor />} />
        <Route path="/cv" element={<CVGeneration />} />
        <Route path="/resume-parser" element={<ResumeParser />} />

        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
        <Route path="/orchestrator" element={
          <ProtectedRoute>
            <OrchestratorChat />
          </ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  );
}
export default App;


