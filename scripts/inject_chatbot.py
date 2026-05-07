"""
Inject mitra-chat.js into all learner HTML pages (not pitch-deck).
"""
import os
from pathlib import Path

ROOT = Path(".")

HTML_FILES = sorted([
    p for p in ROOT.rglob("*.html")
    if ".git" not in str(p) and ".venv" not in str(p)
    and "pitch-deck" not in str(p)
])

print("Files to inject:")
for f in HTML_FILES:
    print(" ", f)

SCRIPT_COMMENT = "<!-- Mitra chatbot widget -->"

for html_file in HTML_FILES:
    rel = os.path.relpath("site/mitra-chat.js", html_file.parent)
    # Normalise to forward slashes for HTML
    rel = rel.replace("\\", "/")
    script_tag = f'<script src="{rel}"></script>'
    tag_block = f"  {SCRIPT_COMMENT}\n  {script_tag}\n"

    content = html_file.read_text(encoding="utf-8")

    if "mitra-chat.js" in content:
        print(f"  SKIP (already injected): {html_file}")
        continue

    new_content = content.replace("</body>", tag_block + "</body>", 1)
    if new_content == content:
        print(f"  WARNING: </body> not found in {html_file}")
        continue

    html_file.write_text(new_content, encoding="utf-8")
    print(f"  OK: {html_file}  (src: {rel})")

print("\nDone.")
