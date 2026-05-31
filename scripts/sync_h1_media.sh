#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root_dir"

python_bin="${PYTHON_BIN:-$root_dir/.venv/bin/python}"
if [[ ! -x "$python_bin" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    python_bin="$(command -v python3)"
  else
    echo "Python not found. Set PYTHON_BIN or create .venv/bin/python." >&2
    exit 1
  fi
fi

if [[ $# -gt 0 ]]; then
  lessons=("$@")
else
  lessons=(H1-01 H1-02 H1-03 H1-04)
fi

echo "Rendering H1 lesson pages from shared content..."
"$python_bin" scripts/render_h1_shared_content.py

echo "Rebuilding H1 videos for: ${lessons[*]}"
"$python_bin" scripts/generate_h1_sample_pack_videos.py --lesson "${lessons[@]}"

echo "H1 sync complete."