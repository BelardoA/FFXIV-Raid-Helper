import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { DrillStateService } from './core/services/drill-state.service';
import { RoleSelectComponent } from './features/role-select/role-select.component';
import { FightSelectComponent } from './features/fight-select/fight-select.component';
import { MechanicSelectComponent } from './features/mechanic-select/mechanic-select.component';
import { MechanicDrillComponent } from './features/mechanic-drill/mechanic-drill.component';
import { SessionResultComponent } from './features/mechanic-drill/session-result.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    HttpClientModule,
    RoleSelectComponent,
    FightSelectComponent,
    MechanicSelectComponent,
    MechanicDrillComponent,
    SessionResultComponent,
  ],
  template: `
    <div class="app-shell">

      <!-- ── Atmospheric grain overlay ── -->
      <div class="grain" aria-hidden="true"></div>

      <!-- ── Header ── -->
      <header class="app-header">
        <button class="logo-btn" (click)="state.reset()">
          <span class="logo-rune">⚔</span>
          <span class="logo-text">
            <span class="logo-main">RaidCoach</span>
            <span class="logo-sub">XIV Mechanic Trainer</span>
          </span>
        </button>

        <nav class="header-nav" *ngIf="state.phase() !== 'role-select'">
          <div class="phase-crumbs">
            <span
              class="crumb-step"
              [class.active]="state.phase() === 'fight-select'"
              [class.done]="isDone('fight-select')"
            >
              <span class="crumb-dot">{{ isDone('fight-select') ? '✓' : '1' }}</span>
              Select Fight
            </span>
            <span class="crumb-arrow">›</span>
            <span
              class="crumb-step"
              [class.active]="state.phase() === 'mechanic-select'"
              [class.done]="isDone('mechanic-select')"
            >
              <span class="crumb-dot">{{ isDone('mechanic-select') ? '✓' : '2' }}</span>
              Mechanic
            </span>
            <span class="crumb-arrow">›</span>
            <span
              class="crumb-step"
              [class.active]="state.phase() === 'drilling' || state.phase() === 'result'"
            >
              <span class="crumb-dot">3</span>
              Drill
            </span>
          </div>
        </nav>
      </header>

      <!-- ── Hero only on landing ── -->
      <div class="hero" *ngIf="state.phase() === 'role-select'">
        <div class="hero-bg">
          <div class="hero-crystal crystal-1"></div>
          <div class="hero-crystal crystal-2"></div>
          <div class="hero-crystal crystal-3"></div>
        </div>
        <div class="hero-content">
          <div class="hero-eyebrow">FFXIV • Patch 7.x</div>
          <h1 class="hero-title">
            <span class="title-line-1">Master the</span>
            <span class="title-line-2">Mechanics</span>
          </h1>
          <p class="hero-desc">
            Interactive mechanic drills for M1S–M4S and FRU.<br>
            Train your muscle memory before the next prog night.
          </p>
        </div>
      </div>

      <!-- ── Main content ── -->
      <main class="app-main">
        <app-role-select     *ngIf="state.phase() === 'role-select'"     />
        <app-fight-select    *ngIf="state.phase() === 'fight-select'"    />
        <app-mechanic-select *ngIf="state.phase() === 'mechanic-select'" />
        <app-mechanic-drill  *ngIf="state.phase() === 'drilling'"        />
        <app-session-result  *ngIf="state.phase() === 'result'"          />
      </main>

      <!-- ── Footer ── -->
      <footer class="app-footer">
        <span>Mechanic data sourced from community guides.</span>
        <span class="footer-sep">·</span>
        <span>Not affiliated with Square Enix.</span>
      </footer>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      min-height: 100vh;
    }

    .app-shell {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      background: #0d0d1a;
      position: relative;
    }

    /* ── Grain overlay ── */
    .grain {
      position: fixed;
      inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='1'/%3E%3C/svg%3E");
      opacity: 0.025;
      pointer-events: none;
      z-index: 1;
    }

    /* ── Header ── */
    .app-header {
      position: sticky;
      top: 0;
      z-index: 100;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.75rem 1.5rem;
      background: rgba(13, 13, 26, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(200, 164, 90, 0.15);
    }

    .logo-btn {
      background: none;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0;
    }

    .logo-rune {
      font-size: 1.5rem;
      color: #c8a45a;
      text-shadow: 0 0 16px rgba(200, 164, 90, 0.6);
      line-height: 1;
    }

    .logo-text {
      display: flex;
      flex-direction: column;
      text-align: left;
    }

    .logo-main {
      font-family: 'Cinzel', serif;
      font-size: 1rem;
      font-weight: 900;
      color: #e8d5a3;
      letter-spacing: 0.08em;
      line-height: 1;
    }

    .logo-sub {
      font-size: 0.6rem;
      color: #7a6a50;
      letter-spacing: 0.15em;
      text-transform: uppercase;
    }

    /* ── Phase breadcrumbs ── */
    .phase-crumbs {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .crumb-step {
      display: flex;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.72rem;
      color: rgba(255,255,255,0.2);
      letter-spacing: 0.05em;
      transition: color 0.2s;
    }

    .crumb-step.active { color: #c8a45a; }
    .crumb-step.done   { color: #22c77a; }

    .crumb-dot {
      width: 18px;
      height: 18px;
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 0.6rem;
      font-weight: 700;
      border: 1px solid currentColor;
      font-family: 'Cinzel', serif;
    }

    .crumb-arrow { color: rgba(255,255,255,0.15); font-size: 0.8rem; }

    /* ── Hero ── */
    .hero {
      position: relative;
      overflow: hidden;
      padding: 4rem 1.5rem 3rem;
      text-align: center;
    }

    .hero-bg {
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse at 50% 0%, rgba(200,164,90,0.08) 0%, transparent 70%);
    }

    .hero-crystal {
      position: absolute;
      border-radius: 50%;
      filter: blur(60px);
      opacity: 0.08;
      animation: float 6s ease-in-out infinite;
    }

    .crystal-1 {
      width: 300px; height: 300px;
      background: #2b7fff;
      top: -100px; left: 10%;
      animation-delay: 0s;
    }

    .crystal-2 {
      width: 400px; height: 400px;
      background: #b06aff;
      top: -150px; right: 5%;
      animation-delay: 2s;
    }

    .crystal-3 {
      width: 200px; height: 200px;
      background: #c8a45a;
      bottom: -50px; left: 45%;
      animation-delay: 4s;
    }

    @keyframes float {
      0%, 100% { transform: translateY(0); }
      50%       { transform: translateY(-20px); }
    }

    .hero-content { position: relative; z-index: 1; }

    .hero-eyebrow {
      font-size: 0.7rem;
      letter-spacing: 0.3em;
      color: #c8a45a;
      font-family: 'Cinzel', serif;
      margin-bottom: 1rem;
    }

    .hero-title {
      margin: 0 0 1rem;
      line-height: 1;
    }

    .title-line-1 {
      display: block;
      font-family: 'Cinzel', serif;
      font-size: clamp(1.5rem, 4vw, 2.5rem);
      font-weight: 400;
      color: #9a8a6a;
      letter-spacing: 0.05em;
    }

    .title-line-2 {
      display: block;
      font-family: 'Cinzel', serif;
      font-size: clamp(2.5rem, 8vw, 5rem);
      font-weight: 900;
      background: linear-gradient(135deg, #e8d5a3, #c8a45a, #a07a3a);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      letter-spacing: -0.01em;
    }

    .hero-desc {
      font-size: clamp(0.85rem, 1.5vw, 1rem);
      color: #7a6a50;
      line-height: 1.8;
      max-width: 480px;
      margin: 0 auto;
    }

    /* ── Main ── */
    .app-main {
      flex: 1;
      position: relative;
      z-index: 2;
    }

    /* ── Footer ── */
    .app-footer {
      padding: 1.5rem;
      text-align: center;
      font-size: 0.7rem;
      color: rgba(255,255,255,0.15);
      letter-spacing: 0.05em;
      border-top: 1px solid rgba(255,255,255,0.05);
      display: flex;
      justify-content: center;
      gap: 0.5rem;
      flex-wrap: wrap;
    }

    .footer-sep { opacity: 0.4; }
  `],
})
export class AppComponent {
  state = inject(DrillStateService);

  readonly PHASE_ORDER = ['role-select', 'fight-select', 'mechanic-select', 'drilling', 'result'];

  isDone(phase: string): boolean {
    const current = this.PHASE_ORDER.indexOf(this.state.phase());
    const target   = this.PHASE_ORDER.indexOf(phase);
    return current > target;
  }
}
