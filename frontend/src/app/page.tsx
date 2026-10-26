"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import Viewport3D from "../components/Viewport3D";
import ViewportSplit3D from "../components/ViewportSplit3D";
import CloudCompareToolbar from "../components/CloudCompareToolbar";
import TelemetryHUD from "../components/TelemetryHUD";
import AIResearcherModal from "../components/AIResearcherModal";
import AnnotationSuite, { BoundingBox3D } from "../components/AnnotationSuite";
import LiDARIngestModal, { LoadedCloudData } from "../components/LiDARIngestModal";
import BenchmarkModal from "../components/BenchmarkModal";
import { ColormapMode } from "../lib/shaders";
import {
  detectEnterpriseObjects,
  detectEnterprisePersons,
  evaluateRoboticsSafety,
} from "../lib/api";

export default function StudioPage() {
  const [isOrtho, setIsOrtho] = useState(false);
  const [activeTool, setActiveTool] = useState<string | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isPiPActive, setIsPiPActive] = useState(false);
  const [isLaserActive, setIsLaserActive] = useState(false);
  const [isTourActive, setIsTourActive] = useState(false);
  const [isSplitScreen, setIsSplitScreen] = useState(false);
  const [isResearcherOpen, setIsResearcherOpen] = useState(false);
  const [isIngestOpen, setIsIngestOpen] = useState(false);
  const [isAnnotationsOpen, setIsAnnotationsOpen] = useState(false);
  const [isBenchmarkOpen, setIsBenchmarkOpen] = useState(false);
  const [isLiveStreaming, setIsLiveStreaming] = useState(false);
  const [colormapMode, setColormapMode] = useState<ColormapMode>("viridis");
  const [recordedVideoUrl, setRecordedVideoUrl] = useState<string | null>(null);
  const [customCloud, setCustomCloud] = useState<LoadedCloudData | null>(null);
  const [isDetecting, setIsDetecting] = useState(false);

  // Safety Zone State
  const [safetyStatus, setSafetyStatus] = useState<{
    zone: string;
    e_stop: boolean;
    speed: number;
    dist: number;
  }>({
    zone: "CLEAR",
    e_stop: false,
    speed: 1.6,
    dist: 12.0,
  });

  // 3D Bounding Boxes State
  const [boxes, setBoxes] = useState<BoundingBox3D[]>([
    {
      id: "VEH_001",
      label: "Vehicle",
      x: 6.5,
      y: 12.0,
      z: -0.8,
      dx: 4.4,
      dy: 1.9,
      dz: 1.6,
      yaw: 15,
      confidence: 0.96,
    },
    {
      id: "CYC_002",
      label: "Cyclist",
      x: -4.2,
      y: 18.5,
      z: -0.5,
      dx: 1.8,
      dy: 0.7,
      dz: 1.5,
      yaw: -45,
      confidence: 0.92,
    },
    {
      id: "PED_003",
      label: "Pedestrian",
      x: 3.8,
      y: 22.0,
      z: -0.3,
      dx: 0.7,
      dy: 0.7,
      dz: 1.75,
      yaw: 80,
      confidence: 0.89,
    },
  ]);
  const [selectedBoxId, setSelectedBoxId] = useState<string | null>("VEH_001");

  // Re-evaluate safety whenever boxes change
  useEffect(() => {
    let isCancelled = false;
    evaluateRoboticsSafety(boxes, 1.2)
      .then((res) => {
        if (!isCancelled && res?.safety_event) {
          const ev = res.safety_event;
          setSafetyStatus({
            zone: ev.zone_name.replace("_ZONE", ""),
            e_stop: ev.e_stop_triggered,
            speed: ev.recommended_speed_limit_mps,
            dist: ev.intrusion_distance_m,
          });
        }
      })
      .catch(() => {
        // Fallback local calculation
        const minDist = Math.min(...boxes.map((b) => Math.sqrt(b.x * b.x + b.y * b.y + b.z * b.z)));
        setSafetyStatus({
          zone: minDist < 2.0 ? "E-STOP" : minDist < 4.0 ? "SLOWDOWN" : "CLEAR",
          e_stop: minDist < 2.0,
          speed: minDist < 2.0 ? 0.0 : minDist < 4.0 ? 0.6 : 1.6,
          dist: minDist,
        });
      });

    return () => {
      isCancelled = true;
    };
  }, [boxes]);

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

  // Run AI Auto-Detection on active point cloud
  const handleRunAIDetection = async () => {
    setIsDetecting(true);
    try {
      // Gather sample coordinates from custom cloud or simulated frame
      const samplePts: number[][] = [];
      if (customCloud && customCloud.positions) {
        const step = Math.max(1, Math.floor(customCloud.positions.length / (3 * 500)));
        for (let i = 0; i < customCloud.positions.length / 3; i += step) {
          samplePts.push([
            customCloud.positions[i * 3],
            customCloud.positions[i * 3 + 1],
            customCloud.positions[i * 3 + 2],
          ]);
        }
      } else {
        // Synthesize dynamic clusters
        for (let i = 0; i < 200; i++) {
          samplePts.push([10 + (Math.random() - 0.5) * 4, 5 + (Math.random() - 0.5) * 2, (Math.random() - 0.5) * 1.5]);
          samplePts.push([-6 + (Math.random() - 0.5) * 0.8, 14 + (Math.random() - 0.5) * 0.8, (Math.random() - 0.5) * 1.8]);
        }
      }

      const [objsRes, pedsRes] = await Promise.all([
        detectEnterpriseObjects(samplePts).catch(() => ({ objects: [] })),
        detectEnterprisePersons(samplePts).catch(() => ({ persons: [] })),
      ]);

      const detected = [...(objsRes.objects || []), ...(pedsRes.persons || [])];
      if (detected.length > 0) {
        const formatted: BoundingBox3D[] = detected.map((d: any, idx: number) => ({
          id: d.id || `AI_OBJ_${idx + 1}`,
          label: d.label || "Vehicle",
          x: d.x,
          y: d.y,
          z: d.z,
          dx: d.dx,
          dy: d.dy,
          dz: d.dz,
          yaw: d.yaw || 0,
          confidence: d.confidence || 0.94,
        }));
        setBoxes(formatted);
        if (formatted.length > 0) setSelectedBoxId(formatted[0].id);
      }
    } finally {
      setIsDetecting(false);
    }
  };

  // Add Box Handler
  const handleAddBox = (preset?: Partial<BoundingBox3D>) => {
    const newId = `${(preset?.label || "OBJ").substring(0, 3).toUpperCase()}_${String(
      boxes.length + 1
    ).padStart(3, "0")}`;
    const newBox: BoundingBox3D = {
      id: newId,
      label: preset?.label || "Vehicle",
      x: 0,
      y: 10,
      z: 0,
      dx: preset?.dx || 4.2,
      dy: preset?.dy || 1.8,
      dz: preset?.dz || 1.6,
      yaw: preset?.yaw || 0,
      confidence: 1.0,
    };
    setBoxes((prev) => [...prev, newBox]);
    setSelectedBoxId(newId);
  };

  const handleUpdateBox = (id: string, updates: Partial<BoundingBox3D>) => {
    setBoxes((prev) => prev.map((b) => (b.id === id ? { ...b, ...updates } : b)));
  };

  const handleDeleteBox = (id: string) => {
    setBoxes((prev) => prev.filter((b) => b.id !== id));
    if (selectedBoxId === id) setSelectedBoxId(null);
  };

  // Ground Truth Export Handler
  const handleExportAnnotations = (format: "kitti" | "nuscenes" | "json") => {
    let content = "";
    let filename = `annotations_${Date.now()}`;

    if (format === "kitti") {
      filename += ".txt";
      content = boxes
        .map((b) => {
          const rotY = ((b.yaw * Math.PI) / 180).toFixed(2);
          return `${b.label} 0.00 0 0.00 0.00 0.00 50.00 50.00 ${b.dz.toFixed(2)} ${b.dy.toFixed(
            2
          )} ${b.dx.toFixed(2)} ${b.x.toFixed(2)} ${b.y.toFixed(2)} ${b.z.toFixed(2)} ${rotY}`;
        })
        .join("\n");
    } else if (format === "nuscenes") {
      filename += "_nuscenes.json";
      const records = boxes.map((b) => ({
        sample_annotation_token: `tok_${b.id}`,
        translation: [b.x, b.y, b.z],
        size: [b.dy, b.dx, b.dz],
        rotation: [0, 0, Math.sin((b.yaw * Math.PI) / 360), Math.cos((b.yaw * Math.PI) / 360)],
        category_name: `vehicle.${b.label.toLowerCase()}`,
        visibility_token: "v4_90_100",
      }));
      content = JSON.stringify(records, null, 2);
    } else {
      filename += ".json";
      content = JSON.stringify(boxes, null, 2);
    }

    const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <main className="flex flex-col w-screen h-screen overflow-hidden bg-[#05070B]">
      {/* 1. Header Bar */}
      <header className="h-12 border-b border-white/10 bg-[#0B0F17]/95 px-4 flex items-center justify-between z-30">
        <div className="flex items-center gap-3">
          {/* Branded Logo Shield */}
          <Link href="/overview" className="flex items-center gap-2 group">
            <svg className="w-6 h-6 text-cyan group-hover:drop-shadow-[0_0_8px_rgba(0,229,255,0.6)] transition-all" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2L3 7v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-9-5z" />
            </svg>
            <div className="flex flex-col">
              <span className="font-mono font-black text-xs tracking-wider text-white">
                AEOVEXOR<span className="text-cyan">.AI</span>
              </span>
              <span className="text-[8px] font-mono text-slate-400">STUDIO PRO v2.4</span>
            </div>
          </Link>

          <div className="h-4 w-px bg-white/15 mx-1" />

          {/* Active Dataset Pill */}
          <button
            onClick={() => setIsIngestOpen(true)}
            className="px-2.5 py-1 rounded bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-mono text-cyan flex items-center gap-1.5 transition-all"
            title="Click to Switch or Ingest Cloud"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-cyan animate-pulse" />
            <span>{customCloud ? customCloud.name : "velodyne_000008.bin"}</span>
            <span className="text-[10px] text-slate-500">
              ({customCloud ? `${customCloud.numPoints.toLocaleString()} pts` : "15k pts"})
            </span>
          </button>

          {/* Dynamic ISO 13849 Safety Badge */}
          <div
            className={`px-2.5 py-1 rounded text-xs font-mono font-bold flex items-center gap-1.5 border transition-all ${
              safetyStatus.e_stop
                ? "bg-rose-500/20 text-rose-400 border-rose-500 animate-pulse"
                : safetyStatus.zone === "SLOWDOWN"
                ? "bg-amber-500/20 text-amber-400 border-amber-500/50"
                : "bg-emerald-500/15 text-emerald-400 border-emerald-500/30"
            }`}
            title={`ISO 13849 Safety Perimeter: Intrusion Distance ${safetyStatus.dist.toFixed(1)}m, Max Speed ${safetyStatus.speed}m/s`}
          >
            <span
              className={`w-2 h-2 rounded-full ${
                safetyStatus.e_stop
                  ? "bg-rose-500"
                  : safetyStatus.zone === "SLOWDOWN"
                  ? "bg-amber-400"
                  : "bg-emerald-400"
              }`}
            />
            <span>
              ISO 13849: {safetyStatus.zone} ({safetyStatus.speed.toFixed(1)} m/s)
            </span>
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
          {/* Autonomous Benchmarks Trigger */}
          <button
            onClick={() => setIsBenchmarkOpen(true)}
            className="px-2.5 py-1 rounded text-xs font-mono font-semibold bg-white/5 hover:bg-white/10 border border-white/10 text-slate-200 transition-all flex items-center gap-1.5"
          >
            <svg className="w-3.5 h-3.5 text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
            </svg>
            Benchmarks
          </button>

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

          {/* Developer IDE Link */}
          <Link
            href="/ide"
            className="px-3 py-1 rounded text-xs font-mono font-semibold bg-white/5 hover:bg-cyan-500/15 hover:text-cyan border border-white/10 text-slate-200 transition-all flex items-center gap-1.5"
          >
            <span>&lt;/&gt;</span> Developer IDE
          </Link>

          {/* Platform Overview Link */}
          <Link
            href="/overview"
            className="px-3 py-1 rounded text-xs font-mono font-semibold bg-white/5 hover:bg-white/10 border border-white/10 text-slate-200 transition-all"
          >
            Platform Docs
          </Link>
        </div>
      </header>

      {/* 2. Main Workspace Layout */}
      <div className="relative flex-1 flex w-full h-[calc(100vh-48px)] overflow-hidden">
        {/* Left Sidebar: Autonomous Perception Roster OR 3D Annotation Suite */}
        <aside className="w-80 border-r border-white/10 bg-[#0B0F17]/90 backdrop-blur-md flex flex-col overflow-hidden z-20">
          {isAnnotationsOpen ? (
            <AnnotationSuite
              boxes={boxes}
              selectedId={selectedBoxId}
              onSelectBox={setSelectedBoxId}
              onAddBox={handleAddBox}
              onUpdateBox={handleUpdateBox}
              onDeleteBox={handleDeleteBox}
              onExport={handleExportAnnotations}
            />
          ) : (
            <div className="p-3 flex flex-col gap-3 h-full overflow-y-auto font-mono text-xs">
              <div className="font-bold text-slate-300 tracking-wide flex items-center justify-between pb-2 border-b border-white/10">
                <span>PERCEPTION ROSTER ({boxes.length})</span>
                <button
                  onClick={() => setIsAnnotationsOpen(true)}
                  className="text-[10px] text-cyan hover:underline font-bold"
                >
                  + EDIT 3D BOXES
                </button>
              </div>

              {/* AI Auto-Detection Action Bar */}
              <button
                onClick={handleRunAIDetection}
                disabled={isDetecting}
                className="w-full py-2 rounded bg-cyan/15 hover:bg-cyan/25 border border-cyan/40 text-cyan font-bold transition-all flex items-center justify-center gap-2 shadow-sm disabled:opacity-50"
              >
                {isDetecting ? (
                  <>
                    <span className="w-2 h-2 rounded-full bg-cyan animate-ping" />
                    <span>Running 3D Perception...</span>
                  </>
                ) : (
                  <>
                    <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                    </svg>
                    <span>Run AI Auto-Detection</span>
                  </>
                )}
              </button>

              {/* Detections List */}
              <div className="flex flex-col gap-2">
                {boxes.map((box) => (
                  <div
                    key={box.id}
                    onClick={() => {
                      setSelectedBoxId(box.id);
                      setIsAnnotationsOpen(true);
                    }}
                    className="p-2.5 rounded bg-white/5 hover:bg-white/10 border border-white/10 cursor-pointer transition-all"
                  >
                    <div className="flex items-center justify-between text-slate-200 font-semibold mb-0.5">
                      <span className="text-white font-bold">{box.id}</span>
                      <span className="text-[10px] text-emerald-400">
                        CONF {(box.confidence * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="text-[11px] text-slate-400">
                      {box.label} · {box.dx.toFixed(1)}x{box.dy.toFixed(1)}x{box.dz.toFixed(1)}m · Yaw {box.yaw}°
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-auto p-3 rounded-lg bg-cyan/5 border border-cyan/20">
                <span className="text-cyan font-bold block mb-1">POLYGLOT ACCELERATION</span>
                <p className="text-[10px] text-slate-400 leading-relaxed">
                  C++ SIMD Voxelization + Rust Zero-Copy Parser active. Streaming over Go microservice at 60Hz.
                </p>
              </div>
            </div>
          )}
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
            colormapMode={colormapMode}
            onChangeColormap={setColormapMode}
            isLiveStreaming={isLiveStreaming}
            onToggleLiveStream={() => setIsLiveStreaming((s) => !s)}
            isAnnotationsOpen={isAnnotationsOpen}
            onToggleAnnotations={() => setIsAnnotationsOpen((a) => !a)}
            onOpenIngest={() => setIsIngestOpen(true)}
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
              isLiveStreaming={isLiveStreaming}
              colormapMode={colormapMode}
              customCloud={customCloud}
              boxes={boxes}
              selectedBoxId={selectedBoxId}
              onSelectBox={setSelectedBoxId}
              onStopRecording={handleStopRecording}
            />
          )}
        </section>
      </div>

      {/* 3. Ingest Cloud Dropzone Modal */}
      <LiDARIngestModal
        isOpen={isIngestOpen}
        onClose={() => setIsIngestOpen(false)}
        onCloudLoaded={(loaded) => setCustomCloud(loaded)}
      />

      {/* 4. Autonomous Benchmarks Modal */}
      <BenchmarkModal
        isOpen={isBenchmarkOpen}
        onClose={() => setIsBenchmarkOpen(false)}
      />

      {/* 5. AI / SI Autonomous Researcher Modal */}
      <AIResearcherModal
        isOpen={isResearcherOpen}
        onClose={() => setIsResearcherOpen(false)}
      />

      {/* 6. Recorded Video Playback Modal */}
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
