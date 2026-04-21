"""
Seed data for Futures Rewritten (Ultimate).

Fight: FRU — Fatebreaker / Usurper of Frost.
"""

FRU_TIER = {
    "tier": {
        "slug": "futures-rewritten",
        "name": "Futures Rewritten",
        "expansion": "Dawntrail",
        "patch": "7.1",
        "order": 2,
    },
    "fights": [
        {
            "slug": "fru",
            "name": "Futures Rewritten (Ultimate)",
            "short_name": "FRU",
            "boss_name": "Fatebreaker / Usurper of Frost",
            "difficulty": "ULTIMATE",
            "arena_shape": "SQUARE",
            "order": 1,
            "mechanics": [
                {
                    "slug": "cyclonic-break",
                    "name": "Cyclonic Break",
                    "phase_name": "P1: Fatebreaker",
                    "description": "Lightning = spread, Blizzard = stack. Debuffs swap after first hit.",
                    "difficulty_rating": 4,
                    "tags": ["debuff", "spread", "stack", "lightning", "ice"],
                    "order": 1,
                    "steps": [
                        {
                            "order": 1,
                            "title": "Check Elemental Debuff",
                            "narration": "Lightning → spread to cardinals. Blizzard → stack in corners with tanks.",
                            "timer_seconds": 6,
                            "action_type": "POSITION",
                            "arena_state": {
                                "boss_position": {"x": 0.5, "y": 0.3},
                                "debuffs": [
                                    {"label": "⚡ Lightning → Spread", "color": "#ffe066"},
                                    {"label": "❄ Blizzard → Stack", "color": "#80d4ff"},
                                ],
                            },
                            "explanation": "Lightning takes outer cardinals. Blizzard stacks in corners.",
                            "role_variants": [
                                {"role": "TANK",   "correct_position": {"x": 0.5,  "y": 0.2}},
                                {"role": "HEALER", "correct_position": {"x": 0.5,  "y": 0.8}},
                                {"role": "MELEE",  "correct_position": {"x": 0.15, "y": 0.5}},
                                {"role": "RANGED", "correct_position": {"x": 0.85, "y": 0.5}},
                            ],
                        },
                        {
                            "order": 2,
                            "title": "Second Hit — Swap Roles",
                            "narration": "Debuffs swap. Previous spreaders now stack; stackers spread.",
                            "timer_seconds": 5,
                            "action_type": "POSITION",
                            "arena_state": {
                                "boss_position": {"x": 0.5, "y": 0.3},
                            },
                            "explanation": "Swap positions after debuff swap.",
                            "role_variants": [
                                {"role": "TANK",   "correct_position": {"x": 0.15, "y": 0.15}},
                                {"role": "HEALER", "correct_position": {"x": 0.85, "y": 0.85}},
                                {"role": "MELEE",  "correct_position": {"x": 0.5,  "y": 0.8}},
                                {"role": "RANGED", "correct_position": {"x": 0.5,  "y": 0.2}},
                            ],
                        },
                    ],
                },
                {
                    "slug": "diamond-dust",
                    "name": "Diamond Dust",
                    "phase_name": "P2: Usurper of Frost",
                    "description": "Arena covered in ice. Stand on small safe platforms based on debuff type.",
                    "difficulty_rating": 5,
                    "tags": ["ice", "platform", "debuff", "ultimate"],
                    "order": 2,
                    "steps": [
                        {
                            "order": 1,
                            "title": "Pre-position for Ice Platforms",
                            "narration": "Only 4 platforms remain safe. Pairs share a platform.",
                            "timer_seconds": 10,
                            "action_type": "POSITION",
                            "arena_state": {
                                "boss_position": {"x": 0.5, "y": 0.5},
                                "aoes": [
                                    {"shape": "rect", "x": 0.0, "y": 0.0, "w": 1.0, "h": 1.0,
                                     "color": "rgba(150,220,255,0.3)", "label": "Ice Floor"},
                                    {"shape": "circle", "cx": 0.25, "cy": 0.25, "r": 0.08,
                                     "color": "rgba(255,255,255,0.7)", "label": "Platform"},
                                    {"shape": "circle", "cx": 0.75, "cy": 0.25, "r": 0.08,
                                     "color": "rgba(255,255,255,0.7)", "label": "Platform"},
                                    {"shape": "circle", "cx": 0.25, "cy": 0.75, "r": 0.08,
                                     "color": "rgba(255,255,255,0.7)", "label": "Platform"},
                                    {"shape": "circle", "cx": 0.75, "cy": 0.75, "r": 0.08,
                                     "color": "rgba(255,255,255,0.7)", "label": "Platform"},
                                ],
                            },
                            "explanation": "Each pair takes one platform. Off-platform = death.",
                            "role_variants": [
                                {
                                    "role": "TANK",
                                    "correct_position": {"x": 0.25, "y": 0.25},
                                    "tolerance": 0.10,
                                    "safe_zones": [
                                        {"shape": "circle", "cx": 0.25, "cy": 0.25, "r": 0.08},
                                        {"shape": "circle", "cx": 0.75, "cy": 0.25, "r": 0.08},
                                        {"shape": "circle", "cx": 0.25, "cy": 0.75, "r": 0.08},
                                        {"shape": "circle", "cx": 0.75, "cy": 0.75, "r": 0.08},
                                    ],
                                },
                                {"role": "HEALER", "correct_position": {"x": 0.75, "y": 0.75}, "tolerance": 0.10},
                                {"role": "MELEE",  "correct_position": {"x": 0.75, "y": 0.25}, "tolerance": 0.10},
                                {"role": "RANGED", "correct_position": {"x": 0.25, "y": 0.75}, "tolerance": 0.10},
                            ],
                        },
                    ],
                },
            ],
        },
    ],
}
