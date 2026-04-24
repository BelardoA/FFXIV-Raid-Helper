"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchRaidTiers, fetchFights } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import type { Fight, RaidTier } from "@/lib/types";

function DifficultyBadge({ difficulty }: { difficulty: string }) {
  const cls =
    difficulty === "ULTIMATE"
      ? "badge-ultimate"
      : difficulty === "SAVAGE"
        ? "badge-savage"
        : "badge-normal";
  return (
    <span className={`${cls} font-cinzel text-[0.55rem] px-2 py-0.5 tracking-[0.18em] uppercase rounded-sm`}>
      {difficulty}
    </span>
  );
}

function FightCard({ fight, onClick }: { fight: Fight; onClick: () => void }) {
  const [hovered, setHovered] = useState(false);
  const accentColor =
    fight.difficulty === "ULTIMATE"
      ? "rgba(130,50,210,0.6)"
      : fight.difficulty === "SAVAGE"
        ? "rgba(200,70,20,0.6)"
        : "rgba(200,164,90,0.4)";

  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className="relative group text-left transition-all duration-250 overflow-hidden"
      style={{
        background: hovered ? "rgba(17,30,56,0.95)" : "rgba(12,21,37,0.9)",
        border: `1px solid ${hovered ? "rgba(200,164,90,0.3)" : "rgba(91,196,232,0.1)"}`,
        boxShadow: hovered ? "0 0 30px rgba(200,164,90,0.06)" : "none",
      }}
    >
      {/* Left accent bar */}
      <div
        className="absolute left-0 top-0 bottom-0 w-0.5 transition-all duration-200"
        style={{ background: hovered ? accentColor : "rgba(91,196,232,0.15)" }}
      />

      {/* Corner brackets */}
      <span
        className="absolute top-0 left-0 w-3 h-3 transition-all duration-200 pointer-events-none"
        style={{
          borderTop: `2px solid ${hovered ? "rgba(200,164,90,0.6)" : "rgba(200,164,90,0.2)"}`,
          borderLeft: `2px solid ${hovered ? "rgba(200,164,90,0.6)" : "rgba(200,164,90,0.2)"}`,
        }}
        aria-hidden
      />
      <span
        className="absolute bottom-0 right-0 w-3 h-3 transition-all duration-200 pointer-events-none"
        style={{
          borderBottom: `2px solid ${hovered ? "rgba(200,164,90,0.6)" : "rgba(200,164,90,0.2)"}`,
          borderRight: `2px solid ${hovered ? "rgba(200,164,90,0.6)" : "rgba(200,164,90,0.2)"}`,
        }}
        aria-hidden
      />

      <div className="pl-5 pr-4 py-5">
        <div className="flex items-start justify-between gap-2 mb-2">
          <div className="flex items-center gap-2.5 flex-wrap">
            <span
              className="font-display text-base font-bold transition-colors"
              style={{ color: hovered ? "var(--color-gold-light)" : "var(--color-body)" }}
            >
              {fight.short_name}
            </span>
            <DifficultyBadge difficulty={fight.difficulty} />
          </div>
          <span className="font-cinzel text-[0.6rem] tracking-widest text-muted shrink-0 mt-0.5">
            {fight.mechanic_count} <span className="text-dim">mechs</span>
          </span>
        </div>
        <p className="text-sm text-body/70 mb-0.5">{fight.boss_name}</p>
        <p className="text-[0.7rem] text-muted tracking-wide">{fight.name}</p>
      </div>
    </button>
  );
}

export default function FightBrowser() {
  const router = useRouter();
  const selectFight = useAppStore((s) => s.selectFight);
  const [tiers, setTiers] = useState<RaidTier[]>([]);
  const [fights, setFights] = useState<Fight[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([fetchRaidTiers(), fetchFights()])
      .then(([t, f]) => { setTiers(t); setFights(f); })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-32 gap-4">
        <div
          className="w-8 h-8 rounded-full animate-spin"
          style={{ border: "2px solid rgba(91,196,232,0.1)", borderTopColor: "var(--color-aether)" }}
        />
        <span className="font-cinzel text-xs tracking-[0.2em] text-muted uppercase animate-pulse">
          Loading encounters…
        </span>
      </div>
    );
  }

  return (
    <section className="relative z-10 max-w-4xl mx-auto px-4 py-10">

      {/* Section header */}
      <div className="text-center mb-12 animate-fade-up">
        <span className="font-cinzel text-[0.6rem] tracking-[0.3em] text-muted uppercase">
          Select Encounter
        </span>
        <h2 className="font-display text-2xl text-gold-light mt-2 tracking-wider">
          Choose a Fight
        </h2>
      </div>

      {tiers.map((tier, ti) => {
        const tierFights = fights.filter((f) => f.raid_tier_name === tier.name);
        if (tierFights.length === 0) return null;

        return (
          <div
            key={tier.slug}
            className="mb-12 animate-fade-up"
            style={{ animationDelay: `${ti * 0.1}s` }}
          >
            {/* Tier header */}
            <div className="flex items-center gap-4 mb-5">
              <div className="flex flex-col">
                <span className="font-cinzel text-base text-gold tracking-wider">
                  {tier.name}
                </span>
                <span className="font-cinzel text-[0.6rem] tracking-[0.18em] text-muted uppercase">
                  {tier.expansion} · Patch {tier.patch}
                </span>
              </div>
              <div
                className="flex-1 h-px"
                style={{ background: "linear-gradient(90deg, rgba(200,164,90,0.25), transparent)" }}
              />
            </div>

            {/* Fight grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {tierFights.map((fight) => (
                <FightCard
                  key={fight.slug}
                  fight={fight}
                  onClick={() => { selectFight(fight); router.push(`/fights/${fight.slug}`); }}
                />
              ))}
            </div>
          </div>
        );
      })}
    </section>
  );
}
