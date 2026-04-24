"use client";

import { useState, useCallback, useRef, useMemo, useEffect } from "react";
import { useRouter } from "next/navigation";
import { simulateStep } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import type { DrillPlan, Mechanic, MechanicStep, Role, RoleVariant, Spot, StepResult } from "@/lib/types";
import Arena from "./Arena";
import Timer from "./Timer";

export default function DrillView() {
  const router = useRouter();
  const {
    drillPlan,
    role,
    spot,
    currentMechanicIndex,
    currentStepIndex,
    sessionKey,
    recordStep,
    advanceStep,
  } = useAppStore();

  const totals = useMemo(() => {
    if (!drillPlan) return { flatIndex: 0, totalSteps: 0 };
    let totalSteps = 0;
    let flatIndex = 0;
    drillPlan.mechanics.forEach((m, mi) => {
      if (mi < currentMechanicIndex) flatIndex += m.steps.length;
      else if (mi === currentMechanicIndex) flatIndex += currentStepIndex;
      totalSteps += m.steps.length;
    });
    return { flatIndex, totalSteps };
  }, [drillPlan, currentMechanicIndex, currentStepIndex]);

  const mechanic = drillPlan?.mechanics[currentMechanicIndex];
  const step: MechanicStep | undefined = mechanic?.steps[currentStepIndex];

  if (!drillPlan || !role || !mechanic || !step) return null;

  return (
    <DrillStepScreen
      key={step.id}
      advanceStep={advanceStep}
      currentMechanicIndex={currentMechanicIndex}
      currentStepIndex={currentStepIndex}
      drillPlan={drillPlan}
      onBack={() => router.push(`/fights/${drillPlan.fight.slug}`)}
      onFinish={() => router.push(`/fights/${drillPlan.fight.slug}/result`)}
      mechanic={mechanic}
      recordStep={recordStep}
      role={role}
      sessionKey={sessionKey}
      spot={spot}
      step={step}
      totals={totals}
    />
  );
}

interface DrillStepScreenProps {
  advanceStep: () => void;
  currentMechanicIndex: number;
  currentStepIndex: number;
  drillPlan: DrillPlan;
  onBack: () => void;
  onFinish: () => void;
  mechanic: Mechanic;
  recordStep: ReturnType<typeof useAppStore.getState>["recordStep"];
  role: Role;
  sessionKey: string;
  spot: Spot;
  step: MechanicStep;
  totals: { flatIndex: number; totalSteps: number };
}

