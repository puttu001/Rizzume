FROM node:22-slim AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM node:22-slim AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Overridable NEXT_PUBLIC_API_URL (baked into the browser bundle at build
# time, so it can't be changed at container-run time — a real ENV var here
# takes precedence over whatever's in the copied .env). Default matches the
# non-Docker local-dev convention; infra/docker-compose.yml passes a
# different value via build.args since it publishes the gateway on a
# different host port.
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
RUN npm run build

FROM node:22-slim AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/public ./public
COPY --from=build /app/.next/standalone ./
COPY --from=build /app/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"]
