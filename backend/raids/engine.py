"""
Mechanic simulation engine.

Pure-function evaluator: given a MechanicStep, a role, and the user's action,
determine correctness and return structured feedback.  No fight-specific logic
lives here — all behaviour is driven by the data in MechanicStep + RoleVariant.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

from .models import ActionType, MechanicStep, RoleVariant

# Default tolerance: fraction of the arena width (0-1 coordinate space).
DEFAULT_TOLERANCE = 0.12


@dataclass(frozen=True)
class StepResult:
    """Immutable result returned by the engine after evaluating one step."""
    is_correct: bool
    explanation: str
    correct_position: Optional[dict]  # {x, y} or None
    correct_choice: Optional[str]
    distance: Optional[float]  # Euclidean distance from correct pos, or None
    tolerance_used: float
    has_next_step: bool
    next_step_order: Optional[int]


def evaluate_position(
    submitted_x: float,
    submitted_y: float,
    correct_x: float,
    correct_y: float,
    tolerance: float,
    alt_positions: list[dict] | None = None,
) -> tuple[bool, float]:
    """
    Check if submitted position is within tolerance of correct position
    or any alternative position.

    Returns (is_correct, best_distance).
    """
    dx = submitted_x - correct_x
    dy = submitted_y - correct_y
    best_distance = math.sqrt(dx * dx + dy * dy)
    is_correct = best_distance <= tolerance

    # Check alternative positions
    if not is_correct and alt_positions:
        for alt in alt_positions:
            alt_dx = submitted_x - alt.get("x", 0)
            alt_dy = submitted_y - alt.get("y", 0)
            alt_dist = math.sqrt(alt_dx * alt_dx + alt_dy * alt_dy)
            if alt_dist <= tolerance:
                is_correct = True
                best_distance = min(best_distance, alt_dist)
                break
            best_distance = min(best_distance, alt_dist)

    return is_correct, best_distance


def evaluate_choice(
    submitted_choice: str,
    correct_choice: str,
) -> bool:
    """Check if the submitted choice matches the correct one."""
    return submitted_choice.strip().lower() == correct_choice.strip().lower()


def evaluate_step(
    step: MechanicStep,
    role: str,
    submitted_x: float | None = None,
    submitted_y: float | None = None,
    submitted_choice: str | None = None,
) -> StepResult:
    """
    Evaluate a user's answer for a single mechanic step.

    This is the primary entry point for the engine.
    """
    # Resolve the role variant for this step+role
    try:
        variant = step.role_variants.get(role=role)
    except RoleVariant.DoesNotExist:
        # Fall back to any "universal" variant if one exists
        # (steps where all roles do the same thing might only have one variant)
        variants = list(step.role_variants.all())
        if len(variants) == 1:
            variant = variants[0]
        else:
            return StepResult(
                is_correct=False,
                explanation=f"No solution defined for role '{role}' on this step.",
                correct_position=None,
                correct_choice=None,
                distance=None,
                tolerance_used=DEFAULT_TOLERANCE,
                has_next_step=_has_next_step(step),
                next_step_order=_next_step_order(step),
            )

    tolerance = (
        variant.tolerance if variant.tolerance is not None
        else step.default_tolerance if step.default_tolerance is not None
        else DEFAULT_TOLERANCE
    )
    explanation = variant.explanation or step.explanation

    # Determine the next step
    has_next = _has_next_step(step)
    next_order = _next_step_order(step)

    # --- Evaluate based on action type ---

    if step.action_type == ActionType.POSITION:
        if submitted_x is None or submitted_y is None:
            return StepResult(
                is_correct=False,
                explanation="No position submitted.",
                correct_position=variant.correct_position,
                correct_choice=None,
                distance=None,
                tolerance_used=tolerance,
                has_next_step=has_next,
                next_step_order=next_order,
            )

        correct_pos = variant.correct_position
        cx = correct_pos.get("x", 0.5)
        cy = correct_pos.get("y", 0.5)

        is_correct, distance = evaluate_position(
            submitted_x, submitted_y, cx, cy, tolerance, variant.alt_positions
        )

        return StepResult(
            is_correct=is_correct,
            explanation=explanation,
            correct_position=variant.correct_position,
            correct_choice=None,
            distance=round(distance, 4),
            tolerance_used=tolerance,
            has_next_step=has_next,
            next_step_order=next_order,
        )

    elif step.action_type == ActionType.CHOICE:
        if not submitted_choice:
            return StepResult(
                is_correct=False,
                explanation="No choice submitted.",
                correct_position=None,
                correct_choice=variant.correct_choice,
                distance=None,
                tolerance_used=tolerance,
                has_next_step=has_next,
                next_step_order=next_order,
            )

        is_correct = evaluate_choice(submitted_choice, variant.correct_choice)

        return StepResult(
            is_correct=is_correct,
            explanation=explanation,
            correct_position=None,
            correct_choice=variant.correct_choice,
            distance=None,
            tolerance_used=tolerance,
            has_next_step=has_next,
            next_step_order=next_order,
        )

    # Unknown action type
    return StepResult(
        is_correct=False,
        explanation=f"Unknown action type: {step.action_type}",
        correct_position=None,
        correct_choice=None,
        distance=None,
        tolerance_used=tolerance,
        has_next_step=has_next,
        next_step_order=next_order,
    )


def _has_next_step(step: MechanicStep) -> bool:
    return step.mechanic.steps.filter(order__gt=step.order).exists()


def _next_step_order(step: MechanicStep) -> int | None:
    nxt = (
        step.mechanic.steps.filter(order__gt=step.order)
        .order_by("order")
        .values_list("order", flat=True)
        .first()
    )
    return nxt
