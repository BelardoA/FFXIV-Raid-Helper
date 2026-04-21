"use client";

import { useEffect, useState } from "react";

interface TimerProps {
  seconds: number;
  running: boolean;
  onExpire: () => void;
}

export default function Timer({ seconds, running, onExpire }: TimerProps) {
  const [remaining, setRemaining] = useState(seconds);

  useEffect(() => {
    if (!running || remaining <= 0) return;
    const interval = setInterval(() => {
      setRemaining((prev) => {
        if (prev <= 1) {
          onExpire();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [running, remaining, onExpire]);

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
