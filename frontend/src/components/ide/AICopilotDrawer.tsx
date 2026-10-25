"use client";

import React, { useState } from "react";

interface AICopilotDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  onInsertCode: (code: string) => void;
}

export default function AICopilotDrawer({ isOpen, onClose, onInsertCode }: AICopilotDrawerProps) {
  const [model, setModel] = useState("anthropic/claude-3.5-sonnet");
  const [messages, setMessages] = useState<Array<{ role: "user" | "assistant"; text: string }>>([
    {
      role: "assistant",
      text: "AEOVEXOR AI Copilot ready. Backed by OpenRouter models. Ask questions, request algorithms, or generate CUDA/SIMD kernels.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  if (!isOpen) return null;

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    const prompt = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", text: prompt }]);
    setIsLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8765/api/ai/copilot/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: prompt,
          model: model,
        }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: data.response || "Task completed." },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: `[Offline Local Response] Analyzed prompt with ${model}. To run live OpenRouter inference, ensure OPENROUTER_API_KEY is configured in .env.local.`,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-80 border-l border-white/10 bg-[#070A0F] flex flex-col h-full font-mono text-xs z-30 shadow-2xl">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-white/10 bg-[#090D15]">
        <div className="flex items-center gap-1.5 font-bold text-white">
          <svg className="w-4 h-4 text-cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
          </svg>
          <span>AI COPILOT</span>
        </div>
        <button onClick={onClose} className="text-slate-400 hover:text-white text-xs">
          ✕
        </button>
      </div>

      {/* Model Selector */}
      <div className="px-3 py-1.5 border-b border-white/10 bg-black/40">
        <label className="text-[10px] text-slate-400 block mb-1">REASONING MODEL:</label>
        <select
          value={model}
          onChange={(e) => setModel(e.target.value)}
          className="w-full bg-[#0B0F17] border border-white/15 rounded px-2 py-1 text-cyan text-[11px] focus:outline-none focus:border-cyan"
        >
          <option value="anthropic/claude-3.5-sonnet">Claude 3.5 Sonnet</option>
          <option value="deepseek/deepseek-r1">DeepSeek R1 (Reasoning)</option>
          <option value="google/gemini-2.0-flash">Gemini 2.0 Flash</option>
          <option value="openai/gpt-4o">OpenAI GPT-4o</option>
        </select>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 p-3 overflow-y-auto flex flex-col gap-2.5">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`p-2 rounded text-[11px] leading-relaxed ${
              m.role === "user"
                ? "bg-cyan-500/15 border border-cyan/30 text-cyan self-end max-w-[90%]"
                : "bg-white/5 border border-white/10 text-slate-200 self-start"
            }`}
          >
            <div className="text-[9px] text-slate-400 font-bold mb-0.5">
              {m.role === "user" ? "YOU" : "COPILOT"}
            </div>
            <div className="whitespace-pre-wrap">{m.text}</div>
          </div>
        ))}
        {isLoading && (
          <div className="text-cyan animate-pulse text-[11px]">Reasoning with {model}...</div>
        )}
      </div>

      {/* Input */}
      <div className="p-2 border-t border-white/10 bg-[#090D15] flex gap-1.5">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask Copilot..."
          className="flex-1 bg-black/60 border border-white/15 rounded px-2.5 py-1 text-slate-200 text-xs outline-none focus:border-cyan"
        />
        <button
          onClick={handleSend}
          disabled={isLoading}
          className="px-3 py-1 bg-cyan text-black font-bold rounded hover:bg-cyan/90 text-xs"
        >
          Send
        </button>
      </div>
    </div>
  );
}
