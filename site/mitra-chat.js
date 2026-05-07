/**
 * Mitra Chatbot Widget — mitra-chat.js
 * Include on every page: <script src="/site/mitra-chat.js"></script>
 * Or with relative path from level pages: <script src="../../../site/mitra-chat.js"></script>
 *
 * SETUP: After deploying the Cloudflare Worker, update WORKER_URL below.
 */

(function () {
  "use strict";

  // ── Config ─────────────────────────────────────────────────────────────────
  const WORKER_URL = "https://mitra-chat-worker.rajendar-mi46.workers.dev";
  const MITRA_ICON_URL =
    "https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/characters/mitra-icon.png";
  // Fallback emoji if icon not loaded yet
  const FALLBACK_EMOJI = "🔵";

  // Detect language from page: index-te.html or level-xx-comic-te.html → Telugu
  const isTelugu =
    document.documentElement.lang === "te" ||
    window.location.pathname.includes("-te.html");

  const PLACEHOLDER = isTelugu
    ? "మీ ప్రశ్న అడగండి..."
    : "Ask me anything...";
  const GREETING = isTelugu
    ? "నమస్కారం! నేను మిత్ర 👋 మీకు ఏ స్థాయి నుండి ప్రారంభించాలో లేదా ఈ platform గురించి ఏమైనా తెలుసుకోవాలంటే అడగండి!"
    : "Hi! I'm Mitra 👋 Ask me which level to start, what this platform teaches, or anything about learning AI in daily life!";

  // ── Conversation history ────────────────────────────────────────────────────
  const history = [];

  // ── Build widget DOM ────────────────────────────────────────────────────────
  function buildWidget() {
    const style = document.createElement("style");
    style.textContent = `
      #mitra-chat-btn {
        position: fixed;
        bottom: 24px;
        right: 24px;
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3b82f6, #06b6d4);
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 16px rgba(59,130,246,0.45);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        transition: transform 0.2s, box-shadow 0.2s;
        padding: 0;
        overflow: hidden;
      }
      #mitra-chat-btn:hover {
        transform: scale(1.08);
        box-shadow: 0 6px 20px rgba(59,130,246,0.6);
      }
      #mitra-chat-btn img {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
      }
      #mitra-chat-btn .fallback {
        font-size: 26px;
        line-height: 1;
      }
      #mitra-chat-panel {
        position: fixed;
        bottom: 90px;
        right: 24px;
        width: 340px;
        max-height: 480px;
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.18);
        display: none;
        flex-direction: column;
        z-index: 9998;
        overflow: hidden;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 14px;
      }
      #mitra-chat-panel.open { display: flex; }
      #mitra-chat-header {
        background: linear-gradient(135deg, #3b82f6, #06b6d4);
        color: #fff;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        flex-shrink: 0;
      }
      #mitra-chat-header img {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        object-fit: cover;
        background: rgba(255,255,255,0.2);
      }
      #mitra-chat-header .hdr-text { flex: 1; }
      #mitra-chat-header .hdr-text strong { display: block; font-size: 15px; }
      #mitra-chat-header .hdr-text span { font-size: 11px; opacity: 0.85; }
      #mitra-chat-close {
        background: none;
        border: none;
        color: #fff;
        font-size: 20px;
        cursor: pointer;
        padding: 0 2px;
        line-height: 1;
        opacity: 0.8;
      }
      #mitra-chat-close:hover { opacity: 1; }
      #mitra-chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 14px 12px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        background: #f8fafc;
      }
      .mc-msg {
        max-width: 85%;
        padding: 9px 12px;
        border-radius: 12px;
        line-height: 1.45;
        word-break: break-word;
        font-size: 13.5px;
      }
      .mc-msg.bot {
        background: #e0f2fe;
        color: #0c4a6e;
        align-self: flex-start;
        border-bottom-left-radius: 3px;
      }
      .mc-msg.user {
        background: #3b82f6;
        color: #fff;
        align-self: flex-end;
        border-bottom-right-radius: 3px;
      }
      .mc-msg.typing { opacity: 0.6; font-style: italic; }
      #mitra-chat-disclaimer {
        font-size: 10.5px;
        color: #94a3b8;
        text-align: center;
        padding: 4px 12px 2px;
        background: #f8fafc;
        flex-shrink: 0;
      }
      #mitra-chat-input-row {
        display: flex;
        padding: 10px;
        gap: 8px;
        background: #fff;
        border-top: 1px solid #e2e8f0;
        flex-shrink: 0;
      }
      #mitra-chat-input {
        flex: 1;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 8px 10px;
        font-size: 13.5px;
        outline: none;
        resize: none;
        font-family: inherit;
        line-height: 1.4;
        max-height: 80px;
        min-height: 36px;
      }
      #mitra-chat-input:focus { border-color: #3b82f6; }
      #mitra-chat-send {
        background: linear-gradient(135deg, #3b82f6, #06b6d4);
        color: #fff;
        border: none;
        border-radius: 8px;
        padding: 0 14px;
        cursor: pointer;
        font-size: 18px;
        transition: opacity 0.2s;
        flex-shrink: 0;
      }
      #mitra-chat-send:hover { opacity: 0.88; }
      #mitra-chat-send:disabled { opacity: 0.4; cursor: not-allowed; }
      @media (max-width: 400px) {
        #mitra-chat-panel { width: calc(100vw - 20px); right: 10px; bottom: 80px; }
        #mitra-chat-btn { bottom: 16px; right: 16px; }
      }
    `;
    document.head.appendChild(style);

    // Floating button
    const btn = document.createElement("button");
    btn.id = "mitra-chat-btn";
    btn.setAttribute("aria-label", "Chat with Mitra");
    btn.setAttribute("title", "Chat with Mitra");

    const btnImg = document.createElement("img");
    btnImg.src = MITRA_ICON_URL;
    btnImg.alt = "Mitra";
    btnImg.onerror = function () {
      btn.innerHTML = `<span class="fallback">${FALLBACK_EMOJI}</span>`;
    };
    btn.appendChild(btnImg);

    // Chat panel
    const panel = document.createElement("div");
    panel.id = "mitra-chat-panel";
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", "Mitra AI Chat");

    // Header
    const header = document.createElement("div");
    header.id = "mitra-chat-header";

    const headerImg = document.createElement("img");
    headerImg.src = MITRA_ICON_URL;
    headerImg.alt = "Mitra";
    headerImg.onerror = function () {
      this.style.display = "none";
    };

    const hdrText = document.createElement("div");
    hdrText.className = "hdr-text";
    hdrText.innerHTML = `<strong>Mitra</strong><span>Your AI learning guide</span>`;

    const closeBtn = document.createElement("button");
    closeBtn.id = "mitra-chat-close";
    closeBtn.setAttribute("aria-label", "Close chat");
    closeBtn.textContent = "×";

    header.appendChild(headerImg);
    header.appendChild(hdrText);
    header.appendChild(closeBtn);

    // Messages container
    const messages = document.createElement("div");
    messages.id = "mitra-chat-messages";
    messages.setAttribute("aria-live", "polite");

    // Disclaimer
    const disclaimer = document.createElement("div");
    disclaimer.id = "mitra-chat-disclaimer";
    disclaimer.textContent = "AI can be wrong. Always verify important information.";

    // Input row
    const inputRow = document.createElement("div");
    inputRow.id = "mitra-chat-input-row";

    const input = document.createElement("textarea");
    input.id = "mitra-chat-input";
    input.placeholder = PLACEHOLDER;
    input.rows = 1;
    input.setAttribute("aria-label", "Message");

    const sendBtn = document.createElement("button");
    sendBtn.id = "mitra-chat-send";
    sendBtn.setAttribute("aria-label", "Send");
    sendBtn.textContent = "➤";

    inputRow.appendChild(input);
    inputRow.appendChild(sendBtn);

    panel.appendChild(header);
    panel.appendChild(messages);
    panel.appendChild(disclaimer);
    panel.appendChild(inputRow);

    document.body.appendChild(btn);
    document.body.appendChild(panel);

    return { btn, panel, closeBtn, messages, input, sendBtn };
  }

  // ── Helpers ─────────────────────────────────────────────────────────────────
  function addMessage(container, text, role) {
    const msg = document.createElement("div");
    msg.className = `mc-msg ${role}`;
    // Simple newline → <br> rendering, no innerHTML injection from API
    msg.textContent = text;
    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
    return msg;
  }

  function addTypingIndicator(container) {
    const msg = document.createElement("div");
    msg.className = "mc-msg bot typing";
    msg.textContent = "Mitra is thinking...";
    msg.id = "mitra-typing";
    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
    return msg;
  }

  // ── Send message with streaming ────────────────────────────────────────────
  async function sendMessage(text, messagesEl, sendBtn, inputEl) {
    if (!text.trim()) return;

    history.push({ role: "user", content: text });
    addMessage(messagesEl, text, "user");

    sendBtn.disabled = true;
    inputEl.disabled = true;
    const typing = addTypingIndicator(messagesEl);

    try {
      const res = await fetch(WORKER_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: history }),
      });

      if (!res.ok) {
        throw new Error(`Worker returned ${res.status}`);
      }

      // Remove typing indicator
      typing.remove();

      // Stream response
      const botMsg = addMessage(messagesEl, "", "bot");
      let fullText = "";

      const reader = res.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const data = line.slice(6).trim();
          if (data === "[DONE]") break;

          try {
            const parsed = JSON.parse(data);
            const delta = parsed.choices?.[0]?.delta?.content;
            if (delta) {
              fullText += delta;
              botMsg.textContent = fullText;
              messagesEl.scrollTop = messagesEl.scrollHeight;
            }
          } catch {
            // partial JSON chunk — skip
          }
        }
      }

      if (fullText) {
        history.push({ role: "assistant", content: fullText });
      }
    } catch (err) {
      typing.remove();
      const errText = isTelugu
        ? "క్షమించండి, సమాధానం పొందడంలో సమస్య వచ్చింది. దయచేసి మళ్ళీ ప్రయత్నించండి."
        : "Sorry, I couldn't reach the server. Please try again in a moment.";
      addMessage(messagesEl, errText, "bot");
      console.error("Mitra chat error:", err);
    } finally {
      sendBtn.disabled = false;
      inputEl.disabled = false;
      inputEl.focus();
    }
  }

  // ── Init ────────────────────────────────────────────────────────────────────
  function init() {
    const { btn, panel, closeBtn, messages, input, sendBtn } = buildWidget();

    // Show greeting on first open
    let greeted = false;

    btn.addEventListener("click", () => {
      const isOpen = panel.classList.contains("open");
      if (!isOpen) {
        panel.classList.add("open");
        btn.setAttribute("aria-expanded", "true");
        if (!greeted) {
          addMessage(messages, GREETING, "bot");
          greeted = true;
        }
        input.focus();
      } else {
        panel.classList.remove("open");
        btn.setAttribute("aria-expanded", "false");
      }
    });

    closeBtn.addEventListener("click", () => {
      panel.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
    });

    // Send on button click
    sendBtn.addEventListener("click", () => {
      const text = input.value.trim();
      if (!text) return;
      input.value = "";
      input.style.height = "auto";
      sendMessage(text, messages, sendBtn, input);
    });

    // Send on Enter (Shift+Enter = new line)
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendBtn.click();
      }
    });

    // Auto-resize textarea
    input.addEventListener("input", () => {
      input.style.height = "auto";
      input.style.height = Math.min(input.scrollHeight, 80) + "px";
    });

    // Close on Escape
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && panel.classList.contains("open")) {
        panel.classList.remove("open");
        btn.setAttribute("aria-expanded", "false");
      }
    });
  }

  // Run after DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
