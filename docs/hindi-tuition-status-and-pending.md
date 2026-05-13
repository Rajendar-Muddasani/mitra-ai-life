# Hindi Tuition — Design System, Status, and Pending Work

> Last updated: 13 May 2026  
> Owner: Rajendra Muddasani  
> Platform: mitraailife.com / Hindi Tuition section  
> Audience: 5–8-year-old Hindi beginners and their parents

---

## 0. Latest changes (13 May 2026)

This session shipped:

- **A/V sync fix** applied to all video scripts via shared `scripts/_av_sync.py` (0.3s head + 0.5–1.2s tail silence).
- **OpenAI image API swap**: `dall-e-3` was retired on this account. All scripts now use `gpt-image-1` with `quality="high"`.
- **Word cards regenerated** (65/65) with photorealistic style and pronunciation row: 12 swar + 12 क + 12 ख + 12 ग + 12 घ + 5 ङ.
- **Swar pair cards** now show pronunciation hints (e.g. "i (short, as in 'it')").
- **Barakhadi PNG cards** regenerated with 34px footer labels (fix 4.6).
- **`generate_ka_highlight.py`** rewritten to accept any letter / varga preset.
- **New highlight videos**: ka, kha, ga, gha, **nga** barakhadi detailed videos.
- **New page `h3.html`** (Words and Reading) with 5 topic groups + listening quiz.
- **New page `parent-guide.html`** with pacing, mistake handling, FAQ.
- **Listening quiz** (`hindi-quiz.js` + `hindi-quiz.css`) using browser SpeechSynthesis.
- **Re-rendered videos with A/V sync**: swar-repeat.mp4, vyanjan-letters.mp4, vyanjan-repeat.mp4, swar-word-sync.mp4, barakhadi-sync.mp4, ka/kha/ga/gha/nga-barakhadi-detailed.mp4.
- **Section navigation** and **OG meta tags** updated across h1, h2, h3, parent-guide, tuition.

### Still TODO (requires OpenAI top-up)

The session hit the OpenAI billing hard limit during the h3 video render. To finish:

```bash
# 1. Top up at platform.openai.com / increase the project's hard limit.
# 2. Generate the 20 remaining h3 cards (script auto-skips existing ones):
.venv/bin/python scripts/generate_h3_words.py --cards-only

# 3. Once all 30 h3 cards are present, render the words-reading video:
.venv/bin/python scripts/generate_h3_words.py
```

`h3.html` is hardened against the missing assets: missing cards render as "Coming soon" tiles and the words-reading video section auto-hides until the file exists. Once you regenerate, the page populates without any HTML edits.

---

## 1. Platform Identity and Design Philosophy

### What we are building

A beginner-first Hindi alphabet and pronunciation course delivered entirely through the browser.
No app install. No login required. Works offline after first load.
The child can sit with a parent or elder and watch, listen, and repeat.

### Target learner

| Property | Value |
|---|---|
| Age | 5 to 8 years old (primary target), also useful up to age 10 |
| Prior knowledge | None assumed. Many learners missed or forgot early Hindi in school. |
| Learning environment | At home, usually with a parent or elder sitting nearby |
| Device | Mobile phone first (most Indian homes), also works on desktop |
| Attention span | 3 to 7 minutes per sitting maximum |

### Tone to maintain (non-negotiable)

- **Never shame the child.** Every message is encouraging.
- "No problem, we will learn slowly." — This is the emotional foundation.
- Use "मेरे साथ बोलिए" (say it with me) framing for all audio.
- Praise after every small step: "बहुत अच्छा!" (Very good!)
- No jargon. No "morpheme", "phoneme", "retroflex" for the child. These words are only in code comments and developer docs.
- Patience is embedded in speed: TTS narration at speed 0.65–0.78.

### Visual design system

| Element | Specification |
|---|---|
| Card type | Gradient background (dark-to-dark colour pairs, never pure white cards) |
| Letter rendering | PIL / Pillow — real Unicode Devanagari, never AI-drawn letter shapes |
| Primary font (Devanagari) | Devanagari Sangam MN.ttc (macOS system font) |
| Primary font (Latin) | Arial Unicode.ttf (macOS system font) |
| Card dimensions — square letter card | 512 × 620 px |
| Card dimensions — wide barakhadi row card | 1080 × 480 px |
| Card dimensions — swar pair card | 1080 × 480 px |
| Video resolution | 1080 × 480 or 1080 × 480 depending on card size |
| Video codec | H.264 (libx264), yuv420p, AAC audio |
| TTS engine | OpenAI TTS, model tts-1, voice nova |
| TTS speed — normal pronunciation | 0.72 to 0.82 |
| TTS speed — slow learning / repeat-after-me | 0.65 to 0.72 |
| Repetitions per letter (highlight video) | 4× per matra form |
| Repetitions per letter (standard video) | 2× per form |
| Image illustrations | DALL-E 3, realistic style, child-friendly, white background, no text in image |
| Word card layout | Letter form (large, top band) → DALL-E image (centre) → Hindi word → English pronunciation → English meaning |

