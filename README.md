# RaidCoach XIV — Mechanic Trainer

Interactive FFXIV mechanic drill trainer for **M1S-M4S**, **M9S-M12S**, and **FRU (Futures Rewritten Ultimate)**. Players select their role, pick a fight, and work through sequential mechanic steps on a live arena canvas — clicking to place their position and getting instant feedback.

---

## Features

- **Visual arena** — Canvas-rendered FFXIV arena (square or circle) with AoE zones, waymarks, tethers, boss position, and role-coloured player markers
- **Role-aware** — Mechanics solved per role (Tank, Healer, Melee DPS, Ranged DPS, Caster DPS) with independent correct positions
- **Two action types** — Position-click drills and multiple-choice decision drills
- **Timed drills** — Each step has a configurable countdown; missing the timer auto-fails and reveals the answer
- **Sequential steps** — Multi-step mechanics walk you through each phase of resolution
- **Correct answer overlay** — After answering, the correct position is shown with crosshair and explanation
- **Session scoring** — S/A/B/C/D grade at the end of each mechanic with per-step breakdown
- **Content-driven** — New fights and mechanics are added via data (seed command or Django Admin), not code
- **Django Admin** — Add/edit/delete any raid tier, fight, mechanic, step, or role variant through the admin UI
- **REST API** — Fully RESTful JSON API via Django REST Framework

---

## Prerequisites

- Python 3.11+
- Node.js 20+
- npm 9+
- Docker and Docker Compose (optional, for containerised setup)

---

## Quick Start

### Option A: Docker (recommended)

```bash
git clone <repo>
cd ffxiv_raid_trainer
docker-compose up
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

The Docker setup automatically runs migrations and seeds the database on first start.

### Option B: Manual

You need two terminals — one for the backend, one for the frontend.

**1. Backend**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_mechanics  # seeds M1S-M4S, M9S-M12S + FRU data
python manage.py createsuperuser # optional, for admin access
python manage.py runserver       # starts on http://localhost:8000
```

**2. Frontend** (in a second terminal)

```bash
cd frontend
npm install
npm run dev                      # starts on http://localhost:3000
```

The Next.js dev server proxies `/api` requests to the Django backend on port 8000. Open http://localhost:3000 to use the app.

---

## Running Tests

```bash
cd backend
source .venv/bin/activate
python manage.py test raids.tests -v2   # 31 tests: engine unit tests + API integration tests
```

---

## Project Structure

```
backend/                              Django 5.1 + DRF 3.17
├── config/
│   ├── settings.py                   Project settings (DB, CORS, DRF config)
│   ├── urls.py                       Root URL conf (/admin, /api)
│   └── wsgi.py                       WSGI entry point
├── raids/                            Main application
│   ├── models.py                     RaidTier, Fight, Mechanic, MechanicStep, RoleVariant, UserSession, DrillResult
│   ├── engine.py                     Stateless mechanic evaluator (evaluate_step, evaluate_position, evaluate_choice)
│   ├── serializers.py                DRF serializers (nested read + action serializers)
│   ├── views.py                      API views (list/detail for tiers/fights/mechanics, SimulateStepView, SessionStatsView)
│   ├── urls.py                       /api/ route definitions
│   ├── admin.py                      Full admin coverage with inlines
│   ├── management/commands/
│   │   └── seed_mechanics.py         Declarative seed data for M1S-M4S, M9S-M12S + FRU
│   └── tests/
│       ├── test_engine.py            Unit tests for engine pure functions
│       └── test_api.py               Integration tests for all API endpoints
├── Dockerfile
├── manage.py
└── requirements.txt

frontend/                             Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS
├── src/
│   ├── app/
│   │   ├── layout.tsx                Root layout (fonts, metadata)
│   │   ├── page.tsx                  Single-page app shell — renders component per Zustand phase
│   │   └── globals.css               Tailwind theme (gold/dark palette), Cinzel font, grain overlay
│   ├── components/
│   │   ├── Arena.tsx                 Canvas-based arena renderer (AoEs, markers, tethers, boss, player dots, safe zones)
│   │   ├── DrillView.tsx             Active drill: arena + timer + choice UI + result feedback
│   │   ├── DrillResults.tsx          Post-drill summary: grade, accuracy, per-step breakdown, retry
│   │   ├── FightBrowser.tsx          Fight selection grid grouped by raid tier
│   │   ├── Header.tsx                Sticky header with logo, role badge, breadcrumbs
│   │   ├── MechanicSelector.tsx      Mechanic list for selected fight, grouped by phase
│   │   ├── RoleSelector.tsx          Hero landing + 5-role card grid
│   │   └── Timer.tsx                 Countdown bar with urgent state
│   └── lib/
│       ├── types.ts                  TypeScript interfaces mirroring API responses
│       ├── api.ts                    HTTP client (fetch wrapper for all API calls)
│       └── store.ts                  Zustand store (AppPhase state machine, drill tracking)
├── next.config.ts                    API proxy rewrites (/api -> localhost:8000)
├── Dockerfile
└── package.json

docker-compose.yml                    Runs backend (:8000) + frontend (:3000)
```

