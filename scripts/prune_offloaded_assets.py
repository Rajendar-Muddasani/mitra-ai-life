#!/usr/bin/env python3
"""Prune local content/assets files only after confirming matching S3 keys exist.

By default this targets the largest public asset folders that are already served
from S3 and runs in dry-run mode.

Examples:
  source .venv/bin/activate
  python scripts/prune_offloaded_assets.py
  python scripts/prune_offloaded_assets.py --path content/assets/students --apply
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import boto3


ROOT = Path(__file__).resolve().parent.parent
ASSET_ROOT = ROOT / "content" / "assets"
BUCKET = "mitra-ai-life-assets"
REGION = os.environ.get("AWS_DEFAULT_REGION", "us-west-2")
DEFAULT_TARGETS = [
    "content/assets/students",
    "content/assets/videos",
    "content/assets/scenes",
    "content/assets/images",
    "content/assets/characters",
    "content/assets/mitra-icons",
]


def load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def format_bytes(size: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.2f} {unit}"
        value /= 1024
    return f"{size} B"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Delete local content/assets files only if the exact S3 key already exists."
    )
    parser.add_argument(
        "--path",
        action="append",
        dest="paths",
        help="Asset path to scan. Repeat to target multiple folders. Defaults to the main public asset folders.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually delete the confirmed offloaded local files. Dry-run is the default.",
    )
    parser.add_argument(
        "--show-missing",
        type=int,
        default=20,
        help="How many local files missing from S3 to print in the summary. Default: 20.",
    )
    return parser.parse_args()


def resolve_targets(raw_paths: list[str] | None) -> list[Path]:
    targets = raw_paths or DEFAULT_TARGETS
    resolved: list[Path] = []
    for raw_path in targets:
        candidate = Path(raw_path)
        if not candidate.is_absolute():
            candidate = ROOT / candidate
        candidate = candidate.resolve()
        if candidate != ASSET_ROOT and ASSET_ROOT not in candidate.parents:
            raise SystemExit(f"Refusing to operate outside {ASSET_ROOT}: {candidate}")
        if not candidate.exists():
            print(f"skip: path does not exist: {candidate}")
            continue
        resolved.append(candidate)
    if not resolved:
        raise SystemExit("No valid target paths found.")
    return resolved


def make_s3_client():
    kwargs = {"region_name": REGION}
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    session_token = os.environ.get("AWS_SESSION_TOKEN")
    if access_key and secret_key:
        kwargs["aws_access_key_id"] = access_key
        kwargs["aws_secret_access_key"] = secret_key
        if session_token:
            kwargs["aws_session_token"] = session_token
    return boto3.client("s3", **kwargs)


def s3_prefix_for(target: Path) -> str:
    relative = target.relative_to(ASSET_ROOT).as_posix()
    if target.is_dir() and relative:
        return relative.rstrip("/") + "/"
    return relative


def fetch_remote_keys(client, prefixes: list[str]) -> set[str]:
    paginator = client.get_paginator("list_objects_v2")
    remote_keys: set[str] = set()
    for prefix in prefixes:
        for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix):
            for item in page.get("Contents", []):
                remote_keys.add(item["Key"])
    return remote_keys


def iter_local_files(targets: list[Path]):
    seen: set[Path] = set()
    for target in targets:
        candidates = [target] if target.is_file() else sorted(path for path in target.rglob("*") if path.is_file())
        for file_path in candidates:
            if file_path in seen:
                continue
            seen.add(file_path)
            yield file_path


def remove_empty_dirs(targets: list[Path]) -> None:
    dirs: set[Path] = set()
    for target in targets:
        if not target.is_dir():
            continue
        dirs.add(target)
        dirs.update(path for path in target.rglob("*") if path.is_dir())
    for dir_path in sorted(dirs, key=lambda path: len(path.parts), reverse=True):
        try:
            dir_path.rmdir()
        except OSError:
            continue


def main() -> int:
    load_env()
    args = parse_args()
    targets = resolve_targets(args.paths)
    prefixes = [s3_prefix_for(path) for path in targets]

    client = make_s3_client()
    remote_keys = fetch_remote_keys(client, prefixes)
    if not remote_keys:
        raise SystemExit("No matching S3 objects found for the selected prefixes. Aborting.")

    candidates: list[tuple[Path, int, str]] = []
    missing: list[tuple[Path, int, str]] = []
    scanned_files = 0
    scanned_bytes = 0

    for file_path in iter_local_files(targets):
        key = file_path.relative_to(ASSET_ROOT).as_posix()
        size = file_path.stat().st_size
        scanned_files += 1
        scanned_bytes += size
        if key in remote_keys:
            candidates.append((file_path, size, key))
        else:
            missing.append((file_path, size, key))

    candidate_bytes = sum(size for _, size, _ in candidates)
    missing_bytes = sum(size for _, size, _ in missing)

    print(f"bucket: {BUCKET} ({REGION})")
    print("targets:")
    for target in targets:
        print(f"  - {target.relative_to(ROOT)}")
    print(f"scanned local files: {scanned_files} ({format_bytes(scanned_bytes)})")
    print(f"confirmed in S3: {len(candidates)} ({format_bytes(candidate_bytes)})")
    print(f"missing from S3: {len(missing)} ({format_bytes(missing_bytes)})")

    if missing and args.show_missing > 0:
        print("sample local files kept because no matching S3 key was found:")
        for file_path, size, key in missing[: args.show_missing]:
            print(f"  - {key} ({format_bytes(size)})")

    if not args.apply:
        print("dry-run complete; re-run with --apply to delete the confirmed local copies")
        return 0

    deleted_files = 0
    deleted_bytes = 0
    for file_path, size, _ in candidates:
        file_path.unlink()
        deleted_files += 1
        deleted_bytes += size

    remove_empty_dirs(targets)
    print(f"deleted local files: {deleted_files} ({format_bytes(deleted_bytes)})")
    if missing:
        print("kept local-only files that are not present in S3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())