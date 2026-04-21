"""
Seed data for M10S — The Xtremes (AAC Heavyweight M2 Savage).

Complete fight walkthrough: Red Hot & Deep Blue dual boss encounter.
Phase 1: Hot Impact → Flame Floater → Alley-oop Inferno → Cutback Blaze →
         Pyrolation → Sick Swell → Sickest Take-off → Alley-oop Double-Dip
Phase 2: Insane Air → Firesnaking / Watersnaking → Hot Aerial
Phase 3: Xtreme Spectacular → Watery Grave → Xtreme Wave
"""

M10S_FIGHT = {
    "slug": "m10s",
    "name": "AAC Heavyweight M2 (Savage)",
    "short_name": "M10S",
    "boss_name": "The Xtremes (Red Hot & Deep Blue)",
    "difficulty": "SAVAGE",
    "arena_shape": "SQUARE",
    "order": 2,
    "mechanics": [
        # ── Phase 1 ──────────────────────────────────────────────────
        {
            "slug": "hot-impact",
            "name": "Hot Impact",
            "phase_name": "Phase 1",
            "description": (
                "Dual tankbuster. Red Hot hits the MT, Deep Blue hits the OT. "
                "Tanks separate, party stays away."
            ),
            "difficulty_rating": 2,
            "tags": ["tankbuster"],
            "order": 1,
            "steps": [
                {
                    "order": 1,
                    "title": "Resolve Tankbuster",
                    "narration": (
                        "Both bosses hit their tanks with cleaving busters. "
                        "Tanks separate north and south, party stays mid."
                    ),
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.4},
                    },
                    "explanation": "Tanks separate to avoid stacking busters. Party stays mid.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.15}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.6}},
                        {"role": "MELEE",  "correct_position": {"x": 0.5,  "y": 0.55}},
                        {"role": "RANGED", "correct_position": {"x": 0.5,  "y": 0.65}},
                    ],
                },
            ],
        },
        {
            "slug": "flame-floater",
            "name": "Flame Floater",
            "phase_name": "Phase 1",
            "description": (
                "Red Hot tethers to two players. Tethered players stretch the "
                "tether far away to reduce damage. Non-tethered stack."
            ),
            "difficulty_rating": 3,
            "tags": ["tether", "spread"],
            "order": 2,
            "steps": [
                {
                    "order": 1,
                    "title": "Stretch or Stack",
                    "narration": (
                        "Two players get fire tethers. Stretch them to opposite "
                        "corners. Everyone else stacks mid."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "tethers": [
                            {"from": {"x": 0.5, "y": 0.5}, "to": {"x": 0.15, "y": 0.15}, "color": "#ff4444"},
                            {"from": {"x": 0.5, "y": 0.5}, "to": {"x": 0.85, "y": 0.85}, "color": "#ff4444"},
                        ],
                    },
                    "explanation": "Tethered players go to opposite corners. Party stays centre.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.15, "y": 0.15}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.5}},
                        {"role": "MELEE",  "correct_position": {"x": 0.85, "y": 0.85}},
                        {"role": "RANGED", "correct_position": {"x": 0.5,  "y": 0.5}},
                    ],
                },
            ],
        },
        {
            "slug": "alley-oop-inferno",
            "name": "Alley-oop Inferno",
            "phase_name": "Phase 1",
            "description": (
                "Red Hot slams the ground creating expanding fire puddles at "
                "each player's position. Spread to designated positions, then "
                "move away from the puddles."
            ),
            "difficulty_rating": 3,
            "tags": ["spread", "puddle", "bait"],
            "order": 3,
            "steps": [
                {
                    "order": 1,
                    "title": "Spread to Bait Positions",
                    "narration": (
                        "Puddles will drop under every player. Spread to your "
                        "assigned clock spot to avoid overlapping."
                    ),
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.5, "r": 0.06,
                             "color": "rgba(255,100,0,0.4)", "label": "Bait puddle"},
                        ],
                    },
                    "explanation": "Standard clock spread. Drop puddles at the edge, then dodge inward.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.1}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.9}},
                        {"role": "MELEE",  "correct_position": {"x": 0.1,  "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.9,  "y": 0.5}},
                    ],
                },
            ],
        },
        {
            "slug": "cutback-blaze",
            "name": "Cutback Blaze",
            "phase_name": "Phase 1",
            "description": (
                "Red Hot targets the furthest player with a tether, then covers "
                "the arena in fire except for a safe cone behind the target."
            ),
            "difficulty_rating": 3,
            "tags": ["cone", "safe-spot", "tether"],
            "order": 4,
            "steps": [
                {
                    "order": 1,
                    "title": "Stack in the Safe Cone",
                    "narration": (
                        "Red Hot tethers to the furthest player (south). "
                        "A safe cone extends behind that player. Stack inside."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.3},
                        "boss_facing": "south",
                        "tethers": [
                            {"from": {"x": 0.5, "y": 0.3}, "to": {"x": 0.5, "y": 0.9}, "color": "#ff4444"},
                        ],
                        "aoes": [
                            {"shape": "rect", "x": 0.0, "y": 0.0, "w": 0.35, "h": 1.0,
                             "color": "rgba(255,80,0,0.3)", "label": "Fire"},
                            {"shape": "rect", "x": 0.65, "y": 0.0, "w": 0.35, "h": 1.0,
                             "color": "rgba(255,80,0,0.3)", "label": "Fire"},
                        ],
                    },
                    "explanation": "Stack south-centre in the safe cone behind the tethered player.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.8}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.85}},
                        {"role": "MELEE",  "correct_position": {"x": 0.45, "y": 0.75}},
                        {"role": "RANGED", "correct_position": {"x": 0.5,  "y": 0.9}},
                    ],
                },
            ],
        },
        {
            "slug": "pyrolation",
            "name": "Pyrolation",
            "phase_name": "Phase 1",
            "description": (
                "Healer stack marker. Both healers must stack with their light party. "
                "LP1 north, LP2 south."
            ),
            "difficulty_rating": 2,
            "tags": ["stack", "healer"],
            "order": 5,
            "steps": [
                {
                    "order": 1,
                    "title": "Stack with Light Party",
                    "narration": "Healer stack markers. LP1 north, LP2 south.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "Stack with healer", "color": "#44ff44"},
                        ],
                    },
                    "explanation": "Stack tightly with your light party healer.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.25}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.25}},
                        {"role": "MELEE",  "correct_position": {"x": 0.5,  "y": 0.25}},
                        {"role": "RANGED", "correct_position": {"x": 0.5,  "y": 0.75}},
                    ],
                },
            ],
        },
        {
            "slug": "sick-swell",
            "name": "Sick Swell",
            "phase_name": "Phase 1",
            "description": (
                "Deep Blue creates a wave from one side. Players are knocked back. "
                "Position so the knockback sends you safely, or use KB immunity."
            ),
            "difficulty_rating": 3,
            "tags": ["knockback", "positioning"],
            "order": 6,
            "steps": [
                {
                    "order": 1,
                    "title": "Position for Knockback",
                    "narration": (
                        "Wave from the north. Position mid so the knockback "
                        "pushes you south safely."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "rect", "x": 0.0, "y": 0.0, "w": 1.0, "h": 0.15,
                             "color": "rgba(0,120,255,0.4)", "label": "Wave (Knockback)"},
                        ],
                    },
                    "explanation": "Stand mid-arena. Use Arm's Length / Surecast or position carefully.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.4}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.45}},
                        {"role": "MELEE",  "correct_position": {"x": 0.4,  "y": 0.4}},
                        {"role": "RANGED", "correct_position": {"x": 0.6,  "y": 0.45}},
                    ],
                },
            ],
        },
        {
            "slug": "sickest-takeoff",
            "name": "Sickest Take-off",
            "phase_name": "Phase 1",
            "description": (
                "Both bosses dash across the arena with orb telegraphs. "
                "Read the orbs: fire orb = spread, water orb = stack."
            ),
            "difficulty_rating": 4,
            "tags": ["dash", "spread", "stack", "choice"],
            "order": 7,
            "steps": [
                {
                    "order": 1,
                    "title": "Read the Dash Orbs",
                    "narration": (
                        "Red Hot shows a spread orb. Deep Blue shows a stack orb. "
                        "DPS spread, supports stack."
                    ),
                    "timer_seconds": 5,
                    "action_type": "CHOICE",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "Red Hot — Spread Orb", "color": "#ff4444"},
                            {"label": "Deep Blue — Stack Orb", "color": "#4488ff"},
                        ],
                    },
                    "choices": [
                        {"id": "spread", "label": "Spread (away from Red Hot's path)"},
                        {"id": "stack",  "label": "Stack (group for Deep Blue's hit)"},
                    ],
                    "explanation": "DPS spread for Red Hot. Tanks and Healers stack for Deep Blue.",
                    "role_variants": [
                        {"role": "TANK",   "correct_choice": "stack"},
                        {"role": "HEALER", "correct_choice": "stack"},
                        {"role": "MELEE",  "correct_choice": "spread"},
                        {"role": "RANGED", "correct_choice": "spread"},
                    ],
                },
                {
                    "order": 2,
                    "title": "Resolve Dash — Position",
                    "narration": "After reading orbs, move to your position.",
                    "timer_seconds": 4,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                    },
                    "explanation": "Spreaders fan out to intercardinals. Stackers group north.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.2}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.2}},
                        {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.85}},
                        {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.85}},
                    ],
                },
            ],
        },
        {
            "slug": "alley-oop-double-dip",
            "name": "Alley-oop Double-Dip",
            "phase_name": "Phase 1",
            "description": (
                "Two alternating sets of cone AoEs from the bosses. "
                "Dodge the first set, then move into the resolved area "
                "to avoid the second."
            ),
            "difficulty_rating": 3,
            "tags": ["cone", "dodge", "sequential"],
            "order": 8,
            "steps": [
                {
                    "order": 1,
                    "title": "Dodge First Cone Set",
                    "narration": (
                        "First cones fire at cardinals. Stand at intercardinals."
                    ),
                    "timer_seconds": 4,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 0,   "spread": 40, "color": "rgba(255,80,0,0.3)", "label": "Cone N"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 90,  "spread": 40, "color": "rgba(255,80,0,0.3)", "label": "Cone E"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 180, "spread": 40, "color": "rgba(255,80,0,0.3)", "label": "Cone S"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 270, "spread": 40, "color": "rgba(255,80,0,0.3)", "label": "Cone W"},
                        ],
                    },
                    "explanation": "Intercardinals are safe from the first set of cardinal cones.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.15, "y": 0.15}},
                        {"role": "HEALER", "correct_position": {"x": 0.85, "y": 0.85}},
                        {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.85}},
                        {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.15}},
                    ],
                },
                {
                    "order": 2,
                    "title": "Dodge Second Cone Set",
                    "narration": "Second cones fire at intercardinals. Move to cardinals.",
                    "timer_seconds": 4,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 45,  "spread": 40, "color": "rgba(0,120,255,0.3)", "label": "Cone NE"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 135, "spread": 40, "color": "rgba(0,120,255,0.3)", "label": "Cone SE"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 225, "spread": 40, "color": "rgba(0,120,255,0.3)", "label": "Cone SW"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 315, "spread": 40, "color": "rgba(0,120,255,0.3)", "label": "Cone NW"},
                        ],
                    },
                    "explanation": "Swap to cardinals for the second set.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.15}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.85}},
                        {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.5}},
                    ],
                },
            ],
        },

        # ── Phase 2 ──────────────────────────────────────────────────
        {
            "slug": "insane-air",
            "name": "Insane Air",
            "phase_name": "Phase 2",
            "description": (
                "Both bosses dash across the arena simultaneously. "
                "Each dash has an orb: spread, stack, or tank buster. "
                "Read both orbs and resolve."
            ),
            "difficulty_rating": 4,
            "tags": ["dash", "spread", "stack", "tankbuster"],
            "order": 9,
            "steps": [
                {
                    "order": 1,
                    "title": "Read the Orbs",
                    "narration": (
                        "Red Hot has a spread orb. Deep Blue has a stack orb. "
                        "Identify your action."
                    ),
                    "timer_seconds": 5,
                    "action_type": "CHOICE",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "Red Hot — Spread Orb", "color": "#ff4444"},
                            {"label": "Deep Blue — Stack Orb", "color": "#4488ff"},
                        ],
                    },
                    "choices": [
                        {"id": "spread", "label": "Spread (away from Red Hot)"},
                        {"id": "stack",  "label": "Stack (group for Deep Blue)"},
                    ],
                    "explanation": "DPS spread. Supports stack.",
                    "role_variants": [
                        {"role": "TANK",   "correct_choice": "stack"},
                        {"role": "HEALER", "correct_choice": "stack"},
                        {"role": "MELEE",  "correct_choice": "spread"},
                        {"role": "RANGED", "correct_choice": "spread"},
                    ],
                },
            ],
        },
        {
            "slug": "firesnaking",
            "name": "Firesnaking / Watersnaking",
            "phase_name": "Phase 2",
            "description": (
                "Fire or water debuffs on players that explode after a timer. "
                "Fire players spread away from the group. Water players stack."
            ),
            "difficulty_rating": 4,
            "tags": ["debuff", "spread", "stack", "proximity"],
            "order": 10,
            "steps": [
                {
                    "order": 1,
                    "title": "Check Your Debuff",
                    "narration": (
                        "Fire debuff = you will explode, spread away. "
                        "Water debuff = you need to stack to share damage."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "🔥 Firesnaking — Spread", "color": "#ff4444"},
                            {"label": "💧 Watersnaking — Stack", "color": "#4488ff"},
                        ],
                    },
                    "explanation": "Fire players go far. Water players stack centre.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.5}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.5}},
                        {"role": "MELEE",  "correct_position": {"x": 0.1,  "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.9,  "y": 0.5}},
                    ],
                },
            ],
        },
        {
            "slug": "hot-aerial",
            "name": "Hot Aerial",
            "phase_name": "Phase 2",
            "description": (
                "Red Hot performs sequential jumps to waymarked positions. "
                "Each jump creates an AoE. Dodge away from each landing zone."
            ),
            "difficulty_rating": 3,
            "tags": ["sequential", "dodge", "aoe"],
            "order": 11,
            "steps": [
                {
                    "order": 1,
                    "title": "Dodge Jump 1 — North",
                    "narration": "Red Hot jumps north. Move south.",
                    "timer_seconds": 4,
                    "action_type": "POSITION",
                    "default_tolerance": 0.25,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.2},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.2, "r": 0.25,
                             "color": "rgba(255,80,0,0.3)", "label": "Jump AoE"},
                        ],
                    },
                    "explanation": "Stay south to avoid the jump AoE.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.75}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.8}},
                        {"role": "MELEE",  "correct_position": {"x": 0.4,  "y": 0.7}},
                        {"role": "RANGED", "correct_position": {"x": 0.6,  "y": 0.8}},
                    ],
                },
                {
                    "order": 2,
                    "title": "Dodge Jump 2 — South",
                    "narration": "Red Hot jumps south. Move north into the resolved area.",
                    "timer_seconds": 4,
                    "action_type": "POSITION",
                    "default_tolerance": 0.25,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.8},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.8, "r": 0.25,
                             "color": "rgba(255,80,0,0.3)", "label": "Jump AoE"},
                        ],
                    },
                    "explanation": "Move back north into the already-resolved safe zone.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.25}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.3}},
                        {"role": "MELEE",  "correct_position": {"x": 0.4,  "y": 0.25}},
                        {"role": "RANGED", "correct_position": {"x": 0.6,  "y": 0.3}},
                    ],
                },
            ],
        },

        # ── Phase 3 ──────────────────────────────────────────────────
        {
            "slug": "xtreme-spectacular",
            "name": "Xtreme Spectacular",
            "phase_name": "Phase 3",
            "description": (
                "Proximity-based raidwide. Get as far as possible from the "
                "centre to reduce damage."
            ),
            "difficulty_rating": 2,
            "tags": ["proximity", "raidwide"],
            "order": 12,
            "steps": [
                {
                    "order": 1,
                    "title": "Maximize Distance from Centre",
                    "narration": "Proximity damage from centre. Run to the edge.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.5, "r": 0.15,
                             "color": "rgba(255,200,0,0.5)", "label": "Proximity Source"},
                        ],
                    },
                    "explanation": "Get to the wall. Further = less damage.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.05}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.95}},
                        {"role": "MELEE",  "correct_position": {"x": 0.05, "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.95, "y": 0.5}},
                    ],
                },
            ],
        },
        {
            "slug": "watery-grave",
            "name": "Watery Grave",
            "phase_name": "Phase 3",
            "description": (
                "Deep Blue traps players in water bubbles (towers). "
                "Other players must soak the bubbles to free them."
            ),
            "difficulty_rating": 4,
            "tags": ["towers", "soak", "bubble"],
            "order": 13,
            "steps": [
                {
                    "order": 1,
                    "title": "Soak the Water Bubbles",
                    "narration": (
                        "Two players trapped in bubbles at intercardinals. "
                        "Remaining players soak to free them."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.25, "cy": 0.25, "r": 0.1,
                             "color": "rgba(0,120,255,0.4)", "label": "Bubble NW"},
                            {"shape": "circle", "cx": 0.75, "cy": 0.75, "r": 0.1,
                             "color": "rgba(0,120,255,0.4)", "label": "Bubble SE"},
                        ],
                    },
                    "explanation": "One soaker per bubble. Free your trapped teammates.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.25, "y": 0.25}, "tolerance": 0.10},
                        {"role": "HEALER", "correct_position": {"x": 0.75, "y": 0.75}, "tolerance": 0.10},
                        {"role": "MELEE",  "correct_position": {"x": 0.25, "y": 0.25}, "tolerance": 0.10},
                        {"role": "RANGED", "correct_position": {"x": 0.75, "y": 0.75}, "tolerance": 0.10},
                    ],
                },
            ],
        },
        {
            "slug": "xtreme-wave",
            "name": "Xtreme Wave",
            "phase_name": "Phase 3",
            "description": (
                "Both bosses tether to players and dash through them. "
                "Stretch tethers and position so dashes don't clip others."
            ),
            "difficulty_rating": 4,
            "tags": ["tether", "dash", "spread"],
            "order": 14,
            "steps": [
                {
                    "order": 1,
                    "title": "Stretch Tethers to Corners",
                    "narration": (
                        "Tethered players take corners. Non-tethered stack centre."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "tethers": [
                            {"from": {"x": 0.5, "y": 0.5}, "to": {"x": 0.1, "y": 0.1}, "color": "#ff4444"},
                            {"from": {"x": 0.5, "y": 0.5}, "to": {"x": 0.9, "y": 0.9}, "color": "#4488ff"},
                        ],
                    },
                    "explanation": "Stretch tethers to opposite corners. Non-tethered stay centre.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.1,  "y": 0.1}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.5}},
                        {"role": "MELEE",  "correct_position": {"x": 0.9,  "y": 0.9}},
                        {"role": "RANGED", "correct_position": {"x": 0.5,  "y": 0.5}},
                    ],
                },
            ],
        },
        {
            "slug": "freaky-pyrotation",
            "name": "Freaky Pyrotation",
            "phase_name": "Phase 3",
            "description": (
                "Role-based stack markers with rotating fire AoEs. "
                "Stack with your group while dodging rotating fire."
            ),
            "difficulty_rating": 4,
            "tags": ["stack", "rotation", "dodge"],
            "order": 15,
            "steps": [
                {
                    "order": 1,
                    "title": "Stack with Role Group",
                    "narration": (
                        "Supports stack north, DPS stack south. "
                        "Dodge rotating fire AoEs while maintaining stacks."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.2, "cy": 0.5, "r": 0.15,
                             "color": "rgba(255,80,0,0.25)", "label": "Rotating Fire"},
                            {"shape": "circle", "cx": 0.8, "cy": 0.5, "r": 0.15,
                             "color": "rgba(255,80,0,0.25)", "label": "Rotating Fire"},
                        ],
                        "debuffs": [
                            {"label": "Role Stack", "color": "#44ff44"},
                        ],
                    },
                    "explanation": "Stay with your role group. Move together to dodge rotating fire.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.25}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.25}},
                        {"role": "MELEE",  "correct_position": {"x": 0.5,  "y": 0.75}},
                        {"role": "RANGED", "correct_position": {"x": 0.5,  "y": 0.75}},
                    ],
                },
            ],
        },
    ],
}
