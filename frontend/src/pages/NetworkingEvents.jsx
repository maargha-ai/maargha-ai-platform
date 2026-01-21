import { useNavigate } from "react-router-dom";
import { 
  ArrowLeft, 
  Calendar, 
  Users, 
  ExternalLink,
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
            src="https://app.powerbi.com/reportEmbed?reportId=e053da7c-aacf-47a9-8d6a-e51472f94956&autoAuth=true&ctid=39fe8ff6-5063-4b45-ad25-ed60e20269a5"
            allowFullScreen
          />
        </div>
      </main>
    </div>
  );
}


