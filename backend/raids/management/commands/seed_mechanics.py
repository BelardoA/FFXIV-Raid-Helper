"""
Seed the database with M1S-M4S, M9S-M12S, and FRU mechanics.

Run:  python manage.py seed_mechanics
"""

import copy

from django.core.management.base import BaseCommand

from raids.models import (
    Fight,
    Mechanic,
    MechanicStep,
    RaidTier,
    RoleVariant,
)

from .seeds.m1s_m4s import AAC_LHW_TIER
from .seeds.fru import FRU_TIER
from .seeds.m9s import M9S_FIGHT
from .seeds.m10s import M10S_FIGHT
from .seeds.m11s import M11S_FIGHT
from .seeds.m12s import M12S_FIGHT

# ---------------------------------------------------------------------------
# Assemble SEED_DATA from per-fight modules
# ---------------------------------------------------------------------------

AAC_HW_TIER = {
    "tier": {
        "slug": "aac-hw",
        "name": "AAC Heavyweight",
        "expansion": "Dawntrail",
        "patch": "7.4",
        "order": 3,
    },
    "fights": [M9S_FIGHT, M10S_FIGHT, M11S_FIGHT, M12S_FIGHT],
}

SEED_DATA = [AAC_LHW_TIER, FRU_TIER, AAC_HW_TIER]


class Command(BaseCommand):
    help = "Seeds the database with M1S-M4S, M9S-M12S, and FRU mechanics."

    def handle(self, *args, **options):
        self.stdout.write("Clearing existing seed data...")
        RaidTier.objects.all().delete()

        # Deep copy so .pop() calls don't mutate the module-level dicts
        seed_data = copy.deepcopy(SEED_DATA)

        for tier_data in seed_data:
            tier_info = tier_data["tier"]
            self.stdout.write(f"  Creating tier: {tier_info['name']}")
            tier = RaidTier.objects.create(**tier_info)

            for fight_data in tier_data["fights"]:
                mechanics_data = fight_data.pop("mechanics")
                self.stdout.write(f"    Fight: {fight_data['short_name']}")
                fight = Fight.objects.create(raid_tier=tier, **fight_data)

                for mech_data in mechanics_data:
                    steps_data = mech_data.pop("steps")
                    mech = Mechanic.objects.create(fight=fight, **mech_data)

                    for step_data in steps_data:
                        variants_data = step_data.pop("role_variants")
                        step = MechanicStep.objects.create(mechanic=mech, **step_data)

                        for variant_data in variants_data:
                            RoleVariant.objects.create(step=step, **variant_data)

        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Seeded: "
                f"{RaidTier.objects.count()} tiers, "
                f"{Fight.objects.count()} fights, "
                f"{Mechanic.objects.count()} mechanics, "
                f"{MechanicStep.objects.count()} steps, "
                f"{RoleVariant.objects.count()} role variants."
            )
        )
