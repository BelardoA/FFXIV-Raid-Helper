from django.db import models


class Role(models.TextChoices):
    TANK = 'TANK', 'Tank'
    HEALER = 'HEALER', 'Healer'
    MELEE = 'MELEE', 'Melee DPS'
    RANGED = 'RANGED', 'Ranged DPS'
    CASTER = 'CASTER', 'Caster DPS'
    ANY = 'ANY', 'Any'


class Difficulty(models.TextChoices):
    NORMAL = 'NORMAL', 'Normal'
    SAVAGE = 'SAVAGE', 'Savage'
    EXTREME = 'EXTREME', 'Extreme'
    ULTIMATE = 'ULTIMATE', 'Ultimate'


class ArenaShape(models.TextChoices):
    SQUARE = 'SQUARE', 'Square'
    CIRCLE = 'CIRCLE', 'Circle'
    OCTAGON = 'OCTAGON', 'Octagon'


class Fight(models.Model):
    """Represents a single raid encounter (e.g. M1S, FRU)"""
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=120)           # "AAC Light-heavyweight M1 (Savage)"
    short_name = models.CharField(max_length=20)      # "M1S"
    boss_name = models.CharField(max_length=120)      # "Black Cat"
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices)
    tier = models.CharField(max_length=80, blank=True)  # "AAC Light-heavyweight"
    patch = models.CharField(max_length=10, blank=True)  # "7.0"
    arena_shape = models.CharField(max_length=20, choices=ArenaShape.choices, default=ArenaShape.CIRCLE)
    order = models.PositiveIntegerField(default=0)
    thumbnail_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.short_name} – {self.boss_name}"


class Phase(models.Model):
    """A named phase within a fight (e.g. 'P1: Fatebreaker', 'Adds Phase')"""
    fight = models.ForeignKey(Fight, on_delete=models.CASCADE, related_name='phases')
    name = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['order']
        unique_together = [('fight', 'order')]

    def __str__(self):
        return f"{self.fight.short_name} – {self.name}"


class Mechanic(models.Model):
    """
    A discrete mechanic within a phase (e.g. 'Witch Hunt', 'Blastburn').
    Contains the overall setup and correct resolution.
    """
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='mechanics')
    name = models.CharField(max_length=120)
    slug = models.SlugField()
    description = models.TextField(blank=True)          # Flavor / strategy overview
    order = models.PositiveIntegerField(default=0)
    difficulty_rating = models.PositiveSmallIntegerField(default=1)  # 1-5
    applicable_roles = models.JSONField(default=list)   # ['TANK','HEALER'] or [] = all
    tags = models.JSONField(default=list)               # ['spread','stack','tether','limit-cut']

    # Visual hint image URL (from community resources)
    diagram_url = models.URLField(blank=True)

    class Meta:
        ordering = ['order']
        unique_together = [('phase', 'slug')]

    def __str__(self):
        return f"{self.phase} / {self.name}"


class MechanicStep(models.Model):
    """
    One sequential step within a mechanic's resolution.
    Used for timed drills — each step shows arena state + asks user to position.
    """
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, related_name='steps')
    order = models.PositiveIntegerField(default=0)

    # What's happening at this moment
    title = models.CharField(max_length=200)
    narration = models.TextField(blank=True)  # "The boss is casting Witch Hunt. Odd debuffs go..."

    # How long players have to react (seconds) — 0 = no timer
    timer_seconds = models.PositiveSmallIntegerField(default=0)

    # Arena state: JSON describing what's visible on the arena
    # {
    #   "markers": [{"id": "A", "x": 0.5, "y": 0.0}],
    #   "aoes": [{"shape": "circle", "cx": 0.5, "cy": 0.5, "r": 0.15, "color": "red"}],
    #   "tethers": [{"from": "boss", "to": "player_tank"}],
    #   "debuffs": [{"role": "TANK", "icon": "magic_vuln", "label": "Magic Vulnerability Up"}]
    # }
    arena_state = models.JSONField(default=dict)

    # Correct positions per role  — key is Role value, value is {x, y} normalised 0-1
    # e.g. {"TANK": {"x": 0.5, "y": 0.1}, "HEALER": {"x": 0.3, "y": 0.9}}
    correct_positions = models.JSONField(default=dict)

    # Alternative valid positions (for mechanics with multiple strats)
    alt_positions = models.JSONField(default=dict)

    # Explanation shown after answer
    explanation = models.TextField(blank=True)

    # Visual cue: highlight zones that are safe
    safe_zones = models.JSONField(default=list)

    class Meta:
        ordering = ['order']
        unique_together = [('mechanic', 'order')]

    def __str__(self):
        return f"{self.mechanic.name} – Step {self.order}: {self.title}"


class UserSession(models.Model):
    """Lightweight anonymous session tracking for drill scores"""
    session_key = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class DrillResult(models.Model):
    """Records how a user performed on a mechanic drill step"""
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='results')
    mechanic_step = models.ForeignKey(MechanicStep, on_delete=models.CASCADE)
    role_used = models.CharField(max_length=20, choices=Role.choices)

    # Position the user clicked, normalised 0-1
    submitted_x = models.FloatField()
    submitted_y = models.FloatField()

    is_correct = models.BooleanField()
    time_taken_ms = models.PositiveIntegerField(default=0)  # response time
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-attempted_at']