### Colour palettes in use

Each consonant varga has its own gradient pair. This helps children associate a colour family with a sound family.

| Varga | Colour A | Colour B |
|---|---|---|
| क-वर्ग | #1a2a6c (deep blue) | #b21f1f (deep red) |
| च-वर्ग | #134e5e (teal) | #71b280 (sage) |
| ट-वर्ग | #4b1248 (deep purple) | #f10711 (vivid red) |
| त-वर्ग | #005c97 (blue) | #363795 (indigo) |
| प-वर्ग | #1a1a2e (dark navy) | #16213e |
| अन्तःस्थ | #373b44 | #4286f4 |
| ऊष्म | #0f0c29 | #302b63 |
| Swar pair a/aa | #c94b4b | #4b134f |
| Swar pair i/ee | #134e5e | #71b280 |
| Swar pair u/oo | #1a1a2e | #4286f4 |
| Swar pair e/ai | #870000 | #c33764 |
| Swar pair o/au | #005c97 | #363795 |
| Swar pair an/ah | #0f9b58 | #00bf8f |

### Navigation model

Every section page has a `<nav class="section-nav">` pill bar at the top:
`Letters and Sounds` | `Barakhadi` | `Words and Reading (soon)` | `Writing (soon)` | `Grammar (soon)`

This replaces the old lesson-link-list approach.
Each pill is a direct page link, not an in-page anchor.
Active pill is highlighted in dark navy.

---

## 2. Scripts and Asset Pipeline

| Script | Purpose | Output |
|---|---|---|
| `scripts/generate_swar_cards.py` | 12 swar PNG cards + swar-letters.mp4 (7× per letter, nova, speed 0.82) | `content/assets/images/swar/`, `content/assets/videos/hindi-h1/swar-letters.mp4` |
| `scripts/generate_swar_pairs.py` | 6 swar pair wide cards + swar-repeat.mp4 (मेरे साथ बोलिए, 3× each, nova, speed 0.78) | `content/assets/images/swar/pair-*.png`, `swar-repeat.mp4` |
| `scripts/generate_vyanjan_cards.py` | 33 vyanjan PNG cards + vyanjan-letters.mp4 (7× per letter, nova, speed 0.82) | `content/assets/images/vyanjan/`, `vyanjan-letters.mp4` |
| `scripts/generate_barakhadi.py` | 33 barakhadi row landscape cards + barakhadi.mp4 (2× per form, Hindi intro, speed 0.65) | `content/assets/images/barakhadi/`, `barakhadi.mp4` |
| `scripts/generate_ka_highlight.py` | ka barakhadi highlight video — each matra lights up while voice says it 4× | `ka-barakhadi-detailed.mp4` |
| `scripts/generate_word_cards.py` | 24 word+image cards using DALL-E 3 (12 swar + 12 ka barakhadi words) | `content/assets/images/word-cards/swar/`, `content/assets/images/word-cards/ka-bara/` |

### Asset naming convention

| Asset type | Pattern | Example |
|---|---|---|
| Swar letter card | `<roman>-card.png` | `a-card.png`, `aa-card.png` |
| Swar pair card | `pair-<name>-card.png` | `pair-a-aa-card.png` |
| Vyanjan card | `<roman>-card.png` | `ka-card.png`, `tta-card.png` |
| Barakhadi row card | `<roman>-bara.png` | `ka-bara.png`, `tta-bara.png` |
| Word+image card | `<slug>.png` | `a.png`, `ka-word.png`, `ke-word.png` |

**macOS case-collision rule:** Retroflex consonants (ट ठ ड ढ ण) use doubled roman prefix (`tta`, `ttha`, `dda`, `ddha`, `nna`) and ष uses `ssha`. Their display labels still show `Ta`, `Tha`, `Da`, `Dha`, `Na`, `Sha`.

---

## 3. Pages Built

