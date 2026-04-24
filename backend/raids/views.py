"""API views for the raids app."""

import copy
import json

from django.db.models import Avg, Count, Q
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

from .engine import evaluate_step
from .models import (
    DrillResult,
    Fight,
    Mechanic,
    MechanicStep,
    RaidTier,
    RoleVariant,
    UserSession,
)
from .serializers import (
    DrillPlanSerializer,
    FightDetailSerializer,
    FightListSerializer,
    MechanicDetailSerializer,
    MechanicListSerializer,
    RaidTierDetailSerializer,
    RaidTierListSerializer,
    SessionStatsSerializer,
    SimulateStepSerializer,
    StepResultSerializer,
)


# ---------------------------------------------------------------------------
# Raid tiers
# ---------------------------------------------------------------------------

class RaidTierListView(generics.ListAPIView):
    queryset = RaidTier.objects.filter(is_active=True)
    serializer_class = RaidTierListSerializer


class RaidTierDetailView(generics.RetrieveAPIView):
    queryset = RaidTier.objects.filter(is_active=True).prefetch_related("fights")
    serializer_class = RaidTierDetailSerializer
    lookup_field = "slug"


# ---------------------------------------------------------------------------
# Fights
# ---------------------------------------------------------------------------

class FightListView(generics.ListAPIView):
    serializer_class = FightListSerializer

    def get_queryset(self):
        qs = Fight.objects.filter(is_active=True).select_related("raid_tier")
        tier_slug = self.request.query_params.get("tier")
        if tier_slug:
            qs = qs.filter(raid_tier__slug=tier_slug)
        difficulty = self.request.query_params.get("difficulty")
        if difficulty:
            qs = qs.filter(difficulty=difficulty.upper())
        return qs


class FightDetailView(generics.RetrieveAPIView):
    queryset = (
        Fight.objects.filter(is_active=True)
        .select_related("raid_tier")
        .prefetch_related("mechanics")
    )
    serializer_class = FightDetailSerializer
    lookup_field = "slug"


