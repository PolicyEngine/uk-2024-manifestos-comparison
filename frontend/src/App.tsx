import { useState } from "react";
import {
  MantineProvider,
  Container,
  Title,
  Text,
  Select,
  Checkbox,
  Tabs,
  Stack,
} from "@mantine/core";
import "@mantine/core/styles.css";
import SocietalImpacts from "./components/SocietalImpacts";
import HouseholdImpacts from "./components/HouseholdImpacts";
import { colors, fonts } from "./designTokens";
import { YEARS } from "./types";

export default function App() {
  const [year, setYear] = useState<number>(2028);
  const [includeIndirect, setIncludeIndirect] = useState(true);

  return (
    <MantineProvider
      theme={{
        fontFamily: fonts.body,
        primaryColor: "teal",
      }}
    >
      <Container size="md" py="xl">
        <Stack gap="lg">
          <Title order={1} style={{ color: colors.primary }}>
            UK 2024 election manifestos
          </Title>
          <Text size="md" c="dimmed">
            This interactive app compares the societal and household-level
            impacts of the Conservative, Labour and Liberal Democrat manifestos.
          </Text>

          <Select
            label="Select a year"
            data={YEARS.map((y) => ({ value: String(y), label: String(y) }))}
            value={String(year)}
            onChange={(v) => setYear(Number(v) || 2028)}
            w={200}
          />

          <Checkbox
            label="Include indirect impacts"
            checked={includeIndirect}
            onChange={(e) => setIncludeIndirect(e.currentTarget.checked)}
            description="Include estimates of indirect impacts through public spending or non-household taxes."
          />

          <Tabs defaultValue="societal">
            <Tabs.List>
              <Tabs.Tab value="societal">Societal impacts</Tabs.Tab>
              <Tabs.Tab value="household">Household impacts</Tabs.Tab>
            </Tabs.List>

            <Tabs.Panel value="societal" pt="md">
              <SocietalImpacts year={year} includeIndirect={includeIndirect} />
            </Tabs.Panel>

            <Tabs.Panel value="household" pt="md">
              <HouseholdImpacts year={year} includeIndirect={includeIndirect} />
            </Tabs.Panel>
          </Tabs>
        </Stack>
      </Container>
    </MantineProvider>
  );
}
