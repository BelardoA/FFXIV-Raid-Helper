import {
  Component, Input, Output, EventEmitter, OnChanges, SimpleChanges,
  ElementRef, ViewChild, AfterViewInit, ChangeDetectionStrategy, HostListener
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { ArenaState, SafeZone, Role, RolePosition, ArenaShape } from '../../core/models/models';

export interface ClickPosition {
  x: number;  // normalised 0-1
  y: number;
}

const ROLE_COLORS: Record<Role, string> = {
  TANK:    '#2b7fff',
  HEALER:  '#22c77a',
  MELEE:   '#ff6b35',
  RANGED:  '#f4c430',
  CASTER:  '#b06aff',
};

@Component({
  selector: 'app-arena',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="arena-wrapper">
      <canvas
        #arenaCanvas
        class="arena-canvas"
        [class.clickable]="allowClick && !locked"
        [class.locked]="locked"
        (click)="onCanvasClick($event)"
        (mousemove)="onMouseMove($event)"
        (mouseleave)="onMouseLeave()"
      ></canvas>

      <!-- Debuff strip -->
      <div class="debuff-strip" *ngIf="arenaState?.debuffs?.length">
        <div
          class="debuff-badge"
          *ngFor="let d of arenaState!.debuffs"
          [style.border-color]="d.color || '#fff'"
        >
          <span class="debuff-label">{{ d.label }}</span>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .arena-wrapper {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
    }

    .arena-canvas {
      border-radius: 8px;
      display: block;
      max-width: 100%;
    }

    .arena-canvas.clickable { cursor: crosshair; }
    .arena-canvas.locked    { cursor: not-allowed; opacity: 0.85; }

    .debuff-strip {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      justify-content: center;
    }

    .debuff-badge {
      padding: 4px 12px;
      border: 1px solid #fff;
      border-radius: 20px;
      background: rgba(0,0,0,0.5);
      font-size: 0.75rem;
      font-family: 'Cinzel', serif;
      letter-spacing: 0.05em;
    }

    .debuff-label { color: #eee; }
  `],
})
export class ArenaComponent implements OnChanges, AfterViewInit {
  @ViewChild('arenaCanvas') canvasRef!: ElementRef<HTMLCanvasElement>;

  @Input() arenaState: ArenaState | null = null;
  @Input() shape: ArenaShape = 'SQUARE';
  @Input() role: Role | null = null;
  @Input() correctPositions: Record<string, RolePosition> | null = null;
  @Input() safeZones: SafeZone[] = [];
  @Input() allowClick = true;
  @Input() locked = false;
  @Input() showCorrectAnswer = false;
  @Input() submittedPosition: ClickPosition | null = null;

  @Output() positionClicked = new EventEmitter<ClickPosition>();

  private size = 500;
  private hoverPos: { x: number; y: number } | null = null;

  ngAfterViewInit() {
    this.resize();
    this.draw();
  }

  ngOnChanges(changes: SimpleChanges) {
    if (this.canvasRef) this.draw();
  }

  @HostListener('window:resize')
  onWindowResize() {
    this.resize();
    this.draw();
  }

  private resize() {
    const canvas = this.canvasRef?.nativeElement;
    if (!canvas) return;
    const parent = canvas.parentElement!;
    const s = Math.min(parent.clientWidth, 500);
    this.size = s;
    canvas.width = s;
    canvas.height = s;
  }

  private draw() {
    const canvas = this.canvasRef?.nativeElement;
    if (!canvas) return;
    const ctx = canvas.getContext('2d')!;
    const s = this.size;

    ctx.clearRect(0, 0, s, s);

    // ── Arena background ──────────────────────────────────────────────────
    this.drawArenaFloor(ctx, s);

    // ── Safe zones ────────────────────────────────────────────────────────
    if (this.showCorrectAnswer && this.safeZones?.length) {
      ctx.save();
      ctx.globalAlpha = 0.35;
      ctx.fillStyle = '#00ff88';
      for (const zone of this.safeZones) {
        this.drawSafeZone(ctx, zone, s);
      }
      ctx.restore();
    }

    // ── AoEs ──────────────────────────────────────────────────────────────
    if (this.arenaState?.aoes) {
      for (const aoe of this.arenaState.aoes) {
        this.drawAoE(ctx, aoe, s);
      }
    }

    // ── Tethers ───────────────────────────────────────────────────────────
    if (this.arenaState?.tethers) {
      for (const t of this.arenaState.tethers) {
        ctx.save();
        ctx.strokeStyle = t.color || '#ff9900';
        ctx.lineWidth = 3;
        ctx.setLineDash([8, 4]);
        ctx.beginPath();
        ctx.moveTo(t.from.x * s, t.from.y * s);
        ctx.lineTo(t.to.x * s, t.to.y * s);
        ctx.stroke();
        ctx.restore();
      }
    }

    // ── Waymarks ─────────────────────────────────────────────────────────
    if (this.arenaState?.markers) {
      for (const m of this.arenaState.markers) {
        this.drawMarker(ctx, m.id, m.x * s, m.y * s, s);
      }
    }

    // ── Boss ──────────────────────────────────────────────────────────────
    if (this.arenaState?.boss_position) {
      const bp = this.arenaState.boss_position;
      this.drawBoss(ctx, bp.x * s, bp.y * s, s);
    }

    // ── Correct answer overlay ────────────────────────────────────────────
    if (this.showCorrectAnswer && this.correctPositions && this.role) {
      const pos = this.correctPositions[this.role] ?? this.correctPositions['ANY'];
      if (pos) {
        this.drawTarget(ctx, pos.x * s, pos.y * s, '#00ff88', '✓', s);
      }
    }

    // ── Submitted position ────────────────────────────────────────────────
    if (this.submittedPosition) {
      const color = this.showCorrectAnswer
        ? (this.isSubmittedCorrect() ? '#00ff88' : '#ff4444')
        : (this.role ? ROLE_COLORS[this.role] : '#ffffff');
      this.drawPlayerMarker(ctx, this.submittedPosition.x * s, this.submittedPosition.y * s, color);
    }

    // ── Hover ghost ───────────────────────────────────────────────────────
    if (this.hoverPos && this.allowClick && !this.locked && !this.submittedPosition) {
      ctx.save();
      ctx.globalAlpha = 0.5;
      this.drawPlayerMarker(ctx, this.hoverPos.x * s, this.hoverPos.y * s,
        this.role ? ROLE_COLORS[this.role] : '#ffffff');
      ctx.restore();
    }
  }

  private drawArenaFloor(ctx: CanvasRenderingContext2D, s: number) {
    ctx.save();

    if (this.shape === 'CIRCLE') {
      // Circular clip
      ctx.beginPath();
      ctx.arc(s / 2, s / 2, s / 2 - 4, 0, Math.PI * 2);
      ctx.clip();
    }

    // Dark stone floor with subtle grid
    const grad = ctx.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s * 0.7);
    grad.addColorStop(0, '#1a1a2e');
    grad.addColorStop(0.6, '#16162a');
    grad.addColorStop(1, '#0d0d1a');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, s, s);

    // Subtle grid lines
    ctx.strokeStyle = 'rgba(255,255,255,0.04)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 10; i++) {
      const p = (i / 10) * s;
      ctx.beginPath(); ctx.moveTo(p, 0); ctx.lineTo(p, s); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0, p); ctx.lineTo(s, p); ctx.stroke();
    }

    // Cardinal cross lines
    ctx.strokeStyle = 'rgba(255,255,255,0.12)';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(s / 2, 0); ctx.lineTo(s / 2, s); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, s / 2); ctx.lineTo(s, s / 2); ctx.stroke();

    // Arena border
    if (this.shape === 'CIRCLE') {
      ctx.beginPath();
      ctx.arc(s / 2, s / 2, s / 2 - 4, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(180,140,80,0.6)';
      ctx.lineWidth = 4;
      ctx.stroke();
    } else {
      ctx.strokeStyle = 'rgba(180,140,80,0.6)';
      ctx.lineWidth = 4;
      ctx.strokeRect(4, 4, s - 8, s - 8);
    }

    ctx.restore();
  }

  private drawAoE(ctx: CanvasRenderingContext2D, aoe: any, s: number) {
    ctx.save();
    ctx.fillStyle = aoe.color || 'rgba(255,80,80,0.4)';
    ctx.strokeStyle = aoe.color?.replace(/[\d.]+\)$/, '0.9)') || 'rgba(255,80,80,0.9)';
    ctx.lineWidth = 2;

    switch (aoe.shape) {
      case 'circle':
        ctx.beginPath();
        ctx.arc(aoe.cx * s, aoe.cy * s, aoe.r * s, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        break;
      case 'rect':
        ctx.fillRect(aoe.x * s, aoe.y * s, aoe.w * s, aoe.h * s);
        ctx.strokeRect(aoe.x * s, aoe.y * s, aoe.w * s, aoe.h * s);
        break;
      case 'cone': {
        const cx = aoe.cx * s, cy = aoe.cy * s;
        const len = s * 0.9;
        const angleRad = (aoe.angle || 0) * Math.PI / 180;
        const spreadRad = (aoe.spread || 90) * Math.PI / 180;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.arc(cx, cy, len, angleRad - spreadRad / 2, angleRad + spreadRad / 2);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        break;
      }
    }

    // AoE label
    if (aoe.label) {
      const lx = aoe.cx !== undefined ? aoe.cx * s : (aoe.x + aoe.w / 2) * s;
      const ly = aoe.cy !== undefined ? aoe.cy * s : (aoe.y + aoe.h / 2) * s;
      ctx.fillStyle = 'rgba(255,220,220,0.9)';
      ctx.font = `bold ${Math.max(10, s * 0.022)}px Cinzel, serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(aoe.label, lx, ly);
    }

    ctx.restore();
  }

  private drawMarker(ctx: CanvasRenderingContext2D, id: string, x: number, y: number, s: number) {
    const MARKER_COLORS: Record<string, string> = {
      'A': '#ff4444', 'B': '#ffcc00', 'C': '#66aaff', 'D': '#aa44ff',
      '1': '#ff6600', '2': '#ffff00', '3': '#33ccff', '4': '#ff66cc',
    };
    const color = MARKER_COLORS[id] || '#ffffff';
    const r = s * 0.028;

    ctx.save();
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.globalAlpha = 0.85;
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.fillStyle = '#fff';
    ctx.font = `bold ${r * 1.2}px Cinzel, serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.globalAlpha = 1;
    ctx.fillText(id, x, y);
    ctx.restore();
  }

  private drawBoss(ctx: CanvasRenderingContext2D, x: number, y: number, s: number) {
    const r = s * 0.055;
    ctx.save();

    // Glow
    const glow = ctx.createRadialGradient(x, y, 0, x, y, r * 2);
    glow.addColorStop(0, 'rgba(255,60,60,0.4)');
    glow.addColorStop(1, 'rgba(255,60,60,0)');
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(x, y, r * 2, 0, Math.PI * 2);
    ctx.fill();

    // Boss circle
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = '#cc2222';
    ctx.fill();
    ctx.strokeStyle = '#ff6666';
    ctx.lineWidth = 3;
    ctx.stroke();

    // Boss label
    ctx.fillStyle = '#fff';
    ctx.font = `bold ${r * 0.9}px Cinzel, serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('⚔', x, y);

    ctx.restore();
  }

  private drawPlayerMarker(ctx: CanvasRenderingContext2D, x: number, y: number, color: string) {
    const r = this.size * 0.04;
    ctx.save();

    // Shadow glow
    const glow = ctx.createRadialGradient(x, y, 0, x, y, r * 2.5);
    glow.addColorStop(0, color.replace(')', ', 0.5)').replace('rgb', 'rgba'));
    glow.addColorStop(1, 'transparent');
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(x, y, r * 2.5, 0, Math.PI * 2);
    ctx.fill();

    // Player dot
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.restore();
  }

  private drawTarget(ctx: CanvasRenderingContext2D, x: number, y: number, color: string, label: string, s: number) {
    const r = s * 0.045;
    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = 3;

    // Crosshair circle
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.stroke();

    // Cross lines
    ctx.beginPath();
    ctx.moveTo(x - r * 1.4, y); ctx.lineTo(x + r * 1.4, y);
    ctx.moveTo(x, y - r * 1.4); ctx.lineTo(x, y + r * 1.4);
    ctx.stroke();

    ctx.fillStyle = color;
    ctx.font = `bold ${r}px sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(label, x, y);
    ctx.restore();
  }

  private drawSafeZone(ctx: CanvasRenderingContext2D, zone: SafeZone, s: number) {
    if (zone.shape === 'circle' || zone.cx !== undefined) {
      ctx.beginPath();
      ctx.arc(zone.cx! * s, zone.cy! * s, zone.r! * s, 0, Math.PI * 2);
      ctx.fill();
    } else if (zone.x !== undefined) {
      ctx.fillRect(zone.x * s, zone.y! * s, zone.w! * s, zone.h! * s);
    }
  }

  private isSubmittedCorrect(): boolean {
    if (!this.submittedPosition || !this.correctPositions || !this.role) return false;
    const pos = this.correctPositions[this.role] ?? this.correctPositions['ANY'];
    if (!pos) return true;
    const dx = this.submittedPosition.x - pos.x;
    const dy = this.submittedPosition.y - pos.y;
    return Math.sqrt(dx * dx + dy * dy) <= 0.12;
  }

  onCanvasClick(event: MouseEvent) {
    if (!this.allowClick || this.locked) return;
    const pos = this.getCanvasPos(event);
    this.positionClicked.emit(pos);
  }

  onMouseMove(event: MouseEvent) {
    if (!this.allowClick || this.locked) return;
    this.hoverPos = this.getCanvasPos(event);
    this.draw();
  }

  onMouseLeave() {
    this.hoverPos = null;
    this.draw();
  }

  private getCanvasPos(event: MouseEvent): ClickPosition {
    const canvas = this.canvasRef.nativeElement;
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    return {
      x: Math.max(0, Math.min(1, ((event.clientX - rect.left) * scaleX) / canvas.width)),
      y: Math.max(0, Math.min(1, ((event.clientY - rect.top) * scaleY) / canvas.height)),
    };
  }
}
