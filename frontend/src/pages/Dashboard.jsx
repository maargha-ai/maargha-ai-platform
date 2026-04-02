import React, { useRef, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, useScroll, useTransform, AnimatePresence } from 'framer-motion';
import { BrainCircuit } from "lucide-react";
import { Map } from "lucide-react";
import { Compass } from "lucide-react";
import { Route } from "lucide-react";
import { Flag } from "lucide-react";
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
  Settings,
  FileUser,
  Layout,
  FileSearch
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../components/ThemeProvider';
import { ThemeToggle } from '../components/ThemeToggle';
import UserProfileModal from '../components/UserProfileModal.jsx';

import '../styles/landscape-dashboard.css';
import "../styles/dashboard.css";
import "../styles/register.css";

const features = [
  { title: "Career Finder", desc: "Discover careers that match your interests and skills.", route: "/career" },
  { title: "AI Roadmap Generator", desc: "Personalized learning paths for your goals.", route: "/roadmap" },
  { title: "AI Tutor", desc: "Ask doubts and learn interactively.", route: "/tutor" },
  { title: "Quiz Generator", desc: "Test yourself with smart quizzes.", route: "/quiz" },
  { title: "Resume Parser", desc: "AI-powered resume analysis and skill extraction.", route: "/resume-parser" },
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
  const scrollContainerRef = useRef(null);
  const [markerPos, setMarkerPos] = useState({ x: 50, y: 10 });
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);

  useEffect(() => {
    // scrollContainerRef.current = document.getElementById('root');
  }, []);

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
      top: '7.5%',
      left: '50%'
    },
    {
      id: 'career',
      title: 'Career Discovery',
      description: 'Analyze your aptitudes and map your professional trajectory.',
      icon: Search,
      path: '/career',
      top: '18.9%',
      left: '20%'
    },
    {
      id: 'roadmap',
      title: 'Career Path Intelligence',
      description: 'Clear learning roadmap with skills, tools, and projects.',
      icon: Route,
      path: '/roadmap',
      top: '23.4%',
      left: '51%'
    },
    {
      id: 'ai-tutor',
      title: 'Knowledge Mastery Engine',
      description: 'Structured AI tutoring for true concept mastery.',
      icon: BrainCircuit,
      path: '/tutor',
      top: '31.3%',
      left: '77%'
    },
    {
      id: 'quiz',
      title: 'Technical Assessment',
      description: 'Validate your competency through AI-driven evaluation engines.',
      icon: Trophy,
      path: '/quiz',
      top: '33.2%',
      left: '42%'
    },
    {
      id: 'news',
      title: 'Tech Pulse Digest',
      description: 'Real-time industry shifts and curated tech insights.',
      icon: Newspaper,
      path: '/news',
      top: '41.6%',
      left: '21%'
    },
    {
      id: 'cv-architect',
      title: 'AI CV Architect',
      description: 'Engineered resumes optimized for ATS and human psychology.',
      icon: FileUser,
      path: '/cv',
      top: '46.8%',
      left: '53%'
    },
    {
      id: 'linkedin',
      title: 'LinkedIn Growth AI',
      description: 'Maximize your profile impact and build high-value connections.',
      icon: Zap,
      path: '/linkedin',
      top: '56.3%',
      left: '51%'
    },
    {
      id: 'resume-parser',
      title: 'Resume Intelligence Engine',
      description: 'Deep resume analysis to extract skills, roles, and career signals using AI.',
      icon: FileSearch,
      path: '/resume-parser',
      top: '58.2%',
      left: '23%'
    },
    {
      id: 'networking',
      title: 'Global Tech Events',
      description: 'Real-time networking, hackathons, and virtual summits.',
      icon: Users,
      path: '/networking-events',
      top: '67.9%',
      left: '40%'
    },
    {
      id: 'music',
      title: 'Sonic Therapy',
      description: 'AI-composed soundscapes for deep focus and mental clarity.',
      icon: Music,
      path: '/music',
      top: '78.5%',
      left: '50%'
    },
    {
      id: 'wellness',
      title: 'Empathetic AI',
      description: 'Your conversational companion for emotional support and wellness.',
      icon: Heart,
      path: '/emotional-support',
      top: '86%',
      left: '36%'
    },
    {
      id: 'jobs',
      title: 'AI Job Architect',
      description: 'Strategic role placement and matching based on your unique profile.',
      icon: Briefcase,
      path: '/jobs',
      top: '96%',
      left: '60%'
    }
  ];
  return (
    <div className={`professional-dashboard ${theme}`}>
      <div className="header-brand">
        <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-primary-foreground">
          M
        </div>
        <span>MAARGHA AI</span>
      </div>
      <div className="map-canvas" ref={containerRef}>
        <div className="map-content-wrapper">
          <svg className="connection-spine-svg" viewBox="0 0 100 132" preserveAspectRatio="none">
            <defs>
              <linearGradient id="activeGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="currentColor" stopOpacity="0.2" />
                <stop offset="100%" stopColor="currentColor" stopOpacity="1" />
              </linearGradient>
            </defs>
            <path
              className="spine-path-bg"
              d="M 50,10 
              C 55,18 20,17 20,25 
              C 19,34 72,31 79,39 
              C 85,49 35,47 23,53 
              C 10,63 68,62 77,71 
              C 85,82 32,77 24,85 
              C 13,95 70,92 76,100 
              C 80,109 35,107 35,115 
              C 35,123 65,122 65,130"
            />
            <motion.path
              className="spine-path-active"
              d="M 50,10 
              C 55,18 20,17 20,25 
              C 19,34 72,31 79,39 
              C 85,49 35,47 23,53 
              C 10,63 68,62 77,71 
              C 85,82 32,77 24,85 
              C 13,95 70,92 76,100 
              C 80,109 35,107 35,115 
              C 35,123 65,122 65,130"
              style={{ pathLength: scrollYProgress }}
            />
            <path
              ref={pathRef}
              d="M 50,10 
              C 55,18 20,17 20,25 
              C 19,34 72,31 79,39 
              C 85,49 35,47 23,53 
              C 10,63 68,62 77,71 
              C 85,82 32,77 24,85 
              C 13,95 70,92 76,100 
              C 80,109 35,107 35,115 
              C 35,123 65,122 65,130"
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
                viewport={{ once: true, margin: "0px" }}
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
        </div>
      </div>
      <div className="dashboard-hud">
        <div className="hud-profile" onClick={() => setIsProfileModalOpen(true)}>
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

      <AnimatePresence>
        {isProfileModalOpen && (
          <UserProfileModal 
            isOpen={isProfileModalOpen} 
            onClose={() => setIsProfileModalOpen(false)} 
          />
        )}
      </AnimatePresence>
    </div>
  );
};


