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

const Dashboard = () => {
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
      title: 'AI Orchestrator',
      description: 'Central command for career strategy & analysis.',
      icon: Cpu,
      path: '/orchestrator',
      top: '10%',
      left: '50%'   
    },
    { 
      id: 'news',
      title: 'Global Intel',
      description: 'Real-time industry shifts & news digest.',
      icon: Newspaper,
      path: '/news',
      top: '22%',
      left: '30%'   
    },
    { 
      id: 'quiz',
      title: 'Skill Matrix',
      description: 'Technical competency validation engine.',
      icon: Trophy,
      path: '/quiz',
      top: '35%',
      left: '70%'
    },
    { 
      id: 'jobs',
      title: 'Job Architect',
      description: 'Strategic role placement & matching.',
      icon: Briefcase,
      path: '/jobs',
      top: '48%',
      left: '40%'   
    },
    { 
      id: 'linkedin',
      title: 'LinkedIn AI',
      description: 'Profile maximization & networking assistant.',
      icon: Zap,
      path: '/linkedin',
      top: '60%',
      left: '60%'   
    },
    { 
      id: 'networking',
      title: 'Events Sync',
      description: 'High-value industry meetups & webinars.',
      icon: Users,
      path: '/networking-events',
      top: '72%',
      left: '30%'   
    },
    { 
      id: 'career',
      title: 'Path Finder',
      description: 'Long-term persona & career mapping.',
      icon: Search,
      path: '/career',
      top: '80%',
      left: '50%'   
    },
    { 
      id: 'wellness',
      title: 'Wellness Core',
      description: 'Emotional aid & sonic focus therapy.',
      icon: Heart, 
      path: '/emotional-support',
      top: '90%',
      left: '70%'   
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
               d="M 50,5 C 50,15 30,15 30,22 C 30,30 70,30 70,35 C 70,42 40,42 40,48 C 40,55 60,55 60,60 C 60,68 30,68 30,72 C 30,78 50,78 50,80 C 50,85 70,85 70,90"
             />
             <motion.path 
               className="spine-path-active"
               d="M 50,5 C 50,15 30,15 30,22 C 30,30 70,30 70,35 C 70,42 40,42 40,48 C 40,55 60,55 60,60 C 60,68 30,68 30,72 C 30,78 50,78 50,80 C 50,85 70,85 70,90"
               style={{ pathLength: scrollYProgress }}
             />
             
             <path 
               ref={pathRef}
               d="M 50,5 C 50,15 30,15 30,22 C 30,30 70,30 70,35 C 70,42 40,42 40,48 C 40,55 60,55 60,60 C 60,68 30,68 30,72 C 30,78 50,78 50,80 C 50,85 70,85 70,90"
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

export default Dashboard;
