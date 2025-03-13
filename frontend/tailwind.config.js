// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        beige: {
          50: "#f9f7f4",
          100: "#f1ece3",
          200: "#e6ddcd",
          300: "#d8c9b1",
          400: "#c7b393",
          500: "#b69c76",
          600: "#a68b67",
          700: "#8c7357",
          800: "#735f49",
          900: "#5f4f3e",
          950: "#302720",
        },
        charcoal: {
          50: "#f6f7f7",
          100: "#e0e5e7",
          200: "#c2ccd1",
          300: "#9baab3",
          400: "#738592",
          500: "#586a79",
          600: "#455561",
          700: "#3a4550",
          800: "#2f3842",
          900: "#1e2630",
          950: "#111821",
        },
      },
    },
  },
  plugins: [],
};
