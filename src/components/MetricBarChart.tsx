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
import type { ManifestoImpact, MetricOption } from "../types";
import { PARTIES } from "../types";
import { formatBn, formatPct } from "../data/useData";

interface Props {
  data: ManifestoImpact[];
  metric: MetricOption;
}

function getMetricValue(row: ManifestoImpact, key: string): number {
  return row[key as keyof ManifestoImpact] as number;
}

export default function MetricBarChart({ data, metric }: Props) {
  const chartData = PARTIES.map((party) => {
    const row = data.find((d) => d.manifesto === party);
    if (!row) return { party, value: 0 };
    let value = getMetricValue(row, metric.key);

    if (metric.key === "cost") {
      // Invert cost so positive = reduces deficit
      value = -value;
    }

    if (metric.unit === "bn") {
      value = value / 1e9;
    }

    return { party, value: Math.round(value * 10) / 10 };
  });

  const formatter = (v: number) =>
    metric.unit === "bn" ? formatBn(v * 1e9) : formatPct(v);

  // Determine the party with the "best" impact
  const isBetterLower =
    metric.key.includes("poverty") ||
    metric.key.includes("gini") ||
    metric.key === "taxes" ||
    metric.key === "cost";
  const bestParty = [...chartData].sort((a, b) =>
    isBetterLower ? a.value - b.value : b.value - a.value,
  )[0]?.party;

  const getTitle = () => {
    const coloredParty = `${bestParty}`;
    if (metric.key === "cost")
      return `The ${coloredParty} would reduce the deficit the most`;
    if (metric.key === "taxes")
      return `The ${coloredParty} would reduce taxes the most`;
    if (metric.key === "benefits")
      return `The ${coloredParty} would increase benefits the most`;
    if (metric.key.includes("poverty") || metric.key.includes("gini")) {
      const bestValue = chartData.find((d) => d.party === bestParty)?.value ?? 0;
      return bestValue < 0
        ? `The ${coloredParty} would decrease ${metric.label.toLowerCase()} the most`
        : `The ${coloredParty} would increase ${metric.label.toLowerCase()} the least`;
    }
    return `${coloredParty} has the largest ${metric.label.toLowerCase()} impact`;
  };

  return (
    <div>
      <p
        style={{
          fontSize: 16,
          fontWeight: 600,
          textAlign: "center",
          marginBottom: 8,
        }}
      >
        {getTitle()}
      </p>
      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={chartData} margin={{ top: 5, right: 30, bottom: 5, left: 20 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="party" />
          <YAxis
            tickFormatter={(v: number) =>
              metric.unit === "bn" ? `${v > 0 ? "+" : ""}${v}` : `${v > 0 ? "+" : ""}${v}%`
            }
          />
          <Tooltip formatter={(v) => formatter(Number(v))} />
          <Legend />
          <ReferenceLine y={0} stroke="#999" strokeDasharray="3 3" />
          <Bar dataKey="value" name={metric.label}>
            {chartData.map((entry) => (
              <Cell key={entry.party} fill={partyColors[entry.party]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
