"""
Generate Class 6 lesson overview videos for lessons 04-12.

Produces (one file per lesson):
  content/assets/students/class-06/lesson-NN-overview-charon.mp4

Uses Google Cloud TTS (en-US-Chirp3-HD-Charon) + Class 6 hero images.

Run:
  source .env
  .venv/bin/python scripts/generate_class06_lessons_04_12.py           # all
  .venv/bin/python scripts/generate_class06_lessons_04_12.py 04        # sample
  .venv/bin/python scripts/generate_class06_lessons_04_12.py 04 05 06  # subset
"""

from __future__ import annotations
import os
import sys
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips

# ── env ──────────────────────────────────────────────────────────────────────
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

# ── config ───────────────────────────────────────────────────────────────────
ROOT           = Path(__file__).parent.parent
ASSET_DIR      = ROOT / "content" / "assets" / "students" / "class-06"
TTS_VOICE      = "en-US-Chirp3-HD-Charon"
TTS_LANG       = "en-US"
TTS_RATE       = 1.0
VIDEO_W        = 1280
VIDEO_H        = 720
FPS            = 24

os.environ["IMAGEIO_FFMPEG_EXE"] = imageio_ffmpeg.get_ffmpeg_exe()

# ── lesson data ───────────────────────────────────────────────────────────────
LESSONS: dict[str, dict] = {
    "04": {
        "badge": "Class 6 · Lesson 4",
        "title": "Types of AI Tools",
        "image": "lesson-04-hero.jpg",
        "scenes": [
            {
                "title": "Six families of AI tools",
                "bullets": ["Language AI reads and writes", "Image AI turns text to pictures", "Voice AI listens and speaks"],
                "text": (
                    "Welcome to Class 6 Lesson 4, Types of AI Tools. "
                    "You will discover the six families of AI tools — and learn which one to use for which task. "
                    "By the end, you will spot them in your own daily life."
                ),
            },
            {
                "title": "Language AI — chatbots",
                "bullets": ["ChatGPT, Gemini, Copilot", "Reads your question, writes an answer", "Check facts before trusting"],
                "text": (
                    "Language AI is the family of chatbots — ChatGPT, Gemini, Microsoft Copilot, and others. "
                    "They read your question and write a reply in natural language. "
                    "They are useful for explaining ideas, drafting messages, and brainstorming — but always check important facts."
                ),
            },
            {
                "title": "Image AI and Voice AI",
                "bullets": ["DALL-E and Firefly make images from words", "Voice AI converts speech to text", "Google Assistant uses both"],
                "text": (
                    "Image AI tools like DALL-E and Adobe Firefly generate pictures from a text description. "
                    "Voice AI tools transcribe your speech, translate languages, and speak back in natural voices. "
                    "Your phone assistant combines both every time you speak a command."
                ),
            },
            {
                "title": "Recommendation AI",
                "bullets": ["Studies your watch and click patterns", "Builds a profile over time", "Filter bubbles are a side-effect"],
                "text": (
                    "Recommendation AI is the invisible curator behind YouTube, Netflix, and Amazon. "
                    "It studies what you watch, buy, and skip — then predicts what to show next. "
                    "The more you interact, the stronger the filter bubble becomes."
                ),
            },
            {
                "title": "Computer Vision AI",
                "bullets": ["Face unlock recognises patterns", "Plantix diagnoses crops from a photo", "CCTV uses it for safety"],
                "text": (
                    "Computer Vision AI lets machines see and interpret images. "
                    "Face unlock, Plantix crop diagnosis, Google Lens, and traffic cameras all use it. "
                    "In India, computer vision is being used in agriculture, healthcare screening, and public safety."
                ),
            },
            {
                "title": "Prediction AI",
                "bullets": ["Weather apps forecast rain", "Banks predict fraud in seconds", "IMD uses it for cyclone alerts"],
                "text": (
                    "Prediction AI studies historical patterns to forecast the future. "
                    "IMD uses it for monsoon and cyclone alerts. Banks use it to block fraud within seconds. "
                    "APSRTC and railways use it to schedule routes and manage maintenance."
                ),
            },
            {
                "title": "Right tool, right task",
                "bullets": ["Match the tool to your need", "Never share personal data", "Verify before acting on any output"],
                "text": (
                    "The key skill is matching the right AI tool to the right task. "
                    "Use language AI for writing and explaining. Use image AI for visuals. Use voice AI for hands-free interaction. "
                    "And always remember: never share personal information with any AI tool, and verify before acting on any output."
                ),
            },
        ],
    },
    "05": {
        "badge": "Class 6 · Lesson 5",
        "title": "AI in Education",
        "image": "lesson-05-hero.jpg",
        "scenes": [
            {
                "title": "AI is changing how we learn",
                "bullets": ["Personalised explanations", "Instant practice and feedback", "Available 24 hours a day"],
                "text": (
                    "Welcome to Class 6 Lesson 5, AI in Education. "
                    "AI tutors can explain topics in simple words, generate practice questions, and give feedback in seconds. "
                    "You are in the first generation of students who can use this power in your study routine."
                ),
            },
            {
                "title": "Khan Academy and DIKSHA",
                "bullets": ["Step-by-step video explanations", "AI tracks progress and adjusts level", "Free for every Indian student"],
                "text": (
                    "Khan Academy uses AI to personalise learning — it identifies where you are struggling and gives you extra practice on those concepts. "
                    "India's DIKSHA platform offers curriculum-aligned content in regional languages. "
                    "Both are free and available on a basic Android phone."
                ),
            },
            {
                "title": "How to ask AI for help with studies",
                "bullets": ["Explain this in simple words", "Give me 5 practice questions", "Check my answer for mistakes"],
                "text": (
                    "Three prompts every student needs: "
                    "Explain this topic in simple words for a Class 6 student. "
                    "Give me five practice questions on this chapter. "
                    "I wrote this answer — what mistakes did I make? "
                    "These three prompts can replace expensive tuition for many topics."
                ),
            },
            {
                "title": "Adaptive learning platforms",
                "bullets": ["Byju's adjusts question difficulty", "Duolingo personalises language practice", "Socratic explains photos of homework"],
                "text": (
                    "Adaptive learning platforms like Byju's, Vedantu, and Unacademy adjust question difficulty based on your answers. "
                    "Duolingo uses AI to personalise your language practice. "
                    "Google's Socratic app can photograph a homework question and explain the steps."
                ),
            },
            {
                "title": "Important limits — AI is not always right",
                "bullets": ["Check against textbook", "AI can fabricate facts", "Your teacher knows the syllabus"],
                "text": (
                    "AI education tools have important limits. They can make up facts, give outdated information, or miss syllabus requirements. "
                    "Always check AI explanations against your textbook. "
                    "Your teacher understands the exam pattern — AI does not know the CBSE or State Board syllabus unless you tell it."
                ),
            },
            {
                "title": "India AI Reporter activity",
                "bullets": ["Pick one AI education tool", "Describe what it can do", "Note one limit or risk"],
                "text": (
                    "In today's activity you are an India AI Reporter. "
                    "Pick one AI education tool available in India — free or paid. "
                    "Write what it does, who it helps, and one important limit or risk. "
                    "Think like a journalist: be curious and balanced."
                ),
            },
        ],
    },
    "06": {
        "badge": "Class 6 · Lesson 6",
        "title": "AI and Creativity",
        "image": "lesson-06-hero.jpg",
        "scenes": [
            {
                "title": "Can AI be creative?",
                "bullets": ["AI recombines patterns it has learned", "You bring original intent", "Human plus AI beats AI alone"],
                "text": (
                    "Welcome to Class 6 Lesson 6, AI and Creativity. "
                    "AI does not have original ideas — it recombines patterns it has seen in millions of examples. "
                    "But when you bring your intent and judgment, AI becomes a powerful creative partner."
                ),
            },
            {
                "title": "AI writing tools",
                "bullets": ["Draft a story opening in seconds", "Ask for different tones and styles", "Edit and add your own voice"],
                "text": (
                    "AI writing tools can draft a story opening, suggest plot twists, or change the tone from formal to friendly. "
                    "Use them to overcome blank-page fear. "
                    "Then take the draft and add your voice, your detail, your lived experience — which AI can never have."
                ),
            },
            {
                "title": "AI image generation",
                "bullets": ["Describe the image in words", "Refine with style cues", "Use for inspiration not plagiarism"],
                "text": (
                    "AI image tools like DALL-E and Adobe Firefly generate images from your text description. "
                    "A good prompt includes subject, mood, style, and lighting. "
                    "Use generated images as inspiration or reference — never pass them off as your own hand-drawn work."
                ),
            },
            {
                "title": "AI music and audio",
                "bullets": ["Suno generates short music clips", "Describe genre, mood, tempo", "School projects love background music"],
                "text": (
                    "AI music tools like Suno and Udio can generate a short background track from a simple description. "
                    "Try: upbeat Indian folk music for a school project video, medium tempo. "
                    "Great for presentations, but always tell your audience when AI audio is used."
                ),
            },
            {
                "title": "Honesty and attribution",
                "bullets": ["Tell your teacher which parts used AI", "Add a note in creative submissions", "Passing AI work as purely yours is dishonest"],
                "text": (
                    "Using AI creatively is not cheating — but claiming AI output as purely your own work is dishonest. "
                    "Add a short note to school projects that says which parts used AI assistance. "
                    "Your teacher will respect your honesty — and your original contribution will stand out more clearly."
                ),
            },
            {
                "title": "Your creative AI project",
                "bullets": ["Choose story, image, or music", "Document what AI suggested", "Write what you changed and why"],
                "text": (
                    "In today's worksheet you will design a short creative project. "
                    "Choose a story, a drawing prompt, or a music description. "
                    "Write what AI suggested, what you changed, and what part is entirely your own. "
                    "That reflection is more valuable than the final output."
                ),
            },
        ],
    },
    "07": {
        "badge": "Class 6 · Lesson 7",
        "title": "AI Safety and Privacy",
        "image": "lesson-07-hero.jpg",
        "scenes": [
            {
                "title": "What data does AI collect?",
                "bullets": ["Every search and click is data", "Apps share data with AI providers", "Your profile builds over time"],
                "text": (
                    "Welcome to Class 6 Lesson 7, AI Safety and Privacy. "
                    "Every search, click, voice command, and location check feeds into AI profiles that grow over time. "
                    "Understanding what data is collected is the first step to staying safe."
                ),
            },
            {
                "title": "Never share personal information",
                "bullets": ["No home address or school name", "No phone number or passwords", "No family details or photos"],
                "text": (
                    "The core safety rule is simple: never share personal information with any AI tool. "
                    "This includes your home address, school name, phone number, passwords, and family photos. "
                    "Even free AI tools store conversations and use them to improve their models."
                ),
            },
            {
                "title": "Deepfakes and fake news",
                "bullets": ["AI can copy anyone's voice and face", "Verify before you share", "Check the original source"],
                "text": (
                    "AI can now generate convincing fake videos and voice clips called deepfakes. "
                    "A video of a famous person saying something does not mean they said it. "
                    "Always check the original source before forwarding anything on WhatsApp or social media."
                ),
            },
            {
                "title": "App permissions and privacy settings",
                "bullets": ["Camera and microphone need a reason", "Location should be on-demand only", "Review permissions once a month"],
                "text": (
                    "Review which apps have camera, microphone, and location permissions on your phone. "
                    "Camera and microphone need a clear reason — a shopping app does not need your microphone. "
                    "Set location to on-demand rather than always-on wherever possible."
                ),
            },
            {
                "title": "India's data protection law",
                "bullets": ["DPDPA 2023 protects your data", "You can request deletion", "Parents must consent for children"],
                "text": (
                    "India's Digital Personal Data Protection Act of 2023 gives you rights over your personal data. "
                    "You can ask companies to tell you what data they hold and request deletion. "
                    "For children under 18, parental consent is required before companies can collect personal data."
                ),
            },
            {
                "title": "Five safety habits to start today",
                "bullets": ["Think before you type", "Verify before you forward", "Review app permissions monthly"],
                "text": (
                    "Five safety habits to start right now. "
                    "Think before typing anything personal into an AI tool. "
                    "Verify before forwarding any news or video. "
                    "Review your app permissions every month. "
                    "Tell a trusted adult if any AI interaction makes you uncomfortable. "
                    "Use strong and unique passwords for every account."
                ),
            },
        ],
    },
    "08": {
        "badge": "Class 6 · Lesson 8",
        "title": "Digital Citizenship",
        "image": "lesson-08-hero.jpg",
        "scenes": [
            {
                "title": "What is a digital citizen?",
                "bullets": ["Rights and responsibilities online", "Respect, safety, and honesty", "Every post shapes your digital footprint"],
                "text": (
                    "Welcome to Class 6 Lesson 8, Digital Citizenship. "
                    "A digital citizen uses technology responsibly and respectfully. "
                    "Every post, search, and comment you make online contributes to a permanent digital footprint."
                ),
            },
            {
                "title": "Your digital footprint",
                "bullets": ["Searches and posts stay forever", "Colleges and employers can find it", "Create a positive record now"],
                "text": (
                    "Your digital footprint is the permanent trail of data you leave every time you use the internet. "
                    "Searches, posts, comments, and logins all contribute. "
                    "Colleges and future employers increasingly check digital presence — so build a positive record now."
                ),
            },
            {
                "title": "Cyberbullying and online respect",
                "bullets": ["Words online cause real harm", "Screenshot and report, do not retaliate", "Be the bystander who speaks up"],
                "text": (
                    "Cyberbullying is using technology to harm, embarrass, or threaten others. "
                    "Words online cause real psychological harm. "
                    "If you see cyberbullying, screenshot it, report it to the platform, and tell a trusted adult. "
                    "Never retaliate — be the bystander who speaks up."
                ),
            },
            {
                "title": "Misinformation and responsible sharing",
                "bullets": ["Read before sharing", "Check the original source", "Forwarding without checking spreads harm"],
                "text": (
                    "Misinformation spreads faster than corrections. "
                    "Before sharing any news, video, or post — read it fully, check the original source, and look for a second confirmation. "
                    "WhatsApp forwards can cause real-world harm. Responsible sharing is a form of digital citizenship."
                ),
            },
            {
                "title": "Healthy screen habits",
                "bullets": ["Intentional use beats passive scrolling", "No phones during study and meals", "One offline hour before sleep"],
                "text": (
                    "Healthy screen use means intentional use — opening an app for a purpose and closing it when done. "
                    "Passive scrolling for long periods crowds out sleep, physical activity, and face-to-face friendships. "
                    "Try one phone-free hour before bed and notice the difference."
                ),
            },
            {
                "title": "My digital citizenship audit",
                "bullets": ["Rate yourself honestly", "Pick one habit to improve", "Write your commitment"],
                "text": (
                    "In today's worksheet, you will audit your own digital citizenship. "
                    "Rate yourself honestly across five areas: privacy, honesty, respect, safety, and screen balance. "
                    "Pick one area to improve — and write one specific action you will take this week."
                ),
            },
        ],
    },
    "09": {
        "badge": "Class 6 · Lesson 9",
        "title": "AI and Creativity — Advanced",
        "image": "lesson-09-hero.jpg",
        "scenes": [
            {
                "title": "Raju, the storyteller",
                "bullets": ["AI gave the opening", "Raju drew the panels", "Human creativity led the way"],
                "text": (
                    "Welcome to Class 6 Lesson 9. "
                    "In our story, Raju used AI to generate a 4-panel comic story — and then drew it himself. "
                    "The AI gave the skeleton; Raju's hand, imagination, and style made it real. "
                    "That collaboration is the future of creative work."
                ),
            },
            {
                "title": "Text-to-image AI",
                "bullets": ["Describe subject, style, lighting", "Add Indian context to prompts", "Use for reference, not submission"],
                "text": (
                    "Text-to-image tools generate visuals from a description. "
                    "A strong prompt includes the subject, art style, mood, and context. "
                    "Try: a Class 6 student in Vijayawada reading under a banyan tree, watercolour style, golden evening light. "
                    "Use the result as reference or inspiration — not as your submitted artwork."
                ),
            },
            {
                "title": "Comic and storyboard generation",
                "bullets": ["Ask AI for a 4-panel story plot", "Each panel gets one scene description", "You supply the drawing skill"],
                "text": (
                    "Ask AI to write a 4-panel comic story plot on any topic. "
                    "Each panel becomes a scene description you can draw. "
                    "You control the characters, the setting, and the visual style. "
                    "AI handles the plot skeleton; you supply the drawing skill and artistic judgment."
                ),
            },
            {
                "title": "Creative writing collaboration",
                "bullets": ["Ask for three different story openings", "Pick the one that excites you", "Rewrite it in your voice"],
                "text": (
                    "Use AI to generate three different openings for the same story idea. "
                    "Pick the one that excites you the most — and rewrite it in your own voice. "
                    "Add details only you could add: your street, your neighbourhood sound, your friend's name. "
                    "That is where AI assistance becomes your creative work."
                ),
            },
            {
                "title": "Attribution and honesty",
                "bullets": ["Note AI's contribution clearly", "Your edits are your intellectual work", "Teachers value honest process"],
                "text": (
                    "When you use AI creatively, note its contribution clearly. "
                    "Your edits, additions, and artistic choices are your intellectual work. "
                    "Teachers and evaluators increasingly value a transparent creative process over a polished final product. "
                    "Show your work — including the AI parts."
                ),
            },
            {
                "title": "My AI creative project worksheet",
                "bullets": ["Choose your creative format", "Describe the AI prompt used", "Write what you added and changed"],
                "text": (
                    "In today's worksheet, plan your own AI creative project. "
                    "Choose a format — story, comic, image, or music. "
                    "Write the prompt you would give the AI, what you expect it to produce, "
                    "and most importantly — what you will add, change, or improve to make it uniquely yours."
                ),
            },
        ],
    },
    "10": {
        "badge": "Class 6 · Lesson 10",
        "title": "AI Ethics and Trust",
        "image": "lesson-10-hero.jpg",
        "scenes": [
            {
                "title": "When AI gets things wrong",
                "bullets": ["AI can generate false facts", "Called hallucination", "Looks confident, can be wrong"],
                "text": (
                    "Welcome to Class 6 Lesson 10, AI Ethics and Trust. "
                    "AI can generate false information with complete confidence — this is called hallucination. "
                    "A chatbot will not say it does not know. It will make up a plausible-sounding answer. "
                    "Your job is to verify."
                ),
            },
            {
                "title": "Deepfakes and manipulated media",
                "bullets": ["AI can create fake videos of anyone", "Voice cloning is now accessible", "Check source, check date, cross-reference"],
                "text": (
                    "Deepfake technology can put words in anyone's mouth using only a few seconds of real audio. "
                    "Before sharing any video or audio clip, check the original source, check the date, and find a second confirmation. "
                    "If something seems designed to make you angry or afraid, be extra sceptical."
                ),
            },
            {
                "title": "Bias in AI systems",
                "bullets": ["AI reflects training data biases", "Facial recognition errors on darker skin", "Biased hiring and lending decisions"],
                "text": (
                    "AI systems can be biased when their training data does not represent everyone fairly. "
                    "Facial recognition systems have shown higher error rates on darker skin tones. "
                    "AI hiring tools have been found to favour certain names and universities. "
                    "Bias in AI can have serious real-world consequences."
                ),
            },
            {
                "title": "The AI fact-check habit",
                "bullets": ["Ask: what is the source?", "Check against a textbook or official site", "Look for bias in the question"],
                "text": (
                    "Develop the AI fact-check habit. "
                    "When AI gives you an important fact, ask yourself: what is the source? "
                    "Check it against your textbook, an official government site, or a trusted news publication. "
                    "And notice whether your own question was framed in a way that pushed the AI toward a biased answer."
                ),
            },
            {
                "title": "Privacy and consent",
                "bullets": ["Consent means choosing freely", "Terms of service can hide data use", "India's DPDPA gives you rights"],
                "text": (
                    "Consent means you have chosen freely, with full information, and can say no without penalty. "
                    "Long terms-of-service documents often bury clauses about how your data will be used. "
                    "India's DPDPA gives you the right to know what data is held and to request its deletion."
                ),
            },
            {
                "title": "AI fact-check challenge",
                "bullets": ["Pick one AI claim", "Verify against a trusted source", "Write what you found"],
                "text": (
                    "In today's worksheet you will run your own AI fact-check challenge. "
                    "Ask an AI tool one factual question about any subject. "
                    "Then verify the answer against your textbook or an official source. "
                    "Write what matched, what was wrong, and what you learned about trusting AI outputs."
                ),
            },
        ],
    },
    "11": {
        "badge": "Class 6 · Lesson 11",
        "title": "AI in India",
        "image": "lesson-11-hero.jpg",
        "scenes": [
            {
                "title": "India and AI — a growing story",
                "bullets": ["1.4 billion users, 22 official languages", "Local language AI is growing fast", "India is both user and builder of AI"],
                "text": (
                    "Welcome to Class 6 Lesson 11, AI in India. "
                    "India has 1.4 billion people, 22 official languages, and one of the world's fastest-growing smartphone populations. "
                    "India is not just a user of AI — it is becoming a major builder too."
                ),
            },
            {
                "title": "AI4Bharat and local language AI",
                "bullets": ["IIT Madras built multilingual models", "Works in Telugu, Tamil, Hindi and more", "Voice, translation, and text generation"],
                "text": (
                    "AI4Bharat, from IIT Madras, builds AI models for Indian languages — including Telugu, Tamil, Hindi, and 19 others. "
                    "Their tools support voice recognition, translation, and text generation in local languages. "
                    "This makes AI accessible to hundreds of millions of people who do not read English."
                ),
            },
            {
                "title": "Aadhaar and DigiLocker",
                "bullets": ["Biometric identity for 1.4 billion", "AI matches face to Aadhaar data", "DigiLocker stores your documents safely"],
                "text": (
                    "Aadhaar uses AI to match a person's fingerprint or iris to their identity record — at massive national scale. "
                    "DigiLocker stores your school certificates, driving licence, and other documents digitally. "
                    "AI verifies your identity when you access them."
                ),
            },
            {
                "title": "Plantix and AI in agriculture",
                "bullets": ["Photograph a diseased crop leaf", "AI identifies the disease instantly", "Used by millions of Indian farmers"],
                "text": (
                    "Plantix is a phone app that identifies crop diseases from a single photograph. "
                    "Farmers in Andhra Pradesh, Telangana, and across India use it to get instant diagnosis and treatment advice. "
                    "This is AI serving farmers who would otherwise wait days for an expert."
                ),
            },
            {
                "title": "AI in Indian healthcare",
                "bullets": ["Wadhwani AI screens for TB in X-rays", "Niramai detects breast cancer from heat scans", "Remedi HQ analyses ECG data"],
                "text": (
                    "Wadhwani AI uses AI to screen chest X-rays for tuberculosis — critical in a country where TB affects millions. "
                    "Niramai uses thermal imaging and AI to detect breast cancer without radiation. "
                    "These tools bring specialist-level diagnosis to clinics in small towns."
                ),
            },
            {
                "title": "My AI in India research worksheet",
                "bullets": ["Pick one AI application in India", "Describe the problem it solves", "Note who benefits and any risk"],
                "text": (
                    "In today's worksheet, you will research one AI application in India. "
                    "Describe the problem it solves, who benefits, and one important ethical or practical risk. "
                    "Think like a responsible citizen: AI can solve problems, but it can also create new ones. "
                    "Your job is to see both sides clearly."
                ),
            },
        ],
    },
    "12": {
        "badge": "Class 6 · Lesson 12",
        "title": "Capstone — What You Learned",
        "image": "lesson-12-hero.jpg",
        "scenes": [
            {
                "title": "You made it to Lesson 12",
                "bullets": ["12 lessons, one year of AI literacy", "From what is AI to building a portfolio", "You are a smarter AI user now"],
                "text": (
                    "Welcome to Class 6 Lesson 12 — your capstone. "
                    "Over 12 lessons you have gone from asking what is AI to spotting bias, checking facts, and using AI safely. "
                    "You are now one of the most AI-literate students in your class."
                ),
            },
            {
                "title": "What you learned — the big 6",
                "bullets": ["What AI is and how it learns", "Six families of AI tools", "AI in education, creativity, and India"],
                "text": (
                    "You learned what AI is and how machine learning works. "
                    "You discovered the six families of AI tools and when to use each. "
                    "You explored AI in education, creativity, digital citizenship, privacy, ethics, and in India's own story."
                ),
            },
            {
                "title": "Your five core skills",
                "bullets": ["Spot AI in everyday apps", "Verify before trusting any output", "Use AI to learn, not to copy"],
                "text": (
                    "You now have five core skills. "
                    "Spot AI in the apps you use every day. "
                    "Verify AI output before trusting or sharing it. "
                    "Use AI to learn and create — not to copy and paste. "
                    "Protect your personal data. "
                    "Think critically about who benefits and who might be harmed."
                ),
            },
            {
                "title": "Your AI skills checklist",
                "bullets": ["Check off each skill you have learned", "Be honest about gaps", "Target those gaps in Class 7"],
                "text": (
                    "In the capstone worksheet you will complete an AI skills checklist. "
                    "Go through each skill from the 12 lessons. "
                    "Be honest about which ones you have mastered and which ones need more practice. "
                    "Your honest self-assessment will guide your Class 7 learning."
                ),
            },
            {
                "title": "Class 7 — what comes next",
                "bullets": ["Deeper into prompt engineering", "AI ethics and society", "Projects using real AI tools"],
                "text": (
                    "In Class 7 you will go deeper. "
                    "You will learn to write prompts that produce professional results. "
                    "You will explore how AI is shaping society, jobs, and the environment. "
                    "And you will build real projects using AI tools with clear documentation of your process."
                ),
            },
            {
                "title": "Congratulations — and keep going",
                "bullets": ["Free Class 7 awaits you", "Share what you learned with family", "AI literacy is a life skill"],
                "text": (
                    "Congratulations on completing Class 6 AI Daily Life Academy. "
                    "Share what you learned with your family — explain one AI tool they use every day. "
                    "Class 7 is free and waiting for you. "
                    "AI literacy is not a school subject — it is a life skill. And you have made a strong start."
                ),
            },
        ],
    },
}


