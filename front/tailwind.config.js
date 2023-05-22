/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,vue}",
  ],

  theme: {
    extend: {},
  },
  darkMode: 'class',
  plugins: [],
  important: true,
  corePlugins: {
    preflight: false,
  }
}

