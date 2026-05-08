#!/usr/bin/env zsh
# generate_all_telugu_videos.sh
# Generates Telugu intro videos for Levels 2–10 and uploads each to S3.
# Level 1 is already done. Run from the project root.
#
# Usage:
#   source .env && zsh scripts/generate_all_telugu_videos.sh
#
# To generate a single level only:
#   source .env && zsh scripts/generate_all_telugu_videos.sh 5

set -e
cd "$(dirname "$0")/.."

# Load environment variables from .env if not already exported
if [[ -f ".env" ]]; then
  set -a
  source .env
  set +a
fi

PYTHON=".venv/bin/python"
S3_BUCKET="s3://mitra-ai-life-assets/videos"
AWS_FLAGS="--content-type 'video/mp4' --cache-control 'public, max-age=86400'"

# Check credentials
if [[ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]]; then
  echo "ERROR: GOOGLE_APPLICATION_CREDENTIALS not set. Run: source .env"
  exit 1
fi
if [[ -z "$AWS_ACCESS_KEY_ID" ]]; then
  echo "ERROR: AWS credentials not set. Run: source .env"
  exit 1
fi

# Determine which levels to run
if [[ -n "$1" ]]; then
  LEVELS=($1)
else
  LEVELS=(2 3 4 5 6 7 8 9 10)
fi

for LEVEL in "${LEVELS[@]}"; do
  PADDED=$(printf "%02d" "$LEVEL")
  SCRIPT="scripts/generate_level${PADDED}_video_te.py"
  VIDEO="content/assets/videos/level-${PADDED}-intro-te.mp4"
  S3_KEY="${S3_BUCKET}/level-${PADDED}-intro-te.mp4"

  echo ""
  echo "============================================"
  echo "  Level ${LEVEL} Telugu Video"
  echo "============================================"

  if [[ ! -f "$SCRIPT" ]]; then
    echo "  SKIP: $SCRIPT not found"
    continue
  fi

  echo "  Generating video..."
  $PYTHON "$SCRIPT"

  if [[ ! -f "$VIDEO" ]]; then
    echo "  ERROR: Video not created at $VIDEO"
    exit 1
  fi

  echo "  Uploading to S3: $S3_KEY"
  aws s3 cp "$VIDEO" "$S3_KEY" \
    --content-type "video/mp4" \
    --cache-control "public, max-age=86400"

  echo "  ✅ Level ${LEVEL} done → $S3_KEY"
done

echo ""
echo "============================================"
echo "  All Telugu videos generated and uploaded!"
echo "  Next: update Telugu lesson pages to embed"
echo "  the new videos (Levels 2–10)."
echo "============================================"
