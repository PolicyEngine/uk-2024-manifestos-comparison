export const colors = {
  primary: "#319795",
  conservatives: "#0087DC",
  labour: "#E4003B",
  libDem: "#FAA61A",
  background: "#FFFFFF",
  surface: "#F8F9FA",
  text: "#212529",
  textSecondary: "#6C757D",
  border: "#DEE2E6",
} as const;

export const partyColors: Record<string, string> = {
  Conservatives: colors.conservatives,
  "Labour Party": colors.labour,
  "Liberal Democrats": colors.libDem,
};

export const fonts = {
  body: "Inter, system-ui, -apple-system, sans-serif",
} as const;

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
} as const;
