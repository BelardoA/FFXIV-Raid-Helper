# Raid Admin Editing Guide

This project includes a Django admin portal for managing raid content: tiers, fights, mechanics, steps, and role-specific variants.

## Access

1. Start the backend.
2. Open `/admin/`.
3. Sign in with a Django staff or superuser account.

If you do not already have an admin account, create one from the backend directory:

```bash
python manage.py createsuperuser
```

## Main Admin Areas

- `Raid Tiers`: top-level grouping such as Arcadion or FRU.
- `Fights`: individual encounters such as `M1S`.
- `Mechanics`: individual mechanics within a fight.
- `Mechanic steps`: each decision point in a mechanic.
- `Role variants`: per-role and per-spot answers for each step.

## Recommended Editing Flow

Use this flow instead of editing tables in arbitrary order:

1. Open `/admin/`.
2. Go to `Fights`.
3. Click `Open Raid Content Editor`.
4. Choose the fight you want to edit.
5. From the fight editor page:
   - edit the fight record
   - add or edit mechanics
   - add or edit steps inside each mechanic
   - add or edit role variants for each step

This portal is the quickest way to work because it shows the full fight structure in one place.

## Content Hierarchy

Raid data is structured like this:

```text
Raid Tier
  -> Fight
    -> Mechanic
      -> Mechanic Step
        -> Role Variant
```

## What Each Model Controls

### Raid Tier

Use this for:

- tier name
- expansion
- patch
- display order
- whether the tier is active

### Fight

Use this for:

- fight name and short name
- boss name
- difficulty
- arena shape
- ordering inside a tier
- active status
- thumbnail / arena / boss image URLs

### Mechanic

Use this for:

- mechanic name
- slug
- phase name
- description
- mechanic order within the fight
- difficulty rating
- tags

### Mechanic Step

Use this for:

- step order
- title
- narration
- timer
- action type
- arena snapshot
- choice options
- explanation text
- default tolerance

### Role Variant

Use this for:

- role
- spot
- correct position
- correct choice
- alternative valid positions
- safe zones
- tolerance override
- role-specific explanation

## Action Types

`MechanicStep.action_type` controls what kind of answer the player gives.

### `POSITION`

Use this when the player should click a location in the arena.

Relevant fields:

- step `arena_state`
- role variant `correct_position`
- role variant `alt_positions`
- role variant `safe_zones`
- role variant `tolerance` or step `default_tolerance`

### `CHOICE`

Use this when the player should select from buttons.

Relevant fields:

- step `choices`
- role variant `correct_choice`

## JSON Fields

Several fields are JSON. The admin includes a `Format JSON` button to pretty-print valid JSON.

### Mechanic tags

```json
["spread", "stack", "tether"]
```

### Step arena state

Example:

```json
{
  "boss_position": { "x": 0.5, "y": 0.5 },
  "markers": [
    { "id": "A", "x": 0.5, "y": 0.1 },
    { "id": "B", "x": 0.9, "y": 0.5 }
  ],
  "aoes": [
    { "shape": "circle", "cx": 0.5, "cy": 0.5, "r": 0.18, "color": "#ff4444" }
  ],
  "tethers": [],
  "debuffs": [
    { "label": "Light Party", "color": "#66ccff" }
  ]
}
```

### Step choices

```json
[
  { "id": "spread", "label": "Spread" },
  { "id": "stack", "label": "Stack" }
]
```

### Role variant correct position

This field now has a visual arena picker in Django admin. Click on the grid to place the marker. The JSON updates automatically.

```json
{ "x": 0.75, "y": 0.25 }
```

Coordinates are normalized from `0` to `1`.

- `x = 0` is left
- `x = 1` is right
- `y = 0` is top
- `y = 1` is bottom

### Role variant alt positions

```json
[
  { "x": 0.72, "y": 0.28, "label": "Alt strat" }
]
```

### Role variant safe zones

Circle example:

```json
[
  { "shape": "circle", "cx": 0.25, "cy": 0.25, "r": 0.12 }
]
```

Rectangle example:

```json
[
  { "shape": "rect", "x": 0.1, "y": 0.1, "w": 0.2, "h": 0.3 }
]
```

## Role and Spot Rules

Each role variant is tied to:

- a role: `TANK`, `HEALER`, `MELEE`, `RANGED`
- a spot: `1` or `2`

Examples:

- `TANK` + `1` = MT-style slot
- `TANK` + `2` = OT-style slot
- `HEALER` + `1` = H1-style slot
- `HEALER` + `2` = H2-style slot

If only spot `1` exists for a role, the engine can fall back to it for spot `2`.

## Common Editing Tasks

### Add a new mechanic to an existing fight

1. Open the fight in the Raid Content Editor.
2. Click `Add mechanic`.
3. Fill in the mechanic metadata.
4. Save.
5. Add steps to that mechanic.
6. Add role variants to each step.

### Add a new step to a mechanic

1. Open the fight editor page.
2. Find the mechanic.
3. Click `Add step`.
4. Set the step order.
5. Choose `POSITION` or `CHOICE`.
6. Fill the arena state or choices.
7. Save.
8. Add role variants.

### Add role answers for a step

1. Open the step from the fight editor page.
2. Add one role variant per role and spot combination you care about.
3. For position steps, fill `correct_position`.
4. For choice steps, fill `correct_choice`.
5. Save.

## Publishing and Visibility

Content only shows up in the frontend if:

- the raid tier is active
- the fight is active

If a fight or tier does not appear in the app, check those flags first.

## Recommended Validation

After editing:

1. Open the frontend.
2. Select the fight.
3. Run the mechanic or full-fight drill you changed.
4. Verify:
   - ordering is correct
   - arena visuals look correct
   - each role gets the expected answer
   - tolerance feels reasonable
   - explanations match the intended strat

## Troubleshooting

### The fight does not show in the app

Check:

- `RaidTier.is_active`
- `Fight.is_active`
- fight ordering and tier assignment

### A step renders but has no valid answer

Check that at least one `RoleVariant` exists for that step for the target role and spot.

### A choice step has no buttons

Check that `MechanicStep.choices` contains valid JSON.

### A position answer is always wrong

Check:

- `correct_position`
- `alt_positions`
- `tolerance`
- `default_tolerance`

### JSON will not save

Use the `Format JSON` button first. If formatting fails, the JSON is invalid.

## Best Practices

- Keep slugs stable once content is in use.
- Use mechanic and step `order` values deliberately.
- Prefer editing through the fight portal instead of hopping across raw admin tables.
- For shared role behavior, define spot `1` first, then only add spot `2` when it is actually different.
- Keep explanations short and role-specific when needed.