---

## Architecture

The application uses a three-layer separation:

**Content layer** — Django models store all fight and mechanic data. The hierarchy is `RaidTier -> Fight -> Mechanic -> MechanicStep -> RoleVariant`. Role variants hold per-role correct answers so the same step can have different solutions for each role.

**Simulation engine** — `raids/engine.py` contains stateless pure functions. `evaluate_step(step, role, action)` returns a `StepResult` with correctness, explanation, distance from correct position, and whether there's a next step. No fight-specific logic exists in code — all behaviour is driven by the data.

**Presentation layer** — Next.js frontend with Zustand state management. The app flows through phases: `role-select -> fight-browse -> mechanic-select -> drilling -> result`. The Arena component renders everything on an HTML5 Canvas.

---

## Data Model

```
RaidTier
  └── Fight (ordered, difficulty-rated, arena shape)
        └── Mechanic (ordered, tagged, grouped by phase_name)
              └── MechanicStep (ordered, timed, action_type: POSITION or CHOICE)
                    └── RoleVariant (per-role correct answer)
                          ├── correct_position {x, y}    for POSITION steps
                          ├── correct_choice "id"         for CHOICE steps
                          ├── tolerance                   override (default: 12%)
                          ├── alt_positions []             alternative strat positions
                          └── safe_zones []                highlighted on reveal
```

