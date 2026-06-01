#!/usr/bin/env python3
"""
Inject a "Print or save this worksheet" button + scoped print CSS + JS
into every student lesson page that contains a .worksheet-section or
.worksheet-box wrapper.

Idempotent: skips files that already contain `ws-print-btn`.
Skips capstone pages that already implement their own cert-print scheme
to avoid conflicting print rules.

Usage:
    python3 scripts/inject_worksheet_print_button.py [--dry]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content" / "students"

# Skip pages that already manage their own print scheme (certificate pages etc.)
SKIP_FILES = {
    "class-07/lesson-12.html",
    "class-08/lesson-12.html",
    "class-11/lesson-12.html",
    "class-12/lesson-12.html",
}

CSS_BLOCK = """
/* ── Worksheet print button (injected) ── */
.ws-print-btn { display:inline-flex; align-items:center; gap:0.4rem; background:#0ea5e9; color:#fff; border:none; padding:0.5rem 1rem; border-radius:8px; font-weight:700; font-family:inherit; font-size:0.85rem; cursor:pointer; margin:0.2rem 0 0.9rem; }
.ws-print-btn:hover { background:#0284c7; }
.ws-print-hint { display:inline-block; color:#64748b; font-size:0.78rem; margin:0 0 0.6rem 0.6rem; }
@media print {
  body.printing-worksheet * { visibility: hidden !important; }
  body.printing-worksheet .worksheet-section.printing,
  body.printing-worksheet .worksheet-section.printing *,
  body.printing-worksheet .worksheet-box.printing,
  body.printing-worksheet .worksheet-box.printing * { visibility: visible !important; }
  body.printing-worksheet .worksheet-section.printing,
  body.printing-worksheet .worksheet-box.printing { position: absolute !important; left: 0; top: 0; width: 100%; padding: 1rem !important; border: none !important; background:#fff !important; }
  body.printing-worksheet .ws-print-btn,
  body.printing-worksheet .ws-print-hint,
  body.printing-worksheet .ws-download-note { display: none !important; }
  body.printing-worksheet .ws-table td { min-height: 44px; height: 44px; }
}
"""

JS_BLOCK = """
<script>
// Injected: print just the worksheet section/box without nav, video, quiz, or footer.
function printWorksheet(btn){
  var ws = btn.closest('.worksheet-section, .worksheet-box');
  if(!ws) return;
  ws.classList.add('printing');
  document.body.classList.add('printing-worksheet');
  var cleanup = function(){
    ws.classList.remove('printing');
    document.body.classList.remove('printing-worksheet');
    window.removeEventListener('afterprint', cleanup);
  };
  window.addEventListener('afterprint', cleanup);
  setTimeout(function(){ window.print(); }, 50);
}
</script>
"""

BUTTON_HTML = (
    '    <button class="ws-print-btn" type="button" onclick="printWorksheet(this)">'
    '🖨️ Print or save this worksheet</button>'
    '<span class="ws-print-hint">Tip: in the print dialog, choose "Save as PDF" to download.</span>\n'
)

# Match the opening tag of a worksheet wrapper followed by its first heading
# (h2 or h3, with possible attributes) on the next non-empty line(s).
WRAPPER_RE = re.compile(
    r'(<div\s+class="worksheet-(?:section|box)"[^>]*>\s*\n'
    r'(?:[ \t]*<!--[^\n]*-->\s*\n)*'
    r'[ \t]*<h[23][^>]*>[^<]*</h[23]>\s*\n)',
    re.IGNORECASE,
)


def inject(html: str, rel_path: str) -> tuple[str, int]:
    if "ws-print-btn" in html:
        return html, 0  # already done

    # 1. Insert buttons after each worksheet wrapper's heading
    count = 0
    def _sub(match: re.Match) -> str:
        nonlocal count
        count += 1
        return match.group(1) + BUTTON_HTML

    new_html, n = WRAPPER_RE.subn(_sub, html)
    if n == 0:
        return html, 0

    # 2. Inject CSS before the first </style>
    if "</style>" in new_html:
        new_html = new_html.replace("</style>", CSS_BLOCK + "</style>", 1)
    else:
        # Fallback: prepend a <style> in <head>
        new_html = new_html.replace("</head>", f"<style>{CSS_BLOCK}</style>\n</head>", 1)

    # 3. Inject JS before </body>
    if "</body>" in new_html:
        new_html = new_html.replace("</body>", JS_BLOCK + "\n</body>", 1)
    else:
        new_html += JS_BLOCK

    return new_html, n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="show what would change, do not write")
    args = ap.parse_args()

    files = sorted(CONTENT_DIR.glob("class-*/*.html"))
    changed = 0
    skipped_already = 0
    skipped_no_match = 0

    for f in files:
        rel = f.relative_to(ROOT).as_posix().split("content/students/", 1)[-1]
        if rel in SKIP_FILES:
            print(f"skip (excluded):       {rel}")
            continue
        original = f.read_text(encoding="utf-8")
        if "ws-print-btn" in original:
            skipped_already += 1
            continue
        new_html, n = inject(original, rel)
        if n == 0:
            skipped_no_match += 1
            continue
        if args.dry:
            print(f"would inject {n} button(s) into {rel}")
        else:
            f.write_text(new_html, encoding="utf-8")
            print(f"injected {n} button(s) into {rel}")
        changed += 1

    print()
    print(f"summary: changed={changed}  already_had={skipped_already}  no_worksheet={skipped_no_match}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
