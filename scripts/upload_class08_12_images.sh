#!/usr/bin/env bash
# upload_class08_12_images.sh
# Uploads Class 8–12 lesson hero images to S3.
# Run after: .venv/bin/python scripts/generate_class08_12_images.py
#
# Usage:
#   bash scripts/upload_class08_12_images.sh [08|09|10|11|12]
#   (no argument = upload all 5 classes)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -f "$REPO_ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$REPO_ROOT/.env"
  set +a
fi

BUCKET="mitra-ai-life-assets"
REGION="${AWS_DEFAULT_REGION:-us-west-2}"

CLASSES=("08" "09" "10" "11" "12")
if [[ $# -ge 1 ]]; then
  CLASSES=("$1")
fi

for CLASS in "${CLASSES[@]}"; do
  LOCAL_DIR="$REPO_ROOT/content/assets/students/class-$CLASS"
  S3_PREFIX="students/class-$CLASS"

  if [[ ! -d "$LOCAL_DIR" ]]; then
    echo "SKIP class-$CLASS: directory not found ($LOCAL_DIR)"
    continue
  fi

  IMG_COUNT=$(find "$LOCAL_DIR" -name "*.jpg" | wc -l | tr -d ' ')
  if [[ "$IMG_COUNT" -eq 0 ]]; then
    echo "SKIP class-$CLASS: no .jpg files found"
    continue
  fi

  echo "Uploading Class $CLASS ($IMG_COUNT images) → s3://${BUCKET}/${S3_PREFIX}/"
  aws s3 sync "$LOCAL_DIR" "s3://${BUCKET}/${S3_PREFIX}" \
    --region "$REGION" \
    --content-type "image/jpeg" \
    --exclude "*.DS_Store" \
    --exclude ".gitkeep"
  echo "  ✓ Class $CLASS done"
done

echo ""
echo "All done. Verify one URL:"
echo "  curl -I https://${BUCKET}.s3.${REGION}.amazonaws.com/students/class-08/lesson-01-hero.jpg"
