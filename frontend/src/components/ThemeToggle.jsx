import { Moon, Sun } from 'lucide-react';

export function ThemeToggle({ theme, setTheme }) {
  const toggleTheme = () => {
    if (theme === 'dark') {
      setTheme('light');
    } else {
      setTheme('dark');
    }
  };

  return (
    <button
      onClick={toggleTheme}
      className="w-10 h-10 rounded-full hover:bg-secondary transition-colors flex items-center justify-center"
      aria-label="Toggle theme"
    >
      <div className="relative w-5 h-5 flex items-center justify-center">
        <Sun
          size={20}
          className={`absolute transition-all duration-300 ${
            theme === "light"
              ? "rotate-0 scale-100"
              : "-rotate-90 scale-0 opacity-0"
          }`}
        />
        <Moon
          size={20}
          className={`absolute transition-all duration-300 ${
            theme === "dark"
              ? "rotate-0 scale-100"
              : "rotate-90 scale-0 opacity-0"
          }`}
        />
      </div>
    </button>
  );
}