| Page | Path | Status |
|---|---|---|
| Tuition landing | `site/tuition.html` | Done — has swar grid, swar video, swar cards, vyanjan grids, vyanjan video, vyanjan cards, barakhadi preview (ka-varga + video + link to h2) |
| Letters and Sounds | `content/tuition/hindi-foundation/h1.html` | Done — swar grid + word cards, swar video, swar letter cards, pair cards + repeat video, vyanjan grids + video + cards, say-it-with-me section |
| Barakhadi | `content/tuition/hindi-foundation/h2.html` | Done — ka highlight video + ka card + ka word cards, full barakhadi video, all 33 row cards grouped by varga with Hindi headings |
| h1-01 to h1-04 | `content/tuition/hindi-foundation/h1-0*.html` | Done but now orphaned — these were old lesson sub-pages, no longer linked from h1.html |

### CSS files

| File | Usage |
|---|---|
| `content/tuition/hindi-foundation/hindi-pack.css` | All tuition section pages |
| `site/track-page.css` | tuition.html landing and related site pages |

Key CSS classes:

| Class | Purpose |
|---|---|
| `.swar-grid` | 6-column grid for letter + label cells |
| `.swar-cell`, `.swar-letter`, `.swar-label` | Individual letter cells in swar/vyanjan grids |
| `.letter-card-grid` | Square letter card grid — `minmax(200px, 1fr)` |
| `.bara-card-grid` | Wide barakhadi row card grid — `minmax(440px, 1fr)`, 2 per row |
| `.word-card-grid` | Word+image card grid — `minmax(160px, 1fr)` |
| `.video-block` | Responsive video container |
| `.section-nav` | Horizontal pill navigation bar |
| `.hero-single-col` | Single-column hero section |

---

## 4. Known Issues — Fix Pending

### 4.1 Word card image realism

**Problem:** DALL-E 3 default style produces flat cartoon / illustration art. The tamarind (इमली) card does not look like a real tamarind. A 5-year-old child will not recognise it as tamarind.  
**Fix needed:** Change DALL-E prompt style from `simple flat cartoon illustration` to `realistic photograph style, studio lighting, white background, isolated subject, no text` for all 24 word cards.  
**Scope:** All 12 swar word cards + all 12 ka barakhadi word cards. Delete existing PNGs and re-run `generate_word_cards.py --set all`.

### 4.2 Word card font sizes too small

**Problem:** On the word card the Hindi word and English meaning text is too small to read comfortably at the rendered page size. The pronunciation label (how the word sounds in English) is missing entirely.  
**Fix needed:**
- Hindi word font: increase from 30 → 40px in `generate_word_cards.py`
- English meaning font: increase from 19 → 24px
- Add a third line for **pronunciation** (e.g. "aam" for आम, "anaar" for अनार) in a distinct colour/size between the Hindi word and English meaning.
- Expand bottom band height from 100px → 140px to fit three lines.
- Update `SWAR_WORDS` and `KA_WORDS` lists to include a `pronunciation` field.

### 4.3 Swar pronunciation labels in the grid are too small

**Problem:** The swar grid below the hero shows `a`, `aa`, `i`, `ee` etc. as small labels under each cell. These are barely readable at mobile size.  
**Fix needed:** Increase `.swar-label` font size from current value to at least `1rem` / `16px`. Also increase `.swar-letter` size if needed.

### 4.4 Video narration not in sync with what is displayed

**Problem:** In all videos (swar-letters.mp4, vyanjan-letters.mp4, barakhadi.mp4, swar-repeat.mp4), the voice says the letter/form before or after the correct card is visible. The audio clip duration does not match the visual hold time cleanly.  
**Root cause:** Current approach plays full audio file then adds a short fixed gap (0.5–0.8s). If the TTS audio overlaps or is assembled without silence padding between clips, the timing appears off.  
**Fix needed (all video scripts):**
- Add 0.3s of silence at the start of each clip before the TTS audio begins (gives visual a moment to register).
- Add 0.5–0.8s silence at the end of each clip after TTS finishes.
- Use `CompositeVideoClip` or `AudioFileClip` with an `offset_t` parameter to delay audio start by 0.3s within each clip.
- Test with ka highlight video first since it has the clearest A/V sync requirement.

### 4.5 Barakhadi card images too small in the page (single-row layout)

**Problem (Screenshot 4):** On the h2.html page, barakhadi cards currently appear in a 2-per-row grid. User wants each row card displayed on its own full-width row so it fills the content column and is readable without zooming.  
**Fix needed:** Change `.bara-card-grid` CSS from `minmax(440px, 1fr)` to `grid-template-columns: 1fr` (single column, full width). Each card then fills the column, making every barakhadi row large and readable.

### 4.6 Footer text on barakhadi cards is unreadable

