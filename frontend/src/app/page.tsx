"use client";

import Header from "@/components/Header";
import RoleSelector from "@/components/RoleSelector";
import FightBrowser from "@/components/FightBrowser";
import MechanicSelector from "@/components/MechanicSelector";
import DrillView from "@/components/DrillView";
import DrillResults from "@/components/DrillResults";
import { useAppStore } from "@/lib/store";

export default function Home() {
  const phase = useAppStore((s) => s.phase);

  return (
    <>
      <Header />
      <main className="flex-1 relative z-10">
        {phase === "role-select" && <RoleSelector />}
        {phase === "fight-browse" && <FightBrowser />}
        {phase === "mechanic-select" && <MechanicSelector />}
        {phase === "drilling" && <DrillView />}
        {phase === "result" && <DrillResults />}
      </main>
      <footer className="py-4 text-center text-[0.65rem] text-white/15 tracking-wide border-t border-white/5 relative z-10">
        <span>Mechanic data sourced from community guides.</span>
        <span className="mx-2 opacity-40">&middot;</span>
        <span>Not affiliated with Square Enix.</span>
      </footer>
    </>
  );
}
