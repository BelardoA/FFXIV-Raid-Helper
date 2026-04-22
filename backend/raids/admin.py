import json

from django import forms
from django.contrib import admin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html

from .models import (
    DrillResult,
    Fight,
    Mechanic,
    MechanicStep,
    RaidTier,
    RoleVariant,
    UserSession,
)


admin.site.site_header = "RaidCoach Admin"
admin.site.site_title = "RaidCoach Admin"
admin.site.index_title = "Raid content management"


class PrettyJSONWidget(forms.Textarea):
    """Formats JSON values for easier editing in Django admin."""

    def __init__(self, attrs=None):
        base_attrs = {
            "class": "vLargeTextField rc-json-editor",
            "rows": 10,
            "spellcheck": "false",
            "data-json-editor": "true",
        }
        if attrs:
            base_attrs.update(attrs)
        super().__init__(attrs=base_attrs)

    def format_value(self, value):
        if value in ("", None):
            return ""
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                return value
            return json.dumps(parsed, indent=2, sort_keys=True)
        try:
            return json.dumps(value, indent=2, sort_keys=True)
        except TypeError:
            return super().format_value(value)


class PositionJSONWidget(PrettyJSONWidget):
    """JSON textarea enhanced with a click-to-place arena picker."""

    def __init__(self, attrs=None):
        base_attrs = {
            "data-position-picker": "true",
            "data-arena-shape": "SQUARE",
        }
        if attrs:
            base_attrs.update(attrs)
        super().__init__(attrs=base_attrs)


class JSONAdminFormMixin:
    """Adds JSON widgets plus small editor assets across admin forms."""

    class Media:
        css = {"all": ("raids/admin/editor.css",)}
        js = ("raids/admin/editor_widgets_v2.js",)


