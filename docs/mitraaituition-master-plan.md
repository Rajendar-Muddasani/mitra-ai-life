# mitraaituition.com — AI Hindi Tuition Master Plan

> Purpose of this document: Use this as the starting blueprint for a new AI-assisted tuition platform focused first on elementary Hindi recovery learning for school children in India.

---

## 1. Genuine Product Call

This idea is strong, but it should start narrow.

The best first version is not "all subjects, Grade 1 to 10". That is too large, needs board-wise accuracy, and will slow launch. The strongest first product is:

**Elementary Hindi Catch-Up Tuition for children who missed basics.**

| Question | Answer |
|---|---|
| Does the idea work? | Yes, if it starts with elementary Hindi foundations instead of all Grade 1-10 subjects. |
| Why it can work | Many Indian children move schools, miss classes, change boards, or fall behind in Hindi basics. Parents need gentle recovery learning. |
| First learner | Grade 2-6 child who cannot confidently read, pronounce, write, or understand basic Hindi. |
| First buyer | Parent who wants low-pressure home practice before or alongside school tuition. |
| Core promise | Colorful Hindi basics explained slowly with voice, repetition, writing practice, and small quizzes. |
| Best launch scope | Hindi letters, matras/barakhadi, numbers, words, simple sentences, reading, dictation, and beginner writing. |
| Risk | Must not claim guaranteed school marks. Must align content carefully with class level and have human review. |

The emotional reason is also strong: this is for children who are not weak, but who missed learning at the right time. The product tone should never shame the child. It should feel like, "No problem, we will rebuild slowly."

---

## 2. Platform Positioning

**mitraaituition.com** is a child-friendly online AI tuition platform under the Mitra AI family.

| Property | Value |
|---|---|
| Target audience | Indian school children, first focus Grade 2-6 Hindi catch-up |
| Parent segment | Parents whose child missed school, changed medium, changed board, or lacks Hindi confidence |
| Core promise | Rebuild Hindi basics through colorful videos, repeated pronunciation, writing practice, and quizzes |
| Language of instruction | English + simple Hindi first; Telugu/English parent guidance later if needed |
| Content style | Very visual, slow, repetitive, encouraging, worksheet-friendly |
| First product | Elementary Hindi Foundation Track |
| Future expansion | Grade-wise Hindi, English reading, Telugu, math basics, full AI tuition assistant |
| Pricing direction | Freemium: free alphabet lessons, paid structured practice packs |
| Status | Planning only. New workspace and repo needed. |

Relationship to mitraailife.com:
- Same founder and Mitra brand family.
- Separate domain and repo because the audience is children and parents.
- Shared infrastructure can be reused, but child safety and privacy rules must be stricter.
- This is not the same as mitraaistudent.com. Student AI literacy teaches students about AI; this platform teaches school subjects using AI-assisted content.

---

## 3. First MVP Recommendation

Build only **Hindi Foundation Level 0 + Level 1** first.

### MVP Name

**Hindi Catch-Up: Start From Zero**

### MVP Learner Outcome

After the MVP, a child should be able to:
- recognize basic Hindi vowels and consonants
- pronounce letters slowly and clearly
- identify matras in simple words
- read beginner words
- write letters on paper after watching stroke guidance
- answer small sound and letter quizzes

### MVP Lessons

| Lesson | Topic | Video Style | Practice |
|---|---|---|---|
| H0-01 | What is Hindi? Why do we learn it? | Friendly story, no pressure | Listen and repeat |
| H1-01 | Swar: अ to अः | Letter appears large, voice repeats 3 times | Trace on paper |
| H1-02 | Vyanjan Part 1: क to ञ | Letter + object + sound | Match sound to letter |
| H1-03 | Vyanjan Part 2: ट to न | Slow pronunciation | Choose correct letter |
| H1-04 | Vyanjan Part 3: प to ह | Practice with examples | Write 5 letters |
| H1-05 | Barakhadi concept | क + matras visually animated | Fill missing matra |
| H1-06 | Simple words | घर, कमल, फल type words | Read aloud + select picture |
| H1-07 | Numbers 1-20 | Number, Hindi word, pronunciation | Match number to word |
| H1-08 | First reading quiz | Tiny reading game | Parent-assisted review |

Do not start with grammar, essay writing, or unseen passage. Those come after reading confidence.

---

## 4. Curriculum Ladder

### Track A: Hindi Foundation

| Level | Name | Child Skill |
|---|---|---|
| H0 | Confidence Reset | Child feels safe, not ashamed |
| H1 | Letters and Sounds | Recognize and pronounce letters |
| H2 | Matras and Barakhadi | Read syllables and small words |
| H3 | Words and Meanings | Build vocabulary with pictures |
| H4 | Simple Sentences | Read and write short sentences |
| H5 | Listening and Dictation | Hear sound/word and write/select |

### Track B: School Hindi Basics

| Level | Name | Child Skill |
|---|---|---|
| H6 | Grammar Basics | Sangya, sarvanam, kriya, ling, vachan |
| H7 | Paragraph Reading | Read small passages and answer questions |
| H8 | Picture Writing | Describe a picture creatively in 5-8 lines |
| H9 | Letter Writing | Informal/formal beginner letters |
| H10 | Essay Writing | Simple essays: my school, festival, my family |

