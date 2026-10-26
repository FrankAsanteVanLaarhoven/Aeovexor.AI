"use client";

import React, { useState } from "react";

export interface BoundingBox3D {
  id: string;
  label: "Vehicle" | "Pedestrian" | "Cyclist" | "Sign" | "Obstacle";
  x: number;
  y: number;
  z: number;
  dx: number;
  dy: number;
  dz: number;
  yaw: number; // in degrees
  confidence: number;
}

const CLASS_COLORS: Record<BoundingBox3D["label"], string> = {
  Vehicle: "#00E5FF", // Cyan
  Pedestrian: "#F43F5E", // Rose
  Cyclist: "#F59E0B", // Amber
  Sign: "#10B981", // Emerald
  Obstacle: "#A855F7", // Purple
};

interface AnnotationSuiteProps {
  boxes: BoundingBox3D[];
  selectedId: string | null;
  onSelectBox: (id: string | null) => void;
  onAddBox: (preset?: Partial<BoundingBox3D>) => void;
  onUpdateBox: (id: string, updates: Partial<BoundingBox3D>) => void;
  onDeleteBox: (id: string) => void;
  onExport: (format: "kitti" | "nuscenes" | "json") => void;
}

export default function AnnotationSuite({
  boxes,
  selectedId,
  onSelectBox,
  onAddBox,
  onUpdateBox,
  onDeleteBox,
  onExport,
}: AnnotationSuiteProps) {
  const selectedBox = boxes.find((b) => b.id === selectedId);
  const [activeTab, setActiveTab] = useState<"list" | "edit" | "export">("list");

  return (
    <div className="flex flex-col h-full bg-[#0B0F17]/95 border-r border-white/10 text-xs font-mono select-none">
      {/* Header */}
      <div className="p-3 border-b border-white/10 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <svg className="w-4 h-4 text-cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
            <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
            <line x1="12" y1="22.08" x2="12" y2="12" />
          </svg>
          <span className="font-bold text-white tracking-wider">3D ANNOTATION SUITE</span>
        </div>
        <span className="text-[10px] px-1.5 py-0.5 rounded bg-cyan/10 text-cyan border border-cyan/20">
          {boxes.length} BOXES
        </span>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-white/10 bg-black/40">
        <button
          onClick={() => setActiveTab("list")}
          className={`flex-1 py-1.5 text-center transition-all ${
            activeTab === "list"
              ? "text-cyan border-b-2 border-cyan font-bold bg-white/5"
              : "text-slate-400 hover:text-white"
          }`}
        >
          Objects ({boxes.length})
        </button>
        <button
          onClick={() => setActiveTab("edit")}
          disabled={!selectedBox}
          className={`flex-1 py-1.5 text-center transition-all ${
            activeTab === "edit"
              ? "text-cyan border-b-2 border-cyan font-bold bg-white/5"
              : selectedBox
              ? "text-slate-400 hover:text-white"
              : "text-slate-600 cursor-not-allowed"
          }`}
        >
          7-DOF Editor
        </button>
        <button
          onClick={() => setActiveTab("export")}
          className={`flex-1 py-1.5 text-center transition-all ${
            activeTab === "export"
              ? "text-cyan border-b-2 border-cyan font-bold bg-white/5"
              : "text-slate-400 hover:text-white"
          }`}
        >
          Export
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-3 flex flex-col gap-3">
        {activeTab === "list" && (
          <>
            {/* Quick Presets Button Group */}
            <div>
              <div className="text-[10px] text-slate-400 font-bold mb-1.5">QUICK SPAWN 3D OBB:</div>
              <div className="grid grid-cols-2 gap-1.5">
                <button
                  onClick={() =>
                    onAddBox({
                      label: "Vehicle",
                      dx: 4.2,
                      dy: 1.8,
                      dz: 1.6,
                      yaw: 0,
                    })
                  }
                  className="px-2 py-1.5 rounded bg-white/5 hover:bg-cyan-500/20 hover:text-cyan border border-white/10 text-left transition-all flex items-center justify-between"
                >
                  <span>+ Car</span>
                  <span className="text-[9px] text-slate-500">4.2x1.8m</span>
                </button>
                <button
                  onClick={() =>
                    onAddBox({
                      label: "Pedestrian",
                      dx: 0.6,
                      dy: 0.6,
                      dz: 1.7,
                      yaw: 0,
                    })
                  }
                  className="px-2 py-1.5 rounded bg-white/5 hover:bg-rose-500/20 hover:text-rose-400 border border-white/10 text-left transition-all flex items-center justify-between"
                >
                  <span>+ Pedestrian</span>
                  <span className="text-[9px] text-slate-500">0.6x0.6m</span>
                </button>
                <button
                  onClick={() =>
                    onAddBox({
                      label: "Cyclist",
                      dx: 1.8,
                      dy: 0.7,
                      dz: 1.5,
                      yaw: 0,
                    })
                  }
                  className="px-2 py-1.5 rounded bg-white/5 hover:bg-amber-500/20 hover:text-amber-400 border border-white/10 text-left transition-all flex items-center justify-between"
                >
                  <span>+ Cyclist</span>
                  <span className="text-[9px] text-slate-500">1.8x0.7m</span>
                </button>
                <button
                  onClick={() =>
                    onAddBox({
                      label: "Obstacle",
                      dx: 1.2,
                      dy: 1.2,
                      dz: 1.2,
                      yaw: 0,
                    })
                  }
                  className="px-2 py-1.5 rounded bg-white/5 hover:bg-purple-500/20 hover:text-purple-400 border border-white/10 text-left transition-all flex items-center justify-between"
                >
                  <span>+ Obstacle</span>
                  <span className="text-[9px] text-slate-500">1.2x1.2m</span>
                </button>
              </div>
            </div>

            {/* Boxes List */}
            <div className="flex flex-col gap-1.5 mt-2">
              <div className="text-[10px] text-slate-400 font-bold mb-0.5">LABELED OBJECTS:</div>
              {boxes.length === 0 ? (
                <div className="p-4 rounded border border-dashed border-white/15 text-center text-slate-500 text-[11px]">
                  No 3D bounding boxes yet. Click a quick spawn button above to add annotations.
                </div>
              ) : (
                boxes.map((box) => {
                  const isSelected = box.id === selectedId;
                  const color = CLASS_COLORS[box.label];
                  return (
                    <div
                      key={box.id}
                      onClick={() => {
                        onSelectBox(box.id);
                        setActiveTab("edit");
                      }}
                      className={`p-2 rounded border cursor-pointer transition-all flex flex-col gap-1 ${
                        isSelected
                          ? "bg-white/10 border-cyan shadow-md"
                          : "bg-white/5 hover:bg-white/10 border-white/10"
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-1.5">
                          <span className="w-2 h-2 rounded-full" style={{ backgroundColor: color }} />
                          <span className="font-bold text-white">{box.id}</span>
                          <span
                            className="text-[9px] px-1 rounded font-semibold"
                            style={{ color, backgroundColor: `${color}20` }}
                          >
                            {box.label}
                          </span>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onDeleteBox(box.id);
                          }}
                          className="text-slate-500 hover:text-rose-400 p-0.5"
                          title="Delete Box"
                        >
                          ✕
                        </button>
                      </div>
                      <div className="text-[10px] text-slate-400 flex justify-between">
                        <span>
                          Pos: ({box.x.toFixed(1)}, {box.y.toFixed(1)}, {box.z.toFixed(1)})
                        </span>
                        <span>Yaw: {box.yaw.toFixed(0)}°</span>
                      </div>
                      <div className="text-[10px] text-slate-400">
                        Dim: {box.dx.toFixed(2)}m × {box.dy.toFixed(2)}m × {box.dz.toFixed(2)}m
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </>
        )}

        {activeTab === "edit" && selectedBox && (
          <div className="flex flex-col gap-3">
            <div className="flex items-center justify-between p-2 rounded bg-white/5 border border-white/10">
              <span className="font-bold text-white">{selectedBox.id}</span>
              <select
                value={selectedBox.label}
                onChange={(e) =>
                  onUpdateBox(selectedBox.id, {
                    label: e.target.value as BoundingBox3D["label"],
                  })
                }
                className="bg-[#0B0F17] border border-white/20 text-white rounded px-2 py-1 text-xs"
              >
                <option value="Vehicle">Vehicle</option>
                <option value="Pedestrian">Pedestrian</option>
                <option value="Cyclist">Cyclist</option>
                <option value="Sign">Sign</option>
                <option value="Obstacle">Obstacle</option>
              </select>
            </div>

            {/* Translation (X, Y, Z) */}
            <div className="flex flex-col gap-1.5 p-2 rounded bg-white/5 border border-white/10">
              <span className="text-[10px] text-cyan font-bold">TRANSLATION (METERS)</span>
              {(["x", "y", "z"] as const).map((axis) => (
                <div key={axis} className="flex items-center gap-2">
                  <span className="w-4 text-slate-400 uppercase font-bold">{axis}:</span>
                  <input
                    type="range"
                    min={-40}
                    max={40}
                    step={0.1}
                    value={selectedBox[axis]}
                    onChange={(e) =>
                      onUpdateBox(selectedBox.id, { [axis]: parseFloat(e.target.value) })
                    }
                    className="flex-1 accent-cyan cursor-pointer"
                  />
                  <input
                    type="number"
                    step={0.1}
                    value={selectedBox[axis]}
                    onChange={(e) =>
                      onUpdateBox(selectedBox.id, { [axis]: parseFloat(e.target.value) })
                    }
                    className="w-14 bg-black/60 border border-white/15 px-1 py-0.5 rounded text-right text-white"
                  />
                </div>
              ))}
            </div>

            {/* Scale / Dimensions (dx, dy, dz) */}
            <div className="flex flex-col gap-1.5 p-2 rounded bg-white/5 border border-white/10">
              <span className="text-[10px] text-amber-400 font-bold">DIMENSIONS (DX, DY, DZ)</span>
              {(["dx", "dy", "dz"] as const).map((dim) => (
                <div key={dim} className="flex items-center gap-2">
                  <span className="w-6 text-slate-400 uppercase font-bold">{dim}:</span>
                  <input
                    type="range"
                    min={0.2}
                    max={12}
                    step={0.1}
                    value={selectedBox[dim]}
                    onChange={(e) =>
                      onUpdateBox(selectedBox.id, { [dim]: parseFloat(e.target.value) })
                    }
                    className="flex-1 accent-amber-400 cursor-pointer"
                  />
                  <input
                    type="number"
                    step={0.1}
                    value={selectedBox[dim]}
                    onChange={(e) =>
                      onUpdateBox(selectedBox.id, { [dim]: parseFloat(e.target.value) })
                    }
                    className="w-14 bg-black/60 border border-white/15 px-1 py-0.5 rounded text-right text-white"
                  />
                </div>
              ))}
            </div>

            {/* Rotation / Yaw Angle */}
            <div className="flex flex-col gap-1.5 p-2 rounded bg-white/5 border border-white/10">
              <span className="text-[10px] text-emerald-400 font-bold">HEADING / YAW ANGLE</span>
              <div className="flex items-center gap-2">
                <span className="w-8 text-slate-400 font-bold">YAW:</span>
                <input
                  type="range"
                  min={-180}
                  max={180}
                  step={1}
                  value={selectedBox.yaw}
                  onChange={(e) =>
                    onUpdateBox(selectedBox.id, { yaw: parseFloat(e.target.value) })
                  }
                  className="flex-1 accent-emerald-400 cursor-pointer"
                />
                <span className="w-12 text-right text-white font-bold">{selectedBox.yaw}°</span>
              </div>
            </div>

            <button
              onClick={() => onDeleteBox(selectedBox.id)}
              className="mt-2 py-1.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/30 hover:bg-rose-500/20 font-bold transition-all text-center"
            >
              Delete Bounding Box
            </button>
          </div>
        )}

        {activeTab === "export" && (
          <div className="flex flex-col gap-2.5">
            <div className="text-[10px] text-slate-400 font-bold">GROUND TRUTH EXPORT FORMATS:</div>

            <div className="p-2.5 rounded bg-white/5 border border-white/10 flex flex-col gap-1">
              <div className="font-bold text-white flex items-center justify-between">
                <span>KITTI 3D Format</span>
                <span className="text-[9px] text-cyan">.txt</span>
              </div>
              <p className="text-[10px] text-slate-400">
                Official autonomous benchmark format: type, truncated, occluded, alpha, bbox(4), h, w, l, x, y, z, rot_y.
              </p>
              <button
                onClick={() => onExport("kitti")}
                className="mt-1 py-1 rounded bg-cyan text-black font-bold hover:bg-cyan/90 transition-all text-center"
              >
                Download KITTI Labels
              </button>
            </div>

            <div className="p-2.5 rounded bg-white/5 border border-white/10 flex flex-col gap-1">
              <div className="font-bold text-white flex items-center justify-between">
                <span>NuScenes JSON Format</span>
                <span className="text-[9px] text-amber-400">.json</span>
              </div>
              <p className="text-[10px] text-slate-400">
                Sample annotation tokens with translation, size, and quaternion rotation.
              </p>
              <button
                onClick={() => onExport("nuscenes")}
                className="mt-1 py-1 rounded bg-amber-400 text-black font-bold hover:bg-amber-400/90 transition-all text-center"
              >
                Download NuScenes JSON
              </button>
            </div>

            <div className="p-2.5 rounded bg-white/5 border border-white/10 flex flex-col gap-1">
              <div className="font-bold text-white flex items-center justify-between">
                <span>Full Aeovexor Spatial Schema</span>
                <span className="text-[9px] text-emerald-400">.json</span>
              </div>
              <p className="text-[10px] text-slate-400">
                Raw 7-DOF parameters with millimeter coordinates and confidence scores.
              </p>
              <button
                onClick={() => onExport("json")}
                className="mt-1 py-1 rounded bg-emerald-400 text-black font-bold hover:bg-emerald-400/90 transition-all text-center"
              >
                Download Raw JSON
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
