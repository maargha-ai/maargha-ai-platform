import React, { useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, useScroll, useTransform } from 'framer-motion';
import { 
  Newspaper, 
  Briefcase, 
  Users, 
  Heart, 
  Map, 
  Cpu,
  Trophy,
  Search,
  Zap,
  LogOut,
  User,
  Music
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../components/ThemeProvider';
import { ThemeToggle } from '../components/ThemeToggle';
import '../styles/landscape-dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { theme, setTheme } = useTheme();
  const mainRef = useRef(null);

  const { scrollYProgress } = useScroll({
    target: mainRef,
    offset: ["start start", "end end"]
  });

  const journeyTools = [
    { 
      id: 'news',
      title: 'News Digest',
      description: 'System intelligence gathering from global industry shifts.',
      icon: Newspaper,
      path: '/news',
      top: '10%',
      left: '20%'
    },
    { 
      id: 'career',
      title: 'Career Finder',
      description: 'AI-powered persona mapping for professional alignment.',
      icon: Search,
      path: '/career',
      top: '20%',
      left: '60%'
    },
    { 
      id: 'quiz',
      title: 'Skill Assessment',
      description: 'Technical validation of core professional competencies.',
      icon: Trophy,
      path: '/quiz',
      top: '30%',
      left: '30%'
    },
    { 
      id: 'jobs',
      title: 'Job Search',
      description: 'Strategic placement matching based on skill telemetry.',
      icon: Briefcase,
      path: '/jobs',
      top: '40%',
      left: '75%'
    },
    { 
      id: 'linkedin',
      title: 'LinkedIn Assistant',
      description: 'Neural profile optimization for digital presence.',
      icon: Zap,
      path: '/linkedin',
      top: '50%',
      left: '25%'
    },
    { 
      id: 'networking',
      title: 'Networking Events',
      description: 'High-impact sync points with industry leads.',
      icon: Users,
      path: '/networking-events',
      top: '60%',
      left: '70%'
    },
    { 
      id: 'emotional',
      title: 'Wellness Sync',
      description: 'Maintaining cognitive equilibrium for high performance.',
      icon: Heart,
      path: '/emotional-support',
      top: '75%',
      left: '30%'
    },
    { 
      id: 'music',
      title: 'Music Therapy',
      description: 'Generative sonic environments for peak focus.',
      icon: Music,
      path: '/music',
      top: '85%',
      left: '65%'
    },
    { 
      id: 'roadmap',
      title: 'Career Roadmap',
      description: 'The final blueprint for long-term professional evolution.',
      icon: Map,
      path: '/roadmap',
      top: '95%',
      left: '50%'
    }
  ];

  // Logic for Sidebar Display (includes Orchestrator)
  const sidebarTools = [
    { id: 'orchestrator', title: 'AI Orchestrator', icon: Cpu, path: '/orchestrator' },
    ...journeyTools.slice(0, 4)
  ];
  const sidebarMore = journeyTools.slice(4);

  return (
    <div className={`professional-dashboard ${theme}`}>
      {/* Sidebar */}
      <aside className="dashboard-sidebar">
        <div className="sidebar-header">
          <div className="sidebar-brand" onClick={() => navigate('/')}>
            <div className="brand-icon">M</div>
            <span>Maargha AI</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <div className="nav-section">
            <div className="nav-label">Core Systems</div>
            {sidebarTools.map((tool) => {
              const Icon = tool.icon;
              return (
                <button
                  key={tool.id}
                  className={`nav-item ${tool.id === 'orchestrator' ? 'orchestrator-nav' : ''}`}
                  onClick={() => navigate(tool.path)}
                >
                  <Icon size={18} />
                  <span>{tool.title}</span>
                </button>
              );
            })}
          </div>

          <div className="nav-section">
            <div className="nav-label">Analysis Tools</div>
            {sidebarMore.map((tool) => {
              const Icon = tool.icon;
              return (
                <button
                  key={tool.id}
                  className="nav-item"
                  onClick={() => navigate(tool.path)}
                >
                  <Icon size={18} />
                  <span>{tool.title}</span>
                </button>
              );
            })}
          </div>
        </nav>

        <div className="sidebar-footer">
          <div className="user-profile">
            <div className="user-avatar">
              <User size={16} />
            </div>
            <div className="user-info">
              <div className="user-name">{user?.name || 'User'}</div>
              <div className="user-email">{user?.email || 'user@example.com'}</div>
            </div>
          </div>
          <button onClick={logout} className="logout-button">
            <LogOut size={16} />
          </button>
        </div>
      </aside>

      {/* Main Journey Content */}
      <main className="dashboard-main" ref={mainRef}>
        <header className="dashboard-header">
          <div className="header-info">
            <h1 className="db-title">TRAJECTORY OVERVIEW</h1>
            <p className="db-subtitle">SYNERGIZED CAREER PATH PROTOCOL ACTIVE</p>
          </div>
          
          <div className="orchestrator-hud">
            <div className="hud-label">AI ORCHESTRATOR STATUS</div>
            <div className="hud-stats">
              <div className="hud-stat">
                <span className="stat-name">READINESS</span>
                <span className="stat-value">84%</span>
                <div className="stat-bar"><div className="stat-fill" style={{ width: '84%' }} /></div>
              </div>
              <div className="hud-stat">
                <span className="stat-name">AI SYNC</span>
                <span className="stat-value text-green-500">OPTIMIZED</span>
              </div>
            </div>
          </div>
          
          <ThemeToggle theme={theme} setTheme={setTheme} />
        </header>

        <div className="journey-path-wrapper">
          {/* Trajectory Protocol Badges */}
          <div className="absolute top-0 right-0 p-4 opacity-20 pointer-events-none select-none">
            <div className="text-[10px] font-mono uppercase tracking-[0.2em]">Trajectory Protocol: v2.4.0</div>
            <div className="text-[10px] font-mono uppercase tracking-[0.2em] mt-1">Status: Active Syncing</div>
          </div>

          {/* SVG Winding Path */}
          <svg className="journey-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
            <defs>
              <linearGradient id="pathGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor="currentColor" stopOpacity="0.2" />
                <stop offset="50%" stopColor="currentColor" stopOpacity="0.5" />
                <stop offset="100%" stopColor="currentColor" stopOpacity="0.2" />
              </linearGradient>
            </defs>
            
            {/* Base Path - Creative Winding */}
            <path
              className="path-base"
              d="M 50,0 C 30,10 20,15 20,20 S 40,25 50,30 S 80,35 80,40 S 60,45 50,50 S 20,55 20,60 S 40,65 50,70 S 80,75 80,80 S 60,85 50,90 S 40,95 50,100"
              fill="none"
              strokeWidth="0.8"
            />
            
            {/* Animated Progress Path */}
            <motion.path
              className="path-progress"
              d="M 50,0 C 30,10 20,15 20,20 S 40,25 50,30 S 80,35 80,40 S 60,45 50,50 S 20,55 20,60 S 40,65 50,70 S 80,75 80,80 S 60,85 50,90 S 40,95 50,100"
              fill="none"
              strokeWidth="0.8"
              style={{ pathLength: scrollYProgress }}
            />
          </svg>

          {/* Journey Nodes */}
          {journeyTools.map((tool, index) => {
            const Icon = tool.icon;
            return (
              <motion.div
                key={tool.id}
                className="journey-node"
                style={{
                  top: tool.top,
                  left: tool.left
                }}
                initial={{ opacity: 0, scale: 0.8, y: 20 }}
                whileInView={{ opacity: 1, scale: 1, y: 0 }}
                viewport={{ once: false, margin: "-100px" }}
                transition={{ duration: 0.6, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
                onClick={() => navigate(tool.path)}
              >
                <div className="node-content">
                  <div className="node-icon">
                    <Icon size={24} />
                  </div>
                  <div className="node-info">
                    <div className="node-label">{tool.title}</div>
                    <div className="node-description">{tool.description}</div>
                  </div>
                </div>
              </motion.div>
            );
          })}

          {/* Current Position Marker - Traveling Pulse */}
          <motion.div
            className="journey-marker"
            style={{
              offsetPath: "path('M 50,0 C 30,10 20,15 20,20 S 40,25 50,30 S 80,35 80,40 S 60,45 50,50 S 20,55 20,60 S 40,65 50,70 S 80,75 80,80 S 60,85 50,90 S 40,95 50,100')",
              offsetDistance: useTransform(scrollYProgress, [0, 1], ['0%', '100%'])
            }}
          >
            <div className="marker-dot" />
          </motion.div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
