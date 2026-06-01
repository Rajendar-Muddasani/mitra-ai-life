#!/usr/bin/env python3
"""
Generate overview videos for Class 7 Lessons 02–12.
Usage:
    python3 scripts/generate_class07_lessons_02_12.py          # all lessons
    python3 scripts/generate_class07_lessons_02_12.py 02 03    # specific lessons
"""

from __future__ import annotations
import os, sys, subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips
from google.cloud import texttospeech

# ── env ──────────────────────────────────────────────────────────────────────
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

os.environ["IMAGEIO_FFMPEG_EXE"] = imageio_ffmpeg.get_ffmpeg_exe()

ROOT = Path(__file__).resolve().parent.parent
ASSET_DIR = ROOT / "content" / "assets" / "students" / "class-07"
HTML_DIR  = ROOT / "content" / "students" / "class-07"
S3_BUCKET = "mitra-ai-life-assets"
S3_PREFIX = "students/class-07"
VIDEO_W, VIDEO_H, FPS = 1280, 720, 24
TTS_LANG  = "en-US"
TTS_VOICE = "en-US-Chirp3-HD-Charon"
TTS_RATE  = 1.0
BADGE_COL = (109, 40, 217)   # purple #6d28d9

try:
    FONT_TITLE  = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 52)
    FONT_BODY   = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 28)
    FONT_BADGE  = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
    FONT_FOOTER = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
except OSError:
    FONT_TITLE = FONT_BODY = FONT_BADGE = FONT_FOOTER = ImageFont.load_default()

