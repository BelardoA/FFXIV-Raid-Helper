"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAppStore } from "@/lib/store";
import { Shell } from "@/components/Shell";
import FightBrowser from "@/components/FightBrowser";

export default function FightsPage() {
  const router = useRouter();
  const role = useAppStore((s) => s.role);

  useEffect(() => {
    if (!role) router.replace("/");
  }, [role, router]);

  if (!role) return null;
  return (
    <Shell>
      <FightBrowser />
    </Shell>
  );
}
