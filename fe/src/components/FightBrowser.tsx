"use client";

import { useEffect, useState } from "react";
import { fetchRaidTiers, fetchFights } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import type { Fight, RaidTier } from "@/lib/types";

function DifficultyBadge({ difficulty }: { difficulty: string }) {
  const cls =
    difficulty === "ULTIMATE"
      ? "bg-purple-500/15 text-purple-400 border-purple-500/30"
      : difficulty === "SAVAGE"
        ? "bg-orange-500/15 text-orange-400 border-orange-500/30"
        : "bg-yellow-500/15 text-yellow-400 border-yellow-500/30";
  return (
    <span className={`text-[0.6rem] px-2 py-0.5 rounded-full border ${cls}`}>
      {difficulty}
    </span>
  );
}

function Stars({ count }: { count: number }) {
  return (
    <span className="text-xs tracking-wider">
      {Array.from({ length: 5 }, (_, i) => (
        <span key={i} className={i < count ? "text-gold" : "text-white/15"}>
          ★
        </span>
      ))}
    </span>
  );
}

export default function FightBrowser() {
  const selectFight = useAppStore((s) => s.selectFight);
  const [tiers, setTiers] = useState<RaidTier[]>([]);
  const [fights, setFights] = useState<Fight[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([fetchRaidTiers(), fetchFights()])
      .then(([t, f]) => {
        setTiers(t);
        setFights(f);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center py-24">
        <span className="text-gold animate-pulse font-cinzel">
          Loading fights...
        </span>
      </div>
    );
  }

  return (
    <section className="max-w-4xl mx-auto px-4 py-8">
      <h2 className="font-cinzel text-2xl text-gold-light tracking-wider mb-8 text-center">
        Choose a Fight
      </h2>

      {tiers.map((tier) => {
        const tierFights = fights.filter(
          (f) => f.raid_tier_name === tier.name
        );
        if (tierFights.length === 0) return null;

        return (
          <div key={tier.slug} className="mb-10">
            <div className="flex items-center gap-3 mb-4">
              <h3 className="font-cinzel text-lg text-gold tracking-wider">
                {tier.name}
              </h3>
              <span className="text-xs text-text-muted">
                {tier.expansion} &bull; Patch {tier.patch}
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {tierFights.map((fight) => (
                <button
                  key={fight.slug}
                  onClick={() => selectFight(fight)}
                  className="group text-left p-5 rounded-xl border border-white/5 bg-bg-card hover:bg-bg-card-hover hover:border-gold/30 transition-all duration-200"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <span className="font-cinzel text-lg font-bold text-gold-light group-hover:text-gold transition-colors">
                        {fight.short_name}
                      </span>
                      <DifficultyBadge difficulty={fight.difficulty} />
                    </div>
                    <span className="text-xs text-text-muted">
                      {fight.mechanic_count} mechanics
                    </span>
                  </div>
                  <p className="text-sm text-white/50 mb-1">
                    {fight.boss_name}
                  </p>
                  <p className="text-xs text-text-muted">{fight.name}</p>
                </button>
              ))}
            </div>
          </div>
        );
      })}
    </section>
  );
}
