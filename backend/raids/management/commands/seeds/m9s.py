"""
Seed data for M9S — Vamp Fatale (AAC Heavyweight M1 Savage, patch 7.4).

Timeline cross-referenced against Icy-Veins guide, FFXIV Consolegameswiki
ability list, and the Toxic Friends raidplan timestamps. wtfdig.info and
the YouTube animated guide are JS-rendered and not scrapable via WebFetch,
so role+spot positions below use the PF-standard 8-clock (MT=N, H1=NE,
M1=E, R1=SE, OT=S, H2=SW, M2=W, R2=NW) and LP1/LP2 light-party pairs
(LP1 = MT+H1+M1+R1, LP2 = OT+H2+M2+R2).

Phase 1: Killer Voice → Hardcore → Vamp Stomp (+Blast Beat) → Brutal Rain →
         Sadistic Screech (arena shrinks) → Coffinfiller → Half Moon →
         Dead Wake → Crowd Kill
Phase 2: Finale Fatale → Pulping Pulse → Aetherletting → Insatiable Thirst →
         Plummet (towers + doornail + buzzsaws)
Phase 3: Hell in a Cell → Ultrasonic Spread / Amp → Sanguine Scratch →
         Undead Deathmatch
"""


# ---------------------------------------------------------------------------
# Helpers — compact role_variants builders (mirror m12s.py)
# ---------------------------------------------------------------------------

def _shared_choice(choice_id: str, **extra) -> list[dict]:
    """Every role × spot picks the same choice (raidwides, cue mechanics)."""
    roles = ("TANK", "HEALER", "MELEE", "RANGED")
    return [
        {"role": r, "spot": s, "correct_choice": choice_id, **extra}
        for r in roles for s in (1, 2)
    ]


def _shared_position(pos: dict, tolerance: float | None = None,
                     safe_zones: list | None = None) -> list[dict]:
    """Every role × spot stands at the same position (stack mechanics)."""
    roles = ("TANK", "HEALER", "MELEE", "RANGED")
    out = []
    for r in roles:
        for s in (1, 2):
            v: dict = {"role": r, "spot": s, "correct_position": pos}
            if tolerance is not None:
                v["tolerance"] = tolerance
            if safe_zones is not None:
                v["safe_zones"] = safe_zones
            out.append(v)
    return out


def _clock_spread(positions: dict[tuple[str, int], dict], safe_zones=None) -> list[dict]:
    """Build role_variants from a {(role, spot): {x, y}} mapping."""
    out = []
    for (role, spot), pos in positions.items():
        v: dict = {"role": role, "spot": spot, "correct_position": pos}
        if safe_zones is not None:
            v["safe_zones"] = safe_zones
        out.append(v)
    return out


# Canonical 8-clock spread (PF-standard "modified" assignment).
CLOCK_8 = {
    ("TANK",   1): {"x": 0.50, "y": 0.10},  # N   (MT)
    ("HEALER", 1): {"x": 0.78, "y": 0.22},  # NE  (H1)
    ("MELEE",  1): {"x": 0.90, "y": 0.50},  # E   (M1)
    ("RANGED", 1): {"x": 0.78, "y": 0.78},  # SE  (R1)
    ("TANK",   2): {"x": 0.50, "y": 0.90},  # S   (OT)
    ("HEALER", 2): {"x": 0.22, "y": 0.78},  # SW  (H2)
    ("MELEE",  2): {"x": 0.10, "y": 0.50},  # W   (M2)
    ("RANGED", 2): {"x": 0.22, "y": 0.22},  # NW  (R2)
}

