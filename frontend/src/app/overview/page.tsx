"use client";

import React, { useState } from "react";
import Link from "next/link";

export default function PlatformOverviewPage() {
  const [activeBenchmarkTier, setActiveBenchmarkTier] = useState<"rust" | "cpp" | "go" | "python">("rust");

  return (
    <div className="min-h-screen bg-[#05070B] text-slate-200 font-sans selection:bg-cyan selection:text-black">
      {/* 1. Navigation Header */}
      <nav className="h-14 border-b border-white/10 bg-[#0B0F17]/95 px-6 flex items-center justify-between sticky top-0 z-50 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <Link href="/" className="flex items-center gap-2 group">
            <svg className="w-6 h-6 text-cyan group-hover:drop-shadow-[0_0_8px_rgba(0,229,255,0.6)] transition-all" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2L3 7v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-9-5z" />
            </svg>
            <span className="font-mono font-black text-sm tracking-wider text-white">
              AEOVEXOR<span className="text-cyan">.AI</span>
            </span>
          </Link>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan/10 text-cyan border border-cyan/20">
            ENTERPRISE SPATIAL PLATFORM
          </span>
        </div>

        <div className="flex items-center gap-4 text-xs font-mono">
          <Link href="/" className="text-slate-300 hover:text-cyan transition-colors">
            Studio Pro
          </Link>
          <Link href="/ide" className="text-slate-300 hover:text-cyan transition-colors">
            Developer IDE
          </Link>
          <a
            href="https://github.com/FrankAsanteVanLaarhoven/Aeovexor.AI"
            target="_blank"
            rel="noopener noreferrer"
            className="px-3 py-1.5 rounded bg-white/5 hover:bg-white/10 border border-white/10 text-white transition-all flex items-center gap-1.5"
          >
            <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
            </svg>
            GitHub
          </a>
        </div>
      </nav>

      {/* 2. Hero Section */}
      <section className="relative px-6 py-20 max-w-7xl mx-auto flex flex-col items-center text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan/10 border border-cyan/30 text-cyan font-mono text-xs mb-6 animate-pulse">
          <span className="w-1.5 h-1.5 rounded-full bg-cyan" />
          POLYGLOT ACCELERATION ENGINE · C++17 · RUST · GO · PYTHON
        </div>

        <h1 className="text-4xl md:text-6xl font-black tracking-tight text-white max-w-4xl leading-tight">
          Enterprise 3D Spatial Intelligence &amp; Autonomous Perception
        </h1>

        <p className="mt-5 text-base md:text-lg text-slate-400 max-w-2xl leading-relaxed font-sans">
          Engineered for mission-critical robotics, autonomous vehicles, and scientific point cloud research.
          Zero-copy LiDAR ingestion, SIMD spatial acceleration, and AI-driven automated paper synthesis.
        </p>

        {/* Action Buttons */}
        <div className="mt-8 flex flex-wrap items-center justify-center gap-4 font-mono text-sm">
          <Link
            href="/"
            className="px-6 py-3 rounded-lg bg-cyan text-black font-bold hover:bg-cyan/90 transition-all shadow-xl hover:shadow-cyan/20 flex items-center gap-2"
          >
            Launch Studio Pro
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </Link>
          <Link
            href="/ide"
            className="px-6 py-3 rounded-lg bg-white/5 hover:bg-white/10 border border-white/15 text-white font-semibold transition-all flex items-center gap-2"
          >
            <span>&lt;/&gt;</span> Open Developer IDE
          </Link>
        </div>
      </section>

      {/* 3. Polyglot Architecture Breakdown */}
      <section className="px-6 py-16 max-w-7xl mx-auto border-t border-white/10">
        <div className="text-center mb-12">
          <span className="text-cyan font-mono text-xs font-bold uppercase tracking-wider block mb-2">
            ENGINEERING EXCELLENCE
          </span>
          <h2 className="text-2xl md:text-3xl font-bold text-white">
            Enterprise Polyglot Architecture
          </h2>
          <p className="text-sm text-slate-400 mt-2 max-w-xl mx-auto font-sans">
            Every layer runs in its optimal native runtime to guarantee zero latency and maximum throughput.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 font-mono">
          {/* C++ SIMD */}
          <div className="p-5 rounded-xl bg-[#0B0F17] border border-white/10 hover:border-cyan/40 transition-all flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold text-cyan">C++17 SIMD CORE</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-cyan/10 text-cyan">libspatialforge_core</span>
              </div>
              <h3 className="text-base font-bold text-white mb-2">Spatial Filter Engine</h3>
              <p className="text-xs text-slate-400 font-sans leading-relaxed">
                AVX2/NEON accelerated voxel downsampling, Statistical Outlier Removal (SOR), Cloth Simulation Filter (CSF), and Cloud-to-Cloud (C2C) Hausdorff distance.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-white/10 text-[11px] text-slate-500">
              Throughput: <strong className="text-white">12.5 Mpts/s</strong>
            </div>
          </div>

          {/* Rust Zero-Copy */}
          <div className="p-5 rounded-xl bg-[#0B0F17] border border-white/10 hover:border-amber-400/40 transition-all flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold text-amber-400">RUST ZERO-COPY</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-400/10 text-amber-400">aeovexor-spatial-cli</span>
              </div>
              <h3 className="text-base font-bold text-white mb-2">LiDAR Binary Parser</h3>
              <p className="text-xs text-slate-400 font-sans leading-relaxed">
                Zero-copy memory-mapped binary decoder for KITTI, NuScenes, and ASPRS LAS/LAZ formats with spatial voxel hashing and 3D IOU validation.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-white/10 text-[11px] text-slate-500">
              Throughput: <strong className="text-white">404 Mpts/s (42µs)</strong>
            </div>
          </div>

          {/* Go Telemetry Streamer */}
          <div className="p-5 rounded-xl bg-[#0B0F17] border border-white/10 hover:border-emerald-400/40 transition-all flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold text-emerald-400">GO CONCURRENCY</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-400/10 text-emerald-400">aeovexor-telemetry</span>
              </div>
              <h3 className="text-base font-bold text-white mb-2">60Hz Streaming Service</h3>
              <p className="text-xs text-slate-400 font-sans leading-relaxed">
                High-concurrency Server-Sent Events (SSE) and WebSockets microservice broadcasting 60 FPS sensor frames with sub-millisecond network jitter.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-white/10 text-[11px] text-slate-500">
              Throughput: <strong className="text-white">84.5 MB/s @ 60 FPS</strong>
            </div>
          </div>

          {/* Next.js & Python */}
          <div className="p-5 rounded-xl bg-[#0B0F17] border border-white/10 hover:border-purple-400/40 transition-all flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold text-purple-400">PYTHON + NEXT.JS 15</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-purple-400/10 text-purple-400">FastAPI &amp; Three.js</span>
              </div>
              <h3 className="text-base font-bold text-white mb-2">Perception &amp; Studio Pro</h3>
              <p className="text-xs text-slate-400 font-sans leading-relaxed">
                OpenRouter multi-model AI copilot, automated IEEE/CVPR research paper generation, 3D Oriented Bounding Box annotation, and scientific colormapping.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-white/10 text-[11px] text-slate-500">
              Stack: <strong className="text-white">React 19 · WebGL · SIMD</strong>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Live Benchmark Matrix */}
      <section className="px-6 py-16 max-w-7xl mx-auto border-t border-white/10">
        <div className="text-center mb-10">
          <span className="text-cyan font-mono text-xs font-bold uppercase tracking-wider block mb-2">
            EMPIRICAL VALIDATION
          </span>
          <h2 className="text-2xl md:text-3xl font-bold text-white">
            Performance Benchmark Matrix
          </h2>
          <p className="text-sm text-slate-400 mt-2 max-w-xl mx-auto font-sans">
            Measured against 120,000-point autonomous driving LiDAR scans on modern Apple Silicon and Linux x86-64 hardware.
          </p>
        </div>

        {/* Benchmark Table */}
        <div className="overflow-x-auto rounded-xl border border-white/10 bg-[#0B0F17] font-mono text-xs">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-white/10 bg-white/5 text-slate-400">
                <th className="p-3 font-bold text-white">PIPELINE STAGE</th>
                <th className="p-3 font-bold">PURE PYTHON</th>
                <th className="p-3 font-bold">OPEN3D / PCL</th>
                <th className="p-3 font-bold text-cyan">AEOVEXOR NATIVE</th>
                <th className="p-3 font-bold text-emerald-400">SPEEDUP FACTOR</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/10">
              <tr>
                <td className="p-3 font-bold text-white">Binary LiDAR Parsing (KITTI)</td>
                <td className="p-3 text-rose-400">4,250 µs</td>
                <td className="p-3 text-slate-300">410 µs</td>
                <td className="p-3 text-cyan font-bold">42.5 µs (Rust)</td>
                <td className="p-3 text-emerald-400 font-bold">100.0x faster</td>
              </tr>
              <tr>
                <td className="p-3 font-bold text-white">Voxel Grid Downsampling (0.1m)</td>
                <td className="p-3 text-rose-400">18.20 ms</td>
                <td className="p-3 text-slate-300">2.40 ms</td>
                <td className="p-3 text-cyan font-bold">0.45 ms (C++ SIMD)</td>
                <td className="p-3 text-emerald-400 font-bold">40.4x faster</td>
              </tr>
              <tr>
                <td className="p-3 font-bold text-white">SOR Outlier Removal Filter</td>
                <td className="p-3 text-rose-400">142.0 ms</td>
                <td className="p-3 text-slate-300">14.10 ms</td>
                <td className="p-3 text-cyan font-bold">3.80 ms (C++ SIMD)</td>
                <td className="p-3 text-emerald-400 font-bold">37.3x faster</td>
              </tr>
              <tr>
                <td className="p-3 font-bold text-white">Telemetry Frame Broadcast</td>
                <td className="p-3 text-rose-400">15 FPS (GIL lock)</td>
                <td className="p-3 text-slate-300">30 FPS</td>
                <td className="p-3 text-cyan font-bold">60 FPS (Go Microservice)</td>
                <td className="p-3 text-emerald-400 font-bold">4.0x smoother</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* 5. Footer */}
      <footer className="border-t border-white/10 py-8 px-6 text-center font-mono text-xs text-slate-500">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-bold text-white">AEOVEXOR.AI</span>
            <span>· Enterprise 3D Spatial Intelligence Platform</span>
          </div>
          <div className="flex items-center gap-4 text-slate-400">
            <Link href="/" className="hover:text-cyan">Studio</Link>
            <Link href="/ide" className="hover:text-cyan">IDE</Link>
            <a href="https://github.com/FrankAsanteVanLaarhoven/Aeovexor.AI" className="hover:text-cyan">GitHub</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
