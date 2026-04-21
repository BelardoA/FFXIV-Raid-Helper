"""DRF serializers for the raids API."""

from rest_framework import serializers

from .models import (
    DrillResult,
    Fight,
    Mechanic,
    MechanicStep,
    RaidTier,
    RoleVariant,
    UserSession,
)


# ---------------------------------------------------------------------------
# Read serializers (nested, read-only)
# ---------------------------------------------------------------------------

class RoleVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleVariant
        fields = [
            "id",
            "role",
            "spot",
            "correct_position",
            "tolerance",
            "alt_positions",
            "correct_choice",
            "safe_zones",
            "explanation",
        ]


class MechanicStepSerializer(serializers.ModelSerializer):
    role_variants = RoleVariantSerializer(many=True, read_only=True)

    class Meta:
        model = MechanicStep
        fields = [
            "id",
            "order",
            "title",
            "narration",
            "timer_seconds",
            "default_tolerance",
            "action_type",
            "arena_state",
            "choices",
            "explanation",
            "role_variants",
        ]


class MechanicListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing mechanics (no nested steps)."""
    step_count = serializers.IntegerField(source="steps.count", read_only=True)

    class Meta:
        model = Mechanic
        fields = [
            "id",
            "slug",
            "name",
            "phase_name",
            "description",
            "order",
            "difficulty_rating",
            "tags",
            "step_count",
        ]


class MechanicDetailSerializer(serializers.ModelSerializer):
    """Full serializer with nested steps and role variants."""
    steps = MechanicStepSerializer(many=True, read_only=True)
    fight_slug = serializers.CharField(source="fight.slug", read_only=True)
    fight_short_name = serializers.CharField(source="fight.short_name", read_only=True)
    arena_shape = serializers.CharField(source="fight.arena_shape", read_only=True)
    arena_image_url = serializers.CharField(source="fight.arena_image_url", read_only=True)
    boss_image_url = serializers.CharField(source="fight.boss_image_url", read_only=True)

    class Meta:
        model = Mechanic
        fields = [
            "id",
            "slug",
            "name",
            "phase_name",
            "description",
            "order",
            "difficulty_rating",
            "tags",
            "fight_slug",
            "fight_short_name",
            "arena_shape",
            "arena_image_url",
            "boss_image_url",
            "steps",
        ]


class FightListSerializer(serializers.ModelSerializer):
    mechanic_count = serializers.IntegerField(source="mechanics.count", read_only=True)
    raid_tier_name = serializers.CharField(source="raid_tier.name", read_only=True)

    class Meta:
        model = Fight
        fields = [
            "id",
            "slug",
            "name",
            "short_name",
            "boss_name",
            "difficulty",
            "arena_shape",
            "order",
            "thumbnail_url",
            "arena_image_url",
            "boss_image_url",
            "mechanic_count",
            "raid_tier_name",
        ]


class FightDetailSerializer(serializers.ModelSerializer):
    mechanics = MechanicListSerializer(many=True, read_only=True)
    raid_tier_name = serializers.CharField(source="raid_tier.name", read_only=True)

    class Meta:
        model = Fight
        fields = [
            "id",
            "slug",
            "name",
            "short_name",
            "boss_name",
            "difficulty",
            "arena_shape",
            "order",
            "thumbnail_url",
            "arena_image_url",
            "boss_image_url",
            "raid_tier_name",
            "mechanics",
        ]


class RaidTierListSerializer(serializers.ModelSerializer):
    fight_count = serializers.IntegerField(source="fights.count", read_only=True)

    class Meta:
        model = RaidTier
        fields = [
            "id",
            "slug",
            "name",
            "expansion",
            "patch",
            "order",
            "fight_count",
        ]


class RaidTierDetailSerializer(serializers.ModelSerializer):
    fights = FightListSerializer(many=True, read_only=True)

    class Meta:
        model = RaidTier
        fields = [
            "id",
            "slug",
            "name",
            "expansion",
            "patch",
            "order",
            "fights",
        ]


# ---------------------------------------------------------------------------
# Action serializers (write)
# ---------------------------------------------------------------------------

class SimulateStepSerializer(serializers.Serializer):
    """Input for the simulate-step endpoint."""
    step_id = serializers.IntegerField()
    role = serializers.ChoiceField(
        choices=[("TANK", "Tank"), ("HEALER", "Healer"),
                 ("MELEE", "Melee"), ("RANGED", "Ranged")]
    )
    spot = serializers.ChoiceField(choices=[1, 2], default=1)
    # For POSITION actions
    submitted_x = serializers.FloatField(required=False, allow_null=True)
    submitted_y = serializers.FloatField(required=False, allow_null=True)
    # For CHOICE actions
    submitted_choice = serializers.CharField(required=False, allow_blank=True, default="")
    # Session tracking
    session_key = serializers.CharField(max_length=64, required=False, default="")
    time_taken_ms = serializers.IntegerField(required=False, default=0)


class StepResultSerializer(serializers.Serializer):
    """Output from the simulate-step endpoint."""
    is_correct = serializers.BooleanField()
    explanation = serializers.CharField()
    correct_position = serializers.DictField(required=False, allow_null=True)
    correct_choice = serializers.CharField(required=False, allow_null=True)
    distance = serializers.FloatField(required=False, allow_null=True)
    tolerance_used = serializers.FloatField()
    has_next_step = serializers.BooleanField()
    next_step_order = serializers.IntegerField(required=False, allow_null=True)


class SessionStatsSerializer(serializers.Serializer):
    """Session summary statistics."""
    session_key = serializers.CharField()
    total_steps = serializers.IntegerField()
    correct = serializers.IntegerField()
    incorrect = serializers.IntegerField()
    accuracy = serializers.FloatField()
    avg_time_ms = serializers.FloatField()
    grade = serializers.CharField()
    per_mechanic = serializers.ListField()


class DrillPlanFightSerializer(serializers.Serializer):
    """Lightweight fight header embedded in a drill plan."""
    slug = serializers.CharField()
    short_name = serializers.CharField()
    name = serializers.CharField()
    boss_name = serializers.CharField()
    arena_shape = serializers.CharField()
    arena_image_url = serializers.CharField(allow_blank=True)
    boss_image_url = serializers.CharField(allow_blank=True)


class DrillPlanSerializer(serializers.Serializer):
    """
    Flattened drill plan for the whole fight or a phase.
    `scope` is either "full" or the phase name.
    `mechanics` is the ordered list of mechanics (each with nested steps).
    """
    fight = DrillPlanFightSerializer()
    scope = serializers.CharField()
    mechanics = MechanicDetailSerializer(many=True)
