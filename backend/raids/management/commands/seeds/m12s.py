"""
Seed data for M12S — Lindwurm (AAC Heavyweight M4 Savage).

Door Boss + Final Boss as one Fight, distinguished by phase_name.
Door Boss (Acts 1-4): The Fixer → Mortal Slayer → Grotesquerie Act 1 →
    Ravenous Reach → Visceral Burst → Grotesquerie Act 2 → Roiling Mass →
    Grotesquerie Act 3 → Split Scourge → Curtain Call → Splattershed
Final Boss (Phases 1-4): Arcadia Aflame → Replication 1 → Snaking Kick →
    Double Sobat → Staging + Replication 2 → Firefall Splash →
    Blood Mana → Idyllic Dream → Twisted Vision
"""

M12S_FIGHT = {
    "slug": "m12s",
    "name": "AAC Heavyweight M4 (Savage)",
    "short_name": "M12S",
    "boss_name": "Lindwurm",
    "difficulty": "SAVAGE",
    "arena_shape": "CIRCLE",
    "order": 4,
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
            "slug": "mortal-slayer",
            "name": "Mortal Slayer",
            "phase_name": "Door Boss: Act 1",
            "description": (
                "Orbs spawn at the arena edge. Players bait them by standing "
                "closest to the orb they're assigned to intercept."
            ),
            "difficulty_rating": 3,
            "tags": ["bait", "orb", "spread"],
            "order": 2,
            "steps": [
                {
                    "order": 1,
                    "title": "Bait Your Assigned Orb",
                    "narration": (
                        "Orbs at N, E, S, W. Each player baits the orb at "
                        "their clock position."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.05, "r": 0.06, "color": "rgba(255,200,0,0.6)", "label": "Orb N"},
                            {"shape": "circle", "cx": 0.95, "cy": 0.5, "r": 0.06, "color": "rgba(255,200,0,0.6)", "label": "Orb E"},
                            {"shape": "circle", "cx": 0.5, "cy": 0.95, "r": 0.06, "color": "rgba(255,200,0,0.6)", "label": "Orb S"},
                            {"shape": "circle", "cx": 0.05, "cy": 0.5, "r": 0.06, "color": "rgba(255,200,0,0.6)", "label": "Orb W"},
                        ],
                    },
                    "explanation": "Stand near your assigned orb to intercept it.",
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
            "slug": "grotesquerie-act1",
            "name": "Grotesquerie: Act 1",
            "phase_name": "Door Boss: Act 1",
            "description": (
                "Players receive directed grotesquerie attachments that fire "
                "conal AoEs. Aim your cone away from the party."
            ),
            "difficulty_rating": 4,
            "tags": ["cone", "directional", "debuff"],
            "order": 3,
            "steps": [
                {
                    "order": 1,
                    "title": "Aim Your Directed Grotesquerie",
                    "narration": (
                        "Your cell points a direction — your cone fires that way. "
                        "Spread to clock positions with cone aimed outward."
                    ),
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
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.15}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.85}},
                        {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.85, "y": 0.15}},
                    ],
                },
            ],
        },
        {
            "slug": "ravenous-reach",
            "name": "Ravenous Reach",
            "phase_name": "Door Boss: Act 1",
            "description": (
                "Lindwurm extends an arm with a massive cone. Bait ground AoEs "
                "south, then dodge north away from the arm cone and puddles."
            ),
            "difficulty_rating": 3,
            "tags": ["bait", "puddle", "cone", "dodge"],
            "order": 4,
            "steps": [
                {
                    "order": 1,
                    "title": "Bait Ground AoEs South",
                    "narration": "Bait AoEs south, then move north.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.3, "cy": 0.7, "r": 0.08, "color": "rgba(255,80,80,0.4)", "label": "Bait AoE"},
                            {"shape": "circle", "cx": 0.7, "cy": 0.7, "r": 0.08, "color": "rgba(255,80,80,0.4)", "label": "Bait AoE"},
                        ],
                    },
                    "explanation": "Bait south, then dodge north.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.3,  "y": 0.7}},
                        {"role": "HEALER", "correct_position": {"x": 0.7,  "y": 0.7}},
                        {"role": "MELEE",  "correct_position": {"x": 0.4,  "y": 0.7}},
                        {"role": "RANGED", "correct_position": {"x": 0.6,  "y": 0.7}},
                        {"role": "CASTER", "correct_position": {"x": 0.6,  "y": 0.7}},
                    ],
                },
                {
                    "order": 2,
                    "title": "Dodge Arm Cone + Puddles",
                    "narration": "Arm cone fires south. Move north between puddles.",
                    "timer_seconds": 4,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "cone", "cx": 0.5, "cy": 0.5, "angle": 180, "spread": 90,
                             "color": "rgba(255,60,60,0.35)", "label": "Arm Cone"},
                            {"shape": "circle", "cx": 0.3, "cy": 0.7, "r": 0.12, "color": "rgba(160,0,200,0.3)", "label": "Puddle"},
                            {"shape": "circle", "cx": 0.7, "cy": 0.7, "r": 0.12, "color": "rgba(160,0,200,0.3)", "label": "Puddle"},
                        ],
                    },
                    "explanation": "Move north to avoid cone and expanding puddles.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.15}, "safe_zones": [{"x": 0.3, "y": 0.0, "w": 0.4, "h": 0.4}]},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.2},  "safe_zones": [{"x": 0.3, "y": 0.0, "w": 0.4, "h": 0.4}]},
                        {"role": "MELEE",  "correct_position": {"x": 0.4,  "y": 0.2},  "safe_zones": [{"x": 0.3, "y": 0.0, "w": 0.4, "h": 0.4}]},
                        {"role": "RANGED", "correct_position": {"x": 0.6,  "y": 0.15}, "safe_zones": [{"x": 0.3, "y": 0.0, "w": 0.4, "h": 0.4}]},
                        {"role": "CASTER", "correct_position": {"x": 0.55, "y": 0.2},  "safe_zones": [{"x": 0.3, "y": 0.0, "w": 0.4, "h": 0.4}]},
                    ],
                },
            ],
        },
        {
            "slug": "visceral-burst",
            "name": "Visceral Burst",
            "phase_name": "Door Boss: Act 2",
            "description": "Tankbuster. Tanks swap or use invulnerability.",
            "difficulty_rating": 2,
            "tags": ["tankbuster"],
            "order": 5,
            "steps": [
                {
                    "order": 1,
                    "title": "Tank Swap or Invuln",
                    "narration": "Heavy tankbuster. Swap or invuln.",
                    "timer_seconds": 4,
                    "action_type": "CHOICE",
                    "arena_state": {"boss_position": {"x": 0.5, "y": 0.5}},
                    "choices": [
                        {"id": "swap",  "label": "Tank swap (provoke)"},
                        {"id": "invuln", "label": "Use invulnerability"},
                    ],
                    "explanation": "Either swap aggro or use your invuln cooldown.",
                    "role_variants": [
                        {"role": "TANK",   "correct_choice": "swap"},
                        {"role": "HEALER", "correct_choice": "swap"},
                        {"role": "MELEE",  "correct_choice": "swap"},
                        {"role": "RANGED", "correct_choice": "swap"},
                        {"role": "CASTER", "correct_choice": "swap"},
                    ],
                },
            ],
        },
        {
            "slug": "grotesquerie-act2",
            "name": "Grotesquerie: Act 2 (Cruel Coil)",
            "phase_name": "Door Boss: Act 2",
            "description": (
                "Rotating conal AoEs around the boss. Find the safe sector "
                "and rotate with the pattern."
            ),
            "difficulty_rating": 4,
            "tags": ["rotation", "cone", "dodge"],
            "order": 6,
            "steps": [
                {
                    "order": 1,
                    "title": "Find Safe Sector",
                    "narration": (
                        "Cones rotate clockwise from the boss. "
                        "Start in the safe sector (south) and rotate with it."
                    ),
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
                    "explanation": "South is the safe sector. Rotate clockwise with the pattern.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.8}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.85}},
                        {"role": "MELEE",  "correct_position": {"x": 0.45, "y": 0.75}},
                        {"role": "RANGED", "correct_position": {"x": 0.55, "y": 0.85}},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.82}},
                    ],
                },
            ],
        },
        {
            "slug": "roiling-mass",
            "name": "Roiling Mass",
            "phase_name": "Door Boss: Act 2",
            "description": (
                "Towers spawn that must be soaked by the correct number of "
                "players. Assign pairs to each tower."
            ),
            "difficulty_rating": 3,
            "tags": ["towers", "soak"],
            "order": 7,
            "steps": [
                {
                    "order": 1,
                    "title": "Soak Assigned Tower",
                    "narration": "Towers at intercardinals. Two players per tower.",
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.25, "cy": 0.25, "r": 0.1, "color": "rgba(0,180,255,0.5)", "label": "Tower NW"},
                            {"shape": "circle", "cx": 0.75, "cy": 0.25, "r": 0.1, "color": "rgba(0,180,255,0.5)", "label": "Tower NE"},
                            {"shape": "circle", "cx": 0.25, "cy": 0.75, "r": 0.1, "color": "rgba(0,180,255,0.5)", "label": "Tower SW"},
                            {"shape": "circle", "cx": 0.75, "cy": 0.75, "r": 0.1, "color": "rgba(0,180,255,0.5)", "label": "Tower SE"},
                        ],
                    },
                    "explanation": "Two players per tower. Standard role assignments.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.25, "y": 0.25}, "tolerance": 0.10},
                        {"role": "HEALER", "correct_position": {"x": 0.75, "y": 0.75}, "tolerance": 0.10},
                        {"role": "MELEE",  "correct_position": {"x": 0.75, "y": 0.25}, "tolerance": 0.10},
                        {"role": "RANGED", "correct_position": {"x": 0.25, "y": 0.75}, "tolerance": 0.10},
                        {"role": "CASTER", "correct_position": {"x": 0.25, "y": 0.75}, "tolerance": 0.10},
                    ],
                },
            ],
        },
        {
            "slug": "grotesquerie-act3",
            "name": "Grotesquerie: Act 3",
            "phase_name": "Door Boss: Act 3",
            "description": (
                "Platform spread mechanic. Players receive debuffs and must "
                "spread to assigned platform positions."
            ),
            "difficulty_rating": 4,
            "tags": ["spread", "platform", "debuff"],
            "order": 8,
            "steps": [
                {
                    "order": 1,
                    "title": "Spread to Platform Positions",
                    "narration": "Each player takes their assigned platform position.",
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "Platform Assignment", "color": "#ff6b35"},
                        ],
                    },
                    "explanation": "Spread to your assigned position. Don't overlap.",
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
            "slug": "split-scourge",
            "name": "Split Scourge",
            "phase_name": "Door Boss: Act 3",
            "description": (
                "Dragon heads fire from multiple directions. Find the safe "
                "lane between the heads."
            ),
            "difficulty_rating": 3,
            "tags": ["line", "dodge"],
            "order": 9,
            "steps": [
                {
                    "order": 1,
                    "title": "Dodge Dragon Heads",
                    "narration": "Dragon heads fire from north and south. Stand east or west.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.25,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "rect", "x": 0.3, "y": 0.0, "w": 0.4, "h": 1.0,
                             "color": "rgba(255,80,80,0.3)", "label": "Dragon Head Line"},
                        ],
                    },
                    "explanation": "East and west sides are safe from the centre line attack.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.1,  "y": 0.5}},
                        {"role": "HEALER", "correct_position": {"x": 0.9,  "y": 0.5}},
                        {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.85, "y": 0.5}},
                    ],
                },
            ],
        },
        {
            "slug": "curtain-call",
            "name": "Curtain Call",
            "phase_name": "Door Boss: Act 4",
            "description": (
                "Cleanse mechanic. Players with debuffs must cleanse by "
                "standing in the purification zone."
            ),
            "difficulty_rating": 3,
            "tags": ["cleanse", "debuff"],
            "order": 10,
            "steps": [
                {
                    "order": 1,
                    "title": "Cleanse Your Debuff",
                    "narration": "Step into the purification zone to cleanse your debuff.",
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.5, "cy": 0.5, "r": 0.15,
                             "color": "rgba(255,255,255,0.4)", "label": "Purification Zone"},
                        ],
                        "debuffs": [
                            {"label": "Grotesquerie Debuff — Cleanse required", "color": "#cc44ff"},
                        ],
                    },
                    "explanation": "Stand in the white zone to cleanse. Move out after cleansing.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.5}, "tolerance": 0.15},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.5}, "tolerance": 0.15},
                        {"role": "MELEE",  "correct_position": {"x": 0.5,  "y": 0.5}, "tolerance": 0.15},
                        {"role": "RANGED", "correct_position": {"x": 0.5,  "y": 0.5}, "tolerance": 0.15},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.5}, "tolerance": 0.15},
                    ],
                },
            ],
        },
        {
            "slug": "splattershed",
            "name": "Splattershed",
            "phase_name": "Door Boss: Act 4",
            "description": (
                "Final door boss mechanic sequence. Multi-hit raidwide "
                "with splash damage. Mitigate heavily."
            ),
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
                    "explanation": "Multiple hits of raidwide. Use all available mitigation.",
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

        # ══════════════════════════════════════════════════════════════
        # Final Boss
        # ══════════════════════════════════════════════════════════════
        {
            "slug": "arcadia-aflame",
            "name": "Arcadia Aflame",
            "phase_name": "Final Boss: Phase 1",
            "description": "Transition raidwide into the final boss phase. Heavy damage.",
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
            "slug": "replication-1",
            "name": "Replication 1 (8 Clones)",
            "phase_name": "Final Boss: Phase 1",
            "description": (
                "Lindwurm summons 8 clones that cast cone attacks in sequence. "
                "Read the clone telegraphs and find the safe zone."
            ),
            "difficulty_rating": 4,
            "tags": ["clone", "cone", "dodge", "sequential"],
            "order": 13,
            "steps": [
                {
                    "order": 1,
                    "title": "Dodge Clone Cones — Wave 1",
                    "narration": (
                        "Clones appear at cardinal positions. Each fires a cone "
                        "in the direction they face. Find the safe zone."
                    ),
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
                    "explanation": "South-centre is safe from all three clone cones.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.8},  "safe_zones": [{"shape": "circle", "cx": 0.5, "cy": 0.8, "r": 0.2}]},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.85}, "safe_zones": [{"shape": "circle", "cx": 0.5, "cy": 0.8, "r": 0.2}]},
                        {"role": "MELEE",  "correct_position": {"x": 0.45, "y": 0.75}, "safe_zones": [{"shape": "circle", "cx": 0.5, "cy": 0.8, "r": 0.2}]},
                        {"role": "RANGED", "correct_position": {"x": 0.55, "y": 0.85}, "safe_zones": [{"shape": "circle", "cx": 0.5, "cy": 0.8, "r": 0.2}]},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.82}, "safe_zones": [{"shape": "circle", "cx": 0.5, "cy": 0.8, "r": 0.2}]},
                    ],
                },
            ],
        },
        {
            "slug": "snaking-kick",
            "name": "Snaking Kick",
            "phase_name": "Final Boss: Phase 1",
            "description": (
                "Lindwurm kicks — get behind the boss to avoid the frontal "
                "cleave."
            ),
            "difficulty_rating": 2,
            "tags": ["cleave", "dodge"],
            "order": 14,
            "steps": [
                {
                    "order": 1,
                    "title": "Get Behind Boss",
                    "narration": "Frontal cleave. Move behind the boss.",
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
                    "explanation": "Stand behind the boss. The entire front half is dangerous.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.7}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.75}},
                        {"role": "MELEE",  "correct_position": {"x": 0.45, "y": 0.65}},
                        {"role": "RANGED", "correct_position": {"x": 0.55, "y": 0.8}},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.75}},
                    ],
                },
            ],
        },
        {
            "slug": "double-sobat",
            "name": "Double Sobat",
            "phase_name": "Final Boss: Phase 1",
            "description": (
                "Shared tankbuster targeting both tanks. Tanks must stack "
                "together, party stays away."
            ),
            "difficulty_rating": 2,
            "tags": ["tankbuster", "shared"],
            "order": 15,
            "steps": [
                {
                    "order": 1,
                    "title": "Tanks Stack, Party Away",
                    "narration": "Shared tankbuster. Tanks stack north, party south.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "default_tolerance": 0.18,
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                    },
                    "explanation": "Tanks share the hit north. Everyone else stays south.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.2}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.75}},
                        {"role": "MELEE",  "correct_position": {"x": 0.5,  "y": 0.7}},
                        {"role": "RANGED", "correct_position": {"x": 0.5,  "y": 0.8}},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.8}},
                    ],
                },
            ],
        },
        {
            "slug": "staging-replication-2",
            "name": "Staging + Replication 2",
            "phase_name": "Final Boss: Phase 2",
            "description": (
                "Player clones appear and replicate your previous movements. "
                "Position carefully — your clone will mirror you."
            ),
            "difficulty_rating": 5,
            "tags": ["clone", "mirror", "positioning"],
            "order": 16,
            "steps": [
                {
                    "order": 1,
                    "title": "Position for Clone Replay",
                    "narration": (
                        "Your clone will replay your movements. Position so "
                        "the replay doesn't hit anyone."
                    ),
                    "timer_seconds": 7,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "debuffs": [
                            {"label": "Clone Recording — Position carefully", "color": "#cc44ff"},
                        ],
                    },
                    "explanation": "Your clone replays at the mirrored position. Account for the mirror.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.25, "y": 0.25}},
                        {"role": "HEALER", "correct_position": {"x": 0.75, "y": 0.75}},
                        {"role": "MELEE",  "correct_position": {"x": 0.25, "y": 0.75}},
                        {"role": "RANGED", "correct_position": {"x": 0.75, "y": 0.25}},
                        {"role": "CASTER", "correct_position": {"x": 0.75, "y": 0.25}},
                    ],
                },
            ],
        },
        {
            "slug": "firefall-splash",
            "name": "Firefall Splash",
            "phase_name": "Final Boss: Phase 2",
            "description": (
                "Fire AoEs drop from above in sequence. Dodge each landing "
                "zone as they appear."
            ),
            "difficulty_rating": 3,
            "tags": ["aoe", "sequential", "dodge"],
            "order": 17,
            "steps": [
                {
                    "order": 1,
                    "title": "Dodge Sequential Fire AoEs",
                    "narration": "Fire drops in sequence: NW → NE → SW → SE. Start SE.",
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
                    "explanation": "Start in the last-to-resolve corner (SE), then rotate.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.75, "y": 0.75}},
                        {"role": "HEALER", "correct_position": {"x": 0.8,  "y": 0.8}},
                        {"role": "MELEE",  "correct_position": {"x": 0.7,  "y": 0.7}},
                        {"role": "RANGED", "correct_position": {"x": 0.8,  "y": 0.75}},
                        {"role": "CASTER", "correct_position": {"x": 0.75, "y": 0.8}},
                    ],
                },
            ],
        },
        {
            "slug": "blood-mana",
            "name": "Blood Mana",
            "phase_name": "Final Boss: Phase 3",
            "description": (
                "Shape-soaking mechanic. Different shapes appear that require "
                "specific numbers of players to soak."
            ),
            "difficulty_rating": 4,
            "tags": ["soak", "shapes"],
            "order": 18,
            "steps": [
                {
                    "order": 1,
                    "title": "Soak Your Assigned Shape",
                    "narration": (
                        "Circle = 1 player, triangle = 3 players. "
                        "Soak based on your assignment."
                    ),
                    "timer_seconds": 6,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.3, "cy": 0.5, "r": 0.08,
                             "color": "rgba(200,0,0,0.4)", "label": "Circle (1 player)"},
                            {"shape": "circle", "cx": 0.7, "cy": 0.5, "r": 0.15,
                             "color": "rgba(200,0,0,0.4)", "label": "Triangle (3 players)"},
                        ],
                    },
                    "explanation": "Match the correct number of players to each shape.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.3,  "y": 0.5}, "tolerance": 0.10},
                        {"role": "HEALER", "correct_position": {"x": 0.7,  "y": 0.5}, "tolerance": 0.15},
                        {"role": "MELEE",  "correct_position": {"x": 0.7,  "y": 0.5}, "tolerance": 0.15},
                        {"role": "RANGED", "correct_position": {"x": 0.7,  "y": 0.5}, "tolerance": 0.15},
                        {"role": "CASTER", "correct_position": {"x": 0.3,  "y": 0.5}, "tolerance": 0.10},
                    ],
                },
            ],
        },
        {
            "slug": "idyllic-dream",
            "name": "Idyllic Dream + Downfall",
            "phase_name": "Final Boss: Phase 3",
            "description": (
                "Arena splits into platforms with elemental towers. "
                "Dark towers = soak, Wind towers = use KB immunity."
            ),
            "difficulty_rating": 5,
            "tags": ["towers", "platform", "elemental", "soak"],
            "order": 19,
            "steps": [
                {
                    "order": 1,
                    "title": "Identify Tower Type",
                    "narration": (
                        "Dark towers must be soaked. Wind towers knock back. "
                        "Check the element."
                    ),
                    "timer_seconds": 6,
                    "action_type": "CHOICE",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.3, "cy": 0.5, "r": 0.08, "color": "rgba(80,0,160,0.5)", "label": "Dark Tower"},
                            {"shape": "circle", "cx": 0.7, "cy": 0.5, "r": 0.08, "color": "rgba(0,200,100,0.5)", "label": "Wind Tower"},
                        ],
                        "debuffs": [
                            {"label": "Dark Tower — Soak required", "color": "#6600cc"},
                            {"label": "Wind Tower — Knockback", "color": "#00cc66"},
                        ],
                    },
                    "choices": [
                        {"id": "soak",  "label": "Soak the Dark Tower"},
                        {"id": "avoid", "label": "Avoid the Wind Tower (use KB immunity)"},
                    ],
                    "explanation": "Dark = soak. Wind = KB immunity or position against wall.",
                    "role_variants": [
                        {"role": "TANK",   "correct_choice": "soak"},
                        {"role": "HEALER", "correct_choice": "soak"},
                        {"role": "MELEE",  "correct_choice": "soak"},
                        {"role": "RANGED", "correct_choice": "avoid"},
                        {"role": "CASTER", "correct_choice": "avoid"},
                    ],
                },
                {
                    "order": 2,
                    "title": "Resolve Towers",
                    "narration": "Soakers stand in tower. KB players brace against wall.",
                    "timer_seconds": 5,
                    "action_type": "POSITION",
                    "arena_state": {
                        "boss_position": {"x": 0.5, "y": 0.5},
                        "aoes": [
                            {"shape": "circle", "cx": 0.3, "cy": 0.5, "r": 0.1, "color": "rgba(80,0,160,0.5)", "label": "Dark Tower (Soak)"},
                            {"shape": "circle", "cx": 0.7, "cy": 0.5, "r": 0.1, "color": "rgba(0,200,100,0.4)", "label": "Wind Tower (KB)"},
                        ],
                    },
                    "explanation": "Soakers in the Dark tower. KB players at the wall.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.3,  "y": 0.5}, "tolerance": 0.10},
                        {"role": "HEALER", "correct_position": {"x": 0.3,  "y": 0.5}, "tolerance": 0.10},
                        {"role": "MELEE",  "correct_position": {"x": 0.3,  "y": 0.5}, "tolerance": 0.10},
                        {"role": "RANGED", "correct_position": {"x": 0.7,  "y": 0.85}},
                        {"role": "CASTER", "correct_position": {"x": 0.7,  "y": 0.85}},
                    ],
                },
            ],
        },
        {
            "slug": "twisted-vision",
            "name": "Twisted Vision",
            "phase_name": "Final Boss: Phase 4",
            "description": (
                "Lindwurm replays memorized patterns from earlier in the fight. "
                "Remember and dodge each pattern in sequence."
            ),
            "difficulty_rating": 5,
            "tags": ["memory", "pattern", "sequential", "dodge"],
            "order": 20,
            "steps": [
                {
                    "order": 1,
                    "title": "Recall Pattern 1 — Dodge",
                    "narration": (
                        "First memorized pattern replays. This was the cardinal "
                        "cone pattern — stand at intercardinals."
                    ),
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
                    "explanation": "Remember: this was the cardinal cone pattern. Intercardinals safe.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.15, "y": 0.15}},
                        {"role": "HEALER", "correct_position": {"x": 0.85, "y": 0.85}},
                        {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.85}},
                        {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.15}},
                        {"role": "CASTER", "correct_position": {"x": 0.85, "y": 0.85}},
                    ],
                },
                {
                    "order": 2,
                    "title": "Recall Pattern 2 — Dodge",
                    "narration": (
                        "Second pattern replays. This was the intercardinal cone "
                        "pattern — stand at cardinals."
                    ),
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
                    "explanation": "Intercardinal cones — stand at cardinals.",
                    "role_variants": [
                        {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.15}},
                        {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.85}},
                        {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.5}},
                        {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.5}},
                        {"role": "CASTER", "correct_position": {"x": 0.5,  "y": 0.85}},
                    ],
                },
            ],
        },
    ],
}
