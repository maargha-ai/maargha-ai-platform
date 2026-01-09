import { useState, useEffect } from 'react';
import { useTheme } from './ThemeProvider';
import { Moon, Sun, Monitor, Menu, X, ChevronRight } from 'lucide-react';
import { Button } from './ui/button';

export default function PremiumNavbar() {
  const { theme, setTheme } = useTheme();
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

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
          ? 'bg-background/80 backdrop-blur-md border-b border-white/10 shadow-sm'
          : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-2 font-bold text-xl tracking-tighter">
          <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-primary-foreground">
            M
          </div>
          <span>MAARGHA.AI</span>
        </div>

        {/* Desktop Links */}
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

        {/* Actions */}
        <div className="hidden md:flex items-center gap-4">
          <ThemeToggle theme={theme} setTheme={setTheme} />
          <Button variant="default" className="rounded-full px-6 shadow-lg shadow-primary/20 hover:shadow-primary/40 transition-all">
            Get Started
          </Button>
        </div>

        {/* Mobile Toggle */}
        <button
          className="md:hidden text-foreground"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden absolute top-16 left-0 right-0 bg-background border-b border-border p-6 flex flex-col gap-4 animate-in slide-in-from-top-4">
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
          <Button className="w-full mt-4 rounded-full">Get Started</Button>
        </div>
      )}
    </nav>
  );
}

function ThemeToggle({ theme, setTheme }) {
  const cycleTheme = () => {
    if (theme === 'light') setTheme('dark');
    else if (theme === 'dark') setTheme('system');
    else setTheme('light');
  };

  return (
    <button
      onClick={cycleTheme}
      className="p-2 rounded-full hover:bg-secondary transition-colors relative"
      aria-label="Toggle theme"
    >
      <div className="relative w-5 h-5">
        <Sun
          className={`absolute inset-0 transition-all duration-300 ${
            theme === 'light' ? 'rotate-0 scale-100' : '-rotate-90 scale-0 opacity-0'
          }`}
        />
        <Moon
          className={`absolute inset-0 transition-all duration-300 ${
            theme === 'dark' ? 'rotate-0 scale-100' : 'rotate-90 scale-0 opacity-0'
          }`}
        />
        <Monitor
          className={`absolute inset-0 transition-all duration-300 ${
            theme === 'system' ? 'rotate-0 scale-100' : 'rotate-90 scale-0 opacity-0'
          }`}
        />
      </div>
    </button>
  );
}