All coordinates are **normalised 0-1** (origin top-left) so they scale to any canvas size.

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/raids/` | List active raid tiers |
| GET | `/api/raids/{slug}/` | Tier detail with nested fights |
| GET | `/api/fights/` | List fights (filter: `?tier=`, `?difficulty=`) |
| GET | `/api/fights/{slug}/` | Fight detail with mechanics |
| GET | `/api/mechanics/{id}/` | Mechanic with all steps and role variants |
| POST | `/api/simulate-step/` | Submit an answer, get validation result |
| GET | `/api/sessions/{key}/stats/` | Session accuracy and grade summary |

**POST /api/simulate-step/**

```json
{
  "step_id": 1,
  "role": "TANK",
  "submitted_x": 0.75,
  "submitted_y": 0.5,
  "session_key": "sess_abc123",
  "time_taken_ms": 2500
}
```

**Response:**

```json
{
  "is_correct": true,
  "explanation": "Step right to avoid the first cleave.",
  "correct_position": {"x": 0.75, "y": 0.5},
  "correct_choice": null,
  "distance": 0.0,
  "tolerance_used": 0.12,
  "has_next_step": true,
  "next_step_order": 2
}
```

---

## Adding New Content

### Via Django Admin

1. Go to http://localhost:8000/admin/ (requires superuser)
2. Under **Raid Tiers**, add or select a tier
3. Add fights under the tier
4. Add mechanics under each fight
5. Add steps to each mechanic — fill in `arena_state` JSON and `action_type`
6. Add role variants to each step with the correct position or choice per role

### Via seed data

Add entries to the `SEED_DATA` list in `backend/raids/management/commands/seed_mechanics.py` and re-run:

```bash
python manage.py seed_mechanics
```

Note: this clears and re-seeds all data.

### Arena State JSON Schema

```json
{
  "boss_position": {"x": 0.5, "y": 0.3},
  "boss_facing": "south",
  "markers": [
    {"id": "A", "x": 0.5, "y": 0.05}
  ],
  "aoes": [
    {
      "shape": "circle",
      "cx": 0.5, "cy": 0.5, "r": 0.15,
      "color": "rgba(255,80,80,0.4)",
      "label": "Nailchipper"
    },
    {
      "shape": "rect",
      "x": 0.0, "y": 0.0, "w": 0.5, "h": 1.0,
      "color": "rgba(255,80,80,0.35)",
      "label": "Left Cleave"
    },
    {
      "shape": "cone",
      "cx": 0.5, "cy": 0.5, "angle": 180, "spread": 90,
      "color": "rgba(160,100,255,0.4)",
      "label": "Cone AoE"
    }
  ],
  "tethers": [
    {"from": {"x": 0.3, "y": 0.5}, "to": {"x": 0.7, "y": 0.5}, "color": "#ff9900"}
  ],
  "debuffs": [
    {"label": "Lightning - Spread", "color": "#ffe066"}
  ]
}
```

---

## Seeded Content

The seed command populates the following:

| Tier | Fight | Mechanics |
|------|-------|-----------|
| AAC Light-heavyweight | M1S (Black Cat) | Leaping One-two Paw, Nailchipper (Spread), Mouser (Limit Cut) |
| AAC Light-heavyweight | M2S (Honey B. Lovely) | Honey B. Bombing, Alarm Pheromones |
| AAC Light-heavyweight | M3S (Brute Bomber) | Brutal Impact (Towers) |
| AAC Light-heavyweight | M4S (Wicked Thunder) | Witch Hunt |
| AAC Heavyweight | M9S (Vamp Fatale) | Half Moon, Aetherletting, Hell in a Cell |
| AAC Heavyweight | M10S (The Xtremes) | Cutback Blaze, Sick Swell, Insane Air |
| AAC Heavyweight | M11S (The Tyrant) | Trophy Weapons, Fire and Fury + Meteorain, Triple Tyrannhilation, Flatliner |
| AAC Heavyweight | M12S (Lindwurm) | Grotesquerie: Act 1, Ravenous Reach, Replication, Idyllic Dream |
| Futures Rewritten | FRU (Fatebreaker / Usurper of Frost) | Cyclonic Break, Diamond Dust |

Total: 3 tiers, 9 fights, 76 mechanics, 94 steps, 470 role variants.

---

## Roadmap

- [ ] M1S-M4S full mechanical coverage — expand via admin or seed data
- [ ] FRU all 5 phases — P3 Oracle, P4 Gaia, P5 Pandora
- [ ] Strat selector — toggle between community strats (e.g. Hamkatsu vs PF strats)
- [ ] Full fight mode — chain mechanics into a timeline with wipe tracking
- [ ] Replay mode — watch a full mechanic walkthrough before drilling
- [ ] Leaderboard — compare session accuracy by role
- [ ] Auth — optional user accounts for persistent score history
- [ ] Mobile touch — touch events for mobile-friendly drilling
- [ ] Randomised mechanic variants — different debuff/number assignments per attempt

---

## Data Sources

Mechanic data and strats referenced from:
- [WTFDIG](https://wtfdig.info/) — written mechanic guides
- [Raidplan.io](https://raidplan.io/) — visual strat diagrams
- Community resources and patch notes

---

*Not affiliated with or endorsed by Square Enix. FINAL FANTASY XIV is a registered trademark of Square Enix Holdings Co., Ltd.*
