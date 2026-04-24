"use client";

import { useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import { useAppStore } from "@/lib/store";
import { Shell } from "@/components/Shell";
import MechanicSelector from "@/components/MechanicSelector";

export default function MechanicPage() {
  const router = useRouter();
  const { slug } = useParams<{ slug: string }>();
  const role = useAppStore((s) => s.role);
  const fight = useAppStore((s) => s.fight);

  useEffect(() => {
    if (!role) router.replace("/");
    else if (!fight || fight.slug !== slug) router.replace("/fights");
  }, [role, fight, slug, router]);

  if (!role || !fight || fight.slug !== slug) return null;
  return (
    <Shell>
      <MechanicSelector />
    </Shell>
  );
}
