"use client";

import React, { useState } from "react";

export interface LoadedCloudData {
  name: string;
  positions: Float32Array;
  intensities: Float32Array | null;
  numPoints: number;
}

interface LiDARIngestModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCloudLoaded: (cloud: LoadedCloudData) => void;
}

export default function LiDARIngestModal({
  isOpen,
  onClose,
  onCloudLoaded,
}: LiDARIngestModalProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [loadingMsg, setLoadingMsg] = useState<string | null>(null);

  if (!isOpen) return null;

  // Preset Generator
  const loadPreset = (presetName: string) => {
    setLoadingMsg(`Generating high-density point cloud: ${presetName}...`);

    setTimeout(() => {
      let numPts = 25000;
      let positions: Float32Array;
      let intensities: Float32Array;

      if (presetName === "KITTI Velodyne 64-Beam") {
        numPts = 45000;
        positions = new Float32Array(numPts * 3);
        intensities = new Float32Array(numPts);

        // Simulate 64 laser scan rings
        const numBeams = 64;
        const ptsPerBeam = Math.floor(numPts / numBeams);
        let idx = 0;

        for (let b = 0; b < numBeams; b++) {
          const elevationAngle = ((b / (numBeams - 1)) * 26.8 - 24.8) * (Math.PI / 180);
          for (let p = 0; p < ptsPerBeam; p++) {
            const azimuth = (p / ptsPerBeam) * Math.PI * 2;
            const range = 5 + Math.random() * 45;

            const x = range * Math.cos(elevationAngle) * Math.cos(azimuth);
            const y = range * Math.cos(elevationAngle) * Math.sin(azimuth);
            const z = range * Math.sin(elevationAngle) - 1.73; // Sensor height at 1.73m

            positions[idx * 3] = x;
            positions[idx * 3 + 1] = y;
            positions[idx * 3 + 2] = z;
            intensities[idx] = Math.random() > 0.85 ? 0.95 : Math.random() * 0.5;
            idx++;
          }
        }
      } else if (presetName === "Stanford 3D High-Res Scan") {
        numPts = 32000;
        positions = new Float32Array(numPts * 3);
        intensities = new Float32Array(numPts);

        // Parametric double-spiral / sculpted bunny approximation
        for (let i = 0; i < numPts; i++) {
          const u = Math.random() * Math.PI * 2;
          const v = (Math.random() - 0.5) * Math.PI;
          const r = 12 + 4 * Math.sin(3 * u) * Math.cos(2 * v);

          positions[i * 3] = r * Math.cos(u) * Math.cos(v);
          positions[i * 3 + 1] = r * Math.sin(u) * Math.cos(v);
          positions[i * 3 + 2] = r * Math.sin(v) * 1.5;
          intensities[i] = (v + Math.PI / 2) / Math.PI;
        }
      } else {
        // NuScenes Radar / LiDAR
        numPts = 28000;
        positions = new Float32Array(numPts * 3);
        intensities = new Float32Array(numPts);

        for (let i = 0; i < numPts; i++) {
          const r = Math.sqrt(Math.random()) * 50;
          const theta = Math.random() * Math.PI * 2;
          positions[i * 3] = r * Math.cos(theta);
          positions[i * 3 + 1] = r * Math.sin(theta);
          positions[i * 3 + 2] = (Math.random() - 0.5) * 3.5;
          intensities[i] = Math.max(0, 1 - r / 50);
        }
      }

      onCloudLoaded({
        name: presetName,
        positions,
        intensities,
        numPoints: numPts,
      });

      setLoadingMsg(null);
      onClose();
    }, 400);
  };

  const handleFileDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      processFile(file);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      processFile(e.target.files[0]);
    }
  };

  const processFile = (file: File) => {
    setLoadingMsg(`Parsing ${file.name} (${(file.size / (1024 * 1024)).toFixed(2)} MB)...`);

    const reader = new FileReader();

    if (file.name.endsWith(".bin")) {
      // KITTI binary (float32 x, y, z, r)
      reader.onload = (evt) => {
        const buffer = evt.target?.result as ArrayBuffer;
        if (!buffer) return;
        const view = new Float32Array(buffer);
        const numPoints = Math.floor(view.length / 4);

        const positions = new Float32Array(numPoints * 3);
        const intensities = new Float32Array(numPoints);

        for (let i = 0; i < numPoints; i++) {
          positions[i * 3] = view[i * 4];
          positions[i * 3 + 1] = view[i * 4 + 1];
          positions[i * 3 + 2] = view[i * 4 + 2];
          intensities[i] = view[i * 4 + 3];
        }

        onCloudLoaded({
          name: file.name,
          positions,
          intensities,
          numPoints,
        });
        setLoadingMsg(null);
        onClose();
      };
      reader.readAsArrayBuffer(file);
    } else {
      // Text / ASCII (xyz, ply, pcd)
      reader.onload = (evt) => {
        const text = evt.target?.result as string;
        if (!text) return;
        const lines = text.split("\n");
        const parsedPositions: number[] = [];
        const parsedIntensities: number[] = [];

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || trimmed.startsWith("#") || trimmed.startsWith("element") || trimmed.startsWith("property") || trimmed.startsWith("FIELDS")) {
            continue;
          }
          const parts = trimmed.split(/[\s,]+/);
          if (parts.length >= 3) {
            const x = parseFloat(parts[0]);
            const y = parseFloat(parts[1]);
            const z = parseFloat(parts[2]);
            if (!isNaN(x) && !isNaN(y) && !isNaN(z)) {
              parsedPositions.push(x, y, z);
              parsedIntensities.push(parts[3] ? parseFloat(parts[3]) : 0.5);
            }
          }
        }

        const numPoints = Math.floor(parsedPositions.length / 3);
        onCloudLoaded({
          name: file.name,
          positions: new Float32Array(parsedPositions),
          intensities: new Float32Array(parsedIntensities),
          numPoints,
        });
        setLoadingMsg(null);
        onClose();
      };
      reader.readAsText(file);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4">
      <div className="flex flex-col bg-[#0B0F17] border border-cyan/40 rounded-xl p-5 max-w-xl w-full shadow-2xl font-mono text-xs">
        {/* Modal Header */}
        <div className="flex items-center justify-between pb-3 border-b border-white/10 mb-4">
          <div className="flex items-center gap-2">
            <svg className="w-5 h-5 text-cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="17 8 12 3 7 8" />
              <line x1="12" y1="3" x2="12" y2="15" />
            </svg>
            <span className="font-bold text-sm text-white">INGEST 3D POINT CLOUD</span>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white">
            ✕
          </button>
        </div>

        {/* Drag & Drop Area */}
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleFileDrop}
          className={`flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg transition-all ${
            isDragging
              ? "border-cyan bg-cyan/10"
              : "border-white/20 bg-white/5 hover:border-cyan/50 hover:bg-white/10"
          }`}
        >
          <svg className="w-10 h-10 text-cyan mb-3 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242" />
            <path d="M12 12v9" />
            <path d="m16 16-4-4-4 4" />
          </svg>
          <span className="font-bold text-white text-sm mb-1">
            Drag & drop raw LiDAR scan
          </span>
          <span className="text-[11px] text-slate-400 mb-4 text-center">
            Supported formats: <strong className="text-cyan">.BIN</strong> (KITTI), <strong className="text-amber-400">.PCD</strong>, <strong className="text-emerald-400">.PLY</strong>, <strong className="text-purple-400">.XYZ</strong>, <strong className="text-rose-400">.LAS</strong>
          </span>

          <label className="px-4 py-2 rounded bg-cyan text-black font-bold cursor-pointer hover:bg-cyan/90 transition-all shadow-md">
            <span>Browse Local Files</span>
            <input
              type="file"
              accept=".bin,.pcd,.ply,.xyz,.txt,.las"
              onChange={handleFileInput}
              className="hidden"
            />
          </label>
        </div>

        {/* Loading Indicator */}
        {loadingMsg && (
          <div className="mt-3 p-2.5 rounded bg-cyan/10 border border-cyan/30 text-cyan text-center flex items-center justify-center gap-2">
            <span className="w-2 h-2 rounded-full bg-cyan animate-ping" />
            <span>{loadingMsg}</span>
          </div>
        )}

        {/* Quick Benchmark Presets */}
        <div className="mt-4 pt-3 border-t border-white/10">
          <span className="text-[11px] font-bold text-slate-400 block mb-2">
            OR LOAD HIGH-FIDELITY PRESET BENCHMARK:
          </span>
          <div className="grid grid-cols-3 gap-2">
            <button
              onClick={() => loadPreset("KITTI Velodyne 64-Beam")}
              className="p-2 rounded bg-white/5 hover:bg-cyan-500/20 hover:text-cyan border border-white/10 text-left transition-all"
            >
              <div className="font-bold text-white">KITTI Velodyne</div>
              <div className="text-[10px] text-slate-400">45k pts · 64 beams</div>
            </button>
            <button
              onClick={() => loadPreset("Stanford 3D High-Res Scan")}
              className="p-2 rounded bg-white/5 hover:bg-amber-500/20 hover:text-amber-400 border border-white/10 text-left transition-all"
            >
              <div className="font-bold text-white">Stanford 3D Scan</div>
              <div className="text-[10px] text-slate-400">32k pts · Sculpted</div>
            </button>
            <button
              onClick={() => loadPreset("NuScenes Autonomous Frame")}
              className="p-2 rounded bg-white/5 hover:bg-emerald-500/20 hover:text-emerald-400 border border-white/10 text-left transition-all"
            >
              <div className="font-bold text-white">NuScenes Radar</div>
              <div className="text-[10px] text-slate-400">28k pts · Multi-sensor</div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
