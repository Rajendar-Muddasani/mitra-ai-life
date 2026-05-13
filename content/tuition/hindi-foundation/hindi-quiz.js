/*
 * Hindi listening quiz — vanilla JS, no framework dependency.
 *
 * Mount: <div id="hindi-quiz" data-quiz="h3-words"></div>
 *
 * Each question shows a Play button and three image options. The child taps
 * the image that matches the spoken Hindi word. Correct → "बहुत अच्छा!".
 * Wrong → "एक बार और बोलिए" (try once more) — no shaming, no scoring.
 *
 * Audio uses the SpeechSynthesis API (browser-native TTS) with `hi-IN` locale
 * when available — falls back gracefully if the device has no Hindi voice.
 */

(function () {
  "use strict";

  const QUIZZES = {
    "h3-words": {
      title: "Listening check",
      base: "../../assets/images/word-cards/",
      questions: [
        // animals
        { word: "शेर",   answer: "h3-animals/sher.png",
          options: ["h3-animals/sher.png", "h3-animals/billi.png", "h3-animals/kutta.png"] },
        { word: "हाथी",  answer: "h3-animals/haathi.png",
          options: ["h3-animals/bandar.png", "h3-animals/haathi.png", "h3-animals/chidiya.png"] },
        // food
        { word: "रोटी",  answer: "h3-food/roti.png",
          options: ["h3-food/dal.png", "h3-food/roti.png", "h3-food/sabzi.png"] },
        { word: "दूध",   answer: "h3-food/doodh.png",
          options: ["h3-food/doodh.png", "h3-food/chawal.png", "h3-food/phal.png"] },
        // home
        { word: "पंखा",  answer: "h3-home/pankha.png",
          options: ["h3-home/kursi.png", "h3-home/darwaza.png", "h3-home/pankha.png"] },
        { word: "खिड़की", answer: "h3-home/khidki.png",
          options: ["h3-home/khidki.png", "h3-home/bistar.png", "h3-home/mez.png"] },
        // body
        { word: "आँख",   answer: "h3-body/aankh.png",
          options: ["h3-body/naak.png", "h3-body/kaan.png", "h3-body/aankh.png"] },
        { word: "हाथ",   answer: "h3-body/haath.png",
          options: ["h3-body/haath.png", "h3-body/pair.png", "h3-body/sir.png"] },
        // colours
        { word: "लाल",   answer: "h3-colours/lal.png",
          options: ["h3-colours/hara.png", "h3-colours/lal.png", "h3-colours/neela.png"] },
        { word: "पीला",  answer: "h3-colours/peela.png",
          options: ["h3-colours/peela.png", "h3-colours/kaala.png", "h3-colours/safed.png"] },
      ],
    },
  };

  function speakHindi(text) {
    if (!("speechSynthesis" in window)) return;
    try {
      window.speechSynthesis.cancel();
      const utter = new SpeechSynthesisUtterance(text);
      utter.lang = "hi-IN";
      utter.rate = 0.78;
      // Prefer a Hindi voice if available
      const voices = window.speechSynthesis.getVoices();
      const hi = voices.find((v) => /hi[-_]IN/i.test(v.lang || ""));
      if (hi) utter.voice = hi;
      window.speechSynthesis.speak(utter);
    } catch (_) {
      /* ignore */
    }
  }

  function pickRandomIndexes(n, k) {
    const out = [];
    const used = new Set();
    while (out.length < k && used.size < n) {
      const idx = Math.floor(Math.random() * n);
      if (!used.has(idx)) {
        used.add(idx);
        out.push(idx);
      }
    }
    return out;
  }

  function buildQuestionCard(spec, qIdx, q, onCorrect, onWrong) {
    const card = document.createElement("div");
    card.className = "hq-card";

    const head = document.createElement("div");
    head.className = "hq-head";

    const counter = document.createElement("span");
    counter.className = "hq-counter";
    counter.textContent = `Question ${qIdx + 1}`;

    const playBtn = document.createElement("button");
    playBtn.type = "button";
    playBtn.className = "hq-play";
    playBtn.innerHTML = "▶ Play <span>" + q.word + "</span>";
    playBtn.addEventListener("click", () => speakHindi(q.word));

    head.appendChild(counter);
    head.appendChild(playBtn);
    card.appendChild(head);

    const grid = document.createElement("div");
    grid.className = "hq-options";

    // Shuffle option order so the answer position varies
    const shuffled = q.options.slice();
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }

    shuffled.forEach((path) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "hq-option";
      const img = document.createElement("img");
      img.src = spec.base + path;
      img.alt = "option";
      img.loading = "lazy";
      btn.appendChild(img);
      btn.addEventListener("click", () => {
        if (btn.classList.contains("hq-correct") || btn.classList.contains("hq-wrong")) return;
        if (path === q.answer) {
          btn.classList.add("hq-correct");
          onCorrect();
        } else {
          btn.classList.add("hq-wrong");
          onWrong();
        }
      });
      grid.appendChild(btn);
    });

    card.appendChild(grid);

    const feedback = document.createElement("div");
    feedback.className = "hq-feedback";
    card.appendChild(feedback);

    return { card, feedback };
  }

  function render(host, spec) {
    host.innerHTML = "";

    const wrap = document.createElement("div");
    wrap.className = "hq-wrap";

    const intro = document.createElement("p");
    intro.className = "hq-intro";
    intro.textContent = "Press Play to hear the word, then tap the picture that matches.";
    wrap.appendChild(intro);

    // Pick 5 random questions per session
    const picks = pickRandomIndexes(spec.questions.length, 5);
    picks.forEach((qIdx, i) => {
      const q = spec.questions[qIdx];
      const { card, feedback } = buildQuestionCard(spec, i, q,
        () => { feedback.textContent = "बहुत अच्छा! Very good."; feedback.dataset.state = "good"; },
        () => { feedback.textContent = "एक बार और बोलिए — try once more."; feedback.dataset.state = "again"; },
      );
      wrap.appendChild(card);
    });

    const again = document.createElement("button");
    again.type = "button";
    again.className = "hq-again";
    again.textContent = "Try a new set →";
    again.addEventListener("click", () => render(host, spec));
    wrap.appendChild(again);

    host.appendChild(wrap);
  }

  function init() {
    document.querySelectorAll("[data-quiz]").forEach((host) => {
      const key = host.getAttribute("data-quiz");
      const spec = QUIZZES[key];
      if (!spec) return;
      render(host, spec);
    });

    // Prime voices on some browsers (Chrome doesn't load until first call)
    if ("speechSynthesis" in window) {
      window.speechSynthesis.getVoices();
      window.speechSynthesis.addEventListener?.("voiceschanged", () => {
        window.speechSynthesis.getVoices();
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
