import { useState } from "react";
import {
  Stack,
  Text,
  NumberInput,
  Select,
  Checkbox,
  Button,
  Loader,
  Center,
  Alert,
} from "@mantine/core";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
  ReferenceLine,
} from "recharts";
import { partyColors } from "../designTokens";
import type { HouseholdResult } from "../types";

const API_URL = import.meta.env.VITE_API_URL || "";

const INCOME_SOURCES = [
  { value: "None", label: "None" },
  { value: "Employment", label: "Employment" },
  { value: "Self-employment", label: "Self-employment" },
  { value: "Pension", label: "Pension" },
];

interface Props {
  year: number;
  includeIndirect: boolean;
}

interface ChildInput {
  age: number;
  attendsPrivateSchool: boolean;
}

function fmt(value: number): string {
  return value >= 0 ? `+\u00A3${value.toLocaleString("en-GB", { maximumFractionDigits: 0 })}` : `-\u00A3${Math.abs(value).toLocaleString("en-GB", { maximumFractionDigits: 0 })}`;
}

export default function HouseholdImpacts({ year, includeIndirect }: Props) {
  const [age, setAge] = useState(30);
  const [incomeSource, setIncomeSource] = useState("Employment");
  const [income, setIncome] = useState(20000);
  const [hasCapitalGains, setHasCapitalGains] = useState(false);
  const [capitalGains, setCapitalGains] = useState(0);
  const [hasPartner, setHasPartner] = useState(false);
  const [partnerAge, setPartnerAge] = useState(30);
  const [partnerIncomeSource, setPartnerIncomeSource] = useState("None");
  const [partnerIncome, setPartnerIncome] = useState(20000);
  const [hasChildren, setHasChildren] = useState(false);
  const [children, setChildren] = useState<ChildInput[]>([
    { age: 10, attendsPrivateSchool: false },
  ]);
  const [buyingFirstHome, setBuyingFirstHome] = useState(false);
  const [propertyValue, setPropertyValue] = useState(200000);
  const [isRenter, setIsRenter] = useState(false);
  const [isPrivateRenter, setIsPrivateRenter] = useState(false);
  const [rent, setRent] = useState(20000);

  const [results, setResults] = useState<HouseholdResult[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedMetric, setSelectedMetric] = useState("Net change");

  const handleCalculate = async () => {
    if (!API_URL) {
      setError(
        "Household impact calculations require a backend API. Set VITE_API_URL to enable.",
      );
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/household`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          year,
          includeIndirect,
          age,
          incomeSource,
          income: incomeSource !== "None" ? income : 0,
          hasCapitalGains,
          capitalGains: hasCapitalGains ? capitalGains : 0,
          hasPartner,
          partnerAge: hasPartner ? partnerAge : null,
          partnerIncomeSource: hasPartner ? partnerIncomeSource : null,
          partnerIncome:
            hasPartner && partnerIncomeSource !== "None"
              ? partnerIncome
              : null,
          hasChildren,
          children: hasChildren ? children : [],
          buyingFirstHome,
          propertyValue: buyingFirstHome ? propertyValue : null,
          isRenter,
          isPrivateRenter: isRenter ? isPrivateRenter : null,
          rent: isRenter ? rent : null,
        }),
      });

      if (!response.ok) throw new Error("Calculation failed");
      const data: HouseholdResult[] = await response.json();
      setResults(data);
    } catch {
      setError("Failed to calculate household impacts. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const metrics = results
    ? [...new Set(results.map((r) => r.metric))]
    : [];

  const chartData = results
    ? ["Conservatives", "Labour", "Liberal Democrats"]
        .map((party) => {
          const row = results.find(
            (r) => r.party === party && r.metric === selectedMetric,
          );
          return { party, value: row ? row.value : 0 };
        })
    : [];

  const bestParty = chartData.length
    ? [...chartData].sort((a, b) => b.value - a.value)[0].party
    : "";

  return (
    <Stack gap="md">
      <Text size="lg" fw={600}>
        Household impact
      </Text>

      <NumberInput
        label="How old are you?"
        value={age}
        onChange={(v) => setAge(Number(v) || 30)}
        min={0}
        max={100}
      />

      <Select
        label="What's your main source of income?"
        data={INCOME_SOURCES}
        value={incomeSource}
        onChange={(v) => setIncomeSource(v || "Employment")}
      />

      {incomeSource !== "None" && (
        <NumberInput
          label="What's your annual income?"
          value={income}
          onChange={(v) => setIncome(Number(v) || 0)}
          min={0}
          prefix="£"
          thousandSeparator=","
        />
      )}

      <Checkbox
        label="I have capital gains"
        checked={hasCapitalGains}
        onChange={(e) => setHasCapitalGains(e.currentTarget.checked)}
      />
      {hasCapitalGains && (
        <NumberInput
          label="What's your annual capital gains income?"
          value={capitalGains}
          onChange={(v) => setCapitalGains(Number(v) || 0)}
          min={0}
          max={1000000}
          prefix="£"
          thousandSeparator=","
        />
      )}

      <Checkbox
        label="I am married or in a civil partnership"
        checked={hasPartner}
        onChange={(e) => setHasPartner(e.currentTarget.checked)}
      />
      {hasPartner && (
        <>
          <NumberInput
            label="How old is your spouse?"
            value={partnerAge}
            onChange={(v) => setPartnerAge(Number(v) || 30)}
            min={0}
            max={100}
          />
          <Select
            label="What's your spouse's main source of income?"
            data={INCOME_SOURCES}
            value={partnerIncomeSource}
            onChange={(v) => setPartnerIncomeSource(v || "None")}
          />
          {partnerIncomeSource !== "None" && (
            <NumberInput
              label="What's your spouse's annual income?"
              value={partnerIncome}
              onChange={(v) => setPartnerIncome(Number(v) || 0)}
              min={0}
              prefix="£"
              thousandSeparator=","
            />
          )}
        </>
      )}

      <Checkbox
        label="I have children"
        checked={hasChildren}
        onChange={(e) => setHasChildren(e.currentTarget.checked)}
      />
      {hasChildren && (
        <>
          <NumberInput
            label="How many children do you have?"
            value={children.length}
            onChange={(v) => {
              const count = Math.max(0, Math.min(10, Number(v) || 0));
              setChildren(
                Array.from({ length: count }, (_, i) =>
                  children[i] || { age: 10, attendsPrivateSchool: false },
                ),
              );
            }}
            min={0}
            max={10}
          />
          {children.map((child, i) => (
            <div key={i} style={{ paddingLeft: 16 }}>
              <NumberInput
                label={`How old is child ${i + 1}?`}
                value={child.age}
                onChange={(v) => {
                  const updated = [...children];
                  updated[i] = { ...updated[i], age: Number(v) || 10 };
                  setChildren(updated);
                }}
                min={0}
                max={18}
              />
              <Checkbox
                label={`Child ${i + 1} attends private school`}
                checked={child.attendsPrivateSchool}
                onChange={(e) => {
                  const updated = [...children];
                  updated[i] = {
                    ...updated[i],
                    attendsPrivateSchool: e.currentTarget.checked,
                  };
                  setChildren(updated);
                }}
                mt="xs"
              />
            </div>
          ))}
        </>
      )}

      <Checkbox
        label="I will buy my first home over the next four years"
        checked={buyingFirstHome}
        onChange={(e) => setBuyingFirstHome(e.currentTarget.checked)}
      />
      {buyingFirstHome && (
        <NumberInput
          label="What's the estimated value of the property you will buy?"
          value={propertyValue}
          onChange={(v) => setPropertyValue(Number(v) || 0)}
          min={0}
          prefix="£"
          thousandSeparator=","
        />
      )}

      <Checkbox
        label="I am a renter"
        checked={isRenter}
        onChange={(e) => setIsRenter(e.currentTarget.checked)}
      />
      {isRenter && (
        <>
          <Checkbox
            label="I rent from a private landlord"
            checked={isPrivateRenter}
            onChange={(e) => setIsPrivateRenter(e.currentTarget.checked)}
          />
          <NumberInput
            label="What's your annual rent?"
            value={rent}
            onChange={(v) => setRent(Number(v) || 0)}
            min={0}
            prefix="£"
            thousandSeparator=","
          />
        </>
      )}

      <Button onClick={handleCalculate} loading={loading}>
        Calculate impacts
      </Button>

      {error && (
        <Alert color="red" title="Error">
          {error}
        </Alert>
      )}

      {loading && (
        <Center h={100}>
          <Loader />
        </Center>
      )}

      {results && (
        <Stack gap="md">
          <Select
            label="Select a metric"
            data={metrics.map((m) => ({ value: m, label: m }))}
            value={selectedMetric}
            onChange={(v) => setSelectedMetric(v || "Net change")}
          />

          <Text size="md" fw={600} ta="center">
            The {bestParty} would increase your net income the most
          </Text>

          <ResponsiveContainer width="100%" height={350}>
            <BarChart
              data={chartData}
              margin={{ top: 5, right: 30, bottom: 5, left: 20 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="party" />
              <YAxis tickFormatter={(v: number) => fmt(v)} />
              <Tooltip formatter={(v) => fmt(Number(v))} />
              <Legend />
              <ReferenceLine y={0} stroke="#999" strokeDasharray="3 3" />
              <Bar dataKey="value" name="Net income change">
                {chartData.map((entry) => (
                  <Cell
                    key={entry.party}
                    fill={
                      partyColors[entry.party] ||
                      partyColors[
                        entry.party === "Labour" ? "Labour Party" : entry.party
                      ]
                    }
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Stack>
      )}
    </Stack>
  );
}
