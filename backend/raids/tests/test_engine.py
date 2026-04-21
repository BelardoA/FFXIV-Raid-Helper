"""Unit tests for the mechanic simulation engine."""

from django.test import TestCase

from raids.engine import DEFAULT_TOLERANCE, evaluate_choice, evaluate_position, evaluate_step
from raids.models import (
    Fight,
    Mechanic,
    MechanicStep,
    RaidTier,
    RoleVariant,
)


class EvaluatePositionTests(TestCase):
    def test_exact_match(self):
        ok, dist = evaluate_position(0.5, 0.5, 0.5, 0.5, 0.12)
        self.assertTrue(ok)
        self.assertAlmostEqual(dist, 0.0)

    def test_within_tolerance(self):
        ok, dist = evaluate_position(0.55, 0.5, 0.5, 0.5, 0.12)
        self.assertTrue(ok)
        self.assertAlmostEqual(dist, 0.05, places=4)

    def test_outside_tolerance(self):
        ok, dist = evaluate_position(0.1, 0.1, 0.9, 0.9, 0.12)
        self.assertFalse(ok)
        self.assertGreater(dist, 0.12)

    def test_alt_position_match(self):
        alts = [{"x": 0.2, "y": 0.2}]
        ok, dist = evaluate_position(0.2, 0.2, 0.8, 0.8, 0.12, alt_positions=alts)
        self.assertTrue(ok)

    def test_alt_position_no_match(self):
        alts = [{"x": 0.2, "y": 0.2}]
        ok, dist = evaluate_position(0.5, 0.5, 0.8, 0.8, 0.12, alt_positions=alts)
        self.assertFalse(ok)

    def test_boundary_tolerance(self):
        # Exactly at the edge of tolerance
        ok, dist = evaluate_position(0.62, 0.5, 0.5, 0.5, 0.12)
        self.assertTrue(ok)
        ok2, dist2 = evaluate_position(0.63, 0.5, 0.5, 0.5, 0.12)
        self.assertFalse(ok2)


class EvaluateChoiceTests(TestCase):
    def test_exact_match(self):
        self.assertTrue(evaluate_choice("north", "north"))

    def test_case_insensitive(self):
        self.assertTrue(evaluate_choice("NORTH", "north"))

    def test_whitespace_stripped(self):
        self.assertTrue(evaluate_choice("  north  ", "north"))

    def test_wrong_choice(self):
        self.assertFalse(evaluate_choice("south", "north"))


class EvaluateStepTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        tier = RaidTier.objects.create(slug="test-tier", name="Test Tier", order=1)
        fight = Fight.objects.create(
            raid_tier=tier, slug="test-fight", name="Test Fight",
            short_name="TF", boss_name="Boss", difficulty="SAVAGE", order=1,
        )
        mech = Mechanic.objects.create(
            fight=fight, slug="test-mech", name="Test Mechanic", order=1,
        )
        cls.step1 = MechanicStep.objects.create(
            mechanic=mech, order=1, title="Step 1",
            action_type="POSITION", arena_state={},
            explanation="Go right side.",
        )
        RoleVariant.objects.create(
            step=cls.step1, role="TANK",
            correct_position={"x": 0.75, "y": 0.5},
        )
        RoleVariant.objects.create(
            step=cls.step1, role="HEALER",
            correct_position={"x": 0.75, "y": 0.7},
        )

        cls.step2 = MechanicStep.objects.create(
            mechanic=mech, order=2, title="Step 2",
            action_type="CHOICE",
            choices=[{"id": "spread", "label": "Spread"}, {"id": "stack", "label": "Stack"}],
            explanation="You should spread.",
        )
        RoleVariant.objects.create(
            step=cls.step2, role="TANK", correct_choice="spread",
        )
        RoleVariant.objects.create(
            step=cls.step2, role="HEALER", correct_choice="stack",
        )

    def test_correct_position(self):
        result = evaluate_step(self.step1, "TANK", submitted_x=0.75, submitted_y=0.5)
        self.assertTrue(result.is_correct)
        self.assertTrue(result.has_next_step)
        self.assertEqual(result.next_step_order, 2)
        self.assertEqual(result.explanation, "Go right side.")

    def test_incorrect_position(self):
        result = evaluate_step(self.step1, "TANK", submitted_x=0.1, submitted_y=0.1)
        self.assertFalse(result.is_correct)

    def test_role_differentiation(self):
        tank = evaluate_step(self.step1, "TANK", submitted_x=0.75, submitted_y=0.5)
        healer = evaluate_step(self.step1, "HEALER", submitted_x=0.75, submitted_y=0.5)
        # Tank should be correct, healer's correct pos is different y
        self.assertTrue(tank.is_correct)
        # Healer at (0.75, 0.5) is 0.2 away from (0.75, 0.7) — outside tolerance
        self.assertFalse(healer.is_correct)

    def test_correct_choice(self):
        result = evaluate_step(self.step2, "TANK", submitted_choice="spread")
        self.assertTrue(result.is_correct)
        self.assertFalse(result.has_next_step)

    def test_incorrect_choice(self):
        result = evaluate_step(self.step2, "HEALER", submitted_choice="spread")
        self.assertFalse(result.is_correct)

    def test_missing_role_variant(self):
        result = evaluate_step(self.step1, "MELEE", submitted_x=0.5, submitted_y=0.5)
        self.assertFalse(result.is_correct)
        self.assertIn("No solution defined", result.explanation)

    def test_spot_differentiation(self):
        """Two spots on the same role should resolve to different positions."""
        tier = RaidTier.objects.create(slug="spot-tier", name="Spot Tier", order=77)
        fight = Fight.objects.create(
            raid_tier=tier, slug="spot-fight", name="Spot Fight",
            short_name="SF", boss_name="Boss", difficulty="SAVAGE", order=1,
        )
        mech = Mechanic.objects.create(
            fight=fight, slug="spot-mech", name="Spot Mechanic", order=1,
        )
        step = MechanicStep.objects.create(
            mechanic=mech, order=1, title="Spot step",
            action_type="POSITION",
        )
        RoleVariant.objects.create(
            step=step, role="TANK", spot=1,
            correct_position={"x": 0.3, "y": 0.5},
        )
        RoleVariant.objects.create(
            step=step, role="TANK", spot=2,
            correct_position={"x": 0.7, "y": 0.5},
        )
        t1 = evaluate_step(step, "TANK", spot=1, submitted_x=0.3, submitted_y=0.5)
        t2 = evaluate_step(step, "TANK", spot=2, submitted_x=0.7, submitted_y=0.5)
        wrong = evaluate_step(step, "TANK", spot=2, submitted_x=0.3, submitted_y=0.5)
        self.assertTrue(t1.is_correct)
        self.assertTrue(t2.is_correct)
        self.assertFalse(wrong.is_correct)

    def test_spot_fallback_to_one(self):
        """When only spot=1 exists, spot=2 requests fall back to it."""
        tier = RaidTier.objects.create(slug="fb-tier", name="Fb Tier", order=78)
        fight = Fight.objects.create(
            raid_tier=tier, slug="fb-fight", name="Fb Fight",
            short_name="FB", boss_name="Boss", difficulty="SAVAGE", order=1,
        )
        mech = Mechanic.objects.create(
            fight=fight, slug="fb-mech", name="Fb Mechanic", order=1,
        )
        step = MechanicStep.objects.create(
            mechanic=mech, order=1, title="Fb step",
            action_type="POSITION",
        )
        RoleVariant.objects.create(
            step=step, role="HEALER", spot=1,
            correct_position={"x": 0.5, "y": 0.2},
        )
        result = evaluate_step(step, "HEALER", spot=2, submitted_x=0.5, submitted_y=0.2)
        self.assertTrue(result.is_correct)

    def test_no_position_submitted(self):
        result = evaluate_step(self.step1, "TANK")
        self.assertFalse(result.is_correct)
        self.assertEqual(result.explanation, "No position submitted.")

    def test_deterministic(self):
        """Same input always produces same output."""
        r1 = evaluate_step(self.step1, "TANK", submitted_x=0.6, submitted_y=0.5)
        r2 = evaluate_step(self.step1, "TANK", submitted_x=0.6, submitted_y=0.5)
        self.assertEqual(r1.is_correct, r2.is_correct)
        self.assertEqual(r1.distance, r2.distance)


