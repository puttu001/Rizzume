# frontend

Next.js (App Router, TypeScript, Tailwind). Talks to the backend exclusively
through `api-gateway` — see `src/lib/api-client.ts` and `src/config/env.ts`.

## Layout

```
src/
├── app/         # routes (Next.js App Router)
├── components/  # shared/dumb UI components
├── features/    # interview/, auth/, report/ — feature-owned UI + logic
├── lib/         # api client, utils
├── hooks/
├── stores/      # client state
└── config/      # env validation
```

## Run locally

```
npm install
cp .env.example .env.local
npm run dev
```

Deploys independently of the backend — see root README for the
frontend/backend hosting split.
