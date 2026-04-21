"use client";

import { useAppStore } from "@/lib/store";
import type { Mechanic, MechanicStep } from "@/lib/types";

const GRADE_COLORS: Record<string, string> = {
  S: "text-yellow-400",
  A: "text-green-400",
  B: "text-blue-400",
  C: "text-orange-400",
  D: "text-red-400",
};

function computeGrade(accuracy: number): string {
  if (accuracy >= 0.95) return "S";
  if (accuracy >= 0.85) return "A";
  if (accuracy >= 0.7) return "B";
  if (accuracy >= 0.5) return "C";
  return "D";
}

export default function DrillResults() {
  const { drillPlan, role, stepResults, reset, goToPhase, startDrill } =
    useAppStore();

  if (!drillPlan || !role) return null;

  const total = stepResults.length;
  const correct = stepResults.filter((r) => r.result.is_correct).length;
  const accuracy = total > 0 ? correct / total : 0;
  const grade = computeGrade(accuracy);
  const avgTime =
    total > 0
      ? Math.round(
          stepResults.reduce((sum, r) => sum + r.timeTakenMs, 0) / total
        )
      : 0;
  const scopeLabel =
    drillPlan.scope === "full"
      ? "Full Fight"
      : drillPlan.mechanics.length === 1
        ? "Single Mechanic"
        : drillPlan.scope;

  const mechanicsById = new Map<number, Mechanic>(
    drillPlan.mechanics.map((mechanic) => [mechanic.id, mechanic])
  );
  const perMechanic = drillPlan.mechanics
    .map((mechanic) => {
      const results = stepResults.filter((record) => record.mechanicId === mechanic.id);
      if (results.length === 0) return null;
      const correctCount = results.filter((record) => record.result.is_correct).length;
      return {
        mechanic,
        total: results.length,
        correct: correctCount,
        accuracy: correctCount / results.length,
      };
    })
    .filter((entry): entry is NonNullable<typeof entry> => entry !== null);

  const findStep = (mechanicId: number, stepId: number): MechanicStep | undefined =>
    mechanicsById.get(mechanicId)?.steps.find((step) => step.id === stepId);

  return (
    <section className="max-w-lg mx-auto px-4 py-12 text-center">
      <h2 className="font-cinzel text-2xl text-gold-light tracking-wider mb-8">
        Drill Complete
      </h2>

      {/* Grade */}
      <div className="mb-8">
        <span
          className={`font-cinzel text-8xl font-black ${GRADE_COLORS[grade] || "text-white"}`}
        >
          {grade}
        </span>
        <p className="text-sm text-text-muted mt-2">
          {drillPlan.fight.short_name} &mdash; {scopeLabel}
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="p-4 rounded-xl bg-bg-card border border-white/5">
          <p className="font-cinzel text-2xl font-bold text-gold-light">
            {correct}/{total}
          </p>
          <p className="text-xs text-text-muted">Correct</p>
        </div>
        <div className="p-4 rounded-xl bg-bg-card border border-white/5">
          <p className="font-cinzel text-2xl font-bold text-gold-light">
            {(accuracy * 100).toFixed(0)}%
          </p>
          <p className="text-xs text-text-muted">Accuracy</p>
        </div>
        <div className="p-4 rounded-xl bg-bg-card border border-white/5">
          <p className="font-cinzel text-2xl font-bold text-gold-light">
            {(avgTime / 1000).toFixed(1)}s
          </p>
          <p className="text-xs text-text-muted">Avg Time</p>
        </div>
      </div>

      {perMechanic.length > 1 && (
        <div className="mb-8 text-left">
          <h3 className="font-cinzel text-sm text-gold tracking-[0.15em] uppercase mb-3">
            Mechanic Breakdown
          </h3>
          <div className="space-y-2">
            {perMechanic.map(({ mechanic, total, correct, accuracy: mechanicAccuracy }) => (
              <div
                key={mechanic.id}
                className="flex items-center justify-between p-3 rounded-lg border border-white/5 bg-bg-card"
              >
                <div>
                  <p className="text-sm text-white/70">{mechanic.name}</p>
                  <p className="text-[0.65rem] text-text-muted">
                    {correct}/{total} correct
                  </p>
                </div>
                <span className="font-cinzel text-sm text-gold-light">
                  {(mechanicAccuracy * 100).toFixed(0)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Per-step breakdown */}
      <div className="mb-8 text-left">
        <h3 className="font-cinzel text-sm text-gold tracking-[0.15em] uppercase mb-3">
          Step Breakdown
        </h3>
        <div className="space-y-2">
          {stepResults.map((r, i) => {
            const mechanic = mechanicsById.get(r.mechanicId);
            const step = findStep(r.mechanicId, r.stepId);
            return (
              <div
                key={i}
                className={`flex items-center justify-between p-3 rounded-lg border ${
                  r.result.is_correct
                    ? "border-green-500/20 bg-green-500/5"
                    : "border-red-500/20 bg-red-500/5"
                }`}
              >
                <div className="flex items-center gap-2">
                  <span
                    className={`text-sm font-bold ${
                      r.result.is_correct ? "text-green-400" : "text-red-400"
                    }`}
                  >
                    {r.result.is_correct ? "\u2713" : "\u2717"}
                  </span>
                  <div className="text-left">
                    <p className="text-sm text-white/60">
                      {step?.title || `Step ${i + 1}`}
                    </p>
                    {mechanic && drillPlan.mechanics.length > 1 && (
                      <p className="text-[0.65rem] text-text-muted">
                        {mechanic.name}
                      </p>
                    )}
                  </div>
                </div>
                <span className="text-xs text-white/30 font-mono">
                  {(r.timeTakenMs / 1000).toFixed(1)}s
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-3">
        <button
          onClick={() => startDrill(drillPlan)}
          className="flex-1 py-3 rounded-xl bg-gold/20 border border-gold/30 text-gold font-cinzel tracking-wider hover:bg-gold/30 transition-colors"
        >
          Retry
        </button>
        <button
          onClick={() => goToPhase("mechanic-select")}
          className="flex-1 py-3 rounded-xl border border-white/10 text-white/50 font-cinzel tracking-wider hover:border-white/20 hover:text-white/70 transition-colors"
        >
          Other Mechanics
        </button>
        <button
          onClick={reset}
          className="flex-1 py-3 rounded-xl border border-white/10 text-white/50 font-cinzel tracking-wider hover:border-white/20 hover:text-white/70 transition-colors"
        >
          Start Over
        </button>
      </div>
    </section>
  );
}
