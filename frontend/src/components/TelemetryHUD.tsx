"use client";

import React, { useEffect, useState } from "react";
import { fetchGoTelemetry, TelemetryStats } from "../lib/api";

export default function TelemetryHUD() {
  const [telemetry, setTelemetry] = useState<TelemetryStats | null>(null);

  useEffect(() => {
    fetchGoTelemetry().then(setTelemetry);
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
    </div>
  );
}
