"use client";

import { useAppStore } from "@/lib/store";

export default function Header() {
  const { phase, role, fight, reset, goToPhase } = useAppStore();

  return (
    <header className="sticky top-0 z-50 flex items-center justify-between px-6 py-3 bg-[#0d0d1a]/85 backdrop-blur-xl border-b border-[rgba(200,164,90,0.15)]">
      <button onClick={reset} className="flex items-center gap-3 group">
        <span className="text-2xl text-gold drop-shadow-[0_0_16px_rgba(200,164,90,0.6)]">
          &#x2694;
        </span>
        <span className="flex flex-col text-left">
          <span className="font-cinzel text-base font-black text-gold-light tracking-wider leading-none">
            RaidCoach
          </span>
          <span className="text-[0.6rem] text-text-muted tracking-[0.15em] uppercase">
            XIV Mechanic Trainer
          </span>
        </span>
      </button>

      {phase !== "role-select" && (
        <nav className="flex items-center gap-2 text-xs tracking-wide">
          {role && (
            <span className="px-2 py-1 rounded border border-gold/20 text-gold font-cinzel">
              {role}
            </span>
          )}
          {fight && phase !== "fight-browse" && (
            <>
              <span className="text-white/15">&rsaquo;</span>
              <button
                onClick={() => goToPhase("mechanic-select")}
                className="text-white/40 hover:text-gold-light transition-colors"
              >
                {fight.short_name}
              </button>
            </>
          )}
        </nav>
      )}
    </header>
  );
}
