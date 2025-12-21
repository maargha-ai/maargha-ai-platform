import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Orchestrator from "./pages/Orchestrator";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        {/* After login */}
        <Route path="/dashboard" element={<Dashboard />} />

        {/* Main AI interaction */}
        <Route path="/orchestrator" element={<Orchestrator />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
