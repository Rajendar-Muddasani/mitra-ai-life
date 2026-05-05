#!/usr/bin/env python3
"""
deploy_s3.py
  1. Creates S3 bucket  mitra-ai-life-assets  (if not exists)
  2. Makes it publicly readable
  3. Uploads everything under  content/assets/
  4. Rewrites asset paths in level-01, level-02, and index.html to CDN URLs
"""

import os, sys, json, pathlib, mimetypes

# ── load .env ──────────────────────────────────────────────────────────────────
ROOT = pathlib.Path(__file__).parent.parent
env_path = ROOT / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

BUCKET   = "mitra-ai-life-assets"
REGION   = os.environ.get("AWS_DEFAULT_REGION", "us-west-2")
ASSETS   = ROOT / "content" / "assets"
CDN_BASE = f"https://{BUCKET}.s3.{REGION}.amazonaws.com/"

import boto3
from botocore.exceptions import ClientError

s3 = boto3.client(
    "s3",
    region_name=REGION,
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
)

# ── 1. create bucket ───────────────────────────────────────────────────────────
print(f"\n🪣  Creating bucket  {BUCKET}  in  {REGION}")
try:
    if REGION == "us-east-1":
        s3.create_bucket(Bucket=BUCKET)
    else:
        s3.create_bucket(
            Bucket=BUCKET,
            CreateBucketConfiguration={"LocationConstraint": REGION},
        )
    print("   ✅  Bucket created")
except ClientError as e:
    code = e.response["Error"]["Code"]
    if code in ("BucketAlreadyOwnedByYou",):
        print("   ℹ️   Bucket already owned by you — skipping creation")
    elif code == "BucketAlreadyExists":
        print("   ❌  Name taken by another AWS account — change BUCKET name in script")
        sys.exit(1)
    else:
        raise

# ── 2. disable block public access ────────────────────────────────────────────
print("🔓  Disabling block public access ...")
s3.put_public_access_block(
    Bucket=BUCKET,
    PublicAccessBlockConfiguration={
        "BlockPublicAcls":        False,
        "IgnorePublicAcls":       False,
        "BlockPublicPolicy":      False,
        "RestrictPublicBuckets":  False,
    },
)

# ── 3. public-read bucket policy ──────────────────────────────────────────────
print("📋  Setting public-read bucket policy ...")
policy = json.dumps({
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "PublicReadGetObject",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": f"arn:aws:s3:::{BUCKET}/*"
    }]
})
s3.put_bucket_policy(Bucket=BUCKET, Policy=policy)
print("   ✅  Policy set")

# ── 4. upload assets ───────────────────────────────────────────────────────────
print(f"\n📤  Uploading assets from  content/assets/")
if not ASSETS.exists():
    print("   ❌  content/assets/ not found — aborting")
    sys.exit(1)

files = sorted(f for f in ASSETS.rglob("*") if f.is_file())
print(f"   Found {len(files)} files\n")

for i, fp in enumerate(files, 1):
    key = fp.relative_to(ASSETS).as_posix()   # e.g.  scenes/img-l2-s01-hero.jpg
    ct, _ = mimetypes.guess_type(str(fp))
    ct = ct or "application/octet-stream"
    size_kb = fp.stat().st_size // 1024
    print(f"   [{i:02}/{len(files):02}]  {key}  ({size_kb} KB) ...", end=" ", flush=True)
    s3.upload_file(str(fp), BUCKET, key, ExtraArgs={"ContentType": ct})
    print("✅")

print(f"\n🌐  CDN base:  {CDN_BASE}")

# ── 5. rewrite HTML asset paths ────────────────────────────────────────────────
HTML_TARGETS = [
    (ROOT / "content/english/level-01-interactive/level-01-comic.html", "../../assets/"),
    (ROOT / "content/english/level-02-daily-help/level-02-comic.html",  "../../assets/"),
    (ROOT / "site/index.html",                                           "../content/assets/"),
]

print("\n✏️   Rewriting HTML asset paths → CDN URLs ...")
for html_path, old_prefix in HTML_TARGETS:
    if not html_path.exists():
        print(f"   ⚠️  {html_path.name} not found — skipping")
        continue
    content = html_path.read_text(encoding="utf-8")
    count = content.count(old_prefix)
    if count == 0:
        print(f"   ℹ️  {html_path.name} — already updated (no local refs found)")
        continue
    html_path.write_text(content.replace(old_prefix, CDN_BASE), encoding="utf-8")
    print(f"   ✅  {html_path.name} — {count} reference(s) replaced")

# ── 6. create root redirect for GitHub Pages ──────────────────────────────────
root_index = ROOT / "index.html"
if not root_index.exists():
    print("\n📄  Creating root index.html (GitHub Pages redirect) ...")
    root_index.write_text(
        '<!DOCTYPE html><html><head>'
        '<meta http-equiv="refresh" content="0;url=site/index.html">'
        '<title>Mitra AI Life</title></head>'
        '<body><a href="site/index.html">Go to site</a></body></html>\n',
        encoding="utf-8",
    )
    print("   ✅  index.html created")

print("\n──────────────────────────────────────────────────────")
print("✅  All done!")
print(f"\n   CDN base:   {CDN_BASE}")
print( "   Next steps:")
print( "     1. git add -A && git commit -m 'deploy: S3 CDN paths + root redirect'")
print( "     2. git push")
print( "     3. GitHub repo → Settings → Pages → Branch: main  /  (root)")
print( "     4. Your live URL: https://rajendarmuddasani.github.io/mitra-ai-life/")