LESSONS: dict[str, dict] = {
    "02": {
        "badge": "CLASS 7 · LESSON 2",
        "title": "AI for Every Subject",
        "image": "lesson-02-hero.jpg",
        "scenes": [
            {
                "title": "AI can help with every subject",
                "bullets": [
                    "Different subjects need different AI prompts",
                    "AI explains, gives examples, and connects ideas",
                    "You still do the thinking — AI is your study partner",
                ],
                "text": (
                    "Welcome to Class 7 Lesson 2 — AI for Every Subject. "
                    "AI is not just for one type of question. "
                    "It can help with science, maths, English, history, and languages. "
                    "The key is knowing which prompt to use for each subject."
                ),
            },
            {
                "title": "AI for Science — Explain, Example, Connect",
                "bullets": [
                    "Ask AI to explain a concept in simple words",
                    "Ask for a real-world Indian example of the concept",
                    "Ask how it connects to something you already know",
                ],
                "text": (
                    "For science, use three steps. "
                    "First, ask AI to explain the concept simply. "
                    "Second, ask for a real-world Indian example — like photosynthesis in a paddy field. "
                    "Third, ask how it connects to something you already know."
                ),
            },
            {
                "title": "AI for Maths — Understand, Not Answer",
                "bullets": [
                    "Never ask AI for the final answer",
                    "Ask AI to explain the method step by step",
                    "Then solve it yourself — check after, not before",
                ],
                "text": (
                    "For maths, the golden rule is never ask AI for the answer. "
                    "Ask it to explain the method step by step. "
                    "Then solve the problem yourself. "
                    "Only check after you have tried — this builds real understanding."
                ),
            },
            {
                "title": "AI for English, History, and Languages",
                "bullets": [
                    "English: use AI to plan, practise, and polish writing",
                    "History: ask for timelines, causes, and effects",
                    "Languages: ask AI to correct your sentences with explanation",
                ],
                "text": (
                    "For English, use AI to plan essays and get feedback on your writing. "
                    "For history, ask for timelines, causes, and effects in simple language. "
                    "For Hindi, Telugu, or any regional language, ask AI to correct your sentences "
                    "and explain why the correction was made."
                ),
            },
            {
                "title": "Build your weekly AI study routine",
                "bullets": [
                    "Pick one AI prompt per subject each week",
                    "Track which prompts helped you the most",
                    "Share your best prompt with a classmate",
                ],
                "text": (
                    "The best way to use AI for studies is to build a routine. "
                    "Pick one AI prompt per subject each week. "
                    "Write down which prompts helped you the most. "
                    "Try sharing your best prompt with a friend — teaching others is the fastest way to learn."
                ),
            },
        ],
    },
    "03": {
        "badge": "CLASS 7 · LESSON 3",
        "title": "Build Your Revision Kit",
        "image": "lesson-03-hero.jpg",
        "scenes": [
            {
                "title": "A revision kit saves exam stress",
                "bullets": [
                    "AI can summarise any chapter in minutes",
                    "Turn summaries into flashcards and self-quizzes",
                    "Build a spaced-repetition timetable with AI",
                ],
                "text": (
                    "Welcome to Class 7 Lesson 3 — Build Your Own Revision Kit. "
                    "AI can help you prepare for exams far more efficiently. "
                    "You can summarise chapters, make flashcards, generate practice questions, "
                    "and build a revision timetable — all with the right prompts."
                ),
            },
            {
                "title": "Step 1 — AI chapter summary",
                "bullets": [
                    "Paste the chapter text and ask for a 10-point summary",
                    "Ask AI to highlight the most important terms",
                    "Save the summary as your revision starting point",
                ],
                "text": (
                    "Start by asking AI to summarise the chapter in ten clear points. "
                    "Then ask it to highlight the most important terms and definitions. "
                    "Save this as the foundation of your revision kit."
                ),
            },
            {
                "title": "Steps 2 and 3 — Flashcards and self-quiz",
                "bullets": [
                    "Ask: make 10 flashcards from this summary",
                    "Ask: write 5 short-answer questions on this topic",
                    "Test yourself before looking at the answers",
                ],
                "text": (
                    "Next, ask AI to turn the summary into ten flashcards — a question on one side, "
                    "the answer on the other. "
                    "Then ask for five short-answer exam questions. "
                    "Try to answer them yourself before reading AI's answers."
                ),
            },
            {
                "title": "Steps 4 and 5 — Practice questions and timetable",
                "bullets": [
                    "Ask for exam-style 5-mark and 10-mark questions",
                    "Ask AI to build a 7-day revision timetable",
                    "Spaced repetition beats last-minute cramming every time",
                ],
                "text": (
                    "For deeper practice, ask AI to write exam-style five-mark and ten-mark questions. "
                    "Finally, ask AI to build a seven-day revision timetable for your upcoming test. "
                    "Spacing your revision over days is far more effective than cramming the night before."
                ),
            },
            {
                "title": "Organise and use your revision kit",
                "bullets": [
                    "Keep summaries, flashcards, and quizzes in one folder",
                    "Review flashcards for 10 minutes every day",
                    "Always verify AI summaries against your textbook",
                ],
                "text": (
                    "Keep all your AI-generated materials in one organised folder. "
                    "Review your flashcards for just ten minutes every day. "
                    "And always verify AI summaries against your actual textbook — "
                    "AI can sometimes get details wrong, so a quick check keeps you accurate."
                ),
            },
        ],
    },
    "04": {
        "badge": "CLASS 7 · LESSON 4",
        "title": "AI and Creative Writing",
        "image": "lesson-04-hero.jpg",
        "scenes": [
            {
                "title": "AI is a creative partner, not the writer",
                "bullets": [
                    "AI can break the blank-page block",
                    "Use AI for ideas, planning, and feedback",
                    "Your voice and choices must drive the writing",
                ],
                "text": (
                    "Welcome to Class 7 Lesson 4 — AI and Creative Writing. "
                    "The blank page is the hardest part of writing. "
                    "AI can help you break through it — but you are still the writer. "
                    "Use AI for story ideas, planning, and feedback, not to write for you."
                ),
            },
            {
                "title": "Story brainstorming with AI",
                "bullets": [
                    "Ask: give me 5 story ideas about a child in rural India",
                    "Pick the idea that excites you most",
                    "Ask AI to suggest a beginning, middle, and end",
                ],
                "text": (
                    "To brainstorm a story, ask AI for five different ideas on a theme. "
                    "For example — give me five story ideas about a child in rural India who discovers something surprising. "
                    "Pick the one that excites you and ask AI to suggest a basic story structure."
                ),
            },
            {
                "title": "Writing poems and essays with AI",
                "bullets": [
                    "Ask AI for rhyme suggestions and rhythm patterns",
                    "Use AI to build an essay outline before you write",
                    "Write the full draft yourself — use AI for feedback after",
                ],
                "text": (
                    "For poems, ask AI for rhyme suggestions or rhythm patterns, then write your own lines. "
                    "For essays, ask AI to create an outline with three main points. "
                    "Write the full essay yourself, then ask AI to review it and suggest improvements."
                ),
            },
            {
                "title": "AI as a writing feedback tool",
                "bullets": [
                    "Paste your draft and ask: what can I improve?",
                    "Ask AI to check grammar without rewriting your style",
                    "Read every suggestion — accept only what feels right",
                ],
                "text": (
                    "After you have written a draft, paste it into AI and ask: what can I improve? "
                    "Ask it to check grammar but not change your style. "
                    "Read every suggestion carefully — you decide what to keep. "
                    "Your original voice is more valuable than perfect AI language."
                ),
            },
            {
                "title": "Honesty rules for creative writing",
                "bullets": [
                    "Always say which parts AI helped with",
                    "Never submit AI-written work as fully your own",
                    "Use AI as a springboard — your ideas must lead",
                ],
                "text": (
                    "The honesty rule is clear. "
                    "Always tell your teacher if AI helped with your work. "
                    "Never submit something written entirely by AI as your own. "
                    "AI is a springboard — your ideas, your voice, and your effort must lead every piece."
                ),
            },
        ],
    },
    "05": {
        "badge": "CLASS 7 · LESSON 5",
        "title": "AI and Maths: Step by Step",
        "image": "lesson-05-hero.jpg",
        "scenes": [
            {
                "title": "AI explains maths — you solve it",
                "bullets": [
                    "Never use AI to get the final answer",
                    "Use AI to understand the method and steps",
                    "Solve problems yourself after understanding the method",
                ],
                "text": (
                    "Welcome to Class 7 Lesson 5 — AI and Maths: Step by Step. "
                    "The biggest mistake students make with AI and maths is asking for the answer. "
                    "AI should explain the method — you do the solving. "
                    "Getting the answer from AI teaches you nothing."
                ),
            },
            {
                "title": "Fractions, decimals, and algebra",
                "bullets": [
                    "Ask: explain how to add fractions with different denominators",
                    "Ask: show me the steps for solving 2x + 5 = 13",
                    "Read the explanation, then solve a similar problem yourself",
                ],
                "text": (
                    "For fractions, ask AI to explain how to find a common denominator and add fractions step by step. "
                    "For algebra, ask it to show you the steps for a sample equation — not your actual homework question. "
                    "Once you understand the method, solve your own problem without AI."
                ),
            },
            {
                "title": "Geometry and word problems",
                "bullets": [
                    "Ask AI to describe shapes and their properties in simple words",
                    "For word problems, ask AI to break the question into smaller parts",
                    "Draw a diagram first — AI can help you plan what to draw",
                ],
                "text": (
                    "For geometry, ask AI to describe the properties of a shape in plain language. "
                    "For word problems, ask AI to break the question into smaller steps before you solve. "
                    "Drawing a diagram first is often the fastest path to the answer."
                ),
            },
            {
                "title": "Ratio, proportion, and percentages",
                "bullets": [
                    "Ask: give me 3 everyday Indian examples of ratio",
                    "Ask: how do I calculate percentage increase step by step?",
                    "Real examples make abstract maths concepts stick",
                ],
                "text": (
                    "For ratio and proportion, ask AI for three everyday Indian examples — "
                    "like mixing dal and rice, or sharing mangoes equally. "
                    "For percentages, ask for a step-by-step explanation of percentage increase and decrease. "
                    "Real examples make abstract concepts much easier to remember."
                ),
            },
            {
                "title": "Build a daily maths practice habit",
                "bullets": [
                    "Do at least 3 maths problems without AI every day",
                    "Use AI only to check your method, not get the answer",
                    "Track your mistakes — they show you what to revise",
                ],
                "text": (
                    "The best way to improve at maths is daily practice without AI. "
                    "Do at least three problems on your own every day. "
                    "After you finish, you can ask AI to check if your method was correct. "
                    "Track the types of mistakes you make — they are your personal revision guide."
                ),
            },
        ],
    },
    "06": {
        "badge": "CLASS 7 · LESSON 6",
        "title": "Research and Reading with AI",
        "image": "lesson-06-hero.jpg",
        "scenes": [
            {
                "title": "AI speeds up research — but verify everything",
                "bullets": [
                    "AI can find key points in any topic quickly",
                    "Always check AI facts against a textbook or trusted site",
                    "AI summaries can contain errors — your verification matters",
                ],
                "text": (
                    "Welcome to Class 7 Lesson 6 — Research and Reading with AI. "
                    "AI is a fast research assistant — but it is not always accurate. "
                    "Use it to get a quick overview of a topic, then verify the key facts "
                    "against your textbook or a trusted website like NCERT or BBC."
                ),
            },
            {
                "title": "How to research a topic with AI",
                "bullets": [
                    "Ask: give me 5 key facts about the Indian independence movement",
                    "Ask: what are the main causes of climate change? Keep it simple",
                    "Use AI output as a starting point, not your final source",
                ],
                "text": (
                    "Start research by asking AI for five key facts on your topic. "
                    "Ask it to keep the language simple and suitable for Class 7. "
                    "Treat AI's output as a starting point — not the finished answer. "
                    "Always dig deeper using your textbook or NCERT resources."
                ),
            },
            {
                "title": "Reading long texts with AI support",
                "bullets": [
                    "Paste a difficult paragraph and ask AI to explain it simply",
                    "Ask AI for the main idea of a long passage in one sentence",
                    "Ask AI to define any difficult words in context",
                ],
                "text": (
                    "If you come across a difficult passage in a textbook or newspaper, "
                    "paste it into AI and ask for a simple explanation. "
                    "Ask AI to give you the main idea in one sentence. "
                    "Ask it to define difficult words in context — this builds your vocabulary."
                ),
            },
            {
                "title": "Fact-checking AI research",
                "bullets": [
                    "Cross-check at least 2 facts from every AI response",
                    "If AI gives a date, number, or name — verify it",
                    "Trusted Indian sources: NCERT, PIB, The Hindu, BBC",
                ],
                "text": (
                    "Always fact-check at least two things from every AI response. "
                    "Dates, numbers, and names are the most likely to be wrong. "
                    "Trusted Indian sources include NCERT, the Press Information Bureau, "
                    "The Hindu, and BBC News India."
                ),
            },
            {
                "title": "Build good research habits",
                "bullets": [
                    "Use AI to get oriented on a topic — then go deeper",
                    "Keep a note of your sources alongside your research",
                    "Never copy AI output directly into your assignment",
                ],
                "text": (
                    "The best researchers use AI to get oriented on a topic quickly. "
                    "After that, they go deeper using books, articles, and primary sources. "
                    "Always keep a note of where your information came from. "
                    "And never copy AI output directly into your assignment — use your own words."
                ),
            },
        ],
    },
    "07": {
        "badge": "CLASS 7 · LESSON 7",
        "title": "Why Does AI Sometimes Get It Wrong?",
        "image": "lesson-07-hero.jpg",
        "scenes": [
            {
                "title": "AI makes mistakes — here is why",
                "bullets": [
                    "AI is trained on human-written text — it reflects our errors too",
                    "AI can confidently state incorrect facts",
                    "Understanding why AI fails makes you a smarter user",
                ],
                "text": (
                    "Welcome to Class 7 Lesson 7 — Why Does AI Sometimes Get It Wrong? "
                    "AI learns from enormous amounts of human-written text. "
                    "That means it can absorb errors, biases, and outdated information. "
                    "Understanding why AI fails makes you a far smarter and safer user."
                ),
            },
            {
                "title": "Hallucination — AI confidently making things up",
                "bullets": [
                    "AI sometimes invents facts, names, or dates that sound real",
                    "This is called hallucination",
                    "Always verify any specific claim AI makes",
                ],
                "text": (
                    "The most dangerous AI failure is called hallucination. "
                    "AI sometimes invents facts, names, book titles, or dates — "
                    "and states them with full confidence as if they are real. "
                    "This is why you must always verify any specific claim AI makes."
                ),
            },
            {
                "title": "Bias — when AI reflects unfair patterns",
                "bullets": [
                    "AI training data reflects real-world biases",
                    "AI may show unfair assumptions about gender, region, or religion",
                    "Notice patterns — do not accept them uncritically",
                ],
                "text": (
                    "AI training data reflects the biases present in human writing. "
                    "This means AI may sometimes show unfair assumptions about gender, "
                    "region, religion, or income. "
                    "Notice these patterns — and do not accept them uncritically."
                ),
            },
            {
                "title": "Outdated information",
                "bullets": [
                    "AI has a training cutoff — it does not know recent events",
                    "Always check the date when researching current events",
                    "For news and recent facts, use a live news website",
                ],
                "text": (
                    "AI has a training cutoff date — it does not know about very recent events. "
                    "If you are researching something from the last year or two, "
                    "always check a live news site like BBC or The Hindu for the latest information."
                ),
            },
            {
                "title": "How to be a careful AI user",
                "bullets": [
                    "Check: does this match what my textbook says?",
                    "Check: is this claim specific enough to verify?",
                    "Check: could this response be biased in any way?",
                ],
                "text": (
                    "Three questions make you a careful AI user. "
                    "First — does this match what my textbook says? "
                    "Second — is this specific enough that I should verify it? "
                    "Third — could this response reflect a bias I should question? "
                    "Ask these every time you use AI for school work."
                ),
            },
        ],
    },
    "08": {
        "badge": "CLASS 7 · LESSON 8",
        "title": "AI Images and Creative Tools",
        "image": "lesson-08-hero.jpg",
        "scenes": [
            {
                "title": "AI can generate images from words",
                "bullets": [
                    "Tools like DALL-E and Adobe Firefly create images from text",
                    "A detailed, specific prompt gives a much better image",
                    "AI images can be used for projects — with honest attribution",
                ],
                "text": (
                    "Welcome to Class 7 Lesson 8 — AI Images and Creative Tools. "
                    "AI image generators like DALL-E and Adobe Firefly can create a picture "
                    "from just a text description. "
                    "The key is writing a detailed, specific prompt to get a useful result."
                ),
            },
            {
                "title": "Writing good image prompts",
                "bullets": [
                    "Include subject, setting, style, and mood in your prompt",
                    "Example: a young girl reading under a banyan tree, soft watercolour style",
                    "Bad prompt: a girl reading — too vague for a good result",
                ],
                "text": (
                    "A good image prompt includes four things: subject, setting, style, and mood. "
                    "For example: a young girl reading a book under a banyan tree at sunset, "
                    "soft watercolour illustration style. "
                    "Vague prompts produce vague images — detail is everything."
                ),
            },
            {
                "title": "AI for school project visuals",
                "bullets": [
                    "Use AI images to illustrate project covers and posters",
                    "Always label AI-generated images in your project",
                    "Do not use AI images in exams or where original art is required",
                ],
                "text": (
                    "AI-generated images can make school project covers and posters look professional. "
                    "Always add a label like 'Image created with AI' in your project. "
                    "Do not use AI images in exams or wherever your teacher has asked for original artwork."
                ),
            },
            {
                "title": "Other AI creative tools",
                "bullets": [
                    "AI music tools can compose short background tracks",
                    "AI video tools can animate still images",
                    "All tools require honest labelling when submitted as work",
                ],
                "text": (
                    "Beyond images, AI music tools like Suno can compose short background tracks. "
                    "AI video tools can animate still images into short clips. "
                    "Whichever tool you use, always be honest about AI's contribution "
                    "when you submit the work."
                ),
            },
            {
                "title": "Ethics of AI-generated images",
                "bullets": [
                    "Never generate realistic fake images of real people",
                    "Never use AI images to mislead or spread false information",
                    "Creative use is welcome — harmful use is never acceptable",
                ],
                "text": (
                    "Using AI images creatively is welcome and exciting. "
                    "But never generate realistic fake images of real people — this can cause serious harm. "
                    "Never use AI images to spread false information. "
                    "Creative freedom comes with the responsibility to use it ethically."
                ),
            },
        ],
    },
    "09": {
        "badge": "CLASS 7 · LESSON 9",
        "title": "AI in Indian Schools",
        "image": "lesson-09-hero.jpg",
        "scenes": [
            {
                "title": "AI is entering Indian classrooms",
                "bullets": [
                    "Schools across India are piloting AI-assisted learning",
                    "DIKSHA, iDream, and ConveGenius reach millions of students",
                    "AI helps personalise learning for diverse needs and languages",
                ],
                "text": (
                    "Welcome to Class 7 Lesson 9 — AI in Indian Schools. "
                    "AI is already entering classrooms across India. "
                    "Platforms like DIKSHA, iDream Education, and ConveGenius reach "
                    "millions of students in multiple Indian languages. "
                    "They adapt lessons to each student's pace and level."
                ),
            },
            {
                "title": "DIKSHA and government AI in education",
                "bullets": [
                    "DIKSHA is India's national digital learning platform",
                    "It offers NCERT content in 36 languages",
                    "Teachers also use DIKSHA to access lesson plans and assessments",
                ],
                "text": (
                    "DIKSHA is India's national digital learning platform, built by the government. "
                    "It provides NCERT content in 36 Indian languages — reaching students "
                    "in rural areas who may have limited access to printed books. "
                    "Teachers use it too, for lesson plans and automated assessments."
                ),
            },
            {
                "title": "AI tutors for personalised learning",
                "bullets": [
                    "AI tutors track where each student is struggling",
                    "They adjust difficulty automatically based on your answers",
                    "This is called adaptive learning",
                ],
                "text": (
                    "AI tutors track exactly where each student is struggling. "
                    "They adjust the difficulty of questions automatically based on your answers. "
                    "This is called adaptive learning — and it means every student gets "
                    "a lesson designed specifically for them."
                ),
            },
            {
                "title": "Challenges of AI in Indian education",
                "bullets": [
                    "Not all students have reliable internet or devices",
                    "AI tools may not cover all regional languages yet",
                    "Teachers need training to use AI tools effectively",
                ],
                "text": (
                    "There are real challenges too. "
                    "Not all students have reliable internet or smartphones. "
                    "Many AI tools do not yet fully support every regional language. "
                    "And teachers need proper training to use AI tools effectively in the classroom."
                ),
            },
            {
                "title": "How you can use school AI tools well",
                "bullets": [
                    "Use digital platforms to practise at your own pace",
                    "Ask your teacher how to access DIKSHA or similar tools",
                    "Remember: AI supports your learning — it cannot replace your effort",
                ],
                "text": (
                    "If your school has access to DIKSHA or any AI learning platform, use it to "
                    "practise at your own pace and revisit topics you find difficult. "
                    "Ask your teacher how to access these tools. "
                    "And always remember — AI supports your learning, but your own effort is irreplaceable."
                ),
            },
        ],
    },
    "10": {
        "badge": "CLASS 7 · LESSON 10",
        "title": "Critical Thinking with AI",
        "image": "lesson-10-hero.jpg",
        "scenes": [
            {
                "title": "AI gives answers — you provide judgment",
                "bullets": [
                    "Critical thinking means questioning what you read",
                    "AI answers are starting points, not conclusions",
                    "Your ability to evaluate information is more valuable than AI",
                ],
                "text": (
                    "Welcome to Class 7 Lesson 10 — Critical Thinking with AI. "
                    "AI can give you fast answers, but it cannot give you judgment. "
                    "Critical thinking means not accepting information at face value — "
                    "questioning it, testing it, and deciding what to believe. "
                    "That is a skill only you can develop."
                ),
            },
            {
                "title": "The SIFT method for evaluating information",
                "bullets": [
                    "Stop — before you share or believe anything",
                    "Investigate the source — who made this claim?",
                    "Find better coverage — check multiple sources",
                ],
                "text": (
                    "A simple framework for evaluating information is called SIFT. "
                    "Stop — before you believe or share anything. "
                    "Investigate the source — who is making this claim and why? "
                    "Find better coverage — check at least two other sources before concluding."
                ),
            },
            {
                "title": "Trace claims — T in SIFT",
                "bullets": [
                    "Trace quotes and evidence back to the original source",
                    "AI often paraphrases — the original may say something different",
                    "If you cannot trace a claim, treat it with caution",
                ],
                "text": (
                    "The T in SIFT stands for Trace. "
                    "Trace quotes and statistics back to the original source. "
                    "AI often paraphrases — and the original may say something quite different. "
                    "If you cannot trace a claim back to a reliable original, treat it with caution."
                ),
            },
            {
                "title": "Spotting bias in AI responses",
                "bullets": [
                    "Notice if AI always presents one side of an argument",
                    "Ask AI to give you the counterargument too",
                    "Your own reasoning must weigh both sides",
                ],
                "text": (
                    "AI can sometimes present only one side of a topic. "
                    "If you are researching something controversial, always ask AI to give you "
                    "the strongest counterargument as well. "
                    "Then use your own reasoning to weigh both sides before forming an opinion."
                ),
            },
            {
                "title": "Critical thinking is your superpower",
                "bullets": [
                    "AI can pass any exam — but AI cannot think for itself",
                    "Your ability to question, judge, and reason is uniquely human",
                    "Practise asking 'how do I know this is true?' every single day",
                ],
                "text": (
                    "Here is the most important thing to remember. "
                    "AI can pass many exams — but AI cannot truly think for itself. "
                    "Your ability to question, judge, and reason is uniquely human. "
                    "Practise asking 'how do I know this is true?' every day — "
                    "it is the most valuable skill you will ever build."
                ),
            },
        ],
    },
    "11": {
        "badge": "CLASS 7 · LESSON 11",
        "title": "AI Safety for Teenagers",
        "image": "lesson-11-hero.jpg",
        "scenes": [
            {
                "title": "Online safety matters more with AI",
                "bullets": [
                    "AI tools collect and process your data",
                    "Some AI tools are not designed for users under 18",
                    "Understanding your rights keeps you safer online",
                ],
                "text": (
                    "Welcome to Class 7 Lesson 11 — AI Safety for Teenagers. "
                    "AI tools collect data about how you use them. "
                    "Some popular AI apps are not designed or approved for users under 18. "
                    "Understanding your digital rights and staying alert keeps you safer online."
                ),
            },
            {
                "title": "Never share personal information with AI",
                "bullets": [
                    "Do not share your name, school, address, or phone number",
                    "Do not share your parents' or friends' personal details",
                    "Treat AI chat like a public noticeboard — not a diary",
                ],
                "text": (
                    "The core safety rule is simple: never share personal information with AI. "
                    "That means no name, no school name, no address, no phone number. "
                    "Treat your AI conversations like a public noticeboard — "
                    "anything you type could be stored or seen by others."
                ),
            },
            {
                "title": "Deepfakes and manipulation",
                "bullets": [
                    "AI can generate realistic fake videos and voice clips",
                    "If someone sends you a shocking video, verify before believing",
                    "Report deepfakes targeting you or your friends to a trusted adult",
                ],
                "text": (
                    "AI can now generate convincing fake videos and voice clips called deepfakes. "
                    "If someone sends you a shocking video — especially one involving a real person — "
                    "verify it before believing or sharing it. "
                    "If you ever receive a deepfake targeting you or a friend, report it to a trusted adult immediately."
                ),
            },
            {
                "title": "AI and mental health",
                "bullets": [
                    "AI chatbots are not mental health professionals",
                    "Do not rely on AI for emotional support during a crisis",
                    "Talk to a real adult or counsellor when you need support",
                ],
                "text": (
                    "AI chatbots can seem friendly and supportive — but they are not mental health professionals. "
                    "Never rely on AI for emotional support during a crisis. "
                    "If you are struggling, talk to a real adult — a parent, teacher, or school counsellor. "
                    "Human support is irreplaceable."
                ),
            },
            {
                "title": "Your five AI safety habits",
                "bullets": [
                    "Never share personal details in AI chat",
                    "Verify any shocking content before sharing",
                    "Tell a trusted adult if something online makes you uncomfortable",
                ],
                "text": (
                    "Five AI safety habits for every teenager. "
                    "One — never share personal details in AI chat. "
                    "Two — verify shocking content before sharing. "
                    "Three — never rely on AI alone for emotional support. "
                    "Four — check app age ratings before using a new AI tool. "
                    "Five — tell a trusted adult if anything online makes you uncomfortable."
                ),
            },
        ],
    },
    "12": {
        "badge": "CLASS 7 · LESSON 12",
        "title": "My Class 7 AI Portfolio",
        "image": "lesson-12-hero.jpg",
        "scenes": [
            {
                "title": "You have completed Class 7!",
                "bullets": [
                    "11 lessons, 11 skills — all about using AI wisely",
                    "From subject prompts to safety habits to critical thinking",
                    "Today you build your personal AI portfolio",
                ],
                "text": (
                    "Welcome to Class 7 Lesson 12 — your capstone and portfolio. "
                    "Over eleven lessons you have built a serious set of AI skills. "
                    "You learned subject-specific prompts, revision techniques, creative tools, "
                    "research habits, critical thinking, and safety practices. "
                    "Today you bring it all together."
                ),
            },
            {
                "title": "Your Class 7 AI skills — the big 5",
                "bullets": [
                    "Subject AI: use the right prompt for each subject",
                    "Revision AI: summaries, flashcards, practice questions",
                    "Research AI: fast overview then verify everything",
                ],
                "text": (
                    "Your five core Class 7 AI skills. "
                    "First — subject AI: using the right prompt for science, maths, English, and more. "
                    "Second — revision AI: summaries, flashcards, and spaced repetition. "
                    "Third — research AI: getting oriented fast, then verifying with trusted sources."
                ),
            },
            {
                "title": "Your Class 7 AI skills — continued",
                "bullets": [
                    "Critical thinking: question every AI answer",
                    "Safety: protect your data and recognise manipulation",
                    "Honesty: always acknowledge AI's contribution",
                ],
                "text": (
                    "Skills four and five. "
                    "Critical thinking — questioning AI answers with SIFT and independent verification. "
                    "Safety — protecting your personal data and recognising deepfakes and manipulation. "
                    "And underpinning everything: honesty about when and how you use AI."
                ),
            },
            {
                "title": "Build your AI portfolio",
                "bullets": [
                    "Choose your three best AI-assisted pieces of work",
                    "Write a short note explaining how AI helped in each",
                    "Reflect on what you did yourself vs what AI contributed",
                ],
                "text": (
                    "For your capstone portfolio, choose three pieces of work from this year "
                    "where AI helped you. "
                    "For each piece, write a short note explaining what AI contributed and what you did yourself. "
                    "This reflection is the most important part — it shows you genuinely understand the tool."
                ),
            },
            {
                "title": "What comes next — Class 8",
                "bullets": [
                    "Class 8 goes deeper into AI tools and real-world projects",
                    "You will learn prompt engineering in more detail",
                    "You will explore how AI is changing careers in India",
                ],
                "text": (
                    "In Class 8 you will go even deeper. "
                    "You will explore prompt engineering in more detail, "
                    "learn how AI is changing careers across India, "
                    "and work on longer AI-assisted projects. "
                    "The skills you built in Class 7 are the perfect foundation."
                ),
            },
            {
                "title": "Congratulations — keep going!",
                "bullets": [
                    "Share one thing you learned with a family member today",
                    "Use your AI skills every week — they grow with practice",
                    "You are now an AI-aware Class 7 student",
                ],
                "text": (
                    "Congratulations on completing Class 7 AI Daily Life Academy. "
                    "You are now an AI-aware student — able to use these tools wisely, "
                    "safely, and honestly. "
                    "Share one thing you learned with a family member today. "
                    "And keep practising — these skills grow the more you use them."
                ),
            },
        ],
    },
}


