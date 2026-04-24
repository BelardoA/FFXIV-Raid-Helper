"use client";

import { useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import { useAppStore } from "@/lib/store";
import { Shell } from "@/components/Shell";
import DrillView from "@/components/DrillView";

export default function DrillPage() {
  const router = useRouter();
  const { slug } = useParams<{ slug: string }>();
  const role = useAppStore((s) => s.role);
  const drillPlan = useAppStore((s) => s.drillPlan);

  useEffect(() => {
    if (!role) router.replace("/");
    else if (!drillPlan) router.replace(`/fights/${slug}`);
  }, [role, drillPlan, slug, router]);

  if (!role || !drillPlan) return null;
  return (
    <Shell>
      <DrillView />
    </Shell>
  );
}
