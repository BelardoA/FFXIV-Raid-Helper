"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAppStore } from "@/lib/store";
import type { Role, Spot } from "@/lib/types";

/* ── Role SVG icons — colored via `color` prop ── */

function ShieldIcon({ color }: { color: string }) {
  return (
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
      <path
        d="M12 2L4 6v6c0 5.25 3.6 10.15 8 11.5 4.4-1.35 8-6.25 8-11.5V6L12 2z"
        fill={color}
        opacity="0.95"
      />
      <path
        d="M12 5L7 7.5v4c0 3.5 2.4 6.8 5 7.7 2.6-.9 5-4.2 5-7.7v-4L12 5z"
        fill="rgba(0,0,0,0.3)"
      />
    </svg>
  );
}

function CrossIcon({ color }: { color: string }) {
  return (
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
      <rect x="9.5" y="2" width="5" height="20" rx="1.5" fill={color} opacity="0.95" />
      <rect x="2" y="9.5" width="20" height="5" rx="1.5" fill={color} opacity="0.95" />
      {/* Inner highlight */}
      <rect x="10.5" y="3" width="3" height="4" rx="1" fill="rgba(255,255,255,0.2)" />
    </svg>
  );
}

function FistIcon({ color }: { color: string }) {
  return (
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
      {/* Four curled fingers */}
      <rect x="5"  y="5" width="3.2" height="6.5" rx="1.6" fill={color} />
      <rect x="9"  y="4" width="3.2" height="7.5" rx="1.6" fill={color} />
      <rect x="13" y="4" width="3.2" height="7.5" rx="1.6" fill={color} />
      <rect x="17" y="5" width="2.5" height="6.5" rx="1.2" fill={color} />
      {/* Palm */}
      <rect x="5" y="10" width="14.5" height="8" rx="2.5" fill={color} />
      {/* Thumb */}
      <rect x="2" y="12.5" width="6" height="3.5" rx="1.75" fill={color} />
      {/* Knuckle shadow lines */}
      <line x1="8.6"  y1="10" x2="8.6"  y2="16" stroke="rgba(0,0,0,0.2)" strokeWidth="1" />
      <line x1="12.2" y1="10" x2="12.2" y2="16" stroke="rgba(0,0,0,0.2)" strokeWidth="1" />
      <line x1="15.8" y1="10" x2="15.8" y2="16" stroke="rgba(0,0,0,0.2)" strokeWidth="1" />
      {/* Knuckle highlight */}
      <rect x="5" y="9" width="14.5" height="2.5" rx="1" fill="rgba(255,255,255,0.15)" />
    </svg>
  );
}

function MagicArrowIcon({ color }: { color: string }) {
  /* Star-tipped arrow: arrow shaft = ranged, 4-pointed star tip = caster/magic */
  return (
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
      {/* Arrow shaft */}
      <line
        x1="4" y1="21" x2="16.5" y2="8.5"
        stroke={color} strokeWidth="2" strokeLinecap="round"
      />
      {/* Fletching */}
      <path
        d="M4 21 L2 17 M4 21 L8 19"
        stroke={color} strokeWidth="1.4" strokeLinecap="round" opacity="0.7"
      />
      {/* 4-pointed star (magic tip) centered at 19,6 */}
      <path
        d="M19 2 L20.3 5 L23.5 6 L20.3 7 L19 10 L17.7 7 L14.5 6 L17.7 5 Z"
        fill={color} opacity="0.95"
      />
      {/* Inner star highlight */}
      <path
        d="M19 4 L19.7 5.5 L21.5 6 L19.7 6.5 L19 8 L18.3 6.5 L16.5 6 L18.3 5.5 Z"
        fill="rgba(255,255,255,0.35)"
      />
      {/* Magic sparkles radiating from star */}
      <line x1="19" y1="0.5" x2="19" y2="1.8" stroke={color} strokeWidth="1.2" strokeLinecap="round" opacity="0.5" />
      <line x1="23" y1="2" x2="22" y2="3" stroke={color} strokeWidth="1.2" strokeLinecap="round" opacity="0.5" />
      <line x1="23.5" y1="6" x2="22.5" y2="6" stroke={color} strokeWidth="1.2" strokeLinecap="round" opacity="0.4" />
    </svg>
  );
}

/* ── Role icon dispatcher ── */
function RoleIcon({ id, color }: { id: Role; color: string }) {
  if (id === "TANK")   return <ShieldIcon color={color} />;
  if (id === "HEALER") return <CrossIcon color={color} />;
  if (id === "MELEE")  return <FistIcon color={color} />;
  return <MagicArrowIcon color={color} />;
}