function DrillStepScreen({
  advanceStep,
  currentMechanicIndex,
  currentStepIndex,
  drillPlan,
  onBack,
  onFinish,
  mechanic,
  recordStep,
  role,
  sessionKey,
  spot,
  step,
  totals,
}: DrillStepScreenProps) {
  const [submittedPos, setSubmittedPos] = useState<{ x: number; y: number } | null>(null);
  const [result, setResult] = useState<StepResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [timerRunning, setTimerRunning] = useState(true);
  const startTimeRef = useRef(0);

  useEffect(() => { startTimeRef.current = performance.now(); }, []);

  const variant: RoleVariant | undefined =
    step.role_variants.find((v) => v.role === role && v.spot === spot) ||
    step.role_variants.find((v) => v.role === role && v.spot === 1);

  const isFinalStep =
    currentMechanicIndex === drillPlan.mechanics.length - 1 &&
    currentStepIndex === mechanic.steps.length - 1;

  const scopeLabel =
    drillPlan.scope === "full"
      ? "Full Fight"
      : drillPlan.mechanics.length === 1
        ? "Single Mechanic"
        : drillPlan.scope;

  const submitPosition = useCallback(
    async (pos: { x: number; y: number }, timeTaken: number) => {
      if (!step || !role || !mechanic) return;
      const res = await simulateStep({
        step_id: step.id, role, spot,
        submitted_x: pos.x, submitted_y: pos.y,
        session_key: sessionKey, time_taken_ms: timeTaken,
      });
      setResult(res);
      recordStep({ mechanicId: mechanic.id, stepId: step.id, result: res, timeTakenMs: timeTaken });
    },
    [mechanic, recordStep, role, sessionKey, spot, step]
  );

  const submitChoice = useCallback(
    async (choiceId: string, timeTaken: number) => {
      const res = await simulateStep({
        step_id: step.id, role, spot,
        submitted_choice: choiceId,
        session_key: sessionKey, time_taken_ms: timeTaken,
      });
      setResult(res);
      recordStep({ mechanicId: mechanic.id, stepId: step.id, result: res, timeTakenMs: timeTaken });
    },
    [mechanic.id, recordStep, role, sessionKey, spot, step.id]
  );

  const submitTimeout = useCallback(
    async (timeTaken: number) => {
      const params = { step_id: step.id, role, spot, session_key: sessionKey, time_taken_ms: timeTaken };
      const res =
        step.action_type === "CHOICE"
          ? await simulateStep(params)
          : await simulateStep({ ...params, submitted_x: null, submitted_y: null });
      setResult(res);
      recordStep({ mechanicId: mechanic.id, stepId: step.id, result: res, timeTakenMs: timeTaken });
    },
    [mechanic.id, recordStep, role, sessionKey, spot, step.action_type, step.id]
  );

  const handlePositionClick = async (pos: { x: number; y: number }, eventTimeStamp: number) => {
    if (loading || result) return;
    setLoading(true);
    setSubmittedPos(pos);
    setTimerRunning(false);
    await submitPosition(pos, Math.max(0, Math.round(eventTimeStamp - startTimeRef.current)));
    setLoading(false);
  };

  const handleChoiceClick = async (choiceId: string, eventTimeStamp: number) => {
    if (loading || result) return;
    setLoading(true);
    setTimerRunning(false);
    await submitChoice(choiceId, Math.max(0, Math.round(eventTimeStamp - startTimeRef.current)));
    setLoading(false);
  };

  const handleTimerExpire = useCallback(async () => {
    if (loading || result) return;
    setLoading(true);
    setTimerRunning(false);
    await submitTimeout(step.timer_seconds * 1000);
    setLoading(false);
  }, [loading, result, step.timer_seconds, submitTimeout]);

  const progress = totals.totalSteps > 0 ? ((totals.flatIndex + 1) / totals.totalSteps) * 100 : 0;

  return (
    <section className="relative z-10 max-w-2xl mx-auto px-4 py-6">

      {/* ── Top bar ── */}
      <div className="flex items-center justify-between mb-3">
        <button
          onClick={onBack}
          className="flex items-center gap-1.5 text-xs text-muted hover:text-gold-light transition-colors font-cinzel tracking-wider group"
        >
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className="transition-transform group-hover:-translate-x-0.5">
            <path d="M8 2L3 6l5 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          Back
        </button>

        <div className="text-center">
          <span className="font-display text-xs text-gold tracking-wider">
            {drillPlan.fight.short_name}
            <span className="text-muted mx-2">·</span>
            {scopeLabel}
          </span>
          {mechanic.phase_name && drillPlan.mechanics.length > 1 && (
            <div className="font-cinzel text-[0.55rem] text-muted tracking-[0.18em] uppercase mt-0.5">
              {mechanic.phase_name}
            </div>
          )}
        </div>

        <span className="font-mono text-xs text-muted tabular-nums">
          {totals.flatIndex + 1}
          <span className="text-dim"> / </span>
          {totals.totalSteps}
        </span>
      </div>

      {/* ── Progress (limit break gauge) ── */}
      <div className="lb-gauge mb-6">
        <div className="lb-fill" style={{ width: `${progress}%` }} />
      </div>

      {/* ── Mechanic context ── */}
      {drillPlan.mechanics.length > 1 && (
        <div className="mb-4 text-center">
          <p className="font-display text-sm text-gold-light">{mechanic.name}</p>
          <p className="text-[0.65rem] text-muted font-cinzel">
            Step {currentStepIndex + 1} of {mechanic.steps.length}
          </p>
        </div>
      )}

      {/* ── Step header + timer ── */}
      <div
        className="flex items-center justify-between px-4 py-3 mb-4"
        style={{ background: "rgba(12,21,37,0.8)", border: "1px solid rgba(91,196,232,0.12)", borderLeft: "3px solid rgba(91,196,232,0.35)" }}
      >
        <h3 className="font-cinzel text-base text-gold-light tracking-wide">{step.title}</h3>
        <Timer seconds={step.timer_seconds} running={timerRunning} onExpire={handleTimerExpire} />
      </div>

      {!result && (
        <p className="text-[0.8rem] text-muted italic mb-5 text-center font-cinzel tracking-wide">
          {step.action_type === "CHOICE"
            ? "Choose your response below."
            : "Click where you would position on the arena."}
        </p>
      )}

      {/* ── Arena or choice UI ── */}
      {step.action_type === "POSITION" ? (
        <Arena
          arenaState={step.arena_state}
          shape={mechanic.arena_shape}
          role={role}
          arenaImageUrl={mechanic.arena_image_url}
          bossImageUrl={mechanic.boss_image_url}
          allowClick={!result}
          locked={!!result}
          onPositionClick={handlePositionClick}
          submittedPosition={submittedPos}
          correctPosition={result?.correct_position}
          showAnswer={!!result}
          isCorrect={result?.is_correct ?? null}
          safeZones={variant?.safe_zones ?? []}
        />
      ) : (
        <div className="grid grid-cols-2 gap-3">
          {step.choices.map((c) => {
            const isCorrectChoice = result && c.id === result.correct_choice;
            return (
              <button
                key={c.id}
                onClick={(event) => handleChoiceClick(c.id, event.timeStamp)}
                disabled={!!result}
                className="p-4 text-sm font-cinzel tracking-wide transition-all duration-200 text-center"
                style={
                  result
                    ? isCorrectChoice
                      ? { background: "rgba(46,203,122,0.1)", border: "1px solid rgba(46,203,122,0.4)", color: "#4de89a" }
                      : { background: "rgba(12,21,37,0.5)", border: "1px solid rgba(91,196,232,0.06)", color: "var(--color-dim)" }
                    : { background: "rgba(12,21,37,0.8)", border: "1px solid rgba(91,196,232,0.12)", color: "var(--color-body)" }
                }
                onMouseEnter={(e) => {
                  if (result) return;
                  const el = e.currentTarget as HTMLElement;
                  el.style.background = "rgba(17,30,56,0.95)";
                  el.style.borderColor = "rgba(200,164,90,0.35)";
                  el.style.color = "var(--color-gold-light)";
                }}
                onMouseLeave={(e) => {
                  if (result) return;
                  const el = e.currentTarget as HTMLElement;
                  el.style.background = "rgba(12,21,37,0.8)";
                  el.style.borderColor = "rgba(91,196,232,0.12)";
                  el.style.color = "var(--color-body)";
                }}
              >
                {c.label}
              </button>
            );
          })}
        </div>
      )}

      {/* ── Result feedback ── */}
      {result && (
        <div className="mt-6 space-y-3 animate-fade-up">
          {/* Narration */}
          <div
            className="px-4 py-3"
            style={{ background: "rgba(91,196,232,0.04)", border: "1px solid rgba(91,196,232,0.1)", borderLeft: "2px solid rgba(91,196,232,0.25)" }}
          >
            <p className="font-cinzel text-[0.55rem] text-muted tracking-[0.2em] uppercase mb-1.5">What happens</p>
            <p className="text-sm text-body/70">{step.narration}</p>
          </div>

          {/* Correct / Incorrect */}
          <div
            className="px-4 py-4"
            style={
              result.is_correct
                ? { background: "rgba(46,203,122,0.07)", border: "1px solid rgba(46,203,122,0.3)", borderLeft: "3px solid rgba(46,203,122,0.5)" }
                : { background: "rgba(232,80,64,0.07)",  border: "1px solid rgba(232,80,64,0.3)",  borderLeft: "3px solid rgba(232,80,64,0.5)" }
            }
          >
            <p
              className="font-display text-lg font-bold mb-1"
              style={{ color: result.is_correct ? "#4de89a" : "#f07060" }}
            >
              {result.is_correct ? "✓ Correct" : "✗ Incorrect"}
            </p>
            <p className="text-sm text-body/60">{result.explanation}</p>
            {result.distance !== null && !result.is_correct && (
              <p className="text-[0.7rem] text-muted mt-1 font-mono">
                Off by {(result.distance * 100).toFixed(1)}% of arena
              </p>
            )}
          </div>

          {/* Next button */}
          <button
            onClick={isFinalStep ? onFinish : advanceStep}
            className="w-full py-3.5 font-cinzel tracking-[0.15em] text-sm transition-all duration-200"
            style={{
              background: "rgba(200,164,90,0.12)",
              border: "1px solid rgba(200,164,90,0.35)",
              color: "var(--color-gold-light)",
            }}
            onMouseEnter={(e) => {
              const el = e.currentTarget as HTMLElement;
              el.style.background = "rgba(200,164,90,0.2)";
              el.style.borderColor = "rgba(200,164,90,0.6)";
              el.style.boxShadow = "0 0 20px rgba(200,164,90,0.1)";
            }}
            onMouseLeave={(e) => {
              const el = e.currentTarget as HTMLElement;
              el.style.background = "rgba(200,164,90,0.12)";
              el.style.borderColor = "rgba(200,164,90,0.35)";
              el.style.boxShadow = "none";
            }}
          >
            {isFinalStep ? "View Results" : "Next Step →"}
          </button>
        </div>
      )}
    </section>
  );
}
