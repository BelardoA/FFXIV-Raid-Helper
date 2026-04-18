"""
Seed data for M11S — The Tyrant (AAC Heavyweight M3 Savage).

Complete fight walkthrough.
Phase 1: Crown of Arcadia → Raw Steel Trophy → Trophy Weapons →
         Void Stardust → Dance of Domination → Charybdistopia →
         Ultimate Trophy Weapons → Powerful Gust
Phase 2: Great Wall of Fire → Orbital Omen → Fire and Fury + Meteorain →
         Foregone Fatality → Triple Tyrannhilation
Phase 3: Flatliner → Majestic Meteor → Fire Breath → Arcadion Avalanche
Phase 4: Ecliptic Stampede → Heartbreak Kick (Enrage)
"""

M11S_FIGHT = {
    "slug": "m11s",
    "name": "AAC Heavyweight M3 (Savage)",
    "short_name": "M11S",
    "boss_name": "The Tyrant",
    "difficulty": "SAVAGE",
    "arena_shape": "SQUARE",
    "order": 3,
    "mechanics": [
        # ── Phase 1 ──────────────────────────────────────────────────
        {
            "slug": "crown-of-arcadia",
            "name": "Crown of Arcadia",
            "phase_name": "Phase 1",
            "description": (
                "Heavy raidwide. The Tyrant's signature raidwide damage. "
                "Mitigate and shield."
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
                        {"id": "nothing",  "label": "Do nothing"},
                    ],
                    "explanation": "Always mitigate raidwides. Deploy shields and party mitigation.",
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
            "slug": "raw-steel-trophy",
            "name": "Raw Steel Trophy",
            "phase_name": "Phase 1",
            "description": (
                "The Tyrant draws either an axe or scythe. Axe = get close "
                "(point-blank safe). Scythe = get far (donut safe)."
            ),
            "difficulty_rating": 2,
            "tags": ["dodge", "reaction"],
            "order": 2,
            "steps": [
                {
                    "order": 1,
                    "title": "Identify Weapon — Axe or Scythe",
                    "narration": (
                        "Watch what weapon The Tyrant draws. "
                        "Axe = in. Scythe = out."
                    ),
                    "timer_seconds": 4,
                    "action_type": "CHOICE",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "Axe = Stay Close", "color": "#ff4444"},
                            {"label": "Scythe = Get Far", "color": "#44ff44"},
                        ],
                    },
                    "choices": [
                        {"id": "in",  "label": "Get In (Axe — point-blank safe)"},
                        {"id": "out", "label": "Get Out (Scythe — donut safe)"},
                    ],
                    "explanation": "Axe hits far, scythe hits close. React to the weapon draw.",
                    "role_variants": [
                        {"role": "TANK",   "correct_choice": "in"},
                        {"role": "HEALER", "correct_choice": "in"},
                        {"role": "MELEE",  "correct_choice": "in"},
                        {"role": "RANGED", "correct_choice": "in"},
                        {"role": "CASTER", "correct_choice": "in"},
                    ],
                },
            ],
        },
        {
            "slug": "trophy-weapons",
            "name": "Trophy Weapons + Assault Evolved",
            "phase_name": "Phase 1",
            "description": (
                "The Tyrant draws a scythe or axe, then spawns three weapons "
                "around the arena. She jumps to each in clockwise order. "
                "Track the weapon order and dodge accordingly."
            ),
            "difficulty_rating": 3,
            "tags": ["dodge", "sequential", "pattern"],
            "order": 3,
            "steps": [
                {
                    "order": 1,
                    "title": "Identify Weapon Pattern",
                    "narration": (
                        "Three weapons spawn: NW, NE, S. The Tyrant jumps "
                        "clockwise starting NW. First weapon is a scythe — "
                        "it cleaves the half it faces."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "default_tolerance": 0.25,
                    "arena_state": {
                        "boss_position": {"x": 0.2, "y": 0.2},
                        "boss_facing": "east",
                        "aoes": [
                            {
                                "shape": "rect",
                                "x": 0.0, "y": 0.0, "w": 0.5, "h": 1.0,
                                "color": "rgba(255,80,80,0.3)",
                                "label": "Scythe Cleave (West)",
                            },
                        ],
                        "markers": [
                            {"id": "1", "x": 0.2, "y": 0.2},
                            {"id": "2", "x": 0.8, "y": 0.2},
                            {"id": "3", "x": 0.5, "y": 0.85},
                        ],
                    },
                    "explanation": "The scythe cleaves the west half. Move east.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.7,  "y": 0.4},  "safe_zones": [{"x": 0.5, "y": 0.0, "w": 0.5, "h": 1.0}]},
                        {"role": "HEALER", "correct_position": {"x": 0.75, "y": 0.6},  "safe_zones": [{"x": 0.5, "y": 0.0, "w": 0.5, "h": 1.0}]},
                        {"role": "MELEE",  "correct_position": {"x": 0.6,  "y": 0.5},  "safe_zones": [{"x": 0.5, "y": 0.0, "w": 0.5, "h": 1.0}]},
                        {"role": "RANGED", "correct_position": {"x": 0.8,  "y": 0.7},  "safe_zones": [{"x": 0.5, "y": 0.0, "w": 0.5, "h": 1.0}]},
                        {"role": "CASTER", "correct_position": {"x": 0.75, "y": 0.75}, "safe_zones": [{"x": 0.5, "y": 0.0, "w": 0.5, "h": 1.0}]},
                    ],
                },
            ],
        },
        {
            "slug": "void-stardust",
            "name": "Void Stardust",
            "phase_name": "Phase 1",
            "description": (
                "Three sets of ground AoEs drop under all players. "
                "Keep moving — don't stand in the same spot twice."
            ),
            "difficulty_rating": 3,
            "tags": ["bait", "puddle", "dodge"],
            "order": 4,
            "steps": [
                {
                    "order": 1,
                    "title": "Bait and Dodge AoEs",
                    "narration": (
                        "AoEs drop under every player in sequence. "
                        "Move in a consistent direction to avoid puddles."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.3, "cy": 0.3, "r": 0.08, "color": "rgba(160,100,255,0.4)", "label": "Stardust"},
                            {"shape": "circle", "cx": 0.7, "cy": 0.3, "r": 0.08, "color": "rgba(160,100,255,0.4)", "label": "Stardust"},
                            {"shape": "circle", "cx": 0.5, "cy": 0.7, "r": 0.08, "color": "rgba(160,100,255,0.4)", "label": "Stardust"},
                        ],
                    },
                    "explanation": "Bait AoEs, then move out. Move in one direction to avoid backtracking.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.15}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.85}},
                        {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.85, "y": 0.85}},
                    ],
                },
            ],
        },
        {
            "slug": "dance-of-domination",
            "name": "Dance of Domination Trophy",
            "phase_name": "Phase 1",
            "description": (
                "Line AoEs plus stack/spread markers. Dodge the lines while "
                "resolving your mechanic."
            ),
            "difficulty_rating": 3,
            "tags": ["line", "stack", "spread", "dodge"],
            "order": 5,
            "steps": [
                {
                    "order": 1,
                    "title": "Dodge Lines + Resolve Markers",
                    "narration": (
                        "Lines fire from east and west walls. Stack markers on "
                        "supports, spread markers on DPS."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "rect", "x": 0.0, "y": 0.3, "w": 1.0, "h": 0.15,
                             "color": "rgba(255,80,80,0.3)", "label": "Line AoE"},
                            {"shape": "rect", "x": 0.0, "y": 0.6, "w": 1.0, "h": 0.15,
                             "color": "rgba(255,80,80,0.3)", "label": "Line AoE"},
                        ],
                        "debuffs": [
                            {"label": "Support — Stack", "color": "#2b7fff"},
                            {"label": "DPS — Spread", "color": "#ff6b35"},
                        ],
                    },
                    "explanation": "Stay in safe rows. Supports stack north, DPS spread south.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.15}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.15}},
                        {"role": "MELEE",  "correct_position": {"x": 0.2,  "y": 0.85}},
                        {"role": "RANGED", "correct_position": {"x": 0.8,  "y": 0.85}},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.85}},
                    ],
                },
            ],
        },
        {
            "slug": "charybdistopia",
            "name": "Charybdistopia",
            "phase_name": "Phase 1",
            "description": (
                "The Tyrant reduces everyone to 1 HP, then applies a bleed. "
                "Healers must top the party quickly. Use personal mitigation."
            ),
            "difficulty_rating": 3,
            "tags": ["raidwide", "heal-check"],
            "order": 6,
            "steps": [
                {
                    "order": 1,
                    "title": "Survive the HP Reduction",
                    "action_type": "CHOICE",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "HP → 1 + Bleed", "color": "#ff0000"},
                        ],
                    },
                    "choices": [
                        {"id": "mitigate", "label": "Use personal mitigation + healers top party"},
                        {"id": "nothing",  "label": "Do nothing"},
                    ],
                    "explanation": "Everyone to 1 HP. Healers must heal immediately. Personal mits help survive the bleed.",
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
            "slug": "ultimate-trophy-weapons",
            "name": "Ultimate Trophy Weapons",
            "phase_name": "Phase 1",
            "description": (
                "Six weapons spawn around the arena. The Tyrant jumps to each "
                "in sequence. Track all six weapons and dodge each attack."
            ),
            "difficulty_rating": 5,
            "tags": ["dodge", "sequential", "pattern", "complex"],
            "order": 7,
            "steps": [
                {
                    "order": 1,
                    "title": "Track Weapon Sequence — First Three",
                    "narration": (
                        "Six weapons spawn. Focus on the first three: "
                        "dodge each cleave or AoE in order."
                    ),
                    "timer_seconds": 8,
                    "action_type": "POSITION",
                    "default_tolerance": 0.25,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "markers": [
                            {"id": "1", "x": 0.15, "y": 0.15},
                            {"id": "2", "x": 0.85, "y": 0.15},
                            {"id": "3", "x": 0.15, "y": 0.85},
                            {"id": "4", "x": 0.85, "y": 0.85},
                            {"id": "5", "x": 0.5,  "y": 0.15},
                            {"id": "6", "x": 0.5,  "y": 0.85},
                        ],
                        "aoes": [
                            {"shape": "rect", "x": 0.0, "y": 0.0, "w": 0.5, "h": 1.0,
                             "color": "rgba(255,80,80,0.2)", "label": "First Cleave"},
                        ],
                    },
                    "explanation": (
                        "Memorize the weapon sequence. Start east for the first "
                        "cleave, then react to each subsequent weapon."
                    ),
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.7,  "y": 0.3}},
                        {"role": "HEALER", "correct_position": {"x": 0.75, "y": 0.7}},
                        {"role": "MELEE",  "correct_position": {"x": 0.6,  "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.8,  "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.75, "y": 0.6}},
                    ],
                },
                {
                    "order": 2,
                    "title": "Track Weapon Sequence — Last Three",
                    "narration": (
                        "Continue tracking. The last three weapons fire. "
                        "Move to the safe spot for each."
                    ),
                    "timer_seconds": 8,
                    "action_type": "POSITION",
                    "default_tolerance": 0.25,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.5, "r": 0.3,
                             "color": "rgba(160,100,255,0.2)", "label": "AoE Pattern"},
                        ],
                    },
                    "explanation": "React to each weapon in sequence. Stay flexible.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.15}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.85}},
                        {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.85, "y": 0.85}},
                    ],
                },
            ],
        },
        {
            "slug": "powerful-gust",
            "name": "Powerful Gust",
            "phase_name": "Phase 1",
            "description": (
                "Tornado baits drop under players. Bait them at the edge, "
                "then move inward to avoid."
            ),
            "difficulty_rating": 2,
            "tags": ["bait", "dodge"],
            "order": 8,
            "steps": [
                {
                    "order": 1,
                    "title": "Bait Tornadoes at Edge",
                    "narration": "Tornadoes drop under players. Bait at the wall.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.5, "r": 0.06,
                             "color": "rgba(0,200,100,0.4)", "label": "Tornado Bait"},
                        ],
                    },
                    "explanation": "Drop tornadoes at the wall, then move centre.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.05}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.95}},
                        {"role": "MELEE",  "correct_position": {"x": 0.05, "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.95, "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.95, "y": 0.95}},
                    ],
                },
            ],
        },

        # ── Phase 2 ──────────────────────────────────────────────────
        {
            "slug": "great-wall-of-fire",
            "name": "Great Wall of Fire",
            "phase_name": "Phase 2",
            "description": (
                "Shared tankbuster that creates a wall of fire across the arena. "
                "Both tanks stack, party avoids."
            ),
            "difficulty_rating": 2,
            "tags": ["tankbuster", "shared"],
            "order": 9,
            "steps": [
                {
                    "order": 1,
                    "title": "Tanks Stack, Party Dodge",
                    "narration": (
                        "Shared tankbuster aimed south. Tanks stack south. "
                        "Party stays north."
                    ),
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.4},
                        "boss_facing": "south",
                    },
                    "explanation": "Tanks share the buster south. Party stays north of boss.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.75}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.2}},
                        {"role": "MELEE",  "correct_position": {"x": 0.5,  "y": 0.25}},
                        {"role": "RANGED", "correct_position": {"x": 0.5,  "y": 0.15}},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.15}},
                    ],
                },
            ],
        },
        {
            "slug": "orbital-omen",
            "name": "Orbital Omen",
            "phase_name": "Phase 2",
            "description": (
                "Portal lines appear on the arena that fire line AoEs. "
                "Identify the safe lanes between portals."
            ),
            "difficulty_rating": 3,
            "tags": ["portal", "line", "dodge"],
            "order": 10,
            "steps": [
                {
                    "order": 1,
                    "title": "Find Safe Lanes",
                    "narration": (
                        "Portals on east and west fire line AoEs across the arena. "
                        "Stand in the gaps between portal lines."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "rect", "x": 0.0, "y": 0.15, "w": 1.0, "h": 0.1,
                             "color": "rgba(160,0,200,0.3)", "label": "Portal Line"},
                            {"shape": "rect", "x": 0.0, "y": 0.45, "w": 1.0, "h": 0.1,
                             "color": "rgba(160,0,200,0.3)", "label": "Portal Line"},
                            {"shape": "rect", "x": 0.0, "y": 0.75, "w": 1.0, "h": 0.1,
                             "color": "rgba(160,0,200,0.3)", "label": "Portal Line"},
                        ],
                    },
                    "explanation": "Stand in rows between the portal lines. Safe rows at y≈0.3, y≈0.6, y≈0.9.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.3}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.6}},
                        {"role": "MELEE",  "correct_position": {"x": 0.4,  "y": 0.3}},
                        {"role": "RANGED", "correct_position": {"x": 0.6,  "y": 0.6}},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.9}},
                    ],
                },
            ],
        },
        {
            "slug": "fire-and-fury",
            "name": "Fire and Fury + Meteorain",
            "phase_name": "Phase 2",
            "description": (
                "Front/back conal AoEs, then Meteorain targets the two closest "
                "players. Non-prey players stack for Fearsome Fireball."
            ),
            "difficulty_rating": 4,
            "tags": ["cone", "prey", "stack", "bait"],
            "order": 11,
            "steps": [
                {
                    "order": 1,
                    "title": "Dodge Fire and Fury Cones",
                    "narration": "Cones fire from the boss's front and back. Stand at the flanks.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "boss_facing": "north",
                        "aoes": [
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 0,   "spread": 60, "color": "rgba(255,120,0,0.35)", "label": "Fire (Front)"},
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 180, "spread": 60, "color": "rgba(255,120,0,0.35)", "label": "Fury (Back)"},
                        ],
                    },
                    "explanation": "Stand east or west — both flanks are safe.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.2,  "y": 0.5}},
                        {"role": "HEALER", "correct_position": {"x": 0.8,  "y": 0.5}},
                        {"role": "MELEE",  "correct_position": {"x": 0.3,  "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.8,  "y": 0.5}},
                    ],
                },
                {
                    "order": 2,
                    "title": "Bait Meteorain or Stack",
                    "narration": (
                        "Tanks bait Meteorain close to boss. "
                        "Everyone else stacks south for Fearsome Fireball."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "Meteorain Prey (Closest 2)", "color": "#ff4444"},
                            {"label": "Fearsome Fireball (Stack)", "color": "#44aaff"},
                        ],
                    },
                    "explanation": "Tanks bait close. All others stack south.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.4}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.85}},
                        {"role": "MELEE",  "correct_position": {"x": 0.45, "y": 0.85}},
                        {"role": "RANGED", "correct_position": {"x": 0.55, "y": 0.85}},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.85}},
                    ],
                },
            ],
        },
        {
            "slug": "foregone-fatality",
            "name": "Foregone Fatality + Triple Tyrannhilation",
            "phase_name": "Phase 2",
            "description": (
                "Portals drop rocks, then three hits of raidwide. "
                "Hide behind rocks — each hit destroys one rock."
            ),
            "difficulty_rating": 4,
            "tags": ["raidwide", "line-of-sight", "sequential"],
            "order": 12,
            "steps": [
                {
                    "order": 1,
                    "title": "Hide Behind Rock 1",
                    "narration": (
                        "Three rocks at south, east, and west. Hide behind "
                        "rock 1 (south). Move to next rock after it breaks."
                    ),
                    "timer_seconds": 4,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.2},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5,  "cy": 0.8,  "r": 0.06, "color": "rgba(180,140,60,0.7)", "label": "Rock 1"},
                            {"shape": "circle", "cx": 0.15, "cy": 0.5,  "r": 0.06, "color": "rgba(180,140,60,0.7)", "label": "Rock 2"},
                            {"shape": "circle", "cx": 0.85, "cy": 0.5,  "r": 0.06, "color": "rgba(180,140,60,0.7)", "label": "Rock 3"},
                        ],
                    },
                    "explanation": "Line-of-sight the boss behind the south rock.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.85}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.88}},
                        {"role": "MELEE",  "correct_position": {"x": 0.45, "y": 0.85}},
                        {"role": "RANGED", "correct_position": {"x": 0.55, "y": 0.88}},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.87}},
                    ],
                },
                {
                    "order": 2,
                    "title": "Move to Rock 2",
                    "narration": "Rock 1 destroyed. Move west to hide behind Rock 2.",
                    "timer_seconds": 4,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.2},
                        "aoes": [
                            {"shape": "circle", "cx": 0.15, "cy": 0.5, "r": 0.06, "color": "rgba(180,140,60,0.7)", "label": "Rock 2"},
                            {"shape": "circle", "cx": 0.85, "cy": 0.5, "r": 0.06, "color": "rgba(180,140,60,0.7)", "label": "Rock 3"},
                        ],
                    },
                    "explanation": "LoS behind the west rock for the second hit.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.1,  "y": 0.5}},
                        {"role": "HEALER", "correct_position": {"x": 0.1,  "y": 0.55}},
                        {"role": "MELEE",  "correct_position": {"x": 0.1,  "y": 0.45}},
                        {"role": "RANGED", "correct_position": {"x": 0.1,  "y": 0.55}},
                        {"role": "CASTER", "correct_position": {"x": 0.1,  "y": 0.5}},
                    ],
                },
            ],
        },

        # ── Phase 3 ──────────────────────────────────────────────────
        {
            "slug": "flatliner",
            "name": "Flatliner",
            "phase_name": "Phase 3",
            "description": (
                "The Tyrant knocks all players back from centre, splitting "
                "the arena into two halves. Resolve mechanics independently."
            ),
            "difficulty_rating": 5,
            "tags": ["knockback", "split", "towers", "tether"],
            "order": 13,
            "steps": [
                {
                    "order": 1,
                    "title": "Pre-position for Knockback",
                    "narration": (
                        "Stand on your assigned side (LP1 west, LP2 east) "
                        "near centre."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.5, "r": 0.08,
                             "color": "rgba(255,255,0,0.3)", "label": "Knockback Origin"},
                        ],
                    },
                    "explanation": "Tanks and Melee go west. Healers and Ranged go east.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.4,  "y": 0.5}},
                        {"role": "HEALER", "correct_position": {"x": 0.6,  "y": 0.5}},
                        {"role": "MELEE",  "correct_position": {"x": 0.38, "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.62, "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.62, "y": 0.5}},
                    ],
                },
                {
                    "order": 2,
                    "title": "Resolve Platform Mechanics",
                    "narration": "Soak your tower. Handle Fire Breath prey.",
                    "timer_seconds": 7,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.25, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.25, "cy": 0.3, "r": 0.08, "color": "rgba(0,180,255,0.5)", "label": "Tower W"},
                            {"shape": "circle", "cx": 0.75, "cy": 0.3, "r": 0.08, "color": "rgba(0,180,255,0.5)", "label": "Tower E"},
                        ],
                        "debuffs": [
                            {"label": "Fire Breath Prey (Closest 4)", "color": "#ff6b35"},
                        ],
                    },
                    "explanation": "Soak your tower and bait Fire Breath away from group.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.25, "y": 0.3}, "tolerance": 0.10},
                        {"role": "HEALER", "correct_position": {"x": 0.75, "y": 0.3}, "tolerance": 0.10},
                        {"role": "MELEE",  "correct_position": {"x": 0.25, "y": 0.7}},
                        {"role": "RANGED", "correct_position": {"x": 0.75, "y": 0.7}},
                        {"role": "CASTER", "correct_position": {"x": 0.75, "y": 0.7}},
                    ],
                },
            ],
        },
        {
            "slug": "majestic-meteor",
            "name": "Majestic Meteor",
            "phase_name": "Phase 3",
            "description": (
                "Towers spawn that need soaking. Portals redirect some tower "
                "positions. Check portal destinations."
            ),
            "difficulty_rating": 4,
            "tags": ["towers", "portals", "soak"],
            "order": 14,
            "steps": [
                {
                    "order": 1,
                    "title": "Soak Portal-Redirected Towers",
                    "narration": (
                        "Towers appear but some are redirected through portals. "
                        "Check where the portal sends your tower."
                    ),
                    "timer_seconds": 7,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.3, "cy": 0.3, "r": 0.09,
                             "color": "rgba(0,180,255,0.5)", "label": "Tower (via portal)"},
                            {"shape": "circle", "cx": 0.7, "cy": 0.7, "r": 0.09,
                             "color": "rgba(0,180,255,0.5)", "label": "Tower (via portal)"},
                        ],
                    },
                    "explanation": "Follow the portal to find where the tower actually resolves.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.3,  "y": 0.3}, "tolerance": 0.10},
                        {"role": "HEALER", "correct_position": {"x": 0.7,  "y": 0.7}, "tolerance": 0.10},
                        {"role": "MELEE",  "correct_position": {"x": 0.3,  "y": 0.3}, "tolerance": 0.10},
                        {"role": "RANGED", "correct_position": {"x": 0.7,  "y": 0.7}, "tolerance": 0.10},
                        {"role": "CASTER", "correct_position": {"x": 0.7,  "y": 0.7}, "tolerance": 0.10},
                    ],
                },
            ],
        },
        {
            "slug": "arcadion-avalanche",
            "name": "Arcadion Avalanche",
            "phase_name": "Phase 3",
            "description": (
                "The platform tilts and players slide. Position against "
                "the safe wall to avoid falling off."
            ),
            "difficulty_rating": 3,
            "tags": ["platform", "positioning"],
            "order": 15,
            "steps": [
                {
                    "order": 1,
                    "title": "Position Against Safe Wall",
                    "narration": "Platform tilts east. Brace against the west wall.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.25,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                    },
                    "explanation": "Stand against the west wall so you don't slide off the east edge.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.1,  "y": 0.4}},
                        {"role": "HEALER", "correct_position": {"x": 0.1,  "y": 0.6}},
                        {"role": "MELEE",  "correct_position": {"x": 0.1,  "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.15, "y": 0.7}},
                        {"role": "CASTER", "correct_position": {"x": 0.15, "y": 0.3}},
                    ],
                },
            ],
        },

        # ── Phase 4 ──────────────────────────────────────────────────
        {
            "slug": "ecliptic-stampede",
            "name": "Ecliptic Stampede",
            "phase_name": "Phase 4",
            "description": (
                "Complex multi-layer mechanic combining previous mechanics. "
                "Dodge sequential attacks while handling debuffs."
            ),
            "difficulty_rating": 5,
            "tags": ["complex", "sequential", "dodge", "debuff"],
            "order": 16,
            "steps": [
                {
                    "order": 1,
                    "title": "First Wave — Dodge + Spread",
                    "narration": (
                        "Multiple AoEs fire in sequence. Spread to clock "
                        "positions while dodging."
                    ),
                    "timer_seconds": 7,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "rect", "x": 0.0, "y": 0.0, "w": 0.5, "h": 0.5,
                             "color": "rgba(255,80,80,0.25)", "label": "Wave 1"},
                        ],
                        "debuffs": [
                            {"label": "Spread", "color": "#ff6b35"},
                        ],
                    },
                    "explanation": "Start at your clock spot in the safe quadrant, then rotate.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.75, "y": 0.6}},
                        {"role": "HEALER", "correct_position": {"x": 0.75, "y": 0.8}},
                        {"role": "MELEE",  "correct_position": {"x": 0.6,  "y": 0.75}},
                        {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.75}},
                        {"role": "CASTER", "correct_position": {"x": 0.85, "y": 0.9}},
                    ],
                },
                {
                    "order": 2,
                    "title": "Second Wave — Stack",
                    "narration": "Regroup for stack damage after the spread resolves.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "Stack", "color": "#2b7fff"},
                        ],
                    },
                    "explanation": "Regroup centre-south for the stack damage.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.7}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.7}},
                        {"role": "MELEE",  "correct_position": {"x": 0.45, "y": 0.7}},
                        {"role": "RANGED", "correct_position": {"x": 0.55, "y": 0.7}},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.72}},
                    ],
                },
            ],
        },
        {
            "slug": "heartbreak-kick",
            "name": "Heartbreak Kick (Enrage)",
            "phase_name": "Phase 4",
            "description": (
                "The Tyrant's enrage cast. Must kill the boss before the cast "
                "completes or it's a wipe."
            ),
            "difficulty_rating": 1,
            "tags": ["enrage", "dps-check"],
            "order": 17,
            "steps": [
                {
                    "order": 1,
                    "title": "DPS Check — Kill Before Enrage",
                    "action_type": "CHOICE",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                    },
                    "choices": [
                        {"id": "dps", "label": "Burn the boss — use all cooldowns"},
                        {"id": "panic", "label": "Panic"},
                    ],
                    "explanation": "Use all remaining burst. Potions, 2-minute buffs, everything.",
                    "role_variants": [
                        {"role": "TANK",   "correct_choice": "dps"},
                        {"role": "HEALER", "correct_choice": "dps"},
                        {"role": "MELEE",  "correct_choice": "dps"},
                        {"role": "RANGED", "correct_choice": "dps"},
                        {"role": "CASTER", "correct_choice": "dps"},
                    ],
                },
            ],
        },
    ],
}
