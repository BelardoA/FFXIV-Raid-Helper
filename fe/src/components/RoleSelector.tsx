"use client";

import { useAppStore } from "@/lib/store";
import type { Role } from "@/lib/types";

const ROLES: { id: Role; label: string; icon: string; color: string }[] = [
  { id: "TANK", label: "Tank", icon: "🛡️", color: "#2b7fff" },
  { id: "HEALER", label: "Healer", icon: "💚", color: "#22c77a" },
  { id: "MELEE", label: "Melee DPS", icon: "⚔️", color: "#ff6b35" },
  { id: "RANGED", label: "Ranged DPS", icon: "🏹", color: "#f4c430" },
  { id: "CASTER", label: "Caster DPS", icon: "✨", color: "#b06aff" },
];

export default function RoleSelector() {
  const selectRole = useAppStore((s) => s.selectRole);

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
          Interactive mechanic drills for M1S&ndash;M4S and FRU.
          <br />
          Train your muscle memory before the next prog night.
        </p>
      </div>

      {/* Role cards */}
      <h2 className="font-cinzel text-lg text-gold-light tracking-wider mb-6">
        Select Your Role
      </h2>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4 max-w-3xl w-full mb-16">
        {ROLES.map((r) => (
          <button
            key={r.id}
            onClick={() => selectRole(r.id)}
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
          </button>
        ))}
      </div>
    </section>
  );
}
