"use client";

import { usePathname, useRouter } from "next/navigation";
import { useAppStore } from "@/lib/store";

const ROLE_STYLE: Record<string, { bg: string; border: string; color: string }> = {
  TANK:   { bg: "rgba(74,144,226,0.15)",  border: "rgba(74,144,226,0.4)",  color: "#6ab0f5" },
  HEALER: { bg: "rgba(46,203,122,0.15)",  border: "rgba(46,203,122,0.4)",  color: "#4de89a" },
  MELEE:  { bg: "rgba(232,80,64,0.15)",   border: "rgba(232,80,64,0.4)",   color: "#f07060" },
  RANGED: { bg: "rgba(232,80,64,0.15)",   border: "rgba(232,80,64,0.4)",   color: "#f07060" },
};

export default function Header() {
  const router = useRouter();
  const pathname = usePathname();
  const { role, spot, fight, reset } = useAppStore();
  const rs = role ? ROLE_STYLE[role] : null;

  const handleLogoClick = () => {
    reset();
    router.push("/");
  };

  // Determine if we're deep enough to show breadcrumb
  const showRole = pathname !== "/";
  const showFight = !!fight && pathname.startsWith("/fights/");

  return (
    <header className="sticky top-0 z-50 border-b border-aether/10 bg-void/85 backdrop-blur-2xl">
      <div className="max-w-5xl mx-auto flex items-center justify-between px-5 py-3 gap-4">

        {/* ── Logo ── */}
        <button onClick={handleLogoClick} className="group flex items-center gap-3 shrink-0">
          <div
            className="relative flex items-center justify-center w-9 h-9 rounded-sm overflow-hidden"
            style={{ border: "1px solid rgba(91,196,232,0.2)", background: "rgba(91,196,232,0.05)" }}
          >
            <span
              className="relative text-xl leading-none transition-transform duration-200 group-hover:scale-110"
              style={{ filter: "drop-shadow(0 0 6px rgba(91,196,232,0.7))", color: "#9de0f8" }}
            >
              ⚔
            </span>
          </div>
          <div className="flex flex-col text-left gap-0.5">
            <span className="font-display text-sm font-bold text-gold-light group-hover:text-gold-bright transition-colors leading-none tracking-widest">
              RaidCoach
            </span>
            <span className="font-cinzel text-[0.5rem] text-muted tracking-[0.22em] uppercase leading-none">
              XIV · Mechanic Trainer
            </span>
          </div>
        </button>

        {/* ── Breadcrumb ── */}
        {showRole && rs && (
          <nav className="flex items-center gap-2 text-xs min-w-0">
            <span
              className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-sm font-cinzel text-xs tracking-wider shrink-0"
              style={{ background: rs.bg, border: `1px solid ${rs.border}`, color: rs.color }}
            >
              {role}
              <span style={{ color: rs.border, fontSize: "0.7em" }}>·</span>
              <span>Spot {spot}</span>
            </span>

            {showFight && (
              <>
                <svg width="6" height="10" viewBox="0 0 6 10" fill="none" className="text-dim shrink-0">
                  <path d="M1 1l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <button
                  onClick={() => router.push(`/fights/${fight!.slug}`)}
                  className="font-cinzel text-muted hover:text-gold-light transition-colors tracking-wide truncate"
                >
                  {fight!.short_name}
                </button>
              </>
            )}
          </nav>
        )}

        {/* ── Import link ── */}
        <button
          onClick={() => router.push("/import")}
          className="hidden sm:flex items-center gap-1 font-cinzel text-[0.6rem] tracking-[0.15em] uppercase shrink-0 px-3 py-1.5 rounded-sm transition-all duration-200"
          style={{ border: "1px solid rgba(91,196,232,0.12)", color: "#3d5470" }}
          onMouseEnter={(e) => {
            (e.currentTarget as HTMLElement).style.borderColor = "rgba(91,196,232,0.3)";
            (e.currentTarget as HTMLElement).style.color = "#9de0f8";
          }}
          onMouseLeave={(e) => {
            (e.currentTarget as HTMLElement).style.borderColor = "rgba(91,196,232,0.12)";
            (e.currentTarget as HTMLElement).style.color = "#3d5470";
          }}
        >
          <span className="text-base leading-none">+</span> Import
        </button>

      </div>
    </header>
  );
}
