"use client";

import { useState } from "react";
import { useAppStore } from "@/lib/store";
import type { Role, Spot } from "@/lib/types";

const ROLES: { id: Role; label: string; icon: string; color: string; spots: [string, string] }[] = [
  { id: "TANK", label: "Tank", icon: "\u{1F6E1}", color: "#2b7fff", spots: ["MT", "OT"] },
  { id: "HEALER", label: "Healer", icon: "\u{1F49A}", color: "#22c77a", spots: ["H1", "H2"] },
  { id: "MELEE", label: "Melee DPS", icon: "\u2694", color: "#ff6b35", spots: ["M1", "M2"] },
  { id: "RANGED", label: "Ranged DPS", icon: "\u{1F3F9}", color: "#f4c430", spots: ["R1", "R2"] },
];

export default function RoleSelector() {
  const selectRole = useAppStore((s) => s.selectRole);
  const [spot, setSpot] = useState<Spot>(1);

  return (
    <section className="flex flex-col items-center px-4">
      {/* Hero */}
      <div className="relative text-center py-16">
        <p className="text-xs tracking-[0.3em] text-gold font-cinzel mb-4">
          FFXIV &bull; Patch 7.x
        </p>
        <h1 className="font-cinzel leading-none mb-4">
          <span className="block text-[clamp(1.5rem,4vw,2.5rem)] font-normal text-text-muted tracking-wider">
            Master the
          </span>
          <span className="block text-[clamp(2.5rem,8vw,5rem)] font-black bg-gradient-to-br from-gold-light via-gold to-gold-dark bg-clip-text text-transparent">
            Mechanics
          </span>
        </h1>
        <p className="text-sm text-text-muted max-w-md mx-auto leading-relaxed">
          Interactive mechanic drills for M1S&ndash;M4S, M9S&ndash;M12S, and FRU.
          <br />
          Train your muscle memory before the next prog night.
        </p>
      </div>

      {/* Spot toggle */}
      <h2 className="font-cinzel text-lg text-gold-light tracking-wider mb-3">
        Party Slot
      </h2>
      <div className="flex gap-2 mb-8">
        {([1, 2] as Spot[]).map((s) => (
          <button
            key={s}
            onClick={() => setSpot(s)}
            className={`px-6 py-2 rounded-lg border font-cinzel text-sm tracking-wider transition-all ${
              spot === s
                ? "border-gold bg-gold/20 text-gold-light"
                : "border-white/10 bg-bg-card text-white/50 hover:border-gold/30"
            }`}
          >
            Spot {s}
          </button>
        ))}
      </div>

      {/* Role cards */}
      <h2 className="font-cinzel text-lg text-gold-light tracking-wider mb-6">
        Select Your Role
      </h2>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-3xl w-full mb-16">
        {ROLES.map((r) => (
          <button
            key={r.id}
            onClick={() => selectRole(r.id, spot)}
            className="group flex flex-col items-center gap-3 p-6 rounded-xl border border-white/5 bg-bg-card hover:bg-bg-card-hover hover:border-gold/30 transition-all duration-200"
          >
            <span className="text-3xl group-hover:scale-110 transition-transform">
              {r.icon}
            </span>
            <span
              className="font-cinzel text-sm font-bold tracking-wider"
              style={{ color: r.color }}
            >
              {r.label}
            </span>
            <span className="text-[0.65rem] tracking-[0.2em] text-white/40 font-cinzel">
              {r.spots[spot - 1]}
            </span>
          </button>
        ))}
      </div>
    </section>
  );
}
