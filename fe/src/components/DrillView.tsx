"use client";

import { useState, useCallback, useRef } from "react";
import { simulateStep } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import type { MechanicStep, StepResult, RoleVariant } from "@/lib/types";
import Arena from "./Arena";
import Timer from "./Timer";

export default function DrillView() {
  const {
    mechanic,
    role,
    currentStepIndex,
    sessionKey,
    recordStep,
    advanceStep,
    finishDrill,
    goToPhase,
  } = useAppStore();

  const [submittedPos, setSubmittedPos] = useState<{
    x: number;
    y: number;
  } | null>(null);
  const [result, setResult] = useState<StepResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [timerRunning, setTimerRunning] = useState(true);
  const startTimeRef = useRef(Date.now());

  if (!mechanic || !role) return null;

  const steps = mechanic.steps;
  const step: MechanicStep | undefined = steps[currentStepIndex];

  if (!step) {
    // All steps done
    finishDrill();
    return null;
  }

  // Find the role variant for the current role
  const variant: RoleVariant | undefined = step.role_variants.find(
    (v) => v.role === role
  );

  const handlePositionClick = async (pos: { x: number; y: number }) => {
    if (loading || result) return;
    setLoading(true);
    setSubmittedPos(pos);
    setTimerRunning(false);

    const timeTaken = Date.now() - startTimeRef.current;
    const res = await simulateStep({
      step_id: step.id,
      role,
      submitted_x: pos.x,
      submitted_y: pos.y,
      session_key: sessionKey,
      time_taken_ms: timeTaken,
    });

    setResult(res);
    recordStep({ stepId: step.id, result: res, timeTakenMs: timeTaken });
    setLoading(false);
  };

  const handleChoiceClick = async (choiceId: string) => {
    if (loading || result) return;
    setLoading(true);
    setTimerRunning(false);

    const timeTaken = Date.now() - startTimeRef.current;
    const res = await simulateStep({
      step_id: step.id,
      role,
      submitted_choice: choiceId,
      session_key: sessionKey,
      time_taken_ms: timeTaken,
    });

    setResult(res);
    recordStep({ stepId: step.id, result: res, timeTakenMs: timeTaken });
    setLoading(false);
  };

  const handleTimerExpire = useCallback(async () => {
    if (result) return;
    setTimerRunning(false);

    // Auto-fail: submit a dummy position far from any correct answer
    const timeTaken = step.timer_seconds * 1000;
    const res = await simulateStep({
      step_id: step.id,
      role,
      submitted_x: -1,
      submitted_y: -1,
      session_key: sessionKey,
      time_taken_ms: timeTaken,
    });

    setResult(res);
    recordStep({ stepId: step.id, result: res, timeTakenMs: timeTaken });
  }, [step, role, sessionKey, result, recordStep]);

  const handleNext = () => {
    setSubmittedPos(null);
    setResult(null);
    setTimerRunning(true);
    startTimeRef.current = Date.now();

    if (currentStepIndex + 1 >= steps.length) {
      finishDrill();
    } else {
      advanceStep();
    }
  };

  const progress = ((currentStepIndex + 1) / steps.length) * 100;

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
        <div className="text-center">
          <span className="font-cinzel text-sm text-gold tracking-wider">
            {mechanic.fight_short_name} &mdash; {mechanic.name}
          </span>
        </div>
        <span className="text-xs text-text-muted">
          {currentStepIndex + 1} / {steps.length}
        </span>
      </div>

      {/* Progress bar */}
      <div className="w-full h-1 rounded-full bg-white/10 mb-6">
        <div
          className="h-full rounded-full bg-gold transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>

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
            const isSelected =
              result && result.correct_choice !== null
                ? undefined
                : undefined;
            const isCorrectChoice =
              result && c.id === result.correct_choice;
            const isWrongChoice =
              result &&
              c.id !== result.correct_choice &&
              result.correct_choice !== null;

            return (
              <button
                key={c.id}
                onClick={() => handleChoiceClick(c.id)}
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
            {currentStepIndex + 1 >= steps.length
              ? "View Results"
              : "Next Step \u2192"}
          </button>
        </div>
      )}
    </section>
  );
}