class FightDrillPlanView(APIView):
    """
    GET /api/fights/<slug>/drill/?phase=<phase_name>

    Returns an ordered drill plan for a full fight or a single phase,
    with every mechanic's steps + role variants inlined.
    """

    def get(self, request, slug):
        try:
            fight = (
                Fight.objects.filter(is_active=True)
                .prefetch_related("mechanics__steps__role_variants")
                .get(slug=slug)
            )
        except Fight.DoesNotExist:
            return Response(
                {"error": "Fight not found."}, status=status.HTTP_404_NOT_FOUND
            )

        mechanics = list(fight.mechanics.all().order_by("order"))
        phase = request.query_params.get("phase", "").strip()
        scope = "full"
        if phase:
            mechanics = [m for m in mechanics if m.phase_name == phase]
            scope = phase
            if not mechanics:
                return Response(
                    {"error": f"No mechanics found for phase '{phase}'."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        payload = {
            "fight": {
                "slug": fight.slug,
                "short_name": fight.short_name,
                "name": fight.name,
                "boss_name": fight.boss_name,
                "arena_shape": fight.arena_shape,
                "arena_image_url": fight.arena_image_url,
                "boss_image_url": fight.boss_image_url,
            },
            "scope": scope,
            "mechanics": MechanicDetailSerializer(mechanics, many=True).data,
        }
        return Response(DrillPlanSerializer(payload).data)


# ---------------------------------------------------------------------------
# Mechanics
# ---------------------------------------------------------------------------

class MechanicListView(generics.ListAPIView):
    serializer_class = MechanicListSerializer

    def get_queryset(self):
        qs = Mechanic.objects.all()
        fight_slug = self.request.query_params.get("fight")
        if fight_slug:
            qs = qs.filter(fight__slug=fight_slug)
        return qs


class MechanicDetailView(generics.RetrieveAPIView):
    queryset = Mechanic.objects.prefetch_related(
        "steps__role_variants"
    ).select_related("fight")
    serializer_class = MechanicDetailSerializer
    lookup_field = "pk"


# ---------------------------------------------------------------------------
# Simulation / Validation
# ---------------------------------------------------------------------------

@method_decorator(csrf_exempt, name="dispatch")
class SimulateStepView(APIView):
    """
    POST /api/simulate-step/

    Accepts the user's answer for a mechanic step and returns evaluation.
    Optionally records the result to a session.
    """
    def post(self, request):
        ser = SimulateStepSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        try:
            step = MechanicStep.objects.prefetch_related("role_variants").get(
                pk=data["step_id"]
            )
        except MechanicStep.DoesNotExist:
            return Response(
                {"error": "Step not found."}, status=status.HTTP_404_NOT_FOUND
            )

        result = evaluate_step(
            step=step,
            role=data["role"],
            spot=int(data.get("spot", 1)),
            submitted_x=data.get("submitted_x"),
            submitted_y=data.get("submitted_y"),
            submitted_choice=data.get("submitted_choice", ""),
        )

        # Persist to session if session_key provided
        session_key = data.get("session_key", "")
        if session_key:
            session, _ = UserSession.objects.get_or_create(session_key=session_key)
            DrillResult.objects.create(
                session=session,
                step=step,
                role=data["role"],
                spot=int(data.get("spot", 1)),
                submitted_x=data.get("submitted_x"),
                submitted_y=data.get("submitted_y"),
                submitted_choice=data.get("submitted_choice", ""),
                is_correct=result.is_correct,
                time_taken_ms=data.get("time_taken_ms", 0),
            )

        return Response(StepResultSerializer(result).data)


# ---------------------------------------------------------------------------
# Session stats
# ---------------------------------------------------------------------------

class SessionStatsView(APIView):
    """GET /api/sessions/<session_key>/stats/"""

    def get(self, request, session_key):
        try:
            session = UserSession.objects.get(session_key=session_key)
        except UserSession.DoesNotExist:
            return Response(
                {"error": "Session not found."}, status=status.HTTP_404_NOT_FOUND
            )

        results = session.results.all()
        total = results.count()
        if total == 0:
            return Response(
                {"error": "No results in this session."},
                status=status.HTTP_404_NOT_FOUND,
            )

        correct = results.filter(is_correct=True).count()
        incorrect = total - correct
        accuracy = correct / total
        avg_time = results.aggregate(avg=Avg("time_taken_ms"))["avg"] or 0

        # Per-mechanic breakdown
        per_mechanic = []
        mechanic_ids = (
            results.values_list("step__mechanic_id", flat=True).distinct()
        )
        for mid in mechanic_ids:
            mech_results = results.filter(step__mechanic_id=mid)
            mech = mech_results.first().step.mechanic
            m_total = mech_results.count()
            m_correct = mech_results.filter(is_correct=True).count()
            per_mechanic.append({
                "mechanic_id": mid,
                "mechanic_name": mech.name,
                "total": m_total,
                "correct": m_correct,
                "accuracy": m_correct / m_total if m_total else 0,
            })

        grade = _compute_grade(accuracy)

        payload = {
            "session_key": session_key,
            "total_steps": total,
            "correct": correct,
            "incorrect": incorrect,
            "accuracy": round(accuracy, 4),
            "avg_time_ms": round(avg_time, 1),
            "grade": grade,
            "per_mechanic": per_mechanic,
        }
        return Response(SessionStatsSerializer(payload).data)


# ---------------------------------------------------------------------------
# WtfDig importer
# ---------------------------------------------------------------------------

@method_decorator(csrf_exempt, name="dispatch")
class WtfdigPreviewView(APIView):
    """
    POST /api/import/preview/
    Body: {"url": "https://wtfdig.info/74/m9s#toxic"}

    Fetches the page, calls Claude to generate structured fight data,
    and returns a preview JSON the frontend can walk the user through.
    """

    def post(self, request):
        from .importer import fetch_page_text, generate_preview, parse_wtfdig_url

        url = (request.data.get("url") or "").strip()
        if not url:
            return Response({"error": "url is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            parsed = parse_wtfdig_url(url)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        scraped = fetch_page_text(url)

        try:
            preview = generate_preview(
                url=url,
                fight_slug=parsed["fight_slug"],
                strat=parsed["strat"],
                scraped_text=scraped,
            )
        except (ImportError, EnvironmentError) as exc:
            return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except json.JSONDecodeError as exc:
            return Response(
                {"error": f"AI returned invalid JSON: {exc}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as exc:
            return Response(
                {"error": f"Import failed: {exc}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(preview)


@method_decorator(csrf_exempt, name="dispatch")
class ImportSaveView(APIView):
    """
    POST /api/import/save/
    Body: the confirmed preview JSON (fight + tier + mechanics).

    Creates or replaces the fight (and its whole mechanic tree) in the DB.
    Existing fight with the same slug is deleted first so this is idempotent.
    """

    def post(self, request):
        data = copy.deepcopy(request.data)

        fight_data = data.get("fight") or {}
        tier_data  = data.get("tier")  or {}
        mechanics_data = data.get("mechanics") or []

        if not fight_data.get("slug"):
            return Response({"error": "fight.slug is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not tier_data.get("slug"):
            return Response({"error": "tier.slug is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tier, _ = RaidTier.objects.get_or_create(
                slug=tier_data["slug"],
                defaults={
                    "name":      tier_data.get("name", tier_data["slug"]),
                    "expansion": tier_data.get("expansion", ""),
                    "patch":     tier_data.get("patch", ""),
                    "order":     tier_data.get("order", 99),
                },
            )

            # Clean-replace: remove any previous version of this fight.
            Fight.objects.filter(slug=fight_data["slug"]).delete()

            fight = Fight.objects.create(
                raid_tier=tier,
                slug=fight_data["slug"],
                name=fight_data.get("name", fight_data["slug"]),
                short_name=fight_data.get("short_name", fight_data["slug"].upper()),
                boss_name=fight_data.get("boss_name", ""),
                difficulty=fight_data.get("difficulty", "SAVAGE"),
                arena_shape=fight_data.get("arena_shape", "SQUARE"),
                order=fight_data.get("order", 99),
                arena_image_url=fight_data.get("arena_image_url", ""),
                boss_image_url=fight_data.get("boss_image_url", ""),
            )

            for i, mech_data in enumerate(mechanics_data, start=1):
                steps_data = mech_data.pop("steps", [])
                mech_data.setdefault("order", i)
                mech = Mechanic.objects.create(fight=fight, **mech_data)

                for j, step_data in enumerate(steps_data, start=1):
                    variants_data = step_data.pop("role_variants", [])
                    step_data.setdefault("order", j)
                    # Ensure JSON fields have correct defaults
                    step_data.setdefault("arena_state", {})
                    step_data.setdefault("choices", [])
                    step = MechanicStep.objects.create(mechanic=mech, **step_data)

                    for variant_data in variants_data:
                        variant_data.setdefault("correct_position", {})
                        variant_data.setdefault("correct_choice", "")
                        variant_data.setdefault("alt_positions", [])
                        variant_data.setdefault("safe_zones", [])
                        RoleVariant.objects.create(step=step, **variant_data)

        except Exception as exc:
            return Response(
                {"error": f"Save failed: {exc}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        fight_obj = (
            Fight.objects.select_related("raid_tier")
            .prefetch_related("mechanics")
            .get(pk=fight.pk)
        )
        return Response(
            {
                "success": True,
                "fight": FightDetailSerializer(fight_obj).data,
                "message": (
                    f"Imported {fight.short_name} with "
                    f"{len(mechanics_data)} mechanic(s)."
                ),
            },
            status=status.HTTP_201_CREATED,
        )


def _compute_grade(accuracy: float) -> str:
    if accuracy >= 0.95:
        return "S"
    elif accuracy >= 0.85:
        return "A"
    elif accuracy >= 0.70:
        return "B"
    elif accuracy >= 0.50:
        return "C"
    return "D"
