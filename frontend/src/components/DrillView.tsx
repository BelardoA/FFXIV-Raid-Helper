"use client";

import { useState, useCallback, useRef, useMemo, useEffect } from "react";
import { simulateStep } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import type { DrillPlan, Mechanic, MechanicStep, Role, RoleVariant, Spot, StepResult } from "@/lib/types";
import Arena from "./Arena";
import Timer from "./Timer";

export default function DrillView() {
  const {
    drillPlan,
    role,
    spot,
    currentMechanicIndex,
    currentStepIndex,
    sessionKey,
    recordStep,
    advanceStep,
    goToPhase,
  } = useAppStore();

  const totals = useMemo(() => {
    if (!drillPlan) return { flatIndex: 0, totalSteps: 0 };
    let totalSteps = 0;
    let flatIndex = 0;
    drillPlan.mechanics.forEach((m, mi) => {
      if (mi < currentMechanicIndex) {
        flatIndex += m.steps.length;
      } else if (mi === currentMechanicIndex) {
        flatIndex += currentStepIndex;
      }
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
      goToPhase={goToPhase}
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
  goToPhase: (phase: "mechanic-select") => void;
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
  goToPhase,
  mechanic,
  recordStep,
  role,
  sessionKey,
  spot,
  step,
  totals,
}: DrillStepScreenProps) {
  const [submittedPos, setSubmittedPos] = useState<{
    x: number;
    y: number;
  } | null>(null);
  const [result, setResult] = useState<StepResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [timerRunning, setTimerRunning] = useState(true);
  const startTimeRef = useRef(0);

  useEffect(() => {
    startTimeRef.current = performance.now();
  }, []);

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
        step_id: step.id,
        role,
        spot,
        submitted_x: pos.x,
        submitted_y: pos.y,
        session_key: sessionKey,
        time_taken_ms: timeTaken,
      });

      setResult(res);
      recordStep({
        mechanicId: mechanic.id,
        stepId: step.id,
        result: res,
        timeTakenMs: timeTaken,
      });
    },
    [mechanic, recordStep, role, sessionKey, spot, step]
  );

  const submitChoice = useCallback(
    async (choiceId: string, timeTaken: number) => {
      const res = await simulateStep({
        step_id: step.id,
        role,
        spot,
        submitted_choice: choiceId,
        session_key: sessionKey,
        time_taken_ms: timeTaken,
      });

      setResult(res);
      recordStep({
        mechanicId: mechanic.id,
        stepId: step.id,
        result: res,
        timeTakenMs: timeTaken,
      });
    },
    [mechanic.id, recordStep, role, sessionKey, spot, step.id]
  );

  const submitTimeout = useCallback(
    async (timeTaken: number) => {
      const params = {
        step_id: step.id,
        role,
        spot,
        session_key: sessionKey,
        time_taken_ms: timeTaken,
      };
      const res =
        step.action_type === "CHOICE"
          ? await simulateStep(params)
          : await simulateStep({
              ...params,
              submitted_x: null,
              submitted_y: null,
            });

      setResult(res);
      recordStep({
        mechanicId: mechanic.id,
        stepId: step.id,
        result: res,
        timeTakenMs: timeTaken,
      });
    },
    [mechanic.id, recordStep, role, sessionKey, spot, step.action_type, step.id]
  );

  const handlePositionClick = async (
    pos: { x: number; y: number },
    eventTimeStamp: number
  ) => {
    if (loading || result) return;
    setLoading(true);
    setSubmittedPos(pos);
    setTimerRunning(false);

    const timeTaken = Math.max(
      0,
      Math.round(eventTimeStamp - startTimeRef.current)
    );
    await submitPosition(pos, timeTaken);
    setLoading(false);
  };

  const handleChoiceClick = async (choiceId: string, eventTimeStamp: number) => {
    if (loading || result) return;
    setLoading(true);
    setTimerRunning(false);

    const timeTaken = Math.max(
      0,
      Math.round(eventTimeStamp - startTimeRef.current)
    );
    await submitChoice(choiceId, timeTaken);
    setLoading(false);
  };

  const handleTimerExpire = useCallback(async () => {
    if (loading || result) return;
    setLoading(true);
    setTimerRunning(false);

    const timeTaken = step.timer_seconds * 1000;
    await submitTimeout(timeTaken);
    setLoading(false);
  }, [loading, result, step.timer_seconds, submitTimeout]);

  const handleNext = () => {
    advanceStep();
  };

  const progress =
    totals.totalSteps > 0
      ? ((totals.flatIndex + 1) / totals.totalSteps) * 100
      : 0;

  return (
    <section className="max-w-2xl mx-auto px-4 py-6">
      {/* Top bar */}
      <div className="flex items-center justify-between mb-4">
        <button
          onClick={() => goToPhase("mechanic-select")}
          className="text-xs text-text-muted hover:text-gold-light transition-colors"
        >
          &larr; Back
        </button>
        <div className="text-center flex flex-col">
          <span className="font-cinzel text-sm text-gold tracking-wider">
            {drillPlan.fight.short_name} &mdash; {scopeLabel}
          </span>
          {mechanic.phase_name && drillPlan.mechanics.length > 1 && (
            <span className="text-[0.65rem] text-text-muted tracking-[0.15em] uppercase">
              {mechanic.phase_name}
            </span>
          )}
        </div>
        <span className="text-xs text-text-muted">
          {totals.flatIndex + 1} / {totals.totalSteps}
        </span>
      </div>

      {/* Progress bar */}
      <div className="w-full h-1 rounded-full bg-white/10 mb-6">
        <div
          className="h-full rounded-full bg-gold transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Mechanic context */}
      {drillPlan.mechanics.length > 1 && (
        <div className="mb-4 text-center">
          <p className="font-cinzel text-base text-gold-light">
            {mechanic.name}
          </p>
          <p className="text-[0.7rem] text-text-muted">
            Step {currentStepIndex + 1} of {mechanic.steps.length} in this mechanic
          </p>
        </div>
      )}

      {/* Step title + timer */}
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-cinzel text-lg text-gold-light">{step.title}</h3>
        <Timer
          seconds={step.timer_seconds}
          running={timerRunning}
          onExpire={handleTimerExpire}
        />
      </div>
      <p className="text-sm text-white/50 mb-6">{step.narration}</p>

      {/* Arena or Choice UI */}
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
                className={`p-4 rounded-xl border text-sm font-cinzel transition-all ${
                  result
                    ? isCorrectChoice
                      ? "border-green-500 bg-green-500/15 text-green-400"
                      : "border-white/5 bg-bg-card text-white/30"
                    : "border-white/10 bg-bg-card hover:border-gold/40 hover:bg-bg-card-hover text-white/70"
                }`}
              >
                {c.label}
              </button>
            );
          })}
        </div>
      )}

      {/* Result feedback */}
      {result && (
        <div className="mt-6 space-y-4">
          <div
            className={`p-4 rounded-xl border ${
              result.is_correct
                ? "border-green-500/30 bg-green-500/10"
                : "border-red-500/30 bg-red-500/10"
            }`}
          >
            <p
              className={`font-cinzel text-lg font-bold mb-1 ${
                result.is_correct ? "text-green-400" : "text-red-400"
              }`}
            >
              {result.is_correct ? "Correct!" : "Incorrect"}
            </p>
            <p className="text-sm text-white/60">{result.explanation}</p>
            {result.distance !== null && !result.is_correct && (
              <p className="text-xs text-white/30 mt-1">
                Distance from correct: {(result.distance * 100).toFixed(1)}% of
                arena
              </p>
            )}
          </div>

          <button
            onClick={handleNext}
            className="w-full py-3 rounded-xl bg-gold/20 border border-gold/30 text-gold font-cinzel tracking-wider hover:bg-gold/30 transition-colors"
          >
            {isFinalStep ? "View Results" : "Next Step \u2192"}
          </button>
        </div>
      )}
    </section>
  );
}
