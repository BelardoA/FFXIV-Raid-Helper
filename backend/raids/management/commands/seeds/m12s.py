"""
Seed data for M12S — Lindwurm (AAC Heavyweight M4 Savage).

Structural demo of the spot-aware layout (wtfdig.info convention):
  T1/T2, H1/H2, M1/M2, R1/R2 — party slots differentiate correct answers.

Cardinal spread (8-clock, PF "modified" standard):
    MT=N, H1=NE, M1=E, R1=SE, OT=S, H2=SW, M2=W, R2=NW
Tower pairs (2 per tower):
    NW=MT+H1, NE=M1+R1, SW=OT+H2, SE=M2+R2

Door Boss + Final Boss as one Fight, distinguished by phase_name.
Door Boss (Acts 1-4): The Fixer → Mortal Slayer → Grotesquerie Act 1 →
    Ravenous Reach → Visceral Burst → Grotesquerie Act 2 → Roiling Mass →
    Grotesquerie Act 3 → Split Scourge → Curtain Call → Splattershed
Final Boss (Phases 1-4): Arcadia Aflame → Replication 1 → Snaking Kick →
    Double Sobat → Staging + Replication 2 → Firefall Splash →
    Blood Mana → Idyllic Dream → Twisted Vision
"""


# ---------------------------------------------------------------------------
# Helpers — compact role_variants builders
# ---------------------------------------------------------------------------

def _shared_choice(choice_id: str, **extra) -> list[dict]:
    """Every role × spot picks the same choice (raidwides, tank swap cues)."""
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
    """
    Build role_variants from a {(role, spot): {x, y}} mapping.
    Any pair not present uses (role, spot=1) as the fallback at load time.
    """
    out = []
    for (role, spot), pos in positions.items():
        v: dict = {"role": role, "spot": spot, "correct_position": pos}
        if safe_zones is not None:
            v["safe_zones"] = safe_zones
        out.append(v)
    return out


# Canonical 8-clock spread (PF-standard "modified" assignment).
# Keys: ("TANK", 1) = MT, ("TANK", 2) = OT, etc.
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

# Tower pairs — each tower takes two players (same position, different role/spot).
TOWERS_4 = {
    ("TANK",   1): {"x": 0.25, "y": 0.25},  # NW with H1
    ("HEALER", 1): {"x": 0.25, "y": 0.25},  # NW with MT
    ("MELEE",  1): {"x": 0.75, "y": 0.25},  # NE with R1
    ("RANGED", 1): {"x": 0.75, "y": 0.25},  # NE with M1
    ("TANK",   2): {"x": 0.25, "y": 0.75},  # SW with H2
    ("HEALER", 2): {"x": 0.25, "y": 0.75},  # SW with OT
    ("MELEE",  2): {"x": 0.75, "y": 0.75},  # SE with R2
    ("RANGED", 2): {"x": 0.75, "y": 0.75},  # SE with M2
}


