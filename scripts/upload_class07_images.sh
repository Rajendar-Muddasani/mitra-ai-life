#!/usr/bin/env bash
# upload_class07_images.sh
# Uploads Class 7 lesson hero images to S3.
# Run after: .venv/bin/python scripts/generate_class07_images.py
#
# Usage:
#   bash scripts/upload_class07_images.sh
#
# Requires: AWS CLI configured (aws configure) or AWS env vars in .env

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Load .env if present
if [[ -f "$REPO_ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$REPO_ROOT/.env"
  set +a
fi

BUCKET="mitra-ai-life-assets"
REGION="${AWS_DEFAULT_REGION:-us-west-2}"
LOCAL_DIR="$REPO_ROOT/content/assets/students/class-07"
S3_PREFIX="students/class-07"

if [[ ! -d "$LOCAL_DIR" ]]; then
  echo "ERROR: $LOCAL_DIR does not exist. Run generate_class07_images.py first."
  exit 1
fi

echo "Uploading Class 7 hero images to s3://${BUCKET}/${S3_PREFIX}/"
echo ""

aws s3 sync "$LOCAL_DIR" "s3://${BUCKET}/${S3_PREFIX}" \
  --region "$REGION" \
  --content-type "image/jpeg" \
  --exclude "*.DS_Store" \
  --exclude ".gitkeep"

echo ""
echo "Done. Verify one URL:"
echo "  curl -I https://${BUCKET}.s3.${REGION}.amazonaws.com/${S3_PREFIX}/lesson-01-hero.jpg"
