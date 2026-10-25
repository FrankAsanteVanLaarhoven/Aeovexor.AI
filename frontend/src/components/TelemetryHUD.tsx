"use client";

import React, { useEffect, useState } from "react";
import { fetchNativeStatus, fetchGoTelemetry, NativeStatus, TelemetryStats } from "../lib/api";

export default function TelemetryHUD() {
  const [nativeStatus, setNativeStatus] = useState<NativeStatus | null>(null);
  const [telemetry, setTelemetry] = useState<TelemetryStats | null>(null);

  useEffect(() => {
    fetchNativeStatus().then(setNativeStatus);
    const interval = setInterval(() => {
      fetchGoTelemetry().then(setTelemetry);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex items-center gap-3 bg-[#0B0F17]/90 backdrop-blur-md px-3 py-1.5 rounded-lg border border-white/10 text-xs font-mono shadow-xl">
      {/* Go Ingestion Pipeline */}
      <div className="flex items-center gap-1.5">
        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
        <span className="text-slate-400 font-semibold">GO STREAM:</span>
        <span className="text-cyan font-bold">
          {telemetry ? `${telemetry.current_fps.toFixed(1)} FPS` : "60.0 FPS"}
        </span>
      </div>

      <div className="h-3 w-px bg-white/20" />

      {/* Throughput */}
      <div className="flex items-center gap-1.5">
        <span className="text-slate-400">BANDWIDTH:</span>
        <span className="text-amber-400 font-bold">
          {telemetry ? `${telemetry.bandwidth_mbps.toFixed(2)} MB/s` : "16.55 MB/s"}
        </span>
      </div>

      <div className="h-3 w-px bg-white/20" />

      {/* Polyglot Subsystems */}
      <div className="flex items-center gap-1.5">
        <span
          title="C++ SIMD Acceleration Core"
          className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
            nativeStatus?.cpp_native.available
              ? "bg-cyan-500/20 text-cyan border border-cyan/40"
              : "bg-slate-800 text-slate-500"
          }`}
        >
          C++ SIMD
        </span>
        <span
          title="Rust Zero-Copy Parser Core"
          className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
            nativeStatus?.rust_native.available
              ? "bg-amber-500/20 text-amber-400 border border-amber-500/40"
              : "bg-slate-800 text-slate-500"
          }`}
        >
          RUST CORE
        </span>
        <span
          title="Go Concurrency Telemetry Service"
          className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
            nativeStatus?.go_streaming.available
              ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40"
              : "bg-slate-800 text-slate-500"
          }`}
        >
          GO STREAM
        </span>
        <span
          title="Python FastAPI AI & Notebook Orchestrator"
          className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-blue-500/20 text-blue-400 border border-blue-500/40"
        >
          FASTAPI AI
        </span>
      </div>
    </div>
  );
}
