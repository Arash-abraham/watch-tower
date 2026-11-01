/** @type {import('tailwindcss').Config} */
import plugin from 'tailwindcss/plugin'

export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          'Inter',
          'ui-sans-serif',
          'system-ui',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'sans-serif',
        ],
        mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Consolas', 'monospace'],
      },
      colors: {
        tower: {
          900: '#04070a',
          800: '#070b10',
          700: '#0b1117',
        },
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(34, 211, 238, 0.18), 0 20px 60px -20px rgba(34, 211, 238, 0.35)',
        'glow-sm': '0 10px 30px -15px rgba(34, 211, 238, 0.5)',
        panel: '0 1px 0 0 rgba(255, 255, 255, 0.04) inset, 0 24px 60px -30px rgba(0, 0, 0, 0.9)',
      },
      keyframes: {
        scanX: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        scanY: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' },
        },
        floatY: {
          '0%, 100%': { transform: 'translate3d(0, 0, 0)', opacity: '0.25' },
          '50%': { transform: 'translate3d(0, -18px, 0)', opacity: '0.75' },
        },
        glowPulse: {
          '0%, 100%': { opacity: '0.35', transform: 'scale(1)' },
          '50%': { opacity: '0.6', transform: 'scale(1.04)' },
        },
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        modalIn: {
          '0%': { opacity: '0', transform: 'scale(0.96) translateY(-12px)' },
          '100%': { opacity: '1', transform: 'scale(1) translateY(0)' },
        },
        progressBar: {
          '0%': { width: '0%' },
          '100%': { width: '65%' },
        },
        radar: {
          to: { transform: 'rotate(360deg)' },
        },
        blip: {
          '0%': { opacity: '0', transform: 'scale(0.4)' },
          '30%': { opacity: '1', transform: 'scale(1)' },
          '100%': { opacity: '0', transform: 'scale(1.6)' },
        },
        marquee: {
          '0%, 12%': { transform: 'translateY(0)' },
          '25%, 37%': { transform: 'translateY(-100%)' },
          '50%, 62%': { transform: 'translateY(-200%)' },
          '75%, 87%': { transform: 'translateY(-300%)' },
          '100%': { transform: 'translateY(-300%)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        gradientShift: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
      },
      animation: {
        'scan-x': 'scanX 9s linear infinite',
        'scan-y': 'scanY 12s linear infinite',
        'float-y': 'floatY 9s ease-in-out infinite',
        'glow-pulse': 'glowPulse 7s ease-in-out infinite',
        'fade-up': 'fadeUp 0.6s ease-out both',
        'modal-in': 'modalIn 0.25s ease-out',
        'progress-bar': 'progressBar 1.5s ease-out forwards',
        gradient: 'gradientShift 6s ease infinite',
        radar: 'radar 6s linear infinite',
        blip: 'blip 3s ease-out infinite',
        marquee: 'marquee 12s ease-in-out infinite',
        shimmer: 'shimmer 3.5s linear infinite',
      },
    },
  },
  plugins: [
    plugin(({ addVariant }) => {
      addVariant('hocus', ['&:hover', '&:focus-visible'])
    }),
  ],
}
