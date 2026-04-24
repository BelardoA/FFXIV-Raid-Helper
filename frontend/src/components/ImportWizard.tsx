"use client";

import { useRef, useState } from "react";
import { previewImport, saveImport } from "@/lib/api";
import type {
  ArenaShape,
  ImportMechanic,
  ImportPreview,
  ImportRoleVariant,
  ImportStep,
} from "@/lib/types";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const ROLE_COLOR: Record<string, string> = {
  TANK:   "#4a9eff",
  HEALER: "#4aff9e",
  MELEE:  "#ff4a6a",
  RANGED: "#ffaa4a",
};

const SPOTS: Array<{ key: string; role: string; spot: 1 | 2; label: string }> = [
  { key: "TANK-1",   role: "TANK",   spot: 1, label: "MT" },
  { key: "TANK-2",   role: "TANK",   spot: 2, label: "OT" },
  { key: "HEALER-1", role: "HEALER", spot: 1, label: "H1" },
  { key: "HEALER-2", role: "HEALER", spot: 2, label: "H2" },
  { key: "MELEE-1",  role: "MELEE",  spot: 1, label: "M1" },
  { key: "MELEE-2",  role: "MELEE",  spot: 2, label: "M2" },
  { key: "RANGED-1", role: "RANGED", spot: 1, label: "R1" },
  { key: "RANGED-2", role: "RANGED", spot: 2, label: "R2" },
];

// ---------------------------------------------------------------------------
// Clickable arena editor — lets the user drag/click each role's position
// ---------------------------------------------------------------------------

