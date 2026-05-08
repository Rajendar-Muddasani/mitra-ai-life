# Mitra AI Life — Task Log

Simple running record of everything completed, decided, or noted.
Format: `#` | Date | Time | Task / Decision / Note | Remarks

---

| # | Date | Time | Task / Decision / Note | Remarks |
|---|------|------|------------------------|---------|
| 1 | 05 May 2026 | 21:29 | Initial commit — repo created on GitHub | Branch: main |
| 2 | 05 May 2026 | 22:43 | Brand name decided: Mitra AI Life Education | Planning docs + pitch deck HTML + PPTX + Level 1 outline added |
| 3 | 05 May 2026 | 23:17 | Level 1 interactive content added + investor PPTX script | First real lesson page |
| 4 | 05 May 2026 | 23:39 | Level 1 upgraded to real DALL-E 3 images | Images generated and pushed to S3 |
| 5 | 05 May 2026 | 23:48 | Landing page (site/index.html) created | Hero, level ladder, demos, language toggle, CTA |
| 6 | 05 May 2026 | 23:57 | Level 2 Daily Help added | HTML + image generation script |
| 7 | 06 May 2026 | 00:29 | AWS S3 CDN paths set up + root redirect + deploy script | S3 bucket: mitra-ai-life-assets |
| 8 | 06 May 2026 | 01:16 | GA4 placeholder added + language toggle + Telugu pages stub + CNAME for custom domain | Domain: mitraailife.com |
| 9 | 06 May 2026 | 10:59 | Major UX pass: 16-tile audience grid, demo cards, broken S3 images fixed, hero contrast overlay, Disqus comments | — |
| 10 | 06 May 2026 | 12:11 | Hero banner dark overlay added (text visibility fix) + brand → home link | — |
| 11 | 06 May 2026 | 12:22 | Level 1 hero image fixed + Level 2 Disqus + bigger titles + language dropdown | — |
| 12 | 06 May 2026 | 13:38 | GA4 tracking activated (G-QGY0LH6W93) on all 6 HTML pages | — |
| 13 | 06 May 2026 | 14:00 | Disqus comments activated (shortname: mitra-ai-life) on L1 and L2 | — |
| 14 | 06 May 2026 | 14:08 | Level 2 content expanded — prompt formula, language-agnostic labels, Telugu prompts, travel packing card | — |
| 15 | 06 May 2026 | 14:24 | 5-question quiz + printable certificate added to Level 1 and Level 2 | — |
| 16 | 06 May 2026 | 14:45 | Full Telugu Level 1 lesson page created (level-01-comic-te.html) | — |
| 17 | 06 May 2026 | 15:01 | Full Telugu Level 2 lesson page created (level-02-comic-te.html) | 1076 lines, all 10 sections, quiz, teal cert |
| 18 | 06 May 2026 | 15:28 | Supabase Google OAuth + progress tracking added to all 6 pages | auth.js, nav login button, quiz saveProgress |
| 19 | 06 May 2026 | 15:46 | Auth OAuth redirect fix — trailing slash bug resolved | Home page OAuth now works |
| 20 | 06 May 2026 | 19:29 | Investor pitch deck created — 11 slides, keyboard nav, dark theme | site/pitch-deck.html |
| 21 | 06 May 2026 | 19:36 | Pitch deck slide 1 bug fixed (classList.add('') halting nav) | — |
| 22 | 06 May 2026 | 19:55 | Pitch deck expanded to 12 slides — 5 problem cards, before/after slide, TAM/SAM/SOM | — |
| 23 | 06 May 2026 | 21:30 | Decision: founder name removed from pitch deck and all public pages | Privacy rule — no personal name anywhere |
| 24 | 06 May 2026 | 22:09 | Level 3 Smart Basics (EN) — free early access, emerald theme, 5 skills, quiz + cert | — |
| 25 | 06 May 2026 | 22:29 | Level 3 Smart Basics (TE) — Telugu translation complete | — |
| 26 | 06 May 2026 | 22:45 | Level 3 image generation script (9 DALL-E 3 scenes) | scripts/generate_level03_images.py |
| 27 | 06 May 2026 | 23:29 | Level 4 Work Smart (EN) — email, meeting summary, resume, interview, study plan | 5 skills, quiz + cert, violet theme |
| 28 | 07 May 2026 | 08:18 | Level 4 Work Smart (TE) — full Telugu translation | — |
| 29 | 07 May 2026 | 08:26 | Level 4 image generation script (8 DALL-E 3 scenes) | — |
| 30 | 07 May 2026 | 08:41 | Level 5 Life Upgrade (EN) | Home page + pitch deck updated |
| 31 | 07 May 2026 | 08:52 | Level 5 Life Upgrade (TE) | — |
| 32 | 07 May 2026 | 09:00 | Level 5 image generation script (8 DALL-E 3 scenes) | — |
| 33 | 07 May 2026 | 09:07 | Level 6 Power User (EN) | Home pages + pitch deck updated |
| 34 | 07 May 2026 | 09:34 | Level 6 Power User (TE) | — |
| 35 | 07 May 2026 | 09:53 | Level 6 image generation script (8 DALL-E 3 scenes) | — |
| 36 | 07 May 2026 | 10:16 | Level 7 Build With AI (EN) | Home pages + pitch deck updated |
| 37 | 07 May 2026 | 10:37 | Level 7 Build With AI (TE) | — |
| 38 | 07 May 2026 | 11:08 | Level 7 image generation script (7 DALL-E 3 scenes) | — |
| 39 | 07 May 2026 | 13:18 | Decision: 0 INR early access offer, chatbot + 3-site + language roadmap documented | docs/resource-tracker + full strategy update |
| 40 | 07 May 2026 | 13:31 | Decision: mitraaistudy renamed → mitraaistudent; Hindi as second priority language after Telugu | — |
| 41 | 07 May 2026 | 13:35 | Mitra chatbot widget created + Cloudflare Worker proxy + injected into all 17 pages | mitra-chat.js |
| 42 | 07 May 2026 | 14:53 | Chatbot connected to live Cloudflare Worker endpoint | — |
| 43 | 07 May 2026 | 15:03 | Supabase progress restore — ladder row highlights + resume bar on home page | — |
| 44 | 07 May 2026 | 15:15 | Level 1 intro video (90s narrated slideshow) generated + embedded on L1 page | S3: videos/level-01-intro.mp4 |
| 45 | 07 May 2026 | 16:09 | Level 8 AI for Small Business (EN + TE) + 8 images on S3 | Home page updated |
| 46 | 07 May 2026 | 16:49 | Level 9 AI for Income (EN + TE) + images | Cloudflare Worker updated for L8 + L9 |
| 47 | 07 May 2026 | 17:25 | Level 10 AI Safety & Society (EN + TE) + 8 images | Home pages, auth, docs, Cloudflare Worker |
| 48 | 07 May 2026 | 17:36 | Level 1 Telugu video script written | — |
| 49 | 07 May 2026 | 17:42 | Level 1 Telugu narrated video generated and uploaded to S3 | Embedded in level-01-comic-te.html |
| 50 | 07 May 2026 | 18:33 | Decision: design themes documented — mitraaistudent multi-colour kids, mitraaiprojects 2-colour dark | — |
| 51 | 07 May 2026 | 18:38 | Level 2 EN intro video generated (~144s) + uploaded to S3 + embedded | — |
| 52 | 07 May 2026 | 18:49 | Level 3 EN intro video generated (~128s) + uploaded to S3 + embedded | — |
| 53 | 07 May 2026 | 18:56 | Level 4 EN intro video generated (~129s) + uploaded to S3 + embedded | — |
| 54 | 07 May 2026 | 19:03 | Level 5 EN intro video generated (~136s) + uploaded to S3 + embedded | — |
| 55 | 07 May 2026 | 19:09 | Level 6 EN intro video generated (~148s) + uploaded to S3 + embedded | — |
| 56 | 07 May 2026 | 20:33 | Level 7 EN intro video generated (~112s) + uploaded to S3 + embedded | — |
| 57 | 07 May 2026 | 20:44 | Level 8 EN intro video generated (~126s) + uploaded to S3 + embedded | — |
| 58 | 07 May 2026 | 21:09 | Level 9 EN intro video generated (~129s) + uploaded to S3 + embedded | — |
| 59 | 07 May 2026 | 22:43 | Level 10 EN video + unified platform plan docs | docs/mitraailife-unified-platform-plan.md etc. |
| 60 | 07 May 2026 | 23:09 | Unified home nav + track pages created | daily-life, students, tuition, spoken-english, projects, small-business, teachers, contact |
| 61 | 07 May 2026 | 23:16 | SEO basics added to all track pages | meta descriptions, canonical links |
| 62 | 07 May 2026 | 23:26 | Mobile layout tightened for all unified pages | — |
| 63 | 07 May 2026 | 23:30 | Branded 404 page added | — |
| 64 | 07 May 2026 | 23:37 | Contact enquiry page improved | Pre-filled mailto links per enquiry type |
| 65 | 07 May 2026 | 23:41 | README updated for unified platform status | — |
| 66 | 07 May 2026 | 23:45 | GitHub Pages deployment checklist added to docs | — |
| 67 | 07 May 2026 | 23:51 | Track page copy patterns aligned across all pages | — |
| 68 | 07 May 2026 | 23:57 | Social metadata (OG + Twitter cards) added to all track pages | — |
| 69 | 08 May 2026 | 00:01 | Telugu video production checklist documented | — |
| 70 | 08 May 2026 | 00:12 | Level 1 Telugu video narration tuned and re-uploaded | — |
| 71 | 08 May 2026 | 00:28 | Legal pages added — Privacy Policy + Payment & Refund Policy + footer links | — |
| 72 | 08 May 2026 | 00:35 | QA script created (site_qa.js) + FAQ sections + JSON-LD structured data on all pages | scripts/site_qa.js |
| 73 | 08 May 2026 | 00:40 | Contact page upgraded — per-track prefilled mailto links for 6 enquiry types | — |
| 74 | 08 May 2026 | 00:48 | Per-track OG images generated (11 PNGs) + extended QA + mobile tap targets (44px) | scripts/generate_og_images.py |
| 75 | 08 May 2026 | 08:37 | Company logo designed: AI oval, 7 VIBGYOR dots, black cluster — 7 variants generated | scripts/generate_logo_variants.py |
| 76 | 08 May 2026 | 08:37 | Decision: Logo option 6 (no lines) selected as official Mitra AI Life logo | site/mitra-ai-logo.svg |
| 77 | 08 May 2026 | 08:37 | VIBGYOR colours applied to nav track buttons (violet → red) | site/track-page.css |
| 78 | 08 May 2026 | 08:37 | Favicon + app icons generated from logo (16/32/180/192/512px + .ico) | scripts/generate_favicons.py |
| 79 | 08 May 2026 | 08:37 | Favicon tags injected into all 14 HTML pages | scripts/inject_favicon_tags.py |
| 80 | 08 May 2026 | 08:37 | site.webmanifest created for PWA home screen icon | — |
| 81 | 08 May 2026 | 08:58 | Decision: all early-access levels made FREE (₹0) during launch period | Original prices struck through in green on home pages |
| 82 | 08 May 2026 | 08:58 | Language switcher added to: Home, Daily Life, Contact, Spoken English, Small Business, Teachers | NOT on Students, Tuition, Projects |
| 83 | 08 May 2026 | 08:58 | Decision: single URL strategy — all tracks under mitraailife.com | Separate sub-sites (mitraaistudent, mitraaiprojects) deferred |
| 84 | 08 May 2026 | 08:58 | Telugu Contact page created (contact-te.html) — full translation with enquiry paths | — |
| 85 | 08 May 2026 | 08:58 | Contact form added to contact.html and contact-te.html using Formspree | Hides Gmail address; form delivers to inbox. Needs Formspree ID setup. |

