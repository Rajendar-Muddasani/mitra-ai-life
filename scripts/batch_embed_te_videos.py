"""
Batch script:
1. Fixes video container width on ALL comic pages (EN + TE) from
   bad `min(70vw,1280px)` → `width:90%; max-width:1280px`
2. Inserts Telugu intro video section into L2-L10 TE pages
   (right after the hero </section>, before the first Section 2 comment)

Run: python scripts/batch_embed_te_videos.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content" / "english"
S3_SCENES = "https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/scenes"
S3_VIDEOS = "https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/videos"

# ── 1. Fix video container width on all pages ──────────────────────────────
BAD_CONTAINER = 'max-width:min(70vw,1280px); margin:0 auto; text-align:center;'
GOOD_CONTAINER = 'width:90%; max-width:1280px; margin:0 auto; text-align:center;'

# Also fix the section padding (1rem side → 0 side) on video sections
BAD_SECTION_PAD  = 'background:#0f172a; padding: 3rem 1rem 3.5rem;'
GOOD_SECTION_PAD = 'background:#0f172a; padding:3rem 0 3.5rem;'

fixed_count = 0
for html_file in sorted(CONTENT.rglob("*-comic*.html")):
    text = html_file.read_text(encoding="utf-8")
    new_text = text.replace(BAD_CONTAINER, GOOD_CONTAINER)
    new_text = new_text.replace(BAD_SECTION_PAD, GOOD_SECTION_PAD)
    if new_text != text:
        html_file.write_text(new_text, encoding="utf-8")
        print(f"  [FIX] {html_file.name}")
        fixed_count += 1

print(f"Fixed video container on {fixed_count} pages\n")

# ── 2. Insert video section into L2-L10 TE pages ──────────────────────────

LEVELS = {
    2:  {"title": "స్థాయి 2 లో మీరు నేర్చుకునేది",  "hero_img": "img-l2-s01-hero.jpg",  "te_title": "రోజువారీ సహాయం"},
    3:  {"title": "స్థాయి 3 లో మీరు నేర్చుకునేది",  "hero_img": "img-l3-s01-hero.jpg",  "te_title": "స్మార్ట్ బేసిక్స్"},
    4:  {"title": "స్థాయి 4 లో మీరు నేర్చుకునేది",  "hero_img": "img-l4-s01-hero.jpg",  "te_title": "స్మార్ట్ గా పని చేయండి"},
    5:  {"title": "స్థాయి 5 లో మీరు నేర్చుకునేది",  "hero_img": "img-l5-s01-hero.jpg",  "te_title": "జీవితాన్ని అప్ గ్రేడ్ చేయండి"},
    6:  {"title": "స్థాయి 6 లో మీరు నేర్చుకునేది",  "hero_img": "img-l6-s01-hero.jpg",  "te_title": "పవర్ యూజర్"},
    7:  {"title": "స్థాయి 7 లో మీరు నేర్చుకునేది",  "hero_img": "img-l7-s01-hero.jpg",  "te_title": "AI తో నిర్మించండి"},
    8:  {"title": "స్థాయి 8 లో మీరు నేర్చుకునేది",  "hero_img": "img-l8-s01-hero.jpg",  "te_title": "AI for బిజినెస్"},
    9:  {"title": "స్థాయి 9 లో మీరు నేర్చుకునేది",  "hero_img": "img-l9-s01-hero.jpg",  "te_title": "AI తో సంపాదన"},
    10: {"title": "స్థాయి 10 లో మీరు నేర్చుకునేది", "hero_img": "img-l10-s01-hero.jpg", "te_title": "AI సేఫ్టీ"},
}

LEVEL_DIRS = {
    2: "level-02-daily-help",
    3: "level-03-smart-basics",
    4: "level-04-work-smart",
    5: "level-05-life-upgrade",
    6: "level-06-power-user",
    7: "level-07-build-with-ai",
    8: "level-08-ai-for-business",
    9: "level-09-ai-for-income",
    10: "level-10-ai-safety",
}


def video_section_html(n, info):
    padded = f"{n:02d}"
    poster  = f"{S3_SCENES}/{info['hero_img']}"
    src     = f"{S3_VIDEOS}/level-{padded}-intro-te.mp4"
    return f"""
<!-- SECTION 1b — INTRO VIDEO (Telugu) -->
<section style="background:#0f172a; padding:3rem 0 3.5rem;">
  <div style="width:90%; max-width:1280px; margin:0 auto; text-align:center;">
    <div style="color:rgba(255,255,255,0.55);font-size:0.75rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.75rem;">
      ముందు చూడండి · 2 నిమిషాలు
    </div>
    <h2 style="color:#fff;font-size:clamp(1.2rem,3vw,1.7rem);font-weight:800;margin:0 0 1.25rem;">
      {info['title']}
    </h2>
    <div style="position:relative;width:100%;padding-top:56.25%;border-radius:14px;overflow:hidden;
                box-shadow:0 8px 40px rgba(0,0,0,0.55);background:#000;">
      <video
        id="l{n}-intro-video-te"
        controls
        preload="none"
        poster="{poster}"
        style="position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover;">
        <source src="{src}" type="video/mp4">
        మీ browser video tag ని support చేయడం లేదు.
      </video>
    </div>
    <p style="color:rgba(255,255,255,0.5);font-size:0.8rem;margin-top:0.75rem;">
      Sign-in అవసరం లేదు · Telugu narration
    </p>
  </div>
</section>

"""


def insert_video_section(html_path, n, info):
    text = html_path.read_text(encoding="utf-8")

    # Already has video — skip
    if f"level-{n:02d}-intro-te.mp4" in text:
        print(f"  [SKIP] L{n} already has video embed")
        return False

    # Find first </section> after which section 2 comment appears
    # Strategy: find the hero </section> then insert after it
    # The hero section always ends with </section>\n\n then a comment
    # We look for the pattern: </section>\n\n\n<!-- or </section>\n\n<!--
    pattern = re.compile(r'(</section>)\s*\n(\s*\n)*(\s*<!--)')
    match = pattern.search(text)
    if not match:
        print(f"  [WARN] L{n}: could not find hero </section> insertion point")
        return False

    insert_pos = match.start(3)  # Before the first <!-- after hero
    new_text = text[:insert_pos] + video_section_html(n, info) + text[insert_pos:]
    html_path.write_text(new_text, encoding="utf-8")
    print(f"  [ADD] L{n} TE video section → {html_path.name}")
    return True


added = 0
for n in range(2, 11):
    level_dir = CONTENT / LEVEL_DIRS[n]
    te_page = level_dir / f"level-{n:02d}-comic-te.html"
    if not te_page.exists():
        print(f"  [MISS] {te_page} not found — skip")
        continue
    if insert_video_section(te_page, n, LEVELS[n]):
        added += 1

print(f"\nInserted video sections on {added} Telugu lesson pages")
print("Done!")
