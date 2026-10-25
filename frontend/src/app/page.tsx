"use client";

import React, { useState } from "react";
import Viewport3D from "../components/Viewport3D";
import ViewportSplit3D from "../components/ViewportSplit3D";
import CloudCompareToolbar from "../components/CloudCompareToolbar";
import TelemetryHUD from "../components/TelemetryHUD";
import AIResearcherModal from "../components/AIResearcherModal";

export default function StudioPage() {
  const [isOrtho, setIsOrtho] = useState(false);
  const [activeTool, setActiveTool] = useState<string | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isPiPActive, setIsPiPActive] = useState(false);
  const [isLaserActive, setIsLaserActive] = useState(false);
  const [isTourActive, setIsTourActive] = useState(false);
  const [isSplitScreen, setIsSplitScreen] = useState(false);
  const [isResearcherOpen, setIsResearcherOpen] = useState(false);
  const [recordedVideoUrl, setRecordedVideoUrl] = useState<string | null>(null);

  const handleCameraView = (view: string) => {
    console.log("[CAMERA VIEW]", view);
  };

  const handleToolTrigger = (tool: string) => {
    setActiveTool((prev) => (prev === tool ? null : tool));
  };

  const handleStopRecording = (blob: Blob) => {
    const url = URL.createObjectURL(blob);
    setRecordedVideoUrl(url);
    setIsRecording(false);
  };

  return (
    <main className="flex flex-col w-screen h-screen overflow-hidden bg-[#05070B]">
      {/* 1. Header Bar */}
      <header className="h-12 border-b border-white/10 bg-[#0B0F17]/95 px-4 flex items-center justify-between z-30">
        <div className="flex items-center gap-3">
          {/* Branded Logo Shield */}
          <div className="flex items-center gap-2">
            <svg className="w-6 h-6 text-cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2L3 7v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-9-5z" />
            </svg>
            <div className="flex flex-col">
              <span className="font-mono font-black text-xs tracking-wider text-white">
                AEOVEXOR<span className="text-cyan">.AI</span>
              </span>
              <span className="text-[8px] font-mono text-slate-400">STUDIO PRO v2.4</span>
            </div>
          </div>

          <div className="h-4 w-px bg-white/15 mx-1" />

          {/* Active Dataset Pill */}
          <div className="px-2.5 py-1 rounded bg-white/5 border border-white/10 text-xs font-mono text-slate-300">
            velodyne_000008.bin
          </div>

          {/* Split Screen Toggle */}
          <button
            onClick={() => setIsSplitScreen((s) => !s)}
            className={`px-2.5 py-1 rounded text-xs font-mono font-semibold border transition-all ${
              isSplitScreen
                ? "bg-cyan-500/20 text-cyan border-cyan/40"
                : "bg-white/5 text-slate-400 border-white/10 hover:text-white"
            }`}
          >
            {isSplitScreen ? "Split View [A/B] Active" : "Single View"}
          </button>
        </div>

        {/* Center: Live Polyglot Telemetry HUD */}
        <TelemetryHUD />

        {/* Right Controls */}
        <div className="flex items-center gap-2">
          {/* AI / SI Researcher Button */}
          <button
            onClick={() => setIsResearcherOpen(true)}
            className="px-3 py-1 rounded text-xs font-mono font-bold bg-cyan text-black hover:bg-cyan/90 transition-all flex items-center gap-1.5 shadow-lg"
          >
            <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" />
              <path d="M2 12l10 5 10-5" />
            </svg>
            AI Researcher
          </button>

          <button className="px-3 py-1 rounded text-xs font-mono font-semibold bg-white/5 hover:bg-white/10 border border-white/10 text-slate-200">
            Export 3D
          </button>
        </div>
      </header>

      {/* 2. Main Workspace Layout */}
      <div className="relative flex-1 flex w-full h-[calc(100vh-48px)] overflow-hidden">
        {/* Left Sidebar: Autonomous Perception Roster */}
        <aside className="w-72 border-r border-white/10 bg-[#0B0F17]/90 backdrop-blur-md p-3 flex flex-col gap-3 overflow-y-auto z-20">
          <div className="text-xs font-mono font-bold text-slate-300 tracking-wide flex items-center justify-between">
            <span>OBJECT ROSTER (25)</span>
            <span className="text-[10px] text-cyan">PM-CSF ACTIVE</span>
          </div>

          {/* Detections List */}
          <div className="flex flex-col gap-2">
            {[
              { id: "OBJ_024_CYCLIST", label: "Cyclist", size: "2.22x0.67x1.00m", conf: "92%", occ: "14%" },
              { id: "OBJ_025_VEHICLE", label: "Vehicle", size: "2.90x1.12x1.16m", conf: "92%", occ: "29%" },
              { id: "OBJ_022_VEHICLE", label: "Vehicle", size: "3.44x1.39x1.31m", conf: "96%", occ: "57%" },
              { id: "OBJ_006_OBSTACLE", label: "Obstacle", size: "1.34x0.57x0.61m", conf: "94%", occ: "43%" },
            ].map((item) => (
              <div
                key={item.id}
                className="p-2 rounded bg-white/5 hover:bg-white/10 border border-white/10 cursor-pointer transition-all text-xs font-mono"
              >
                <div className="flex items-center justify-between text-slate-200 font-semibold mb-0.5">
                  <span>{item.id}</span>
                  <span className="text-[10px] text-emerald-400">OCC {item.occ}</span>
                </div>
                <div className="text-[11px] text-slate-400">
                  {item.label} · {item.size} · {item.conf}
                </div>
              </div>
            ))}
          </div>
        </aside>

        {/* Central 3D Canvas Area */}
        <section className="relative flex-1 h-full overflow-hidden bg-black">
          {/* CloudCompare Toolbars */}
          <CloudCompareToolbar
            onSetCameraView={handleCameraView}
            onToggleOrtho={() => setIsOrtho((v) => !v)}
            isOrtho={isOrtho}
            onTriggerTool={handleToolTrigger}
            activeTool={activeTool}
            onToggleRecording={() => setIsRecording((v) => !v)}
            isRecording={isRecording}
            onTogglePiP={() => setIsPiPActive((v) => !v)}
            isPiPActive={isPiPActive}
            onToggleLaser={() => setIsLaserActive((v) => !v)}
            isLaserActive={isLaserActive}
            onToggleTour={() => setIsTourActive((v) => !v)}
            isTourActive={isTourActive}
            onAddPin={() => console.log("Add pin")}
          />

          {/* Three.js Dynamic Viewport (Single or Split Screen) */}
          {isSplitScreen ? (
            <ViewportSplit3D isOrtho={isOrtho} />
          ) : (
            <Viewport3D
              isOrtho={isOrtho}
              activeTool={activeTool}
              isTourActive={isTourActive}
              isLaserActive={isLaserActive}
              isPiPActive={isPiPActive}
              isRecording={isRecording}
              onStopRecording={handleStopRecording}
            />
          )}
        </section>
      </div>

      {/* 3. AI / SI Autonomous Researcher Modal */}
      <AIResearcherModal
        isOpen={isResearcherOpen}
        onClose={() => setIsResearcherOpen(false)}
      />

      {/* 4. Recorded Video Playback Modal */}
      {recordedVideoUrl && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-6">
          <div className="flex flex-col bg-[#0B0F17] border border-cyan/40 rounded-xl p-4 max-w-3xl w-full shadow-2xl">
            <div className="flex items-center justify-between mb-3">
              <span className="font-mono font-bold text-sm text-white flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-rose-500 animate-pulse" />
                Session Screen Recording Playback (60 FPS WebM)
              </span>
              <button
                onClick={() => setRecordedVideoUrl(null)}
                className="text-slate-400 hover:text-white font-mono text-sm"
              >
                ✕ Close
              </button>
            </div>

            <video
              src={recordedVideoUrl}
              controls
              autoPlay
              loop
              className="w-full aspect-video rounded-lg border border-white/10 bg-black"
            />

            <div className="flex items-center justify-between mt-3">
              <span className="text-xs font-mono text-slate-400">Format: WebM / VP9 · Captured 60 Hz Stream</span>
              <a
                href={recordedVideoUrl}
                download="aeovexor_session_recording.webm"
                className="px-4 py-1.5 rounded-lg font-mono text-xs font-bold bg-cyan text-black hover:bg-cyan/90 transition-all shadow-lg"
              >
                Download Recording (.webm)
              </a>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
