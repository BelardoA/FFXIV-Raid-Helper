/** Zustand store — predictable state for the drill flow. */

import { create } from "zustand";
import type { Fight, Mechanic, MechanicStep, Role, StepResult } from "./types";

export type AppPhase =
  | "role-select"
  | "fight-browse"
  | "mechanic-select"
  | "drilling"
  | "result";

export interface DrillStepRecord {
  stepId: number;
  result: StepResult;
  timeTakenMs: number;
}

interface AppState {
  // Navigation
  phase: AppPhase;

  // Selections
  role: Role | null;
  fight: Fight | null;
  mechanic: Mechanic | null;

  // Drill state
  currentStepIndex: number;
  stepResults: DrillStepRecord[];
  sessionKey: string;

  // Actions
  selectRole: (role: Role) => void;
  selectFight: (fight: Fight) => void;
  selectMechanic: (mechanic: Mechanic) => void;
  startDrill: () => void;
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
  fight: null,
  mechanic: null,
  currentStepIndex: 0,
  stepResults: [],
  sessionKey: generateSessionKey(),

  selectRole: (role) => set({ role, phase: "fight-browse" }),

  selectFight: (fight) => set({ fight, phase: "mechanic-select" }),

  selectMechanic: (mechanic) =>
    set({ mechanic, phase: "drilling", currentStepIndex: 0, stepResults: [] }),

  startDrill: () => set({ phase: "drilling", currentStepIndex: 0, stepResults: [] }),

  recordStep: (record) =>
    set((s) => ({ stepResults: [...s.stepResults, record] })),

  advanceStep: () =>
    set((s) => ({ currentStepIndex: s.currentStepIndex + 1 })),

  finishDrill: () => set({ phase: "result" }),

  reset: () =>
    set({
      phase: "role-select",
      role: null,
      fight: null,
      mechanic: null,
      currentStepIndex: 0,
      stepResults: [],
      sessionKey: generateSessionKey(),
    }),

  goToPhase: (phase) => set({ phase }),
}));
