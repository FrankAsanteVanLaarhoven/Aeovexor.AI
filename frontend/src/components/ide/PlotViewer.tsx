"use client";

import React from "react";

interface PlotViewerProps {
  plotB64: string | null;
  metrics: Record<string, any>;
  seriesData?: any[];
}

export default function PlotViewer({ plotB64, metrics, seriesData }: PlotViewerProps) {
  const metricEntries = Object.entries(metrics || {});

  return (
    <div className="flex flex-col h-full bg-[#05070B] border-l border-white/10 font-mono text-xs overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-1.5 bg-[#090D15] border-b border-white/10 text-slate-400 select-none">
        <span className="font-bold text-slate-300 text-[10px] tracking-wider uppercase">SCIENTIFIC PLOTS & METRICS</span>
        {metricEntries.length > 0 && (
          <span className="text-[10px] text-cyan">{metricEntries.length} METRICS EXTRACTED</span>
        )}
      </div>

      <div className="flex-1 p-3 overflow-y-auto flex flex-col gap-3">
        {/* Rendered Matplotlib Base64 Image */}
        {plotB64 ? (
          <div className="rounded-lg border border-white/10 bg-black/50 p-2 flex items-center justify-center shadow-lg">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={`data:image/png;base64,${plotB64}`}
              alt="Scientific Output Plot"
              className="max-w-full max-h-[280px] object-contain rounded"
            />
          </div>
        ) : (
          <div className="h-44 border border-dashed border-white/10 rounded-lg flex flex-col items-center justify-center text-slate-500 text-center p-4">
            <svg className="w-8 h-8 mb-2 opacity-40 text-cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
            </svg>
            <div>Execute a script with `plt.show()` or generate metrics to view scientific figures here.</div>
          </div>
        )}

        {/* Metric Cards Grid */}
        {metricEntries.length > 0 && (
          <div className="flex flex-col gap-1.5">
            <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">TELEMETRY & DESCRIPTIVE STATS</div>
            <div className="grid grid-cols-2 gap-2">
              {metricEntries.map(([key, val]) => (
                <div key={key} className="p-2 rounded bg-white/5 border border-white/10 flex flex-col">
                  <span className="text-[10px] text-slate-400 truncate">{key}</span>
                  <span className="text-cyan font-bold text-xs truncate">
                    {typeof val === "number" ? val.toFixed(4) : String(val)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
