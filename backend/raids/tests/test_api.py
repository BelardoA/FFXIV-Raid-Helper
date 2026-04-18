"""Integration tests for the raids REST API."""

from django.test import TestCase
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


class SessionStatsAPITests(APITestBase):
    def test_nonexistent_session(self):
        resp = self.client.get("/api/sessions/no-such-session/stats/")
        self.assertEqual(resp.status_code, 404)
