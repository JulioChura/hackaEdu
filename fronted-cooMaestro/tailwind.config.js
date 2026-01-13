/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Morado principal
        'primary': '#5247e6',
        'primary-dark': '#3d35b8',
        
        // Texto
        'charcoal': '#2C3238',
        'slate-text': '#638288',
        
        // Fondos
        'background-light': '#f6f6f8',
        'background-subtle': '#F2F5F7',
      },
    },
  },
  plugins: [],
}

