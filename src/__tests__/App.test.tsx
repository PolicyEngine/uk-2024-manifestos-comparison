import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "../App";

const mockManifestoData = [
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
    year: 2028,
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
    year: 2028,
    includesIndirectImpacts: true,
  },
  {
    manifesto: "Liberal Democrats",
    cost: -1873906248.9,
    benefits: 26727960794.3,
    taxes: 24854057617.9,
    povertyImpact: -17.52,
    childPovertyImpact: -23.06,
    adultPovertyImpact: -12.61,
    seniorPovertyImpact: -19.54,
    giniIndexImpact: -3.68,
    year: 2028,
    includesIndirectImpacts: true,
  },
];

const mockDecileData = Array.from({ length: 30 }, (_, i) => ({
  reform: ["Conservatives", "Labour Party", "Liberal Democrats"][
    Math.floor(i / 10)
  ],
  decile: (i % 10) + 1,
  relativeIncomeChange: Math.random() * 4 - 2,
  year: 2028,
  includesIndirectImpacts: true,
}));

beforeEach(() => {
  vi.spyOn(globalThis, "fetch").mockImplementation((url) => {
    const urlStr = typeof url === "string" ? url : url.toString();
    if (urlStr.includes("manifesto_impact")) {
      return Promise.resolve(
        new Response(JSON.stringify(mockManifestoData), {
          headers: { "Content-Type": "application/json" },
        }),
      );
    }
    if (urlStr.includes("decile_impact")) {
      return Promise.resolve(
        new Response(JSON.stringify(mockDecileData), {
          headers: { "Content-Type": "application/json" },
        }),
      );
    }
    return Promise.resolve(new Response("Not found", { status: 404 }));
  });
});

describe("App", () => {
  it("renders the title", async () => {
    render(<App />);
    expect(
      screen.getByText("UK 2024 election manifestos"),
    ).toBeInTheDocument();
  });

  it("renders year selector with default 2028", async () => {
    render(<App />);
    // Mantine Select renders the value in an input
    const yearInput = screen.getByRole("textbox", { name: /select a year/i });
    expect(yearInput).toHaveValue("2028");
  });

  it("renders include indirect impacts checkbox", async () => {
    render(<App />);
    expect(
      screen.getByLabelText("Include indirect impacts"),
    ).toBeInTheDocument();
  });

  it("renders both tab labels", async () => {
    render(<App />);
    expect(screen.getByText("Societal impacts")).toBeInTheDocument();
    expect(screen.getByText("Household impacts")).toBeInTheDocument();
  });

  it("shows societal impact content after data loads", async () => {
    render(<App />);
    await waitFor(() => {
      expect(
        screen.getByText(/impact by income decile/i),
      ).toBeInTheDocument();
    });
  });

  it("switches to household impacts tab", async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.click(screen.getByText("Household impacts"));
    await waitFor(() => {
      expect(screen.getByText("Household impact")).toBeInTheDocument();
    });
  });
});