class StepDefaultToleranceTests(TestCase):
    """Tests for the three-tier tolerance fallback: variant → step → global."""

    @classmethod
    def setUpTestData(cls):
        tier = RaidTier.objects.create(slug="tol-tier", name="Tol Tier", order=99)
        fight = Fight.objects.create(
            raid_tier=tier, slug="tol-fight", name="Tol Fight",
            short_name="TL", boss_name="Boss", difficulty="SAVAGE", order=1,
        )
        mech = Mechanic.objects.create(
            fight=fight, slug="tol-mech", name="Tol Mechanic", order=1,
        )

        # Step with loose default_tolerance (0.25)
        cls.loose_step = MechanicStep.objects.create(
            mechanic=mech, order=1, title="Loose Step",
            action_type="POSITION", default_tolerance=0.25,
        )
        # Variant with NO tolerance override — should use step's 0.25
        RoleVariant.objects.create(
            step=cls.loose_step, role="TANK",
            correct_position={"x": 0.5, "y": 0.5},
        )
        # Variant WITH tolerance override (0.08) — should override step's 0.25
        RoleVariant.objects.create(
            step=cls.loose_step, role="HEALER",
            correct_position={"x": 0.5, "y": 0.5},
            tolerance=0.08,
        )

        # Step with NO default_tolerance — should use global DEFAULT_TOLERANCE
        cls.default_step = MechanicStep.objects.create(
            mechanic=mech, order=2, title="Default Step",
            action_type="POSITION",
        )
        RoleVariant.objects.create(
            step=cls.default_step, role="TANK",
            correct_position={"x": 0.5, "y": 0.5},
        )

    def test_step_default_tolerance_used(self):
        """Step default_tolerance is used when variant has no override."""
        # 0.20 away — outside global 0.12 but inside step's 0.25
        result = evaluate_step(self.loose_step, "TANK", submitted_x=0.7, submitted_y=0.5)
        self.assertTrue(result.is_correct)
        self.assertEqual(result.tolerance_used, 0.25)

    def test_variant_tolerance_overrides_step(self):
        """Variant tolerance takes priority over step default_tolerance."""
        # 0.10 away — inside step's 0.25 but outside variant's 0.08
        result = evaluate_step(self.loose_step, "HEALER", submitted_x=0.6, submitted_y=0.5)
        self.assertFalse(result.is_correct)
        self.assertEqual(result.tolerance_used, 0.08)

    def test_global_default_when_both_null(self):
        """Falls back to DEFAULT_TOLERANCE when step and variant are both null."""
        result = evaluate_step(self.default_step, "TANK", submitted_x=0.5, submitted_y=0.5)
        self.assertTrue(result.is_correct)
        self.assertEqual(result.tolerance_used, DEFAULT_TOLERANCE)
