"use client";

import { useRouter } from "next/navigation";
import { useAppStore } from "@/lib/store";
import type { Mechanic, MechanicStep } from "@/lib/types";

const GRADE_CONFIG: Record<string, { color: string; glow: string; label: string }> = {
  S: { color: "#f2cc70", glow: "rgba(242,204,112,0.35)", label: "Flawless" },
  A: { color: "#4de89a", glow: "rgba(77,232,154,0.3)",  label: "Excellent" },
  B: { color: "#5bc4e8", glow: "rgba(91,196,232,0.3)",  label: "Good" },
  C: { color: "#f0b030", glow: "rgba(240,176,48,0.28)", label: "Average" },
  D: { color: "#f07060", glow: "rgba(240,112,96,0.3)",  label: "Keep Practicing" },
};

function computeGrade(accuracy: number): string {
  if (accuracy >= 0.95) return "S";
  if (accuracy >= 0.85) return "A";
  if (accuracy >= 0.70) return "B";
  if (accuracy >= 0.50) return "C";
  return "D";
}

export default function DrillResults() {
  const router = useRouter();
  const { drillPlan, role, stepResults, reset, startDrill } = useAppStore();
  if (!drillPlan || !role) return null;

  const total    = stepResults.length;
  const correct  = stepResults.filter((r) => r.result.is_correct).length;
  const accuracy = total > 0 ? correct / total : 0;
  const grade    = computeGrade(accuracy);
  const gc       = GRADE_CONFIG[grade];
  const avgTime  = total > 0
    ? Math.round(stepResults.reduce((s, r) => s + r.timeTakenMs, 0) / total)
    : 0;

  const scopeLabel =
    drillPlan.scope === "full"
      ? "Full Fight"
      : drillPlan.mechanics.length === 1
        ? "Single Mechanic"
        : drillPlan.scope;

  const mechanicsById = new Map<number, Mechanic>(
    drillPlan.mechanics.map((m) => [m.id, m])
  );
  const perMechanic = drillPlan.mechanics
    .map((mech) => {
      const results = stepResults.filter((r) => r.mechanicId === mech.id);
      if (results.length === 0) return null;
      const ok = results.filter((r) => r.result.is_correct).length;
      return { mech, total: results.length, correct: ok, accuracy: ok / results.length };
    })
    .filter((e): e is NonNullable<typeof e> => e !== null);

  const findStep = (mechanicId: number, stepId: number): MechanicStep | undefined =>
    mechanicsById.get(mechanicId)?.steps.find((s) => s.id === stepId);

  return (
    <section className="relative z-10 max-w-lg mx-auto px-4 py-12 text-center">

      {/* ── Fight label ── */}
      <div className="mb-8 animate-fade-up">
        <span className="font-cinzel text-[0.6rem] tracking-[0.3em] text-muted uppercase">
          {drillPlan.fight.short_name} · {scopeLabel}
        </span>
        <h2 className="font-display text-xl text-gold-light mt-1 tracking-wider">Drill Complete</h2>
        <div className="flex items-center justify-center gap-3 mt-3">
          <div className="h-px w-12" style={{ background: "rgba(200,164,90,0.2)" }} />
          <span style={{ color: "rgba(200,164,90,0.35)", fontSize: "0.5rem" }}>◆</span>
          <div className="h-px w-12" style={{ background: "rgba(200,164,90,0.2)" }} />
        </div>
      </div>

      {/* ── Grade ── */}
      <div className="mb-10 animate-fade-up-1">
        <div
          className="inline-flex flex-col items-center justify-center w-36 h-36 mx-auto rounded-full mb-4 grade-reveal"
          style={{
            background: `radial-gradient(circle, ${gc.glow} 0%, rgba(12,21,37,0.95) 70%)`,
            border: `2px solid ${gc.color}`,
            boxShadow: `0 0 60px ${gc.glow}, inset 0 0 40px ${gc.glow}`,
          }}
        >
          <span
            className="font-display text-7xl font-bold leading-none"
            style={{ color: gc.color, textShadow: `0 0 30px ${gc.glow}` }}
          >
            {grade}
          </span>
        </div>
        <p className="font-cinzel text-sm tracking-[0.2em] uppercase" style={{ color: gc.color }}>
          {gc.label}
        </p>
      </div>

      {/* ── Stats row ── */}
      <div className="grid grid-cols-3 gap-3 mb-10 animate-fade-up-2">
        {[
          { value: `${correct}/${total}`, label: "Correct" },
          { value: `${(accuracy * 100).toFixed(0)}%`, label: "Accuracy" },
          { value: `${(avgTime / 1000).toFixed(1)}s`, label: "Avg Time" },
        ].map((stat) => (
          <div
            key={stat.label}
            className="py-5 flex flex-col items-center gap-1"
            style={{ background: "rgba(12,21,37,0.9)", border: "1px solid rgba(91,196,232,0.1)" }}
          >
            <span className="font-display text-2xl font-bold text-gold-light">{stat.value}</span>
            <span className="font-cinzel text-[0.6rem] tracking-[0.2em] text-muted uppercase">{stat.label}</span>
          </div>
        ))}
      </div>

      {/* ── Mechanic breakdown ── */}
      {perMechanic.length > 1 && (
        <div className="mb-8 text-left animate-fade-up-3">
          <div className="flex items-center gap-3 mb-4">
            <span className="font-cinzel text-[0.6rem] tracking-[0.25em] text-muted uppercase">Mechanic Breakdown</span>
            <div className="flex-1 h-px" style={{ background: "rgba(91,196,232,0.08)" }} />
          </div>
          <div className="space-y-2">
            {perMechanic.map(({ mech, total: t, correct: c, accuracy: a }) => {
              const pct = Math.round(a * 100);
              const barColor = a >= 0.85 ? "#4de89a" : a >= 0.6 ? "#f2cc70" : "#f07060";
              return (
                <div
                  key={mech.id}
                  className="px-4 py-3"
                  style={{ background: "rgba(12,21,37,0.85)", border: "1px solid rgba(91,196,232,0.08)" }}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-body/80 font-cinzel">{mech.name}</span>
                    <span className="font-mono text-xs text-muted">{c}/{t}</span>
                  </div>
                  <div className="lb-gauge">
                    <div
                      className="lb-fill"
                      style={{
                        width: `${pct}%`,
                        background: `linear-gradient(90deg, ${barColor}88, ${barColor})`,
                        boxShadow: `0 0 8px ${barColor}66`,
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ── Step breakdown ── */}
      <div className="mb-10 text-left animate-fade-up-3">
        <div className="flex items-center gap-3 mb-4">
          <span className="font-cinzel text-[0.6rem] tracking-[0.25em] text-muted uppercase">Step Breakdown</span>
          <div className="flex-1 h-px" style={{ background: "rgba(91,196,232,0.08)" }} />
        </div>
        <div className="space-y-1.5">
          {stepResults.map((r, i) => {
            const mech = mechanicsById.get(r.mechanicId);
            const step = findStep(r.mechanicId, r.stepId);
            return (
              <div
                key={i}
                className="flex items-center justify-between px-3 py-2.5"
                style={
                  r.result.is_correct
                    ? { background: "rgba(46,203,122,0.05)", border: "1px solid rgba(46,203,122,0.18)", borderLeft: "2px solid rgba(46,203,122,0.4)" }
                    : { background: "rgba(232,80,64,0.05)",  border: "1px solid rgba(232,80,64,0.18)",  borderLeft: "2px solid rgba(232,80,64,0.4)" }
                }
              >
                <div className="flex items-center gap-2.5 min-w-0">
                  <span
                    className="text-xs font-bold shrink-0"
                    style={{ color: r.result.is_correct ? "#4de89a" : "#f07060" }}
                  >
                    {r.result.is_correct ? "✓" : "✗"}
                  </span>
                  <div className="min-w-0">
                    <p className="text-sm text-body/70 truncate">{step?.title || `Step ${i + 1}`}</p>
                    {mech && drillPlan.mechanics.length > 1 && (
                      <p className="text-[0.6rem] text-muted font-cinzel tracking-wide">{mech.name}</p>
                    )}
                  </div>
                </div>
                <span className="font-mono text-[0.65rem] text-dim tabular-nums shrink-0 ml-3">
                  {(r.timeTakenMs / 1000).toFixed(1)}s
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* ── Actions ── */}
      <div className="flex gap-3 animate-fade-up-4">
        <button
          onClick={() => { startDrill(drillPlan); router.push(`/fights/${drillPlan.fight.slug}/drill`); }}
          className="flex-1 py-3.5 font-cinzel tracking-widest text-xs transition-all duration-200"
          style={{ background: "rgba(200,164,90,0.12)", border: "1px solid rgba(200,164,90,0.35)", color: "var(--color-gold-light)" }}
          onMouseEnter={(e) => {
            const el = e.currentTarget as HTMLElement;
            el.style.background = "rgba(200,164,90,0.2)";
            el.style.borderColor = "rgba(200,164,90,0.6)";
          }}
          onMouseLeave={(e) => {
            const el = e.currentTarget as HTMLElement;
            el.style.background = "rgba(200,164,90,0.12)";
            el.style.borderColor = "rgba(200,164,90,0.35)";
          }}
        >
          Retry
        </button>
        <button
          onClick={() => router.push(`/fights/${drillPlan.fight.slug}`)}
          className="flex-1 py-3.5 font-cinzel tracking-widest text-xs transition-all duration-200"
          style={{ background: "transparent", border: "1px solid rgba(91,196,232,0.12)", color: "var(--color-muted)" }}
          onMouseEnter={(e) => {
            const el = e.currentTarget as HTMLElement;
            el.style.borderColor = "rgba(91,196,232,0.25)";
            el.style.color = "var(--color-aether-light)";
          }}
          onMouseLeave={(e) => {
            const el = e.currentTarget as HTMLElement;
            el.style.borderColor = "rgba(91,196,232,0.12)";
            el.style.color = "var(--color-muted)";
          }}
        >
          Mechanics
        </button>
        <button
          onClick={() => { reset(); router.push("/"); }}
          className="flex-1 py-3.5 font-cinzel tracking-widest text-xs transition-all duration-200"
          style={{ background: "transparent", border: "1px solid rgba(91,196,232,0.12)", color: "var(--color-muted)" }}
          onMouseEnter={(e) => {
            const el = e.currentTarget as HTMLElement;
            el.style.borderColor = "rgba(91,196,232,0.25)";
            el.style.color = "var(--color-aether-light)";
          }}
          onMouseLeave={(e) => {
            const el = e.currentTarget as HTMLElement;
            el.style.borderColor = "rgba(91,196,232,0.12)";
            el.style.color = "var(--color-muted)";
          }}
        >
          Start Over
        </button>
      </div>
    </section>
  );
}
