"""
Management command to seed the database with M1S–M4S (AAC Light-heavyweight)
and FRU (Futures Rewritten Ultimate) mechanics.

Run: python manage.py seed_mechanics
"""
from django.core.management.base import BaseCommand
from raids.models import Fight, Phase, Mechanic, MechanicStep


SEED_DATA = [
    # ─────────────────────────────────────────────────────────────────────────
    # M1S — Black Cat
    # ─────────────────────────────────────────────────────────────────────────
    {
        'slug': 'm1s',
        'name': 'AAC Light-heavyweight M1 (Savage)',
        'short_name': 'M1S',
        'boss_name': 'Black Cat',
        'difficulty': 'SAVAGE',
        'tier': 'AAC Light-heavyweight',
        'patch': '7.0',
        'arena_shape': 'SQUARE',
        'order': 1,
        'phases': [
            {
                'name': 'Phase 1',
                'order': 1,
                'description': 'Opening rotation with Leaping One-two Paw and Nailchipper.',
                'mechanics': [
                    {
                        'name': 'Leaping One-two Paw',
                        'slug': 'leaping-one-two-paw',
                        'description': 'Boss leaps to a cardinal/intercardinal, then cleaves both sides sequentially. '
                                       'Identify the safe side from the claw telegraph.',
                        'difficulty_rating': 2,
                        'applicable_roles': [],
                        'tags': ['cleave', 'dodge'],
                        'order': 1,
                        'steps': [
                            {
                                'order': 1,
                                'title': 'Identify the Leap Direction',
                                'narration': 'Black Cat leaps to a cardinal. '
                                             'Watch which paw she raises — it telegraphs the FIRST cleave side.',
                                'timer_seconds': 5,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.1},
                                    'boss_facing': 'south',
                                    'aoes': [
                                        {'shape': 'rect', 'x': 0.0, 'y': 0.0, 'w': 0.5, 'h': 1.0,
                                         'color': 'rgba(255,80,80,0.35)', 'label': 'First Cleave (Left)'},
                                    ],
                                    'safe_hint': 'right',
                                },
                                'correct_positions': {
                                    'TANK':    {'x': 0.75, 'y': 0.5},
                                    'HEALER':  {'x': 0.75, 'y': 0.7},
                                    'MELEE':   {'x': 0.75, 'y': 0.5},
                                    'RANGED':  {'x': 0.8,  'y': 0.5},
                                    'CASTER':  {'x': 0.8,  'y': 0.5},
                                },
                                'explanation': 'Step right to avoid the first (left-side) cleave. '
                                               'Be ready to immediately move left for the follow-up.',
                                'safe_zones': [{'x': 0.5, 'y': 0.0, 'w': 0.5, 'h': 1.0}],
                            },
                            {
                                'order': 2,
                                'title': 'Second Cleave — Swap Sides',
                                'narration': 'The second cleave hits the opposite side. Move through the boss to safety.',
                                'timer_seconds': 4,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.1},
                                    'boss_facing': 'south',
                                    'aoes': [
                                        {'shape': 'rect', 'x': 0.5, 'y': 0.0, 'w': 0.5, 'h': 1.0,
                                         'color': 'rgba(255,80,80,0.35)', 'label': 'Second Cleave (Right)'},
                                    ],
                                },
                                'correct_positions': {
                                    'TANK':    {'x': 0.25, 'y': 0.5},
                                    'HEALER':  {'x': 0.25, 'y': 0.7},
                                    'MELEE':   {'x': 0.25, 'y': 0.5},
                                    'RANGED':  {'x': 0.2,  'y': 0.5},
                                    'CASTER':  {'x': 0.2,  'y': 0.5},
                                },
                                'explanation': 'Cross through the boss to the left side before the second cleave lands.',
                                'safe_zones': [{'x': 0.0, 'y': 0.0, 'w': 0.5, 'h': 1.0}],
                            },
                        ],
                    },
                    {
                        'name': 'Nailchipper (Spread)',
                        'slug': 'nailchipper-spread',
                        'description': 'Eight individual AoEs — one on each player. Spread to designated spots.',
                        'difficulty_rating': 2,
                        'applicable_roles': [],
                        'tags': ['spread', 'aoe'],
                        'order': 2,
                        'steps': [
                            {
                                'order': 1,
                                'title': 'Spread to Assigned Positions',
                                'narration': 'Nailchipper fires an AoE at every player simultaneously. '
                                             'Use the standard 8-way spread: Tanks N/S, Healers NE/SW, '
                                             'Melee NW/SE, Ranged/Casters E/W.',
                                'timer_seconds': 6,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.5},
                                    'aoes': [
                                        {'shape': 'circle', 'cx': 0.5, 'cy': 0.5, 'r': 0.08,
                                         'color': 'rgba(255,200,0,0.5)', 'label': 'AoE (each player)'},
                                    ],
                                    'markers': [
                                        {'id': 'A', 'x': 0.5, 'y': 0.05},
                                        {'id': 'B', 'x': 0.95, 'y': 0.5},
                                        {'id': 'C', 'x': 0.5, 'y': 0.95},
                                        {'id': 'D', 'x': 0.05, 'y': 0.5},
                                    ],
                                },
                                'correct_positions': {
                                    'TANK':    {'x': 0.5,  'y': 0.15},
                                    'HEALER':  {'x': 0.15, 'y': 0.85},
                                    'MELEE':   {'x': 0.15, 'y': 0.15},
                                    'RANGED':  {'x': 0.85, 'y': 0.5},
                                    'CASTER':  {'x': 0.85, 'y': 0.5},
                                },
                                'explanation': 'Spread far apart. MT/OT take North; Healers take SW and NE diagonals; '
                                               'Melee take NW/SE diagonals; Ranged/Caster take East/West.',
                                'safe_zones': [],
                            },
                        ],
                    },
                    {
                        'name': 'Mouser (Limit Cut)',
                        'slug': 'mouser-limit-cut',
                        'description': 'Numbered limit-cut AoEs — players explode in order 1→4. '
                                       'Pairs share the explosion. Requires memorising your number.',
                        'difficulty_rating': 4,
                        'applicable_roles': [],
                        'tags': ['limit-cut', 'spread', 'numbered'],
                        'order': 3,
                        'steps': [
                            {
                                'order': 1,
                                'title': 'Check Your Number',
                                'narration': 'Overhead numbers 1–4 appear on two players each. '
                                             'Numbers 1 & 3 go North. Numbers 2 & 4 go South.',
                                'timer_seconds': 5,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.5},
                                    'debuffs': [
                                        {'label': '#1', 'color': '#fff'},
                                        {'label': '#2', 'color': '#fff'},
                                        {'label': '#3', 'color': '#fff'},
                                        {'label': '#4', 'color': '#fff'},
                                    ],
                                },
                                'correct_positions': {
                                    'ANY': {'x': 0.5, 'y': 0.2},
                                },
                                'explanation': 'Odd numbers (1,3) stack North. Even numbers (2,4) stack South. '
                                               'Resolve in order with brief gaps between explosions.',
                                'safe_zones': [],
                            },
                        ],
                    },
                ],
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # M2S — Honey B. Lovely
    # ─────────────────────────────────────────────────────────────────────────
    {
        'slug': 'm2s',
        'name': 'AAC Light-heavyweight M2 (Savage)',
        'short_name': 'M2S',
        'boss_name': 'Honey B. Lovely',
        'difficulty': 'SAVAGE',
        'tier': 'AAC Light-heavyweight',
        'patch': '7.0',
        'arena_shape': 'CIRCLE',
        'order': 2,
        'phases': [
            {
                'name': 'Phase 1',
                'order': 1,
                'description': 'Honey B. Lovely\'s opening mechanics with towers and stacks.',
                'mechanics': [
                    {
                        'name': 'Honey B. Bombing',
                        'slug': 'honey-b-bombing',
                        'description': 'Pink AoE circles drop on the arena in a pattern. '
                                       'Players must stand in the remaining safe spots.',
                        'difficulty_rating': 3,
                        'applicable_roles': [],
                        'tags': ['aoe', 'dodge', 'pattern'],
                        'order': 1,
                        'steps': [
                            {
                                'order': 1,
                                'title': 'Identify Safe Columns',
                                'narration': 'Pink "Love" circles fill most of the arena in a checkerboard. '
                                             'Find a safe square and stand in it.',
                                'timer_seconds': 6,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.5},
                                    'aoes': [
                                        {'shape': 'circle', 'cx': 0.25, 'cy': 0.25, 'r': 0.18, 'color': 'rgba(255,100,180,0.5)'},
                                        {'shape': 'circle', 'cx': 0.75, 'cy': 0.25, 'r': 0.18, 'color': 'rgba(255,100,180,0.5)'},
                                        {'shape': 'circle', 'cx': 0.25, 'cy': 0.75, 'r': 0.18, 'color': 'rgba(255,100,180,0.5)'},
                                        {'shape': 'circle', 'cx': 0.75, 'cy': 0.75, 'r': 0.18, 'color': 'rgba(255,100,180,0.5)'},
                                    ],
                                },
                                'correct_positions': {
                                    'TANK':    {'x': 0.5, 'y': 0.5},
                                    'HEALER':  {'x': 0.5, 'y': 0.5},
                                    'MELEE':   {'x': 0.5, 'y': 0.5},
                                    'RANGED':  {'x': 0.5, 'y': 0.5},
                                    'CASTER':  {'x': 0.5, 'y': 0.5},
                                },
                                'explanation': 'Stand in the centre or the gaps between bombs. '
                                               'The centre cross is always safe in this pattern.',
                                'safe_zones': [{'shape': 'cross', 'cx': 0.5, 'cy': 0.5}],
                            },
                        ],
                    },
                    {
                        'name': 'Alarm Pheromones (Stack/Spread)',
                        'slug': 'alarm-pheromones',
                        'description': 'Debuffs split the party: hearts (stack) and bee icons (spread). '
                                       'React to your debuff icon.',
                        'difficulty_rating': 3,
                        'applicable_roles': [],
                        'tags': ['spread', 'stack', 'debuff'],
                        'order': 2,
                        'steps': [
                            {
                                'order': 1,
                                'title': 'React to Your Debuff',
                                'narration': 'Heart debuff = stack with your partner. '
                                             'Bee debuff = spread far apart.',
                                'timer_seconds': 5,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.5},
                                    'debuffs': [
                                        {'label': '♥ Stack', 'color': '#ff69b4'},
                                        {'label': '🐝 Spread', 'color': '#ffd700'},
                                    ],
                                },
                                'correct_positions': {
                                    'TANK':    {'x': 0.5, 'y': 0.2},
                                    'HEALER':  {'x': 0.5, 'y': 0.2},
                                    'MELEE':   {'x': 0.15, 'y': 0.5},
                                    'RANGED':  {'x': 0.85, 'y': 0.5},
                                    'CASTER':  {'x': 0.5, 'y': 0.8},
                                },
                                'explanation': 'Heart players stack North/South. Bee players spread East/West. '
                                               'Keep distance to avoid clipping others.',
                                'safe_zones': [],
                            },
                        ],
                    },
                ],
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # M3S — Brute Bomber
    # ─────────────────────────────────────────────────────────────────────────
    {
        'slug': 'm3s',
        'name': 'AAC Light-heavyweight M3 (Savage)',
        'short_name': 'M3S',
        'boss_name': 'Brute Bomber',
        'difficulty': 'SAVAGE',
        'tier': 'AAC Light-heavyweight',
        'patch': '7.0',
        'arena_shape': 'SQUARE',
        'order': 3,
        'phases': [
            {
                'name': 'Phase 1',
                'order': 1,
                'description': 'Brute Bomber\'s opening combination attacks and tethers.',
                'mechanics': [
                    {
                        'name': 'Brutal Impact (Towers)',
                        'slug': 'brutal-impact-towers',
                        'description': 'Towers spawn across the arena. Each must be soaked by a specific number of players. '
                                       'Unsoaked towers kill the group.',
                        'difficulty_rating': 3,
                        'applicable_roles': [],
                        'tags': ['towers', 'soak'],
                        'order': 1,
                        'steps': [
                            {
                                'order': 1,
                                'title': 'Identify Your Tower',
                                'narration': 'Four towers spawn (NE, NW, SE, SW). '
                                             'Pair assignments: MT+H1 NE, OT+H2 NW, M1+M2 SE, R1+C1 SW.',
                                'timer_seconds': 8,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.5},
                                    'aoes': [
                                        {'shape': 'circle', 'cx': 0.75, 'cy': 0.25, 'r': 0.1, 'color': 'rgba(0,180,255,0.5)', 'label': 'Tower NE'},
                                        {'shape': 'circle', 'cx': 0.25, 'cy': 0.25, 'r': 0.1, 'color': 'rgba(0,180,255,0.5)', 'label': 'Tower NW'},
                                        {'shape': 'circle', 'cx': 0.75, 'cy': 0.75, 'r': 0.1, 'color': 'rgba(0,180,255,0.5)', 'label': 'Tower SE'},
                                        {'shape': 'circle', 'cx': 0.25, 'cy': 0.75, 'r': 0.1, 'color': 'rgba(0,180,255,0.5)', 'label': 'Tower SW'},
                                    ],
                                },
                                'correct_positions': {
                                    'TANK':    {'x': 0.75, 'y': 0.25},
                                    'HEALER':  {'x': 0.75, 'y': 0.25},
                                    'MELEE':   {'x': 0.75, 'y': 0.75},
                                    'RANGED':  {'x': 0.25, 'y': 0.75},
                                    'CASTER':  {'x': 0.25, 'y': 0.75},
                                },
                                'explanation': 'Each pair soaks their assigned tower. '
                                               'Two players per tower prevents lethal damage.',
                                'safe_zones': [],
                            },
                        ],
                    },
                    {
                        'name': 'Chain Deathmatch (Tethers)',
                        'slug': 'chain-deathmatch',
                        'description': 'Tethers connect random pairs of players. '
                                       'The tether stretches — move apart to break damage, '
                                       'but not too far or you\'ll be yanked.',
                        'difficulty_rating': 4,
                        'applicable_roles': [],
                        'tags': ['tether', 'distance'],
                        'order': 2,
                        'steps': [
                            {
                                'order': 1,
                                'title': 'Stretch the Tether',
                                'narration': 'Tethers appear between four pairs. '
                                             'Stretch to half-arena distance. Too close = heavy damage; '
                                             'too far = yank.',
                                'timer_seconds': 7,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.5},
                                    'tethers': [
                                        {'from': {'x': 0.5, 'y': 0.3}, 'to': {'x': 0.5, 'y': 0.7}, 'color': '#ff9900'},
                                    ],
                                },
                                'correct_positions': {
                                    'TANK':   {'x': 0.5, 'y': 0.15},
                                    'HEALER': {'x': 0.5, 'y': 0.85},
                                    'MELEE':  {'x': 0.15, 'y': 0.5},
                                    'RANGED': {'x': 0.85, 'y': 0.5},
                                    'CASTER': {'x': 0.85, 'y': 0.5},
                                },
                                'explanation': 'Move to your designated outer position. '
                                               'Stay on your assigned cardinal/intercardinal to keep the tether clean.',
                                'safe_zones': [],
                            },
                        ],
                    },
                ],
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # M4S — Wicked Thunder
    # ─────────────────────────────────────────────────────────────────────────
    {
        'slug': 'm4s',
        'name': 'AAC Light-heavyweight M4 (Savage)',
        'short_name': 'M4S',
        'boss_name': 'Wicked Thunder',
        'difficulty': 'SAVAGE',
        'tier': 'AAC Light-heavyweight',
        'patch': '7.0',
        'arena_shape': 'SQUARE',
        'order': 4,
        'phases': [
            {
                'name': 'Phase 1',
                'order': 1,
                'description': 'Wicked Thunder\'s electrifying openers.',
                'mechanics': [
                    {
                        'name': 'Witch Hunt',
                        'slug': 'witch-hunt',
                        'description': 'Odd and even debuffs rotate around a fixed axis. '
                                       'Players must resolve their debuffs in the correct order.',
                        'difficulty_rating': 5,
                        'applicable_roles': [],
                        'tags': ['debuff', 'rotation', 'spread'],
                        'order': 1,
                        'steps': [
                            {
                                'order': 1,
                                'title': 'Identify Debuff Parity',
                                'narration': 'Check your Thunder debuff number (1/2/3/4). '
                                             'Odd numbers go to the left intercardinals, '
                                             'even numbers go to the right.',
                                'timer_seconds': 8,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.5},
                                    'debuffs': [
                                        {'label': 'Thunder #1 (Odd)', 'color': '#a0e0ff'},
                                        {'label': 'Thunder #2 (Even)', 'color': '#ffd080'},
                                    ],
                                    'markers': [
                                        {'id': 'A', 'x': 0.5, 'y': 0.05},
                                        {'id': 'B', 'x': 0.95, 'y': 0.5},
                                        {'id': 'C', 'x': 0.5, 'y': 0.95},
                                        {'id': 'D', 'x': 0.05, 'y': 0.5},
                                    ],
                                },
                                'correct_positions': {
                                    'TANK':    {'x': 0.15, 'y': 0.15},
                                    'HEALER':  {'x': 0.85, 'y': 0.85},
                                    'MELEE':   {'x': 0.15, 'y': 0.85},
                                    'RANGED':  {'x': 0.85, 'y': 0.15},
                                    'CASTER':  {'x': 0.85, 'y': 0.15},
                                },
                                'explanation': 'Odd #s spread NW/SW. Even #s spread NE/SE. '
                                               'The boss cleaves the other two intercardinals.',
                                'safe_zones': [],
                            },
                            {
                                'order': 2,
                                'title': 'Rotate for Second Hit',
                                'narration': 'After the first explosion the pattern rotates 90°. '
                                             'Move clockwise to the next safe intercardinal.',
                                'timer_seconds': 5,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.5},
                                    'aoes': [
                                        {'shape': 'cone', 'cx': 0.5, 'cy': 0.5, 'angle': 315, 'spread': 90,
                                         'color': 'rgba(160,100,255,0.4)', 'label': 'Cleave'},
                                        {'shape': 'cone', 'cx': 0.5, 'cy': 0.5, 'angle': 135, 'spread': 90,
                                         'color': 'rgba(160,100,255,0.4)', 'label': 'Cleave'},
                                    ],
                                },
                                'correct_positions': {
                                    'TANK':    {'x': 0.85, 'y': 0.15},
                                    'HEALER':  {'x': 0.15, 'y': 0.85},
                                    'MELEE':   {'x': 0.85, 'y': 0.85},
                                    'RANGED':  {'x': 0.15, 'y': 0.15},
                                    'CASTER':  {'x': 0.15, 'y': 0.15},
                                },
                                'explanation': 'Rotate 90° clockwise from your starting intercardinal. '
                                               'This keeps you in the gaps between the rotating cleaves.',
                                'safe_zones': [],
                            },
                        ],
                    },
                    {
                        'name': 'Blastburn (Role-specific)',
                        'slug': 'blastburn',
                        'description': 'Tanks must bait a charged AoE while DPS stack behind. '
                                       'Healers position to cover both.',
                        'difficulty_rating': 3,
                        'applicable_roles': ['TANK'],
                        'tags': ['bait', 'stack', 'role-specific'],
                        'order': 2,
                        'steps': [
                            {
                                'order': 1,
                                'title': 'Tank: Bait the Blast (TANK ONLY)',
                                'narration': 'Wicked Thunder targets both tanks with a wide cone. '
                                             'Tanks drag the boss to the wall and face it outward.',
                                'timer_seconds': 6,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.5},
                                    'aoes': [
                                        {'shape': 'cone', 'cx': 0.5, 'cy': 0.0, 'angle': 180, 'spread': 120,
                                         'color': 'rgba(255,120,0,0.45)', 'label': 'Blast Cone'},
                                    ],
                                },
                                'correct_positions': {
                                    'TANK': {'x': 0.5, 'y': 0.1},
                                },
                                'explanation': 'Drag the boss to the North wall and face it away from the party. '
                                               'The cone fires into the wall, away from DPS.',
                                'safe_zones': [],
                            },
                        ],
                    },
                ],
            },
            {
                'name': 'Phase 2 — Intermission',
                'order': 2,
                'description': 'Adds phase / Electrope adds.',
                'mechanics': [
                    {
                        'name': 'Electrope Edge (Chain Lightning)',
                        'slug': 'electrope-edge',
                        'description': 'Chain lightning jumps between players. '
                                       'Maintain exact spacing to control the chain path.',
                        'difficulty_rating': 4,
                        'applicable_roles': [],
                        'tags': ['chain', 'spacing', 'lightning'],
                        'order': 1,
                        'steps': [
                            {
                                'order': 1,
                                'title': 'Space Evenly Around Arena',
                                'narration': 'Chain lightning will jump to the nearest player. '
                                             'Spread to cardinals and intercardinals at mid-range.',
                                'timer_seconds': 8,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.5},
                                    'aoes': [
                                        {'shape': 'circle', 'cx': 0.5, 'cy': 0.5, 'r': 0.07,
                                         'color': 'rgba(100,220,255,0.5)', 'label': 'Chain Origin'},
                                    ],
                                    'markers': [
                                        {'id': 'A', 'x': 0.5,  'y': 0.05},
                                        {'id': 'B', 'x': 0.95, 'y': 0.5},
                                        {'id': 'C', 'x': 0.5,  'y': 0.95},
                                        {'id': 'D', 'x': 0.05, 'y': 0.5},
                                    ],
                                },
                                'correct_positions': {
                                    'TANK':    {'x': 0.5,  'y': 0.15},
                                    'HEALER':  {'x': 0.85, 'y': 0.85},
                                    'MELEE':   {'x': 0.15, 'y': 0.85},
                                    'RANGED':  {'x': 0.85, 'y': 0.15},
                                    'CASTER':  {'x': 0.15, 'y': 0.15},
                                },
                                'explanation': 'Eight-way spread. Maintain equal distance between neighbours '
                                               'so the chain travels in the intended order.',
                                'safe_zones': [],
                            },
                        ],
                    },
                ],
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # FRU — Futures Rewritten (Ultimate)
    # ─────────────────────────────────────────────────────────────────────────
    {
        'slug': 'fru',
        'name': 'Futures Rewritten (Ultimate)',
        'short_name': 'FRU',
        'boss_name': 'Fatebreaker / Usurper of Frost',
        'difficulty': 'ULTIMATE',
        'tier': 'Futures Rewritten',
        'patch': '7.1',
        'arena_shape': 'SQUARE',
        'order': 5,
        'phases': [
            {
                'name': 'P1: Fatebreaker',
                'order': 1,
                'description': 'Fatebreaker opens with Cyclonic Break and Bound of Faith.',
                'mechanics': [
                    {
                        'name': 'Cyclonic Break',
                        'slug': 'cyclonic-break',
                        'description': 'Two sets of AoEs hit in sequence. '
                                       'Players with "Lightning" debuff spread; '
                                       'players with "Blizzard" debuff stack with the tanks.',
                        'difficulty_rating': 4,
                        'applicable_roles': [],
                        'tags': ['debuff', 'spread', 'stack', 'lightning', 'ice'],
                        'order': 1,
                        'steps': [
                            {
                                'order': 1,
                                'title': 'Check Elemental Debuff',
                                'narration': 'Cyclonic Break resolves twice. '
                                             'Identify whether you have Lightning (spread) or Blizzard (stack).',
                                'timer_seconds': 6,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.3},
                                    'debuffs': [
                                        {'label': '⚡ Lightning → Spread', 'color': '#ffe066'},
                                        {'label': '❄ Blizzard → Stack', 'color': '#80d4ff'},
                                    ],
                                },
                                'correct_positions': {
                                    'TANK':    {'x': 0.5,  'y': 0.2},
                                    'HEALER':  {'x': 0.5,  'y': 0.8},
                                    'MELEE':   {'x': 0.15, 'y': 0.5},
                                    'RANGED':  {'x': 0.85, 'y': 0.5},
                                    'CASTER':  {'x': 0.85, 'y': 0.5},
                                },
                                'explanation': 'Lightning players take the 4 outer cardinals (N/S/E/W). '
                                               'Blizzard players stack with the tanks in the corners.',
                                'safe_zones': [],
                            },
                            {
                                'order': 2,
                                'title': 'Second Hit — Swap Roles',
                                'narration': 'Debuffs swap after the first hit. '
                                             'Lightning players now stack; Blizzard players spread.',
                                'timer_seconds': 5,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.3},
                                },
                                'correct_positions': {
                                    'TANK':    {'x': 0.15, 'y': 0.15},
                                    'HEALER':  {'x': 0.85, 'y': 0.85},
                                    'MELEE':   {'x': 0.5,  'y': 0.8},
                                    'RANGED':  {'x': 0.5,  'y': 0.2},
                                    'CASTER':  {'x': 0.85, 'y': 0.15},
                                },
                                'explanation': 'Swap positions — previous spreaders now stack at the corners '
                                               'while the other group takes the cardinal spots.',
                                'safe_zones': [],
                            },
                        ],
                    },
                    {
                        'name': 'Bound of Faith',
                        'slug': 'bound-of-faith',
                        'description': 'Fatebreaker targets a non-tank with a large line AoE. '
                                       'Tanks must quickly intercept by standing between the boss and the target.',
                        'difficulty_rating': 3,
                        'applicable_roles': ['TANK'],
                        'tags': ['line-aoe', 'bait', 'tank-specific'],
                        'order': 2,
                        'steps': [
                            {
                                'order': 1,
                                'title': 'Tank: Intercept the Line',
                                'narration': 'Fatebreaker fires a line AoE at the farthest player. '
                                             'A tank must step into the line to take the hit.',
                                'timer_seconds': 5,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.1},
                                    'aoes': [
                                        {'shape': 'rect', 'x': 0.45, 'y': 0.1, 'w': 0.1, 'h': 0.9,
                                         'color': 'rgba(255,60,60,0.4)', 'label': 'Line AoE'},
                                    ],
                                },
                                'correct_positions': {
                                    'TANK': {'x': 0.5, 'y': 0.5},
                                },
                                'explanation': 'MT intercepts by standing in the line between boss and target. '
                                               'Use tank cooldowns — this hits hard.',
                                'safe_zones': [],
                            },
                        ],
                    },
                ],
            },
            {
                'name': 'P2: Usurper of Frost',
                'order': 2,
                'description': 'Usurper of Frost with Mirror mirrors and Diamond Dust.',
                'mechanics': [
                    {
                        'name': 'Diamond Dust',
                        'slug': 'diamond-dust',
                        'description': 'The entire arena is covered. '
                                       'Players must stand in very specific spots based on their ice debuff type.',
                        'difficulty_rating': 5,
                        'applicable_roles': [],
                        'tags': ['ice', 'platform', 'debuff', 'ultimate'],
                        'order': 1,
                        'steps': [
                            {
                                'order': 1,
                                'title': 'Pre-position for Ice Platforms',
                                'narration': 'Diamond Dust covers the floor in ice. '
                                             'Only 4 small platforms remain safe. '
                                             'Hellfire debuff = inner; Frostbite = outer.',
                                'timer_seconds': 10,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.5},
                                    'aoes': [
                                        {'shape': 'rect', 'x': 0.0, 'y': 0.0, 'w': 1.0, 'h': 1.0,
                                         'color': 'rgba(150,220,255,0.3)', 'label': 'Ice Floor'},
                                        {'shape': 'circle', 'cx': 0.25, 'cy': 0.25, 'r': 0.08,
                                         'color': 'rgba(255,255,255,0.7)', 'label': 'Platform'},
                                        {'shape': 'circle', 'cx': 0.75, 'cy': 0.25, 'r': 0.08,
                                         'color': 'rgba(255,255,255,0.7)', 'label': 'Platform'},
                                        {'shape': 'circle', 'cx': 0.25, 'cy': 0.75, 'r': 0.08,
                                         'color': 'rgba(255,255,255,0.7)', 'label': 'Platform'},
                                        {'shape': 'circle', 'cx': 0.75, 'cy': 0.75, 'r': 0.08,
                                         'color': 'rgba(255,255,255,0.7)', 'label': 'Platform'},
                                    ],
                                },
                                'correct_positions': {
                                    'TANK':    {'x': 0.25, 'y': 0.25},
                                    'HEALER':  {'x': 0.75, 'y': 0.75},
                                    'MELEE':   {'x': 0.75, 'y': 0.25},
                                    'RANGED':  {'x': 0.25, 'y': 0.75},
                                    'CASTER':  {'x': 0.25, 'y': 0.75},
                                },
                                'explanation': 'Each pair (Tank+Healer, M1+R1, M2+C1, OT+H2) takes one platform. '
                                               'Two players per platform. Standing off-platform = instant death.',
                                'safe_zones': [
                                    {'shape': 'circle', 'cx': 0.25, 'cy': 0.25, 'r': 0.08},
                                    {'shape': 'circle', 'cx': 0.75, 'cy': 0.25, 'r': 0.08},
                                    {'shape': 'circle', 'cx': 0.25, 'cy': 0.75, 'r': 0.08},
                                    {'shape': 'circle', 'cx': 0.75, 'cy': 0.75, 'r': 0.08},
                                ],
                            },
                        ],
                    },
                    {
                        'name': 'Akh Morn (Tankbuster)',
                        'slug': 'akh-morn',
                        'description': 'Multi-hit tankbuster. Both tanks must swap to share the damage hits.',
                        'difficulty_rating': 2,
                        'applicable_roles': ['TANK'],
                        'tags': ['tankbuster', 'swap', 'cooldown'],
                        'order': 2,
                        'steps': [
                            {
                                'order': 1,
                                'title': 'Tanks: Stack and Cooldown',
                                'narration': 'Akh Morn hits the MT 3 times. '
                                             'OT invulnerability covers hits 2–3, or both stack for shared mitigation.',
                                'timer_seconds': 8,
                                'arena_state': {
                                    'boss_position': {'x': 0.5, 'y': 0.3},
                                    'aoes': [
                                        {'shape': 'circle', 'cx': 0.5, 'cy': 0.15, 'r': 0.06,
                                         'color': 'rgba(255,80,80,0.6)', 'label': 'Akh Morn'},
                                    ],
                                },
                                'correct_positions': {
                                    'TANK': {'x': 0.5, 'y': 0.15},
                                },
                                'explanation': 'MT takes the first hit; invuln or stack for hits 2–3. '
                                               'Coordinate tank cooldowns before the cast.',
                                'safe_zones': [],
                            },
                        ],
                    },
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with M1S–M4S and FRU mechanics.'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')
        Fight.objects.all().delete()

        for fight_data in SEED_DATA:
            self.stdout.write(f"  Creating {fight_data['short_name']}...")
            phases_data = fight_data.pop('phases')
            fight = Fight.objects.create(**fight_data)

            for phase_data in phases_data:
                mechanics_data = phase_data.pop('mechanics')
                phase = Phase.objects.create(fight=fight, **phase_data)

                for mech_data in mechanics_data:
                    steps_data = mech_data.pop('steps')
                    mech = Mechanic.objects.create(phase=phase, **mech_data)

                    for step_data in steps_data:
                        MechanicStep.objects.create(mechanic=mech, **step_data)

        self.stdout.write(self.style.SUCCESS(
            f'✓ Seeded {Fight.objects.count()} fights, '
            f'{Phase.objects.count()} phases, '
            f'{Mechanic.objects.count()} mechanics, '
            f'{MechanicStep.objects.count()} steps.'
        ))
