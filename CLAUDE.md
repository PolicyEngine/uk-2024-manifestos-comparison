# UK 2024 manifestos comparison

Compares societal and household-level impacts of Conservative, Labour, and Liberal Democrat manifestos for the 2024 UK general election.

## Architecture

- **Frontend**: React + TypeScript + Mantine v8 + Recharts in `frontend/`
- **API**: Modal backend in `api/modal_app.py` for household impact calculations
- **Data**: Pre-computed JSON in `frontend/public/data/` (converted from CSV)

## Development

```bash
cd frontend
npm install
npm run dev      # Dev server
npm test         # Vitest
npm run build    # Production build
```

## Deployment

- Frontend: Vercel (config at repo root `vercel.json`)
- API: `unset MODAL_TOKEN_ID MODAL_TOKEN_SECRET && modal deploy api/modal_app.py`
- Set `VITE_API_URL` env var in Vercel to the Modal endpoint URL

## Key files

- `frontend/src/App.tsx` - Main app with year selector, indirect impacts toggle, tabs
- `frontend/src/components/SocietalImpacts.tsx` - Decile chart, impact table, metric bar chart
- `frontend/src/components/HouseholdImpacts.tsx` - User input form, API-driven calculations
- `frontend/src/designTokens.ts` - Colors, fonts, spacing
- `api/modal_app.py` - policyengine_uk Simulation endpoint
