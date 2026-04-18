/** Shared TypeScript types mirroring the Django API responses. */

export type Role = "TANK" | "HEALER" | "MELEE" | "RANGED" | "CASTER";
export type Difficulty = "NORMAL" | "SAVAGE" | "EXTREME" | "ULTIMATE";
export type ArenaShape = "SQUARE" | "CIRCLE";
export type ActionType = "POSITION" | "CHOICE";

// --- API response types ---

export interface RaidTier {
  id: number;
  slug: string;
  name: string;
  expansion: string;
  patch: string;
  order: number;
  fight_count: number;
  fights?: Fight[];
}

export interface Fight {
  id: number;
  slug: string;
  name: string;
  short_name: string;
  boss_name: string;
  difficulty: Difficulty;
  arena_shape: ArenaShape;
  order: number;
  thumbnail_url: string;
  mechanic_count: number;
  raid_tier_name: string;
  mechanics?: MechanicSummary[];
}

export interface MechanicSummary {
  id: number;
  slug: string;
  name: string;
  phase_name: string;
  description: string;
  order: number;
  difficulty_rating: number;
  tags: string[];
  step_count: number;
}

export interface Mechanic {
  id: number;
  slug: string;
  name: string;
  phase_name: string;
  description: string;
  order: number;
  difficulty_rating: number;
  tags: string[];
  fight_slug: string;
  fight_short_name: string;
  arena_shape: ArenaShape;
  steps: MechanicStep[];
}

export interface MechanicStep {
  id: number;
  order: number;
  title: string;
  narration: string;
  timer_seconds: number;
  default_tolerance: number | null;
  action_type: ActionType;
  arena_state: ArenaState;
  choices: ChoiceOption[];
  explanation: string;
  role_variants: RoleVariant[];
}

export interface RoleVariant {
  id: number;
  role: Role;
  correct_position: { x: number; y: number };
  tolerance: number | null;
  alt_positions: { x: number; y: number; label?: string }[];
  correct_choice: string;
  safe_zones: SafeZone[];
  explanation: string;
}

export interface ChoiceOption {
  id: string;
  label: string;
}

// --- Arena rendering types ---

export interface ArenaState {
  boss_position?: { x: number; y: number };
  boss_facing?: string;
  markers?: ArenaMarker[];
  aoes?: ArenaAoE[];
  tethers?: ArenaTether[];
  debuffs?: ArenaDebuff[];
}

export interface ArenaMarker {
  id: string;
  x: number;
  y: number;
}

export interface ArenaAoE {
  shape: "circle" | "rect" | "cone";
  // circle
  cx?: number;
  cy?: number;
  r?: number;
  // rect
  x?: number;
  y?: number;
  w?: number;
  h?: number;
  // cone
  angle?: number;
  spread?: number;
  // common
  color?: string;
  label?: string;
}

export interface ArenaTether {
  from: { x: number; y: number };
  to: { x: number; y: number };
  color?: string;
}

export interface ArenaDebuff {
  label: string;
  color?: string;
}

export interface SafeZone {
  shape?: string;
  cx?: number;
  cy?: number;
  r?: number;
  x?: number;
  y?: number;
  w?: number;
  h?: number;
}

// --- Simulation result ---

export interface StepResult {
  is_correct: boolean;
  explanation: string;
  correct_position: { x: number; y: number } | null;
  correct_choice: string | null;
  distance: number | null;
  tolerance_used: number;
  has_next_step: boolean;
  next_step_order: number | null;
}

// --- Session stats ---

export interface SessionStats {
  session_key: string;
  total_steps: number;
  correct: number;
  incorrect: number;
  accuracy: number;
  avg_time_ms: number;
  grade: string;
  per_mechanic: {
    mechanic_id: number;
    mechanic_name: string;
    total: number;
    correct: number;
    accuracy: number;
  }[];
}
