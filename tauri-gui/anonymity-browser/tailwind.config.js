/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Neon colors - Cyberpunk accents
        neon: {
          cyan: '#00FFFF',
          purple: '#9201CB',
          pink: '#F715AB',
          blue: '#0313A6',
          green: '#39FF14',
        },
        // Dark colors - Professional base
        dark: {
          bg: '#0A0E27',
          darker: '#070F34',
          charcoal: '#1A1F3A',
          slate: '#2D3250',
        },
        // Text colors
        text: {
          primary: '#E8E9ED',
          secondary: '#A0A3BD',
          muted: '#6B7280',
        },
      },
      fontFamily: {
        heading: ['Orbitron', 'Rajdhani', 'sans-serif'],
        body: ['Inter', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      boxShadow: {
        'glow-cyan': '0 0 20px rgba(0, 255, 255, 0.5)',
        'glow-purple': '0 0 20px rgba(146, 1, 203, 0.5)',
        'glow-pink': '0 0 20px rgba(247, 21, 171, 0.5)',
        'glow-green': '0 0 20px rgba(57, 255, 20, 0.5)',
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'slide-up': 'slide-up 0.3s ease-out',
        'fade-in': 'fade-in 0.2s ease-in',
      },
      keyframes: {
        'pulse-glow': {
          '0%, 100%': { boxShadow: '0 0 20px rgba(0, 255, 255, 0.5)' },
          '50%': { boxShadow: '0 0 40px rgba(0, 255, 255, 0.8)' },
        },
        'slide-up': {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}

