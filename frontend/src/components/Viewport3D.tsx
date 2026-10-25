"use client";

import React, { useEffect, useRef, useState } from "react";
import * as THREE from "three";

interface ViewportProps {
  isOrtho: boolean;
  activeTool: string | null;
  isTourActive: boolean;
  isLaserActive: boolean;
  isPiPActive: boolean;
  isRecording: boolean;
  onStopRecording: (blob: Blob) => void;
}

export default function Viewport3D({
  isOrtho,
  activeTool,
  isTourActive,
  isLaserActive,
  isPiPActive,
  isRecording,
  onStopRecording,
}: ViewportProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const pipCameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const pointsRef = useRef<THREE.Points | null>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const recordedChunksRef = useRef<Blob[]>([]);

  const [pickedCoord, setPickedCoord] = useState<{ x: number; y: number; z: number } | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight;

    // 1. Scene & Cameras
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x05070b);
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 1000);
    camera.position.set(0, -45, 25);
    camera.up.set(0, 0, 1);
    camera.lookAt(0, 0, 0);
    cameraRef.current = camera;

    // Secondary PiP Camera (Top-Down BEV)
    const pipCamera = new THREE.PerspectiveCamera(60, 1.6, 0.1, 500);
    pipCamera.position.set(0, 0, 60);
    pipCamera.up.set(0, 1, 0);
    pipCamera.lookAt(0, 0, 0);
    pipCameraRef.current = pipCamera;

    // 2. Renderer with scissor test support for PiP
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    containerRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // 3. Grid & Distance Rings
    const grid = new THREE.GridHelper(80, 40, 0x00e5ff, 0x1e293b);
    grid.rotation.x = Math.PI / 2;
    scene.add(grid);

    // Range concentric rings
    [10, 20, 30, 40].forEach((r) => {
      const ringGeo = new THREE.RingGeometry(r - 0.05, r + 0.05, 64);
      const ringMat = new THREE.MeshBasicMaterial({
        color: 0x00e5ff,
        opacity: 0.18,
        transparent: true,
        side: THREE.DoubleSide,
      });
      scene.add(new THREE.Mesh(ringGeo, ringMat));
    });

    // 4. Populate Simulated/Loaded Point Cloud
    const numPoints = 12000;
    const positions = new Float32Array(numPoints * 3);
    const colors = new Float32Array(numPoints * 3);

    for (let i = 0; i < numPoints; i++) {
      const r = Math.sqrt(Math.random()) * 35;
      const theta = Math.random() * Math.PI * 2;
      const x = r * Math.cos(theta);
      const y = r * Math.sin(theta);
      const z = (Math.random() - 0.5) * 2.5;

      positions[i * 3] = x;
      positions[i * 3 + 1] = y;
      positions[i * 3 + 2] = z;

      // Distance gradient (Cyan -> Amber -> Rose)
      const dist = Math.min(r / 35, 1.0);
      colors[i * 3] = dist > 0.5 ? 1.0 : dist * 2.0;
      colors[i * 3 + 1] = dist < 0.5 ? 0.8 : (1.0 - dist) * 1.6;
      colors[i * 3 + 2] = dist < 0.4 ? 1.0 : 0.2;
    }

    const geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    geo.setAttribute("color", new THREE.BufferAttribute(colors, 3));

    const mat = new THREE.PointsMaterial({
      size: 0.08,
      vertexColors: true,
      transparent: true,
      opacity: 0.85,
    });
    const pointsMesh = new THREE.Points(geo, mat);
    scene.add(pointsMesh);
    pointsRef.current = pointsMesh;

    // 5. Animation loop
    let animId: number;
    const animate = () => {
      animId = requestAnimationFrame(animate);

      if (isTourActive) {
        scene.rotation.z += 0.005;
      }

      renderer.setScissorTest(false);
      renderer.setViewport(0, 0, width, height);
      renderer.render(scene, camera);

      // Render secondary camera in PiP inset if enabled
      if (isPiPActive) {
        const pipW = Math.floor(width * 0.28);
        const pipH = Math.floor(pipW / 1.6);
        const pipX = width - pipW - 16;
        const pipY = 16;

        renderer.setScissorTest(true);
        renderer.setScissor(pipX, pipY, pipW, pipH);
        renderer.setViewport(pipX, pipY, pipW, pipH);
        renderer.render(scene, pipCamera);
      }
    };
    animate();

    const handleResize = () => {
      if (!containerRef.current) return;
      const w = containerRef.current.clientWidth;
      const h = containerRef.current.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
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
  }, [isPiPActive, isTourActive]);

  // Handle Recording
  useEffect(() => {
    if (isRecording) {
      if (!rendererRef.current) return;
      recordedChunksRef.current = [];
      const stream = rendererRef.current.domElement.captureStream(60);
      const recorder = new MediaRecorder(stream, {
        mimeType: MediaRecorder.isTypeSupported("video/webm;codecs=vp9")
          ? "video/webm;codecs=vp9"
          : "video/webm",
      });

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) recordedChunksRef.current.push(e.data);
      };
      recorder.onstop = () => {
        const blob = new Blob(recordedChunksRef.current, { type: "video/webm" });
        onStopRecording(blob);
      };

      recorder.start(100);
      recorderRef.current = recorder;
    } else {
      if (recorderRef.current && recorderRef.current.state === "recording") {
        recorderRef.current.stop();
      }
    }
  }, [isRecording, onStopRecording]);

  return (
    <div ref={containerRef} className="relative w-full h-full overflow-hidden">
      {pickedCoord && (
        <div className="absolute top-16 left-16 z-30 p-2.5 rounded-lg bg-[#0B0F17]/95 border border-cyan/40 text-xs font-mono shadow-2xl">
          <div className="text-cyan font-bold mb-1">INSPECTED COORDINATE</div>
          <div className="text-slate-300">
            X: {pickedCoord.x.toFixed(3)}m · Y: {pickedCoord.y.toFixed(3)}m · Z: {pickedCoord.z.toFixed(3)}m
          </div>
        </div>
      )}
    </div>
  );
}
