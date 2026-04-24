/** Zustand store — data state only. Navigation handled by Next.js router. */

import { create } from "zustand";
import type { DrillPlan, Fight, Role, Spot, StepResult } from "./types";

export interface DrillStepRecord {
  mechanicId: number;
  stepId: number;
  result: StepResult;
  timeTakenMs: number;
}

interface AppState {
  role: Role | null;
  spot: Spot;
  fight: Fight | null;
  drillPlan: DrillPlan | null;
  currentMechanicIndex: number;
  currentStepIndex: number;
  stepResults: DrillStepRecord[];
  sessionKey: string;

  selectRole: (role: Role, spot?: Spot) => void;
  selectSpot: (spot: Spot) => void;
  selectFight: (fight: Fight) => void;
  startDrill: (plan: DrillPlan) => void;
  recordStep: (record: DrillStepRecord) => void;
  advanceStep: () => void;
  reset: () => void;
}

function generateSessionKey(): string {
  return `sess_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

export const useAppStore = create<AppState>((set) => ({
  role: null,
  spot: 1,
  fight: null,
  drillPlan: null,
  currentMechanicIndex: 0,
  currentStepIndex: 0,
  stepResults: [],
  sessionKey: generateSessionKey(),

  selectRole: (role, spot = 1) => set({ role, spot }),
  selectSpot: (spot) => set({ spot }),
  selectFight: (fight) => set({ fight }),

  startDrill: (plan) =>
    set({
      drillPlan: plan,
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
      if (s.currentStepIndex + 1 < mech.steps.length) {
        return { currentStepIndex: s.currentStepIndex + 1 };
      }
      if (s.currentMechanicIndex + 1 < s.drillPlan.mechanics.length) {
        return { currentMechanicIndex: s.currentMechanicIndex + 1, currentStepIndex: 0 };
      }
      return {};
    }),

  reset: () =>
    set({
      role: null,
      spot: 1,
      fight: null,
      drillPlan: null,
      currentMechanicIndex: 0,
      currentStepIndex: 0,
      stepResults: [],
      sessionKey: generateSessionKey(),
    }),
}));