### Track C: Grade-Wise Expansion Later

After the foundation track works, create board-aware packs:
- Grade 1 Hindi basics
- Grade 2 Hindi basics
- Grade 3 Hindi reading and writing
- Grade 4 grammar and paragraph writing
- Grade 5 unseen passage and composition
- Grade 6-8 grammar, comprehension, writing
- Grade 9-10 board-focused writing and exam prep

This should not be built first because every board and textbook differs.

---

## 5. Lesson Format

Each lesson should follow the same pattern.

| Part | Description |
|---|---|
| 1. Watch | 2-4 minute colorful video with slow pronunciation |
| 2. Repeat | Letter or word repeated 3 times with mouth-position hint |
| 3. Trace | Child writes on paper while video pauses |
| 4. Listen | Audio says a sound or word |
| 5. Choose | Child selects from 3-4 options |
| 6. Write | Child writes in notebook; parent can mark done |
| 7. Tiny Win | Sticker/star/reward message |

### Video Style

- large letters on screen
- bright background, but not visually noisy
- one concept per screen
- pronunciation repeated slowly
- examples from Indian home and school life
- child-friendly voice, not robotic
- never say "wrong" harshly; say "try again"

### Quiz Types

- hear sound, choose letter
- see letter, choose sound
- see picture, choose word
- missing matra dropdown
- word ordering into sentence
- read passage, choose answer
- picture prompt, child writes in notebook

---

## 6. Technology Plan

Reuse the Mitra stack, but add child-safe rules.

### Hosting

| Item | Recommendation |
|---|---|
| Domain | mitraaituition.com |
| GitHub repo | `mitra-ai-tuition` |
| Hosting | GitHub Pages initially |
| Media storage | S3 folder `tuition/` inside existing bucket |
| Analytics | Same GA4 initially, but separate event names |
| Auth | Parent login first, child profile later |

### S3 Folder Layout

```text
s3://mitra-ai-life-assets/tuition/hindi-foundation/videos/
s3://mitra-ai-life-assets/tuition/hindi-foundation/scenes/
s3://mitra-ai-life-assets/tuition/hindi-foundation/audio/
s3://mitra-ai-life-assets/tuition/hindi-foundation/worksheets/
```

### AI Usage

| Use | Model/Tool |
|---|---|
| Lesson draft | GPT model with human review |
| Voice pronunciation | TTS, but manually checked by Hindi speaker |
| Images | DALL-E 3 or reusable illustrated assets |
| Quizzes | Generated from lesson manifest, reviewed |
| Parent assistant | Strict child-safe chatbot later |

Important: pronunciation must be reviewed. Hindi learning fails if sound is unclear.

---

## 7. Pricing Model

Start free enough for trust, then charge for structured practice.

| Product | Price Idea |
|---|---|
| Free starter | H0 + first 2 alphabet lessons free |
| Hindi Foundation Pack | ₹299-₹499 one-time early access |
| Monthly practice | ₹99-₹199/month later |
| Parent worksheet bundle | ₹99 download pack |
| Personal review | Optional paid add-on later |

Do not make it expensive at first. Parents must first trust quality.

---

## 8. Legal, Safety, and Ethics

This platform is for children, so safety is more important than speed.

Required rules:
- parent account, not direct child account, in the first version
- no public comments on child lesson pages
- no Disqus for children-facing pages
- no collection of child photos, voice, school name, or location in MVP
- no claim of guaranteed marks
- no medical or psychological claims
- human review before publishing every lesson
- parent guidance page: this is practice support, not a school replacement

If interactive voice recording is added later, get explicit parent consent and store minimal data.

---

## 9. Build Phases

### Phase 1: Proof of Need

Timeline: 1-2 weeks

Deliverables:
- landing page
- 3 sample Hindi videos
- printable worksheet PDF
- parent feedback form
- WhatsApp sharing flow

Success signal:
- 20 parents try sample lessons
- 10 children complete at least 2 lessons
- parents say pronunciation and pacing helped

### Phase 2: Hindi Foundation MVP

Timeline: 3-5 weeks

Deliverables:
- H0-H1 lessons
- quizzes and worksheet downloads
- progress tracking
- parent dashboard basics

Success signal:
- 50 children complete H1
- parents request next level
- children can identify letters more confidently

### Phase 3: Barakhadi and Words

Timeline: 4-6 weeks

Deliverables:
- H2-H3 videos
- listen-and-select quizzes
- writing practice sheets
- simple reading challenges

### Phase 4: Writing and Comprehension

Timeline: 6-8 weeks

Deliverables:
- sentence writing
- picture writing
- unseen passage basics
- letter writing
- essay writing starter packs

---

## 10. Next Concrete Step

Before buying/building too much, create a **Hindi Foundation Sample Pack**:

1. Lesson 1: अ, आ, इ, ई
2. Lesson 2: क, ख, ग, घ
3. Lesson 3: क + matras intro
4. One printable worksheet
5. One 10-question quiz
6. One parent feedback form

If this sample helps even 10 real children, the platform is worth building.