# ── TTS ──────────────────────────────────────────────────────────────────────

# ── rendering helpers ─────────────────────────────────────────────────────────

def _cover(path: Path) -> Image.Image:
    img = Image.open(path).convert("RGB")
    scale = max(VIDEO_W / img.width, VIDEO_H / img.height)
    img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    left = (img.width  - VIDEO_W) // 2
    top  = (img.height - VIDEO_H) // 2
    return img.crop((left, top, left + VIDEO_W, top + VIDEO_H))


def _wrap(draw: ImageDraw.ImageDraw, text: str,
          font: ImageFont.ImageFont, max_w: int) -> list[str]:
    words, lines, current = text.split(), [], ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if draw.textlength(candidate, font=font) <= max_w:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _put_lines(draw: ImageDraw.ImageDraw, lines: list[str], x: int, y: int,
               font: ImageFont.ImageFont, fill, gap: int) -> int:
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y += (bbox[3] - bbox[1]) + gap
    return y


def _make_frame(lesson_data: dict, scene: dict, idx: int, total: int) -> np.ndarray:
    base = _cover(ASSET_DIR / lesson_data["image"]).convert("RGBA")

    shade = Image.new("RGBA", (VIDEO_W, VIDEO_H), (0, 0, 0, 70))
    base.alpha_composite(shade)

    grad = Image.new("RGBA", (VIDEO_W, VIDEO_H), (0, 0, 0, 0))
    gd   = ImageDraw.Draw(grad)
    for x in range(0, 690):
        alpha = int(170 * (1 - x / 690))
        gd.line([(x, 0), (x, VIDEO_H)], fill=(2, 6, 23, alpha))
    base.alpha_composite(grad)

    ov  = Image.new("RGBA", (VIDEO_W, VIDEO_H), (0, 0, 0, 0))
    drw = ImageDraw.Draw(ov)
    drw.rounded_rectangle((56, 60, 642, 656), radius=28, fill=(8, 20, 36, 220), outline=(167, 139, 250, 145), width=2)
    drw.rounded_rectangle((86, 90, 336, 132), radius=20, fill=(*BADGE_COL, 220))
    drw.text((106, 99), lesson_data["badge"].upper(), font=FONT_BADGE, fill=(240, 240, 255, 255))
    drw.text((86, 155), f"{idx:02d}/{total:02d}", font=FONT_FOOTER, fill=(196, 181, 253, 255))

    y = 195
    for line in _wrap(drw, scene["title"], FONT_TITLE, 500):
        drw.text((86, y), line, font=FONT_TITLE, fill=(255, 255, 255, 255))
        bbox = drw.textbbox((86, y), line, font=FONT_TITLE)
        y += (bbox[3] - bbox[1]) + 12
    y += 20

    for bullet in scene["bullets"]:
        lines = _wrap(drw, bullet, FONT_BODY, 455)
        drw.ellipse((90, y + 12, 108, y + 30), fill=(167, 139, 250, 255))
        y = _put_lines(drw, lines, 126, y, FONT_BODY, (226, 232, 240, 255), 8)
        y += 14

    drw.text((86, 610), "Mitra AI Life", font=FONT_FOOTER, fill=(196, 181, 253, 255))
    base.alpha_composite(ov)
    return np.array(base.convert("RGB"))


