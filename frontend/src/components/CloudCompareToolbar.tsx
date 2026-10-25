"use client";

import React, { useState } from "react";

interface ToolbarProps {
  onSetCameraView: (view: string) => void;
  onToggleOrtho: () => void;
  isOrtho: boolean;
  onTriggerTool: (tool: string) => void;
  activeTool: string | null;
  onToggleRecording: () => void;
  isRecording: boolean;
  onTogglePiP: () => void;
  isPiPActive: boolean;
  onToggleLaser: () => void;
  isLaserActive: boolean;
  onToggleTour: () => void;
  isTourActive: boolean;
  onAddPin: () => void;
}

export default function CloudCompareToolbar({
  onSetCameraView,
  onToggleOrtho,
  isOrtho,
  onTriggerTool,
  activeTool,
  onToggleRecording,
  isRecording,
  onTogglePiP,
  isPiPActive,
  onToggleLaser,
  isLaserActive,
  onToggleTour,
  isTourActive,
  onAddPin,
}: ToolbarProps) {
  return (
    <>
      {/* 1. Left Vertical Standard View & Gizmo Toolbar */}
      <div className="absolute left-3.5 top-14 z-40 flex flex-col gap-1.5 p-1.5 bg-[#0B0F17]/90 backdrop-blur-md border border-white/10 rounded-lg shadow-2xl">
        <button
          onClick={() => onSetCameraView("reset")}
          title="Reset Standard Isometric Overview"
          className="w-8 h-8 flex items-center justify-center rounded text-xs font-mono font-bold bg-white/5 hover:bg-cyan-500/20 hover:text-cyan border border-white/10 transition-all"
        >
          1:1
        </button>
        <button
          onClick={onToggleOrtho}
          title={isOrtho ? "Switch to Perspective Projection" : "Switch to Orthographic Projection"}
          className={`w-8 h-8 flex items-center justify-center rounded text-xs font-mono font-bold transition-all border ${
            isOrtho
              ? "bg-cyan-500/20 text-cyan border-cyan/50"
              : "bg-white/5 hover:bg-cyan-500/20 hover:text-cyan border-white/10 text-slate-300"
          }`}
        >
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polygon points="12 2 2 7 12 12 22 7 12 2" />
            <polyline points="2 17 12 22 22 17" />
            <polyline points="2 12 12 17 22 12" />
          </svg>
        </button>

        <div className="h-px w-full bg-white/10 my-0.5" />

        {["TOP", "FRNT", "BACK", "LEFT", "RGHT", "ISO"].map((view) => (
          <button
            key={view}
            onClick={() => onSetCameraView(view.toLowerCase())}
            title={`${view} Camera View`}
            className="w-8 h-8 flex items-center justify-center rounded text-[10px] font-mono font-bold bg-white/5 hover:bg-cyan-500/20 hover:text-cyan border border-white/10 text-slate-300 transition-all"
          >
            {view}
          </button>
        ))}

        <div className="h-px w-full bg-white/10 my-0.5" />

        {/* Crosshair Coordinate Picker */}
        <button
          onClick={() => onTriggerTool("picker")}
          title="Inspect Point Coordinates (Raycasting)"
          className={`w-8 h-8 flex items-center justify-center rounded text-xs transition-all border ${
            activeTool === "picker"
              ? "bg-cyan-500/20 text-cyan border-cyan/50"
              : "bg-white/5 hover:bg-cyan-500/20 hover:text-cyan border-white/10 text-slate-300"
          }`}
        >
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="9" />
            <line x1="12" y1="3" x2="12" y2="21" />
            <line x1="3" y1="12" x2="21" y2="12" />
          </svg>
        </button>

        {/* 7-DOF Transform Gizmos */}
        <button
          onClick={() => onTriggerTool("gizmo-translate")}
          title="Translate Gizmo (W)"
          className={`w-8 h-8 flex items-center justify-center rounded text-xs transition-all border ${
            activeTool === "gizmo-translate"
              ? "bg-cyan-500/20 text-cyan border-cyan/50"
              : "bg-white/5 hover:bg-cyan-500/20 hover:text-cyan border-white/10 text-slate-300"
          }`}
        >
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="5 9 2 12 5 15" />
            <polyline points="9 5 12 2 15 5" />
            <polyline points="15 19 12 22 9 19" />
            <polyline points="19 9 22 12 19 15" />
            <line x1="2" y1="12" x2="22" y2="12" />
            <line x1="12" y1="2" x2="12" y2="22" />
          </svg>
        </button>
      </div>

      {/* 2. Top Centered CloudCompare Manipulation Toolbar */}
      <div className="absolute left-1/2 -translate-x-1/2 top-3.5 z-40 flex items-center gap-1.5 px-3 py-1.5 bg-[#0B0F17]/90 backdrop-blur-md border border-white/10 rounded-lg shadow-2xl">
        <button
          onClick={() => onTriggerTool("scissors")}
          className={`px-2.5 py-1 rounded text-xs font-mono font-semibold flex items-center gap-1.5 border transition-all ${
            activeTool === "scissors"
              ? "bg-cyan-500/20 text-cyan border-cyan/50"
              : "bg-white/5 hover:bg-cyan-500/10 hover:text-cyan border-white/10 text-slate-300"
          }`}
        >
          <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="6" cy="6" r="3" />
            <circle cx="6" cy="18" r="3" />
            <line x1="20" y1="4" x2="8.12" y2="15.88" />
            <line x1="14.47" y1="14.48" x2="20" y2="20" />
            <line x1="8.12" y1="8.12" x2="12" y2="12" />
          </svg>
          Scissors Crop
        </button>

        <button
          onClick={() => onTriggerTool("slice")}
          className={`px-2.5 py-1 rounded text-xs font-mono font-semibold flex items-center gap-1.5 border transition-all ${
            activeTool === "slice"
              ? "bg-cyan-500/20 text-cyan border-cyan/50"
              : "bg-white/5 hover:bg-cyan-500/10 hover:text-cyan border-white/10 text-slate-300"
          }`}
        >
          <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
          </svg>
          Slicing Box
        </button>

        <button
          onClick={() => onTriggerTool("sor")}
          className="px-2.5 py-1 rounded text-xs font-mono font-semibold flex items-center gap-1.5 border bg-white/5 hover:bg-cyan-500/10 hover:text-cyan border-white/10 text-slate-300 transition-all"
        >
          <svg className="w-3.5 h-3.5 text-cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
          </svg>
          SOR Filter (C++)
        </button>

        <button
          onClick={() => onTriggerTool("subsample")}
          className="px-2.5 py-1 rounded text-xs font-mono font-semibold flex items-center gap-1.5 border bg-white/5 hover:bg-cyan-500/10 hover:text-cyan border-white/10 text-slate-300 transition-all"
        >
          <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="2" />
            <circle cx="12" cy="5" r="2" />
            <circle cx="12" cy="19" r="2" />
          </svg>
          Subsample (SIMD)
        </button>

        <button
          onClick={() => onTriggerTool("csf")}
          className="px-2.5 py-1 rounded text-xs font-mono font-semibold flex items-center gap-1.5 border bg-white/5 hover:bg-emerald-500/10 hover:text-emerald-400 border-white/10 text-slate-300 transition-all"
        >
          <svg className="w-3.5 h-3.5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 20h18L12 4z" />
          </svg>
          CSF Ground
        </button>

        <button
          onClick={() => onTriggerTool("c2c")}
          className="px-2.5 py-1 rounded text-xs font-mono font-semibold flex items-center gap-1.5 border bg-white/5 hover:bg-amber-500/10 hover:text-amber-400 border-white/10 text-slate-300 transition-all"
        >
          <svg className="w-3.5 h-3.5 text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          C2C Heatmap
        </button>
      </div>

      {/* 3. Bottom-Right Presentation & Recording Toolbar */}
      <div className="absolute right-3.5 bottom-12 z-40 flex items-center gap-1.5 p-1.5 bg-[#0B0F17]/90 backdrop-blur-md border border-white/10 rounded-lg shadow-2xl">
        <button
          onClick={onToggleRecording}
          className={`px-3 py-1 rounded text-xs font-mono font-bold flex items-center gap-1.5 border transition-all ${
            isRecording
              ? "bg-rose-500/30 text-rose-400 border-rose-500 animate-pulse"
              : "bg-white/5 hover:bg-rose-500/20 hover:text-rose-400 border-white/10 text-slate-300"
          }`}
        >
          <span className={`w-2 h-2 rounded-full ${isRecording ? "bg-rose-500" : "bg-rose-400"}`} />
          {isRecording ? "Stop Rec" : "Record"}
        </button>

        <button
          onClick={onTogglePiP}
          className={`px-2.5 py-1 rounded text-xs font-mono font-semibold flex items-center gap-1.5 border transition-all ${
            isPiPActive
              ? "bg-cyan-500/20 text-cyan border-cyan/50"
              : "bg-white/5 hover:bg-cyan-500/10 hover:text-cyan border-white/10 text-slate-300"
          }`}
        >
          <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="2" y="3" width="20" height="14" rx="2" />
            <rect x="11" y="9" width="9" height="6" rx="1" />
          </svg>
          PiP View
        </button>

        <button
          onClick={onToggleTour}
          className={`px-2.5 py-1 rounded text-xs font-mono font-semibold flex items-center gap-1.5 border transition-all ${
            isTourActive
              ? "bg-cyan-500/20 text-cyan border-cyan/50"
              : "bg-white/5 hover:bg-cyan-500/10 hover:text-cyan border-white/10 text-slate-300"
          }`}
        >
          <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67" />
          </svg>
          360° Tour
        </button>

        <button
          onClick={onToggleLaser}
          className={`px-2.5 py-1 rounded text-xs font-mono font-semibold flex items-center gap-1.5 border transition-all ${
            isLaserActive
              ? "bg-cyan-500/20 text-cyan border-cyan/50"
              : "bg-white/5 hover:bg-cyan-500/10 hover:text-cyan border-white/10 text-slate-300"
          }`}
        >
          <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="3" />
            <line x1="3" y1="12" x2="6" y2="12" />
            <line x1="18" y1="12" x2="21" y2="12" />
            <line x1="12" y1="3" x2="12" y2="6" />
            <line x1="12" y1="18" x2="12" y2="21" />
          </svg>
          Laser
        </button>

        <button
          onClick={onAddPin}
          className="px-2.5 py-1 rounded text-xs font-mono font-semibold flex items-center gap-1.5 border bg-white/5 hover:bg-cyan-500/10 hover:text-cyan border-white/10 text-slate-300 transition-all"
        >
          <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
            <circle cx="12" cy="10" r="3" />
          </svg>
          Add Pin
        </button>
      </div>
    </>
  );
}
