"""Integration tests for the raids REST API."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from rest_framework.test import APIClient

from raids.models import (
    Fight,
    Mechanic,
    MechanicStep,
    RaidTier,
    RoleVariant,
)


class APITestBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tier = RaidTier.objects.create(
            slug="test-tier", name="Test Tier", patch="7.0", order=1,
        )
        cls.fight = Fight.objects.create(
            raid_tier=cls.tier, slug="test-fight", name="Test Fight",
            short_name="TF", boss_name="Boss", difficulty="SAVAGE",
            arena_shape="SQUARE", order=1,
        )
        cls.mech = Mechanic.objects.create(
            fight=cls.fight, slug="test-mech", name="Test Mech",
            phase_name="P1", order=1, difficulty_rating=3,
        )
        cls.step = MechanicStep.objects.create(
            mechanic=cls.mech, order=1, title="Step 1",
            action_type="POSITION",
            arena_state={"boss_position": {"x": 0.5, "y": 0.5}},
            explanation="Stand right.",
        )
        RoleVariant.objects.create(
            step=cls.step, role="TANK",
            correct_position={"x": 0.75, "y": 0.5},
        )

    def setUp(self):
        self.client = APIClient()


class RaidTierAPITests(APITestBase):
    def test_list_raids(self):
        resp = self.client.get("/api/raids/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 1)
        self.assertEqual(resp.json()["results"][0]["slug"], "test-tier")

    def test_raid_detail(self):
        resp = self.client.get("/api/raids/test-tier/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data["fights"]), 1)
        self.assertEqual(data["fights"][0]["short_name"], "TF")


class FightAPITests(APITestBase):
    def test_list_fights(self):
        resp = self.client.get("/api/fights/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 1)

    def test_fight_detail(self):
        resp = self.client.get("/api/fights/test-fight/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["boss_name"], "Boss")
        self.assertEqual(len(data["mechanics"]), 1)

    def test_filter_by_tier(self):
        resp = self.client.get("/api/fights/?tier=test-tier")
        self.assertEqual(resp.json()["count"], 1)
        resp2 = self.client.get("/api/fights/?tier=nonexistent")
        self.assertEqual(resp2.json()["count"], 0)

    def test_filter_by_difficulty(self):
        resp = self.client.get("/api/fights/?difficulty=savage")
        self.assertEqual(resp.json()["count"], 1)
        resp2 = self.client.get("/api/fights/?difficulty=ultimate")
        self.assertEqual(resp2.json()["count"], 0)

    def test_fight_list_works_with_admin_session_cookie(self):
        admin_user = get_user_model().objects.create_superuser(
            username="fight-admin",
            email="fight-admin@example.com",
            password="password123",
        )
        client = Client(enforce_csrf_checks=True, HTTP_ORIGIN="http://localhost:3000")
        client.force_login(admin_user)
        resp = client.get("/api/fights/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 1)


class DrillPlanAPITests(APITestBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # Add a second mechanic in a different phase to exercise filtering.
        cls.mech2 = Mechanic.objects.create(
            fight=cls.fight, slug="test-mech-2", name="Test Mech P2",
            phase_name="P2", order=2, difficulty_rating=4,
        )
        cls.step2 = MechanicStep.objects.create(
            mechanic=cls.mech2, order=1, title="Step 2A",
            action_type="POSITION",
        )
        RoleVariant.objects.create(
            step=cls.step2, role="HEALER",
            correct_position={"x": 0.3, "y": 0.3},
        )

    def test_full_fight_scope(self):
        resp = self.client.get("/api/fights/test-fight/drill/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["scope"], "full")
        self.assertEqual(data["fight"]["slug"], "test-fight")
        self.assertEqual(len(data["mechanics"]), 2)
        # Mechanics ordered by `order`
        self.assertEqual(data["mechanics"][0]["slug"], "test-mech")
        self.assertEqual(data["mechanics"][1]["slug"], "test-mech-2")
        # Steps + role variants are inlined
        self.assertEqual(len(data["mechanics"][0]["steps"]), 1)
        self.assertEqual(
            len(data["mechanics"][0]["steps"][0]["role_variants"]), 1
        )

    def test_phase_scope(self):
        resp = self.client.get("/api/fights/test-fight/drill/?phase=P2")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["scope"], "P2")
        self.assertEqual(len(data["mechanics"]), 1)
        self.assertEqual(data["mechanics"][0]["slug"], "test-mech-2")

    def test_unknown_phase_returns_404(self):
        resp = self.client.get("/api/fights/test-fight/drill/?phase=Nonexistent")
        self.assertEqual(resp.status_code, 404)

    def test_unknown_fight_returns_404(self):
        resp = self.client.get("/api/fights/nope/drill/")
        self.assertEqual(resp.status_code, 404)

    def test_drill_plan_works_with_admin_session_cookie(self):
        admin_user = get_user_model().objects.create_superuser(
            username="drill-admin",
            email="drill-admin@example.com",
            password="password123",
        )
        client = Client(enforce_csrf_checks=True, HTTP_ORIGIN="http://localhost:3000")
        client.force_login(admin_user)
        resp = client.get("/api/fights/test-fight/drill/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["fight"]["slug"], "test-fight")


class MechanicAPITests(APITestBase):
    def test_list_mechanics(self):
        resp = self.client.get("/api/mechanics/?fight=test-fight")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 1)

    def test_mechanic_detail_includes_steps_and_variants(self):
        resp = self.client.get(f"/api/mechanics/{self.mech.pk}/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data["steps"]), 1)
        self.assertEqual(len(data["steps"][0]["role_variants"]), 1)
        self.assertEqual(data["steps"][0]["role_variants"][0]["role"], "TANK")


class SimulateStepAPITests(APITestBase):
    def test_correct_submission(self):
        resp = self.client.post("/api/simulate-step/", {
            "step_id": self.step.pk,
            "role": "TANK",
            "submitted_x": 0.75,
            "submitted_y": 0.5,
            "session_key": "api-test-sess",
            "time_taken_ms": 2000,
        }, format="json")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["is_correct"])

    def test_incorrect_submission(self):
        resp = self.client.post("/api/simulate-step/", {
            "step_id": self.step.pk,
            "role": "TANK",
            "submitted_x": 0.1,
            "submitted_y": 0.1,
        }, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.json()["is_correct"])

    def test_missing_step(self):
        resp = self.client.post("/api/simulate-step/", {
            "step_id": 99999,
            "role": "TANK",
            "submitted_x": 0.5,
            "submitted_y": 0.5,
        }, format="json")
        self.assertEqual(resp.status_code, 404)

    def test_session_recording(self):
        self.client.post("/api/simulate-step/", {
            "step_id": self.step.pk,
            "role": "TANK",
            "submitted_x": 0.75,
            "submitted_y": 0.5,
            "session_key": "record-test",
            "time_taken_ms": 1500,
        }, format="json")
        resp = self.client.get("/api/sessions/record-test/stats/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total_steps"], 1)
        self.assertEqual(data["correct"], 1)
        self.assertEqual(data["grade"], "S")

    def test_simulate_step_is_csrf_exempt(self):
        csrf_client = Client(enforce_csrf_checks=True)
        resp = csrf_client.post("/api/simulate-step/", {
            "step_id": self.step.pk,
            "role": "TANK",
            "submitted_x": 0.75,
            "submitted_y": 0.5,
        }, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["is_correct"])

    def test_simulate_step_works_with_admin_session_cookie(self):
        admin_user = get_user_model().objects.create_superuser(
            username="api-admin",
            email="admin@example.com",
            password="password123",
        )
        csrf_client = Client(enforce_csrf_checks=True, HTTP_ORIGIN="http://localhost:3000")
        csrf_client.force_login(admin_user)
        resp = csrf_client.post("/api/simulate-step/", {
            "step_id": self.step.pk,
            "role": "TANK",
            "submitted_x": 0.75,
            "submitted_y": 0.5,
        }, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["is_correct"])


class SessionStatsAPITests(APITestBase):
    def test_nonexistent_session(self):
        resp = self.client.get("/api/sessions/no-such-session/stats/")
        self.assertEqual(resp.status_code, 404)
