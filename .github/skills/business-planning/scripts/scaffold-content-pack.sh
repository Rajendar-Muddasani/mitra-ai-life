#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: scaffold-content-pack.sh <level-slug> <lesson-slug>"
  exit 1
fi

level_slug="$1"
lesson_slug="$2"
root_dir="$(cd "$(dirname "$0")/../../../../" && pwd)"
en_dir="$root_dir/content/english/$level_slug"
te_dir="$root_dir/content/telugu/$level_slug"

en_file="$en_dir/$lesson_slug.md"
te_file="$te_dir/$lesson_slug-te.md"

mkdir -p "$en_dir" "$te_dir"

if [[ ! -f "$en_file" ]]; then
  cat > "$en_file" <<EOF
# ${lesson_slug//-/ }

## Objective

## Target learner

## Story setup

## Practical prompts
1.
2.
3.

## Caution note

## Asset ideas
- comic:
- image slides:
- short video:

## Worksheet activity
EOF
fi

if [[ ! -f "$te_file" ]]; then
  cat > "$te_file" <<EOF
# ${lesson_slug//-/ }

## లక్ష్యం

## లక్ష్య విద్యార్థి

## కథా పరిచయం

## ప్రాక్టికల్ ప్రాంప్ట్‌లు
1.
2.
3.

## జాగ్రత్త గమనిక

## ఆస్తి ఆలోచనలు
- కామిక్:
- ఇమేజ్ స్లైడ్స్:
- చిన్న వీడియో:

## వర్క్‌షీట్ కార్యక్రమం
EOF
fi

echo "Created: $en_file"
echo "Created: $te_file"
