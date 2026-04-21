from django.contrib import admin

from .models import (
    DrillResult,
    Fight,
    Mechanic,
    MechanicStep,
    RaidTier,
    RoleVariant,
    UserSession,
)


class FightInline(admin.TabularInline):
    model = Fight
    extra = 0
    fields = ["slug", "short_name", "boss_name", "difficulty", "order", "is_active"]


@admin.register(RaidTier)
class RaidTierAdmin(admin.ModelAdmin):
    list_display = ["name", "expansion", "patch", "order", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [FightInline]


class MechanicInline(admin.TabularInline):
    model = Mechanic
    extra = 0
    fields = ["slug", "name", "phase_name", "order", "difficulty_rating"]


@admin.register(Fight)
class FightAdmin(admin.ModelAdmin):
    list_display = ["short_name", "boss_name", "difficulty", "raid_tier", "order", "is_active"]
    list_filter = ["difficulty", "raid_tier"]
    prepopulated_fields = {"slug": ("short_name",)}
    inlines = [MechanicInline]


class MechanicStepInline(admin.StackedInline):
    model = MechanicStep
    extra = 0


@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display = ["name", "fight", "phase_name", "order", "difficulty_rating"]
    list_filter = ["fight", "difficulty_rating"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [MechanicStepInline]


class RoleVariantInline(admin.TabularInline):
    model = RoleVariant
    extra = 0


@admin.register(MechanicStep)
class MechanicStepAdmin(admin.ModelAdmin):
    list_display = ["title", "mechanic", "order", "action_type", "timer_seconds"]
    list_filter = ["action_type"]
    inlines = [RoleVariantInline]


@admin.register(RoleVariant)
class RoleVariantAdmin(admin.ModelAdmin):
    list_display = ["step", "role", "spot"]
    list_filter = ["role", "spot"]


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ["session_key", "created_at"]
    readonly_fields = ["session_key", "created_at"]


@admin.register(DrillResult)
class DrillResultAdmin(admin.ModelAdmin):
    list_display = ["session", "step", "role", "spot", "is_correct", "time_taken_ms", "attempted_at"]
    list_filter = ["is_correct", "role", "spot"]
    readonly_fields = ["attempted_at"]
