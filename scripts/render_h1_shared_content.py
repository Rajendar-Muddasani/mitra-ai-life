from __future__ import annotations

import json
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "content" / "tuition" / "hindi-foundation" / "manifests" / "h1-shared-content.json"
READING_START = "<!-- AUTO:READING START -->"
READING_END = "<!-- AUTO:READING END -->"
SCENES_START = "<!-- AUTO:SCENES START -->"
SCENES_END = "<!-- AUTO:SCENES END -->"


def load_data() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def render_reading_section(lesson: dict) -> str:
    reading = lesson["reading"]
    cards_html = "\n".join(
        (
            "      <div class=\"reading-card\">"
            f"<span class=\"reading-letter devanagari\">{escape(card['letter'])}</span>"
            f"<span class=\"reading-word devanagari\">{escape(card['word'])}</span>"
            f"<span class=\"reading-gloss\">{escape(card['gloss'])}</span>"
            "</div>"
        )
        for card in reading["cards"]
    )
    return "\n".join(
        [
            READING_START,
            "  <section class=\"section\">",
            f"    <div class=\"tag\">{escape(reading['label'])}</div>",
            f"    <h2>{escape(reading['heading'])}</h2>",
            f"    <p>{escape(reading['body'])}</p>",
            f"    <div class=\"reading-grid {escape(reading['columns'])}\">",
            cards_html,
            "    </div>",
            f"    <p class=\"reading-note\">{escape(reading['note'])}</p>",
            "  </section>",
            READING_END,
        ]
    )


def render_scene_section(lesson: dict) -> str:
    scenes = lesson["scenes"]
    boards_html = []
    for board in scenes["boards"]:
        chips_class = "scene-board-chips" if len(board["chips"]) > 2 else "scene-board-footer"
        chips = "\n".join(f"            <span class=\"scene-chip\">{escape(chip)}</span>" for chip in board["chips"])
        boards_html.append(
            "\n".join(
                [
                    "      <article class=\"lesson-card scene-card\">",
                    f"        <div class=\"scene-board {escape(board['theme'])}\" role=\"img\" aria-label=\"{escape(board['aria'])}\">",
                    "          <div class=\"scene-board-header\">",
                    f"            <span class=\"scene-board-label\">{escape(board['label'])}</span>",
                    f"            <span class=\"scene-board-scene\">{escape(board['badge'])}</span>",
                    "          </div>",
                    "          <div class=\"scene-board-main\">",
                    f"            <p class=\"scene-board-title\">{escape(board['title'])}</p>",
                    f"            <p class=\"scene-board-hindi\">{escape(board['hindi'])}</p>",
                    f"            <p class=\"scene-board-caption\">{escape(board['caption'])}</p>",
                    "          </div>",
                    f"          <div class=\"{chips_class}\">",
                    chips,
                    "          </div>",
                    "        </div>",
                    "        <div class=\"scene-content\">",
                    f"          <div class=\"scene-meta\"><span class=\"scene-step\">{escape(board['summaryBadge'])}</span></div>",
                    f"          <h3>{escape(board['summaryTitle'])}</h3>",
                    f"          <p>{escape(board['summaryText'])}</p>",
                    "        </div>",
                    "      </article>",
                ]
            )
        )
    return "\n".join(
        [
            SCENES_START,
            "  <section class=\"section\" id=\"lesson-scenes\">",
            f"    <div class=\"tag\">{escape(scenes['label'])}</div>",
            f"    <h2>{escape(scenes['heading'])}</h2>",
            f"    <p>{escape(scenes['body'])}</p>",
            "    <div class=\"scene-flow\">",
            "\n".join(boards_html),
            "    </div>",
            "  </section>",
            SCENES_END,
        ]
    )


def replace_block(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.index(start_marker)
    end = text.index(end_marker) + len(end_marker)
    return text[:start] + replacement + text[end:]


def render_pages() -> None:
    data = load_data()
    for lesson in data.values():
        page_path = ROOT / lesson["page"]
        source = page_path.read_text(encoding="utf-8")
        source = replace_block(source, READING_START, READING_END, render_reading_section(lesson))
        source = replace_block(source, SCENES_START, SCENES_END, render_scene_section(lesson))
        page_path.write_text(source, encoding="utf-8")
        print(f"Updated {page_path}")


if __name__ == "__main__":
    render_pages()