function ArenaEditor({
  shape,
  variants,
  onChange,
}: {
  shape: ArenaShape;
  variants: ImportRoleVariant[];
  onChange: (updated: ImportRoleVariant[]) => void;
}) {
  const S = 240;
  const pad = 8;
  const inner = S - pad * 2;
  const svgRef = useRef<SVGSVGElement>(null);
  const [selected, setSelected] = useState("TANK-1");
  const [dragging, setDragging] = useState(false);

  const getCoords = (e: React.MouseEvent | React.TouchEvent): { x: number; y: number } | null => {
    const svg = svgRef.current;
    if (!svg) return null;
    const rect = svg.getBoundingClientRect();
    let clientX: number, clientY: number;
    if ("touches" in e) {
      clientX = e.touches[0].clientX;
      clientY = e.touches[0].clientY;
    } else {
      clientX = e.clientX;
      clientY = e.clientY;
    }
    const rawX = (clientX - rect.left) / rect.width;
    const rawY = (clientY - rect.top) / rect.height;
    return {
      x: Math.max(0, Math.min(1, rawX)),
      y: Math.max(0, Math.min(1, rawY)),
    };
  };

  const applyPosition = (e: React.MouseEvent | React.TouchEvent) => {
    const coords = getCoords(e);
    if (!coords) return;
    const spot = SPOTS.find((s) => s.key === selected);
    if (!spot) return;
    const updated = variants.map((rv) =>
      rv.role === spot.role && rv.spot === spot.spot
        ? { ...rv, correct_position: coords }
        : rv
    );
    // If the role variant didn't exist yet, add it
    if (!updated.some((rv) => rv.role === spot.role && rv.spot === spot.spot)) {
      updated.push({ role: spot.role as ImportRoleVariant["role"], spot: spot.spot, correct_position: coords });
    }
    onChange(updated);
  };

  const selectedSpot = SPOTS.find((s) => s.key === selected);

  return (
    <div className="flex flex-col gap-3">
      {/* Role selector */}
      <div className="flex flex-wrap gap-1.5">
        {SPOTS.map((s) => {
          const rv = variants.find((v) => v.role === s.role && v.spot === s.spot);
          return (
            <button
              key={s.key}
              onClick={() => setSelected(s.key)}
              className={`px-2.5 py-1 rounded-lg text-xs font-mono transition-all ${
                selected === s.key
                  ? "ring-2 ring-offset-1 ring-offset-bg-card scale-105"
                  : "opacity-60 hover:opacity-90"
              }`}
              style={{
                background: ROLE_COLOR[s.role] + "22",
                color: ROLE_COLOR[s.role],
                borderColor: ROLE_COLOR[s.role] + (selected === s.key ? "88" : "33"),
                border: `1px solid`,
                outline: selected === s.key ? `2px solid ${ROLE_COLOR[s.role]}66` : undefined,
                outlineOffset: selected === s.key ? "2px" : undefined,
              }}
              title={rv?.correct_position ? `(${rv.correct_position.x.toFixed(2)}, ${rv.correct_position.y.toFixed(2)})` : "not set"}
            >
              {s.label}
            </button>
          );
        })}
      </div>

      <p className="text-[0.65rem] text-text-muted">
        Selected: <span style={{ color: selectedSpot ? ROLE_COLOR[selectedSpot.role] : "#fff" }} className="font-mono font-bold">{selectedSpot?.label}</span>
        {" — click or drag on the arena to reposition"}
      </p>

      {/* Clickable SVG arena */}
      <svg
        ref={svgRef}
        width={S}
        height={S}
        className="rounded-xl border border-white/10 cursor-crosshair touch-none"
        style={{ background: "#0d0d1a" }}
        onMouseDown={(e) => { setDragging(true); applyPosition(e); }}
        onMouseMove={(e) => { if (dragging) applyPosition(e); }}
        onMouseUp={() => setDragging(false)}
        onMouseLeave={() => setDragging(false)}
        onTouchStart={(e) => { setDragging(true); applyPosition(e); }}
        onTouchMove={(e) => { if (dragging) applyPosition(e); e.preventDefault(); }}
        onTouchEnd={() => setDragging(false)}
      >
        {/* Arena floor */}
        {shape === "CIRCLE" ? (
          <circle cx={S / 2} cy={S / 2} r={inner / 2} fill="#16162a" stroke="rgba(255,255,255,0.08)" strokeWidth={1} />
        ) : (
          <rect x={pad} y={pad} width={inner} height={inner} fill="#16162a" stroke="rgba(255,255,255,0.08)" strokeWidth={1} />
        )}
        {/* Guide lines */}
        <line x1={S / 2} y1={pad} x2={S / 2} y2={S - pad} stroke="rgba(255,255,255,0.04)" strokeWidth={1} />
        <line x1={pad} y1={S / 2} x2={S - pad} y2={S / 2} stroke="rgba(255,255,255,0.04)" strokeWidth={1} />

        {/* Cardinal labels */}
        {[
          { label: "N", x: S/2, y: pad + 10 },
          { label: "S", x: S/2, y: S - pad - 4 },
          { label: "W", x: pad + 8, y: S/2 + 4 },
          { label: "E", x: S - pad - 4, y: S/2 + 4 },
        ].map(({ label, x, y }) => (
          <text key={label} x={x} y={y} textAnchor="middle" fill="rgba(255,255,255,0.12)" fontSize={8}>
            {label}
          </text>
        ))}

        {/* Role dots */}
        {variants.map((rv) => {
          if (!rv.correct_position) return null;
          const cx = rv.correct_position.x * S;
          const cy = rv.correct_position.y * S;
          const color = ROLE_COLOR[rv.role] ?? "#fff";
          const sp = SPOTS.find((s) => s.role === rv.role && s.spot === rv.spot);
          const isSelected = selected === sp?.key;
          return (
            <g key={`${rv.role}-${rv.spot}`}>
              {isSelected && (
                <circle cx={cx} cy={cy} r={14} fill="none" stroke={color} strokeWidth={1.5} opacity={0.5} strokeDasharray="3 2" />
              )}
              <circle cx={cx} cy={cy} r={isSelected ? 9 : 7} fill={color} opacity={isSelected ? 1 : 0.75} />
              <text x={cx} y={cy + 4} textAnchor="middle" fill="#000" fontSize={isSelected ? 7 : 6} fontWeight="bold" style={{ userSelect: "none", pointerEvents: "none" }}>
                {sp?.label ?? `${rv.role[0]}${rv.spot}`}
              </text>
            </g>
          );
        })}
      </svg>

      {/* Coordinate readout */}
      <div className="grid grid-cols-4 gap-1 text-[0.55rem] font-mono text-white/30">
        {SPOTS.map((s) => {
          const rv = variants.find((v) => v.role === s.role && v.spot === s.spot);
          return (
            <span key={s.key} style={{ color: selected === s.key ? ROLE_COLOR[s.role] : undefined }}>
              {s.label}: {rv?.correct_position
                ? `${rv.correct_position.x.toFixed(2)},${rv.correct_position.y.toFixed(2)}`
                : "—"}
            </span>
          );
        })}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Editable step card
// ---------------------------------------------------------------------------

function StepEditor({
  step,
  arenaShape,
  onChange,
  onRemove,
}: {
  step: ImportStep;
  arenaShape: ArenaShape;
  onChange: (updated: ImportStep) => void;
  onRemove: () => void;
}) {
  const [showArena, setShowArena] = useState(false);

  const updateField = (field: keyof ImportStep, value: unknown) =>
    onChange({ ...step, [field]: value });

  const updateVariants = (variants: ImportRoleVariant[]) =>
    onChange({ ...step, role_variants: variants });

  return (
    <div className="rounded-lg border border-white/8 bg-bg-deep overflow-hidden">
      {/* Step header */}
      <div className="flex items-center gap-2 px-3 py-2 border-b border-white/5">
        <span className="text-[0.6rem] text-text-muted font-mono shrink-0">Step {step.order}</span>
        <span className={`text-[0.6rem] px-1.5 py-0.5 rounded font-mono shrink-0 ${
          step.action_type === "POSITION" ? "bg-blue-900/40 text-blue-300" : "bg-purple-900/40 text-purple-300"
        }`}>
          {step.action_type}
        </span>
        <button
          onClick={() => updateField("action_type", step.action_type === "POSITION" ? "CHOICE" : "POSITION")}
          className="text-[0.55rem] text-text-muted hover:text-gold transition-colors ml-auto"
        >
          toggle type
        </button>
        <button onClick={onRemove} className="text-[0.55rem] text-red-400/50 hover:text-red-400 transition-colors">
          remove
        </button>
      </div>

      <div className="p-3 space-y-2">
        {/* Title */}
        <div>
          <label className="block text-[0.6rem] text-text-muted mb-0.5">Title</label>
          <input
            value={step.title}
            onChange={(e) => updateField("title", e.target.value)}
            className="w-full px-2 py-1.5 rounded bg-bg-card border border-white/8 text-sm text-white focus:outline-none focus:border-gold/30"
          />
        </div>

        {/* Narration + timer on same row */}
        <div className="flex gap-2">
          <div className="flex-1">
            <label className="block text-[0.6rem] text-text-muted mb-0.5">Narration</label>
            <input
              value={step.narration ?? ""}
              onChange={(e) => updateField("narration", e.target.value)}
              placeholder="Coaching cue shown during drill"
              className="w-full px-2 py-1.5 rounded bg-bg-card border border-white/8 text-xs text-white/70 focus:outline-none focus:border-gold/30 placeholder-white/15"
            />
          </div>
          <div className="w-20 shrink-0">
            <label className="block text-[0.6rem] text-text-muted mb-0.5">Timer (s)</label>
            <input
              type="number"
              min={0}
              max={30}
              value={step.timer_seconds ?? 0}
              onChange={(e) => updateField("timer_seconds", parseInt(e.target.value) || 0)}
              className="w-full px-2 py-1.5 rounded bg-bg-card border border-white/8 text-xs text-white focus:outline-none focus:border-gold/30 text-center"
            />
          </div>
        </div>

        {/* Explanation */}
        <div>
          <label className="block text-[0.6rem] text-text-muted mb-0.5">Explanation (shown after answer)</label>
          <input
            value={step.explanation ?? ""}
            onChange={(e) => updateField("explanation", e.target.value)}
            className="w-full px-2 py-1.5 rounded bg-bg-card border border-white/8 text-xs text-white/60 focus:outline-none focus:border-gold/30"
          />
        </div>

        {/* POSITION: arena editor */}
        {step.action_type === "POSITION" && (
          <div>
            <button
              onClick={() => setShowArena((v) => !v)}
              className="text-xs text-gold/60 hover:text-gold transition-colors mb-2"
            >
              {showArena ? "▲ Hide arena editor" : "▼ Edit positions on arena"}
            </button>
            {showArena && (
              <ArenaEditor
                shape={arenaShape}
                variants={step.role_variants}
                onChange={updateVariants}
              />
            )}
            {!showArena && (
              <div className="flex flex-wrap gap-1">
                {step.role_variants.filter(rv => rv.correct_position).map((rv) => {
                  const sp = SPOTS.find((s) => s.role === rv.role && s.spot === rv.spot);
                  return (
                    <span key={`${rv.role}-${rv.spot}`} className="text-[0.55rem] px-1.5 py-0.5 rounded bg-white/5 font-mono" style={{ color: ROLE_COLOR[rv.role] + "cc" }}>
                      {sp?.label}: {rv.correct_position!.x.toFixed(2)},{rv.correct_position!.y.toFixed(2)}
                    </span>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* CHOICE: edit choices and correct answers */}
        {step.action_type === "CHOICE" && (
          <div className="space-y-1.5">
            <label className="block text-[0.6rem] text-text-muted">Choices & correct answers</label>
            {(step.choices ?? []).map((c, i) => {
              const isCorrect = step.role_variants.some((rv) => rv.correct_choice === c.id);
              return (
                <div key={c.id} className="flex items-center gap-2">
                  <span
                    className={`text-[0.6rem] px-2 py-0.5 rounded-full border cursor-pointer select-none transition-colors ${
                      isCorrect ? "border-gold/50 bg-gold/10 text-gold" : "border-white/10 text-white/30 hover:border-white/20"
                    }`}
                    onClick={() => {
                      // Toggle all role_variants to use this choice as correct
                      const updated = step.role_variants.map((rv) => ({ ...rv, correct_choice: c.id }));
                      updateVariants(updated);
                    }}
                    title="Click to set as correct answer for all roles"
                  >
                    {isCorrect ? "✓ " : "○ "}{c.label}
                  </span>
                  <input
                    value={c.label}
                    onChange={(e) => {
                      const choices = step.choices!.map((ch, j) => j === i ? { ...ch, label: e.target.value } : ch);
                      updateField("choices", choices);
                    }}
                    className="flex-1 px-2 py-1 rounded bg-bg-card border border-white/8 text-xs text-white/60 focus:outline-none focus:border-gold/30"
                    placeholder="Choice label"
                  />
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Editable mechanic block
// ---------------------------------------------------------------------------

function MechanicEditor({
  mech,
  arenaShape,
  onChange,
  onRemove,
}: {
  mech: ImportMechanic;
  arenaShape: ArenaShape;
  onChange: (updated: ImportMechanic) => void;
  onRemove: () => void;
}) {
  const [expanded, setExpanded] = useState(false);

  const updateField = (field: keyof ImportMechanic, value: unknown) =>
    onChange({ ...mech, [field]: value });

  const updateStep = (idx: number, updated: ImportStep) => {
    const steps = mech.steps.map((s, i) => (i === idx ? updated : s));
    onChange({ ...mech, steps });
  };

  const removeStep = (idx: number) => {
    onChange({ ...mech, steps: mech.steps.filter((_, i) => i !== idx) });
  };

  return (
    <div className="rounded-xl border border-white/8 overflow-hidden">
      {/* Accordion header */}
      <div className="flex items-center gap-2 px-4 py-2.5 bg-bg-card">
        <span className="text-[0.6rem] text-text-muted font-mono w-5 shrink-0">#{mech.order}</span>
        <button
          className="flex-1 text-left"
          onClick={() => setExpanded((v) => !v)}
        >
          <span className="font-cinzel text-sm text-gold-light">{mech.name}</span>
          {mech.phase_name && (
            <span className="text-[0.6rem] text-text-muted ml-2">{mech.phase_name}</span>
          )}
        </button>
        <span className="text-[0.6rem] text-text-muted shrink-0">
          {mech.steps.length} step{mech.steps.length !== 1 ? "s" : ""}
        </span>
        <button
          onClick={() => setExpanded((v) => !v)}
          className="text-white/20 text-xs w-5 text-center shrink-0"
        >
          {expanded ? "▲" : "▼"}
        </button>
      </div>

      {expanded && (
        <div className="border-t border-white/5 p-4 space-y-4 bg-bg-card/50">
          {/* Mechanic metadata */}
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-[0.6rem] text-text-muted mb-0.5">Name</label>
              <input
                value={mech.name}
                onChange={(e) => updateField("name", e.target.value)}
                className="w-full px-2 py-1.5 rounded bg-bg-card border border-white/8 text-sm text-white focus:outline-none focus:border-gold/30"
              />
            </div>
            <div>
              <label className="block text-[0.6rem] text-text-muted mb-0.5">Phase</label>
              <input
                value={mech.phase_name ?? ""}
                onChange={(e) => updateField("phase_name", e.target.value)}
                className="w-full px-2 py-1.5 rounded bg-bg-card border border-white/8 text-sm text-white focus:outline-none focus:border-gold/30"
              />
            </div>
          </div>

          <div>
            <label className="block text-[0.6rem] text-text-muted mb-0.5">Description</label>
            <textarea
              value={mech.description ?? ""}
              onChange={(e) => updateField("description", e.target.value)}
              rows={2}
              className="w-full px-2 py-1.5 rounded bg-bg-card border border-white/8 text-xs text-white/70 focus:outline-none focus:border-gold/30 resize-none"
            />
          </div>

          <div className="flex gap-2 items-center">
            <div>
              <label className="block text-[0.6rem] text-text-muted mb-0.5">Difficulty (1–5)</label>
              <input
                type="number"
                min={1}
                max={5}
                value={mech.difficulty_rating ?? 1}
                onChange={(e) => updateField("difficulty_rating", parseInt(e.target.value) || 1)}
                className="w-16 px-2 py-1.5 rounded bg-bg-card border border-white/8 text-xs text-white focus:outline-none focus:border-gold/30 text-center"
              />
            </div>
            <div className="flex-1">
              <label className="block text-[0.6rem] text-text-muted mb-0.5">Tags (comma-separated)</label>
              <input
                value={(mech.tags ?? []).join(", ")}
                onChange={(e) => updateField("tags", e.target.value.split(",").map((t) => t.trim()).filter(Boolean))}
                className="w-full px-2 py-1.5 rounded bg-bg-card border border-white/8 text-xs text-white/70 focus:outline-none focus:border-gold/30"
                placeholder="spread, stack, clock"
              />
            </div>
          </div>

          {/* Steps */}
          <div className="space-y-2">
            <h4 className="text-[0.65rem] text-text-muted uppercase tracking-widest">Steps</h4>
            {mech.steps.map((step, idx) => (
              <StepEditor
                key={idx}
                step={step}
                arenaShape={arenaShape}
                onChange={(updated) => updateStep(idx, updated)}
                onRemove={() => removeStep(idx)}
              />
            ))}
          </div>

          <button
            onClick={onRemove}
            className="text-xs text-red-400/50 hover:text-red-400 transition-colors mt-2"
          >
            Remove this mechanic
          </button>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main wizard
// ---------------------------------------------------------------------------

type WizardStep = "input" | "generating" | "review" | "saving" | "done";
type InputMode = "url" | "json";

export default function ImportWizard() {
  const [step, setStep]         = useState<WizardStep>("input");
  const [inputMode, setInputMode] = useState<InputMode>("json");
  const [url, setUrl]           = useState("");
  const [pastedJson, setPastedJson] = useState("");
  const [error, setError]       = useState("");
  const [edited, setEdited]     = useState<ImportPreview | null>(null);
  const [savedSlug, setSavedSlug] = useState("");

  // ── helpers ──────────────────────────────────────────────────────────────

  const loadPreview = (raw: ImportPreview) => {
    const normalised: ImportPreview = {
      ...raw,
      mechanics: raw.mechanics.map((m, i) => ({
        ...m,
        order: m.order ?? i + 1,
        steps: m.steps.map((s, j) => ({ ...s, order: s.order ?? j + 1 })),
      })),
    };
    setEdited(normalised);
    setStep("review");
  };

  const handleUrlGenerate = async () => {
    setError("");
    if (!url.trim()) { setError("Please enter a wtfdig.info URL."); return; }
    setStep("generating");
    try {
      loadPreview(await previewImport(url.trim()));
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
      setStep("input");
    }
  };

  const handleJsonLoad = () => {
    setError("");
    if (!pastedJson.trim()) { setError("Paste the JSON preview first."); return; }
    try {
      const parsed = JSON.parse(pastedJson);
      if (!parsed.fight || !parsed.mechanics) throw new Error("JSON must have 'fight' and 'mechanics' keys.");
      loadPreview(parsed);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    }
  };

  const handleSave = async () => {
    if (!edited) return;
    setError("");
    setStep("saving");
    try {
      const result = await saveImport(edited);
      setSavedSlug(result.fight.slug);
      setStep("done");
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
      setStep("review");
    }
  };

  const updateMechanic = (idx: number, updated: ImportMechanic) => {
    if (!edited) return;
    setEdited({ ...edited, mechanics: edited.mechanics.map((m, i) => (i === idx ? updated : m)) });
  };

  const removeMechanic = (idx: number) => {
    if (!edited) return;
    setEdited({ ...edited, mechanics: edited.mechanics.filter((_, i) => i !== idx) });
  };

  const reset = () => {
    setStep("input"); setUrl(""); setPastedJson(""); setError(""); setEdited(null); setSavedSlug("");
  };

  // ── renders ───────────────────────────────────────────────────────────────

  if (step === "generating") {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-4">
        <div className="w-10 h-10 rounded-full border-2 border-gold/30 border-t-gold animate-spin" />
        <p className="font-cinzel text-gold animate-pulse">Generating preview…</p>
        <p className="text-xs text-text-muted max-w-xs text-center">
          Claude is reading the fight and generating positions for all roles. This may take up to 30 seconds.
        </p>
      </div>
    );
  }

  if (step === "saving") {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-4">
        <div className="w-10 h-10 rounded-full border-2 border-gold/30 border-t-gold animate-spin" />
        <p className="font-cinzel text-gold animate-pulse">Saving to database…</p>
      </div>
    );
  }

  if (step === "done") {
    return (
      <div className="max-w-lg mx-auto px-4 py-16 text-center">
        <div className="text-5xl mb-4">✓</div>
        <h2 className="font-cinzel text-2xl text-gold-light mb-2">Import complete!</h2>
        <p className="text-sm text-text-muted mb-8">
          The fight has been saved and is now available in the drill trainer.
        </p>
        <div className="flex gap-3 justify-center flex-wrap">
          <a href="/" className="px-6 py-2.5 rounded-xl bg-gold text-bg-deep font-cinzel tracking-wider text-sm font-bold hover:bg-gold-light transition-colors">
            Go to Trainer
          </a>
          <button onClick={reset} className="px-6 py-2.5 rounded-xl border border-white/10 text-white/60 text-sm hover:border-gold/30 hover:text-gold-light transition-colors">
            Import Another
          </button>
        </div>
        {savedSlug && (
          <p className="text-xs text-text-muted mt-6">
            Saved as <code className="bg-white/5 px-1.5 rounded text-gold/60">{savedSlug}</code>
          </p>
        )}
      </div>
    );
  }

  // ── Input step ─────────────────────────────────────────────────────────────

  if (step === "input") {
    return (
      <div className="max-w-2xl mx-auto px-4 py-10">
        <h1 className="font-cinzel text-2xl text-gold-light tracking-wider mb-1">
          Import from wtfdig.info
        </h1>
        <p className="text-sm text-text-muted mb-6">
          Load mechanic data, review every position on the arena editor, then save to the database.
        </p>

        {/* Mode tabs */}
        <div className="flex rounded-xl border border-white/10 overflow-hidden mb-6 text-sm">
          {(["json", "url"] as InputMode[]).map((m) => (
            <button
              key={m}
              onClick={() => { setInputMode(m); setError(""); }}
              className={`flex-1 py-2.5 font-cinzel tracking-wide transition-colors ${
                inputMode === m
                  ? "bg-gold/15 text-gold border-b-2 border-gold"
                  : "text-text-muted hover:text-white/60"
              }`}
            >
              {m === "json" ? "Paste JSON" : "URL (needs API key)"}
            </button>
          ))}
        </div>

        {inputMode === "json" && (
          <div className="space-y-4">
            <div className="p-3 rounded-xl bg-blue-900/20 border border-blue-800/40 text-xs text-blue-300/80 space-y-1.5">
              <p className="font-semibold text-blue-200">How to use Paste JSON</p>
              <ol className="list-decimal list-inside space-y-1 text-blue-300/70">
                <li>Ask Claude Code in this terminal to generate the import JSON for your fight.</li>
                <li>Copy the JSON it outputs.</li>
                <li>Paste it below and click Load.</li>
              </ol>
              <p className="italic">
                Example prompt: <span className="not-italic font-mono bg-white/5 px-1 rounded">
                  Generate an ImportPreview JSON for M9S using the Toxic Friends strat.
                </span>
              </p>
            </div>

            <div>
              <label className="block text-xs text-text-muted mb-1.5">ImportPreview JSON</label>
              <textarea
                value={pastedJson}
                onChange={(e) => setPastedJson(e.target.value)}
                rows={10}
                placeholder={'{\n  "fight": { "slug": "m9s", ... },\n  "tier": { ... },\n  "mechanics": [ ... ]\n}'}
                className="w-full px-4 py-3 rounded-xl border border-white/10 bg-bg-card text-white/80 placeholder-white/15 focus:outline-none focus:border-gold/40 text-xs font-mono resize-y"
              />
            </div>

            {error && (
              <p className="text-sm text-red-400 p-3 rounded-lg bg-red-900/20 border border-red-900/30">{error}</p>
            )}

            <button
              onClick={handleJsonLoad}
              className="w-full py-3 rounded-xl bg-gold text-bg-deep font-cinzel tracking-wider text-sm font-bold hover:bg-gold-light transition-colors"
            >
              Load &amp; Review
            </button>
          </div>
        )}

        {inputMode === "url" && (
          <div className="space-y-4">
            <div className="p-3 rounded-xl bg-amber-900/20 border border-amber-800/40 text-xs text-amber-300/80">
              Requires <code className="bg-white/5 px-1 rounded">ANTHROPIC_API_KEY</code> with API credits in the
              backend environment. Claude Pro (claude.ai) does not include API credits — purchase them separately at{" "}
              <span className="underline">console.anthropic.com</span>.
            </div>

            <div>
              <label className="block text-xs text-text-muted mb-1.5">WtfDig URL</label>
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleUrlGenerate()}
                placeholder="https://wtfdig.info/74/m9s#toxic"
                className="w-full px-4 py-3 rounded-xl border border-white/10 bg-bg-card text-white placeholder-white/20 focus:outline-none focus:border-gold/40 text-sm"
              />
            </div>

            {error && (
              <p className="text-sm text-red-400 p-3 rounded-lg bg-red-900/20 border border-red-900/30">{error}</p>
            )}

            <button
              onClick={handleUrlGenerate}
              className="w-full py-3 rounded-xl bg-gold text-bg-deep font-cinzel tracking-wider text-sm font-bold hover:bg-gold-light transition-colors"
            >
              Generate Preview
            </button>
          </div>
        )}
      </div>
    );
  }

  // ── Review / edit step ─────────────────────────────────────────────────────

  if (!edited) return null;

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <button onClick={reset} className="text-xs text-text-muted hover:text-gold-light transition-colors mb-6 block">
        &larr; Start over
      </button>

      {/* Fight info summary */}
      <div className="rounded-2xl border border-gold/20 bg-bg-card p-5 mb-6">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h2 className="font-cinzel text-xl text-gold-light tracking-wider">
              {edited.fight.short_name} — {edited.fight.boss_name}
            </h2>
            <p className="text-sm text-text-muted mt-0.5">{edited.fight.name}</p>
          </div>
          <div className="flex flex-col items-end gap-1 text-xs text-text-muted">
            <span>{edited.fight.difficulty} · {edited.fight.arena_shape}</span>
            <span>{edited.tier.name} (patch {edited.tier.patch})</span>
          </div>
        </div>
        <div className="mt-3 pt-3 border-t border-white/5 flex gap-4 text-xs text-text-muted">
          <span>{edited.mechanics.length} mechanics</span>
          <span>{edited.mechanics.reduce((n, m) => n + m.steps.length, 0)} steps</span>
          <span>{edited.mechanics.reduce((n, m) => n + m.steps.reduce((k, s) => k + s.role_variants.length, 0), 0)} role variants</span>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 rounded-lg bg-red-900/20 border border-red-900/30 text-sm text-red-400">{error}</div>
      )}

      {/* Instructions */}
      <div className="mb-4 p-3 rounded-xl bg-white/3 border border-white/5 text-xs text-text-muted space-y-1">
        <p className="font-semibold text-white/40">Editing guide</p>
        <p>Expand each mechanic to edit its name, description, and steps. For POSITION steps, click <span className="text-gold/70">Edit positions on arena</span> to open the clickable arena — select a role then click/drag to set their position. Click a CHOICE option to mark it correct for all roles. Remove mechanics or steps you do not want.</p>
      </div>

      <h3 className="font-cinzel text-sm text-gold tracking-[0.15em] uppercase mb-3">Mechanics</h3>

      <div className="space-y-2 mb-8">
        {edited.mechanics.length === 0 && (
          <p className="text-sm text-text-muted text-center py-8">All mechanics removed.</p>
        )}
        {edited.mechanics.map((mech, idx) => (
          <MechanicEditor
            key={`${mech.slug}-${idx}`}
            mech={mech}
            arenaShape={edited.fight.arena_shape}
            onChange={(updated) => updateMechanic(idx, updated)}
            onRemove={() => removeMechanic(idx)}
          />
        ))}
      </div>

      {/* Save controls */}
      <div className="flex gap-3 flex-wrap sticky bottom-4">
        <button
          onClick={handleSave}
          disabled={edited.mechanics.length === 0}
          className="px-8 py-3 rounded-xl bg-gold text-bg-deep font-cinzel tracking-wider text-sm font-bold hover:bg-gold-light transition-colors disabled:opacity-40 disabled:cursor-not-allowed shadow-lg"
        >
          Save to Database
        </button>
        <button
          onClick={reset}
          className="px-6 py-3 rounded-xl border border-white/10 text-white/60 text-sm hover:border-gold/30 hover:text-gold-light transition-colors shadow-lg"
        >
          Cancel
        </button>
      </div>
    </div>
  );
}