interface RoleConfig {
  id: Role;
  label: string;
  sub: string;
  color: string;
  glow: string;
  border: string;
  bg: string;
  spots: [string, string];
}

const ROLES: RoleConfig[] = [
  {
    id: "TANK",
    label: "Tank",
    sub: "Shield the party",
    color: "#5a9de8",
    glow: "rgba(74,144,226,0.3)",
    border: "rgba(74,144,226,0.45)",
    bg: "rgba(74,144,226,0.09)",
    spots: ["MT", "OT"],
  },
  {
    id: "HEALER",
    label: "Healer",
    sub: "Sustain & support",
    color: "#36d47e",
    glow: "rgba(46,203,122,0.28)",
    border: "rgba(46,203,122,0.45)",
    bg: "rgba(46,203,122,0.08)",
    spots: ["H1", "H2"],
  },
  {
    id: "MELEE",
    label: "Melee DPS",
    sub: "Close-range fury",
    color: "#f07060",
    glow: "rgba(232,80,64,0.28)",
    border: "rgba(232,80,64,0.45)",
    bg: "rgba(232,80,64,0.08)",
    spots: ["M1", "M2"],
  },
  {
    id: "RANGED",
    label: "Ranged DPS",
    sub: "Strike from afar",
    color: "#f07060",
    glow: "rgba(232,80,64,0.28)",
    border: "rgba(232,80,64,0.45)",
    bg: "rgba(232,80,64,0.08)",
    spots: ["R1", "R2"],
  },
];

