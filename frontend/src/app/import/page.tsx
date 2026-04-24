import ImportWizard from "@/components/ImportWizard";
import Link from "next/link";

export const metadata = {
  title: "Import Fight — RaidCoach XIV",
  description: "Import fight mechanics from wtfdig.info",
};

export default function ImportPage() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Minimal header */}
      <header className="sticky top-0 z-50 flex items-center justify-between px-6 py-3 bg-[#0d0d1a]/85 backdrop-blur-xl border-b border-[rgba(200,164,90,0.15)]">
        <Link href="/" className="flex items-center gap-3 group">
          <span className="text-2xl text-gold drop-shadow-[0_0_16px_rgba(200,164,90,0.6)]">
            &#x2694;
          </span>
          <span className="flex flex-col text-left">
            <span className="font-cinzel text-base font-black text-gold-light tracking-wider leading-none">
              RaidCoach
            </span>
            <span className="text-[0.6rem] text-text-muted tracking-[0.15em] uppercase">
              XIV Mechanic Trainer
            </span>
          </span>
        </Link>
        <span className="font-cinzel text-xs text-text-muted tracking-wider uppercase">
          Import Wizard
        </span>
      </header>

      <main className="flex-1 relative z-10">
        <ImportWizard />
      </main>

      <footer className="py-4 text-center text-[0.65rem] text-white/15 tracking-wide border-t border-white/5 relative z-10">
        <span>Not affiliated with Square Enix or wtfdig.info.</span>
      </footer>
    </div>
  );
}
