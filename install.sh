#!/usr/bin/env bash
# Link every skill in this repository into the shared agent skills folders.
# Safe to re-run. Usage: ./install.sh
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
targets=("$HOME/.agents/skills" "$HOME/.claude/skills")

for skill in "$repo"/*/; do
  [ -f "$skill/SKILL.md" ] || continue
  name="$(basename "$skill")"
  for target in "${targets[@]}"; do
    mkdir -p "$target"
    if [ -e "$target/$name" ] && [ ! -L "$target/$name" ]; then
      echo "skip $target/$name: a real folder is there, not a link" >&2
      continue
    fi
    ln -sfn "${skill%/}" "$target/$name"
    echo "linked $target/$name"
  done
done
