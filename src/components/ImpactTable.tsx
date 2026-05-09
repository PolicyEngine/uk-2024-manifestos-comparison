import { Table } from "@mantine/core";
import type { ManifestoImpact } from "../types";
import { PARTIES } from "../types";

interface Props {
  data: ManifestoImpact[];
}

function fmtBn(v: number): string {
  return (v / 1e9).toFixed(1);
}

function fmtPct(v: number): string {
  return v.toFixed(1);
}

const ROW_DEFS = [
  { label: "Cost (bn)", key: "cost" as const, fmt: fmtBn },
  { label: "Benefits (bn)", key: "benefits" as const, fmt: fmtBn },
  { label: "Taxes (bn)", key: "taxes" as const, fmt: fmtBn },
  { label: "Poverty impact (%)", key: "povertyImpact" as const, fmt: fmtPct },
  {
    label: "Child poverty impact (%)",
    key: "childPovertyImpact" as const,
    fmt: fmtPct,
  },
  {
    label: "Adult poverty impact (%)",
    key: "adultPovertyImpact" as const,
    fmt: fmtPct,
  },
  {
    label: "Senior poverty impact (%)",
    key: "seniorPovertyImpact" as const,
    fmt: fmtPct,
  },
  {
    label: "Gini index impact (%)",
    key: "giniIndexImpact" as const,
    fmt: fmtPct,
  },
];

export default function ImpactTable({ data }: Props) {
  const getPartyValue = (party: string, key: keyof ManifestoImpact) => {
    const row = data.find((d) => d.manifesto === party);
    return row ? (row[key] as number) : 0;
  };

  return (
    <Table striped highlightOnHover withTableBorder>
      <Table.Thead>
        <Table.Tr>
          <Table.Th>Metric</Table.Th>
          {PARTIES.map((p) => (
            <Table.Th key={p}>{p}</Table.Th>
          ))}
        </Table.Tr>
      </Table.Thead>
      <Table.Tbody>
        {ROW_DEFS.map((row) => (
          <Table.Tr key={row.key}>
            <Table.Td>{row.label}</Table.Td>
            {PARTIES.map((p) => (
              <Table.Td key={p}>{row.fmt(getPartyValue(p, row.key))}</Table.Td>
            ))}
          </Table.Tr>
        ))}
      </Table.Tbody>
    </Table>
  );
}
