import { useState, useEffect } from 'react';
import { useTheme } from './ThemeProvider';
import { Menu, X } from 'lucide-react';
import { Button } from './ui/button';
import { ThemeToggle } from './ThemeToggle';

import { useAuth } from '../context/AuthContext';

export default function PremiumNavbar({ onOpenAuth, onGetStarted }) {
  const { theme, setTheme } = useTheme();
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { name: 'Features', href: '#features' },
    { name: 'How it Works', href: '#how-it-works' },
    { name: 'Career Path', href: '#career-path' },
  ];

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-background/80 backdrop-blur-md border-b border-border shadow-sm'
          : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2 font-bold text-xl tracking-tighter cursor-pointer" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
          <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-primary-foreground">
            M
          </div>
          <span>MAARGHA.AI</span>
        </div>

        <div className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <a
              key={link.name}
              href={link.href}
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
            >
              {link.name}
            </a>
          ))}
        </div>

        <div className="hidden md:flex items-center gap-4">
          <ThemeToggle theme={theme} setTheme={setTheme} />
          <button 
             onClick={onOpenAuth}
             className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
          >
             {isAuthenticated ? "Dashboard" : "Login"}
          </button>
          <Button 
            variant="default" 
            className="rounded-full px-6 shadow-lg shadow-primary/20 hover:shadow-primary/40 transition-all"
            onClick={onGetStarted}
          >
            Get Started
          </Button>
        </div>

        <button
          className="md:hidden text-foreground"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {mobileMenuOpen && (
        <div className="md:hidden absolute top-16 left-0 right-0 bg-background border-b border-border p-6 flex flex-col gap-4 animate-in slide-in-from-top-4 shadow-xl">
          {navLinks.map((link) => (
            <a
              key={link.name}
              href={link.href}
              className="text-lg font-medium py-2 border-b border-border/50"
              onClick={() => setMobileMenuOpen(false)}
            >
              {link.name}
            </a>
          ))}
          <div className="flex items-center justify-between pt-4">
            <span className="text-muted-foreground">Theme</span>
            <ThemeToggle theme={theme} setTheme={setTheme} />
          </div>
          <div className="flex gap-4 mt-4">
             <Button variant="outline" className="flex-1 rounded-full" onClick={() => { setMobileMenuOpen(false); onOpenAuth(); }}>
               {isAuthenticated ? "Dashboard" : "Login"}
             </Button>
             <Button className="flex-1 rounded-full" onClick={() => { setMobileMenuOpen(false); onGetStarted(); }}>Get Started</Button>
          </div>
        </div>
      )}
    </nav>
  );
}

