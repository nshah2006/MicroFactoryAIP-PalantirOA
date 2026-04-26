import type { Config } from "tailwindcss";

export default {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0B0F14",
        panel: "#111827",
        elevated: "#162033",
        border: "#263244",
        primary: "#3B82F6",
        warning: "#F59E0B",
        critical: "#EF4444",
        success: "#22C55E",
        text: "#E5E7EB",
        muted: "#94A3B8"
      }
    }
  },
  plugins: []
} satisfies Config;