class MechanicAdminForm(JSONAdminFormMixin, forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = "__all__"
        widgets = {
            "tags": PrettyJSONWidget(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].help_text = (
            'JSON array of tags, for example `["spread", "stack", "tether"]`.'
        )


class MechanicStepAdminForm(JSONAdminFormMixin, forms.ModelForm):
    class Meta:
        model = MechanicStep
        fields = "__all__"
        widgets = {
            "arena_state": PrettyJSONWidget(attrs={"rows": 16}),
            "choices": PrettyJSONWidget(attrs={"rows": 8}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["arena_state"].help_text = (
            "Arena snapshot for this step. Include boss, markers, AoEs, tethers, and debuffs."
        )
        self.fields["choices"].help_text = (
            'For choice steps, use JSON like `[{"id": "spread", "label": "Spread"}]`.'
        )


class RoleVariantAdminForm(JSONAdminFormMixin, forms.ModelForm):
    class Meta:
        model = RoleVariant
        fields = "__all__"
        widgets = {
            "correct_position": PositionJSONWidget(attrs={"rows": 6}),
            "alt_positions": PrettyJSONWidget(attrs={"rows": 8}),
            "safe_zones": PrettyJSONWidget(attrs={"rows": 8}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        arena_shape = self._resolve_arena_shape()
        self.fields["correct_position"].widget.attrs["data-arena-shape"] = arena_shape
        self.fields["correct_position"].help_text = (
            "Click in the arena picker to place the correct position. "
            'The JSON stays editable if you need to fine-tune it.'
        )
        self.fields["alt_positions"].help_text = (
            "Alternative valid coordinates for different strats."
        )
        self.fields["safe_zones"].help_text = (
            "Safe zone overlays revealed after the answer is submitted."
        )

    def _resolve_arena_shape(self):
        step = getattr(self.instance, "step", None)
        if step and getattr(step, "mechanic_id", None):
            return step.mechanic.fight.arena_shape

        step_id = self.initial.get("step") or self.data.get("step")
        if step_id:
            try:
                step = (
                    MechanicStep.objects.select_related("mechanic__fight")
                    .get(pk=step_id)
                )
                return step.mechanic.fight.arena_shape
            except (MechanicStep.DoesNotExist, ValueError, TypeError):
                pass

        return "SQUARE"


class FightInline(admin.TabularInline):
    model = Fight
    extra = 0
    show_change_link = True
    fields = [
        "slug",
        "short_name",
        "boss_name",
        "difficulty",
        "order",
        "is_active",
    ]


class MechanicInline(admin.TabularInline):
    model = Mechanic
    extra = 0
    show_change_link = True
    fields = [
        "slug",
        "name",
        "phase_name",
        "order",
        "difficulty_rating",
    ]


class MechanicStepInline(admin.StackedInline):
    model = MechanicStep
    form = MechanicStepAdminForm
    extra = 0
    show_change_link = True
    fields = [
        "order",
        "title",
        "narration",
        "timer_seconds",
        "default_tolerance",
        "action_type",
        "arena_state",
        "choices",
        "explanation",
    ]


class RoleVariantInline(admin.StackedInline):
    model = RoleVariant
    form = RoleVariantAdminForm
    extra = 0
    show_change_link = True
    fields = [
        ("role", "spot"),
        ("correct_choice", "tolerance"),
        "correct_position",
        "alt_positions",
        "safe_zones",
        "explanation",
    ]


@admin.register(RaidTier)
class RaidTierAdmin(admin.ModelAdmin):
    list_display = ["name", "expansion", "patch", "fight_total", "order", "is_active"]
    list_editable = ["order", "is_active"]
    search_fields = ["name", "slug", "expansion", "patch"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [FightInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(fight_total=Count("fights"))

    @admin.display(ordering="fight_total", description="Fights")
    def fight_total(self, obj):
        return obj.fight_total


@admin.register(Fight)
class FightAdmin(admin.ModelAdmin):
    change_list_template = "admin/raids/fight/change_list.html"
    list_display = [
        "short_name",
        "boss_name",
        "difficulty",
        "raid_tier",
        "mechanic_total",
        "step_total",
        "order",
        "is_active",
        "editor_link",
    ]
    list_editable = ["order", "is_active"]
    list_filter = ["difficulty", "raid_tier", "is_active"]
    search_fields = ["short_name", "name", "boss_name", "slug"]
    prepopulated_fields = {"slug": ("short_name",)}
    inlines = [MechanicInline]
    readonly_fields = ["mechanic_total_display", "step_total_display"]
    fieldsets = (
        (
            "Fight",
            {
                "fields": (
                    ("raid_tier", "difficulty"),
                    ("name", "short_name", "slug"),
                    ("boss_name", "order", "is_active"),
                )
            },
        ),
        (
            "Arena Assets",
            {
                "fields": (
                    "arena_shape",
                    "thumbnail_url",
                    "arena_image_url",
                    "boss_image_url",
                )
            },
        ),
        (
            "Editor Summary",
            {"fields": ("mechanic_total_display", "step_total_display")},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            mechanic_total=Count("mechanics", distinct=True),
            step_total=Count("mechanics__steps", distinct=True),
        )

    @admin.display(ordering="mechanic_total", description="Mechanics")
    def mechanic_total(self, obj):
        return obj.mechanic_total

    @admin.display(ordering="step_total", description="Steps")
    def step_total(self, obj):
        return obj.step_total

    @admin.display(description="Mechanics")
    def mechanic_total_display(self, obj):
        return obj.mechanics.count()

    @admin.display(description="Steps")
    def step_total_display(self, obj):
        return MechanicStep.objects.filter(mechanic__fight=obj).count()

    @admin.display(description="Portal")
    def editor_link(self, obj):
        url = reverse("admin:raids_editor_fight", args=[obj.pk])
        return format_html('<a href="{}">Open editor</a>', url)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "editor/",
                self.admin_site.admin_view(self.editor_index_view),
                name="raids_editor_index",
            ),
            path(
                "editor/fight/<int:fight_id>/",
                self.admin_site.admin_view(self.editor_fight_view),
                name="raids_editor_fight",
            ),
        ]
        return custom_urls + urls

    def editor_index_view(self, request):
        fights = (
            Fight.objects.select_related("raid_tier")
            .annotate(
                mechanic_total=Count("mechanics", distinct=True),
                step_total=Count("mechanics__steps", distinct=True),
                role_variant_total=Count("mechanics__steps__role_variants", distinct=True),
            )
            .order_by(
                "raid_tier__order",
                "order",
            )
        )
        tiers = RaidTier.objects.order_by("order")
        fights_by_tier = {
            tier.pk: [fight for fight in fights if fight.raid_tier_id == tier.pk]
            for tier in tiers
        }
        context = {
            **self.admin_site.each_context(request),
            "title": "Raid Content Editor",
            "tiers": tiers,
            "fights_by_tier": fights_by_tier,
            "opts": self.model._meta,
        }
        return TemplateResponse(request, "admin/raids/editor_index.html", context)

    def editor_fight_view(self, request, fight_id):
        fight = get_object_or_404(
            Fight.objects.select_related("raid_tier")
            .prefetch_related("mechanics__steps__role_variants"),
            pk=fight_id,
        )
        mechanics = sorted(fight.mechanics.all(), key=lambda mechanic: mechanic.order)
        for mechanic in mechanics:
            mechanic.sorted_steps = sorted(mechanic.steps.all(), key=lambda step: step.order)
            mechanic.step_total = len(mechanic.sorted_steps)
            mechanic.role_variant_total = sum(
                step.role_variants.count() for step in mechanic.sorted_steps
            )

        context = {
            **self.admin_site.each_context(request),
            "title": f"Edit {fight.short_name}",
            "fight": fight,
            "mechanics": mechanics,
            "opts": self.model._meta,
            "fight_change_url": reverse("admin:raids_fight_change", args=[fight.pk]),
            "add_mechanic_url": (
                reverse("admin:raids_mechanic_add") + f"?fight={fight.pk}"
            ),
        }
        return TemplateResponse(request, "admin/raids/editor_fight.html", context)


@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    form = MechanicAdminForm
    list_display = [
        "name",
        "fight",
        "phase_name",
        "step_total",
        "difficulty_rating",
        "order",
        "editor_link",
    ]
    list_editable = ["order", "difficulty_rating"]
    list_filter = ["fight", "fight__raid_tier", "difficulty_rating", "phase_name"]
    search_fields = ["name", "slug", "phase_name", "fight__short_name", "fight__boss_name"]
    autocomplete_fields = ["fight"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [MechanicStepInline]
    readonly_fields = ["step_total_display", "role_variant_total_display"]
    fieldsets = (
        (
            "Mechanic",
            {
                "fields": (
                    "fight",
                    ("name", "slug"),
                    ("phase_name", "order"),
                    ("difficulty_rating", "tags"),
                    "description",
                )
            },
        ),
        (
            "Editor Summary",
            {"fields": ("step_total_display", "role_variant_total_display")},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("fight").annotate(
            step_total=Count("steps", distinct=True)
        )

    @admin.display(ordering="step_total", description="Steps")
    def step_total(self, obj):
        return obj.step_total

    @admin.display(description="Steps")
    def step_total_display(self, obj):
        return obj.steps.count()

    @admin.display(description="Role variants")
    def role_variant_total_display(self, obj):
        return RoleVariant.objects.filter(step__mechanic=obj).count()

    @admin.display(description="Portal")
    def editor_link(self, obj):
        url = reverse("admin:raids_editor_fight", args=[obj.fight_id])
        return format_html('<a href="{}#mechanic-{}">Open in portal</a>', url, obj.pk)


@admin.register(MechanicStep)
class MechanicStepAdmin(admin.ModelAdmin):
    form = MechanicStepAdminForm
    list_display = [
        "title",
        "mechanic",
        "order",
        "action_type",
        "timer_seconds",
        "role_variant_total",
        "editor_link",
    ]
    list_filter = ["action_type", "mechanic__fight", "mechanic__phase_name"]
    search_fields = ["title", "mechanic__name", "mechanic__fight__short_name"]
    autocomplete_fields = ["mechanic"]
    inlines = [RoleVariantInline]
    readonly_fields = ["role_variant_total_display"]
    fieldsets = (
        (
            "Step",
            {
                "fields": (
                    "mechanic",
                    ("order", "title"),
                    ("action_type", "timer_seconds"),
                    "default_tolerance",
                    "narration",
                    "explanation",
                )
            },
        ),
        (
            "Arena Data",
            {
                "fields": (
                    "arena_state",
                    "choices",
                )
            },
        ),
        (
            "Editor Summary",
            {"fields": ("role_variant_total_display",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "mechanic",
            "mechanic__fight",
        ).annotate(role_variant_total=Count("role_variants", distinct=True))

    @admin.display(ordering="role_variant_total", description="Variants")
    def role_variant_total(self, obj):
        return obj.role_variant_total

    @admin.display(description="Role variants")
    def role_variant_total_display(self, obj):
        return obj.role_variants.count()

    @admin.display(description="Portal")
    def editor_link(self, obj):
        url = reverse("admin:raids_editor_fight", args=[obj.mechanic.fight_id])
        return format_html('<a href="{}#step-{}">Open in portal</a>', url, obj.pk)


@admin.register(RoleVariant)
class RoleVariantAdmin(admin.ModelAdmin):
    form = RoleVariantAdminForm
    list_display = ["step", "role", "spot", "position_preview", "correct_choice"]
    list_filter = ["role", "spot", "step__mechanic__fight", "step__mechanic__phase_name"]
    search_fields = ["step__title", "step__mechanic__name", "step__mechanic__fight__short_name"]
    autocomplete_fields = ["step"]

    @admin.display(description="Position")
    def position_preview(self, obj):
        if not obj.correct_position:
            return "—"
        x = obj.correct_position.get("x")
        y = obj.correct_position.get("y")
        if x is None or y is None:
            return "—"
        return f"({x}, {y})"


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ["session_key", "created_at"]
    search_fields = ["session_key"]
    readonly_fields = ["session_key", "created_at"]


@admin.register(DrillResult)
class DrillResultAdmin(admin.ModelAdmin):
    list_display = [
        "session",
        "step",
        "role",
        "spot",
        "is_correct",
        "time_taken_ms",
        "attempted_at",
    ]
    list_filter = ["is_correct", "role", "spot", "step__mechanic__fight"]
    search_fields = ["session__session_key", "step__title", "step__mechanic__name"]
    readonly_fields = ["attempted_at"]
