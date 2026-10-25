"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import FileTree from "../../components/ide/FileTree";
import CodeEditor, { TabFile } from "../../components/ide/CodeEditor";
import TerminalView from "../../components/ide/TerminalView";
import PlotViewer from "../../components/ide/PlotViewer";
import AICopilotDrawer from "../../components/ide/AICopilotDrawer";

const DEFAULT_SCRIPT = `import numpy as np
import matplotlib.pyplot as plt
from spatialforge.signal_processing import kaufman_adaptive_filter_1d

# 1. Simulate noisy LiDAR range profile
np.random.seed(42)
r = np.linspace(10.0, 25.0, 100) + np.random.normal(0, 0.45, 100)

# 2. Apply Kaufman Adaptive Volatility Filter
filtered_r = kaufman_adaptive_filter_1d(r, period=10)

# 3. Visualize Filter Trajectory
plt.figure(figsize=(6, 3.2))
plt.plot(r, label='Raw LiDAR Profile', color='#94A3B8', alpha=0.7)
plt.plot(filtered_r, label='Kaufman Adaptive Filter', color='#00E5FF', linewidth=2)
plt.title('LiDAR Range Smoothing (Zero Lag)')
plt.xlabel('Azimuth Angle Index')
plt.ylabel('Range (meters)')
plt.grid(True, alpha=0.15)
plt.legend()
plt.tight_layout()
plt.show()

print(f"Filter completed. Raw Variance: {np.var(r):.4f}, Filtered Variance: {np.var(filtered_r):.4f}")
`;

