/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/artikel.html',
    './templates/index.html',
    './templates/about.html',
    './templates/proyek.html',
    './templates/apa.html',
    './templates/posting-artikel.html',
    './templates/detail-artikel.html',
    './static/**/*.{html,js,ts,jsx,tsx}',  
  ],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}