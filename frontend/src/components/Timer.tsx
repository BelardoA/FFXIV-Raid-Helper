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
    <div className="flex items-center gap-2">
      <div className="w-32 h-2 rounded-full bg-white/10 overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-1000 ${
            urgent ? "bg-red-500" : "bg-gold"
          }`}
          style={{ width: `${pct * 100}%` }}
        />
      </div>
      <span
        className={`font-mono text-sm font-bold ${
          urgent ? "text-red-400" : "text-gold"
        }`}
      >
        {remaining}s
      </span>
    </div>
  );
}
