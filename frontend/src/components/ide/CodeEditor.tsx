"use client";

import React, { useEffect, useRef } from "react";

export interface TabFile {
  path: string;
  name: string;
  content: string;
  isDirty?: boolean;
}

interface CodeEditorProps {
  openTabs: TabFile[];
  activeTabPath: string | null;
  onSelectTab: (path: string) => void;
  onCloseTab: (path: string) => void;
  onChangeContent: (content: string) => void;
  onSaveFile: () => void;
  theme: "atom" | "eclipse";
}

export default function CodeEditor({
  openTabs,
  activeTabPath,
  onSelectTab,
  onCloseTab,
  onChangeContent,
  onSaveFile,
  theme,
}: CodeEditorProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const activeTab = openTabs.find((t) => t.path === activeTabPath);

  // Handle Tab key and Cmd+S / Ctrl+S
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "s") {
      e.preventDefault();
      onSaveFile();
    } else if (e.key === "Tab") {
      e.preventDefault();
      const ta = e.currentTarget;
      const start = ta.selectionStart;
      const end = ta.selectionEnd;
      const val = ta.value;
      const newVal = val.substring(0, start) + "    " + val.substring(end);
      onChangeContent(newVal);
      setTimeout(() => {
        ta.selectionStart = ta.selectionEnd = start + 4;
      }, 0);
    }
  };

  const lines = (activeTab?.content || "").split("\n");

  const isDark = theme === "atom";

  return (
    <div
      className={`flex flex-col h-full flex-1 font-mono text-xs overflow-hidden ${
        isDark ? "bg-[#05070B] text-slate-200" : "bg-[#F8FAFC] text-slate-800"
      }`}
    >
      {/* 1. Tab Bar */}
      <div
        className={`flex items-center gap-1 border-b overflow-x-auto px-2 py-1 select-none ${
          isDark ? "bg-[#090D15] border-white/10" : "bg-slate-200 border-slate-300"
        }`}
      >
        {openTabs.map((tab) => {
          const isActive = tab.path === activeTabPath;
          return (
            <div
              key={tab.path}
              onClick={() => onSelectTab(tab.path)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded cursor-pointer border transition-all text-xs ${
                isActive
                  ? isDark
                    ? "bg-[#0F1523] text-cyan border-cyan/40 font-semibold"
                    : "bg-white text-blue-600 border-slate-300 font-semibold shadow-sm"
                  : isDark
                  ? "bg-transparent text-slate-400 border-transparent hover:text-slate-200"
                  : "bg-transparent text-slate-600 border-transparent hover:text-slate-900"
              }`}
            >
              <span>{tab.name}</span>
              {tab.isDirty && <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onCloseTab(tab.path);
                }}
                className="hover:text-rose-400 ml-1 text-slate-400 text-[10px]"
              >
                ✕
              </button>
            </div>
          );
        })}
      </div>

      {/* 2. Editor Body */}
      {activeTab ? (
        <div className="flex flex-1 relative overflow-hidden">
          {/* Line Numbers */}
          <div
            className={`w-12 py-3 select-none text-right pr-3 font-mono text-[11px] leading-5 border-r ${
              isDark ? "bg-[#070A0F] text-slate-600 border-white/5" : "bg-slate-100 text-slate-400 border-slate-200"
            }`}
          >
            {lines.map((_, i) => (
              <div key={i}>{i + 1}</div>
            ))}
          </div>

          {/* Text Area */}
          <textarea
            ref={textareaRef}
            value={activeTab.content}
            onChange={(e) => onChangeContent(e.target.value)}
            onKeyDown={handleKeyDown}
            spellCheck={false}
            className={`flex-1 p-3 font-mono text-[12px] leading-5 outline-none resize-none overflow-auto whitespace-pre bg-transparent ${
              isDark ? "text-slate-200 caret-cyan" : "text-slate-900 caret-blue-600"
            }`}
          />
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center text-slate-500 font-mono text-xs">
          Select a file from the explorer to begin editing.
        </div>
      )}
    </div>
  );
}
