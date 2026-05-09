import { describe, it, expect } from "vitest";
import {
  filterManifestoData,
  filterDecileData,
  formatBn,
  formatPct,
} from "../data/useData";
import type { ManifestoImpact, DecileImpact } from "../types";

const sampleManifesto: ManifestoImpact[] = [
  {
    manifesto: "Conservatives",
    cost: -1909743165.6,
    benefits: -3235029268.0,
    taxes: -5144776752.0,
    povertyImpact: 2.03,
    childPovertyImpact: 1.55,
    adultPovertyImpact: 2.29,
    seniorPovertyImpact: 1.86,
    giniIndexImpact: 0.38,
    year: 2025,
    includesIndirectImpacts: true,
  },
  {
    manifesto: "Labour Party",
    cost: 3294842909.8,
    benefits: 4195599885.7,
    taxes: 7490427971.1,
    povertyImpact: -1.91,
    childPovertyImpact: -0.38,
    adultPovertyImpact: -1.16,
    seniorPovertyImpact: -8.58,
    giniIndexImpact: -0.69,
    year: 2025,
    includesIndirectImpacts: true,
  },
  {
    manifesto: "Conservatives",
    cost: -7053853830.1,
    benefits: -70920320.5,
    taxes: -7124775732.5,
    povertyImpact: -0.99,
    childPovertyImpact: -0.12,
    adultPovertyImpact: -0.85,
    seniorPovertyImpact: -3.66,
    giniIndexImpact: 0.07,
    year: 2025,
    includesIndirectImpacts: false,
  },
  {
    manifesto: "Labour Party",
    cost: 3146563347.7,
    benefits: 4195599447.4,
    taxes: 7342177974.3,
    povertyImpact: -0.85,
    childPovertyImpact: -0.06,
    adultPovertyImpact: -0.81,
    seniorPovertyImpact: -2.88,
    giniIndexImpact: -0.64,
    year: 2026,
    includesIndirectImpacts: true,
  },
];

const sampleDecile: DecileImpact[] = [
  {
    reform: "Conservatives",
    decile: 1,
    relativeIncomeChange: -2.12,
    year: 2025,
    includesIndirectImpacts: true,
  },
  {
    reform: "Labour Party",
    decile: 1,
    relativeIncomeChange: 2.2,
    year: 2025,
    includesIndirectImpacts: true,
  },
  {
    reform: "Conservatives",
    decile: 1,
    relativeIncomeChange: 0.56,
    year: 2025,
    includesIndirectImpacts: false,
  },
  {
    reform: "Labour Party",
    decile: 1,
    relativeIncomeChange: 0.0,
    year: 2026,
    includesIndirectImpacts: true,
  },
];

describe("filterManifestoData", () => {
  it("filters by year and indirect impacts", () => {
    const result = filterManifestoData(sampleManifesto, 2025, true);
    expect(result).toHaveLength(2);
    expect(result[0].manifesto).toBe("Conservatives");
    expect(result[1].manifesto).toBe("Labour Party");
  });

  it("filters direct impacts only", () => {
    const result = filterManifestoData(sampleManifesto, 2025, false);
    expect(result).toHaveLength(1);
    expect(result[0].manifesto).toBe("Conservatives");
  });

  it("returns empty for non-matching year", () => {
    const result = filterManifestoData(sampleManifesto, 2028, true);
    expect(result).toHaveLength(0);
  });
});

describe("filterDecileData", () => {
  it("filters by year and indirect impacts", () => {
    const result = filterDecileData(sampleDecile, 2025, true);
    expect(result).toHaveLength(2);
  });

  it("filters direct impacts", () => {
    const result = filterDecileData(sampleDecile, 2025, false);
    expect(result).toHaveLength(1);
    expect(result[0].reform).toBe("Conservatives");
  });
});

describe("formatBn", () => {
  it("formats positive values", () => {
    expect(formatBn(3.3e9)).toBe("+3.3bn");
  });

  it("formats negative values", () => {
    expect(formatBn(-1.9e9)).toBe("-1.9bn");
  });

  it("formats zero", () => {
    expect(formatBn(0)).toBe("+0.0bn");
  });
});

describe("formatPct", () => {
  it("formats positive percentages", () => {
    expect(formatPct(2.03)).toBe("+2.0%");
  });

  it("formats negative percentages", () => {
    expect(formatPct(-1.91)).toBe("-1.9%");
  });
});
