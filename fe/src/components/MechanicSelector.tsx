"use client";

import { useEffect, useState } from "react";
import { fetchFight, fetchMechanic } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import type { Fight, MechanicSummary } from "@/lib/types";

function Stars({ count }: { count: number }) {
  return (
    <span className="text-xs tracking-wider">
      {Array.from({ length: 5 }, (_, i) => (
        <span key={i} className={i < count ? "text-gold" : "text-white/15"}>
          ★
        </span>
      ))}
    </span>
  );
}

export default function MechanicSelector() {
  const { fight, selectMechanic, goToPhase } = useAppStore();
  const [fightDetail, setFightDetail] = useState<Fight | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!fight) return;
    fetchFight(fight.slug)
      .then(setFightDetail)
      .finally(() => setLoading(false));
  }, [fight]);

  if (!fight) return null;

  const handleSelect = async (mech: MechanicSummary) => {
    const full = await fetchMechanic(mech.id);
    selectMechanic(full);
  };

  if (loading) {
    return (
      <div className="flex justify-center py-24">
        <span className="text-gold animate-pulse font-cinzel">
          Loading mechanics...
        </span>
      </div>
    );
  }

  const mechanics = fightDetail?.mechanics ?? [];

  // Group by phase
  const phases = new Map<string, MechanicSummary[]>();
  for (const m of mechanics) {
    const key = m.phase_name || "General";
    if (!phases.has(key)) phases.set(key, []);
    phases.get(key)!.push(m);
  }

  return (
    <section className="max-w-3xl mx-auto px-4 py-8">
      <button
        onClick={() => goToPhase("fight-browse")}
        className="text-xs text-text-muted hover:text-gold-light transition-colors mb-6 block"
      >
        &larr; Back to fights
      </button>

      <div className="text-center mb-8">
        <h2 className="font-cinzel text-2xl text-gold-light tracking-wider">
          {fight.short_name} &mdash; {fight.boss_name}
        </h2>
        <p className="text-sm text-text-muted mt-1">{fight.name}</p>
      </div>

      {Array.from(phases.entries()).map(([phaseName, mechs]) => (
        <div key={phaseName} className="mb-8">
          <h3 className="font-cinzel text-sm text-gold tracking-[0.15em] uppercase mb-3">
            {phaseName}
          </h3>
          <div className="space-y-3">
            {mechs.map((mech) => (
              <button
                key={mech.id}
                onClick={() => handleSelect(mech)}
                className="group w-full text-left p-4 rounded-xl border border-white/5 bg-bg-card hover:bg-bg-card-hover hover:border-gold/30 transition-all duration-200"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-cinzel text-base font-bold text-gold-light group-hover:text-gold transition-colors">
                    {mech.name}
                  </span>
                  <Stars count={mech.difficulty_rating} />
                </div>
                <p className="text-sm text-white/40 mb-2">{mech.description}</p>
                <div className="flex items-center gap-2 flex-wrap">
                  {mech.tags.map((tag) => (
                    <span
                      key={tag}
                      className="text-[0.6rem] px-2 py-0.5 rounded-full bg-white/5 text-white/30"
                    >
                      {tag}
                    </span>
                  ))}
                  <span className="text-[0.6rem] text-text-muted ml-auto">
                    {mech.step_count} step{mech.step_count !== 1 ? "s" : ""}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>
      ))}
    </section>
  );
}
