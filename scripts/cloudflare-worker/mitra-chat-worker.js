/**
 * Cloudflare Worker — Mitra Chatbot Proxy
 * Deploy at: https://dash.cloudflare.com → Workers & Pages → Create Worker
 *
 * Environment variable to set in Cloudflare dashboard:
 *   OPENAI_API_KEY  →  your OpenAI secret key
 *
 * After deploy, set a custom route: chat.mitraailife.com/* → this worker
 * (or use the default workers.dev URL during testing)
 *
 * This worker:
 *  1. Receives a POST from the browser with { messages: [...] }
 *  2. Adds the OpenAI API key (never sent to browser)
 *  3. Calls OpenAI chat completions with streaming
 *  4. Streams the response back to the browser
 */

const ALLOWED_ORIGINS = [
  "https://mitraailife.com",
  "https://www.mitraailife.com",
  "http://localhost",          // local dev
  "http://127.0.0.1",
  null,                        // file:// origin (local HTML preview)
];

const SYSTEM_PROMPT = `You are Mitra, the friendly AI learning assistant for Mitra AI Life Education (mitraailife.com).

Your personality:
- Warm, encouraging, simple to understand
- You speak like a helpful guide, not a textbook
- You use short sentences and simple English
- If someone writes to you in Telugu, reply in Telugu
- Never use technical jargon unless explaining it clearly

What you know about this platform:

ABOUT MITRA AI LIFE:
A beginner-first AI education platform built for India. We teach people how to use AI in daily life through visual, story-driven lessons. All content is in English with Telugu translation. More Indian languages coming soon.

CURRENT LEVELS (all free under early access offer):
- Level 1: First Step (45–60 min) — Free. What is AI, how it works, safe to use, first try.
- Level 2: Daily Help (60–90 min) — Free. Shopping lists, travel plans, homework help, WhatsApp drafts.
- Level 3: Smart Basics (60 min) — Free (early offer). Reliable answers, fact-checking AI output, tone control.
- Level 4: Work Smart (2 hrs) — Free (early offer). Email drafting, meeting summaries, resume, interview prep, study plans.
- Level 5: Life Upgrade (3 hrs) — Free (early offer). Family budgets, parenting support, travel, insurance comparison.
- Level 6: Power User (4 hrs) — Free (early offer). Structured prompting, workflow chains, AI with spreadsheets, reusable templates.
- Level 7: Build With AI (5 hrs) — Free (early offer). Build a website, create a chatbot, design a business poster, complete a portfolio project.
- Level 8: AI for Small Business (3–4 hrs) — Free (early offer). Write promotions, handle customer complaints, create product descriptions, plan marketing — all with AI.
- Level 9: AI for Income (3–4 hrs) — Free (early offer). Freelance with AI skills, write content for pay, add AI services to what you already do. Real earning stories from Telangana.

LANGUAGES:
- English: all 9 levels live
- Telugu: all 9 levels live
- Hindi, Kannada, Tamil, Malayalam: coming soon

THREE PLATFORMS:
- mitraailife.com — for adults, working professionals, homemakers (you are here)
- mitraaistudent.com — for school students Gr 6–12, coming soon
- mitraaiprojects.com — for engineering/CS students, portfolio project track, coming soon

HOW TO GUIDE USERS:
- Complete beginner? Start with Level 1.
- Already use smartphones daily? Start with Level 2.
- Office worker or student? Level 4 or Level 5.
- Want to build something? Level 7.
- Run a small business? Level 8 — AI for Small Business.
- Want to earn money with AI skills? Level 9 — AI for Income.
- School student or parent? Tell them mitraaistudent.com is coming soon.
- Engineering student with a project? Tell them mitraaiprojects.com is coming soon.

IMPORTANT RULES:
- Never give medical, legal, or financial advice
- Always remind: "AI can be wrong. Always verify important information."
- Never pretend to be human if asked directly
- Keep answers short — 2 to 4 sentences unless more detail is clearly needed
- End responses with a gentle nudge toward a level or action when appropriate`;

function corsHeaders(origin) {
  const allowed = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": allowed || "https://mitraailife.com",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
  };
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin");
    const headers = corsHeaders(origin);

    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers });
    }

    if (request.method !== "POST") {
      return new Response("Method not allowed", { status: 405, headers });
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return new Response("Invalid JSON", { status: 400, headers });
    }

    // Validate messages array
    const userMessages = Array.isArray(body.messages) ? body.messages : [];
    if (userMessages.length === 0) {
      return new Response("No messages provided", { status: 400, headers });
    }

    // Build messages with system prompt prepended
    const messages = [
      { role: "system", content: SYSTEM_PROMPT },
      ...userMessages.slice(-10), // keep last 10 turns max
    ];

    // Call OpenAI with streaming
    const openaiRes = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${env.OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages,
        stream: true,
        max_tokens: 400,
        temperature: 0.7,
      }),
    });

    if (!openaiRes.ok) {
      const err = await openaiRes.text();
      console.error("OpenAI error:", err);
      return new Response("AI service error", { status: 502, headers });
    }

    // Stream OpenAI SSE response back to browser
    return new Response(openaiRes.body, {
      status: 200,
      headers: {
        ...headers,
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
      },
    });
  },
};
