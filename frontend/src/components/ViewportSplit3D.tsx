"use client";

import React, { useEffect, useRef, useState } from "react";
import * as THREE from "three";

interface ViewportSplitProps {
  isOrtho: boolean;
}

export default function ViewportSplit3D({ isOrtho }: ViewportSplitProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isSynced, setIsSynced] = useState(false);

  useEffect(() => {
    if (!containerRef.current) return;
    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight;
    const halfWidth = Math.floor(width / 2);

    // 1. Scene A (Raw Ingest) & Scene B (Processed)
    const sceneA = new THREE.Scene();
    sceneA.background = new THREE.Color(0x05070b);

    const sceneB = new THREE.Scene();
    sceneB.background = new THREE.Color(0x070a10);

    // 2. Grids
    const gridA = new THREE.GridHelper(60, 30, 0x94a3b8, 0x1e293b);
    gridA.rotation.x = Math.PI / 2;
    sceneA.add(gridA);

    const gridB = new THREE.GridHelper(60, 30, 0x00e5ff, 0x1e293b);
    gridB.rotation.x = Math.PI / 2;
    sceneB.add(gridB);

    // 3. Points in A (Monochrome Raw)
    const numPoints = 8000;
    const posA = new Float32Array(numPoints * 3);
    for (let i = 0; i < numPoints; i++) {
      const r = Math.sqrt(Math.random()) * 25;
      const t = Math.random() * Math.PI * 2;
      posA[i * 3] = r * Math.cos(t);
      posA[i * 3 + 1] = r * Math.sin(t);
      posA[i * 3 + 2] = (Math.random() - 0.5) * 2;
    }
    const geoA = new THREE.BufferGeometry();
    geoA.setAttribute("position", new THREE.BufferAttribute(posA, 3));
    const matA = new THREE.PointsMaterial({ size: 0.08, color: 0x94a3b8 });
    sceneA.add(new THREE.Points(geoA, matA));

    // 4. Points in B (Color Ramp & Bounding Boxes)
    const posB = new Float32Array(numPoints * 3);
    const colB = new Float32Array(numPoints * 3);
    for (let i = 0; i < numPoints; i++) {
      posB[i * 3] = posA[i * 3];
      posB[i * 3 + 1] = posA[i * 3 + 1];
      posB[i * 3 + 2] = posA[i * 3 + 2];

      const r = Math.sqrt(posA[i * 3] ** 2 + posA[i * 3 + 1] ** 2) / 25;
      colB[i * 3] = r > 0.5 ? 1.0 : r * 2.0;
      colB[i * 3 + 1] = r < 0.5 ? 0.8 : (1.0 - r) * 1.6;
      colB[i * 3 + 2] = r < 0.4 ? 1.0 : 0.2;
    }
    const geoB = new THREE.BufferGeometry();
    geoB.setAttribute("position", new THREE.BufferAttribute(posB, 3));
    geoB.setAttribute("color", new THREE.BufferAttribute(colB, 3));
    const matB = new THREE.PointsMaterial({ size: 0.08, vertexColors: true });
    sceneB.add(new THREE.Points(geoB, matB));

    // 3D Bounding Box in Scene B
    const boxGeo = new THREE.BoxGeometry(2.5, 4.5, 1.8);
    const edges = new THREE.EdgesGeometry(boxGeo);
    const lineMat = new THREE.LineBasicMaterial({ color: 0x00e5ff });
    const boxMesh = new THREE.LineSegments(edges, lineMat);
    boxMesh.position.set(0, 12, 0.9);
    sceneB.add(boxMesh);

    // 5. Cameras
    const camA = new THREE.PerspectiveCamera(55, halfWidth / height, 0.1, 1000);
    camA.position.set(0, -35, 18);
    camA.up.set(0, 0, 1);
    camA.lookAt(0, 0, 0);

    const camB = new THREE.PerspectiveCamera(55, halfWidth / height, 0.1, 1000);
    camB.position.set(0, -35, 18);
    camB.up.set(0, 0, 1);
    camB.lookAt(0, 0, 0);

    // 6. Renderer with Dual Viewport Scissor
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    containerRef.current.appendChild(renderer.domElement);

    let animId: number;
    const animate = () => {
      animId = requestAnimationFrame(animate);

      renderer.setScissorTest(true);

      // Left Viewport: Screen A (Raw)
      renderer.setScissor(0, 0, halfWidth, height);
      renderer.setViewport(0, 0, halfWidth, height);
      renderer.render(sceneA, camA);

      // Right Viewport: Screen B (Processed)
      renderer.setScissor(halfWidth, 0, width - halfWidth, height);
      renderer.setViewport(halfWidth, 0, width - halfWidth, height);
      renderer.render(sceneB, camB);
    };
    animate();

    const handleResize = () => {
      if (!containerRef.current) return;
      const w = containerRef.current.clientWidth;
      const h = containerRef.current.clientHeight;
      const hw = Math.floor(w / 2);
      camA.aspect = hw / h;
      camA.updateProjectionMatrix();
      camB.aspect = (w - hw) / h;
      camB.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener("resize", handleResize);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", handleResize);
      renderer.dispose();
      if (containerRef.current) {
        containerRef.current.innerHTML = "";
      }
    };
  }, []);

  return (
    <div className="relative w-full h-full">
      <div ref={containerRef} className="w-full h-full" />

      {/* Viewport Labels */}
      <div className="absolute top-4 left-4 z-30 px-3 py-1 bg-[#0B0F17]/90 border border-white/10 rounded font-mono text-xs text-slate-300">
        STATE A: RAW INGEST [8,000 PTS]
      </div>
      <div className="absolute top-4 right-4 z-30 px-3 py-1 bg-[#0B0F17]/90 border border-cyan/40 rounded font-mono text-xs text-cyan font-bold">
        STATE B: PROCESSED [8,000 PTS · 3D BOXES]
      </div>

      {/* Sync Toggle */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-30">
        <button
          onClick={() => setIsSynced((s) => !s)}
          className={`px-3 py-1.5 rounded-lg font-mono text-xs font-semibold border backdrop-blur-md transition-all ${
            isSynced
              ? "bg-cyan-500/20 text-cyan border-cyan/50"
              : "bg-[#0B0F17]/90 text-slate-400 border-white/15 hover:text-white"
          }`}
        >
          {isSynced ? "Cameras: Synchronized" : "Cameras: Decoupled (Individual Control)"}
        </button>
      </div>

      {/* Vertical Divider Line */}
      <div className="absolute top-0 bottom-0 left-1/2 -translate-x-1/2 w-px bg-white/20 pointer-events-none" />
    </div>
  );
}
