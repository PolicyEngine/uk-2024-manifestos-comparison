import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import { partyColors } from "../designTokens";
import type { DecileImpact } from "../types";
import { PARTIES } from "../types";

interface Props {
  data: DecileImpact[];
}

export default function DecileChart({ data }: Props) {
  // Pivot data: one row per decile, columns per party
  const pivoted = Array.from({ length: 10 }, (_, i) => {
    const decile = i + 1;
    const row: Record<string, number> = { decile };
    for (const party of PARTIES) {
      const match = data.find(
        (d) => d.decile === decile && d.reform === party,
      );
      row[party] = match ? match.relativeIncomeChange : 0;
    }
    return row;
  });

  const allValues = data.map((d) => d.relativeIncomeChange);
  const absMax = Math.max(
    Math.abs(Math.min(...allValues, 0)),
    Math.abs(Math.max(...allValues, 0)),
  );
  const yBound = Math.ceil(absMax * 1.1);

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={pivoted} margin={{ top: 5, right: 30, bottom: 5, left: 20 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="decile"
          ticks={[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
          label={{ value: "Income decile", position: "insideBottom", offset: -5 }}
        />
        <YAxis
          domain={[-yBound, yBound]}
          tickFormatter={(v: number) => `${v > 0 ? "+" : ""}${v.toFixed(0)}%`}
          label={{
            value: "Relative income change (%)",
            angle: -90,
            position: "insideLeft",
            offset: 10,
          }}
        />
        <Tooltip
          formatter={(value) => {
            const v = Number(value);
            return `${v > 0 ? "+" : ""}${v.toFixed(2)}%`;
          }}
        />
        <Legend />
        <ReferenceLine y={0} stroke="#999" strokeDasharray="3 3" />
        {PARTIES.map((party) => (
          <Line
            key={party}
            type="monotone"
            dataKey={party}
            stroke={partyColors[party]}
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}
