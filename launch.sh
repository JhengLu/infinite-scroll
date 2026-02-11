#!/usr/bin/env bash
set -euo pipefail

IMAGE="infinite-scroll"
CONTAINER="infinite-scroll"
PORT="${PORT:-8020}"
DIR="$(cd "$(dirname "$0")" && pwd)"

# ── helpers ──────────────────────────────────────────────────────────────────
log()  { echo "[launch] $*"; }
err()  { echo "[launch] ERROR: $*" >&2; exit 1; }

# ── pre-flight ───────────────────────────────────────────────────────────────
command -v docker >/dev/null 2>&1 || err "Docker is not installed or not in PATH."

# ── stop & remove existing container ─────────────────────────────────────────
if docker inspect "$CONTAINER" >/dev/null 2>&1; then
  log "Stopping existing container '$CONTAINER'..."
  docker stop "$CONTAINER" >/dev/null 2>&1 || true
  docker rm   "$CONTAINER" >/dev/null 2>&1 || true
fi

# ── build ─────────────────────────────────────────────────────────────────────
log "Building image '$IMAGE'..."
docker build -t "$IMAGE" "$DIR"

# ── run ───────────────────────────────────────────────────────────────────────
log "Starting container on port $PORT..."
docker run -d \
  --name "$CONTAINER" \
  --restart unless-stopped \
  -p "${PORT}:80" \
  "$IMAGE"

log "Ready at http://localhost:${PORT}"