# ── rendering helpers (identical to generate_class06_lesson_videos.py) ───────

def _load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


FONT_BADGE  = _load_font(26, bold=True)
FONT_TITLE  = _load_font(54, bold=True)
FONT_BODY   = _load_font(34)
FONT_FOOTER = _load_font(22, bold=True)


def _cover(path: Path) -> Image.Image:
    img = Image.open(path).convert("RGB")
    scale = max(VIDEO_W / img.width, VIDEO_H / img.height)
    img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    left = (img.width  - VIDEO_W) // 2
    top  = (img.height - VIDEO_H) // 2
    return img.crop((left, top, left + VIDEO_W, top + VIDEO_H))


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_w: int) -> list[str]:
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
    drw.rounded_rectangle((56, 60, 642, 656), radius=28, fill=(8, 20, 36, 220), outline=(56, 189, 248, 145), width=2)
    drw.rounded_rectangle((86, 90, 336, 132), radius=20, fill=(14, 165, 233, 220))
    drw.text((106, 99), lesson_data["badge"].upper(), font=FONT_BADGE, fill=(240, 249, 255, 255))
    drw.text((86, 155), f"{idx:02d}/{total:02d}", font=FONT_FOOTER, fill=(125, 211, 252, 255))

    y = 195
    for line in _wrap(drw, scene["title"], FONT_TITLE, 500):
        drw.text((86, y), line, font=FONT_TITLE, fill=(255, 255, 255, 255))
        bbox = drw.textbbox((86, y), line, font=FONT_TITLE)
        y += (bbox[3] - bbox[1]) + 12
    y += 20

    for bullet in scene["bullets"]:
        lines = _wrap(drw, bullet, FONT_BODY, 455)
        drw.ellipse((90, y + 12, 108, y + 30), fill=(34, 197, 94, 255))
        y = _put_lines(drw, lines, 126, y, FONT_BODY, (226, 232, 240, 255), 8)
        y += 14

    drw.text((86, 610), "Mitra AI Life", font=FONT_FOOTER, fill=(186, 230, 253, 255))
    base.alpha_composite(ov)
    return np.array(base.convert("RGB"))


