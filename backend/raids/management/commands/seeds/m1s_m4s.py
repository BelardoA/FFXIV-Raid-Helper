"""
Seed data for AAC Light-heavyweight (M1S–M4S).

Fights: Black Cat, Honey B. Lovely, Brute Bomber, Wicked Thunder.
"""

AAC_LHW_TIER = {
    "tier": {
        "slug": "aac-lhw",
        "name": "AAC Light-heavyweight",
        "expansion": "Dawntrail",
        "patch": "7.0",
        "order": 1,
    },
    "fights": [
        # ── M1S ──────────────────────────────────────────────────────
        {
            "slug": "m1s",
            "name": "AAC Light-heavyweight M1 (Savage)",
            "short_name": "M1S",
            "boss_name": "Black Cat",
            "difficulty": "SAVAGE",
            "arena_shape": "SQUARE",
            "order": 1,
            "mechanics": [
                {
                    "slug": "leaping-one-two-paw",
                    "name": "Leaping One-two Paw",
                    "phase_name": "Phase 1",
                    "description": (
                        "Boss leaps to a cardinal then cleaves both sides "
                        "sequentially. Identify the safe side from the claw telegraph."
                    ),
                    "difficulty_rating": 2,
                    "tags": ["cleave", "dodge"],
                    "order": 1,
                    "steps": [
                        {
                            "order": 1,
                            "title": "Identify the Leap Direction",
                            "narration": (
                                "Black Cat leaps north. Watch which paw she raises — "
                                "it telegraphs the FIRST cleave side."
                            ),
                            "timer_seconds": 5,
                            "action_type": "POSITION",
                            "arena_state": {
                                "boss_position": {"x": 0.5, "y": 0.1},
                                "boss_facing": "south",
                                "aoes": [
                                    {
                                        "shape": "rect",
                                        "x": 0.0, "y": 0.0,
                                        "w": 0.5, "h": 1.0,
                                        "color": "rgba(255,80,80,0.35)",
                                        "label": "First Cleave (Left)",
                                    }
                                ],
                            },
                            "explanation": (
                                "Step right to avoid the first (left-side) cleave. "
                                "Be ready to immediately move left for the follow-up."
                            ),
                            "role_variants": [
                                {"role": "TANK",   "correct_position": {"x": 0.75, "y": 0.5},  "safe_zones": [{"x": 0.5, "y": 0.0, "w": 0.5, "h": 1.0}]},
                                {"role": "HEALER", "correct_position": {"x": 0.75, "y": 0.7},  "safe_zones": [{"x": 0.5, "y": 0.0, "w": 0.5, "h": 1.0}]},
                                {"role": "MELEE",  "correct_position": {"x": 0.75, "y": 0.5},  "safe_zones": [{"x": 0.5, "y": 0.0, "w": 0.5, "h": 1.0}]},
                                {"role": "RANGED", "correct_position": {"x": 0.8,  "y": 0.5},  "safe_zones": [{"x": 0.5, "y": 0.0, "w": 0.5, "h": 1.0}]},
                            ],
                        },
                        {
                            "order": 2,
                            "title": "Second Cleave — Swap Sides",
                            "narration": "The second cleave hits the opposite side. Move through the boss to safety.",
                            "timer_seconds": 4,
                            "action_type": "POSITION",
                            "arena_state": {
                                "boss_position": {"x": 0.5, "y": 0.1},
                                "boss_facing": "south",
                                "aoes": [
                                    {
                                        "shape": "rect",
                                        "x": 0.5, "y": 0.0,
                                        "w": 0.5, "h": 1.0,
                                        "color": "rgba(255,80,80,0.35)",
                                        "label": "Second Cleave (Right)",
                                    }
                                ],
                            },
                            "explanation": "Cross through the boss to the left side before the second cleave lands.",
                            "role_variants": [
                                {"role": "TANK",   "correct_position": {"x": 0.25, "y": 0.5},  "safe_zones": [{"x": 0.0, "y": 0.0, "w": 0.5, "h": 1.0}]},
                                {"role": "HEALER", "correct_position": {"x": 0.25, "y": 0.7},  "safe_zones": [{"x": 0.0, "y": 0.0, "w": 0.5, "h": 1.0}]},
                                {"role": "MELEE",  "correct_position": {"x": 0.25, "y": 0.5},  "safe_zones": [{"x": 0.0, "y": 0.0, "w": 0.5, "h": 1.0}]},
                                {"role": "RANGED", "correct_position": {"x": 0.2,  "y": 0.5},  "safe_zones": [{"x": 0.0, "y": 0.0, "w": 0.5, "h": 1.0}]},
                            ],
                        },
                    ],
                },
                {
                    "slug": "nailchipper-spread",
                    "name": "Nailchipper (Spread)",
                    "phase_name": "Phase 1",
                    "description": "Eight individual AoEs — spread to designated spots.",
                    "difficulty_rating": 2,
                    "tags": ["spread", "aoe"],
                    "order": 2,
                    "steps": [
                        {
                            "order": 1,
                            "title": "Spread to Assigned Positions",
                            "narration": (
                                "Nailchipper fires an AoE at every player. "
                                "Standard 8-way spread: Tanks N/S, Healers NE/SW, "
                                "Melee NW/SE, Ranged/Casters E/W."
                            ),
                            "timer_seconds": 6,
                            "action_type": "POSITION",
                            "arena_state": {
                                "boss_position": {"x": 0.5, "y": 0.5},
                                "aoes": [
                                    {"shape": "circle", "cx": 0.5, "cy": 0.5, "r": 0.08,
                                     "color": "rgba(255,200,0,0.5)", "label": "AoE (each player)"},
                                ],
                                "markers": [
                                    {"id": "A", "x": 0.5,  "y": 0.05},
                                    {"id": "B", "x": 0.95, "y": 0.5},
                                    {"id": "C", "x": 0.5,  "y": 0.95},
                                    {"id": "D", "x": 0.05, "y": 0.5},
                                ],
                            },
                            "explanation": "Spread far apart using standard 8-way positions.",
                            "role_variants": [
                                {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.15}},
                                {"role": "HEALER", "correct_position": {"x": 0.15, "y": 0.85}},
                                {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.15}},
                                {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.5}},
                            ],
                        },
                    ],
                },
                {
                    "slug": "mouser-limit-cut",
                    "name": "Mouser (Limit Cut)",
                    "phase_name": "Phase 1",
                    "description": "Numbered limit-cut AoEs. Players resolve in order 1→4.",
                    "difficulty_rating": 4,
                    "tags": ["limit-cut", "spread", "numbered"],
                    "order": 3,
                    "steps": [
                        {
                            "order": 1,
                            "title": "Check Your Number — Odds North",
                            "narration": "Numbers 1 & 3 go North. Numbers 2 & 4 go South.",
                            "timer_seconds": 5,
                            "action_type": "CHOICE",
                            "arena_state": {
                                "boss_position": {"x": 0.5, "y": 0.5},
                                "debuffs": [
                                    {"label": "#1 — Odd", "color": "#fff"},
                                    {"label": "#2 — Even", "color": "#fff"},
                                ],
                            },
                            "choices": [
                                {"id": "north", "label": "Go North (Odd)"},
                                {"id": "south", "label": "Go South (Even)"},
                            ],
                            "explanation": "Odd numbers (1,3) stack North. Even numbers (2,4) stack South.",
                            "role_variants": [
                                {"role": "TANK",   "correct_choice": "north"},
                                {"role": "HEALER", "correct_choice": "north"},
                                {"role": "MELEE",  "correct_choice": "south"},
                                {"role": "RANGED", "correct_choice": "south"},
                            ],
                        },
                    ],
                },
            ],
        },
        # ── M2S ──────────────────────────────────────────────────────
        {
            "slug": "m2s",
            "name": "AAC Light-heavyweight M2 (Savage)",
            "short_name": "M2S",
            "boss_name": "Honey B. Lovely",
            "difficulty": "SAVAGE",
            "arena_shape": "CIRCLE",
            "order": 2,
            "mechanics": [
                {
                    "slug": "honey-b-bombing",
                    "name": "Honey B. Bombing",
                    "phase_name": "Phase 1",
                    "description": "Pink AoE circles in a checkerboard. Find the safe spots.",
                    "difficulty_rating": 3,
                    "tags": ["aoe", "dodge", "pattern"],
                    "order": 1,
                    "steps": [
                        {
                            "order": 1,
                            "title": "Identify Safe Columns",
                            "narration": "Pink circles fill most of the arena. Stand in the centre cross.",
                            "timer_seconds": 6,
                            "action_type": "POSITION",
                            "arena_state": {
                                "boss_position": {"x": 0.5, "y": 0.5},
                                "aoes": [
                                    {"shape": "circle", "cx": 0.25, "cy": 0.25, "r": 0.18, "color": "rgba(255,100,180,0.5)"},
                                    {"shape": "circle", "cx": 0.75, "cy": 0.25, "r": 0.18, "color": "rgba(255,100,180,0.5)"},
                                    {"shape": "circle", "cx": 0.25, "cy": 0.75, "r": 0.18, "color": "rgba(255,100,180,0.5)"},
                                    {"shape": "circle", "cx": 0.75, "cy": 0.75, "r": 0.18, "color": "rgba(255,100,180,0.5)"},
                                ],
                            },
                            "explanation": "The centre cross is always safe in this pattern.",
                            "role_variants": [
                                {"role": "TANK",   "correct_position": {"x": 0.5, "y": 0.5}, "tolerance": 0.15},
                                {"role": "HEALER", "correct_position": {"x": 0.5, "y": 0.5}, "tolerance": 0.15},
                                {"role": "MELEE",  "correct_position": {"x": 0.5, "y": 0.5}, "tolerance": 0.15},
                                {"role": "RANGED", "correct_position": {"x": 0.5, "y": 0.5}, "tolerance": 0.15},
                            ],
                        },
                    ],
                },
                {
                    "slug": "alarm-pheromones",
                    "name": "Alarm Pheromones (Stack/Spread)",
                    "phase_name": "Phase 1",
                    "description": "Heart = stack, Bee = spread. React to your debuff.",
                    "difficulty_rating": 3,
                    "tags": ["spread", "stack", "debuff"],
                    "order": 2,
                    "steps": [
                        {
                            "order": 1,
                            "title": "React to Your Debuff",
                            "narration": "Heart = stack with partner. Bee = spread far apart.",
                            "timer_seconds": 5,
                            "action_type": "POSITION",
                            "arena_state": {
                                "boss_position": {"x": 0.5, "y": 0.5},
                                "debuffs": [
                                    {"label": "♥ Stack", "color": "#ff69b4"},
                                    {"label": "🐝 Spread", "color": "#ffd700"},
                                ],
                            },
                            "explanation": "Heart players stack North/South. Bee players spread East/West.",
                            "role_variants": [
                                {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.2}},
                                {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.2}},
                                {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.5}},
                                {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.5}},
                            ],
                        },
                    ],
                },
            ],
        },
        # ── M3S ──────────────────────────────────────────────────────
        {
            "slug": "m3s",
            "name": "AAC Light-heavyweight M3 (Savage)",
            "short_name": "M3S",
            "boss_name": "Brute Bomber",
            "difficulty": "SAVAGE",
            "arena_shape": "SQUARE",
            "order": 3,
            "mechanics": [
                {
                    "slug": "brutal-impact-towers",
                    "name": "Brutal Impact (Towers)",
                    "phase_name": "Phase 1",
                    "description": "Four towers spawn. Each must be soaked by a pair of players.",
                    "difficulty_rating": 3,
                    "tags": ["towers", "soak"],
                    "order": 1,
                    "steps": [
                        {
                            "order": 1,
                            "title": "Identify Your Tower",
                            "narration": "Towers at NE/NW/SE/SW. Pair up: MT+H1 NE, M1+M2 SE, R1+C1 SW.",
                            "timer_seconds": 8,
                            "action_type": "POSITION",
                            "arena_state": {
                                "boss_position": {"x": 0.5, "y": 0.5},
                                "aoes": [
                                    {"shape": "circle", "cx": 0.75, "cy": 0.25, "r": 0.1, "color": "rgba(0,180,255,0.5)", "label": "Tower NE"},
                                    {"shape": "circle", "cx": 0.25, "cy": 0.25, "r": 0.1, "color": "rgba(0,180,255,0.5)", "label": "Tower NW"},
                                    {"shape": "circle", "cx": 0.75, "cy": 0.75, "r": 0.1, "color": "rgba(0,180,255,0.5)", "label": "Tower SE"},
                                    {"shape": "circle", "cx": 0.25, "cy": 0.75, "r": 0.1, "color": "rgba(0,180,255,0.5)", "label": "Tower SW"},
                                ],
                            },
                            "explanation": "Each pair soaks their assigned tower.",
                            "role_variants": [
                                {"role": "TANK",   "correct_position": {"x": 0.75, "y": 0.25}},
                                {"role": "HEALER", "correct_position": {"x": 0.75, "y": 0.25}},
                                {"role": "MELEE",  "correct_position": {"x": 0.75, "y": 0.75}},
                                {"role": "RANGED", "correct_position": {"x": 0.25, "y": 0.75}},
                            ],
                        },
                    ],
                },
            ],
        },
        # ── M4S ──────────────────────────────────────────────────────
        {
            "slug": "m4s",
            "name": "AAC Light-heavyweight M4 (Savage)",
            "short_name": "M4S",
            "boss_name": "Wicked Thunder",
            "difficulty": "SAVAGE",
            "arena_shape": "SQUARE",
            "order": 4,
            "mechanics": [
                {
                    "slug": "witch-hunt",
                    "name": "Witch Hunt",
                    "phase_name": "Phase 1",
                    "description": "Odd/even debuffs rotate. Spread to correct intercardinals, then rotate 90°.",
                    "difficulty_rating": 5,
                    "tags": ["debuff", "rotation", "spread"],
                    "order": 1,
                    "steps": [
                        {
                            "order": 1,
                            "title": "Identify Debuff Parity",
                            "narration": "Odd numbers go left intercardinals, even go right.",
                            "timer_seconds": 8,
                            "action_type": "POSITION",
                            "arena_state": {
                                "boss_position": {"x": 0.5, "y": 0.5},
                                "debuffs": [
                                    {"label": "Thunder #1 (Odd)", "color": "#a0e0ff"},
                                    {"label": "Thunder #2 (Even)", "color": "#ffd080"},
                                ],
                                "markers": [
                                    {"id": "A", "x": 0.5,  "y": 0.05},
                                    {"id": "B", "x": 0.95, "y": 0.5},
                                    {"id": "C", "x": 0.5,  "y": 0.95},
                                    {"id": "D", "x": 0.05, "y": 0.5},
                                ],
                            },
                            "explanation": "Odd spreads NW/SW, Even spreads NE/SE.",
                            "role_variants": [
                                {"role": "TANK",   "correct_position": {"x": 0.15, "y": 0.15}},
                                {"role": "HEALER", "correct_position": {"x": 0.85, "y": 0.85}},
                                {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.85}},
                                {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.15}},
                            ],
                        },
                        {
                            "order": 2,
                            "title": "Rotate for Second Hit",
                            "narration": "Pattern rotates 90° clockwise. Move to next safe intercardinal.",
                            "timer_seconds": 5,
                            "action_type": "POSITION",
                            "arena_state": {
                                "boss_position": {"x": 0.5, "y": 0.5},
                                "aoes": [
                                    {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 315, "spread": 90,
                                     "color": "rgba(160,100,255,0.4)", "label": "Cleave"},
                                    {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 135, "spread": 90,
                                     "color": "rgba(160,100,255,0.4)", "label": "Cleave"},
                                ],
                            },
                            "explanation": "Rotate 90° clockwise from your starting intercardinal.",
                            "role_variants": [
                                {"role": "TANK",   "correct_position": {"x": 0.85, "y": 0.15}},
                                {"role": "HEALER", "correct_position": {"x": 0.15, "y": 0.85}},
                                {"role": "MELEE",  "correct_position": {"x": 0.85, "y": 0.85}},
                                {"role": "RANGED", "correct_position": {"x": 0.15, "y": 0.15}},
                            ],
                        },
                    ],
                },
            ],
        },
    ],
}
