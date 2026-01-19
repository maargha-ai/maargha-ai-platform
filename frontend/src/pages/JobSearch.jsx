import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { 
  Briefcase, 
  MapPin, 
  Upload, 
  Search, 
  ExternalLink,
  Building2,
  ArrowRight,
  Sparkles,
  ArrowLeft
} from "lucide-react";
import { useTheme } from "../components/ThemeProvider";
import { Button } from "../components/ui/button";
import "../styles/jobsearch.css";

export default function JobSearch() {
  const navigate = useNavigate();
  const { theme, setTheme } = useTheme();
  
  const [role, setRole] = useState("");
  const [location, setLocation] = useState("");
  const [cv, setCv] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    if (!role || !location || !cv) return;

    setLoading(true);
    setJobs([]);

    const formData = new FormData();
    formData.append("role", role);
    formData.append("location", location);
    formData.append("cv", cv);

    try {
      const res = await fetch("http://localhost:8000/jobs/match", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: formData,
      });

      const data = await res.json();
      setJobs(data.jobs || []);
    } catch (error) {
      console.error("Error matching jobs:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`job-search-page ${theme}`}>
      {/* Background Effects */}
      <div className="job-search-bg">
        <div className="bg-gradient-spot spot-1"></div>
        <div className="bg-gradient-spot spot-2"></div>
      </div>

      <div className="job-content">
        {/* Header */}
        <header className="job-header">
           <div className="flex items-center gap-4">
             <div className="job-title-section">
                <h1>AI Job Architect</h1>
                <p>Upload your CV and let our AI match you with your dream role.</p>
             </div>
           </div>
           
           <div className="flex items-center gap-2">
           </div>
        </header>

        {/* Search Section */}
        <div className="search-card">
          <div className="input-group">
            <div className="input-field-wrapper">
              <Briefcase size={20} />
              <input
                placeholder="Target Role (e.g. Full Stack Developer)"
                value={role}
                onChange={(e) => setRole(e.target.value)}
              />
            </div>

            <div className="input-field-wrapper">
              <MapPin size={20} />
              <input
                placeholder="Preferred Location (e.g. Remote, Bangalore)"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
              />
            </div>

            <label className="file-upload-btn">
              <Upload size={20} />
              <span>{cv ? cv.name : "Upload Resume (PDF)"}</span>
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => setCv(e.target.files[0])}
              />
            </label>

            <button 
              className="search-btn" 
              onClick={submit} 
              disabled={loading || !role || !location || !cv}
            >
              {loading ? (
                <>
                  <Sparkles size={20} className="animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Search size={20} />
                  Find Matches
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results Section */}
        {jobs.length > 0 ? (
          <div className="results-container">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <Sparkles className="text-primary" size={24} />
              Top AI-Curated Matches
            </h2>
            <div className="results-grid">
              {jobs.map((job, i) => (
                <div key={i} className="job-card">
                  <div className="match-badge">
                    {(job.score * 100).toFixed(0)}% Match
                  </div>
                  
                  <div className="job-card-header">
                    <h3>{job.title}</h3>
                    <div className="company-name">
                      <Building2 size={16} />
                      {job.company}
                    </div>
                  </div>

                  <div className="job-details">
                     <span>• {job.source}</span>
                     <span>• Full Time</span>
                  </div>

                  <p className="job-desc">{job.desc}</p>

                  <div className="job-card-footer">
                    <a href={job.link} target="_blank" rel="noreferrer" className="view-job-btn">
                      View Application <ExternalLink size={16} />
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          !loading && <div className="text-center text-muted-foreground mt-20">
             <Briefcase size={48} className="mx-auto mb-4 opacity-20" />
             <p>Enter your details above to start the AI matching engine.</p>
          </div>
        )}
      </div>
    </div>
  );
}
