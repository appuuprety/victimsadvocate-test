#!/usr/bin/env bash
# Local git pre-push hook — run smoke tests before allowing a push.
#
# Install (from the test repo root):
#   cp scripts/pre-push.sh .git/hooks/pre-push
#   chmod +x .git/hooks/pre-push
#
# To bypass in an emergency: git push --no-verify

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

# Activate venv if present
if [ -f .venv/Scripts/activate ]; then
  # Windows (Git Bash)
  source .venv/Scripts/activate
elif [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
else
  echo "pre-push: no .venv found — skipping tests"
  exit 0
fi

# Make sure the dev server is reachable
if ! curl -fs http://localhost:5173 >/dev/null 2>&1; then
  echo "pre-push: app not running at http://localhost:5173 — skipping UI tests."
  echo "          Start it with 'npm run dev' in VictimsAdvocate to enable full coverage."
  pytest -m "api and smoke" || exit 1
else
  pytest -m smoke || exit 1
fi

echo "pre-push: smoke tests passed ✓"
