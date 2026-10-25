import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          primary: "#05070B",
          secondary: "#0B0F17",
          card: "#0F1523",
          hover: "rgba(0, 229, 255, 0.08)",
        },
        cyan: {
          DEFAULT: "#00E5FF",
          dim: "rgba(0, 229, 255, 0.12)",
          glow: "rgba(0, 229, 255, 0.35)",
        },
        rose: {
          DEFAULT: "#EF4444",
          dim: "rgba(239, 68, 68, 0.15)",
        },
        amber: {
          DEFAULT: "#F59E0B",
          dim: "rgba(245, 158, 11, 0.15)",
        },
        emerald: {
          DEFAULT: "#10B981",
          dim: "rgba(16, 185, 129, 0.15)",
        },
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
    },
  },
  plugins: [],
};
export default config;
