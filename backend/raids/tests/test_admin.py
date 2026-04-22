from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from raids.admin import RoleVariantAdminForm
from raids.models import Fight, Mechanic, MechanicStep, RaidTier, RoleVariant


class AdminPortalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password123",
        )
        cls.tier = RaidTier.objects.create(
            slug="arcadion",
            name="Arcadion",
            expansion="Dawntrail",
            patch="7.0",
            order=1,
        )
        cls.fight = Fight.objects.create(
            raid_tier=cls.tier,
            slug="m1s",
            name="AAC Light-heavyweight M1 (Savage)",
            short_name="M1S",
            boss_name="Black Cat",
            difficulty="SAVAGE",
            order=1,
        )
        cls.mechanic = Mechanic.objects.create(
            fight=cls.fight,
            slug="witch-hunt",
            name="Witch Hunt",
            phase_name="P1",
            order=1,
            tags=["spread"],
        )
        cls.step = MechanicStep.objects.create(
            mechanic=cls.mechanic,
            order=1,
            title="Spread Positions",
            action_type="POSITION",
            arena_state={"boss_position": {"x": 0.5, "y": 0.5}},
        )
        cls.variant = RoleVariant.objects.create(
            step=cls.step,
            role="TANK",
            spot=1,
            correct_position={"x": 0.7, "y": 0.3},
        )

    def setUp(self):
        self.client.force_login(self.superuser)

    def test_editor_index_renders(self):
        response = self.client.get(reverse("admin:raids_editor_index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Raid Content Editor")
        self.assertContains(response, self.fight.short_name)

    def test_editor_fight_page_renders_nested_content(self):
        response = self.client.get(reverse("admin:raids_editor_fight", args=[self.fight.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.mechanic.name)
        self.assertContains(response, self.step.title)
        self.assertContains(response, "Tank")

    def test_fight_changelist_shows_editor_link(self):
        response = self.client.get(reverse("admin:raids_fight_changelist"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("admin:raids_editor_fight", args=[self.fight.pk]))

    def test_role_variant_form_uses_arena_picker_shape_from_instance(self):
        form = RoleVariantAdminForm(instance=self.variant)
        widget = form.fields["correct_position"].widget
        self.assertEqual(widget.attrs["data-position-picker"], "true")
        self.assertEqual(widget.attrs["data-arena-shape"], "SQUARE")

    def test_role_variant_form_uses_initial_step_for_picker_shape(self):
        self.fight.arena_shape = "CIRCLE"
        self.fight.save(update_fields=["arena_shape"])
        form = RoleVariantAdminForm(initial={"step": self.step.pk})
        widget = form.fields["correct_position"].widget
        self.assertEqual(widget.attrs["data-arena-shape"], "CIRCLE")