# ── per-lesson generation ─────────────────────────────────────────────────────

def generate(lesson_id: str) -> None:
    data    = LESSONS[lesson_id]
    out     = ASSET_DIR / f"lesson-{lesson_id}-overview-charon.mp4"
    aud_dir = ASSET_DIR / f"audio_tmp_lesson-{lesson_id}-charon"
    aud_dir.mkdir(parents=True, exist_ok=True)

    # ── TTS ──────────────────────────────────────────────────────────────────
    client = texttospeech.TextToSpeechClient()
    audio_files: list[Path] = []
    print(f"\n=== Lesson {lesson_id}: {data['title']} ===")
    print(f"Step 1: TTS ({len(data['scenes'])} scenes)...")
    for i, scene in enumerate(data["scenes"], 1):
        path = aud_dir / f"scene-{i:02d}.mp3"
        if path.exists():
            print(f"  [{i}] skip (cached): {path.name}")
        else:
            print(f"  [{i}] TTS: {scene['text'][:64]}...")
            resp = client.synthesize_speech(
                input=texttospeech.SynthesisInput(text=scene["text"]),
                voice=texttospeech.VoiceSelectionParams(language_code=TTS_LANG, name=TTS_VOICE),
                audio_config=texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3,
                    speaking_rate=TTS_RATE,
                ),
                timeout=45,
            )
            path.write_bytes(resp.audio_content)
            print(f"    saved: {path.name}")
        audio_files.append(path)

    # ── video ────────────────────────────────────────────────────────────────
    print("Step 2: Building video...")
    total = len(data["scenes"])
    clips = []
    for i, (scene, aud) in enumerate(zip(data["scenes"], audio_files), 1):
        print(f"  [{i}/{total}] {scene['title']}")
        audio    = AudioFileClip(str(aud))
        duration = audio.duration + 0.45
        frame    = _make_frame(data, scene, i, total)
        clip     = ImageClip(frame, duration=duration)

        def _zoom(get_frame, t, dur=duration):
            f = get_frame(t)
            s = 1.0 + 0.035 * (float(t) / dur)
            h, w = f.shape[:2]
            z = Image.fromarray(f).resize((int(w * s), int(h * s)), Image.LANCZOS)
            ox, oy = (z.width - w) // 2, (z.height - h) // 2
            return np.array(z.crop((ox, oy, ox + w, oy + h)))

        clips.append(clip.transform(_zoom, apply_to="video").with_audio(audio))

    final = concatenate_videoclips(clips, method="compose")
    print(f"Step 3: Writing {out.name} ...")
    final.write_videofile(
        str(out), fps=FPS, codec="libx264", audio_codec="aac",
        temp_audiofile=str(aud_dir / "final_audio.m4a"), remove_temp=True, logger="bar",
    )
    print(f"Done: {out}  ({final.duration:.1f}s, {out.stat().st_size/1024/1024:.1f} MB)")

    # ── S3 upload ────────────────────────────────────────────────────────────
    s3_key = f"students/class-07/lesson-{lesson_id}-overview-charon.mp4"
    print(f"Step 4: Uploading to s3://mitra-ai-life-assets/{s3_key} ...")
    result = subprocess.run(
        ["aws", "s3", "cp", str(out),
         f"s3://mitra-ai-life-assets/{s3_key}",
         "--content-type", "video/mp4",
         "--cache-control", "public, max-age=86400"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print(f"  Uploaded OK: {s3_key}")
    else:
        print(f"  ERROR uploading: {result.stderr.strip()}")
        return

    embed_video_in_html(lesson_id)


def embed_video_in_html(lesson_id: str) -> None:
    """Replace the .video-coming placeholder with a real <video> element."""
    html_path = HTML_DIR / f"lesson-{lesson_id}.html"
    if not html_path.exists():
        print(f"  HTML not found: {html_path}")
        return

    html = html_path.read_text(encoding="utf-8")
    if "<video" in html:
        print(f"  HTML already has <video>: {html_path.name}")
        return

    s3_url = (
        f"https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/"
        f"{S3_PREFIX}/lesson-{lesson_id}-overview-charon.mp4"
    )
    poster_url = (
        f"https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/"
        f"{S3_PREFIX}/lesson-{lesson_id}-hero.jpg"
    )

    # Build the replacement block — keep .video-box wrapper for CSS compatibility
    video_element = (
        f'<div class="video-box">\n'
        f'      <video controls preload="none"\n'
        f'             poster="{poster_url}">\n'
        f'        <source src="{s3_url}" type="video/mp4">\n'
        f'        Your browser does not support the video tag.\n'
        f'      </video>\n'
        f'    </div>'
    )

    # Replace <div class="video-coming">...</div> using depth counter
    MARKER = '<div class="video-coming">'
    if MARKER not in html:
        print(f"  WARNING: No .video-coming placeholder in {html_path.name} — edit manually")
        return

    start = html.index(MARKER)
    depth = 0
    i = start
    while i < len(html):
        if html[i:i+4] == "<div":
            depth += 1
        elif html[i:i+6] == "</div>":
            depth -= 1
            if depth == 0:
                end = i + 6
                break
        i += 1
    else:
        print(f"  WARNING: Could not find closing </div> for .video-coming in {html_path.name}")
        return

    new_html = html[:start] + video_element + html[end:]

    # Also add .video-box CSS if not present
    if ".video-box {" not in new_html:
        video_box_css = (
            ".video-box { position: relative; width: 90%; max-width: 820px; "
            "margin: 0 auto; padding-top: 56.25%; border-radius: 14px; "
            "overflow: hidden; background: #020617; border: 2px solid rgba(139,92,246,0.35); }\n"
            ".video-box video { position: absolute; inset: 0; width: 100%; height: 100%; "
            "display: block; background: #020617; }\n"
        )
        new_html = new_html.replace(".video-coming {", video_box_css + ".video-coming {", 1)

    html_path.write_text(new_html, encoding="utf-8")
    print(f"  Embedded video in: {html_path.name}")


def main() -> None:
    ids = sys.argv[1:] if len(sys.argv) > 1 else list(LESSONS.keys())
    for lesson_id in ids:
        if lesson_id not in LESSONS:
            print(f"Unknown lesson ID: {lesson_id}")
            continue
        generate(lesson_id)
    print("\nAll done.")


if __name__ == "__main__":
    main()
