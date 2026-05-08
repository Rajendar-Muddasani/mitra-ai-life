#!/usr/bin/env python3
"""Inject favicon/app icon tags into all top-level site HTML pages.

Idempotent: pages that already contain rel="icon" are skipped.
"""

from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

TAG_BLOCK_INLINE = (
    '<link rel="icon" href="favicon.ico" sizes="any" />'
    '<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png" />'
    '<link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png" />'
    '<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png" />'
    '<link rel="manifest" href="site.webmanifest" />'
    '<meta name="theme-color" content="#06111f" />'
)

TAG_BLOCK_PRETTY = (
    '  <link rel="icon" href="favicon.ico" sizes="any" />\n'
    '  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png" />\n'
    '  <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png" />\n'
    '  <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png" />\n'
    '  <link rel="manifest" href="site.webmanifest" />\n'
    '  <meta name="theme-color" content="#06111f" />\n'
)


def inject(html: str) -> str:
    if 'rel="icon"' in html:
        return html

    pretty = '<head>\n' in html
    tag_block = TAG_BLOCK_PRETTY if pretty else TAG_BLOCK_INLINE

    canonical_match = re.search(r'(<link rel="canonical"[^>]+/>)', html)
    if canonical_match:
        anchor = canonical_match.group(1)
        if pretty:
            return html.replace(anchor, anchor + '\n' + tag_block, 1)
        return html.replace(anchor, anchor + tag_block, 1)

    robots_match = re.search(r'(<meta name="robots"[^>]+/>)', html)
    if robots_match:
        anchor = robots_match.group(1)
        if pretty:
            return html.replace(anchor, anchor + '\n' + tag_block, 1)
        return html.replace(anchor, anchor + tag_block, 1)

    viewport_match = re.search(r'(<meta name="viewport"[^>]+/>)', html)
    if viewport_match:
        anchor = viewport_match.group(1)
        if pretty:
            return html.replace(anchor, anchor + '\n' + tag_block, 1)
        return html.replace(anchor, anchor + tag_block, 1)

    raise RuntimeError('No insertion anchor found')


def main() -> None:
    for file_path in sorted(SITE.glob('*.html')):
        html = file_path.read_text(encoding='utf-8')
        updated = inject(html)
        if updated != html:
            file_path.write_text(updated, encoding='utf-8')
            print(f'updated site/{file_path.name}')
        else:
            print(f'skipped site/{file_path.name}')


if __name__ == '__main__':
    main()
