#!/usr/bin/env bash
set -euo pipefail

CONTAINER="infinite-scroll"

if docker inspect "$CONTAINER" >/dev/null 2>&1; then
  echo "[stop] Stopping container '$CONTAINER'..."
  docker stop "$CONTAINER" >/dev/null
  docker rm   "$CONTAINER" >/dev/null
  echo "[stop] Done."
else
  echo "[stop] Container '$CONTAINER' is not running."
fi
