"use client";

import { useEffect, useState } from "react";
import { fetchDrillPlan, fetchFight, fetchMechanic } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import type { DrillPlan, Fight, MechanicSummary } from "@/lib/types";

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
  const { fight, startDrill, goToPhase } = useAppStore();
  const [fightDetail, setFightDetail] = useState<Fight | null>(null);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);

  useEffect(() => {
    if (!fight) return;
    fetchFight(fight.slug)
      .then(setFightDetail)
      .finally(() => setLoading(false));
  }, [fight]);

  if (!fight) return null;

  const mechanics = fightDetail?.mechanics ?? [];

  // Distinct phase names in first-appearance order.
  const phaseOrder: string[] = [];
  const phases = new Map<string, MechanicSummary[]>();
  for (const m of mechanics) {
    const key = m.phase_name || "General";
    if (!phases.has(key)) {
      phases.set(key, []);
      phaseOrder.push(key);
    }
    phases.get(key)!.push(m);
  }

  const startFullFight = async () => {
    if (starting) return;
    setStarting(true);
    try {
      const plan = await fetchDrillPlan(fight.slug);
      startDrill(plan);
    } finally {
      setStarting(false);
    }
  };

  const startPhase = async (phaseName: string) => {
    if (starting) return;
    setStarting(true);
    try {
      const plan = await fetchDrillPlan(fight.slug, phaseName);
      startDrill(plan);
    } finally {
      setStarting(false);
    }
  };

  const startSingleMechanic = async (mech: MechanicSummary) => {
    if (starting) return;
    setStarting(true);
    try {
      const full = await fetchMechanic(mech.id);
      // Synthesise a single-mechanic DrillPlan so DrillView only knows one shape.
      const plan: DrillPlan = {
        scope: full.name,
        fight: {
          slug: fight.slug,
          short_name: fight.short_name,
          name: fight.name,
          boss_name: fight.boss_name,
          arena_shape: fight.arena_shape,
          arena_image_url: fight.arena_image_url ?? "",
          boss_image_url: fight.boss_image_url ?? "",
        },
        mechanics: [full],
      };
      startDrill(plan);
    } finally {
      setStarting(false);
    }
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

      {/* Scope selectors — full fight + per-phase */}
      {mechanics.length > 0 && (
        <div className="mb-10">
          <h3 className="font-cinzel text-sm text-gold tracking-[0.15em] uppercase mb-3">
            Run the Fight
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <button
              onClick={startFullFight}
              disabled={starting}
              className="p-4 rounded-xl border border-gold/30 bg-gold/10 hover:bg-gold/20 text-gold-light font-cinzel tracking-wider transition-colors disabled:opacity-50 disabled:cursor-wait text-left"
            >
              <div className="text-base font-bold">Full Fight</div>
              <div className="text-[0.7rem] text-gold/70 tracking-wide mt-1">
                {mechanics.length} mechanics &middot;{" "}
                {mechanics.reduce((n, m) => n + m.step_count, 0)} steps
              </div>
            </button>
            {phaseOrder.map((name) => {
              const list = phases.get(name)!;
              const steps = list.reduce((n, m) => n + m.step_count, 0);
              return (
                <button
                  key={name}
                  onClick={() => startPhase(name)}
                  disabled={starting}
                  className="p-4 rounded-xl border border-white/10 bg-bg-card hover:border-gold/30 hover:bg-bg-card-hover font-cinzel tracking-wider transition-colors disabled:opacity-50 disabled:cursor-wait text-left"
                >
                  <div className="text-base font-bold text-gold-light">{name}</div>
                  <div className="text-[0.7rem] text-text-muted tracking-wide mt-1">
                    {list.length} mechanic{list.length !== 1 ? "s" : ""} &middot;{" "}
                    {steps} step{steps !== 1 ? "s" : ""}
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Individual mechanic selectors, still grouped by phase */}
      <h3 className="font-cinzel text-sm text-gold tracking-[0.15em] uppercase mb-3">
        Or drill a single mechanic
      </h3>
      {phaseOrder.map((phaseName) => (
        <div key={phaseName} className="mb-8">
          <h4 className="font-cinzel text-xs text-text-muted tracking-[0.15em] uppercase mb-3">
            {phaseName}
          </h4>
          <div className="space-y-3">
            {phases.get(phaseName)!.map((mech) => (
              <button
                key={mech.id}
                onClick={() => startSingleMechanic(mech)}
                disabled={starting}
                className="group w-full text-left p-4 rounded-xl border border-white/5 bg-bg-card hover:bg-bg-card-hover hover:border-gold/30 transition-all duration-200 disabled:opacity-50 disabled:cursor-wait"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-cinzel text-base font-bold text-gold-light group-hover:text-gold transition-colors">
                    {mech.name}
                  </span>
                  <Stars count={mech.difficulty_rating} />
                </div>
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
