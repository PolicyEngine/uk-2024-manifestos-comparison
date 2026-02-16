import { useState } from "react";
import { Select, Text, Stack, Loader, Center } from "@mantine/core";
import DecileChart from "./DecileChart";
import MetricBarChart from "./MetricBarChart";
import ImpactTable from "./ImpactTable";
import {
  useManifestoData,
  useDecileData,
  filterManifestoData,
  filterDecileData,
} from "../data/useData";
import { METRICS } from "../types";
import type { MetricOption } from "../types";

interface Props {
  year: number;
  includeIndirect: boolean;
}

export default function SocietalImpacts({ year, includeIndirect }: Props) {
  const { data: manifesto, loading: mLoading } = useManifestoData();
  const { data: decile, loading: dLoading } = useDecileData();
  const [selectedMetric, setSelectedMetric] = useState<MetricOption>(
    METRICS[0],
  );

  if (mLoading || dLoading) {
    return (
      <Center h={200}>
        <Loader />
      </Center>
    );
  }

  const filteredManifesto = filterManifestoData(manifesto, year, includeIndirect);
  const filteredDecile = filterDecileData(decile, year, includeIndirect);

  return (
    <Stack gap="lg">
      <Text size="lg" fw={600}>
        Societal impacts
      </Text>
      <Text size="sm" c="dimmed">
        The chart below shows the impact by income decile of each manifesto
        policy, as a percentage of prior household disposable income.
      </Text>

      <DecileChart data={filteredDecile} />

      <Text size="sm" c="dimmed">
        The table below shows the total impact of each manifesto policy on
        different societal metrics.
      </Text>

      <ImpactTable data={filteredManifesto} />

      <Select
        label="Select a metric to display"
        data={METRICS.map((m) => ({ value: m.key, label: m.label }))}
        value={selectedMetric.key}
        onChange={(v) => {
          const found = METRICS.find((m) => m.key === v);
          if (found) setSelectedMetric(found);
        }}
      />

      <MetricBarChart data={filteredManifesto} metric={selectedMetric} />
    </Stack>
  );
}
