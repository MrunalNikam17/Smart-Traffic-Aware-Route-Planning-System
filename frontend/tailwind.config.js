module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx}",
    "./src/components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        traffic: {
          light: "#4ade80",
          normal: "#facc15",
          heavy: "#f97316",
          congestion: "#ef4444",
        },
      },
    },
  },
  plugins: [],
}