**Problem (Screenshot 5):** The roman label text at the bottom of each cell in the barakhadi row card (e.g. "e", "ai", "o", "au", "an", "ah") is too small. In the rendered page thumbnail it is nearly invisible.  
**Fix needed in `generate_barakhadi.py`:**
- Increase `f_label` font from 20px → 26px
- Ensure `ly` (label y position) leaves enough space: move to `cy + cell_h - 32`
- Re-run `--cards-only` to regenerate all 33 cards, then rebuild `barakhadi.mp4` (cards re-used in video).

---

## 5. Pending Work — Letters and Sounds Page (h1.html)

| # | Task | Detail |
|---|---|---|
| 1 | Realistic word card images | Re-generate all 12 swar word cards with photorealistic DALL-E prompt |
| 2 | Word card font sizes | Increase Hindi word + meaning fonts, add pronunciation line |
| 3 | Swar grid label size | Increase `.swar-label` font so it is readable on mobile |
| 4 | A/V sync fix for swar-letters.mp4 | Add 0.3s visual-first gap at clip start |
| 5 | A/V sync fix for swar-repeat.mp4 | Same gap fix; also verify "बहुत अच्छा" plays while correct pair card is still visible |
| 6 | Vyanjan label sizes | Same as swar — check `.swar-label` in vyanjan grids |
| 7 | A/V sync fix for vyanjan-letters.mp4 | Same clip-start gap fix |
| 8 | Swar pair cards — add pronunciation | e.g. "a / aa" shown below the letter, above the roman label |
| 9 | Page section header clarity | Add "स्वर (Swar)" and "व्यंजन (Vyanjan)" as bold sub-headings before each grid block |

---

## 6. Pending Work — Barakhadi Page (h2.html)

| # | Task | Detail |
|---|---|---|
| 1 | Barakhadi card footer text size | Increase label font from 20 to 26px in `generate_barakhadi.py`, re-generate all 33 cards |
| 2 | Single-column card layout | Change `.bara-card-grid` to `grid-template-columns: 1fr` so each row card fills the full width |
| 3 | Realistic ka word card images | Re-generate all 12 ka barakhadi word cards with photorealistic DALL-E prompt |
| 4 | Ka word card font + pronunciation | Same fix as swar word cards — add pronunciation line, increase fonts |
| 5 | A/V sync fix for barakhadi.mp4 | Add 0.3s clip-start visual gap |
| 6 | A/V sync fix for ka-barakhadi-detailed.mp4 | Same; also ensure highlighted cell is visible for at least 0.3s before TTS starts |
| 7 | Add word+image cards for ख ग घ ङ varga | Currently only क has word cards. Extend `generate_word_cards.py` with `KHA_WORDS`, `GA_WORDS` etc. and add sections in h2.html |
| 8 | Add remaining varga word cards | च-वर्ग through ह — one word + image per matra form for each consonant |
| 9 | Add highlight videos for ख ग etc. | Create sibling scripts of `generate_ka_highlight.py` or make it varga-configurable with a `--letter` arg |
| 10 | Say-it-with-me section for barakhadi | After each varga section, add a pair-card style "repeat after me" clip for the most common forms |
| 11 | Barakhadi card headings — remove "barakhadi" English word | Headings now read "क-वर्ग barakhadi" — replace with fully Hindi: "क-वर्ग बाराखड़ी" for ALL remaining entries (ट, त, प, अन्तःस्थ, ऊष्म already done; verify क, च) |

---

## 7. Remaining Hindi Tuition Sections (Not Yet Built)

### 7.1 Words and Reading (h3.html — not created yet)

Goal: Child can see a picture, say the Hindi word, and recognise the written form.

Planned structure:
- 3–5 topic groups (animals, food, home objects, body parts, colours)
- Each group: picture → Hindi word → pronunciation → slow TTS reading
- Short 30-second video per topic group
- Listening quiz: "which word do you hear?" — 3 image options

Pending tasks:
- Write 25–30 common Hindi words with pictures and pronunciations
- Generate word+image cards using same `generate_word_cards.py` style
- Build h3.html page
- Generate words-reading.mp4 (slow TTS for each word, 2×)
- Add "Words and Reading" pill to section-nav on h1.html and h2.html

### 7.2 Writing (h4.html — not created yet)

Goal: Child can trace and then write each letter correctly.

Planned structure:
- Show stroke order for each swar (short animation or numbered stroke image)
- Show stroke order for each vyanjan
- Tracing worksheet per varga group (printable PDF or SVG)
- Writing practice: "write the letter 3 times" with guide lines

Pending tasks:
- Decide on stroke-order source: use standard Unicode + PIL-drawn stroke guides, or embed a pre-made SVG font
- Generate stroke-order images for all 12 swar
- Generate stroke-order images for all 33 vyanjan
- Build h4.html page
- Design printable worksheet layout (A4, landscape)
- Generate PDF worksheets per varga group