export default function RoleSelector() {
  const router = useRouter();
  const selectRole = useAppStore((s) => s.selectRole);
  const [spot, setSpot] = useState<Spot>(1);
  const [hovered, setHovered] = useState<Role | null>(null);

  return (
    <section className="relative z-10 flex flex-col items-center px-4 pb-20 overflow-hidden">

      {/* ── Hero ── */}
      <div className="relative text-center pt-16 pb-12 max-w-xl mx-auto animate-fade-up">
        <div className="flex items-center gap-4 justify-center mb-6">
          <div className="h-px flex-1 max-w-16" style={{ background: "linear-gradient(90deg, transparent, rgba(200,164,90,0.4))" }} />
          <span className="font-cinzel text-[0.6rem] tracking-[0.35em] text-gold/70 uppercase">
            FFXIV · Patch 7.x
          </span>
          <div className="h-px flex-1 max-w-16" style={{ background: "linear-gradient(90deg, rgba(200,164,90,0.4), transparent)" }} />
        </div>

        <h1 className="font-display leading-none mb-2">
          <span className="block text-[clamp(0.9rem,2.5vw,1.1rem)] font-normal tracking-[0.3em] uppercase mb-3" style={{ color: "var(--color-muted)" }}>
            Master the
          </span>
          <span className="block text-[clamp(2.8rem,9vw,5.5rem)] font-bold text-shimmer leading-none">
            Mechanics
          </span>
        </h1>

        <div className="flex items-center justify-center gap-3 my-5">
          <div className="h-px w-12" style={{ background: "rgba(200,164,90,0.2)" }} />
          <span style={{ color: "rgba(200,164,90,0.4)", fontSize: "0.6rem" }}>◆</span>
          <div className="h-px w-12" style={{ background: "rgba(200,164,90,0.2)" }} />
        </div>

        <p className="text-sm leading-relaxed" style={{ color: "var(--color-muted)" }}>
          Interactive mechanic drills for{" "}
          <span style={{ color: "var(--color-body)" }}>M1S–M4S</span>,{" "}
          <span style={{ color: "var(--color-body)" }}>M9S–M12S</span>, and{" "}
          <span style={{ color: "var(--color-body)" }}>FRU</span>.
          <br />
          Train positioning before your next prog night.
        </p>
      </div>

      {/* ── Spot toggle ── */}
      <div className="animate-fade-up-1 mb-10 flex flex-col items-center gap-3">
        <span
          className="font-cinzel text-xs tracking-[0.25em] uppercase"
          style={{ color: "var(--color-muted)" }}
        >
          Party Slot
        </span>
        <div
          className="flex gap-1 p-1 rounded-sm"
          style={{ background: "rgba(91,196,232,0.05)", border: "1px solid rgba(91,196,232,0.1)" }}
        >
          {([1, 2] as Spot[]).map((s) => (
            <button
              key={s}
              onClick={() => setSpot(s)}
              className="px-8 py-2 rounded-sm font-cinzel text-xs tracking-widest transition-all duration-200"
              style={
                spot === s
                  ? { background: "rgba(200,164,90,0.18)", border: "1px solid rgba(200,164,90,0.45)", color: "var(--color-gold-light)" }
                  : { background: "transparent", border: "1px solid transparent", color: "var(--color-muted)" }
              }
            >
              Slot {s}
            </button>
          ))}
        </div>
      </div>

      {/* ── Role cards ── */}
      <div className="animate-fade-up-2 w-full max-w-3xl">
        <div className="flex items-center gap-4 justify-center mb-6">
          <div className="h-px flex-1" style={{ background: "rgba(91,196,232,0.1)" }} />
          <span
            className="font-cinzel text-[0.6rem] tracking-[0.28em] uppercase"
            style={{ color: "var(--color-muted)" }}
          >
            Select Role
          </span>
          <div className="h-px flex-1" style={{ background: "rgba(91,196,232,0.1)" }} />
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {ROLES.map((r, i) => {
            const isHovered = hovered === r.id;
            return (
              <button
                key={r.id}
                onClick={() => { selectRole(r.id, spot); router.push("/fights"); }}
                onMouseEnter={() => setHovered(r.id)}
                onMouseLeave={() => setHovered(null)}
                className="relative group flex flex-col items-center gap-3 px-4 py-7 panel-cut-sm transition-all duration-250"
                style={{
                  animationDelay: `${0.18 + i * 0.06}s`,
                  background: isHovered ? r.bg : "rgba(12,21,37,0.9)",
                  border: `1px solid ${isHovered ? r.border : "rgba(91,196,232,0.1)"}`,
                  boxShadow: isHovered ? `0 0 40px ${r.glow}, inset 0 0 30px ${r.glow}` : "none",
                }}
              >
                {/* Corner brackets */}
                <span
                  className="absolute top-0 left-0 w-3 h-3 transition-all duration-200"
                  style={{
                    borderTop: `2px solid ${isHovered ? r.color : "rgba(200,164,90,0.2)"}`,
                    borderLeft: `2px solid ${isHovered ? r.color : "rgba(200,164,90,0.2)"}`,
                  }}
                  aria-hidden
                />
                <span
                  className="absolute bottom-0 right-0 w-3 h-3 transition-all duration-200"
                  style={{
                    borderBottom: `2px solid ${isHovered ? r.color : "rgba(200,164,90,0.2)"}`,
                    borderRight: `2px solid ${isHovered ? r.color : "rgba(200,164,90,0.2)"}`,
                  }}
                  aria-hidden
                />

                {/* Colored SVG icon */}
                <div
                  className="transition-all duration-200"
                  style={{
                    filter: isHovered ? `drop-shadow(0 0 10px ${r.glow})` : "none",
                    transform: isHovered ? "scale(1.12)" : "scale(1)",
                  }}
                >
                  <RoleIcon id={r.id} color={r.color} />
                </div>

                {/* Label */}
                <div className="flex flex-col items-center gap-1">
                  <span
                    className="font-cinzel text-sm font-bold tracking-wider transition-colors"
                    style={{ color: isHovered ? r.color : "var(--color-body)" }}
                  >
                    {r.label}
                  </span>
                  <span
                    className="text-[0.6rem] tracking-wider"
                    style={{ color: "var(--color-muted)" }}
                  >
                    {r.sub}
                  </span>
                </div>

                {/* Spot badge */}
                <span
                  className="font-cinzel text-[0.65rem] tracking-[0.2em] px-3 py-1 rounded-sm transition-all duration-200"
                  style={{
                    background: isHovered ? r.bg : "rgba(255,255,255,0.04)",
                    border: `1px solid ${isHovered ? r.border : "rgba(255,255,255,0.08)"}`,
                    color: isHovered ? r.color : "var(--color-muted)",
                  }}
                >
                  {r.spots[spot - 1]}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* ── Bottom decoration ── */}
      <div className="animate-fade-up-3 mt-16 flex items-center gap-3">
        <div className="h-px w-8" style={{ background: "rgba(91,196,232,0.1)" }} />
        <span
          className="font-cinzel text-[0.55rem] tracking-[0.3em] uppercase"
          style={{ color: "var(--color-dim)" }}
        >
          Mechanic data sourced from community guides · Not affiliated with Square Enix
        </span>
        <div className="h-px w-8" style={{ background: "rgba(91,196,232,0.1)" }} />
      </div>
    </section>
  );
}
