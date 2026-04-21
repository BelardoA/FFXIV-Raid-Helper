"use client";

import { useRef, useEffect, useCallback, useState } from "react";
import type {
  ArenaAoE,
  ArenaShape,
  ArenaState,
  Role,
  SafeZone,
} from "@/lib/types";

const ROLE_COLORS: Record<Role, string> = {
  TANK: "#2b7fff",
  HEALER: "#22c77a",
  MELEE: "#ff6b35",
  RANGED: "#f4c430",
};

const MARKER_COLORS: Record<string, string> = {
  A: "#ff4444",
  B: "#ffcc00",
  C: "#66aaff",
  D: "#aa44ff",
  "1": "#ff6600",
  "2": "#ffff00",
  "3": "#33ccff",
  "4": "#ff66cc",
};

interface ArenaProps {
  arenaState: ArenaState;
  shape: ArenaShape;
  role: Role;
  arenaImageUrl?: string;
  bossImageUrl?: string;
  // Click interaction
  allowClick?: boolean;
  locked?: boolean;
  onPositionClick?: (pos: { x: number; y: number }, timeStamp: number) => void;
  // Feedback overlays
  submittedPosition?: { x: number; y: number } | null;
  correctPosition?: { x: number; y: number } | null;
  showAnswer?: boolean;
  isCorrect?: boolean | null;
  safeZones?: SafeZone[];
}