export default function DeveloperIDEPage() {
  const [theme, setTheme] = useState<"atom" | "eclipse">("atom");
  const [openTabs, setOpenTabs] = useState<TabFile[]>([
    {
      path: "workspace/kaufman_filter.py",
      name: "kaufman_filter.py",
      content: DEFAULT_SCRIPT,
      isDirty: false,
    },
  ]);
  const [activeTabPath, setActiveTabPath] = useState<string>("workspace/kaufman_filter.py");
  const [isRunning, setIsRunning] = useState(false);
  const [execTimeMs, setExecTimeMs] = useState<number | undefined>(undefined);
  const [logs, setLogs] = useState<Array<{ type: "stdout" | "stderr" | "info"; text: string }>>([
    { type: "info", text: "AEOVEXOR Scientific IDE v2.4 initialized. Ready." },
  ]);
  const [plotB64, setPlotB64] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<Record<string, any>>({});
  const [isCopilotOpen, setIsCopilotOpen] = useState(false);

  const handleSelectFile = async (path: string) => {
    // If already open, select tab
    const existing = openTabs.find((t) => t.path === path);
    if (existing) {
      setActiveTabPath(path);
      return;
    }

    try {
      const res = await fetch(`http://127.0.0.1:8765/api/ide/files/read?path=${encodeURIComponent(path)}`);
      const data = await res.json();
      if (data && data.status === "SUCCESS") {
        const newTab: TabFile = {
          path: path,
          name: path.split("/").pop() || path,
          content: data.content || "",
          isDirty: false,
        };
        setOpenTabs((prev) => [...prev, newTab]);
        setActiveTabPath(path);
      }
    } catch {
      setLogs((prev) => [...prev, { type: "stderr", text: `Failed to load file: ${path}` }]);
    }
  };

  const handleCloseTab = (path: string) => {
    const remaining = openTabs.filter((t) => t.path !== path);
    setOpenTabs(remaining);
    if (activeTabPath === path && remaining.length > 0) {
      setActiveTabPath(remaining[0].path);
    }
  };

  const handleChangeContent = (newContent: string) => {
    setOpenTabs((prev) =>
      prev.map((t) => (t.path === activeTabPath ? { ...t, content: newContent, isDirty: true } : t))
    );
  };

  const handleSaveFile = async () => {
    const tab = openTabs.find((t) => t.path === activeTabPath);
    if (!tab) return;
    try {
      const res = await fetch("http://127.0.0.1:8765/api/ide/files/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          path: tab.path,
          content: tab.content,
        }),
      });
      const data = await res.json();
      if (data.status === "SUCCESS") {
        setOpenTabs((prev) =>
          prev.map((t) => (t.path === activeTabPath ? { ...t, isDirty: false } : t))
        );
        setLogs((prev) => [...prev, { type: "info", text: `Saved file: ${tab.path}` }]);
      }
    } catch {
      setLogs((prev) => [...prev, { type: "stderr", text: `Error saving: ${tab.path}` }]);
    }
  };

  const handleRunScript = async () => {
    const tab = openTabs.find((t) => t.path === activeTabPath);
    if (!tab || isRunning) return;

    setIsRunning(true);
    setLogs((prev) => [...prev, { type: "info", text: `Executing ${tab.name}...` }]);

    const t0 = performance.now();
    try {
      const res = await fetch("http://127.0.0.1:8765/api/ide/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: tab.content }),
      });
      const data = await res.json();
      const elapsed = performance.now() - t0;
      setExecTimeMs(elapsed);

      if (data.status === "SUCCESS") {
        if (data.stdout) {
          setLogs((prev) => [...prev, { type: "stdout", text: data.stdout }]);
        }
        if (data.stderr) {
          setLogs((prev) => [...prev, { type: "stderr", text: data.stderr }]);
        }
        if (data.plot_b64) {
          setPlotB64(data.plot_b64);
        }
        if (data.metrics_summary) {
          setMetrics(data.metrics_summary);
        }
      } else {
        setLogs((prev) => [...prev, { type: "stderr", text: data.error || "Execution failed" }]);
      }
    } catch (err: any) {
      setLogs((prev) => [...prev, { type: "stderr", text: `Execution failed: ${err.message}` }]);
    } finally {
      setIsRunning(false);
    }
  };

  const handleRunCLI = async (cmd: string) => {
    setIsRunning(true);
    setLogs((prev) => [...prev, { type: "info", text: `$ ${cmd}` }]);
    try {
      const res = await fetch("http://127.0.0.1:8765/api/ide/cli", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: cmd }),
      });
      const data = await res.json();
      if (data.stdout) setLogs((prev) => [...prev, { type: "stdout", text: data.stdout }]);
      if (data.stderr) setLogs((prev) => [...prev, { type: "stderr", text: data.stderr }]);
    } catch {
      setLogs((prev) => [...prev, { type: "stderr", text: "CLI execution failed." }]);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="flex flex-col w-screen h-screen overflow-hidden bg-[#05070B] font-mono">
      {/* 1. Header Navigation Bar */}
      <header className="h-11 border-b border-white/10 bg-[#090D15] px-4 flex items-center justify-between z-30 select-none">
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-cyan font-bold transition-all"
          >
            <span>◀</span> 3D Studio
          </Link>

          <div className="h-4 w-px bg-white/15 mx-1" />

          <div className="flex items-center gap-2">
            <span className="text-white font-black text-xs tracking-wider">
              AEOVEXOR <span className="text-cyan">IDE</span>
            </span>
            <span className="text-[10px] text-slate-500">v2.4</span>
          </div>

          <div className="h-4 w-px bg-white/15 mx-1" />

          {/* Run Button */}
          <button
            onClick={handleRunScript}
            disabled={isRunning}
            className={`px-3 py-1 rounded text-xs font-bold flex items-center gap-1.5 transition-all shadow-md ${
              isRunning
                ? "bg-amber-500/20 text-amber-400 border border-amber-500/40"
                : "bg-cyan text-black hover:bg-cyan/90"
            }`}
          >
            <span>▶</span> {isRunning ? "Running..." : "Run Script"}
          </button>

          {/* Save Button */}
          <button
            onClick={handleSaveFile}
            className="px-2.5 py-1 rounded text-xs bg-white/5 hover:bg-white/10 border border-white/10 text-slate-300"
          >
            Save (Cmd+S)
          </button>
        </div>

        {/* Right Header Tools */}
        <div className="flex items-center gap-2">
          {/* Theme Toggle */}
          <button
            onClick={() => setTheme((t) => (t === "atom" ? "eclipse" : "atom"))}
            className="px-2.5 py-1 rounded text-xs bg-white/5 hover:bg-white/10 border border-white/10 text-slate-400 hover:text-white"
          >
            Theme: {theme === "atom" ? "Atom Dark" : "Eclipse Light"}
          </button>

          {/* AI Copilot Toggle */}
          <button
            onClick={() => setIsCopilotOpen((o) => !o)}
            className={`px-3 py-1 rounded text-xs font-bold border flex items-center gap-1.5 transition-all ${
              isCopilotOpen
                ? "bg-cyan-500/20 text-cyan border-cyan/40"
                : "bg-white/5 text-slate-400 border-white/10 hover:text-white"
            }`}
          >
            Copilot
          </button>
        </div>
      </header>

      {/* 2. Main Workspace Layout */}
      <div className="flex flex-1 overflow-hidden relative">
        {/* Left: File Tree Explorer */}
        <aside className="w-60 h-full overflow-hidden">
          <FileTree onSelectFile={handleSelectFile} selectedPath={activeTabPath} />
        </aside>

        {/* Center & Bottom: Code Editor & Execution Views */}
        <div className="flex-1 flex flex-col h-full overflow-hidden">
          {/* Top: Code Editor */}
          <div className="h-[55%] border-b border-white/10">
            <CodeEditor
              openTabs={openTabs}
              activeTabPath={activeTabPath}
              onSelectTab={setActiveTabPath}
              onCloseTab={handleCloseTab}
              onChangeContent={handleChangeContent}
              onSaveFile={handleSaveFile}
              theme={theme}
            />
          </div>

          {/* Bottom Split: Terminal (Left) & Plot Viewer (Right) */}
          <div className="h-[45%] flex overflow-hidden">
            <div className="w-1/2 h-full">
              <TerminalView
                logs={logs}
                onClear={() => setLogs([])}
                onRunCLI={handleRunCLI}
                isRunning={isRunning}
                execTimeMs={execTimeMs}
              />
            </div>
            <div className="w-1/2 h-full">
              <PlotViewer plotB64={plotB64} metrics={metrics} />
            </div>
          </div>
        </div>

        {/* Right Collapsible AI Copilot Drawer */}
        <AICopilotDrawer
          isOpen={isCopilotOpen}
          onClose={() => setIsCopilotOpen(false)}
          onInsertCode={(code) => handleChangeContent(code)}
        />
      </div>
    </div>
  );
}
