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
        cyber: {
          bg: '#0a0e17',
          surface: '#111827',
          surfaceHover: '#1f2937',
          card: '#0f172a',
          cardBorder: '#1e293b',
          cyan: '#06b6d4',
          cyanGlow: 'rgba(6, 182, 212, 0.15)',
          teal: '#14b8a6',
          low: '#10b981',
          lowGlow: 'rgba(16, 185, 129, 0.15)',
          medium: '#f59e0b',
          mediumGlow: 'rgba(245, 158, 11, 0.15)',
          high: '#ef4444',
          highGlow: 'rgba(239, 68, 68, 0.15)',
          muted: '#94a3b8',
          text: '#f8fafc',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Courier New', 'monospace'],
      }
    },
  },
  plugins: [],
}
