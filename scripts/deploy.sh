#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

docker compose -f docker-compose.yml -f docker-compose.prod.yml down --remove-orphans

docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

docker compose -f docker-compose.yml -f docker-compose.prod.yml ps

echo "Deployment complete. Health check: http://localhost/health"
