/** API client for the Django backend. */

import type {
  DrillPlan,
  Fight,
  Mechanic,
  RaidTier,
  Role,
  SessionStats,
  Spot,
  StepResult,
} from "./types";

const BASE = "/api";

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

// --- Raid tiers ---

export async function fetchRaidTiers(): Promise<RaidTier[]> {
  const data = await get<PaginatedResponse<RaidTier>>("/raids/");
  return data.results;
}

export async function fetchRaidTier(slug: string): Promise<RaidTier> {
  return get<RaidTier>(`/raids/${slug}/`);
}

// --- Fights ---

export async function fetchFights(params?: {
  tier?: string;
  difficulty?: string;
}): Promise<Fight[]> {
  const query = new URLSearchParams();
  if (params?.tier) query.set("tier", params.tier);
  if (params?.difficulty) query.set("difficulty", params.difficulty);
  const qs = query.toString();
  const data = await get<PaginatedResponse<Fight>>(
    `/fights/${qs ? `?${qs}` : ""}`
  );
  return data.results;
}

export async function fetchFight(slug: string): Promise<Fight> {
  return get<Fight>(`/fights/${slug}/`);
}

// --- Mechanics ---

export async function fetchMechanic(id: number): Promise<Mechanic> {
  return get<Mechanic>(`/mechanics/${id}/`);
}

// --- Drill plan ---

export async function fetchDrillPlan(
  slug: string,
  phase?: string
): Promise<DrillPlan> {
  const qs = phase ? `?phase=${encodeURIComponent(phase)}` : "";
  return get<DrillPlan>(`/fights/${slug}/drill/${qs}`);
}

// --- Simulation ---

export async function simulateStep(params: {
  step_id: number;
  role: Role;
  spot?: Spot;
  submitted_x?: number | null;
  submitted_y?: number | null;
  submitted_choice?: string;
  session_key?: string;
  time_taken_ms?: number;
}): Promise<StepResult> {
  return post<StepResult>("/simulate-step/", params);
}

// --- Sessions ---

export async function fetchSessionStats(
  sessionKey: string
): Promise<SessionStats> {
  return get<SessionStats>(`/sessions/${sessionKey}/stats/`);
}
