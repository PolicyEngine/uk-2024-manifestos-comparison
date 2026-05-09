# UK 2024 manifestos comparison

Compares societal and household-level impacts of Conservative, Labour, and Liberal Democrat manifestos for the 2024 UK general election.

## Architecture

- **Frontend**: Next.js App Router + React + TypeScript + Mantine v8 + Recharts at the repo root
- **API**: Modal backend in `api/modal_app.py` for household impact calculations
- **Data**: Pre-computed JSON in `public/data/` (converted from CSV)

## Development

```bash
bun install
bun run dev      # Dev server
bun test         # Vitest
bun run build    # Production build
```

## Deployment

- Frontend: Vercel (config at repo root `vercel.json`)
- API: `unset MODAL_TOKEN_ID MODAL_TOKEN_SECRET && modal deploy api/modal_app.py`
- Set `NEXT_PUBLIC_API_URL` env var in Vercel to the Modal endpoint URL

## Key files

- `src/App.tsx` - Main app with year selector, indirect impacts toggle, tabs
- `src/components/SocietalImpacts.tsx` - Decile chart, impact table, metric bar chart
- `src/components/HouseholdImpacts.tsx` - User input form, API-driven calculations
- `src/designTokens.ts` - Colors, fonts, spacing
- `api/modal_app.py` - policyengine_uk Simulation endpoint