M12S_FIGHT = {
    "slug": "m12s",
    "name": "AAC Heavyweight M4 (Savage)",
    "short_name": "M12S",
    "boss_name": "Lindwurm",
    "difficulty": "SAVAGE",
    "arena_shape": "CIRCLE",
    "order": 4,
    # Asset hooks — blank strings render the default canvas floor + boss dot.
    # Drop in CDN/local URLs (e.g. /assets/arenas/m12s-floor.png) when available.
    "arena_image_url": "",
    "boss_image_url": "",
    "mechanics": [
        # ══════════════════════════════════════════════════════════════
        # Door Boss
        # ══════════════════════════════════════════════════════════════
        {
            "slug": "the-fixer",
            "name": "The Fixer",
            "phase_name": "Door Boss: Act 1",
            "description": (
                "Raidwide damage. Lindwurm's signature attack. "
                "Mitigate and heal."
            ),
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
            "slug": "mortal-slayer",
            "name": "Mortal Slayer",
            "phase_name": "Door Boss: Act 1",
            "description": (
                "Spread to 8-clock positions to bait the orbs. Each player "
                "covers their assigned clock spot."
            ),
            "difficulty_rating": 3,
            "tags": ["bait", "orb", "spread"],
            "order": 2,
            "steps": [
                {
                    "order": 1,
                    "title": "Bait Your Clock Spot",
                    "narration": (
                        "8 orbs telegraph — each party member baits a single "
                        "clock position (MT=N, H1=NE, M1=E, R1=SE, "
                        "OT=S, H2=SW, M2=W, R2=NW)."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.50, "cy": 0.05, "r": 0.05, "color": "rgba(255,200,0,0.6)", "label": "N"},
                            {"shape": "circle", "cx": 0.82, "cy": 0.18, "r": 0.05, "color": "rgba(255,200,0,0.6)", "label": "NE"},
                            {"shape": "circle", "cx": 0.95, "cy": 0.50, "r": 0.05, "color": "rgba(255,200,0,0.6)", "label": "E"},
                            {"shape": "circle", "cx": 0.82, "cy": 0.82, "r": 0.05, "color": "rgba(255,200,0,0.6)", "label": "SE"},
                            {"shape": "circle", "cx": 0.50, "cy": 0.95, "r": 0.05, "color": "rgba(255,200,0,0.6)", "label": "S"},
                            {"shape": "circle", "cx": 0.18, "cy": 0.82, "r": 0.05, "color": "rgba(255,200,0,0.6)", "label": "SW"},
                            {"shape": "circle", "cx": 0.05, "cy": 0.50, "r": 0.05, "color": "rgba(255,200,0,0.6)", "label": "W"},
                            {"shape": "circle", "cx": 0.18, "cy": 0.18, "r": 0.05, "color": "rgba(255,200,0,0.6)", "label": "NW"},
                        ],
                    },
                    "explanation": "Stand on your clock spot to intercept only your orb.",
                    "role_variants": _clock_spread(CLOCK_8),
                },
            ],
        },
        {
            "slug": "grotesquerie-act1",
            "name": "Grotesquerie: Act 1",
            "phase_name": "Door Boss: Act 1",
            "description": (
                "Directed cones on each player. Spread to 8-clock and aim "
                "your cone outward."
            ),
            "difficulty_rating": 4,
            "tags": ["cone", "directional", "debuff"],
            "order": 3,
            "steps": [
                {
                    "order": 1,
                    "title": "Aim Your Directed Grotesquerie",
                    "narration": "Stand on your clock spot — cone fires outward from the party.",
                    "timer_seconds": 7,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "Directed Grotesquerie — Cone fires your direction", "color": "#ff6b35"},
                            {"label": "Bursting Grotesquerie — AoE on self", "color": "#cc44ff"},
                            {"label": "Shared Grotesquerie — Stack marker", "color": "#2b7fff"},
                        ],
                    },
                    "explanation": "Face your cone outward. Bursting = spread, Shared = stack with partner.",
                    "role_variants": _clock_spread(CLOCK_8),
                },
            ],
        },
        {
            "slug": "ravenous-reach",
            "name": "Ravenous Reach",
            "phase_name": "Door Boss: Act 1",
            "description": (
                "Bait puddles south-left (G1) and south-right (G2), "
                "then dodge the arm cone north."
            ),
            "difficulty_rating": 3,
            "tags": ["bait", "puddle", "cone", "dodge"],
            "order": 4,
            "steps": [
                {
                    "order": 1,
                    "title": "Bait Ground AoEs — Your Group's Side",
                    "narration": "G1 (T1/H1/M1/R1) baits SW. G2 (T2/H2/M2/R2) baits SE.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.30, "cy": 0.72, "r": 0.08, "color": "rgba(255,80,80,0.4)", "label": "G1 Bait"},
                            {"shape": "circle", "cx": 0.70, "cy": 0.72, "r": 0.08, "color": "rgba(255,80,80,0.4)", "label": "G2 Bait"},
                        ],
                    },
                    "explanation": "Split bait by group so puddles land evenly.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.28, "y": 0.72},
                        ("HEALER", 1): {"x": 0.34, "y": 0.72},
                        ("MELEE",  1): {"x": 0.26, "y": 0.66},
                        ("RANGED", 1): {"x": 0.32, "y": 0.78},
                        ("TANK",   2): {"x": 0.72, "y": 0.72},
                        ("HEALER", 2): {"x": 0.66, "y": 0.72},
                        ("MELEE",  2): {"x": 0.74, "y": 0.66},
                        ("RANGED", 2): {"x": 0.68, "y": 0.78},
                    }),
                },
                {
                    "order": 2,
                    "title": "Dodge Arm Cone — Move North",
                    "narration": "Arm cone covers the southern half. Move to the north lane between puddles.",
                    "timer_seconds": 4,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 180, "spread": 90,
                             "color": "rgba(255,60,60,0.35)", "label": "Arm Cone"},
                            {"shape": "circle", "cx": 0.30, "cy": 0.72, "r": 0.12, "color": "rgba(160,0,200,0.3)", "label": "Puddle"},
                            {"shape": "circle", "cx": 0.70, "cy": 0.72, "r": 0.12, "color": "rgba(160,0,200,0.3)", "label": "Puddle"},
                        ],
                    },
                    "explanation": "Move north between the puddles — G1 left, G2 right.",
                    "role_variants": _clock_spread(
                        {
                            ("TANK",   1): {"x": 0.35, "y": 0.18},
                            ("HEALER", 1): {"x": 0.42, "y": 0.18},
                            ("MELEE",  1): {"x": 0.30, "y": 0.12},
                            ("RANGED", 1): {"x": 0.38, "y": 0.24},
                            ("TANK",   2): {"x": 0.65, "y": 0.18},
                            ("HEALER", 2): {"x": 0.58, "y": 0.18},
                            ("MELEE",  2): {"x": 0.70, "y": 0.12},
                            ("RANGED", 2): {"x": 0.62, "y": 0.24},
                        },
                        safe_zones=[{"x": 0.20, "y": 0.02, "w": 0.60, "h": 0.32}],
                    ),
                },
            ],
        },
        {
            "slug": "visceral-burst",
            "name": "Visceral Burst",
            "phase_name": "Door Boss: Act 2",
            "description": (
                "Heavy single-target tankbuster. MT takes the first hit, "
                "OT provokes for the second."
            ),
            "difficulty_rating": 2,
            "tags": ["tankbuster"],
            "order": 5,
            "steps": [
                {
                    "order": 1,
                    "title": "MT Takes First — OT Swaps",
                    "narration": "T1 uses personal mits on the first hit. T2 provokes before the second.",
                    "timer_seconds": 4,
                    "action_type": "CHOICE",
                    "arena_state": {"boss_position": {"x": 0.5, "y": 0.5}},
                    "choices": [
                        {"id": "mt_takes", "label": "MT eats first hit, OT provokes"},
                        {"id": "invuln",   "label": "MT uses invuln and eats both"},
                        {"id": "nothing",  "label": "Do nothing"},
                    ],
                    "explanation": "Standard MT → OT swap keeps both tanks alive.",
                    "role_variants": _shared_choice("mt_takes"),
                },
            ],
        },
        {
            "slug": "grotesquerie-act2",
            "name": "Grotesquerie: Act 2 (Cruel Coil)",
            "phase_name": "Door Boss: Act 2",
            "description": (
                "Rotating cones around the boss. Start in the south safe "
                "sector and rotate clockwise with the pattern."
            ),
            "difficulty_rating": 4,
            "tags": ["rotation", "cone", "dodge"],
            "order": 6,
            "steps": [
                {
                    "order": 1,
                    "title": "Find Safe Sector — G1 West, G2 East",
                    "narration": "South is safe. G1 takes south-west side, G2 takes south-east side.",
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 0,   "spread": 60, "color": "rgba(255,80,80,0.3)", "label": "Coil"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 90,  "spread": 60, "color": "rgba(255,80,80,0.3)", "label": "Coil"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 270, "spread": 60, "color": "rgba(255,80,80,0.3)", "label": "Coil"},
                        ],
                    },
                    "explanation": "Split south sector into G1 (west half) and G2 (east half).",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.40, "y": 0.82},
                        ("HEALER", 1): {"x": 0.36, "y": 0.78},
                        ("MELEE",  1): {"x": 0.42, "y": 0.88},
                        ("RANGED", 1): {"x": 0.34, "y": 0.86},
                        ("TANK",   2): {"x": 0.60, "y": 0.82},
                        ("HEALER", 2): {"x": 0.64, "y": 0.78},
                        ("MELEE",  2): {"x": 0.58, "y": 0.88},
                        ("RANGED", 2): {"x": 0.66, "y": 0.86},
                    }),
                },
            ],
        },
        {
            "slug": "roiling-mass",
            "name": "Roiling Mass",
            "phase_name": "Door Boss: Act 2",
            "description": (
                "Four towers at intercardinals — two players per tower. "
                "Pairs: MT+H1 NW, M1+R1 NE, OT+H2 SW, M2+R2 SE."
            ),
            "difficulty_rating": 3,
            "tags": ["towers", "soak"],
            "order": 7,
            "steps": [
                {
                    "order": 1,
                    "title": "Soak Your Assigned Tower",
                    "narration": "NW=MT+H1, NE=M1+R1, SW=OT+H2, SE=M2+R2.",
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.25, "cy": 0.25, "r": 0.1, "color": "rgba(0,180,255,0.5)", "label": "MT+H1"},
                            {"shape": "circle", "cx": 0.75, "cy": 0.25, "r": 0.1, "color": "rgba(0,180,255,0.5)", "label": "M1+R1"},
                            {"shape": "circle", "cx": 0.25, "cy": 0.75, "r": 0.1, "color": "rgba(0,180,255,0.5)", "label": "OT+H2"},
                            {"shape": "circle", "cx": 0.75, "cy": 0.75, "r": 0.1, "color": "rgba(0,180,255,0.5)", "label": "M2+R2"},
                        ],
                    },
                    "explanation": "Two-player soak per tower — role+spot drives which tower.",
                    "role_variants": [
                        {"role": r, "spot": s, "correct_position": pos, "tolerance": 0.10}
                        for (r, s), pos in TOWERS_4.items()
                    ],
                },
            ],
        },
        {
            "slug": "grotesquerie-act3",
            "name": "Grotesquerie: Act 3",
            "phase_name": "Door Boss: Act 3",
            "description": "Platform spread — every player goes to their clock spot.",
            "difficulty_rating": 4,
            "tags": ["spread", "platform", "debuff"],
            "order": 8,
            "steps": [
                {
                    "order": 1,
                    "title": "Spread to Clock Platform",
                    "narration": "8-clock spread — same MT=N, H1=NE, M1=E, R1=SE convention.",
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "Platform Assignment", "color": "#ff6b35"},
                        ],
                    },
                    "explanation": "Same clock-spread assignment as Mortal Slayer.",
                    "role_variants": _clock_spread(CLOCK_8),
                },
            ],
        },
        {
            "slug": "split-scourge",
            "name": "Split Scourge",
            "phase_name": "Door Boss: Act 3",
            "description": "Centre line AoE — G1 goes west, G2 goes east.",
            "difficulty_rating": 3,
            "tags": ["line", "dodge"],
            "order": 9,
            "steps": [
                {
                    "order": 1,
                    "title": "Split East/West by Group",
                    "narration": "G1 (spot 1) all go west. G2 (spot 2) all go east.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "rect", "x": 0.3, "y": 0.0, "w": 0.4, "h": 1.0,
                             "color": "rgba(255,80,80,0.3)", "label": "Centre Line"},
                        ],
                    },
                    "explanation": "Clean left/right group split.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.12, "y": 0.40},
                        ("HEALER", 1): {"x": 0.10, "y": 0.55},
                        ("MELEE",  1): {"x": 0.18, "y": 0.50},
                        ("RANGED", 1): {"x": 0.14, "y": 0.65},
                        ("TANK",   2): {"x": 0.88, "y": 0.40},
                        ("HEALER", 2): {"x": 0.90, "y": 0.55},
                        ("MELEE",  2): {"x": 0.82, "y": 0.50},
                        ("RANGED", 2): {"x": 0.86, "y": 0.65},
                    }),
                },
            ],
        },
        {
            "slug": "curtain-call",
            "name": "Curtain Call",
            "phase_name": "Door Boss: Act 4",
            "description": "Cleanse zone in the centre — everyone steps in.",
            "difficulty_rating": 3,
            "tags": ["cleanse", "debuff"],
            "order": 10,
            "steps": [
                {
                    "order": 1,
                    "title": "Cleanse in the Centre",
                    "narration": "All 8 players step into the purification ring.",
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.5, "r": 0.15,
                             "color": "rgba(255,255,255,0.4)", "label": "Cleanse"},
                        ],
                        "debuffs": [
                            {"label": "Grotesquerie Debuff — Cleanse required", "color": "#cc44ff"},
                        ],
                    },
                    "explanation": "Stand in the white zone to cleanse, then step out.",
                    "role_variants": _shared_position({"x": 0.5, "y": 0.5}, tolerance=0.15),
                },
            ],
        },
        {
            "slug": "splattershed",
            "name": "Splattershed",
            "phase_name": "Door Boss: Act 4",
            "description": "Multi-hit raidwide. Stack all mitigation.",
            "difficulty_rating": 3,
            "tags": ["raidwide", "multi-hit"],
            "order": 11,
            "steps": [
                {
                    "order": 1,
                    "title": "Mitigate Multi-hit Raidwide",
                    "action_type": "CHOICE",
                    "arena_state": {"boss_position": {"x": 0.5, "y": 0.5}},
                    "choices": [
                        {"id": "mitigate", "label": "Deploy all mitigation"},
                        {"id": "nothing",  "label": "Do nothing"},
                    ],
                    "explanation": "Multiple hits. Use everything.",
                    "role_variants": _shared_choice("mitigate"),
                },
            ],
        },

        # ══════════════════════════════════════════════════════════════
        # Final Boss
        # ══════════════════════════════════════════════════════════════
        {
            "slug": "arcadia-aflame",
            "name": "Arcadia Aflame",
            "phase_name": "Final Boss: Phase 1",
            "description": "Transition raidwide into phase 2. Heavy damage.",
            "difficulty_rating": 2,
            "tags": ["raidwide", "transition"],
            "order": 12,
            "steps": [
                {
                    "order": 1,
                    "title": "Mitigate Transition Raidwide",
                    "action_type": "CHOICE",
                    "arena_state": {"boss_position": {"x": 0.5, "y": 0.5}},
                    "choices": [
                        {"id": "mitigate", "label": "Mitigate and shield"},
                        {"id": "nothing",  "label": "Do nothing"},
                    ],
                    "explanation": "Heavy transition damage. Deploy everything.",
                    "role_variants": _shared_choice("mitigate"),
                },
            ],
        },
        {
            "slug": "replication-1",
            "name": "Replication 1 (8 Clones)",
            "phase_name": "Final Boss: Phase 1",
            "description": "Three clones fire cones — south sector is safe.",
            "difficulty_rating": 4,
            "tags": ["clone", "cone", "dodge", "sequential"],
            "order": 13,
            "steps": [
                {
                    "order": 1,
                    "title": "Dodge Clone Cones — South Safe",
                    "narration": "Clones at N/W/E all fire inward. G1 takes south-west, G2 south-east.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "cone", "cx": 0.5, "cy": 0.1, "angle": 180, "spread": 60, "color": "rgba(255,80,80,0.3)", "label": "Clone N"},
                            {"shape": "cone", "cx": 0.1, "cy": 0.5, "angle": 0,   "spread": 60, "color": "rgba(255,80,80,0.3)", "label": "Clone W"},
                            {"shape": "cone", "cx": 0.9, "cy": 0.5, "angle": 180, "spread": 60, "color": "rgba(255,80,80,0.3)", "label": "Clone E"},
                        ],
                    },
                    "explanation": "South-centre is safe — split G1/G2 into the west/east halves.",
                    "role_variants": _clock_spread(
                        {
                            ("TANK",   1): {"x": 0.40, "y": 0.82},
                            ("HEALER", 1): {"x": 0.36, "y": 0.78},
                            ("MELEE",  1): {"x": 0.42, "y": 0.88},
                            ("RANGED", 1): {"x": 0.34, "y": 0.86},
                            ("TANK",   2): {"x": 0.60, "y": 0.82},
                            ("HEALER", 2): {"x": 0.64, "y": 0.78},
                            ("MELEE",  2): {"x": 0.58, "y": 0.88},
                            ("RANGED", 2): {"x": 0.66, "y": 0.86},
                        },
                        safe_zones=[{"shape": "circle", "cx": 0.5, "cy": 0.8, "r": 0.2}],
                    ),
                },
            ],
        },
        {
            "slug": "snaking-kick",
            "name": "Snaking Kick",
            "phase_name": "Final Boss: Phase 1",
            "description": "Frontal cleave — get behind the boss.",
            "difficulty_rating": 2,
            "tags": ["cleave", "dodge"],
            "order": 14,
            "steps": [
                {
                    "order": 1,
                    "title": "Get Behind Boss (Splits by Group)",
                    "narration": "Behind the boss — G1 left-behind, G2 right-behind for clean stacks.",
                    "timer_seconds": 4,
                    "action_type": "POSITION",
                    "default_tolerance": 0.25,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.4},
                        "boss_facing": "north",
                        "aoes": [
                            {"shape": "cone", "cx": 0.5, "cy": 0.4, "angle": 0, "spread": 120,
                             "color": "rgba(255,80,80,0.3)", "label": "Snaking Kick"},
                        ],
                    },
                    "explanation": "Stand behind the boss on your group's side.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.40, "y": 0.70},
                        ("HEALER", 1): {"x": 0.36, "y": 0.76},
                        ("MELEE",  1): {"x": 0.44, "y": 0.80},
                        ("RANGED", 1): {"x": 0.34, "y": 0.82},
                        ("TANK",   2): {"x": 0.60, "y": 0.70},
                        ("HEALER", 2): {"x": 0.64, "y": 0.76},
                        ("MELEE",  2): {"x": 0.56, "y": 0.80},
                        ("RANGED", 2): {"x": 0.66, "y": 0.82},
                    }),
                },
            ],
        },
        {
            "slug": "double-sobat",
            "name": "Double Sobat",
            "phase_name": "Final Boss: Phase 1",
            "description": "Shared tankbuster — tanks stack north, party stacks south.",
            "difficulty_rating": 2,
            "tags": ["tankbuster", "shared"],
            "order": 15,
            "steps": [
                {
                    "order": 1,
                    "title": "Tanks Stack North, Party Stack South",
                    "narration": "Both tanks share the hit north. Party stacks south and cleanses.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.15,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                    },
                    "explanation": "Tanks share north; rest stack south to share the splash.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.50, "y": 0.18},
                        ("TANK",   2): {"x": 0.50, "y": 0.22},
                        ("HEALER", 1): {"x": 0.48, "y": 0.78},
                        ("HEALER", 2): {"x": 0.52, "y": 0.78},
                        ("MELEE",  1): {"x": 0.46, "y": 0.82},
                        ("MELEE",  2): {"x": 0.54, "y": 0.82},
                        ("RANGED", 1): {"x": 0.44, "y": 0.80},
                        ("RANGED", 2): {"x": 0.56, "y": 0.80},
                    }),
                },
            ],
        },
        {
            "slug": "staging-replication-2",
            "name": "Staging + Replication 2",
            "phase_name": "Final Boss: Phase 2",
            "description": (
                "Clones mirror your movement. Each slot has a fixed staging "
                "corner — intercardinals by group."
            ),
            "difficulty_rating": 5,
            "tags": ["clone", "mirror", "positioning"],
            "order": 16,
            "steps": [
                {
                    "order": 1,
                    "title": "Staging Corner by Role + Spot",
                    "narration": "NW=MT+H1, NE=M1+R1, SW=OT+H2, SE=M2+R2 — mirror positions keep replays safe.",
                    "timer_seconds": 7,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "Clone Recording — Position carefully", "color": "#cc44ff"},
                        ],
                    },
                    "explanation": "Corner pairs match the Roiling Mass tower assignments.",
                    "role_variants": [
                        {"role": r, "spot": s, "correct_position": pos}
                        for (r, s), pos in TOWERS_4.items()
                    ],
                },
            ],
        },
        {
            "slug": "firefall-splash",
            "name": "Firefall Splash",
            "phase_name": "Final Boss: Phase 2",
            "description": "Sequential fire AoEs NW→NE→SW→SE. Start SE.",
            "difficulty_rating": 3,
            "tags": ["aoe", "sequential", "dodge"],
            "order": 17,
            "steps": [
                {
                    "order": 1,
                    "title": "Start SE — G1 South, G2 East",
                    "narration": "First fire drops NW. G1 stacks south edge, G2 stacks east edge.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.25, "cy": 0.25, "r": 0.2,
                             "color": "rgba(255,80,0,0.3)", "label": "Fire 1 (NW)"},
                        ],
                    },
                    "explanation": "Rotate counter-clockwise with the fire sequence.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.60, "y": 0.88},
                        ("HEALER", 1): {"x": 0.55, "y": 0.84},
                        ("MELEE",  1): {"x": 0.65, "y": 0.82},
                        ("RANGED", 1): {"x": 0.50, "y": 0.90},
                        ("TANK",   2): {"x": 0.88, "y": 0.60},
                        ("HEALER", 2): {"x": 0.84, "y": 0.55},
                        ("MELEE",  2): {"x": 0.82, "y": 0.65},
                        ("RANGED", 2): {"x": 0.90, "y": 0.50},
                    }),
                },
            ],
        },
        {
            "slug": "blood-mana",
            "name": "Blood Mana",
            "phase_name": "Final Boss: Phase 3",
            "description": (
                "Shape soak — Circle (1) takes T1, Triangle (3) takes H1/M1/R1. "
                "G2 handles the other shape pair."
            ),
            "difficulty_rating": 4,
            "tags": ["soak", "shapes"],
            "order": 18,
            "steps": [
                {
                    "order": 1,
                    "title": "Soak Your Shape",
                    "narration": "Spot 1 of each role owns the west shape; spot 2 owns the east.",
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.30, "cy": 0.50, "r": 0.08,
                             "color": "rgba(200,0,0,0.4)", "label": "G1 Shape"},
                            {"shape": "circle", "cx": 0.70, "cy": 0.50, "r": 0.15,
                             "color": "rgba(200,0,0,0.4)", "label": "G2 Shape (3)"},
                        ],
                    },
                    "explanation": "G1 covers the west (1-soak) shape, G2 covers the east (3-soak) shape.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.30, "y": 0.50},
                        ("HEALER", 1): {"x": 0.26, "y": 0.48},
                        ("MELEE",  1): {"x": 0.34, "y": 0.52},
                        ("RANGED", 1): {"x": 0.28, "y": 0.54},
                        ("TANK",   2): {"x": 0.70, "y": 0.50},
                        ("HEALER", 2): {"x": 0.74, "y": 0.48},
                        ("MELEE",  2): {"x": 0.66, "y": 0.52},
                        ("RANGED", 2): {"x": 0.72, "y": 0.54},
                    }),
                },
            ],
        },
        {
            "slug": "idyllic-dream",
            "name": "Idyllic Dream + Downfall",
            "phase_name": "Final Boss: Phase 3",
            "description": (
                "Dark towers (soak) on the west, wind towers (KB) on the east. "
                "Tanks and melees soak; healers and ranged brace."
            ),
            "difficulty_rating": 5,
            "tags": ["towers", "platform", "elemental", "soak"],
            "order": 19,
            "steps": [
                {
                    "order": 1,
                    "title": "Identify Your Tower Type",
                    "narration": "Tanks/Melee soak the Dark tower. Healers/Ranged brace for Wind.",
                    "timer_seconds": 6,
                    "action_type": "CHOICE",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.3, "cy": 0.5, "r": 0.08, "color": "rgba(80,0,160,0.5)", "label": "Dark"},
                            {"shape": "circle", "cx": 0.7, "cy": 0.5, "r": 0.08, "color": "rgba(0,200,100,0.5)", "label": "Wind"},
                        ],
                        "debuffs": [
                            {"label": "Dark Tower — Soak required", "color": "#6600cc"},
                            {"label": "Wind Tower — Knockback", "color": "#00cc66"},
                        ],
                    },
                    "choices": [
                        {"id": "soak",  "label": "Soak the Dark Tower"},
                        {"id": "avoid", "label": "Avoid / KB immunity"},
                    ],
                    "explanation": "Dark = soak (melee + tanks). Wind = KB immunity / brace (healers + ranged).",
                    "role_variants": [
                        {"role": "TANK",   "spot": 1, "correct_choice": "soak"},
                        {"role": "TANK",   "spot": 2, "correct_choice": "soak"},
                        {"role": "MELEE",  "spot": 1, "correct_choice": "soak"},
                        {"role": "MELEE",  "spot": 2, "correct_choice": "soak"},
                        {"role": "HEALER", "spot": 1, "correct_choice": "avoid"},
                        {"role": "HEALER", "spot": 2, "correct_choice": "avoid"},
                        {"role": "RANGED", "spot": 1, "correct_choice": "avoid"},
                        {"role": "RANGED", "spot": 2, "correct_choice": "avoid"},
                    ],
                },
                {
                    "order": 2,
                    "title": "Resolve Towers",
                    "narration": "Soakers inside the Dark tower. Braced players against the wind tower's wall side.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.3, "cy": 0.5, "r": 0.1, "color": "rgba(80,0,160,0.5)", "label": "Dark (Soak)"},
                            {"shape": "circle", "cx": 0.7, "cy": 0.5, "r": 0.1, "color": "rgba(0,200,100,0.4)", "label": "Wind (KB)"},
                        ],
                    },
                    "explanation": "Soakers in the Dark tower (pair per spot). KB players at far east wall.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.28, "y": 0.44},
                        ("TANK",   2): {"x": 0.32, "y": 0.56},
                        ("MELEE",  1): {"x": 0.26, "y": 0.50},
                        ("MELEE",  2): {"x": 0.34, "y": 0.50},
                        ("HEALER", 1): {"x": 0.92, "y": 0.40},
                        ("HEALER", 2): {"x": 0.92, "y": 0.60},
                        ("RANGED", 1): {"x": 0.88, "y": 0.45},
                        ("RANGED", 2): {"x": 0.88, "y": 0.55},
                    }),
                },
            ],
        },
        {
            "slug": "twisted-vision",
            "name": "Twisted Vision",
            "phase_name": "Final Boss: Phase 4",
            "description": "Memorised patterns replay. Spread to your clock spot each wave.",
            "difficulty_rating": 5,
            "tags": ["memory", "pattern", "sequential", "dodge"],
            "order": 20,
            "steps": [
                {
                    "order": 1,
                    "title": "Recall Pattern 1 — Cardinals",
                    "narration": "Cardinal cones replay. Intercardinal clock spots are safe.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 0,   "spread": 40, "color": "rgba(160,0,200,0.3)", "label": "Replay"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 90,  "spread": 40, "color": "rgba(160,0,200,0.3)", "label": "Replay"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 180, "spread": 40, "color": "rgba(160,0,200,0.3)", "label": "Replay"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 270, "spread": 40, "color": "rgba(160,0,200,0.3)", "label": "Replay"},
                        ],
                    },
                    "explanation": "Go to your intercardinal clock spot: H1=NE, R1=SE, H2=SW, R2=NW; tanks/melee pick an adjacent intercardinal.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.25, "y": 0.25},
                        ("HEALER", 1): {"x": 0.75, "y": 0.25},
                        ("MELEE",  1): {"x": 0.78, "y": 0.22},
                        ("RANGED", 1): {"x": 0.75, "y": 0.75},
                        ("TANK",   2): {"x": 0.25, "y": 0.75},
                        ("HEALER", 2): {"x": 0.25, "y": 0.75},
                        ("MELEE",  2): {"x": 0.22, "y": 0.78},
                        ("RANGED", 2): {"x": 0.25, "y": 0.25},
                    }),
                },
                {
                    "order": 2,
                    "title": "Recall Pattern 2 — Intercardinals",
                    "narration": "Intercardinal cones replay. Cardinal clock spots are safe.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 45,  "spread": 40, "color": "rgba(160,0,200,0.3)", "label": "Replay"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 135, "spread": 40, "color": "rgba(160,0,200,0.3)", "label": "Replay"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 225, "spread": 40, "color": "rgba(160,0,200,0.3)", "label": "Replay"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 315, "spread": 40, "color": "rgba(160,0,200,0.3)", "label": "Replay"},
                        ],
                    },
                    "explanation": "Same clock spots as Mortal Slayer — MT=N, OT=S, M1=E, M2=W; H/R pair onto the cardinals next to them.",
                    "role_variants": _clock_spread({
                        ("TANK",   1): {"x": 0.50, "y": 0.10},
                        ("HEALER", 1): {"x": 0.46, "y": 0.12},
                        ("MELEE",  1): {"x": 0.90, "y": 0.50},
                        ("RANGED", 1): {"x": 0.88, "y": 0.54},
                        ("TANK",   2): {"x": 0.50, "y": 0.90},
                        ("HEALER", 2): {"x": 0.54, "y": 0.88},
                        ("MELEE",  2): {"x": 0.10, "y": 0.50},
                        ("RANGED", 2): {"x": 0.12, "y": 0.46},
                    }),
                },
            ],
        },
    ],
}
