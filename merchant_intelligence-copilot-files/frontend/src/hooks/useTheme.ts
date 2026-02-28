import { useEffect, useState } from 'react';

export type Theme = 'dark' | 'light' | 'gradient-dark' | 'glassmorphism' | 'minimal';

export function useTheme() {
  const [theme, setTheme] = useState<Theme>(() => {
    const stored = localStorage.getItem('theme') as Theme;
    if (['dark', 'light', 'gradient-dark', 'glassmorphism', 'minimal'].includes(stored)) {
      return stored;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  });

  useEffect(() => {
    const root = document.documentElement;
    
    // Remove all theme classes
    root.classList.remove('dark', 'light', 'gradient-dark', 'glassmorphism', 'minimal');
    
    // Add current theme class
    root.classList.add(theme);
    
    // For dark mode compatibility
    if (theme === 'dark' || theme === 'gradient-dark' || theme === 'glassmorphism') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => {
      const themes: Theme[] = ['light', 'dark', 'gradient-dark', 'glassmorphism', 'minimal'];
      const currentIndex = themes.indexOf(prev);
      return themes[(currentIndex + 1) % themes.length];
    });
  };

  return { theme, setTheme, toggleTheme };
}