# Light-party towers — LP1 (MT/H1/M1/R1) vs LP2 (OT/H2/M2/R2).
# Used for Hell in a Cell rotation and Plummet tower soaks.
LP_TOWERS_4 = {
    # LP1 — north pair of towers
    ("TANK",   1): {"x": 0.25, "y": 0.25},  # NW  (MT)
    ("HEALER", 1): {"x": 0.75, "y": 0.25},  # NE  (H1)
    ("MELEE",  1): {"x": 0.25, "y": 0.25},  # NW  (M1 with MT)
    ("RANGED", 1): {"x": 0.75, "y": 0.25},  # NE  (R1 with H1)
    # LP2 — south pair of towers
    ("TANK",   2): {"x": 0.25, "y": 0.75},  # SW  (OT)
    ("HEALER", 2): {"x": 0.75, "y": 0.75},  # SE  (H2)
    ("MELEE",  2): {"x": 0.25, "y": 0.75},  # SW  (M2 with OT)
    ("RANGED", 2): {"x": 0.75, "y": 0.75},  # SE  (R2 with H2)
}


M9S_FIGHT = {
    "slug": "m9s",
    "name": "AAC Heavyweight M1 (Savage)",
    "short_name": "M9S",
    "boss_name": "Vamp Fatale",
    "difficulty": "SAVAGE",
    "arena_shape": "SQUARE",
    "order": 1,
    # Asset hooks — drop in CDN/local URLs (e.g. /assets/arenas/m9s-floor.png).
    "arena_image_url": "",
    "boss_image_url": "",
    "mechanics": [
        # ══════════════════════════════════════════════════════════════
        # Phase 1 — 4×4 square arena
        # ══════════════════════════════════════════════════════════════
        {
            "slug": "killer-voice",
            "name": "Killer Voice",
            "phase_name": "Phase 1",
            "description": "Opening raidwide. Mitigate and heal through.",
            "difficulty_rating": 1,
            "tags": ["raidwide"],
            "order": 1,
            "steps": [
                {
                    "order": 1,
                    "title": "Mitigate Raidwide",
                    "action_type": "CHOICE",
                    "arena_state": {"boss_position": {"x": 0.5, "y": 0.5}},
                    "choices": [
                        {"id": "mitigate", "label": "Use mitigation/shields"},
                        {"id": "nothing",  "label": "Do nothing"},
                    ],
                    "explanation": "Always mitigate raidwides.",
                    "role_variants": _shared_choice("mitigate"),
                },
            ],
        },
        {
            "slug": "hardcore",
            "name": "Hardcore",
            "phase_name": "Phase 1",
            "description": (
                "Shared tankbuster on the top two enmity targets. Both tanks "
                "stack to share, or one tank uses an invulnerability."
            ),
            "difficulty_rating": 2,
            "tags": ["tankbuster"],
            "order": 2,
            "steps": [
                {
                    "order": 1,
                    "title": "Tanks Stack North, Party South",
                    "narration": "MT and OT stack to share the cleave. Non-tanks clear the tank area.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.15,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "boss_facing": "north",
                    },
                    "explanation": "Tanks share in front of the boss; everyone else uptime south.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.50, "y": 0.30},  # MT
                        ("TANK",   2): {"x": 0.50, "y": 0.30},  # OT — stacked with MT
                        ("HEALER", 1): {"x": 0.60, "y": 0.75},
                        ("HEALER", 2): {"x": 0.40, "y": 0.75},
                        ("MELEE",  1): {"x": 0.55, "y": 0.65},
                        ("MELEE",  2): {"x": 0.45, "y": 0.65},
                        ("RANGED", 1): {"x": 0.70, "y": 0.80},
                        ("RANGED", 2): {"x": 0.30, "y": 0.80},
                    }),
                },
            ],
        },
        {
            "slug": "vamp-stomp",
            "name": "Vamp Stomp + Blast Beat",
            "phase_name": "Phase 1",
            "description": (
                "Vamp Fatale jumps to centre and summons Vampette bat adds at clock "
                "positions. Expanding ring cleanses Curse of the Bombpyre; bats "
                "explode in point-blank AoEs when the ring hits them."
            ),
            "difficulty_rating": 3,
            "tags": ["spread", "adds", "clock", "vuln"],
            "order": 3,
            "steps": [
                {
                    "order": 1,
                    "title": "Spread to Clock Spots",
                    "narration": (
                        "Spread to your assigned clock position. Each player "
                        "baits one Vampette."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.5, "r": 0.2,
                             "color": "rgba(255,80,80,0.25)", "label": "Vamp Stomp"},
                        ],
                    },
                    "explanation": (
                        "Standard 8-clock. Vuln cleanse by moving through the "
                        "expanding ring onto your bat (the ring's impact on the "
                        "bat resolves Blast Beat)."
                    ),
                    "role_variants": _clock_spread(CLOCK_8),
                },
            ],
        },
        {
            "slug": "brutal-rain",
            "name": "Brutal Rain",
            "phase_name": "Phase 1",
            "description": (
                "Multi-hit stack marker on a healer. Share the damage across "
                "the whole party. Hit count scales up over the fight."
            ),
            "difficulty_rating": 2,
            "tags": ["stack"],
            "order": 4,
            "steps": [
                {
                    "order": 1,
                    "title": "Stack on Marked Healer",
                    "narration": "One healer is marked. Stack tightly on them, south of the boss.",
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "default_tolerance": 0.10,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.4},
                        "debuffs": [
                            {"label": "Brutal Rain — Stack", "color": "#2b7fff"},
                        ],
                    },
                    "explanation": "Full-party stack. Mitigate — hits scale up with each cast.",
                    "role_variants": _shared_position({"x": 0.5, "y": 0.65}, tolerance=0.10),
                },
            ],
        },
        {
            "slug": "sadistic-screech",
            "name": "Sadistic Screech (Arena Shift)",
            "phase_name": "Phase 1",
            "description": (
                "Raidwide damage that shrinks the arena to a 2×4 rectangle "
                "(east and west columns removed). Summons Coffinmaker from north."
            ),
            "difficulty_rating": 2,
            "tags": ["raidwide", "arena-shift"],
            "order": 5,
            "steps": [
                {
                    "order": 1,
                    "title": "Move Off the Edges",
                    "narration": (
                        "East and west columns disappear. Get into the centre "
                        "2 columns before the cast resolves."
                    ),
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "rect", "x": 0.0, "y": 0.0, "w": 0.25, "h": 1.0,
                             "color": "rgba(255,80,80,0.35)", "label": "Removed"},
                            {"shape": "rect", "x": 0.75, "y": 0.0, "w": 0.25, "h": 1.0,
                             "color": "rgba(255,80,80,0.35)", "label": "Removed"},
                        ],
                    },
                    "explanation": "Stay in the inner 2 columns (0.25–0.75). Pre-position before Screech resolves.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.45, "y": 0.30},
                        ("TANK",   2): {"x": 0.55, "y": 0.70},
                        ("HEALER", 1): {"x": 0.55, "y": 0.30},
                        ("HEALER", 2): {"x": 0.45, "y": 0.70},
                        ("MELEE",  1): {"x": 0.40, "y": 0.50},
                        ("MELEE",  2): {"x": 0.60, "y": 0.50},
                        ("RANGED", 1): {"x": 0.60, "y": 0.30},
                        ("RANGED", 2): {"x": 0.40, "y": 0.70},
                    }),
                },
            ],
        },
        {
            "slug": "coffinfiller",
            "name": "Coffinfiller",
            "phase_name": "Phase 1",
            "description": (
                "Two columns of the Coffinmaker glow white, then fire line AoEs "
                "down those columns. The other two columns fire next."
            ),
            "difficulty_rating": 3,
            "tags": ["line", "dodge", "sequential"],
            "order": 6,
            "steps": [
                {
                    "order": 1,
                    "title": "Stand in Dark Columns (First Set)",
                    "narration": (
                        "The glowing columns fire first. Move into a dark column."
                    ),
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.12,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.2},
                        "aoes": [
                            {"shape": "rect", "x": 0.25, "y": 0.0, "w": 0.25, "h": 1.0,
                             "color": "rgba(255,80,80,0.35)", "label": "Lit"},
                        ],
                    },
                    "explanation": (
                        "Columns are 0.25 wide. Dark (safe) column is 0.50–0.75. "
                        "Swap to the other after first set resolves."
                    ),
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.60, "y": 0.40},
                        ("TANK",   2): {"x": 0.60, "y": 0.80},
                        ("HEALER", 1): {"x": 0.65, "y": 0.50},
                        ("HEALER", 2): {"x": 0.65, "y": 0.70},
                        ("MELEE",  1): {"x": 0.55, "y": 0.40},
                        ("MELEE",  2): {"x": 0.55, "y": 0.80},
                        ("RANGED", 1): {"x": 0.70, "y": 0.60},
                        ("RANGED", 2): {"x": 0.70, "y": 0.60},
                    }),
                },
            ],
        },
        {
            "slug": "half-moon",
            "name": "Half Moon",
            "phase_name": "Phase 1",
            "description": (
                "Boss cleaves one half of the arena, then the other. Arm raise "
                "telegraphs the first side. Size increases with 8+ Satisfied."
            ),
            "difficulty_rating": 2,
            "tags": ["cleave", "dodge"],
            "order": 7,
            "steps": [
                {
                    "order": 1,
                    "title": "Dodge to the Safe Side",
                    "narration": "Left arm raised → east safe; right arm raised → west safe.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "boss_facing": "south",
                        "aoes": [
                            {"shape": "rect", "x": 0.0, "y": 0.0, "w": 0.5, "h": 1.0,
                             "color": "rgba(255,80,80,0.3)", "label": "Half Moon (West)"},
                        ],
                    },
                    "explanation": "East half safe for the first cleave; flip sides for the second.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.65, "y": 0.45},
                        ("TANK",   2): {"x": 0.65, "y": 0.55},
                        ("HEALER", 1): {"x": 0.80, "y": 0.35},
                        ("HEALER", 2): {"x": 0.80, "y": 0.65},
                        ("MELEE",  1): {"x": 0.60, "y": 0.40},
                        ("MELEE",  2): {"x": 0.60, "y": 0.60},
                        ("RANGED", 1): {"x": 0.85, "y": 0.50},
                        ("RANGED", 2): {"x": 0.85, "y": 0.50},
                    }, safe_zones=[{"x": 0.5, "y": 0.0, "w": 0.5, "h": 1.0}]),
                },
            ],
        },
        {
            "slug": "dead-wake",
            "name": "Dead Wake",
            "phase_name": "Phase 1",
            "description": (
                "Coffinmaker charges forward one column; instant death to anyone "
                "caught in the fire trail. Kill it or sidestep."
            ),
            "difficulty_rating": 2,
            "tags": ["dodge", "add"],
            "order": 8,
            "steps": [
                {
                    "order": 1,
                    "title": "Clear the Coffinmaker's Column",
                    "narration": "The Coffinmaker moves south one block at a time. Don't stand in front.",
                    "timer_seconds": 4,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "rect", "x": 0.45, "y": 0.0, "w": 0.10, "h": 1.0,
                             "color": "rgba(255,80,80,0.45)", "label": "Dead Wake"},
                        ],
                    },
                    "explanation": "Move off the Coffinmaker's forward column. One-shot damage.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.30, "y": 0.40},
                        ("TANK",   2): {"x": 0.70, "y": 0.40},
                        ("HEALER", 1): {"x": 0.70, "y": 0.60},
                        ("HEALER", 2): {"x": 0.30, "y": 0.60},
                        ("MELEE",  1): {"x": 0.35, "y": 0.50},
                        ("MELEE",  2): {"x": 0.65, "y": 0.50},
                        ("RANGED", 1): {"x": 0.75, "y": 0.70},
                        ("RANGED", 2): {"x": 0.25, "y": 0.70},
                    }),
                },
            ],
        },
        {
            "slug": "crowd-kill",
            "name": "Crowd Kill",
            "phase_name": "Phase 1",
            "description": (
                "Raidwide that grants Vamp Fatale 4 stacks of Satisfied. "
                "No movement — deploy all available mitigation."
            ),
            "difficulty_rating": 2,
            "tags": ["raidwide"],
            "order": 9,
            "steps": [
                {
                    "order": 1,
                    "title": "Mitigate & Check Satisfied Count",
                    "action_type": "CHOICE",
                    "arena_state": {"boss_position": {"x": 0.5, "y": 0.5}},
                    "choices": [
                        {"id": "mitigate", "label": "Heavy mitigation"},
                        {"id": "nothing",  "label": "Do nothing"},
                    ],
                    "explanation": (
                        "Crowd Kill is a big raidwide AND increases boss damage by "
                        "4 stacks. Subsequent Hardcore/Half Moon/Vamp Stomp grow."
                    ),
                    "role_variants": _shared_choice("mitigate"),
                },
            ],
        },

        # ══════════════════════════════════════════════════════════════
        # Phase 2 — Circular death-wall arena
        # ══════════════════════════════════════════════════════════════
        {
            "slug": "finale-fatale",
            "name": "Finale Fatale",
            "phase_name": "Phase 2",
            "description": (
                "Transition raidwide. Arena becomes a circle; outer edge is a "
                "death wall. Mitigate heavily."
            ),
            "difficulty_rating": 2,
            "tags": ["raidwide", "transition"],
            "order": 10,
            "steps": [
                {
                    "order": 1,
                    "title": "Mitigate Transition",
                    "action_type": "CHOICE",
                    "arena_state": {"boss_position": {"x": 0.5, "y": 0.5}},
                    "choices": [
                        {"id": "mitigate", "label": "Use mitigation/shields"},
                        {"id": "nothing",  "label": "Do nothing"},
                    ],
                    "explanation": "Stay inside the shrinking circle. Death wall forms on the outside.",
                    "role_variants": _shared_choice("mitigate"),
                },
            ],
        },
        {
            "slug": "pulping-pulse",
            "name": "Pulping Pulse",
            "phase_name": "Phase 2",
            "description": "Ground circle AoEs resolve on a delay. Avoid stacked puddles.",
            "difficulty_rating": 2,
            "tags": ["puddle", "dodge"],
            "order": 11,
            "steps": [
                {
                    "order": 1,
                    "title": "Dodge Floor Puddles",
                    "narration": "Circular ground AoEs pop in sequence. Move to clean ground.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.3, "cy": 0.3, "r": 0.10,
                             "color": "rgba(160,0,200,0.3)", "label": "Pulse"},
                            {"shape": "circle", "cx": 0.7, "cy": 0.3, "r": 0.10,
                             "color": "rgba(160,0,200,0.3)", "label": "Pulse"},
                            {"shape": "circle", "cx": 0.3, "cy": 0.7, "r": 0.10,
                             "color": "rgba(160,0,200,0.3)", "label": "Pulse"},
                            {"shape": "circle", "cx": 0.7, "cy": 0.7, "r": 0.10,
                             "color": "rgba(160,0,200,0.3)", "label": "Pulse"},
                        ],
                    },
                    "explanation": "Stand between the puddles. Centre stays safe while outer pulses resolve.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.50, "y": 0.18},
                        ("TANK",   2): {"x": 0.50, "y": 0.82},
                        ("HEALER", 1): {"x": 0.50, "y": 0.50},
                        ("HEALER", 2): {"x": 0.50, "y": 0.50},
                        ("MELEE",  1): {"x": 0.18, "y": 0.50},
                        ("MELEE",  2): {"x": 0.82, "y": 0.50},
                        ("RANGED", 1): {"x": 0.50, "y": 0.30},
                        ("RANGED", 2): {"x": 0.50, "y": 0.70},
                    }),
                },
            ],
        },
        {
            "slug": "aetherletting",
            "name": "Aetherletting",
            "phase_name": "Phase 2",
            "description": (
                "Boss fires four cone AoEs rotating clockwise or counter-clockwise, "
                "then drops burn-mark circles on marked players (two per role in sequence). "
                "Burns leave + / × AoE patterns on the floor."
            ),
            "difficulty_rating": 4,
            "tags": ["cone", "dodge", "prey-marker"],
            "order": 12,
            "steps": [
                {
                    "order": 1,
                    "title": "Dodge the Four Cones",
                    "narration": "Cones fire at intercardinals. Stand at a cardinal.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 45,  "spread": 40,
                             "color": "rgba(180,60,60,0.35)", "label": "Cone"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 135, "spread": 40,
                             "color": "rgba(180,60,60,0.35)", "label": "Cone"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 225, "spread": 40,
                             "color": "rgba(180,60,60,0.35)", "label": "Cone"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 315, "spread": 40,
                             "color": "rgba(180,60,60,0.35)", "label": "Cone"},
                        ],
                    },
                    "explanation": "Cardinals are safe during the cone cast.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.50, "y": 0.15},
                        ("TANK",   2): {"x": 0.50, "y": 0.85},
                        ("HEALER", 1): {"x": 0.50, "y": 0.15},
                        ("HEALER", 2): {"x": 0.50, "y": 0.85},
                        ("MELEE",  1): {"x": 0.15, "y": 0.50},
                        ("MELEE",  2): {"x": 0.85, "y": 0.50},
                        ("RANGED", 1): {"x": 0.15, "y": 0.50},
                        ("RANGED", 2): {"x": 0.85, "y": 0.50},
                    }),
                },
                {
                    "order": 2,
                    "title": "Drop Burns Between Cones",
                    "narration": (
                        "Marked players step between cones to drop burn circles "
                        "offset counter-clockwise. Unmarked players clump centre."
                    ),
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "Prey — burn drop", "color": "#ffcc00"},
                        ],
                    },
                    "explanation": (
                        "Burns form + / × patterns on resolve. Drop them on the "
                        "cone lines so safe spots remain at cardinals."
                    ),
                    "role_variants": _clock_spread(CLOCK_8),
                },
            ],
        },
        {
            "slug": "insatiable-thirst",
            "name": "Insatiable Thirst",
            "phase_name": "Phase 2",
            "description": "Raidwide that reverts the arena to its original 4×4 shape.",
            "difficulty_rating": 1,
            "tags": ["raidwide"],
            "order": 13,
            "steps": [
                {
                    "order": 1,
                    "title": "Mitigate Revert",
                    "action_type": "CHOICE",
                    "arena_state": {"boss_position": {"x": 0.5, "y": 0.5}},
                    "choices": [
                        {"id": "mitigate", "label": "Use mitigation/shields"},
                        {"id": "nothing",  "label": "Do nothing"},
                    ],
                    "explanation": "Arena is restored; heal through and reposition for Plummet.",
                    "role_variants": _shared_choice("mitigate"),
                },
            ],
        },
        {
            "slug": "plummet",
            "name": "Plummet (Towers + Doornail + Buzzsaws)",
            "phase_name": "Phase 2",
            "description": (
                "Two tank towers spawn Fatal Flail adds (Barbed Burst is a wipe "
                "if the add lives). Puddle AoEs drop Deadly Doornail adds with "
                "expanding DoTs. Buzzsaws sweep across NW/SE and N/S lines."
            ),
            "difficulty_rating": 4,
            "tags": ["towers", "adds", "dodge", "dps-check"],
            "order": 14,
            "steps": [
                {
                    "order": 1,
                    "title": "Tanks Soak Towers, Party Dodges Saws",
                    "narration": (
                        "MT soaks the north tower (Fatal Flail). OT soaks the "
                        "south tower. DPS/healers burn Deadly Doornails and "
                        "dodge the buzzsaws."
                    ),
                    "timer_seconds": 8,
                    "action_type": "POSITION",
                    "default_tolerance": 0.12,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.18, "r": 0.09,
                             "color": "rgba(0,180,255,0.5)", "label": "Tower N"},
                            {"shape": "circle", "cx": 0.5, "cy": 0.82, "r": 0.09,
                             "color": "rgba(0,180,255,0.5)", "label": "Tower S"},
                            {"shape": "rect", "x": 0.0, "y": 0.42, "w": 1.0, "h": 0.16,
                             "color": "rgba(255,200,0,0.35)", "label": "Buzzsaw"},
                        ],
                    },
                    "explanation": "Tanks per tower; party in safe intercardinals; kill Doornails fast.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.50, "y": 0.18},  # MT north tower
                        ("TANK",   2): {"x": 0.50, "y": 0.82},  # OT south tower
                        ("HEALER", 1): {"x": 0.25, "y": 0.25},
                        ("HEALER", 2): {"x": 0.75, "y": 0.75},
                        ("MELEE",  1): {"x": 0.30, "y": 0.25},
                        ("MELEE",  2): {"x": 0.70, "y": 0.75},
                        ("RANGED", 1): {"x": 0.75, "y": 0.25},
                        ("RANGED", 2): {"x": 0.25, "y": 0.75},
                    }),
                },
            ],
        },

        # ══════════════════════════════════════════════════════════════
        # Phase 3 — Hell in a Cell, Deathmatch finale
        # ══════════════════════════════════════════════════════════════
        {
            "slug": "hell-in-a-cell",
            "name": "Hell in a Cell",
            "phase_name": "Phase 3",
            "description": (
                "Four towers spawn. Light Party 1 soaks first (each player is "
                "trapped in a Charnel Cell and must kill the add to escape). "
                "Light Party 2 stays outside to resolve Ultrasonic. Roles swap "
                "on the second set."
            ),
            "difficulty_rating": 5,
            "tags": ["towers", "soak", "light-party"],
            "order": 15,
            "steps": [
                {
                    "order": 1,
                    "title": "LP1 Soaks the Four Towers",
                    "narration": (
                        "LP1 (MT/H1/M1/R1) each soak one of the four intercardinal "
                        "towers. LP2 stays centre to handle the Ultrasonic cast."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.25, "cy": 0.25, "r": 0.09,
                             "color": "rgba(0,180,255,0.5)", "label": "Tower NW"},
                            {"shape": "circle", "cx": 0.75, "cy": 0.25, "r": 0.09,
                             "color": "rgba(0,180,255,0.5)", "label": "Tower NE"},
                            {"shape": "circle", "cx": 0.25, "cy": 0.75, "r": 0.09,
                             "color": "rgba(0,180,255,0.5)", "label": "Tower SW"},
                            {"shape": "circle", "cx": 0.75, "cy": 0.75, "r": 0.09,
                             "color": "rgba(0,180,255,0.5)", "label": "Tower SE"},
                        ],
                    },
                    "explanation": (
                        "Soakers gain Hell in a Cell / Hell Awaits. A second soak is "
                        "instant death, so LP1 handles set 1 only; LP2 sits outside."
                    ),
                    "role_variants": _clock_spread({
                        # LP1 soaks
                        ("TANK",   1): {"x": 0.25, "y": 0.25},  # MT NW
                        ("HEALER", 1): {"x": 0.75, "y": 0.25},  # H1 NE
                        ("MELEE",  1): {"x": 0.25, "y": 0.75},  # M1 SW
                        ("RANGED", 1): {"x": 0.75, "y": 0.75},  # R1 SE
                        # LP2 stays centre
                        ("TANK",   2): {"x": 0.50, "y": 0.55},
                        ("HEALER", 2): {"x": 0.50, "y": 0.45},
                        ("MELEE",  2): {"x": 0.45, "y": 0.50},
                        ("RANGED", 2): {"x": 0.55, "y": 0.50},
                    }),
                },
            ],
        },
        {
            "slug": "ultrasonic",
            "name": "Ultrasonic Spread or Amp",
            "phase_name": "Phase 3",
            "description": (
                "Simultaneous with Hell in a Cell. Boss casts either Ultrasonic "
                "Spread (cone AoE on one player per role) or Ultrasonic Amp "
                "(shared-damage cone — stack to split)."
            ),
            "difficulty_rating": 3,
            "tags": ["spread", "stack", "cue"],
            "order": 16,
            "steps": [
                {
                    "order": 1,
                    "title": "Read the Cast",
                    "narration": "Check the castbar — Spread = fan out, Amp = stack together.",
                    "action_type": "CHOICE",
                    "arena_state": {"boss_position": {"x": 0.5, "y": 0.5}},
                    "choices": [
                        {"id": "spread", "label": "Ultrasonic Spread — fan to role spots"},
                        {"id": "stack",  "label": "Ultrasonic Amp — stack to share"},
                    ],
                    "explanation": (
                        "Spread resolves as cone AoEs (tank takes the wide one). "
                        "Amp is a shared cone — stack all non-soaked players to split."
                    ),
                    # Vary per role: both Spread and Amp are valid practice targets;
                    # here we drill Spread as the common case, matching wtfdig's
                    # default resolution.
                    "role_variants": _shared_choice("spread"),
                },
            ],
        },
        {
            "slug": "sanguine-scratch",
            "name": "Sanguine Scratch",
            "phase_name": "Phase 3",
            "description": (
                "Five alternating cone AoEs from the boss. The first is "
                "telegraphed; the remaining four are invisible — read the rhythm."
            ),
            "difficulty_rating": 4,
            "tags": ["dodge", "cone", "rhythm"],
            "order": 17,
            "steps": [
                {
                    "order": 1,
                    "title": "Dodge the First Cone",
                    "narration": "First cone is visible. Move to the opposite side.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.15,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 0, "spread": 60,
                             "color": "rgba(180,60,60,0.35)", "label": "Scratch"},
                        ],
                    },
                    "explanation": "Remaining four cones alternate sides — pre-commit to the rhythm.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.50, "y": 0.82},
                        ("TANK",   2): {"x": 0.50, "y": 0.82},
                        ("HEALER", 1): {"x": 0.30, "y": 0.80},
                        ("HEALER", 2): {"x": 0.70, "y": 0.80},
                        ("MELEE",  1): {"x": 0.40, "y": 0.70},
                        ("MELEE",  2): {"x": 0.60, "y": 0.70},
                        ("RANGED", 1): {"x": 0.20, "y": 0.70},
                        ("RANGED", 2): {"x": 0.80, "y": 0.70},
                    }),
                },
            ],
        },
        {
            "slug": "undead-deathmatch",
            "name": "Undead Deathmatch",
            "phase_name": "Phase 3",
            "description": (
                "Two big towers (N and S). Soakers tether to rotating Vampettes "
                "that orbit 180° before casting either Breakdown Drop (donut) or "
                "Breakwing Beat (point-blank). Swap distance relative to the bat "
                "based on cast."
            ),
            "difficulty_rating": 5,
            "tags": ["towers", "tether", "rotation", "donut-pb"],
            "order": 18,
            "steps": [
                {
                    "order": 1,
                    "title": "Soak Light-Party Towers",
                    "narration": "LP1 soaks the north tower; LP2 soaks the south tower.",
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.2, "r": 0.12,
                             "color": "rgba(0,180,255,0.5)", "label": "Tower N"},
                            {"shape": "circle", "cx": 0.5, "cy": 0.8, "r": 0.12,
                             "color": "rgba(0,180,255,0.5)", "label": "Tower S"},
                        ],
                    },
                    "explanation": "Each light party stacks on its tower to soak the shared damage.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.50, "y": 0.20},
                        ("HEALER", 1): {"x": 0.50, "y": 0.20},
                        ("MELEE",  1): {"x": 0.50, "y": 0.20},
                        ("RANGED", 1): {"x": 0.50, "y": 0.20},
                        ("TANK",   2): {"x": 0.50, "y": 0.80},
                        ("HEALER", 2): {"x": 0.50, "y": 0.80},
                        ("MELEE",  2): {"x": 0.50, "y": 0.80},
                        ("RANGED", 2): {"x": 0.50, "y": 0.80},
                    }),
                },
                {
                    "order": 2,
                    "title": "Resolve the Bat Cast",
                    "narration": (
                        "Bats rotate 180° then cast — donut means stay on them at "
                        "melee range; point-blank means run out to the boss hitbox."
                    ),
                    "action_type": "CHOICE",
                    "arena_state": {"boss_position": {"x": 0.5, "y": 0.5}},
                    "choices": [
                        {"id": "donut",   "label": "Breakdown Drop — stay on bat"},
                        {"id": "pb",      "label": "Breakwing Beat — run out to boss"},
                    ],
                    "explanation": (
                        "Read the cast name. Donut is safe at point-blank; PB is "
                        "safe at max melee. Four casts per bat — keep rotating."
                    ),
                    # Practice the donut case — swap to "pb" in future drills.
                    "role_variants": _shared_choice("donut"),
                },
            ],
        },
    ],
}
