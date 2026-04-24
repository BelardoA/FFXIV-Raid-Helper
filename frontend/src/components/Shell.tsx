"use client";

import Header from "./Header";

export function Shell({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Header />
      <main className="flex-1 relative z-10">{children}</main>
      <footer
        className="relative z-10 py-4 text-center border-t"
        style={{ borderColor: "rgba(91,196,232,0.06)" }}
      >
        <span className="font-cinzel text-[0.55rem] text-dim tracking-[0.2em] uppercase">
          Mechanic data sourced from community guides
          <span className="mx-2 opacity-40">·</span>
          Not affiliated with Square Enix
        </span>
      </footer>
    </>
  );
}
