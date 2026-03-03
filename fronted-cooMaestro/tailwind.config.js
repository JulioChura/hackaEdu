/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Morado principal
        'primary': '#5447e6',
        'primary-dark': '#3d35b8',
        
        // Accent
        'accent': '#FFD700',
        
        // Texto
        'charcoal': '#333333',
        'slate-text': '#638288',
        'medium-gray': '#888888',
        
        // Fondos
        'background-light': '#f6f6f8',
        'background-dark': '#242428',
        'background-subtle': '#F2F5F7',
      },
      fontFamily: {
        'display': ['Lexend', 'sans-serif']
      },
      borderRadius: {
        'DEFAULT': '0.5rem',
        'lg': '1rem',
        'xl': '1.5rem',
        'full': '9999px'
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
}