export default function Arena({
  arenaState,
  shape,
  role,
  arenaImageUrl,
  bossImageUrl,
  allowClick = true,
  locked = false,
  onPositionClick,
  submittedPosition = null,
  correctPosition = null,
  showAnswer = false,
  isCorrect = null,
  safeZones = [],
}: ArenaProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [hoverPos, setHoverPos] = useState<{ x: number; y: number } | null>(
    null
  );
  const [size, setSize] = useState(460);
  const [arenaAsset, setArenaAsset] = useState<{
    image: HTMLImageElement | null;
    url: string;
  }>({ image: null, url: "" });
  const [bossAsset, setBossAsset] = useState<{
    image: HTMLImageElement | null;
    url: string;
  }>({ image: null, url: "" });

  // Load image assets
  useEffect(() => {
    if (!arenaImageUrl) return;
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = () => setArenaAsset({ image: img, url: arenaImageUrl });
    img.onerror = () => setArenaAsset({ image: null, url: arenaImageUrl });
    img.src = arenaImageUrl;
  }, [arenaImageUrl]);

  useEffect(() => {
    if (!bossImageUrl) return;
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = () => setBossAsset({ image: img, url: bossImageUrl });
    img.onerror = () => setBossAsset({ image: null, url: bossImageUrl });
    img.src = bossImageUrl;
  }, [bossImageUrl]);

  const arenaImg =
    arenaImageUrl && arenaAsset.url === arenaImageUrl ? arenaAsset.image : null;
  const bossImg =
    bossImageUrl && bossAsset.url === bossImageUrl ? bossAsset.image : null;

  // Resize handler
  useEffect(() => {
    const resize = () => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const parent = canvas.parentElement;
      if (!parent) return;
      const s = Math.min(parent.clientWidth - 16, 460);
      setSize(s);
    };
    resize();
    window.addEventListener("resize", resize);
    return () => window.removeEventListener("resize", resize);
  }, []);

  // Main draw
  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const s = size;
    canvas.width = s;
    canvas.height = s;

    ctx.clearRect(0, 0, s, s);

    // Arena floor (image or canvas-drawn)
    drawArenaFloor(ctx, s, shape, arenaImg);

    // Safe zones
    if (showAnswer && safeZones.length > 0) {
      ctx.save();
      ctx.globalAlpha = 0.3;
      ctx.fillStyle = "#00ff88";
      for (const zone of safeZones) {
        drawSafeZone(ctx, zone, s);
      }
      ctx.restore();
    }

    // AoEs
    if (arenaState.aoes) {
      for (const aoe of arenaState.aoes) {
        drawAoE(ctx, aoe, s);
      }
    }

    // Tethers
    if (arenaState.tethers) {
      for (const t of arenaState.tethers) {
        ctx.save();
        ctx.strokeStyle = t.color || "#ff9900";
        ctx.lineWidth = 3;
        ctx.setLineDash([8, 4]);
        ctx.beginPath();
        ctx.moveTo(t.from.x * s, t.from.y * s);
        ctx.lineTo(t.to.x * s, t.to.y * s);
        ctx.stroke();
        ctx.restore();
      }
    }

    // Waymarks
    if (arenaState.markers) {
      for (const m of arenaState.markers) {
        drawMarker(ctx, m.id, m.x * s, m.y * s, s);
      }
    }

    // Boss
    if (arenaState.boss_position) {
      drawBoss(ctx, arenaState.boss_position.x * s, arenaState.boss_position.y * s, s, bossImg);
    }

    // Correct answer crosshair
    if (showAnswer && correctPosition) {
      drawTarget(ctx, correctPosition.x * s, correctPosition.y * s, "#00ff88", s);
    }

    // Submitted position
    if (submittedPosition) {
      const col =
        showAnswer && isCorrect !== null
          ? isCorrect
            ? "#00ff88"
            : "#ff4444"
          : ROLE_COLORS[role];
      drawPlayerDot(ctx, submittedPosition.x * s, submittedPosition.y * s, col, s);
    }

    // Hover ghost
    if (hoverPos && allowClick && !locked && !submittedPosition) {
      ctx.save();
      ctx.globalAlpha = 0.45;
      drawPlayerDot(ctx, hoverPos.x * s, hoverPos.y * s, ROLE_COLORS[role], s);
      ctx.restore();
    }
  }, [
    size,
    shape,
    arenaState,
    role,
    hoverPos,
    allowClick,
    locked,
    submittedPosition,
    correctPosition,
    showAnswer,
    isCorrect,
    safeZones,
    arenaImg,
    bossImg,
  ]);

  useEffect(() => {
    draw();
  }, [draw]);

  // Click handler
  const handleClick = (e: React.MouseEvent) => {
    if (!allowClick || locked || submittedPosition) return;
    const pos = canvasPos(e);
    onPositionClick?.(pos, e.timeStamp);
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!allowClick || locked || submittedPosition) return;
    setHoverPos(canvasPos(e));
  };

  const canvasPos = (e: React.MouseEvent): { x: number; y: number } => {
    const canvas = canvasRef.current!;
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    return {
      x: Math.max(0, Math.min(1, ((e.clientX - rect.left) * scaleX) / canvas.width)),
      y: Math.max(0, Math.min(1, ((e.clientY - rect.top) * scaleY) / canvas.height)),
    };
  };

  const cursorClass =
    allowClick && !locked && !submittedPosition
      ? "cursor-crosshair"
      : locked
        ? "cursor-not-allowed opacity-85"
        : "";

  return (
    <div className="flex flex-col items-center gap-3">
      <canvas
        ref={canvasRef}
        className={`rounded-lg max-w-full ${cursorClass}`}
        onClick={handleClick}
        onMouseMove={handleMouseMove}
        onMouseLeave={() => setHoverPos(null)}
      />

      {/* Debuff strip */}
      {arenaState.debuffs && arenaState.debuffs.length > 0 && (
        <div className="flex flex-wrap gap-2 justify-center">
          {arenaState.debuffs.map((d, i) => (
            <span
              key={i}
              className="px-3 py-1 rounded-full border bg-black/50 text-xs font-cinzel tracking-wide text-white/80"
              style={{ borderColor: d.color || "#fff" }}
            >
              {d.label}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

// --- Drawing helpers ---

function drawArenaFloor(
  ctx: CanvasRenderingContext2D,
  s: number,
  shape: ArenaShape,
  img: HTMLImageElement | null
) {
  ctx.save();

  if (shape === "CIRCLE") {
    ctx.beginPath();
    ctx.arc(s / 2, s / 2, s / 2 - 4, 0, Math.PI * 2);
    ctx.clip();
  }

  if (img) {
    ctx.drawImage(img, 0, 0, s, s);
    // Darken slightly so overlays remain readable
    ctx.fillStyle = "rgba(13,13,26,0.35)";
    ctx.fillRect(0, 0, s, s);
  } else {
    const grad = ctx.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s * 0.7);
    grad.addColorStop(0, "#1a1a2e");
    grad.addColorStop(0.6, "#16162a");
    grad.addColorStop(1, "#0d0d1a");
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, s, s);
  }

  // Grid
  ctx.strokeStyle = "rgba(255,255,255,0.04)";
  ctx.lineWidth = 1;
  for (let i = 0; i <= 10; i++) {
    const p = (i / 10) * s;
    ctx.beginPath();
    ctx.moveTo(p, 0);
    ctx.lineTo(p, s);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(0, p);
    ctx.lineTo(s, p);
    ctx.stroke();
  }

  // Cardinal cross
  ctx.strokeStyle = "rgba(255,255,255,0.12)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(s / 2, 0);
  ctx.lineTo(s / 2, s);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(0, s / 2);
  ctx.lineTo(s, s / 2);
  ctx.stroke();

  // Border
  ctx.strokeStyle = "rgba(180,140,80,0.6)";
  ctx.lineWidth = 4;
  if (shape === "CIRCLE") {
    ctx.beginPath();
    ctx.arc(s / 2, s / 2, s / 2 - 4, 0, Math.PI * 2);
    ctx.stroke();
  } else {
    ctx.strokeRect(4, 4, s - 8, s - 8);
  }

  ctx.restore();
}

function drawAoE(ctx: CanvasRenderingContext2D, aoe: ArenaAoE, s: number) {
  ctx.save();
  ctx.fillStyle = aoe.color || "rgba(255,80,80,0.4)";
  const edgeColor = (aoe.color || "rgba(255,80,80,0.4)")
    .replace(/[\d.]+\)$/, "0.9)");
  ctx.strokeStyle = edgeColor;
  ctx.lineWidth = 2;

  switch (aoe.shape) {
    case "circle":
      ctx.beginPath();
      ctx.arc(aoe.cx! * s, aoe.cy! * s, aoe.r! * s, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      break;
    case "rect":
      ctx.fillRect(aoe.x! * s, aoe.y! * s, aoe.w! * s, aoe.h! * s);
      ctx.strokeRect(aoe.x! * s, aoe.y! * s, aoe.w! * s, aoe.h! * s);
      break;
    case "cone": {
      const cx = aoe.cx! * s;
      const cy = aoe.cy! * s;
      const len = s * 0.9;
      const angleRad = ((aoe.angle || 0) * Math.PI) / 180;
      const spreadRad = ((aoe.spread || 90) * Math.PI) / 180;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, len, angleRad - spreadRad / 2, angleRad + spreadRad / 2);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
      break;
    }
  }

  // Label
  if (aoe.label) {
    const lx = aoe.cx !== undefined ? aoe.cx * s : (aoe.x! + aoe.w! / 2) * s;
    const ly = aoe.cy !== undefined ? aoe.cy * s : (aoe.y! + aoe.h! / 2) * s;
    ctx.fillStyle = "rgba(255,220,220,0.9)";
    ctx.font = `bold ${Math.max(10, s * 0.022)}px Cinzel, serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(aoe.label, lx, ly);
  }

  ctx.restore();
}

function drawMarker(
  ctx: CanvasRenderingContext2D,
  id: string,
  x: number,
  y: number,
  s: number
) {
  const color = MARKER_COLORS[id] || "#ffffff";
  const r = s * 0.028;

  ctx.save();
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fillStyle = color;
  ctx.globalAlpha = 0.85;
  ctx.fill();
  ctx.strokeStyle = "#fff";
  ctx.lineWidth = 2;
  ctx.stroke();

  ctx.fillStyle = "#fff";
  ctx.font = `bold ${r * 1.2}px Cinzel, serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.globalAlpha = 1;
  ctx.fillText(id, x, y);
  ctx.restore();
}

function drawBoss(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  s: number,
  img: HTMLImageElement | null
) {
  const r = s * 0.055;
  ctx.save();

  // Glow
  const glow = ctx.createRadialGradient(x, y, 0, x, y, r * 2);
  glow.addColorStop(0, "rgba(255,60,60,0.4)");
  glow.addColorStop(1, "rgba(255,60,60,0)");
  ctx.fillStyle = glow;
  ctx.beginPath();
  ctx.arc(x, y, r * 2, 0, Math.PI * 2);
  ctx.fill();

  if (img) {
    ctx.save();
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.clip();
    ctx.drawImage(img, x - r, y - r, r * 2, r * 2);
    ctx.restore();
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.strokeStyle = "#ff6666";
    ctx.lineWidth = 3;
    ctx.stroke();
  } else {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = "#cc2222";
    ctx.fill();
    ctx.strokeStyle = "#ff6666";
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.fillStyle = "#fff";
    ctx.font = `bold ${r * 0.9}px Cinzel, serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("\u2694", x, y);
  }

  ctx.restore();
}

function drawPlayerDot(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  color: string,
  s: number
) {
  const r = s * 0.04;
  ctx.save();

  // Glow
  const glow = ctx.createRadialGradient(x, y, 0, x, y, r * 2.5);
  glow.addColorStop(0, color + "80");
  glow.addColorStop(1, "transparent");
  ctx.fillStyle = glow;
  ctx.beginPath();
  ctx.arc(x, y, r * 2.5, 0, Math.PI * 2);
  ctx.fill();

  // Dot
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fillStyle = color;
  ctx.fill();
  ctx.strokeStyle = "#ffffff";
  ctx.lineWidth = 2;
  ctx.stroke();

  ctx.restore();
}

function drawTarget(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  color: string,
  s: number
) {
  const r = s * 0.045;
  ctx.save();
  ctx.strokeStyle = color;
  ctx.lineWidth = 3;

  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(x - r * 1.4, y);
  ctx.lineTo(x + r * 1.4, y);
  ctx.moveTo(x, y - r * 1.4);
  ctx.lineTo(x, y + r * 1.4);
  ctx.stroke();

  ctx.fillStyle = color;
  ctx.font = `bold ${r}px sans-serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("\u2713", x, y);
  ctx.restore();
}

function drawSafeZone(ctx: CanvasRenderingContext2D, zone: SafeZone, s: number) {
  if (zone.shape === "circle" || zone.cx !== undefined) {
    ctx.beginPath();
    ctx.arc(zone.cx! * s, zone.cy! * s, zone.r! * s, 0, Math.PI * 2);
    ctx.fill();
  } else if (zone.x !== undefined) {
    ctx.fillRect(zone.x * s, zone.y! * s, zone.w! * s, zone.h! * s);
  }
}
