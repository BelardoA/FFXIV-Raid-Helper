"""
Seed data for M9S — Vamp Fatale (AAC Heavyweight M1 Savage).

Complete fight walkthrough: every mechanic from pull to enrage.
Phase 1: Killer Voice → Hardcore → Vamp Stomp → Sadistic Screech →
         Coffinfiller → Dead Wake → Half Moon → Brutal Rain + Flaying Fry →
         Crowd Kill
Phase 2: Finale Fatale → Aetherletting → Buzzsaws + Adds
Phase 3: Hell in a Cell → Ultrasonic Amp/Spread → Sanguine Scratch →
         Undead Deathmatch
"""

M9S_FIGHT = {
    "slug": "m9s",
    "name": "AAC Heavyweight M1 (Savage)",
    "short_name": "M9S",
    "boss_name": "Vamp Fatale",
    "difficulty": "SAVAGE",
    "arena_shape": "SQUARE",
    "order": 1,
    "mechanics": [
        # ── Phase 1 ──────────────────────────────────────────────────
        {
            "slug": "killer-voice",
            "name": "Killer Voice",
            "phase_name": "Phase 1",
            "description": (
                "Heavy raidwide damage. Mitigate and heal through it. "
                "This is Vamp Fatale's signature raidwide."
            ),
            "difficulty_rating": 1,
            "tags": ["raidwide"],
            "order": 1,
            "steps": [
                {
                    "order": 1,
                    "title": "Mitigate the Raidwide",
                    "action_type": "CHOICE",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                    },
                    "choices": [
                        {"id": "mitigate", "label": "Use mitigation/shields"},
                        {"id": "nothing", "label": "Do nothing"},
                    ],
                    "explanation": "Always mitigate raidwides. Healers shield, tanks use party mit.",
                    "role_variants": [
                        {"role": "TANK",   "correct_choice": "mitigate"},
                        {"role": "HEALER", "correct_choice": "mitigate"},
                        {"role": "MELEE",  "correct_choice": "mitigate"},
                        {"role": "RANGED", "correct_choice": "mitigate"},
                        {"role": "CASTER", "correct_choice": "mitigate"},
                    ],
                },
            ],
        },
        {
            "slug": "hardcore",
            "name": "Hardcore",
            "phase_name": "Phase 1",
            "description": (
                "Dual tankbuster. Both tanks must split the damage or use "
                "invulnerability. Non-tanks stay away."
            ),
            "difficulty_rating": 2,
            "tags": ["tankbuster"],
            "order": 2,
            "steps": [
                {
                    "order": 1,
                    "title": "Resolve Tankbuster",
                    "narration": (
                        "Hardcore targets both tanks. Stack together to share, "
                        "or use invulns. Party stays away."
                    ),
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "boss_facing": "south",
                    },
                    "explanation": (
                        "Tanks stack north of boss. Everyone else stays south to "
                        "avoid the cleave."
                    ),
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.3}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.75}},
                        {"role": "MELEE",  "correct_position": {"x": 0.5,  "y": 0.7}},
                        {"role": "RANGED", "correct_position": {"x": 0.5,  "y": 0.8}},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.8}},
                    ],
                },
            ],
        },
        {
            "slug": "vamp-stomp",
            "name": "Vamp Stomp + Bat Adds",
            "phase_name": "Phase 1",
            "description": (
                "Vamp Fatale slams the ground, spawning bat adds at clock spots. "
                "Players spread to assigned clock positions to handle them."
            ),
            "difficulty_rating": 2,
            "tags": ["spread", "adds", "clock"],
            "order": 3,
            "steps": [
                {
                    "order": 1,
                    "title": "Spread to Clock Positions",
                    "narration": (
                        "Bat adds spawn at 8 positions around the arena. "
                        "Spread to your assigned clock spot."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "markers": [
                            {"id": "A", "x": 0.5,  "y": 0.05},
                            {"id": "B", "x": 0.95, "y": 0.5},
                            {"id": "C", "x": 0.5,  "y": 0.95},
                            {"id": "D", "x": 0.05, "y": 0.5},
                        ],
                    },
                    "explanation": "Standard clock spread. Each player handles their bat add.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.1}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.9}},
                        {"role": "MELEE",  "correct_position": {"x": 0.1,  "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.9,  "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.85, "y": 0.15}},
                    ],
                },
            ],
        },
        {
            "slug": "sadistic-screech",
            "name": "Sadistic Screech",
            "phase_name": "Phase 1",
            "description": (
                "Point-blank AoE centred on the boss. Get out to the edge of "
                "the arena to avoid it."
            ),
            "difficulty_rating": 1,
            "tags": ["aoe", "dodge"],
            "order": 4,
            "steps": [
                {
                    "order": 1,
                    "title": "Move Away from Boss",
                    "narration": "Large point-blank AoE. Get to the edge.",
                    "timer_seconds": 4,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.5, "r": 0.35,
                             "color": "rgba(255,80,80,0.3)", "label": "Sadistic Screech"},
                        ],
                    },
                    "explanation": "Stay outside the large circle. Max melee range or further.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.1}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.9}},
                        {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.9,  "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.9,  "y": 0.9}},
                    ],
                },
            ],
        },
        {
            "slug": "coffinfiller",
            "name": "Coffinfiller + Dead Wake",
            "phase_name": "Phase 1",
            "description": (
                "Line AoEs fire across the arena in sequence. Identify the "
                "safe lanes and dodge between them."
            ),
            "difficulty_rating": 3,
            "tags": ["line", "dodge", "sequential"],
            "order": 5,
            "steps": [
                {
                    "order": 1,
                    "title": "Dodge the Line AoEs",
                    "narration": (
                        "Lines fire from the west wall in sequence. "
                        "Stand in the gap between the first and second line."
                    ),
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "rect", "x": 0.0, "y": 0.0,  "w": 1.0, "h": 0.2,
                             "color": "rgba(255,80,80,0.3)", "label": "Line 1"},
                            {"shape": "rect", "x": 0.0, "y": 0.4,  "w": 1.0, "h": 0.2,
                             "color": "rgba(255,80,80,0.3)", "label": "Line 2"},
                            {"shape": "rect", "x": 0.0, "y": 0.8,  "w": 1.0, "h": 0.2,
                             "color": "rgba(255,80,80,0.3)", "label": "Line 3"},
                        ],
                    },
                    "explanation": "Stand in the gaps between the lines. Safe rows are roughly y=0.3 and y=0.7.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.3}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.7}},
                        {"role": "MELEE",  "correct_position": {"x": 0.4,  "y": 0.3}},
                        {"role": "RANGED", "correct_position": {"x": 0.6,  "y": 0.7}},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.7}},
                    ],
                },
                {
                    "order": 2,
                    "title": "Dead Wake — Dodge the Follow-up",
                    "narration": (
                        "Dead Wake fires a cross-shaped AoE through the centre. "
                        "Move to an intercardinal corner."
                    ),
                    "timer_seconds": 4,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "rect", "x": 0.4, "y": 0.0, "w": 0.2, "h": 1.0,
                             "color": "rgba(255,80,80,0.35)", "label": "Dead Wake (Vertical)"},
                            {"shape": "rect", "x": 0.0, "y": 0.4, "w": 1.0, "h": 0.2,
                             "color": "rgba(255,80,80,0.35)", "label": "Dead Wake (Horizontal)"},
                        ],
                    },
                    "explanation": "Intercardinal corners are safe from the cross AoE.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.15, "y": 0.15}},
                        {"role": "HEALER", "correct_position": {"x": 0.85, "y": 0.85}},
                        {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.85}},
                        {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.15}},
                        {"role": "CASTER", "correct_position": {"x": 0.85, "y": 0.85}},
                    ],
                },
            ],
        },
        {
            "slug": "half-moon",
            "name": "Half Moon",
            "phase_name": "Phase 1",
            "description": (
                "Vamp Fatale cleaves one half of the arena. "
                "Identify the telegraph and move to the safe half."
            ),
            "difficulty_rating": 2,
            "tags": ["cleave", "dodge"],
            "order": 6,
            "steps": [
                {
                    "order": 1,
                    "title": "Dodge the Half Moon Cleave",
                    "narration": (
                        "Vamp Fatale raises her left arm — the left half "
                        "of the arena will be cleaved. Move to the right (east) side."
                    ),
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.25,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "boss_facing": "south",
                        "aoes": [
                            {
                                "shape": "rect",
                                "x": 0.0, "y": 0.0,
                                "w": 0.5, "h": 1.0,
                                "color": "rgba(255,80,80,0.3)",
                                "label": "Half Moon (Left)",
                            },
                        ],
                    },
                    "explanation": (
                        "Stand in the east (right) half to avoid the cleave. "
                        "Melee stay close to the boss for uptime."
                    ),
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.65, "y": 0.4},  "safe_zones": [{"x": 0.5, "y": 0.0, "w": 0.5, "h": 1.0}]},
                        {"role": "HEALER", "correct_position": {"x": 0.75, "y": 0.65}, "safe_zones": [{"x": 0.5, "y": 0.0, "w": 0.5, "h": 1.0}]},
                        {"role": "MELEE",  "correct_position": {"x": 0.6,  "y": 0.5},  "safe_zones": [{"x": 0.5, "y": 0.0, "w": 0.5, "h": 1.0}]},
                        {"role": "RANGED", "correct_position": {"x": 0.8,  "y": 0.7},  "safe_zones": [{"x": 0.5, "y": 0.0, "w": 0.5, "h": 1.0}]},
                        {"role": "CASTER", "correct_position": {"x": 0.75, "y": 0.75}, "safe_zones": [{"x": 0.5, "y": 0.0, "w": 0.5, "h": 1.0}]},
                    ],
                },
            ],
        },
        {
            "slug": "brutal-rain-flaying-fry",
            "name": "Brutal Rain + Flaying Fry",
            "phase_name": "Phase 1",
            "description": (
                "Stack marker (Brutal Rain) on one group, spread markers "
                "(Flaying Fry) on the other. Resolve simultaneously."
            ),
            "difficulty_rating": 3,
            "tags": ["stack", "spread"],
            "order": 7,
            "steps": [
                {
                    "order": 1,
                    "title": "Stack or Spread Based on Debuff",
                    "narration": (
                        "Support roles get stack markers — group north. "
                        "DPS get spread markers — fan out south."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "Brutal Rain — Stack", "color": "#2b7fff"},
                            {"label": "Flaying Fry — Spread", "color": "#ff6b35"},
                        ],
                    },
                    "explanation": (
                        "Supports stack north of boss for Brutal Rain. "
                        "DPS spread to south intercardinals for Flaying Fry."
                    ),
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.25}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.25}},
                        {"role": "MELEE",  "correct_position": {"x": 0.25, "y": 0.8}},
                        {"role": "RANGED", "correct_position": {"x": 0.75, "y": 0.8}},
                        {"role": "CASTER", "correct_position": {"x": 0.85, "y": 0.7}},
                    ],
                },
            ],
        },
        {
            "slug": "penetrating-pitch",
            "name": "Penetrating Pitch",
            "phase_name": "Phase 1",
            "description": (
                "Baited AoEs drop under each player. Keep moving to avoid "
                "standing in your own puddle."
            ),
            "difficulty_rating": 2,
            "tags": ["bait", "puddle"],
            "order": 8,
            "steps": [
                {
                    "order": 1,
                    "title": "Bait and Dodge Puddles",
                    "narration": (
                        "AoEs drop under every player. Bait them in a line, "
                        "then move to clean ground."
                    ),
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.5, "r": 0.08,
                             "color": "rgba(160,0,200,0.3)", "label": "Bait puddle"},
                        ],
                    },
                    "explanation": "Bait puddles along your assigned edge, then dodge inward.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.1}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.9}},
                        {"role": "MELEE",  "correct_position": {"x": 0.1,  "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.9,  "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.9,  "y": 0.9}},
                    ],
                },
            ],
        },
        {
            "slug": "crowd-kill",
            "name": "Crowd Kill",
            "phase_name": "Phase 1",
            "description": (
                "Heavy raidwide + knockback from centre. Pre-position to avoid "
                "being knocked into the wall."
            ),
            "difficulty_rating": 2,
            "tags": ["raidwide", "knockback"],
            "order": 9,
            "steps": [
                {
                    "order": 1,
                    "title": "Position for Knockback",
                    "narration": (
                        "Knockback from centre. Stand near centre so you don't "
                        "fly into the death wall."
                    ),
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.5, "r": 0.1,
                             "color": "rgba(255,255,0,0.3)", "label": "Knockback Origin"},
                        ],
                    },
                    "explanation": (
                        "Stand close to centre. Use Arm's Length / Surecast to negate "
                        "the knockback, or position just off-centre toward your assigned side."
                    ),
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.4}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.6}},
                        {"role": "MELEE",  "correct_position": {"x": 0.4,  "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.6,  "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.55, "y": 0.55}},
                    ],
                },
            ],
        },

        # ── Phase 2 ──────────────────────────────────────────────────
        {
            "slug": "finale-fatale",
            "name": "Finale Fatale",
            "phase_name": "Phase 2",
            "description": (
                "Transition raidwide. Vamp Fatale transforms the arena. "
                "Mitigate and heal through the heavy damage."
            ),
            "difficulty_rating": 2,
            "tags": ["raidwide", "transition"],
            "order": 10,
            "steps": [
                {
                    "order": 1,
                    "title": "Mitigate the Transition",
                    "action_type": "CHOICE",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                    },
                    "choices": [
                        {"id": "mitigate", "label": "Use mitigation/shields"},
                        {"id": "nothing",  "label": "Do nothing"},
                    ],
                    "explanation": "Heavy transition damage. Deploy all available mitigation.",
                    "role_variants": [
                        {"role": "TANK",   "correct_choice": "mitigate"},
                        {"role": "HEALER", "correct_choice": "mitigate"},
                        {"role": "MELEE",  "correct_choice": "mitigate"},
                        {"role": "RANGED", "correct_choice": "mitigate"},
                        {"role": "CASTER", "correct_choice": "mitigate"},
                    ],
                },
            ],
        },
        {
            "slug": "aetherletting",
            "name": "Aetherletting",
            "phase_name": "Phase 2",
            "description": (
                "Vamp Fatale fires four conal AoEs at intercardinals, then "
                "role-based markers drop on players. Dodge the cones first, "
                "then resolve your role marker."
            ),
            "difficulty_rating": 3,
            "tags": ["cone", "dodge", "spread", "stack"],
            "order": 11,
            "steps": [
                {
                    "order": 1,
                    "title": "Dodge the Conal AoEs",
                    "narration": (
                        "Four cone AoEs fire at intercardinals. "
                        "Stand at a cardinal position to avoid them."
                    ),
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 45,  "spread": 40, "color": "rgba(180,60,60,0.35)", "label": "Cone NE"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 135, "spread": 40, "color": "rgba(180,60,60,0.35)", "label": "Cone SE"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 225, "spread": 40, "color": "rgba(180,60,60,0.35)", "label": "Cone SW"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 315, "spread": 40, "color": "rgba(180,60,60,0.35)", "label": "Cone NW"},
                        ],
                    },
                    "explanation": "Cardinals are safe. Stand at N, E, S, or W to dodge all four cones.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.15}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.85}},
                        {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.85, "y": 0.5}},
                    ],
                },
                {
                    "order": 2,
                    "title": "Resolve Role Markers",
                    "narration": (
                        "DPS receive spread markers — fan out to intercardinals. "
                        "Supports receive stack markers — pair up at cardinals."
                    ),
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "DPS — Spread", "color": "#ff6b35"},
                            {"label": "Support — Stack", "color": "#2b7fff"},
                        ],
                        "markers": [
                            {"id": "A", "x": 0.5,  "y": 0.05},
                            {"id": "B", "x": 0.95, "y": 0.5},
                            {"id": "C", "x": 0.5,  "y": 0.95},
                            {"id": "D", "x": 0.05, "y": 0.5},
                        ],
                    },
                    "explanation": (
                        "DPS spread to intercardinals. "
                        "Tank+Healer stack at north cardinal."
                    ),
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.1}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.1}},
                        {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.15}},
                        {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.85}},
                        {"role": "CASTER", "correct_position": {"x": 0.85, "y": 0.15}},
                    ],
                },
            ],
        },
        {
            "slug": "insatiable-thirst",
            "name": "Insatiable Thirst + Buzzsaws",
            "phase_name": "Phase 2",
            "description": (
                "Vamp Fatale summons buzzsaws on the arena edges and adds "
                "that must be killed. Dodge the saws while handling adds."
            ),
            "difficulty_rating": 3,
            "tags": ["adds", "dodge", "dps-check"],
            "order": 12,
            "steps": [
                {
                    "order": 1,
                    "title": "Position for Adds + Dodge Saws",
                    "narration": (
                        "Buzzsaws orbit the arena edges. Stack mid to group adds, "
                        "then dodge outward when saws pass."
                    ),
                    "timer_seconds": 7,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "rect", "x": 0.0, "y": 0.0, "w": 0.1, "h": 1.0,
                             "color": "rgba(255,200,0,0.4)", "label": "Buzzsaw W"},
                            {"shape": "rect", "x": 0.9, "y": 0.0, "w": 0.1, "h": 1.0,
                             "color": "rgba(255,200,0,0.4)", "label": "Buzzsaw E"},
                        ],
                    },
                    "explanation": (
                        "Stay in the centre to avoid saws. Group adds together "
                        "for AoE damage."
                    ),
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.4}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.6}},
                        {"role": "MELEE",  "correct_position": {"x": 0.45, "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.55, "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.55}},
                    ],
                },
            ],
        },

        # ── Phase 3 ──────────────────────────────────────────────────
        {
            "slug": "hell-in-a-cell",
            "name": "Hell in a Cell",
            "phase_name": "Phase 3",
            "description": (
                "Four towers spawn that must be soaked. Soaking a tower damages "
                "the bat adds. Players must also handle Ultrasonic Amp (stack) "
                "or Ultrasonic Spread."
            ),
            "difficulty_rating": 4,
            "tags": ["towers", "soak", "stack", "spread"],
            "order": 13,
            "steps": [
                {
                    "order": 1,
                    "title": "Soak Assigned Tower",
                    "narration": (
                        "Four towers appear at intercardinals. "
                        "Each pair soaks one tower. Tanks/Melee north pair, "
                        "Healers/Ranged south pair."
                    ),
                    "timer_seconds": 7,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.8,  "cy": 0.2,  "r": 0.09, "color": "rgba(0,180,255,0.5)", "label": "Tower NE"},
                            {"shape": "circle", "cx": 0.2,  "cy": 0.2,  "r": 0.09, "color": "rgba(0,180,255,0.5)", "label": "Tower NW"},
                            {"shape": "circle", "cx": 0.8,  "cy": 0.8,  "r": 0.09, "color": "rgba(0,180,255,0.5)", "label": "Tower SE"},
                            {"shape": "circle", "cx": 0.2,  "cy": 0.8,  "r": 0.09, "color": "rgba(0,180,255,0.5)", "label": "Tower SW"},
                        ],
                    },
                    "explanation": "Two players per tower. Tank+Melee soak NE/NW, Healer+Ranged soak SE/SW.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.8,  "y": 0.2}, "tolerance": 0.10},
                        {"role": "HEALER", "correct_position": {"x": 0.2,  "y": 0.8}, "tolerance": 0.10},
                        {"role": "MELEE",  "correct_position": {"x": 0.2,  "y": 0.2}, "tolerance": 0.10},
                        {"role": "RANGED", "correct_position": {"x": 0.8,  "y": 0.8}, "tolerance": 0.10},
                        {"role": "CASTER", "correct_position": {"x": 0.8,  "y": 0.8}, "tolerance": 0.10},
                    ],
                },
                {
                    "order": 2,
                    "title": "Ultrasonic Amp — Stack South",
                    "narration": (
                        "After towers, Vamp Fatale casts Ultrasonic Amp "
                        "(wide conal stack). Stack together south."
                    ),
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.3},
                        "boss_facing": "south",
                        "aoes": [
                            {
                                "shape": "cone",
                                "cx": 0.5, "cy": 0.3,
                                "angle": 180, "spread": 60,
                                "color": "rgba(0,150,255,0.35)",
                                "label": "Ultrasonic Amp (Stack)",
                            },
                        ],
                    },
                    "explanation": "Stack tightly south of the boss to share the Amp damage.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.6}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.65}},
                        {"role": "MELEE",  "correct_position": {"x": 0.45, "y": 0.6}},
                        {"role": "RANGED", "correct_position": {"x": 0.55, "y": 0.65}},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.62}},
                    ],
                },
            ],
        },
        {
            "slug": "sanguine-scratch",
            "name": "Sanguine Scratch",
            "phase_name": "Phase 3",
            "description": (
                "Protean wave attack — cone AoEs fire at every player's position. "
                "Spread to clock positions so cones don't overlap."
            ),
            "difficulty_rating": 3,
            "tags": ["protean", "spread", "cone"],
            "order": 14,
            "steps": [
                {
                    "order": 1,
                    "title": "Spread for Proteans",
                    "narration": (
                        "Protean cones fire at each player. Spread to assigned "
                        "clock positions so cones don't clip anyone."
                    ),
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 0,   "spread": 22, "color": "rgba(180,60,60,0.25)", "label": "Protean"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 90,  "spread": 22, "color": "rgba(180,60,60,0.25)", "label": "Protean"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 180, "spread": 22, "color": "rgba(180,60,60,0.25)", "label": "Protean"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 270, "spread": 22, "color": "rgba(180,60,60,0.25)", "label": "Protean"},
                        ],
                    },
                    "explanation": "Standard 8-way spread for protean cones. Don't overlap.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.1}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.9}},
                        {"role": "MELEE",  "correct_position": {"x": 0.1,  "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.9,  "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.85, "y": 0.15}},
                    ],
                },
            ],
        },
        {
            "slug": "undead-deathmatch",
            "name": "Undead Deathmatch",
            "phase_name": "Phase 3",
            "description": (
                "Final phase mechanic. Towers spawn with rotating bat adds. "
                "Soak towers in sequence while dodging the bats' AoEs."
            ),
            "difficulty_rating": 5,
            "tags": ["towers", "rotation", "sequential", "dodge"],
            "order": 15,
            "steps": [
                {
                    "order": 1,
                    "title": "Soak First Tower Set",
                    "narration": (
                        "Two towers spawn north. Tank + Melee soak the NW tower, "
                        "Healer + Ranged soak the NE tower. Watch for bat rotation."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.3, "cy": 0.2, "r": 0.09,
                             "color": "rgba(0,180,255,0.5)", "label": "Tower NW"},
                            {"shape": "circle", "cx": 0.7, "cy": 0.2, "r": 0.09,
                             "color": "rgba(0,180,255,0.5)", "label": "Tower NE"},
                        ],
                    },
                    "explanation": "Soak towers in pairs. Watch the bat rotation to know which set is next.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.3,  "y": 0.2}, "tolerance": 0.10},
                        {"role": "HEALER", "correct_position": {"x": 0.7,  "y": 0.2}, "tolerance": 0.10},
                        {"role": "MELEE",  "correct_position": {"x": 0.3,  "y": 0.2}, "tolerance": 0.10},
                        {"role": "RANGED", "correct_position": {"x": 0.7,  "y": 0.2}, "tolerance": 0.10},
                        {"role": "CASTER", "correct_position": {"x": 0.7,  "y": 0.2}, "tolerance": 0.10},
                    ],
                },
                {
                    "order": 2,
                    "title": "Soak Second Tower Set + Dodge Bats",
                    "narration": (
                        "Bats rotate clockwise. Second towers spawn south. "
                        "Move south and soak while avoiding the bat AoEs."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.3, "cy": 0.8, "r": 0.09,
                             "color": "rgba(0,180,255,0.5)", "label": "Tower SW"},
                            {"shape": "circle", "cx": 0.7, "cy": 0.8, "r": 0.09,
                             "color": "rgba(0,180,255,0.5)", "label": "Tower SE"},
                            {"shape": "circle", "cx": 0.15, "cy": 0.5, "r": 0.12,
                             "color": "rgba(255,80,80,0.25)", "label": "Bat AoE"},
                        ],
                    },
                    "explanation": "Move south to soak the second set. Dodge bats by staying centre-south.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.3,  "y": 0.8}, "tolerance": 0.10},
                        {"role": "HEALER", "correct_position": {"x": 0.7,  "y": 0.8}, "tolerance": 0.10},
                        {"role": "MELEE",  "correct_position": {"x": 0.3,  "y": 0.8}, "tolerance": 0.10},
                        {"role": "RANGED", "correct_position": {"x": 0.7,  "y": 0.8}, "tolerance": 0.10},
                        {"role": "CASTER", "correct_position": {"x": 0.7,  "y": 0.8}, "tolerance": 0.10},
                    ],
                },
            ],
        },
    ],
}
