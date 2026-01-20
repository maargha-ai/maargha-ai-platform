import React, { useRef, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, useScroll, useTransform } from 'framer-motion';
import { 
  Newspaper, 
  Briefcase, 
  Users, 
  Heart, 
  Map as MapIcon, 
  Cpu,
  Trophy,
  Search,
  Zap,
  LogOut,
  User,
  Music,
  Settings
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../components/ThemeProvider';
import { ThemeToggle } from '../components/ThemeToggle';

import '../styles/landscape-dashboard.css';
import "../styles/dashboard.css";
import "../styles/register.css"; 

const features = [
  { title: "Career Finder", desc: "Discover careers that match your interests and skills.", route: "/career" },
  { title: "AI Roadmap Generator", desc: "Personalized learning paths for your goals.", route: "/roadmap" },
  { title: "AI Tutor", desc: "Ask doubts and learn interactively.", route: "/tutor" },
  { title: "Quiz Generator", desc: "Test yourself with smart quizzes.", route: "/quiz" },
  // { title: "Quiz Evaluation", desc: "Evaluate your answers.", route: "/quiz/evaluation" },
  { title: "Job Search", desc: "AI-powered job discovery.", route: "/jobs" },
  { title: "CV Generation", desc: "AI-powered CV generator.", route: "/cv" },
  { title: "LinkedIn Assistant", desc: "Optimize your profile and posts.", route: "/linkedin" },
  { title: "Networking Events", desc: "Find relevant hackathons & events.", route: "/networking-events" },
  { title: "Emotional Support", desc: "Talk when you need motivation.", route: "/emotional-support" },
  { title: "Music Recommendation", desc: "Mood-based playlists.", route: "/music" },
  { title: "News Digest", desc: "Curated AI & tech updates.", route: "/news" },
];

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { theme, setTheme } = useTheme();
  const containerRef = useRef(null);
  const pathRef = useRef(null);
  const [markerPos, setMarkerPos] = useState({ x: 50, y: 5 });
  const { scrollYProgress } = useScroll({
    offset: ["start start", "end end"]
  });
  useEffect(() => {
    const unsubscribe = scrollYProgress.on('change', (latest) => {
      if (pathRef.current) {
        const pathLength = pathRef.current.getTotalLength();
        const point = pathRef.current.getPointAtLength(latest * pathLength);
        setMarkerPos({ x: point.x, y: point.y });
      }
    });
    return () => unsubscribe();
  }, [scrollYProgress]);
  const journeyNodes = [
    { 
      id: 'orchestrator',
      title: 'Maargha Orchestrator',
      description: 'Your AI career architect for strategic planning and analysis.',
      icon: Cpu,
      path: '/orchestrator',
      top: '10%',
      left: '50%'   
    },
    { 
      id: 'news',
      title: 'Tech Pulse Digest',
      description: 'Real-time industry shifts and curated tech insights.',
      icon: Newspaper,
      path: '/news',
      top: '20%',
      left: '30%'   
    },
    { 
      id: 'quiz',
      title: 'Technical Assessment',
      description: 'Validate your competency through AI-driven evaluation engines.',
      icon: Trophy,
      path: '/quiz',
      top: '30%',
      left: '70%'
    },
    { 
      id: 'jobs',
      title: 'AI Job Architect',
      description: 'Strategic role placement and matching based on your unique profile.',
      icon: Briefcase,
      path: '/jobs',
      top: '40%',
      left: '40%'   
    },
    { 
      id: 'linkedin',
      title: 'LinkedIn Growth AI',
      description: 'Maximize your profile impact and build high-value connections.',
      icon: Zap,
      path: '/linkedin',
      top: '52%',
      left: '60%'   
    },
    { 
      id: 'networking',
      title: 'Global Tech Events',
      description: 'Real-time networking, hackathons, and virtual summits.',
      icon: Users,
      path: '/networking-events',
      top: '65%',
      left: '30%'   
    },
    { 
      id: 'career',
      title: 'Career Discovery',
      description: 'Analyze your aptitudes and map your professional trajectory.',
      icon: Search,
      path: '/career',
      top: '75%',
      left: '50%'   
    },
    { 
      id: 'music',
      title: 'Sonic Therapy',
      description: 'AI-composed soundscapes for deep focus and mental clarity.',
      icon: Music,
      path: '/music',
      top: '85%',
      left: '68%'
    },
    { 
      id: 'wellness',
      title: 'Empathetic AI',
      description: 'Your conversational companion for emotional support and wellness.',
      icon: Heart, 
      path: '/emotional-support',
      top: '92%',
      left: '35%'   
    }
  ];
  return (
    <div className={`professional-dashboard ${theme}`}>
      <div className="header-brand">
        <div className="brand-dot"></div>
        <span>MAARGHA AI</span>
      </div>
      <div className="map-canvas" ref={containerRef}>
        <div className="map-content-wrapper">
          <svg className="connection-spine-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
             <defs>
               <linearGradient id="activeGradient" x1="0" y1="0" x2="0" y2="1">
                 <stop offset="0%" stopColor="currentColor" stopOpacity="0.2"/>
                 <stop offset="100%" stopColor="currentColor" stopOpacity="1"/>
               </linearGradient>
             </defs>
             <path 
               className="spine-path-bg"
               d="M 50,5 C 50,12 30,12 30,20 C 30,26 70,26 70,30 C 70,36 40,36 40,40 C 40,46 60,46 60,52 C 60,60 30,60 30,65 C 30,70 50,70 50,75 C 50,80 68,80 68,85 C 68,89 35,89 35,92"
             />
             <motion.path 
               className="spine-path-active"
               d="M 50,5 C 50,12 30,12 30,20 C 30,26 70,26 70,30 C 70,36 40,36 40,40 C 40,46 60,46 60,52 C 60,60 30,60 30,65 C 30,70 50,70 50,75 C 50,80 68,80 68,85 C 68,89 35,89 35,92"
               style={{ pathLength: scrollYProgress }}
             />
             <path 
               ref={pathRef}
               d="M 50,5 C 50,12 30,12 30,20 C 30,26 70,26 70,30 C 70,36 40,36 40,40 C 40,46 60,46 60,52 C 60,60 30,60 30,65 C 30,70 50,70 50,75 C 50,80 68,80 68,85 C 68,89 35,89 35,92"
               fill="none"
               stroke="none"
             />
             <circle
                cx={markerPos.x}
                cy={markerPos.y}
                r="2.2"
                fill="hsl(var(--primary))"
                opacity="0.2"
             />
             <circle
                cx={markerPos.x}
                cy={markerPos.y}
                r="1.5"
                fill="hsl(var(--primary))"
                opacity="1"
             />
             <circle
                cx={markerPos.x - 0.4}
                cy={markerPos.y - 0.4}
                r="0.5"
                fill="white"
                opacity="0.8"
             />
          </svg>
          {journeyNodes.map((node, index) => {
            const Icon = node.icon;
            return (
               <motion.div
                 key={node.id}
                 className="map-node"
                 style={{ top: node.top, left: node.left }}
                 initial={{ opacity: 0, y: 30 }}
                 whileInView={{ opacity: 1, y: 0 }}
                 viewport={{ once: true, margin: "-50px" }}
                 transition={{ duration: 0.5, delay: index * 0.1 }}
                 onClick={() => navigate(node.path)}
               >
                 <div className="node-card">
                    <div className="node-icon-box">
                       <Icon size={24} />
                    </div>
                    <div className="node-meta">
                       <div className="node-title">{node.title}</div>
                       <div className="node-desc">{node.description}</div>
                    </div>
                 </div>
               </motion.div>
            );
          })}
          <div style={{ position: 'absolute', top: '95%', width: '100%', height: '100px' }} />
        </div>
      </div>
      <div className="dashboard-hud">
         <div className="hud-profile" onClick={() => navigate('/roadmap')}>
            <div className="profile-avatar">
               {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
            </div>
            <div className="profile-name">
               {user?.name || 'User Profile'}
            </div>
         </div>
         <div className="hud-divider"></div>
         <div className="hud-divder" style={{ width: '0px' }}></div> 
         <ThemeToggle theme={theme} setTheme={setTheme} />
         <div className="hud-divider"></div>
         <div className="hud-item" onClick={logout} title="Logout">
            <LogOut size={20} className="text-destructive" />
         </div>
      </div>
    </div>
  );
};


