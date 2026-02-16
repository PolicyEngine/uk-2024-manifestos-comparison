export interface ManifestoImpact {
  manifesto: string;
  cost: number;
  benefits: number;
  taxes: number;
  povertyImpact: number;
  childPovertyImpact: number;
  adultPovertyImpact: number;
  seniorPovertyImpact: number;
  giniIndexImpact: number;
  year: number;
  includesIndirectImpacts: boolean;
}

export interface DecileImpact {
  reform: string;
  decile: number;
  relativeIncomeChange: number;
  year: number;
  includesIndirectImpacts: boolean;
}

export type MetricKey =
  | "cost"
  | "benefits"
  | "taxes"
  | "povertyImpact"
  | "childPovertyImpact"
  | "adultPovertyImpact"
  | "seniorPovertyImpact"
  | "giniIndexImpact";

export interface MetricOption {
  key: MetricKey;
  label: string;
  unit: "bn" | "pct";
}

export const METRICS: MetricOption[] = [
  { key: "cost", label: "Cost", unit: "bn" },
  { key: "benefits", label: "Benefits", unit: "bn" },
  { key: "taxes", label: "Taxes", unit: "bn" },
  { key: "povertyImpact", label: "Poverty", unit: "pct" },
  { key: "childPovertyImpact", label: "Child poverty", unit: "pct" },
  { key: "adultPovertyImpact", label: "Adult poverty", unit: "pct" },
  { key: "seniorPovertyImpact", label: "Senior poverty", unit: "pct" },
  { key: "giniIndexImpact", label: "Gini index", unit: "pct" },
];

export const PARTIES = [
  "Conservatives",
  "Labour Party",
  "Liberal Democrats",
] as const;

export const YEARS = [2025, 2026, 2027, 2028] as const;

export interface HouseholdPerson {
  age: number;
  incomeSource: "None" | "Employment" | "Self-employment" | "Pension";
  income: number;
  capitalGains: number;
  hasCapitalGains: boolean;
  attendsPrivateSchool?: boolean;
}

export interface HouseholdSituation {
  you: HouseholdPerson;
  hasPartner: boolean;
  partner?: HouseholdPerson;
  hasChildren: boolean;
  children: { age: number; attendsPrivateSchool: boolean }[];
  buyingFirstHome: boolean;
  propertyValue: number;
  isRenter: boolean;
  isPrivateRenter: boolean;
  rent: number;
}

export interface HouseholdResult {
  metric: string;
  value: number;
  party: string;
}