---

## Pending / Next items

_Updated 08 May 2026 — items P1–P5, P7 DONE. Items below are active._

| # | Item | Priority | Notes |
|---|------|----------|-------|
| P8 | Verify L8–L10 DALL-E 3 images uploaded to S3 (`scenes/img-l8/9/10-*`) | Medium | Run `aws s3 ls s3://mitra-ai-life-assets/scenes/ \| grep img-l8` |
| P9 | Hindi as third language — planning only, no build yet | Low | Deferred |
| P10 | Disqus comments on Levels 3–10 (currently only L1 and L2 have it) | Low | — |
| P11 | WhatsApp channel or support number — add to contact page when ready | Low | — |
| P12 | Payment gateway integration for paid levels when early access ends | Future | — |
| P13 | Company registration | Future | Wait for real traction |
| P14 | Bigger / more colorful nav track buttons on lesson pages (VIBGYOR style) | Medium | User showed reference image — more prominent CTAs needed |
| P15 | AI for Students track — content plan + Level 1 lesson | Medium | School-safe AI literacy, Class 8–12, CBSE/SSC patterns |
| P16 | index.html hero video — replace placeholder with real Mitra intro video | Medium | Placeholder already in place |
| P17 | Track page videos — generate + embed for each service page | Medium | All 7 track pages have "VIDEO COMING SOON" placeholder |
| P18 | Consider moving GitHub repo from personal → org account | Low | Steps documented in task log; do when org is ready |
| P19 | index-te.html — Telugu home page full content review | Medium | Partial — verify all sections translated |
| 86 | Jun 2025 | — | Telugu intro videos L1–L10 confirmed generated + uploaded to S3 (15–28 MB each) | content/assets/videos/level-NN-intro-te.mp4 |
| 87 | Jun 2025 | — | Video player size fixed to width:90%; max-width:1280px on all 21 lesson pages (EN + TE) | scripts/batch_embed_te_videos.py |
| 88 | Jun 2025 | — | Home + Language button color fixed (navy #1e3a5f) on all 10 EN lesson pages — was invisible white | content/english/**/level-NN-comic.html |
| 89 | Jun 2025 | — | Video placeholders added to all 7 track pages + index.html landing page | site/daily-life.html, students.html, tuition.html, spoken-english.html, projects.html, small-business.html, teachers.html, index.html |
| 90 | Jun 2025 | — | Telugu track pages created: daily-life-te.html, spoken-english-te.html, small-business-te.html, teachers-te.html | site/ |
| 91 | Jun 2025 | — | L2–L10 Telugu video sections embedded on all TE lesson pages (S3 URLs) | scripts/batch_embed_te_videos.py |
| 92 | Jun 2025 | — | Lang switchers updated on EN track pages: daily-life, spoken-english, small-business, teachers → now point to TE pages | site/ |
| 93 | Jun 2025 | — | accounts.md created (local only, gitignored) — full service inventory | accounts.md |
| 94 | 08 May 2026 | 15:00 | Telugu TTS scripts updated to SSML — AI pronunciation fixed (Ay + Eye) across all 10 levels | Patch script: scripts/patch_te_scripts_ai_ssml.py; `<say-as interpret-as="characters">AI</say-as>` replaces plain text in all L1–L10 scripts |
| 95 | 08 May 2026 | 15:18 | All 10 Telugu intro videos regenerated with SSML-fixed audio and re-uploaded to S3 | L1–L10 complete; commit 7d43212; S3: s3://mitra-ai-life-assets/videos/level-NN-intro-te.mp4 |
| 96 | 08 May 2026 | — | students.html fully redesigned — class grid (Class 6–12), hero, safety strip, video placeholder, bands, chatbot section, notebooks strip, parents note, FAQ, bottom CTA | commit 6b777ca |
| 97 | 08 May 2026 | — | Class 6 lesson page created — content/students/class-06/class-06.html — 5 sections, quiz, worksheet, parent/teacher note | Anu story, Indian examples, safety rules, 5-question quiz with JS scoring |
| 98 | 08 May 2026 | — | Renamed Class 11 → Junior College +1, Class 12 → Junior College +2 across students.html — 14 instances total; new FAQ added explaining +1/+2 mapping to Inter/PUC/CBSE | commit c9fdb34 |
| 99 | 08 May 2026 | — | Class 6 DALL-E 3 images generated (3 scenes) + uploaded to S3 + embedded in class-06.html; class-06 intro video generated (111s) + uploaded to S3 + embedded | commit 28c180a |
| 100 | 08 May 2026 | — | index.html Students card updated to "Live · Class 6 Free"; mitraaistudent-master-plan.md updated for JC +1/+2 naming | commit 28c180a |
| 101 | 08 May 2026 | — | Class 7 lesson page created — content/students/class-07/class-07.html — 5 sections (prompting, formula, study use, weak answers, honesty), quiz, worksheet, parent note; Class 7 card on students.html now live + linked | commit 3244757 |
| 102 | 08 May 2026 | — | class-06.html: fixed video black box (position:absolute on video element inside .video-box); lesson labelled Lesson 1 of 12; duration updated 30-45min → 60-90min | commit a623a2b |
| 103 | 08 May 2026 | — | class-06.html: added Full Year Curriculum Map (12 lessons, 1 active + 11 coming soon); added Section 6 (How AI Learns — training data, supervised learning), Section 7 (Types of AI Tools — table with 6 types), Section 8 (AI in India — 6 real examples: Plantix, Aravind Eye, IRCTC, DIKSHA, Bhashini, IMD) | commit a623a2b |
| 104 | 08 May 2026 | — | class-06.html: expanded quiz from 5 to 10 questions (Q6–Q10 cover AI learning, recommendation AI, Plantix, factual error handling, AI vs calculator); updated JS correct answers, feedback text, score messages | commit a623a2b |
| 105 | 08 May 2026 | — | "Suggest a Topic" tile added: full Formspree form on students.html (before bottom CTA); mailto-based tile on teachers.html, projects.html, small-business.html — each page-specific subject line and body template | commit a623a2b |
| 106 | 08 May 2026 | — | Class 6 Lesson 2 built — lesson-02.html: 8 sections (YouTube rabbit hole, Google Search personalisation, Maps traffic AI, face unlock biometrics, autocorrect/predictive text, weather AI/IMD/INSAT, filter bubbles, 5 smart-user habits), 10Q quiz, AI Spy Day worksheet, parent/teacher note; class-06.html curriculum map L2 card → Live + linked | commit 4c78109 |
| 107 | 08 May 2026 | — | Class 6 Lesson 3 built — lesson-03.html: 8 sections (ML vs memorisation, training data, data annotation, pattern finding, test set/accuracy, biased data/overfitting, Sort Shapes hands-on activity, training-to-deployment pipeline), 10Q quiz, worksheet, parent note; class-06.html L3 card → Live | commit 4e6b5b4 |
| 108 | 08 May 2026 | — | Class 6 Lesson 4 built — lesson-04.html: 8 sections (6 tool families overview, Language/Chatbot AI + hallucinations, Image AI + deepfakes, Voice AI + India languages, Recommendation AI deeper dive, Computer Vision AI, Prediction/Forecasting AI, which tool for which task), 10Q quiz, AI Tool Matcher worksheet, parent note; class-06.html L4 card → Live | commit 2ba6719 |
| 109 | 08 May 2026 | — | docs/curriculum-qa-index.md created — full hierarchy: AI for Students → Class 6 → Lessons 1–4, each with section topics and full 10Q quiz Q&A table (correct answers marked); Lessons 5–12 and Classes 7–JC+2 listed as planned | — |
| 110 | 08 May 2026 | — | Class 6 Lesson 5 built — lesson-05.html: 8 sections (8 case studies: Plantix, Aravind Eye Care, DIKSHA, Bhashini, Indian Railways/AskDISHA, Qure.ai TB detection, UPI fraud detection, AI access map + Digital Divide), 10Q quiz, India AI Reporter worksheet, parent note; class-06.html L5 card → Live | commit ff7438a |
| 111 | 08 May 2026 | — | Class 6 Lesson 6 built — lesson-06.html: 8 sections (What is a prompt, CTFX formula, weak vs strong prompts, study help patterns, creative prompting, Telugu/Hindi/Tamil prompts, follow-up prompts, ethical prompting), 10Q quiz, Prompt Improver worksheet, parent note; class-06.html L6 card → Live; curriculum-qa-index.md updated with L5 + L6 full Q&A tables | commit 8de73c5 |
| 112 | 08 May 2026 | — | Class 6 Lesson 7 built — lesson-07.html: 8 sections (AI as study partner, concept explanation + teach-it-back, practice tests, notes + mnemonics, maths word problems, writing improvement, oral exam prep, 3-day study plan), 10Q quiz, AI Study Session Planner worksheet, parent+teacher note; class-06.html L7 card → Live; curriculum-qa-index.md updated with L7 Q&A | commit d2d69bc |
| 113 | 08 May 2026 | — | Class 6 Lesson 8 built — lesson-08.html: 8 sections (digital citizen qualities, digital footprint timeline, privacy/personal info safety, cyberbullying 5-step plan + Indian helplines, fake news 5-step check + Boom Live/Alt News/deepfakes, screen time balance, AI ethics scenarios, positive pledge), 10Q quiz, Digital Citizenship Audit worksheet, parent note; class-06.html L8 card → Live; curriculum-qa-index.md updated with L8 Q&A | commit 3249952 |
| 114 | 09 May 2026 | — | Class 6 Lesson 9 built — lesson-09.html: 8 sections (can machines be creative, AI for writing/storytelling, AI for poetry/lyrics, AI for art/visual ideas, AI for comics/scripts, AI for music/sound, AI as collaborator, creativity rules + copyright), 10Q quiz, AI Creative Project worksheet, parent note; class-06.html L9 card → Live; curriculum-qa-index.md updated with L9 Q&A | commit ea19035 |
| 117 | 10 May 2026 | — | Class 6 Lesson 12 built — lesson-12.html: 8 sections (year recap grid, journal habits, biggest AI moments prompts, 10 summer experiments, open questions, personal pledge, year summary template, Class 7 preview), final 10Q quiz covering all 12 lessons, year summary worksheet, parent note; class-06.html L12 card → Live; curriculum-qa-index.md updated with L12 Q&A — all 12 lessons complete | commit 75ac4ba |
| 116 | 10 May 2026 | — | Class 6 Lesson 11 built — lesson-11.html: 8 sections (jobs changing not disappearing, AI jobs in India, jobs AI helps, India AI industry cities/companies, skills that always matter, Class 6 preparation roadmap, Indian role models, career path routes), 10Q quiz, career interview worksheet, parent note; class-06.html L11 card → Live; curriculum-qa-index.md updated with L11 Q&A | commit 2a5d9fc |
| 115 | 09 May 2026 | — | Class 6 Lesson 10 built — lesson-10.html: 8 sections (hallucinations + confident errors, 6 types of AI mistakes, why AI hallucinates, AI and maths, AI bias and fairness, knowledge cutoffs, 5-step fact-check process, critical AI habits + red flags), 10Q quiz, AI Fact-Check Challenge worksheet, parent note; class-06.html L10 card → Live; curriculum-qa-index.md updated with L10 Q&A | commit b0c3bae |
| 118 | 11 May 2026 | — | Class 7 hub conversion — class-07.html upgraded from single lesson to 12-card hub: added curriculum map CSS (purple theme), "Lesson 1 of 12" eyebrow badge, hero image, 12-card lesson grid (L1 active + L2 live-linked + L3–L12 coming soon), bottom nav → lesson-02.html; Class 6 visual pass all 12 hero images live on S3 | — |
| 119 | 11 May 2026 | — | Class 7 Lesson 2 built — lesson-02.html: 8 sections (subject-by-subject approach, Science prompts, Maths concept-not-answer rule, English plan-practise-polish, History/SST timelines, Geography causes/connections, regional language cautions, 6-step weekly study routine), 10Q quiz, subject prompt worksheet, parent note; class-07.html L2 card → Live; curriculum-qa-index.md updated with Class 7 L1 + L2 Q&A | commit ecad089 |
| 120 | 11 May 2026 | — | docs/pending_actions.md created — tracks Class 7 hero image generation (generate_class07_images.py + upload_class07_images.sh created and ready to run) and Class 7 video generation pending user action | — |
| 127 | 8 May 2026 | — | Class 7 Lesson 9 built — lesson-09.html: 8 sections (India school scale stats strip — 1.5M+ schools/260M+ students, key government initiatives grid: NEP 2020/PM eVIDYA/DIKSHA/CBSE AI elective/NITI Aayog AI for All/Atal Tinkering Labs, AI tools already in Indian school life: BYJU'S/Grammarly/Photomath/Google Translate/ChatGPT, timeline 2009–2026 of AI education milestones, challenges vs opportunities two-column grid: connectivity/language/device/teacher-training gaps vs mobile-first/multilingual-AI/DIKSHA/great-equaliser, how AI changes teacher and student roles, future Indian classroom in 5–10 years, action table for every device-access scenario), 10Q quiz, My School's AI Situation worksheet, parent note; class-07.html L9 card → Live; curriculum-qa-index.md updated | — |
| 126 | 8 May 2026 | — | Class 7 Lesson 8 built — lesson-08.html: 8 sections (how AI image generators work + what they are/not good at, 4-ingredient image prompt formula: subject/setting/style/mood, compare weak vs strong prompt, iteration + refinement prompts, correct vs incorrect use in school projects + dos-and-donts, copyright and honesty rules + never-generate list, AI creative tools beyond images: Canva AI / Adobe Firefly / Suno, AI and human creativity as partners not rivals + creative exploration prompt, summary table), 10Q quiz, AI Image Prompt Lab worksheet, parent note; class-07.html L8 card → Live; curriculum-qa-index.md updated | — |
| 125 | 8 May 2026 | — | Class 7 Lesson 7 built — lesson-07.html: 8 sections (how AI works in simple terms, 4 error types grid: hallucination/outdated/bias/overconfident, hallucination detail + check prompt, outdated information + currency prompt, bias + Indian perspective prompt, overconfidence red-flag signals + confidence-level prompt, 5 everyday protection habits, AI error spotter quick-reference table), 10Q quiz, AI error spotter log worksheet, parent note; class-07.html L7 card → Live; curriculum-qa-index.md updated | — |
| 124 | 8 May 2026 | — | Class 7 Lesson 6 built — lesson-06.html: 8 sections (AI as starting point rule, topic overview + gap-identification prompts, source trust grid high/medium/low, 3-pass reading method + difficult-word prompt, cross-checking 5-step workflow, writing in own words + outline prompt, citing sources including AI, full 6-step research workflow table), 10Q quiz, research project tracker worksheet, parent note; class-07.html L6 card → Live; curriculum-qa-index.md updated | — |
| 123 | 8 May 2026 | — | Class 7 Lesson 5 built — lesson-05.html: 8 sections (one rule for AI + Maths, fractions/decimals concept-first prompts, algebra balancing concept + check-my-working prompt, geometry visualising + formula-why prompt, word problem 4-step breakdown, ratio/proportion/percentage topic grid + real-life prompt, simpler-explanation + practice-problems prompts, daily Maths practice 6-step habit table), 10Q quiz, Maths problem log worksheet, parent note; class-07.html L5 card → Live; curriculum-qa-index.md updated | — |
| 122 | 8 May 2026 | — | Class 7 Lesson 4 built — lesson-04.html: 8 sections (AI as partner vs ghostwriter comparison table, story brainstorming + character building + plot structure prompts, poem rhyme helper + haiku, essay 4-stage planning process with stage cards, feedback using explain-don't-fix rule, academic honesty rules box + simple test, finding your own voice + voice check prompt, 5-day creative writing sprint table), 10Q quiz, story planning worksheet, parent note; class-07.html L4 card → Live; curriculum-qa-index.md updated | — |
| 121 | 11 May 2026 | — | Class 7 Lesson 3 built — lesson-03.html: 8 sections (5-part revision kit overview, AI chapter summary + key terms, flashcard set with NCERT example, self-quiz generation, exam-style practice questions, revision timetable, spaced repetition D1/D2/D5/D10 method, revision kit organisation + teach-it-back), 10Q quiz, Build One Chapter's Kit worksheet, parent note; class-07.html L3 card → Live; curriculum-qa-index.md updated | — |