# ── per-lesson generation ─────────────────────────────────────────────────────

def generate(lesson_id: str) -> None:
    data    = LESSONS[lesson_id]
    out     = ASSET_DIR / f"lesson-{lesson_id}-overview-charon.mp4"
    aud_dir = ASSET_DIR / f"audio_tmp_lesson-{lesson_id}-charon"
    aud_dir.mkdir(parents=True, exist_ok=True)

    # ── TTS ──────────────────────────────────────────────────────────────────
    from google.cloud import texttospeech
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
    s3_key = f"students/class-06/lesson-{lesson_id}-overview-charon.mp4"
    print(f"Step 4: Uploading to s3://mitra-ai-life-assets/{s3_key} ...")
    import subprocess
    result = subprocess.run([
        "aws", "s3", "cp", str(out),
        f"s3://mitra-ai-life-assets/{s3_key}",
        "--content-type", "video/mp4",
        "--cache-control", "public, max-age=86400",
    ], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  Uploaded OK: {s3_key}")
    else:
        print(f"  UPLOAD FAILED:\n{result.stderr}")


# ── embed video in HTML ───────────────────────────────────────────────────────

def embed_video_in_html(lesson_id: str) -> None:
    """Replace the placeholder .video-box block with a real <video> element, or skip if already done."""
    html_path = ROOT / "content" / "students" / "class-06" / f"lesson-{lesson_id}.html"
    if not html_path.exists():
        print(f"  HTML not found: {html_path}")
        return

    html = html_path.read_text(encoding="utf-8")
    if "<video" in html:
        print(f"  HTML already has <video>: {html_path.name}")
        return

    s3_url = (
        f"https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/"
        f"students/class-06/lesson-{lesson_id}-overview-charon.mp4"
    )
    poster_url = (
        f"https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/"
        f"students/class-06/lesson-{lesson_id}-hero.jpg"
    )
    video_element = (
        f'<div class="video-box">\n'
        f'      <video controls preload="none"\n'
        f'             poster="{poster_url}">\n'
        f'        <source src="{s3_url}" type="video/mp4">\n'
        f'        Your browser does not support the video tag.\n'
        f'      </video>\n'
        f'    </div>'
    )

    # Find the .video-box block and replace it using a div-depth counter
    MARKER = '<div class="video-box">'
    if MARKER not in html:
        print(f"  WARNING: No .video-box placeholder found in {html_path.name} — edit manually")
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
        print(f"  WARNING: Could not find matching </div> for .video-box in {html_path.name}")
        return

    new_html = html[:start] + video_element + html[end:]
    html_path.write_text(new_html, encoding="utf-8")
    print(f"  Embedded video in: {html_path.name}")


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    targets = sys.argv[1:] if len(sys.argv) > 1 else sorted(LESSONS)
    for lid in targets:
        lid = lid.zfill(2)
        if lid not in LESSONS:
            print(f"Unknown lesson id: {lid}. Available: {sorted(LESSONS)}")
            sys.exit(1)
        generate(lid)
        embed_video_in_html(lid)
    print("\nAll done.")


if __name__ == "__main__":
    main()
