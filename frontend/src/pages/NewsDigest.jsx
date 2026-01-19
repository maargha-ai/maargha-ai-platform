import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { 
  ArrowLeft, 
  ExternalLink, 
  Newspaper,
  Loader2,
  RefreshCw
} from "lucide-react";
import { useTheme } from "../components/ThemeProvider";
import { Button } from "../components/ui/button";
import "../styles/news.css";

export default function NewsDigest() {
  const navigate = useNavigate();
  const { theme, setTheme } = useTheme();
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchNews = () => {
    setLoading(true);
    fetch("http://localhost:8000/news/latest")
      .then(res => res.json())
      .then(data => {
        setNews(data.articles || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchNews();
  }, []);

  return (
    <div className={`news-layout ${theme}`}>
      <div className="news-container">
         <header className="news-header">
            <div className="flex flex-col gap-4">
              <Button variant="ghost" className="w-fit p-0 hover:bg-transparent" onClick={() => navigate("/dashboard")}>
                 <ArrowLeft size={20} className="mr-2" /> Back to Dashboard
              </Button>
              <div className="news-title">
                 <h1>Tech Pulse <span>Digest</span></h1>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
               <Button variant="outline" size="icon" onClick={fetchNews} disabled={loading}>
                 <RefreshCw size={18} className={loading ? "animate-spin" : ""} />
               </Button>
            </div>
         </header>

         {loading ? (
           <div className="loading-skeleton">
             <Loader2 size={48} className="animate-spin text-primary" />
             <p>Curating latest tech insights...</p>
           </div>
         ) : news.length > 0 ? (
           <div className="news-grid">
             {news.map((n, i) => (
               <article key={i} className="news-card">
                 <div className="news-source">
                   {n.source || "TechCrunch"}
                 </div>
                 <h4>{n.title}</h4>
                 <div className="news-footer">
                   <a href={n.link} target="_blank" rel="noreferrer" className="read-btn">
                     Read Full Story <ExternalLink size={16} />
                   </a>
                 </div>
               </article>
             ))}
           </div>
         ) : (
           <div className="text-center py-20 text-muted-foreground">
             <Newspaper size={48} className="mx-auto mb-4 opacity-20" />
             <p>No fresh news at the moment.</p>
           </div>
         )}
      </div>
    </div>
  );
}
