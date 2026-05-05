---
description: "Generate a beginner-friendly lesson pack for a selected level and topic, with English master content and Telugu localization notes."
name: "Create Lesson Pack"
argument-hint: "Level name and lesson topic"
agent: "Bilingual Content Architect"
model: "GPT-5 (copilot)"
tools: [read, edit, search]
---

Create a complete lesson pack for the requested level and topic.

Requirements:
- follow the level ladder and positioning in [level-content-plan](../../docs/level-content-plan.md)
- produce English master content first
- add Telugu localization notes after the English content
- keep the lesson beginner-friendly unless the requested level is Level 6 or Level 7
- include:
  - objective
  - target learner
  - estimated duration
  - story-based introduction
  - 3 practical prompts
  - 1 caution or verification note
  - asset ideas for comic, image slide, and short video
  - worksheet activity

Write the output as markdown suitable for the `content/` folders.
