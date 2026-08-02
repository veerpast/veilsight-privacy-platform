#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -x ".venv/bin/uvicorn" ]]; then
  echo "Missing .venv. Run: make setup-full"
  exit 1
fi

cleanup() {
  kill "$API_PID" "$WEB_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "VeilSight API: http://127.0.0.1:8000"
echo "VeilSight UI : http://127.0.0.1:5173"
echo "Press Ctrl-C to stop both services."

PYTHONPATH=backend .venv/bin/uvicorn app.main:app --port 8000 &
API_PID=$!
(cd frontend && npm run dev -- --host 127.0.0.1) &
WEB_PID=$!
wait
