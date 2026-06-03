/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Gaming-inspired dark theme
        'dark-bg': '#0a0a0f',
        'dark-card': '#14141f',
        'dark-border': '#2a2a3a',
        'neon-green': '#10b981',
        'neon-blue': '#3b82f6',
        'neon-purple': '#8b5cf6',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [],
};