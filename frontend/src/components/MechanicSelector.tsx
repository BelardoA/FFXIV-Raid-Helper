"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchDrillPlan, fetchFight, fetchMechanic } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import type { DrillPlan, Fight, MechanicSummary } from "@/lib/types";

function Stars({ count }: { count: number }) {
  return (
    <span className="flex gap-0.5">
      {Array.from({ length: 5 }, (_, i) => (
        <span key={i} className="text-[0.6rem]" style={{ color: i < count ? "var(--color-gold)" : "rgba(255,255,255,0.1)" }}>★</span>
      ))}
    </span>
  );
}

export default function MechanicSelector() {
  const router = useRouter();
  const { fight, startDrill } = useAppStore();
  const [fightDetail, setFightDetail] = useState<Fight | null>(null);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);

  useEffect(() => {
    if (!fight) return;
    fetchFight(fight.slug).then(setFightDetail).finally(() => setLoading(false));
  }, [fight]);

  if (!fight) return null;

  const mechanics = fightDetail?.mechanics ?? [];

  const phaseOrder: string[] = [];
  const phases = new Map<string, MechanicSummary[]>();
  for (const m of mechanics) {
    const key = m.phase_name || "General";
    if (!phases.has(key)) { phases.set(key, []); phaseOrder.push(key); }
    phases.get(key)!.push(m);
  }

  const startFullFight = async () => {
    if (starting) return;
    setStarting(true);
    try {
      startDrill(await fetchDrillPlan(fight.slug));
      router.push(`/fights/${fight.slug}/drill`);
    } finally { setStarting(false); }
  };

  const startPhase = async (phaseName: string) => {
    if (starting) return;
    setStarting(true);
    try {
      startDrill(await fetchDrillPlan(fight.slug, phaseName));
      router.push(`/fights/${fight.slug}/drill`);
    } finally { setStarting(false); }
  };

  const startSingleMechanic = async (mech: MechanicSummary) => {
    if (starting) return;
    setStarting(true);
    try {
      const full = await fetchMechanic(mech.id);
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
      router.push(`/fights/${fight.slug}/drill`);
    } finally { setStarting(false); }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-32 gap-4">
        <div className="w-8 h-8 rounded-full animate-spin" style={{ border: "2px solid rgba(91,196,232,0.1)", borderTopColor: "var(--color-aether)" }} />
        <span className="font-cinzel text-xs tracking-[0.2em] text-muted uppercase animate-pulse">Loading mechanics…</span>
      </div>
    );
  }

  return (
    <section className="relative z-10 max-w-3xl mx-auto px-4 py-8">

      {/* Back */}
      <button
        onClick={() => router.push("/fights")}
        className="flex items-center gap-2 text-xs text-muted hover:text-gold-light transition-colors mb-8 font-cinzel tracking-wider group"
      >
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" className="transition-transform group-hover:-translate-x-0.5">
          <path d="M9 2L4 7l5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        All Fights
      </button>

      {/* Fight identity */}
      <div className="text-center mb-10 animate-fade-up">
        <div className="inline-flex flex-col items-center gap-2">
          <span className="font-cinzel text-[0.6rem] tracking-[0.3em] text-muted uppercase">{fight.name}</span>
          <h2 className="font-display text-2xl text-gold-light tracking-wider">{fight.short_name}</h2>
          <span className="text-sm text-body/60">{fight.boss_name}</span>
          <div className="flex items-center gap-3 mt-1">
            <div className="h-px w-10" style={{ background: "rgba(200,164,90,0.2)" }} />
            <span style={{ color: "rgba(200,164,90,0.35)", fontSize: "0.5rem" }}>◆</span>
            <div className="h-px w-10" style={{ background: "rgba(200,164,90,0.2)" }} />
          </div>
        </div>
      </div>

      {/* ── Run scope selectors ── */}
      {mechanics.length > 0 && (
        <div className="mb-10 animate-fade-up-1">
          <div className="flex items-center gap-3 mb-4">
            <span className="font-cinzel text-[0.6rem] tracking-[0.25em] text-muted uppercase">Run</span>
            <div className="flex-1 h-px" style={{ background: "rgba(91,196,232,0.08)" }} />
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <button
              onClick={startFullFight}
              disabled={starting}
              className="relative p-5 text-left panel-cut-sm transition-all duration-200 disabled:opacity-50 disabled:cursor-wait"
              style={{ background: "rgba(200,164,90,0.1)", border: "1px solid rgba(200,164,90,0.3)" }}
              onMouseEnter={(e) => { const el = e.currentTarget as HTMLElement; el.style.background = "rgba(200,164,90,0.17)"; el.style.borderColor = "rgba(200,164,90,0.55)"; el.style.boxShadow = "0 0 25px rgba(200,164,90,0.1)"; }}
              onMouseLeave={(e) => { const el = e.currentTarget as HTMLElement; el.style.background = "rgba(200,164,90,0.1)"; el.style.borderColor = "rgba(200,164,90,0.3)"; el.style.boxShadow = "none"; }}
            >
              <div className="font-display text-base text-gold-light mb-1">Full Fight</div>
              <div className="text-[0.7rem] text-gold/60 font-cinzel tracking-wide">
                {mechanics.length} mechanics · {mechanics.reduce((n, m) => n + m.step_count, 0)} steps
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
                  className="relative p-5 text-left transition-all duration-200 disabled:opacity-50 disabled:cursor-wait"
                  style={{ background: "rgba(12,21,37,0.9)", border: "1px solid rgba(91,196,232,0.1)" }}
                  onMouseEnter={(e) => { const el = e.currentTarget as HTMLElement; el.style.background = "rgba(17,30,56,0.95)"; el.style.borderColor = "rgba(200,164,90,0.25)"; }}
                  onMouseLeave={(e) => { const el = e.currentTarget as HTMLElement; el.style.background = "rgba(12,21,37,0.9)"; el.style.borderColor = "rgba(91,196,232,0.1)"; }}
                >
                  <div className="font-display text-sm text-body mb-1">{name}</div>
                  <div className="text-[0.68rem] text-muted font-cinzel tracking-wide">
                    {list.length} mechanic{list.length !== 1 ? "s" : ""} · {steps} step{steps !== 1 ? "s" : ""}
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* ── Individual mechanics ── */}
      <div className="animate-fade-up-2">
        <div className="flex items-center gap-3 mb-5">
          <span className="font-cinzel text-[0.6rem] tracking-[0.25em] text-muted uppercase">Single Mechanic</span>
          <div className="flex-1 h-px" style={{ background: "rgba(91,196,232,0.08)" }} />
        </div>
        {phaseOrder.map((phaseName) => (
          <div key={phaseName} className="mb-8">
            <div className="flex items-center gap-2 mb-3">
              <span className="inline-block h-3 w-0.5 rounded-full" style={{ background: "rgba(91,196,232,0.3)" }} aria-hidden />
              <h4 className="font-cinzel text-[0.65rem] text-muted tracking-[0.2em] uppercase">{phaseName}</h4>
            </div>
            <div className="space-y-2">
              {phases.get(phaseName)!.map((mech) => (
                <MechanicRow key={mech.id} mech={mech} disabled={starting} onClick={() => startSingleMechanic(mech)} />
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function MechanicRow({ mech, disabled, onClick }: { mech: MechanicSummary; disabled: boolean; onClick: () => void }) {
  const [hovered, setHovered] = useState(false);
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className="w-full text-left px-4 py-3.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-wait flex items-center justify-between gap-4"
      style={{
        background: hovered ? "rgba(17,30,56,0.95)" : "rgba(12,21,37,0.85)",
        border: `1px solid ${hovered ? "rgba(200,164,90,0.3)" : "rgba(91,196,232,0.08)"}`,
        borderLeft: `2px solid ${hovered ? "rgba(200,164,90,0.5)" : "rgba(91,196,232,0.15)"}`,
      }}
    >
      <div className="min-w-0">
        <div className="font-cinzel text-sm font-semibold tracking-wide truncate transition-colors" style={{ color: hovered ? "var(--color-gold-light)" : "var(--color-body)" }}>
          {mech.name}
        </div>
        <div className="flex items-center gap-2 mt-1.5 flex-wrap">
          {mech.tags.map((tag) => (
            <span key={tag} className="text-[0.55rem] px-1.5 py-0.5 tracking-wider font-cinzel" style={{ background: "rgba(91,196,232,0.06)", border: "1px solid rgba(91,196,232,0.12)", color: "var(--color-muted)", borderRadius: "2px" }}>
              {tag}
            </span>
          ))}
        </div>
      </div>
      <div className="flex items-center gap-4 shrink-0">
        <Stars count={mech.difficulty_rating} />
        <span className="font-mono text-[0.65rem] text-dim tabular-nums">{mech.step_count}s</span>
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className="transition-all duration-200" style={{ color: hovered ? "var(--color-gold)" : "var(--color-dim)", transform: hovered ? "translateX(2px)" : "none" }}>
          <path d="M2 6h8M6 2l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </div>
    </button>
  );
}
