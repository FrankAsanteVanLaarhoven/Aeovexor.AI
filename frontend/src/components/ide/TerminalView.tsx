"use client";

import React, { useState } from "react";

interface TerminalViewProps {
  logs: Array<{ type: "stdout" | "stderr" | "info"; text: string }>;
  onClear: () => void;
  onRunCLI: (cmd: string) => void;
  isRunning: boolean;
  execTimeMs?: number;
}

export default function TerminalView({
  logs,
  onClear,
  onRunCLI,
  isRunning,
  execTimeMs,
}: TerminalViewProps) {
  const [cmdInput, setCmdInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!cmdInput.trim() || isRunning) return;
    onRunCLI(cmdInput.trim());
    setCmdInput("");
  };

  return (
    <div className="flex flex-col h-full bg-[#05070B] border-t border-white/10 font-mono text-xs overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-1.5 bg-[#090D15] border-b border-white/10 text-slate-400 select-none">
        <div className="flex items-center gap-2">
          <span className="font-bold text-slate-300 text-[10px] tracking-wider uppercase">TERMINAL</span>
          {isRunning ? (
            <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-400 animate-pulse">
              RUNNING
            </span>
          ) : (
            <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400">
              READY
            </span>
          )}
          {execTimeMs !== undefined && (
            <span className="text-[10px] text-slate-500">{execTimeMs.toFixed(1)} ms</span>
          )}
        </div>
        <button onClick={onClear} className="hover:text-cyan text-[10px]" title="Clear output">
          Clear
        </button>
      </div>

      {/* Log Output Body */}
      <div className="flex-1 p-3 overflow-y-auto flex flex-col gap-1 text-[11px] leading-relaxed">
        {logs.map((log, i) => (
          <div
            key={i}
            className={`whitespace-pre-wrap break-all ${
              log.type === "stderr"
                ? "text-rose-400"
                : log.type === "info"
                ? "text-cyan"
                : "text-slate-300"
            }`}
          >
            {log.text}
          </div>
        ))}
      </div>

      {/* CLI Input */}
      <form onSubmit={handleSubmit} className="flex items-center border-t border-white/10 bg-[#070A0F] px-2 py-1">
        <span className="text-cyan font-bold mr-1">$</span>
        <input
          type="text"
          value={cmdInput}
          onChange={(e) => setCmdInput(e.target.value)}
          placeholder="Run Python or CLI command (e.g. spatialforge benchmark)..."
          className="flex-1 bg-transparent text-slate-200 outline-none text-xs font-mono"
        />
        <button
          type="submit"
          disabled={isRunning}
          className="px-2 py-0.5 text-[10px] bg-white/10 hover:bg-white/20 text-slate-200 rounded"
        >
          Execute
        </button>
      </form>
    </div>
  );
}
