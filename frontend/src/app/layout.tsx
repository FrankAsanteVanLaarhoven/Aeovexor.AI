import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AEOVEXOR Studio — Precision 3D Geometry & Spatial Perception",
  description: "Next.js 15 Modular 3D Spatial Intelligence platform accelerated by C++, Rust, and Go microservices.",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased select-none bg-[#05070B] text-slate-100">
        {children}
      </body>
    </html>
  );
}
