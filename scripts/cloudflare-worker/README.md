# Cloudflare Worker — Mitra Chatbot Proxy Setup Guide

## What this is

A tiny serverless function that proxies OpenAI API calls from the browser.
The OpenAI API key lives only in Cloudflare's secure environment — never in browser code.

## Deploy steps

### 1. Go to Cloudflare Workers
https://dash.cloudflare.com → Workers & Pages → Create Worker

### 2. Paste the worker code
Copy the entire contents of `mitra-chat-worker.js` into the worker editor.
Click "Save and Deploy".

### 3. Set the environment variable
In the worker dashboard → Settings → Variables → Add variable:
```
Variable name:  OPENAI_API_KEY
Value:          sk-... (your key from .env)
```
Mark it as a secret (encrypted). Click Save.

### 4. Set the custom domain (after testing)
In the worker → Settings → Triggers → Add Custom Domain:
```
chat.mitraailife.com
```
This requires mitraailife.com to be using Cloudflare DNS (it must already be proxied through Cloudflare for GitHub Pages custom domain to work).

### 5. Test with curl first
```bash
curl -X POST https://your-worker.workers.dev \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What is Level 1?"}]}'
```

### 6. Update WORKER_URL in mitra-chat.js
Once the worker is live, set the URL in `site/mitra-chat.js`:
```js
const WORKER_URL = 'https://chat.mitraailife.com';
// or during testing:
// const WORKER_URL = 'https://mitra-chat.YOUR-SUBDOMAIN.workers.dev';
```

## Free tier limits
- 100,000 requests per day
- 10ms CPU time per request (streaming is fine — mostly I/O wait)
- No credit card needed for this usage level

## Security notes
- CORS is restricted to mitraailife.com origins only
- OpenAI key never reaches the browser
- Max 10 conversation turns sent per request (prevents prompt injection via history bloat)
- Max 400 tokens per response (keeps costs low)
