import { useNavigate } from "react-router-dom";
import { 
  ArrowLeft, 
  Calendar, 
  Globe,
  MapPin
} from "lucide-react";
import { useTheme } from "../components/ThemeProvider";
import { Button } from "../components/ui/button";
import "../styles/networking.css";
export default function NetworkingEvents() {
  const navigate = useNavigate();
  const { theme, setTheme } = useTheme();
  return (
    <div className={`networking-layout ${theme}`}>
      <header className="net-header">
        <div className="flex items-center gap-4">
           <Button variant="ghost" size="icon" onClick={() => navigate("/dashboard")} className="rounded-full">
              <ArrowLeft size={24} />
           </Button>
           <div>
              <h1 className="text-xl font-bold font-display">Global Tech Events</h1>
              <p className="text-xs text-muted-foreground">Real-time networking & hackathon data</p>
           </div>
        </div>
      </header>
      <main className="net-main">
        {}
        <div className="net-stats-row">
           <div className="net-stat-card">
              <div className="stat-icon"><Calendar size={20} /></div>
              <div className="stat-value">142</div>
              <div className="stat-label">Upcoming Hackathons</div>
           </div>
           <div className="net-stat-card">
              <div className="stat-icon"><Globe size={20} /></div>
              <div className="stat-value">28</div>
              <div className="stat-label">Virtual Summits</div>
           </div>
           <div className="net-stat-card">
              <div className="stat-icon"><MapPin size={20} /></div>
              <div className="stat-value">Bangalore</div>
              <div className="stat-label">Top Tech Hub</div>
           </div>
        </div>
        <div className="iframe-wrapper">
          <iframe
            title="Networking Events Dashboard"
            src="http://localhost:8050"
            allowFullScreen
          />
        </div>
      </main>
    </div>
  );
}


