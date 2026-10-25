"use client";

import React, { useEffect, useState } from "react";

export interface TreeNode {
  name: string;
  path: string;
  type: "file" | "directory";
  children?: TreeNode[];
  size?: number;
  ext?: string;
  item_count?: number;
}

interface FileTreeProps {
  onSelectFile: (path: string) => void;
  selectedPath: string | null;
}

export default function FileTree({ onSelectFile, selectedPath }: FileTreeProps) {
  const [tree, setTree] = useState<TreeNode[]>([]);
  const [expanded, setExpanded] = useState<Record<string, boolean>>({
    "spatialforge": true,
    "native": true,
    "services": true,
    "workspace": true,
  });

  useEffect(() => {
    fetch("http://127.0.0.1:8765/api/ide/files/tree")
      .then((res) => res.json())
      .then((data) => {
        if (data && data.tree) setTree(data.tree);
      })
      .catch(() => {
        // Fallback offline mock tree
        setTree([
          {
            name: "spatialforge",
            path: "spatialforge",
            type: "directory",
            children: [
              { name: "core.py", path: "spatialforge/core.py", type: "file", ext: ".py" },
              { name: "native_bridge.py", path: "spatialforge/native_bridge.py", type: "file", ext: ".py" },
              { name: "geometry.py", path: "spatialforge/geometry.py", type: "file", ext: ".py" },
            ],
          },
          {
            name: "native",
            path: "native",
            type: "directory",
            children: [
              { name: "spatialforge_core.cpp", path: "native/cpp/src/spatialforge_core.cpp", type: "file", ext: ".cpp" },
              { name: "lib.rs", path: "native/rust/src/lib.rs", type: "file", ext: ".rs" },
            ],
          },
        ]);
      });
  }, []);

  const toggleExpand = (path: string) => {
    setExpanded((prev) => ({ ...prev, [path]: !prev[path] }));
  };

  const renderNode = (node: TreeNode, depth = 0) => {
    const isDir = node.type === "directory";
    const isExpanded = !!expanded[node.path];
    const isSelected = selectedPath === node.path;

    return (
      <div key={node.path} className="flex flex-col select-none">
        <div
          onClick={() => {
            if (isDir) toggleExpand(node.path);
            else onSelectFile(node.path);
          }}
          style={{ paddingLeft: `${depth * 14 + 8}px` }}
          className={`flex items-center gap-1.5 py-1 text-xs font-mono cursor-pointer transition-colors rounded ${
            isSelected
              ? "bg-cyan-500/20 text-cyan font-semibold border-l-2 border-cyan"
              : "text-slate-300 hover:bg-white/5 hover:text-white"
          }`}
        >
          {isDir ? (
            <span className="text-[10px] text-slate-400 w-3 text-center">
              {isExpanded ? "▼" : "▶"}
            </span>
          ) : (
            <span className="text-[10px] text-cyan/70 w-3 text-center">•</span>
          )}
          <span className="truncate">{node.name}</span>
        </div>

        {isDir && isExpanded && node.children && (
          <div className="flex flex-col">
            {node.children.map((child) => renderNode(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="flex flex-col h-full overflow-y-auto p-2 bg-[#080C14] border-r border-white/10 font-mono text-xs">
      <div className="flex items-center justify-between px-2 py-1.5 mb-1 text-slate-400 font-bold uppercase tracking-wider text-[10px]">
        <span>EXPLORER</span>
        <button
          onClick={() => {
            fetch("http://127.0.0.1:8765/api/ide/files/tree")
              .then((r) => r.json())
              .then((d) => d?.tree && setTree(d.tree));
          }}
          className="hover:text-cyan"
          title="Refresh Tree"
        >
          ↻
        </button>
      </div>
      <div className="flex flex-col">{tree.map((node) => renderNode(node, 0))}</div>
    </div>
  );
}
