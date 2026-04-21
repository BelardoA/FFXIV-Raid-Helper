/** Zustand store — predictable state for the drill flow. */

import { create } from "zustand";
import type { DrillPlan, Fight, Role, Spot, StepResult } from "./types";

export type AppPhase =
  | "role-select"
  | "fight-browse"
  | "mechanic-select"
  | "drilling"
  | "result";

export interface DrillStepRecord {
  mechanicId: number;
  stepId: number;
  result: StepResult;
  timeTakenMs: number;
}

interface AppState {
  // Navigation
  phase: AppPhase;

  // Selections
  role: Role | null;
  spot: Spot;
  fight: Fight | null;
  drillPlan: DrillPlan | null;

  // Drill progression — flat (mechanicIndex, stepIndex) pointer into drillPlan.
  currentMechanicIndex: number;
  currentStepIndex: number;
  stepResults: DrillStepRecord[];
  sessionKey: string;

  // Actions
  selectRole: (role: Role, spot?: Spot) => void;
  selectSpot: (spot: Spot) => void;
  selectFight: (fight: Fight) => void;
  startDrill: (plan: DrillPlan) => void;
  recordStep: (record: DrillStepRecord) => void;
  advanceStep: () => void;
  finishDrill: () => void;
  reset: () => void;
  goToPhase: (phase: AppPhase) => void;
}

function generateSessionKey(): string {
  return `sess_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

export const useAppStore = create<AppState>((set) => ({
  phase: "role-select",
  role: null,
  spot: 1,
  fight: null,
  drillPlan: null,
  currentMechanicIndex: 0,
  currentStepIndex: 0,
  stepResults: [],
  sessionKey: generateSessionKey(),

  selectRole: (role, spot = 1) => set({ role, spot, phase: "fight-browse" }),

  selectSpot: (spot) => set({ spot }),

  selectFight: (fight) => set({ fight, phase: "mechanic-select" }),

  startDrill: (plan) =>
    set({
      drillPlan: plan,
      phase: "drilling",
      currentMechanicIndex: 0,
      currentStepIndex: 0,
      stepResults: [],
    }),

  recordStep: (record) =>
    set((s) => ({ stepResults: [...s.stepResults, record] })),

  advanceStep: () =>
    set((s) => {
      if (!s.drillPlan) return {};
      const mech = s.drillPlan.mechanics[s.currentMechanicIndex];
      if (!mech) return {};
      // More steps remaining in the current mechanic?
      if (s.currentStepIndex + 1 < mech.steps.length) {
        return { currentStepIndex: s.currentStepIndex + 1 };
      }
      // Move to the next mechanic.
      if (s.currentMechanicIndex + 1 < s.drillPlan.mechanics.length) {
        return {
          currentMechanicIndex: s.currentMechanicIndex + 1,
          currentStepIndex: 0,
        };
      }
      // Drill complete.
      return { phase: "result" as AppPhase };
    }),

  finishDrill: () => set({ phase: "result" }),

  reset: () =>
    set({
      phase: "role-select",
      role: null,
      spot: 1,
      fight: null,
      drillPlan: null,
      currentMechanicIndex: 0,
      currentStepIndex: 0,
      stepResults: [],
      sessionKey: generateSessionKey(),
    }),

  goToPhase: (phase) => set({ phase }),
}));
