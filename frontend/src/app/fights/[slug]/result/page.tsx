"use client";

import { useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import { useAppStore } from "@/lib/store";
import { Shell } from "@/components/Shell";
import DrillResults from "@/components/DrillResults";

export default function ResultPage() {
  const router = useRouter();
  const { slug } = useParams<{ slug: string }>();
  const role = useAppStore((s) => s.role);
  const stepResults = useAppStore((s) => s.stepResults);

  useEffect(() => {
    if (!role) router.replace("/");
    else if (!stepResults.length) router.replace(`/fights/${slug}`);
  }, [role, stepResults, slug, router]);

  if (!role || !stepResults.length) return null;
  return (
    <Shell>
      <DrillResults />
    </Shell>
  );
}
