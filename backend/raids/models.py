"""
Data models for the RaidCoach XIV mechanic trainer.

Hierarchy: RaidTier → Fight → Mechanic → MechanicStep → RoleVariant
Session tracking: UserSession → DrillResult
"""

from django.db import models


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Role(models.TextChoices):
    TANK = "TANK", "Tank"
    HEALER = "HEALER", "Healer"
    MELEE = "MELEE", "Melee DPS"
    RANGED = "RANGED", "Ranged DPS"
    CASTER = "CASTER", "Caster DPS"


class Difficulty(models.TextChoices):
    NORMAL = "NORMAL", "Normal"
    SAVAGE = "SAVAGE", "Savage"
    EXTREME = "EXTREME", "Extreme"
    ULTIMATE = "ULTIMATE", "Ultimate"


class ArenaShape(models.TextChoices):
    SQUARE = "SQUARE", "Square"
    CIRCLE = "CIRCLE", "Circle"


class ActionType(models.TextChoices):
    """The kind of input expected from the player for a step."""
    POSITION = "POSITION", "Click a position on the arena"
    CHOICE = "CHOICE", "Pick from a list of options"


# ---------------------------------------------------------------------------
# Content models
# ---------------------------------------------------------------------------

class RaidTier(models.Model):
    """A raid tier grouping (e.g. 'AAC Light-heavyweight', 'Futures Rewritten')."""
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=120)
    expansion = models.CharField(max_length=40, blank=True)  # "Dawntrail"
    patch = models.CharField(max_length=10, blank=True)  # "7.0"
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Fight(models.Model):
    """A single encounter within a raid tier (e.g. M1S, FRU)."""
    raid_tier = models.ForeignKey(
        RaidTier, on_delete=models.CASCADE, related_name="fights"
    )
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=120)
    short_name = models.CharField(max_length=20)
    boss_name = models.CharField(max_length=120)
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices)
    arena_shape = models.CharField(
        max_length=20, choices=ArenaShape.choices, default=ArenaShape.CIRCLE
    )
    order = models.PositiveIntegerField(default=0)
    thumbnail_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.short_name} – {self.boss_name}"


class Mechanic(models.Model):
    """
    A discrete mechanic within a fight (e.g. 'Witch Hunt', 'Diamond Dust').
    Groups sequential MechanicSteps.
    """
    fight = models.ForeignKey(
        Fight, on_delete=models.CASCADE, related_name="mechanics"
    )
    slug = models.SlugField()
    name = models.CharField(max_length=120)
    phase_name = models.CharField(max_length=120, blank=True)  # "P1", "Adds Phase"
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    difficulty_rating = models.PositiveSmallIntegerField(default=1)  # 1-5
    tags = models.JSONField(default=list)  # ["spread","stack","tether"]

    class Meta:
        ordering = ["order"]
        unique_together = [("fight", "slug")]

    def __str__(self):
        return f"{self.fight.short_name} / {self.name}"


class MechanicStep(models.Model):
    """
    One atomic decision point within a mechanic's resolution.

    Defines WHAT is happening (arena_state) and HOW the player responds
    (action_type). Per-role correct answers live in RoleVariant.
    """
    mechanic = models.ForeignKey(
        Mechanic, on_delete=models.CASCADE, related_name="steps"
    )
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    narration = models.TextField(blank=True)
    timer_seconds = models.PositiveSmallIntegerField(default=0)  # 0 = untimed

    # Step-level tolerance override (fraction of arena width, 0-1).
    # Used when RoleVariant.tolerance is null. Falls back to DEFAULT_TOLERANCE.
    default_tolerance = models.FloatField(null=True, blank=True)

    action_type = models.CharField(
        max_length=20, choices=ActionType.choices, default=ActionType.POSITION
    )

    # JSON: what the arena looks like at this moment
    # Schema: {boss_position, boss_facing, markers[], aoes[], tethers[], debuffs[]}
    arena_state = models.JSONField(default=dict)

    # For CHOICE action_type — the options presented to the player
    # e.g. [{"id": "spread", "label": "Spread"}, {"id": "stack", "label": "Stack"}]
    choices = models.JSONField(default=list)

    # Explanation shown after the player answers
    explanation = models.TextField(blank=True)

    class Meta:
        ordering = ["order"]
        unique_together = [("mechanic", "order")]

    def __str__(self):
        return f"{self.mechanic.name} – Step {self.order}: {self.title}"


class RoleVariant(models.Model):
    """
    Per-role correct answer for a MechanicStep.

    This is the core content that makes mechanics role-aware without
    hardcoding logic. For POSITION steps, defines correct {x,y}.
    For CHOICE steps, defines the correct choice id.
    """
    step = models.ForeignKey(
        MechanicStep, on_delete=models.CASCADE, related_name="role_variants"
    )
    role = models.CharField(max_length=20, choices=Role.choices)

    # For POSITION: {x, y} normalised 0-1
    correct_position = models.JSONField(default=dict)

    # Tolerance override for this specific role+step (fraction of arena width).
    # If null, engine uses the global default (0.12).
    tolerance = models.FloatField(null=True, blank=True)

    # Alternative valid positions (different strats)
    # [{x, y, label: "Hamkatsu strat"}]
    alt_positions = models.JSONField(default=list)

    # For CHOICE: the correct choice id string
    correct_choice = models.CharField(max_length=80, blank=True)

    # Safe zones to highlight on reveal [{shape, cx, cy, r, x, y, w, h}]
    safe_zones = models.JSONField(default=list)

    # Role-specific explanation override (falls back to MechanicStep.explanation)
    explanation = models.TextField(blank=True)

    class Meta:
        unique_together = [("step", "role")]

    def __str__(self):
        return f"{self.step} [{self.role}]"


# ---------------------------------------------------------------------------
# Session tracking
# ---------------------------------------------------------------------------

class UserSession(models.Model):
    """Lightweight anonymous session for tracking drill scores."""
    session_key = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.session_key


class DrillResult(models.Model):
    """Records a single answer within a drill session."""
    session = models.ForeignKey(
        UserSession, on_delete=models.CASCADE, related_name="results"
    )
    step = models.ForeignKey(MechanicStep, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices)

    # What the user submitted
    submitted_x = models.FloatField(null=True, blank=True)
    submitted_y = models.FloatField(null=True, blank=True)
    submitted_choice = models.CharField(max_length=80, blank=True)

    is_correct = models.BooleanField()
    time_taken_ms = models.PositiveIntegerField(default=0)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-attempted_at"]

    def __str__(self):
        status = "✓" if self.is_correct else "✗"
        return f"{status} {self.step} [{self.role}]"
