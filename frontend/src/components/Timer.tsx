"use client";

import { useEffect, useRef, useState } from "react";

interface TimerProps {
  seconds: number;
  running: boolean;
  onExpire: () => void;
}

export default function Timer({ seconds, running, onExpire }: TimerProps) {
  const [remaining, setRemaining] = useState(seconds);
  const expiredRef = useRef(false);

  useEffect(() => {
    if (!running || seconds <= 0) return;
    expiredRef.current = false;
    const interval = setInterval(() => {
      setRemaining((prev) => Math.max(prev - 1, 0));
    }, 1000);
    return () => clearInterval(interval);
  }, [running, seconds]);

  useEffect(() => {
    if (!running || seconds <= 0 || remaining > 0 || expiredRef.current) return;
    expiredRef.current = true;
    onExpire();
  }, [onExpire, remaining, running, seconds]);

  if (seconds === 0) return null;

  const pct = seconds > 0 ? remaining / seconds : 0;
  const urgent = pct <= 0.3;

  return (
    <div className="flex items-center gap-3">
      {/* Limit-break style gauge */}
      <div className="w-28 lb-gauge rounded-sm">
        <div
          className={`lb-fill rounded-sm ${urgent ? "urgent" : ""}`}
          style={{ width: `${pct * 100}%` }}
        />
      </div>
      <span
        className="font-mono text-sm font-bold tabular-nums w-8 text-right"
        style={{ color: urgent ? "#ff6060" : "var(--color-gold)" }}
      >
        {remaining}s
      </span>
    </div>
  );
}
