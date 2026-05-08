#!/usr/bin/env bash
# upload_class06_images.sh
# Uploads Class 6 lesson hero images to S3.
# Run after: .venv/bin/python scripts/generate_class06_images.py
#
# Usage:
#   bash scripts/upload_class06_images.sh
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
LOCAL_DIR="$REPO_ROOT/content/assets/students/class-06"
S3_PREFIX="students/class-06"

if [[ ! -d "$LOCAL_DIR" ]]; then
  echo "ERROR: $LOCAL_DIR does not exist. Run generate_class06_images.py first."
  exit 1
fi

echo "Uploading Class 6 hero images to s3://${BUCKET}/${S3_PREFIX}/"
echo ""

aws s3 sync "$LOCAL_DIR" "s3://${BUCKET}/${S3_PREFIX}" \
  --region "$REGION" \
  --acl public-read \
  --content-type "image/jpeg" \
  --exclude "*.DS_Store" \
  --exclude ".gitkeep"

echo ""
echo "Done. Images available at:"
echo "  https://${BUCKET}.s3.${REGION}.amazonaws.com/${S3_PREFIX}/lesson-01-hero.jpg"
echo "  ... through ..."
echo "  https://${BUCKET}.s3.${REGION}.amazonaws.com/${S3_PREFIX}/lesson-12-hero.jpg"
