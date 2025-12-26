/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/pages/**/*.{js,jsx,ts,tsx}",
    "./src/components/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        industrial: {
          900: '#0f1117',
          800: '#1a1d2a',
          700: '#252936',
          600: '#2d3748',
          500: '#4a5568',
          accent: '#00d4ff',
          warning: '#ff6b00',
        }
      },
      fontFamily: {
        mono: ['"Courier New"', 'monospace'],
        display: ['"Rajdhani"', 'sans-serif'],
      },
      animation: {
        'spin-slow': 'spin 3s linear infinite',
        'pulse-glow': 'pulseGlow 2s infinite',
        'glitch': 'glitch 1s linear infinite',
      },
      keyframes: {
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 5px #00d4ff' },
          '50%': { boxShadow: '0 0 20px #00d4ff, 0 0 30px #00d4ff' },
        },
        glitch: {
          '0%': { textShadow: '2px 2px #ff00ff, -2px -2px #00ffff' },
          '25%': { textShadow: '-2px -2px #ff00ff, 2px 2px #00ffff' },
          '50%': { textShadow: '2px -2px #ff00ff, -2px 2px #00ffff' },
          '100%': { textShadow: '-2px 2px #ff00ff, 2px -2px #00ffff' },
        }
      }
    },
  },
  plugins: [],
}