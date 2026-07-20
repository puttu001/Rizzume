#!/usr/bin/env bash
# Regenerates every services/*/.env and frontend/.env from their .env.example
# templates, substituting shared secrets from .env.secrets (repo root).
#
# Usage: ./scripts/bootstrap-env.sh
# Rerun any time .env.secrets changes (e.g. after rotating a key).
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f .env.secrets ]; then
  echo "Missing .env.secrets — copy .env.secrets.example to .env.secrets and fill it in first." >&2
  exit 1
fi

if ! command -v envsubst >/dev/null 2>&1; then
  echo "envsubst not found (part of gettext). Install it and re-run." >&2
  exit 1
fi

set -a
# shellcheck disable=SC1091
source .env.secrets
set +a

for example in services/*/.env.example frontend/.env.example; do
  dir=$(dirname "$example")
  target="$dir/.env"
  envsubst < "$example" > "$target"
  echo "generated $target"
done