### 7.3 Grammar (h5.html — not created yet)

Goal: Child understands basic sentence structure and common question patterns.

Planned structure:
- What is a noun / verb / adjective in Hindi (very simple, picture-led)
- Simple sentence frames: subject + verb, subject + object + verb
- Common question words: क्या, कौन, कहाँ, कब, क्यों, कैसे
- Matching exercises: picture → correct sentence

Pending tasks:
- Scope grammar to Grade 2–4 level only (no complex cases)
- Write 10–15 model sentences using words already introduced in section 3
- Build h5.html page

### 7.4 Listening Check / Quiz (across all sections)

Goal: A short interactive check after each section so the child knows if they are ready to move on.

Planned structure:
- 5 audio clips → child taps which letter/word they heard (multiple choice, 3 options)
- 5 picture cards → child says the Hindi word aloud (no auto-grading; parent confirms)
- "Great job!" card if 4/5 correct; "Let us try again" card otherwise

Pending tasks:
- Decide on implementation: pure HTML/JS (no backend) vs hosted quiz tool
- Build reusable quiz component in vanilla JS (no framework dependency)
- Write question sets for swar, vyanjan, barakhadi, and words sections

### 7.5 Parent Guide Page (not created yet)

Goal: Help parents understand how to use the platform with their child.

Planned content:
- How long to study each day (10–15 minutes maximum at age 5–6)
- How to do the repeat-after-me exercises correctly
- What to do when the child gets it wrong (never repeat the mistake; always model the correct sound)
- How to move between sections
- How to download or print worksheets

Pending tasks:
- Write parent guide content in simple English
- Consider adding a short Telugu translation for parents in Andhra Pradesh / Telangana
- Build parent guide HTML page (no navigation section nav — it is a standalone guide)

---

## 8. Infrastructure and Hosting Pending

| # | Task | Detail |
|---|---|---|
| 1 | Large asset hosting | Videos and DALL-E images should move out of the GitHub repo to object storage (Cloudflare R2 or AWS S3) before public launch. Repo is already large. |
| 2 | GitHub Pages deployment | `site/tuition.html` and all content pages need relative-path verification when served from GitHub Pages (not `file://`). Run `scripts/serve-site.sh` and test all asset paths. |
| 3 | OpenGraph / social preview | Add og:image, og:title, og:description to all tuition pages |
| 4 | Analytics | Google Tag Manager tag is already in all pages (G-QGY0LH6W93). Verify it fires correctly in production. |
| 5 | Mobile test | All pages tested only in desktop browser so far. Test on a real Android phone at 375px width. |

---

## 9. Content Quality Rules (non-negotiable before any public share)

1. Every letter shape must come from real Unicode + a known Hindi font — never from an AI-drawn or handwriting-style source that could produce incorrect letterforms.
2. Every word used in a word card must be a real, common Hindi word that a child in Grade 2 would recognise.
3. Every DALL-E image must be reviewed by a human before publishing — reject any image where the object is unclear or culturally unfamiliar.
4. Every TTS narration must be listened to end-to-end before publishing — reject any clip where a letter is mispronounced or the pacing is wrong.
5. Never use the word "wrong" or "mistake" in any learner-facing text. Use "try again" or "one more time".
6. All new Hindi words added to word cards must first appear in a checked word list. Do not invent words from combining letters.

---

## 10. Quick Reference — Immediate Next Steps (Priority Order)

1. **Fix barakhadi card footer labels** — increase font to 26px, re-run `--cards-only`, rebuild video (30 min)
2. **Switch `.bara-card-grid` to single-column** — one-line CSS change (5 min)
3. **Re-generate all 24 word cards with realistic photo prompts** — update `generate_word_cards.py`, delete existing PNGs, re-run (15 min + DALL-E time)
4. **Add pronunciation field to word cards** — add `pronunciation` key to each word entry, update `render_word_card()`, increase bottom band height (45 min)
5. **Fix A/V sync in all 4 video scripts** — add 0.3s visual-first clip gap, re-render videos (45 min + render time per video)
6. **Increase swar grid label font size** — one CSS change (5 min)
7. **Extend word cards to ख ग घ ङ varga** — add word lists, re-run script, update h2.html (60 min + DALL-E time)
8. **Build Words and Reading page (h3.html)** — new page, new word set, new video (3–4 hrs)
9. **Design and generate writing stroke-order assets** — research and script (half day)
10. **Mobile responsive test and fix** — test on physical Android device (1–2 hrs)
