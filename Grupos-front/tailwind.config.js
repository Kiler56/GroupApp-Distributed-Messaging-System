/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./modulos/**/*.{js,ts,jsx,tsx}",
    "./core/**/*.{js,ts,jsx,tsx}",
    "./index.html", // Si tienes un index.html en la raíz de frontend
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
