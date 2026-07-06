#!/usr/bin/env bash
set -euo pipefail

# Create and push the Continuity Ledger Initiative repo.
# Requirements: git and GitHub CLI (`gh`) authenticated as chaosweaver007.

REPO="chaosweaver007/continuity-ledger"

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI not found. Install gh first: https://cli.github.com/"
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init
fi

git add .
git commit -m "Initialize Continuity Ledger Initiative" || true

gh repo create "$REPO" --public --source . --remote origin --push

echo "Repository created: https://github.com/$REPO"
