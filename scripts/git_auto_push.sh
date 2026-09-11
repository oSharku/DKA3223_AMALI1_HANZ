#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/oSharku/DKA3223_AMALI1_HANZ.git"
BRANCH="main"
NOTEBOOK="DKA3223_AMALI1_HANZ.ipynb"

MSG="${1:-}"
if [ -z "$MSG" ]; then
  echo "Usage: $0 \"commit message\""
  echo "Example messages:"
  echo "  \"Complete ANN model and evaluation\""
  echo "  \"Complete CNN, digit prediction and comparison\""
  exit 2
fi

# must be inside a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: not inside a git repository. Clone the repo first:"
  echo "  git clone ${REPO_URL}"
  exit 1
fi

# file exists?
if [ ! -f "$NOTEBOOK" ]; then
  echo "Error: file '$NOTEBOOK' not found in current directory."
  exit 1
fi

# stage file
git add -- "$NOTEBOOK"

# if nothing staged, exit gracefully
if git diff --no-ext-diff --cached --quiet; then
  echo "No changes staged for commit."
  git --no-pager log --oneline -n 3
  exit 0
fi

# commit
git commit -m "$MSG"

# push: use GITHUB_TOKEN if present (safe handling)
if [ -n "${GITHUB_TOKEN-}" ]; then
  ORIG_URL="$(git remote get-url origin)"
  # restore origin on exit
  trap 'git remote set-url origin "$ORIG_URL" >/dev/null 2>&1 || true' EXIT
  AUTH_URL="https://x-access-token:${GITHUB_TOKEN}@github.com/oSharku/DKA3223_AMALI1_HANZ.git"
  git remote set-url origin "$AUTH_URL"
  git push origin "$BRANCH"
  # trap will restore origin
else
  git push origin "$BRANCH"
fi

# show last 3 commits as proof
git --no-pager log --oneline -n 3
