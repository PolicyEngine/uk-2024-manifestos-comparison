import { useState, useEffect } from "react";
import type { ManifestoImpact, DecileImpact } from "../types";

export function useManifestoData() {
  const [data, setData] = useState<ManifestoImpact[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/data/manifesto_impact.json")
      .then((r) => r.json())
      .then((d: ManifestoImpact[]) => {
        setData(d);
        setLoading(false);
      });
  }, []);

  return { data, loading };
}

export function useDecileData() {
  const [data, setData] = useState<DecileImpact[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/data/decile_impact.json")
      .then((r) => r.json())
      .then((d: DecileImpact[]) => {
        setData(d);
        setLoading(false);
      });
  }, []);

  return { data, loading };
}

export function filterManifestoData(
  data: ManifestoImpact[],
  year: number,
  includeIndirect: boolean,
): ManifestoImpact[] {
  return data.filter(
    (d) => d.year === year && d.includesIndirectImpacts === includeIndirect,
  );
}

export function filterDecileData(
  data: DecileImpact[],
  year: number,
  includeIndirect: boolean,
): DecileImpact[] {
  return data.filter(
    (d) => d.year === year && d.includesIndirectImpacts === includeIndirect,
  );
}

export function formatBn(value: number): string {
  const bn = value / 1e9;
  const sign = bn >= 0 ? "+" : "";
  return `${sign}${bn.toFixed(1)}bn`;
}

export function formatPct(value: number): string {
  const sign = value >= 0 ? "+" : "";
  return `${sign}${value.toFixed(1)}%`;
}
