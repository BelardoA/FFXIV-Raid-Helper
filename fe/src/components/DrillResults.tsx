"use client";

import { useAppStore } from "@/lib/store";

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
  const { mechanic, role, stepResults, reset, goToPhase, selectMechanic } =
    useAppStore();

  if (!mechanic || !role) return null;

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
          {mechanic.fight_short_name} &mdash; {mechanic.name}
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

      {/* Per-step breakdown */}
      <div className="mb-8 text-left">
        <h3 className="font-cinzel text-sm text-gold tracking-[0.15em] uppercase mb-3">
          Step Breakdown
        </h3>
        <div className="space-y-2">
          {stepResults.map((r, i) => {
            const step = mechanic.steps.find((s) => s.id === r.stepId);
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
                  <span className="text-sm text-white/60">
                    {step?.title || `Step ${i + 1}`}
                  </span>
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
          onClick={() => {
            // Retry same mechanic
            selectMechanic(mechanic);
          }}
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
