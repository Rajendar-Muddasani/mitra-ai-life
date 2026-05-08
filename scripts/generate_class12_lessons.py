#!/usr/bin/env python3
"""Generate Class 12 lesson HTML files for Mitra AI Life.

Each lesson follows the established Class 11 template with:
- Indigo theme (#4f46e5)
- Hero with breadcrumb, S3 image, meta pills
- 4-6 lesson sections (label + title + HTML body)
- 8-question quiz, all answers 'b', GA4 event
- Schema.org LearningResource JSON-LD
- Prev/Next navigation
"""

from pathlib import Path
from textwrap import dedent

OUT_DIR = Path(__file__).parent.parent / "content" / "students" / "class-12"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Common quiz answer key — every lesson uses option 'b'
ANSWERS = {i: 'b' for i in range(1, 9)}


def page(num, title, emoji, character, city, story_summary, sections, quiz_questions,
         age="16-17", lesson_count=12, prev=None, next_=None):
    """Render one lesson HTML page."""
    fname = f"lesson-{num:02d}.html"
    prev_html = (
        f'<a href="{prev["href"]}" class="btn-prev">← {prev["label"]}</a>'
        if prev else '<a href="class-12.html" class="btn-prev">← Class 12 Hub</a>'
    )
    next_html = (
        f'<a href="{next_["href"]}" class="btn-hub">{next_["label"]} →</a>'
        if next_ else '<a href="class-12.html" class="btn-hub">← Back to Class 12 Hub</a>'
    )

    sections_html = ""
    for s in sections:
        sections_html += f'''
  <div class="lesson-section">
    <div class="ls-label">{s["label"]}</div>
    <div class="ls-title">{s["title"]}</div>
    {s["body"]}
  </div>'''

    quiz_html = ""
    for i, q in enumerate(quiz_questions, 1):
        opts_html = ""
        for letter in ['a', 'b', 'c', 'd']:
            opts_html += f'        <div class="quiz-opt" data-opt="{letter}">{letter}) {q["opts"][letter]}</div>\n'
        quiz_html += f'''      <div class="q-block" data-q="{i}">
        <div class="q-text">{i}. {q["q"]}</div>
{opts_html}      </div>
'''

    answers_js = ",".join([f"{i}:'b'" for i in range(1, len(quiz_questions) + 1)])
    canonical_url = f"https://mitraailife.com/content/students/class-12/{fname}"
    s3_image = f"https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/students/class-12/lesson-{num:02d}-hero.jpg"
    og_desc = f"Class 12 Lesson {num:02d}: {title}. {story_summary[:140]}"
    meta_desc = f"Class 12 Lesson {num:02d} for JC +2 students: {title}. Story of {character}, {city}. {story_summary[:120]}"

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Lesson {num:02d} — {title} | Class 12 | Mitra AI Life</title>
<meta name="description" content="{meta_desc}" />
<link rel="canonical" href="{canonical_url}" />
<link rel="icon" href="../../../site/favicon.ico" sizes="any" />
<meta name="theme-color" content="#4f46e5" />
<meta property="og:type" content="article" />
<meta property="og:title" content="Lesson {num:02d} — {title} | Class 12 | Mitra AI Life" />
<meta property="og:description" content="{og_desc}" />
<meta property="og:url" content="{canonical_url}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Baloo+2:wght@700;800&display=swap" rel="stylesheet" />
<script async src="https://www.googletagmanager.com/gtag/js?id=G-QGY0LH6W93"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-QGY0LH6W93');</script>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Nunito',sans-serif;background:#eef2ff;color:#312e81;line-height:1.7}}
a{{color:#4f46e5;text-decoration:none}}a:hover{{text-decoration:underline}}
.topnav{{background:#0f172a;padding:.75rem 1.5rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:.5rem}}
.topnav .brand{{color:#fff;font-family:'Baloo 2',cursive;font-size:1.1rem;font-weight:800;text-decoration:none}}
.topnav .brand span{{color:#a5b4fc}}
.topnav .nav-links{{display:flex;gap:1rem;flex-wrap:wrap}}
.topnav .nav-links a{{color:rgba(255,255,255,.7);font-size:.85rem;font-weight:600;text-decoration:none}}
.topnav .nav-links a:hover{{color:#fff}}.topnav .nav-links a.active{{color:#a5b4fc}}
.lesson-hero{{background:linear-gradient(135deg,#1e1b4b,#3730a3,#4f46e5);padding:3rem 1.5rem 4rem;color:#fff;text-align:center;position:relative;overflow:hidden}}
.lesson-hero::before{{content:'';position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23fff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")}}
.lesson-hero .breadcrumb{{font-size:.78rem;color:rgba(255,255,255,.65);margin-bottom:1rem;position:relative}}
.lesson-hero .breadcrumb a{{color:rgba(255,255,255,.78);text-decoration:underline}}
.lesson-hero h1{{font-family:'Baloo 2',cursive;font-size:clamp(1.9rem,5vw,3rem);font-weight:800;line-height:1.15;margin-bottom:.7rem;position:relative}}
.lesson-hero .meta{{font-size:.85rem;color:rgba(255,255,255,.78);position:relative}}
.lesson-hero .meta span{{background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.22);border-radius:20px;padding:.2rem .75rem;margin:.2rem;display:inline-block}}
.hero-img{{width:100%;height:240px;object-fit:cover;object-position:center 40%;display:block}}
.content-wrap{{max-width:820px;margin:0 auto;padding:2.5rem 1.5rem 4rem}}
.lesson-section{{margin-bottom:2.5rem}}
.ls-label{{font-size:.7rem;font-weight:800;letter-spacing:.15em;text-transform:uppercase;color:#4f46e5;margin-bottom:.3rem}}
.ls-title{{font-family:'Baloo 2',cursive;font-size:1.55rem;color:#312e81;margin-bottom:.7rem}}
.lesson-section p{{font-size:.95rem;color:#4338ca;margin-bottom:.9rem}}
.lesson-section ul,ol{{font-size:.93rem;color:#4338ca;padding-left:1.4rem;margin-bottom:.9rem}}
.lesson-section li{{margin-bottom:.45rem}}
.lesson-section strong{{color:#312e81}}
.callout{{border-radius:12px;padding:.9rem 1.1rem;font-size:.88rem;margin:1rem 0}}
.callout.indigo{{background:#eef2ff;border-left:4px solid #4f46e5;color:#312e81}}
.callout.green{{background:#ecfdf5;border-left:4px solid #059669;color:#064e3b}}
.callout.red{{background:#fef2f2;border-left:4px solid #dc2626;color:#7f1d1d}}
pre{{background:#1e1b4b;color:#e0e7ff;border-radius:10px;padding:.9rem 1rem;overflow-x:auto;font-size:.8rem;line-height:1.55;margin:.8rem 0;font-family:'Menlo','Monaco',monospace}}
code{{font-family:'Menlo','Monaco',monospace;background:#e0e7ff;color:#3730a3;padding:1px 5px;border-radius:4px;font-size:.85em}}
pre code{{background:transparent;color:inherit;padding:0}}
.story-card{{background:#fff;border:2px solid #c7d2fe;border-radius:14px;padding:1.1rem 1.3rem;margin:1rem 0}}
.story-card .story-who{{font-size:.78rem;font-weight:800;color:#4f46e5;letter-spacing:.08em;text-transform:uppercase;margin-bottom:.4rem}}
.story-card p{{margin-bottom:.6rem}}
.story-card p:last-child{{margin-bottom:0}}
.concept-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:.7rem;margin:1rem 0}}
.concept-card{{background:#fff;border:1.5px solid #c7d2fe;border-radius:10px;padding:.7rem .85rem}}
.concept-card h4{{font-family:'Baloo 2',cursive;font-size:.88rem;color:#4f46e5;margin-bottom:.25rem}}
.concept-card p{{font-size:.78rem;color:#4338ca;margin:0;line-height:1.45}}
table{{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.84rem}}
th{{background:#4f46e5;color:#fff;padding:.5rem .7rem;text-align:left}}
td{{padding:.5rem .7rem;border-bottom:1px solid #c7d2fe;color:#312e81;vertical-align:top}}
tr:nth-child(even) td{{background:#eef2ff}}
.quiz-section{{background:#fff;border:2px solid #4f46e5;border-radius:18px;padding:1.8rem;margin:2rem 0}}
.quiz-section h3{{font-family:'Baloo 2',cursive;font-size:1.2rem;color:#312e81;margin-bottom:1.2rem}}
.q-block{{margin-bottom:1.5rem}}
.q-block .q-text{{font-weight:700;color:#312e81;font-size:.93rem;margin-bottom:.6rem}}
.quiz-opt{{display:flex;align-items:flex-start;gap:.6rem;padding:.55rem .8rem;border-radius:8px;cursor:pointer;margin-bottom:.3rem;border:1.5px solid #c7d2fe;background:#eef2ff;font-size:.87rem;color:#312e81;transition:border-color .15s;line-height:1.45}}
.quiz-opt:hover{{border-color:#4f46e5}}
.quiz-opt.selected{{border-color:#4f46e5;font-weight:700}}
.quiz-opt.correct{{border-color:#22c55e;background:#f0fdf4;color:#14532d}}
.quiz-opt.wrong{{border-color:#f43f5e;background:#fff1f2;color:#881337}}
.quiz-btn{{background:#4f46e5;color:#fff;border:none;border-radius:10px;padding:.7rem 2rem;font-weight:800;font-size:.95rem;cursor:pointer;margin-top:.5rem;font-family:'Nunito',sans-serif}}
.quiz-btn:hover{{background:#3730a3}}
.quiz-btn:disabled{{opacity:.6;cursor:not-allowed}}
.quiz-result{{display:none;margin-top:1rem;padding:1rem;border-radius:10px;font-weight:700;text-align:center}}
.quiz-result.good{{background:#f0fdf4;color:#14532d;border:2px solid #22c55e}}
.quiz-result.ok{{background:#fef3c7;color:#78350f;border:2px solid #f59e0b}}
.quiz-result.low{{background:#fff1f2;color:#881337;border:2px solid #f43f5e}}
.lesson-nav{{display:flex;justify-content:space-between;align-items:center;margin-top:2.5rem;flex-wrap:wrap;gap:1rem}}
.lesson-nav a{{display:inline-block;padding:.65rem 1.4rem;border-radius:10px;font-weight:800;font-size:.88rem;text-decoration:none}}
.lesson-nav .btn-prev{{background:#fff;border:2px solid #4f46e5;color:#4f46e5}}
.lesson-nav .btn-hub{{background:#4f46e5;color:#fff}}
.lesson-nav .btn-prev:hover{{background:#eef2ff}}
.lesson-nav .btn-hub:hover{{background:#3730a3}}
footer{{background:#0f172a;color:rgba(255,255,255,.55);padding:2rem 1.5rem;text-align:center;font-size:.82rem}}
footer a{{color:rgba(255,255,255,.6)}}
footer .footer-brand{{font-family:'Baloo 2',cursive;font-size:.9rem;color:rgba(255,255,255,.8);margin-bottom:.5rem}}
@media(max-width:600px){{.content-wrap{{padding:2rem 1rem 3rem}}.concept-grid{{grid-template-columns:1fr 1fr}}}}
</style>
</head>
<body>
<nav class="topnav">
  <a href="../../../site/index.html" class="brand">Mitra <span>AI</span> Life</a>
  <div class="nav-links">
    <a href="class-12.html" class="active">Class 12</a>
    <a href="../../../site/students.html">All Classes</a>
    <a href="../../../site/index.html">Home</a>
  </div>
</nav>

<header class="lesson-hero">
  <div class="breadcrumb"><a href="class-12.html">Class 12</a> → Lesson {num:02d}</div>
  <h1>{title} {emoji}</h1>
  <div class="meta">
    <span>Class 12</span><span>Age {age}</span><span>Lesson {num:02d} of {lesson_count}</span><span>🆓 Free</span>
  </div>
</header>

<img class="hero-img" src="{s3_image}" alt="Class 12 Lesson {num:02d} hero — {character}, {city}" loading="lazy" onerror="this.style.display='none'" />

<main class="content-wrap">
{sections_html}

  <div class="quiz-section">
    <h3>📝 Check Your Understanding (8 Questions)</h3>
    <div id="quiz-container">
{quiz_html}    </div>
    <button class="quiz-btn" id="quiz-submit">Submit Quiz</button>
    <div class="quiz-result" id="quiz-result"></div>
  </div>

  <div class="lesson-nav">
    {prev_html}
    {next_html}
  </div>
</main>

<footer>
  <div class="footer-brand">Mitra AI Life</div>
  <p style="margin-bottom:.5rem;"><a href="../../../site/index.html">Home</a> · <a href="class-12.html">Class 12</a> · <a href="../../../site/students.html">All Classes</a> · <a href="../../../site/privacy.html">Privacy Policy</a></p>
  <p>© 2026 Mitra AI Life Education · Free AI education for every student</p>
</footer>

<script>
const ANSWERS={{{answers_js}}};
document.querySelectorAll('.q-block').forEach(block=>{{
  block.querySelectorAll('.quiz-opt').forEach(opt=>{{
    opt.addEventListener('click',()=>{{
      block.querySelectorAll('.quiz-opt').forEach(o=>o.classList.remove('selected'));
      opt.classList.add('selected');
    }});
  }});
}});
document.getElementById('quiz-submit').addEventListener('click',()=>{{
  let score=0,total=Object.keys(ANSWERS).length;
  Object.keys(ANSWERS).forEach(q=>{{
    const block=document.querySelector(`.q-block[data-q="${{q}}"]`);
    const sel=block.querySelector('.quiz-opt.selected');
    block.querySelectorAll('.quiz-opt').forEach(o=>{{
      o.classList.remove('correct','wrong');
      if(o.dataset.opt===ANSWERS[q])o.classList.add('correct');
    }});
    if(sel){{if(sel.dataset.opt===ANSWERS[q])score++;else sel.classList.add('wrong');}}
  }});
  const res=document.getElementById('quiz-result');
  res.style.display='block';
  let pct=Math.round(score/total*100);
  if(pct>=80){{res.className='quiz-result good';res.textContent=`Excellent! ${{score}}/${{total}} (${{pct}}%) — You're ready for the next lesson.`;}}
  else if(pct>=60){{res.className='quiz-result ok';res.textContent=`${{score}}/${{total}} (${{pct}}%) — Good. Review the wrong ones, then continue.`;}}
  else{{res.className='quiz-result low';res.textContent=`${{score}}/${{total}} (${{pct}}%) — Re-read the lesson, especially the sections related to the wrong answers.`;}}
  gtag('event','quiz_complete',{{event_category:'class12',event_label:'class12_lesson{num:02d}_quiz',value:score}});
  document.getElementById('quiz-submit').disabled=true;
}});
</script>
<script type="application/ld+json">
{{
  "@context":"https://schema.org",
  "@type":"LearningResource",
  "name":"{title} — Class 12 Lesson {num:02d}",
  "description":"{og_desc}",
  "url":"{canonical_url}",
  "learningResourceType":"Lesson",
  "educationalLevel":"Junior College +2",
  "typicalAgeRange":"{age}",
  "inLanguage":"en",
  "isAccessibleForFree":true,
  "provider":{{"@type":"Organization","name":"Mitra AI Life Education","url":"https://mitraailife.com"}}
}}
</script>
</body>
</html>
'''
    (OUT_DIR / fname).write_text(html, encoding="utf-8")
    print(f"  ✓ {fname}")


# ============================================================================
# LESSON SPECS — 12 lessons for Class 12 (JC +2)
# ============================================================================

LESSONS = []

# ----------------- LESSON 01 -----------------
LESSONS.append(dict(
    num=1, title="LLM Fine-tuning with LoRA &amp; QLoRA", emoji="🔧",
    character="Aishwarya", city="Pune",
    story_summary="College student fine-tunes Llama-3 on Marathi-English Q&A using LoRA on a free Colab GPU.",
    sections=[
        dict(label="Story", title="Aishwarya's Marathi Tutor Bot",
             body='''<div class="story-card"><div class="story-who">👩‍🎓 Aishwarya · Pune · Age 17</div>
<p>Aishwarya wanted to build a Marathi-English study tutor for her school's juniors. Llama-3-8B understands Marathi roughly but answers awkwardly. Full fine-tuning needs 80GB of GPU memory — way beyond Colab's free 15GB T4.</p>
<p>She discovered <strong>LoRA</strong>: train only 0.5% of the parameters, freeze the rest. With <strong>QLoRA</strong> (4-bit quantisation), she fine-tuned Llama-3-8B on a free Colab GPU in 2 hours using 1,000 Marathi Q&A pairs. The result: a tutor that explains concepts in fluent Marathi-English code-switching.</p></div>'''),
        dict(label="Why LoRA", title="The Problem with Full Fine-tuning",
             body='''<p>Llama-3-8B has 8 billion parameters. To fine-tune all of them you need to store: model weights (16GB in fp16), gradients (16GB), optimiser state (32GB for Adam) = <strong>64GB+ of GPU memory</strong>. A free Colab T4 has 15GB. An A100 80GB costs ₹150/hour.</p>
<p><strong>Insight from research (Hu et al., 2021):</strong> When you fine-tune, the weight updates have very low intrinsic rank. You can approximate the update <code>ΔW</code> as a product of two small matrices: <code>ΔW ≈ B·A</code> where <code>A</code> is <code>r×k</code> and <code>B</code> is <code>d×r</code>, with <code>r=8</code> or <code>16</code>.</p>
<div class="concept-grid">
<div class="concept-card"><h4>Full FT</h4><p>8B trainable params · 64GB VRAM · ₹150/hr A100</p></div>
<div class="concept-card"><h4>LoRA r=16</h4><p>~40M trainable (0.5%) · 18GB VRAM · 1× A10</p></div>
<div class="concept-card"><h4>QLoRA r=16</h4><p>~40M trainable + 4-bit base · 12GB VRAM · free T4</p></div>
</div>'''),
        dict(label="Code", title="Fine-tune Llama-3 with QLoRA in Colab",
             body='''<p>Install dependencies (run once in Colab):</p>
<pre><code>!pip install -q transformers peft bitsandbytes accelerate datasets trl</code></pre>
<p>Load Llama-3 in 4-bit and add LoRA adapters:</p>
<pre><code>from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="bfloat16",
    bnb_4bit_use_double_quant=True,
)

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id, quantization_config=bnb_config, device_map="auto"
)
model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: 41,943,040 || all params: 8,071,061,504 || trainable%: 0.52</code></pre>
<p>Train with TRL's SFTTrainer on Aishwarya's Marathi Q&A dataset:</p>
<pre><code>from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset

dataset = load_dataset("json", data_files="marathi_qa.jsonl", split="train")

trainer = SFTTrainer(
    model=model, tokenizer=tokenizer, train_dataset=dataset,
    dataset_text_field="text", max_seq_length=512,
    args=TrainingArguments(
        output_dir="./marathi-tutor", num_train_epochs=3,
        per_device_train_batch_size=4, gradient_accumulation_steps=4,
        learning_rate=2e-4, logging_steps=10, save_strategy="epoch",
        bf16=True, optim="paged_adamw_8bit",
    ),
)
trainer.train()
model.save_pretrained("./marathi-tutor-lora")  # only ~150 MB</code></pre>'''),
        dict(label="Inference", title="Loading and Using Your Adapter",
             body='''<pre><code>from peft import PeftModel

base = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto")
model = PeftModel.from_pretrained(base, "./marathi-tutor-lora")

prompt = "विद्यार्थी: प्रकाश संश्लेषण म्हणजे काय?\\nशिक्षक:"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
output = model.generate(**inputs, max_new_tokens=200, temperature=0.7)
print(tokenizer.decode(output[0], skip_special_tokens=True))</code></pre>
<div class="callout indigo"><strong>Tip:</strong> The LoRA adapter is just ~150MB. You can keep multiple adapters (Marathi tutor, Hindi tutor, English summariser) and swap them on the same base model. This is the foundation of multi-tenant LLM serving.</div>'''),
        dict(label="What's Next", title="Production Considerations",
             body='''<ul>
<li><strong>Evaluation:</strong> Don't trust loss numbers. Build a held-out Marathi test set with 50 questions and have a Marathi speaker rate each answer.</li>
<li><strong>Merge for serving:</strong> <code>model.merge_and_unload()</code> bakes the adapter into the base for faster inference.</li>
<li><strong>Llama license:</strong> Meta's Llama-3 community license allows commercial use up to 700M monthly users — fine for any Indian school project.</li>
<li><strong>Beware overfit:</strong> 3 epochs on 1,000 examples works. 30 epochs makes the model parrot training data and forget general knowledge.</li>
</ul>'''),
    ],
    quiz_questions=[
        dict(q="Why does Aishwarya choose LoRA over full fine-tuning for her Marathi tutor?",
             opts=dict(a="LoRA always produces higher quality models than full fine-tuning",
                       b="Full fine-tuning of Llama-3-8B requires ~64GB GPU memory which exceeds Colab's free T4 (15GB); LoRA trains only 0.5% of parameters, fitting easily in 12GB",
                       c="LoRA is the only method that supports Indian languages",
                       d="Full fine-tuning is illegal under Meta's Llama license"),
             answer="b"),
        dict(q="What is the core mathematical idea behind LoRA?",
             opts=dict(a="Replace all matrix multiplications with element-wise operations",
                       b="Approximate weight updates ΔW as a low-rank product B·A where A is r×k and B is d×r, with r much smaller than d and k",
                       c="Use Fourier transforms to compress the weight matrices",
                       d="Train the model only on the most important 1% of training data"),
             answer="b"),
        dict(q="What does QLoRA add on top of LoRA?",
             opts=dict(a="Quantum-inspired noise injection during training",
                       b="4-bit quantisation (NF4) of the frozen base model, dramatically reducing memory while still training the LoRA adapters in higher precision",
                       c="Q-learning style reward shaping during fine-tuning",
                       d="Quality-of-service guarantees for production deployment"),
             answer="b"),
        dict(q="In Aishwarya's LoraConfig, why does she target q_proj, k_proj, v_proj, o_proj?",
             opts=dict(a="Those are the only modules that PEFT library supports",
                       b="These are the attention projection matrices — empirically the highest-impact modules to adapt; touching them changes how the model attends to information",
                       c="LoRA cannot be applied to feed-forward layers due to a mathematical limitation",
                       d="These four modules collectively contain over 90% of the model's parameters"),
             answer="b"),
        dict(q="Why is the saved LoRA adapter only ~150 MB despite the base model being 16 GB?",
             opts=dict(a="The PEFT library compresses the base model alongside the adapter",
                       b="The adapter only contains the small A and B matrices (millions of parameters), not the frozen 8 billion base parameters which remain unchanged",
                       c="Hugging Face automatically removes redundant weights when saving adapters",
                       d="The adapter is stored as a delta against a publicly known checksum"),
             answer="b"),
        dict(q="If Aishwarya trains for 30 epochs instead of 3 on 1,000 Marathi examples, what is the most likely outcome?",
             opts=dict(a="The model becomes 10× more accurate because it sees the data more times",
                       b="Catastrophic overfitting — the model memorises and regurgitates training answers and loses general knowledge from pre-training",
                       c="The model converts to a different language by accident",
                       d="The training crashes because PEFT does not support more than 5 epochs"),
             answer="b"),
        dict(q="Why is paged_adamw_8bit a good optimiser choice in QLoRA training?",
             opts=dict(a="It runs natively on Apple Silicon and Intel CPUs",
                       b="It pages optimiser state between GPU and CPU memory and stores it in 8-bit, drastically reducing GPU memory use vs standard AdamW",
                       c="It is the only optimiser compatible with NF4 quantisation",
                       d="It uses pages of memory rather than continuous allocation, which improves cache hit rates"),
             answer="b"),
        dict(q="What is the most reliable way to know if Aishwarya's fine-tuned model is actually better at Marathi?",
             opts=dict(a="Compare the final training loss to the starting loss",
                       b="Build a held-out test set of ~50 Marathi questions and have a Marathi speaker rate the answers from base model vs fine-tuned model side-by-side",
                       c="Check the perplexity score on a generic English benchmark",
                       d="Count the number of Marathi tokens in the model's output vocabulary"),
             answer="b"),
    ],
    prev=None,
    next_={"href": "lesson-02.html", "label": "Lesson 2: Vector DBs &amp; RAG"},
))

# ----------------- LESSON 02 -----------------
LESSONS.append(dict(
    num=2, title="Vector Databases &amp; Production RAG", emoji="🗄️",
    character="Karthik", city="Chennai",
    story_summary="Builds a Tamil legal aid chatbot serving 5,000 queries/day with Pinecone, hybrid search and reranking.",
    sections=[
        dict(label="Story", title="Karthik's Tamil Legal Aid Chatbot",
             body='''<div class="story-card"><div class="story-who">👨‍⚖️ Karthik · Chennai · Age 17</div>
<p>Karthik volunteered with a Chennai NGO that helps daily-wage workers with legal questions in Tamil. They had 12,000 pages of Tamil legal Q&A documents. A simple ChromaDB prototype worked for 100 documents but timed out at 5,000 queries/day.</p>
<p>He rebuilt with <strong>Pinecone</strong> (managed vector DB), <strong>hybrid search</strong> (BM25 + dense embeddings), and a <strong>reranker</strong>. Result: P95 latency dropped from 4 seconds to 280ms, and answer accuracy improved from 62% to 89%.</p></div>'''),
        dict(label="Concepts", title="Why Vector Databases?",
             body='''<p>A vector database stores high-dimensional vectors (embeddings) and finds nearest neighbours in milliseconds — even across billions of vectors. The magic is the <strong>HNSW index</strong> (Hierarchical Navigable Small Worlds), which avoids comparing the query to every vector.</p>
<table>
<thead><tr><th>Vector DB</th><th>Type</th><th>Best For</th><th>Indian Cost</th></tr></thead>
<tbody>
<tr><td>ChromaDB</td><td>Embedded / Self-hosted</td><td>Prototypes, &lt;100K vectors</td><td>Free (your server)</td></tr>
<tr><td>Pinecone</td><td>Managed cloud</td><td>Production, low ops</td><td>~$70/mo starter</td></tr>
<tr><td>Weaviate</td><td>Self/managed, hybrid native</td><td>Hybrid search apps</td><td>Free OSS or $25/mo cloud</td></tr>
<tr><td>Qdrant</td><td>Self/managed, fast filters</td><td>Filtered search at scale</td><td>Free OSS or $25/mo</td></tr>
<tr><td>pgvector</td><td>Postgres extension</td><td>Apps already on Postgres</td><td>Free with your DB</td></tr>
</tbody>
</table>
<div class="callout indigo"><strong>Karthik's choice:</strong> Pinecone Starter — ₹6,000/month, zero ops, scales to 5M vectors. The NGO budget allowed it; ChromaDB self-hosted would have cost more in volunteer DevOps time.</div>'''),
        dict(label="Code", title="Build the Indexing Pipeline",
             body='''<p>Step 1 — Embed the Tamil legal documents using a multilingual model:</p>
<pre><code>from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

# Multilingual model — supports Tamil, Hindi, English natively
model = SentenceTransformer("intfloat/multilingual-e5-large")

pc = Pinecone(api_key="YOUR_KEY")
pc.create_index(
    name="tamil-legal",
    dimension=1024,  # e5-large output dim
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)
index = pc.Index("tamil-legal")</code></pre>
<p>Step 2 — Chunk and upsert (semantic chunking with overlap):</p>
<pre><code>from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
docs = []  # list of {"id", "text", "source", "law_section"}
for raw_doc in load_legal_docs("./legal_pdfs/"):
    chunks = splitter.split_text(raw_doc.text)
    for i, chunk in enumerate(chunks):
        docs.append({
            "id": f"{raw_doc.id}-{i}", "text": chunk,
            "source": raw_doc.source, "law_section": raw_doc.section,
        })

# Embed in batches of 64 to avoid OOM
batch_size = 64
for start in range(0, len(docs), batch_size):
    batch = docs[start:start+batch_size]
    texts = [f"passage: {d['text']}" for d in batch]  # e5 requires "passage:" prefix
    embeddings = model.encode(texts, normalize_embeddings=True)
    index.upsert(vectors=[
        {"id": d["id"], "values": emb.tolist(),
         "metadata": {"text": d["text"], "source": d["source"], "law_section": d["law_section"]}}
        for d, emb in zip(batch, embeddings)
    ])</code></pre>'''),
        dict(label="Code", title="Hybrid Search + Reranking",
             body='''<p>Pure dense search misses exact-match queries (e.g. "Section 138 of the Negotiable Instruments Act"). Hybrid search combines <strong>BM25</strong> (keyword) and <strong>dense embeddings</strong>:</p>
<pre><code>from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder

# BM25 index built once on all chunk texts
bm25 = BM25Okapi([d["text"].split() for d in docs])

# Reranker — small but high-precision cross-encoder
reranker = CrossEncoder("BAAI/bge-reranker-v2-m3")

def hybrid_rag(query: str, top_k: int = 5):
    # 1. Dense recall — get top 30 candidates
    q_emb = model.encode(f"query: {query}", normalize_embeddings=True).tolist()
    dense_hits = index.query(vector=q_emb, top_k=30, include_metadata=True)
    candidates = {h["id"]: h["metadata"] for h in dense_hits["matches"]}

    # 2. BM25 recall — add top 20 keyword matches
    bm25_scores = bm25.get_scores(query.split())
    top_bm25_idx = bm25_scores.argsort()[-20:][::-1]
    for idx in top_bm25_idx:
        candidates[docs[idx]["id"]] = docs[idx]

    # 3. Rerank — let the cross-encoder pick the best top_k
    pairs = [(query, c["text"]) for c in candidates.values()]
    rerank_scores = reranker.predict(pairs)
    ranked = sorted(zip(candidates.values(), rerank_scores), key=lambda x: -x[1])
    return [c for c, _ in ranked[:top_k]]</code></pre>
<p>Final step — feed top chunks to an LLM with grounded prompting:</p>
<pre><code>def answer(query: str) -> str:
    chunks = hybrid_rag(query, top_k=5)
    context = "\\n\\n".join([f"[{c['source']}, {c['law_section']}]\\n{c['text']}" for c in chunks])
    prompt = f"""You are a Tamil legal aid assistant. Answer ONLY using the context.
If the context does not contain the answer, say "என்னிடம் இந்த கேள்விக்கான தகவல் இல்லை" (I don't have information on this).
Always cite the source in [brackets].

Context:
{context}

Question: {query}
Answer in Tamil:"""
    return llm.generate(prompt)</code></pre>'''),
        dict(label="Production", title="What Made Karthik's Latency Drop 14×",
             body='''<ul>
<li><strong>Embedding cache:</strong> A Redis cache of <code>hash(query) → embedding</code> for repeated queries (legal aid users ask similar questions). Cache hit rate: 47%.</li>
<li><strong>Pre-filter by law section:</strong> Pinecone metadata filter <code>{"law_section": "labour"}</code> reduces the search space 8×.</li>
<li><strong>Async API + connection pool:</strong> FastAPI with <code>asyncio</code> + a single Pinecone client across requests.</li>
<li><strong>Reranker on GPU:</strong> The cross-encoder is small (568M params) and runs in 40ms on a T4 for 50 candidates. CPU would take 800ms.</li>
</ul>
<div class="callout green"><strong>Public good outcome:</strong> The NGO now serves 5,000+ queries per day with one volunteer engineer maintaining the system. Karthik's GitHub repo became a template for 4 other Indian legal aid NGOs.</div>'''),
    ],
    quiz_questions=[
        dict(q="What problem does an HNSW index solve in vector databases?",
             opts=dict(a="It compresses vectors to take less storage space",
                       b="It enables sub-millisecond nearest-neighbour search across millions or billions of vectors by avoiding exhaustive comparison with every stored vector",
                       c="It encrypts vectors so embeddings cannot be reverse-engineered",
                       d="It synchronises vectors across multiple geographic regions"),
             answer="b"),
        dict(q="Why does Karthik use a multilingual embedding model rather than an English-only one?",
             opts=dict(a="Multilingual models are always faster than English-only models",
                       b="His documents and user queries are in Tamil; an English-only embedding model would not place semantically similar Tamil sentences close together in vector space",
                       c="Multilingual models are required by Indian data localisation law",
                       d="English-only models cannot store more than 1024 dimensions"),
             answer="b"),
        dict(q="Why does pure dense retrieval fail for queries like 'Section 138 of the Negotiable Instruments Act'?",
             opts=dict(a="Dense models cannot encode numbers",
                       b="Exact identifiers (section numbers, code IDs, legal citations) carry critical semantic weight that dense embeddings often dilute; BM25 keyword matching catches them precisely",
                       c="Pinecone strips numerals from queries before searching",
                       d="The phrase is too long to embed"),
             answer="b"),
        dict(q="What is the role of the cross-encoder reranker in Karthik's pipeline?",
             opts=dict(a="It encrypts the retrieved chunks before sending them to the LLM",
                       b="It re-scores the top candidates from dense + BM25 retrieval using a more accurate (but slower) model that processes query and candidate together, picking the best top_k",
                       c="It translates Tamil text into English before reranking",
                       d="It removes duplicate candidates that appear in both dense and BM25 results"),
             answer="b"),
        dict(q="Why does the e5 embedding model require 'passage:' and 'query:' prefixes?",
             opts=dict(a="The prefixes are arbitrary metadata for the vector database",
                       b="The model was trained with these prefixes to produce different embeddings for the same text depending on whether it is being indexed (passage) or searched (query), improving asymmetric retrieval",
                       c="The prefixes are required by Pinecone's API",
                       d="The prefixes activate special multilingual tokens in the tokeniser"),
             answer="b"),
        dict(q="Why does the grounded prompt instruct the model to say 'I don't have information' when the context is insufficient?",
             opts=dict(a="It is a marketing requirement from the LLM provider",
                       b="To prevent hallucination — without this instruction the LLM may invent legal advice from its pre-training, which is dangerous in a legal aid context where wrong answers can harm vulnerable users",
                       c="To save tokens and reduce API costs",
                       d="To comply with Pinecone's terms of service"),
             answer="b"),
        dict(q="What does the metadata filter {'law_section': 'labour'} achieve?",
             opts=dict(a="It changes the embedding model to a labour-law-specific model",
                       b="It restricts the vector search to only chunks tagged with that law section, shrinking the search space and improving both speed and relevance",
                       c="It assigns higher weights to labour-related vectors during scoring",
                       d="It is purely cosmetic — Pinecone uses metadata only for display"),
             answer="b"),
        dict(q="What is the most important reliability lesson from Karthik's production work?",
             opts=dict(a="Always use the most expensive vector database available",
                       b="A production RAG system requires the full stack — embeddings + retrieval (dense + BM25 hybrid) + reranking + grounded prompting + caching + monitoring; missing any layer creates a different failure mode at scale",
                       c="Tamil legal questions should always be translated to English before indexing",
                       d="ChromaDB cannot be used for any production application"),
             answer="b"),
    ],
    prev={"href": "lesson-01.html", "label": "Lesson 1: LLM Fine-tuning"},
    next_={"href": "lesson-03.html", "label": "Lesson 3: Distributed Training"},
))


# ----------------- LESSON 03 -----------------
LESSONS.append(dict(
    num=3, title="Distributed Training (PyTorch DDP)", emoji="⚡",
    character="Ishaan", city="Bengaluru",
    story_summary="Speeds up training of an Indian-language sentiment model from 14 hours on 1 GPU to 2 hours on 8 GPUs using PyTorch DDP.",
    sections=[
        dict(label="Story", title="Ishaan's 14-Hour to 2-Hour Win",
             body='''<div class="story-card"><div class="story-who">👨‍💻 Ishaan · Bengaluru · Age 17</div>
<p>Ishaan was training an IndicBERT sentiment classifier on 2M Hindi+Telugu+Tamil tweets. On a single A100 GPU, one epoch took 4.7 hours. With 3 epochs needed, the experiment took 14 hours — and a single typo cost him a day.</p>
<p>His college lab had 8× A100s in one node. Using <strong>PyTorch DDP (DistributedDataParallel)</strong>, he scaled to all 8 GPUs in 12 lines of code change. Training dropped to 2 hours. Then he learned <strong>DeepSpeed ZeRO</strong> for fitting larger models that don't even fit on one GPU.</p></div>'''),
        dict(label="Why DDP", title="Data Parallel vs Model Parallel",
             body='''<div class="concept-grid">
<div class="concept-card"><h4>Data Parallel (DDP)</h4><p>Each GPU has a full model copy + a different data shard. Gradients averaged via all-reduce. Use when model fits on 1 GPU.</p></div>
<div class="concept-card"><h4>Model Parallel</h4><p>Model split across GPUs. Each GPU runs different layers. Use when model is too big for 1 GPU.</p></div>
<div class="concept-card"><h4>Tensor Parallel</h4><p>Each layer's weight matrix split across GPUs. Used inside huge LLMs (Megatron-LM).</p></div>
<div class="concept-card"><h4>Pipeline Parallel</h4><p>Layers in stages, micro-batches flow through. Reduces idle time vs naive model parallel.</p></div>
<div class="concept-card"><h4>ZeRO (DeepSpeed)</h4><p>Shards optimiser state, gradients, and parameters across GPUs. Enables huge models with little extra code.</p></div>
<div class="concept-card"><h4>FSDP (PyTorch)</h4><p>PyTorch's native ZeRO-equivalent. Recommended for new projects after PyTorch 2.0.</p></div>
</div>
<p>Ishaan's IndicBERT model is 280M parameters — fits easily on one A100 (40GB). So <strong>DDP is the right choice</strong>: 8× speedup with no engineering complexity.</p>'''),
        dict(label="Code", title="DDP in 12 Lines",
             body='''<p>Single-GPU training looks like this (simplified):</p>
<pre><code>model = IndicBERTClassifier().cuda()
loader = DataLoader(dataset, batch_size=64, shuffle=True)
opt = torch.optim.AdamW(model.parameters(), lr=2e-5)
for batch in loader:
    loss = model(batch).loss
    loss.backward(); opt.step(); opt.zero_grad()</code></pre>
<p>The DDP version — only 5 lines change:</p>
<pre><code>import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data.distributed import DistributedSampler

def train(local_rank: int, world_size: int):
    dist.init_process_group("nccl", rank=local_rank, world_size=world_size)
    torch.cuda.set_device(local_rank)

    model = IndicBERTClassifier().cuda(local_rank)
    model = DDP(model, device_ids=[local_rank])

    sampler = DistributedSampler(dataset, num_replicas=world_size, rank=local_rank)
    loader = DataLoader(dataset, batch_size=64, sampler=sampler)
    opt = torch.optim.AdamW(model.parameters(), lr=2e-5)

    for epoch in range(3):
        sampler.set_epoch(epoch)  # so shuffling differs per epoch
        for batch in loader:
            batch = {k: v.cuda(local_rank) for k, v in batch.items()}
            loss = model(**batch).loss
            loss.backward()
            opt.step(); opt.zero_grad()

    dist.destroy_process_group()</code></pre>
<p>Launch with <code>torchrun</code>:</p>
<pre><code># 1 node, 8 GPUs
torchrun --nproc_per_node=8 train_ddp.py</code></pre>'''),
        dict(label="Theory", title="What Happens Inside DDP",
             body='''<ol>
<li><strong>Replicate:</strong> Each GPU starts with an identical copy of the model.</li>
<li><strong>Shard data:</strong> <code>DistributedSampler</code> ensures each GPU sees a different subset of the batch each step.</li>
<li><strong>Forward + backward locally:</strong> Each GPU computes its own gradients on its own data shard.</li>
<li><strong>All-reduce gradients:</strong> Before <code>opt.step()</code>, NCCL averages every gradient across all 8 GPUs. After this, every GPU has identical gradients.</li>
<li><strong>Step optimiser:</strong> Each GPU applies the same optimiser update with the same gradients — so all model copies stay in sync without explicit broadcast.</li>
</ol>
<p>The genius is that all-reduce happens <strong>during</strong> the backward pass (overlapped with compute), so the only extra wall time is the slowest GPU's bandwidth.</p>
<div class="callout indigo"><strong>Effective batch size:</strong> With 8 GPUs × batch_size=64, your <em>effective</em> batch is 512. That changes the optimal learning rate. Linear scaling rule: multiply LR by world_size (so 2e-5 → 1.6e-4) — but warm up over the first epoch to avoid divergence.</div>'''),
        dict(label="Beyond DDP", title="When You Need DeepSpeed ZeRO or FSDP",
             body='''<p>If Ishaan wanted to fine-tune Llama-3-70B (140GB in fp16) on 8× A100s, no single GPU could hold the full model. ZeRO-3 / FSDP shards the model itself:</p>
<table>
<thead><tr><th>Stage</th><th>Shards</th><th>VRAM Saving</th><th>Comm Overhead</th></tr></thead>
<tbody>
<tr><td>ZeRO-1</td><td>Optimiser state</td><td>~4× (Adam)</td><td>None vs DDP</td></tr>
<tr><td>ZeRO-2</td><td>+ Gradients</td><td>~8×</td><td>Slight</td></tr>
<tr><td>ZeRO-3</td><td>+ Parameters</td><td>~N× (linear in GPUs)</td><td>~50% more</td></tr>
</tbody>
</table>
<p>FSDP API is similar — PyTorch native, recommended for new code:</p>
<pre><code>from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
model = FSDP(model, sharding_strategy=ShardingStrategy.FULL_SHARD)</code></pre>
<div class="callout green"><strong>Indian student tip:</strong> Most college labs have one node with 4–8 GPUs. DDP is enough for almost everything you'll do as a student. Save FSDP/ZeRO for when you're training a 70B+ model — usually after you join an industry team.</div>'''),
    ],
    quiz_questions=[
        dict(q="Why does Ishaan choose DistributedDataParallel (DDP) over model parallelism for his IndicBERT classifier?",
             opts=dict(a="Model parallelism is deprecated in PyTorch 2.0",
                       b="His 280M-parameter model fits comfortably on one A100 (40GB), so the simpler and faster approach is to replicate it on each GPU and shard the data — which is exactly what DDP does",
                       c="DDP supports BERT-style models while model parallel does not",
                       d="Model parallelism requires Kubernetes which is unavailable in his lab"),
             answer="b"),
        dict(q="What does the all-reduce step in DDP accomplish?",
             opts=dict(a="It synchronises model weights across GPUs by broadcasting from rank 0",
                       b="It averages gradients across all GPUs so that, after the optimiser step, every model replica applies the same update and stays identical without explicit weight broadcast",
                       c="It reduces the precision of weights from fp32 to fp16 to save memory",
                       d="It removes duplicate samples from each GPU's data shard"),
             answer="b"),
        dict(q="Why must Ishaan call sampler.set_epoch(epoch) every epoch?",
             opts=dict(a="It is required to log the current epoch to the distributed logger",
                       b="DistributedSampler uses the epoch number as a shuffle seed; without it, every epoch sees the same shard order, hurting generalisation",
                       c="It tells NCCL to switch communication backends between epochs",
                       d="It resets gradient accumulation buffers between epochs"),
             answer="b"),
        dict(q="What is the linear scaling rule for learning rate when going from 1 GPU to 8 GPUs?",
             opts=dict(a="Divide the learning rate by the number of GPUs",
                       b="Multiply the learning rate by the number of GPUs (world size), because effective batch size grew by that factor — but combine with a warmup to prevent early divergence",
                       c="Keep the learning rate the same — DDP handles scaling internally",
                       d="Square the learning rate to compensate for parallel noise reduction"),
             answer="b"),
        dict(q="When would Ishaan need to use ZeRO-3 (or FSDP) instead of plain DDP?",
             opts=dict(a="When he wants to train faster on the same model",
                       b="When the model itself is too large to fit on a single GPU — ZeRO-3 shards parameters across GPUs, enabling models like Llama-3-70B on 8× A100s",
                       c="When training data exceeds 1 TB",
                       d="When the model uses attention layers"),
             answer="b"),
        dict(q="Why is the all-reduce communication overlapped with the backward pass?",
             opts=dict(a="It is mandated by the NCCL protocol",
                       b="To hide communication latency behind useful compute — the moment one layer's gradients are ready, NCCL begins reducing them while later layers continue to compute, so the only wall time penalty is the slowest GPU's bandwidth",
                       c="It is a side effect of how PyTorch implements autograd",
                       d="It compresses gradients into smaller tensors during the backward"),
             answer="b"),
        dict(q="What does torchrun --nproc_per_node=8 do?",
             opts=dict(a="It runs the script 8 times sequentially with different random seeds",
                       b="It launches 8 worker processes on the current node, one per GPU, each receiving its own LOCAL_RANK environment variable so the training script can call dist.init_process_group correctly",
                       c="It splits the script into 8 sub-processes that share a single GPU via time-slicing",
                       d="It spawns 8 Docker containers, one per GPU"),
             answer="b"),
        dict(q="What is the most important practical lesson from Ishaan's DDP work?",
             opts=dict(a="Always use the maximum number of GPUs available regardless of model size",
                       b="DDP gives near-linear speedup with minimal code change when the model fits on one GPU; choose the simplest distributed strategy that solves your actual bottleneck — don't over-engineer with FSDP/ZeRO until you need them",
                       c="DDP requires rewriting the entire training loop in JAX",
                       d="DDP is only useful for models with more than 1 billion parameters"),
             answer="b"),
    ],
    prev={"href": "lesson-02.html", "label": "Lesson 2: Vector DBs &amp; RAG"},
    next_={"href": "lesson-04.html", "label": "Lesson 4: Graph Neural Networks"},
))

# ----------------- LESSON 04 -----------------
LESSONS.append(dict(
    num=4, title="Graph Neural Networks", emoji="🕸️",
    character="Sneha", city="Kolkata",
    story_summary="Builds a transaction-graph fraud detector that catches money-laundering rings missed by traditional rule-based systems.",
    sections=[
        dict(label="Story", title="Sneha's Fraud Detection Network",
             body='''<div class="story-card"><div class="story-who">👩‍💼 Sneha · Kolkata · Age 17</div>
<p>Sneha interned with a Kolkata fintech startup. Their UPI fraud detector used 30 hand-written rules ("flag if &gt; ₹50,000 to a new payee at 3 AM") and had a 32% false-positive rate, annoying real users.</p>
<p>The fraud team showed her a graph: nodes are accounts, edges are transactions. Fraud rings form distinctive patterns — a "fan" of small transfers into one account, then a single large outflow. Traditional ML treats each transaction independently and misses these patterns. <strong>Graph Neural Networks</strong> see the whole structure.</p>
<p>Sneha built a <strong>GraphSAGE</strong> model that reduced false positives from 32% to 9% while catching 28% more actual fraud rings.</p></div>'''),
        dict(label="Concepts", title="Why Graphs?",
             body='''<p>Many real-world problems are naturally graphs:</p>
<ul>
<li><strong>UPI fraud:</strong> accounts ↔ transactions</li>
<li><strong>Drug discovery:</strong> atoms ↔ chemical bonds</li>
<li><strong>Recommendations:</strong> users ↔ products they bought</li>
<li><strong>Knowledge graphs:</strong> entities ↔ relationships</li>
<li><strong>Indian Railways:</strong> stations ↔ train routes (delay propagation)</li>
</ul>
<p>The core operation in a GNN is <strong>message passing</strong>: each node updates its representation by aggregating information from its neighbours. Stack k layers, and each node "sees" k hops away.</p>
<div class="concept-grid">
<div class="concept-card"><h4>GCN</h4><p>Symmetric normalised aggregation. Foundational. Limited to fixed graphs.</p></div>
<div class="concept-card"><h4>GraphSAGE</h4><p>Samples a fixed-size neighbourhood. Scales to billions of nodes. Inductive (works on unseen nodes).</p></div>
<div class="concept-card"><h4>GAT</h4><p>Graph Attention — neighbours weighted by learned attention. Best when some edges matter more.</p></div>
<div class="concept-card"><h4>GIN</h4><p>Graph Isomorphism Network. Most expressive — can distinguish structurally different graphs.</p></div>
</div>'''),
        dict(label="Code", title="Build a Fraud Detector with PyTorch Geometric",
             body='''<pre><code>!pip install -q torch-geometric</code></pre>
<p>Build the transaction graph:</p>
<pre><code>import torch
from torch_geometric.data import Data

# Each account is a node with features (age_days, kyc_level, avg_balance, ...)
node_features = torch.tensor([
    [180, 2, 12000.0, 23, 0],   # account 0: 180 days old, KYC L2, ...
    [12,  1, 800.0,   45, 1],   # account 1: new, low KYC, suspicious
    # ... thousands of accounts
], dtype=torch.float)

# Edges: each transaction is a directed edge from sender to receiver
edge_index = torch.tensor([
    [0, 1, 1, 2, 3],   # source accounts
    [1, 2, 3, 4, 4],   # destination accounts
], dtype=torch.long)

# Edge features: amount, timestamp, channel
edge_attr = torch.tensor([
    [5000.0, 1700000000, 0],
    [4900.0, 1700000050, 0],
    # ...
], dtype=torch.float)

# Labels: 0 = clean, 1 = fraud (only on labelled accounts)
y = torch.tensor([0, 1, 1, 0, 0], dtype=torch.long)

graph = Data(x=node_features, edge_index=edge_index,
             edge_attr=edge_attr, y=y)</code></pre>
<p>Define the GraphSAGE classifier:</p>
<pre><code>import torch.nn.functional as F
from torch_geometric.nn import SAGEConv

class FraudGNN(torch.nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim):
        super().__init__()
        self.sage1 = SAGEConv(in_dim, hidden_dim, aggr="mean")
        self.sage2 = SAGEConv(hidden_dim, hidden_dim, aggr="mean")
        self.classifier = torch.nn.Linear(hidden_dim, out_dim)

    def forward(self, x, edge_index):
        # 1-hop neighbourhood aggregation
        h = self.sage1(x, edge_index)
        h = F.relu(h)
        h = F.dropout(h, p=0.3, training=self.training)
        # 2-hop: each node now sees neighbours-of-neighbours
        h = self.sage2(h, edge_index)
        h = F.relu(h)
        return self.classifier(h)  # logits per node</code></pre>'''),
        dict(label="Training", title="Mini-batch Training with NeighborLoader",
             body='''<p>Real fraud graphs have millions of nodes — too big to fit one batch. <code>NeighborLoader</code> samples a fixed-size neighbourhood per labelled node:</p>
<pre><code>from torch_geometric.loader import NeighborLoader

train_loader = NeighborLoader(
    graph,
    num_neighbors=[20, 10],   # 20 1-hop neighbours, 10 2-hop neighbours
    batch_size=256,
    input_nodes=train_mask,
)

model = FraudGNN(in_dim=5, hidden_dim=64, out_dim=2).cuda()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)

# Class weighting — fraud is rare (~0.5% of accounts)
class_weights = torch.tensor([1.0, 50.0]).cuda()

for epoch in range(20):
    model.train()
    for batch in train_loader:
        batch = batch.cuda()
        out = model(batch.x, batch.edge_index)
        # Predictions only for the seed nodes in the batch
        loss = F.cross_entropy(
            out[:batch.batch_size],
            batch.y[:batch.batch_size],
            weight=class_weights,
        )
        opt.zero_grad(); loss.backward(); opt.step()
    print(f"Epoch {epoch}  loss={loss.item():.4f}")</code></pre>
<div class="callout indigo"><strong>Why NeighborLoader matters:</strong> A node's 2-hop neighbourhood can have millions of nodes (high-degree hubs). Sampling caps per-batch compute and forces the model to generalise from partial neighbourhoods — the same idea that made Inception/Dropout work for CNNs.</div>'''),
        dict(label="Production", title="Deploying the Fraud Model",
             body='''<ul>
<li><strong>Inference latency:</strong> Each new transaction adds an edge. To score it, gather both accounts' k-hop neighbourhoods, run the GNN. With k=2 and degree cap 20, this is ~30ms on CPU.</li>
<li><strong>Online graph updates:</strong> Use a graph store like Neo4j or DGraph that handles streaming edge inserts. Embed-on-the-fly for new nodes via GraphSAGE's inductive nature.</li>
<li><strong>Explainability:</strong> Use <code>GNNExplainer</code> from PyG to highlight which neighbours drove the fraud prediction — auditors and regulators need this.</li>
<li><strong>Cold start:</strong> Brand-new accounts have no neighbours. Fall back to feature-only logistic regression for the first 7 days.</li>
</ul>
<div class="callout green"><strong>Sneha's outcome:</strong> 32% → 9% false positive rate. The fintech team productionised the model. Sneha's GitHub repo got 800 stars and an internship offer.</div>'''),
    ],
    quiz_questions=[
        dict(q="Why do traditional ML models miss fraud rings that GNNs catch?",
             opts=dict(a="Traditional models can't process amounts above ₹50,000",
                       b="Traditional ML treats each transaction as an independent row of features and ignores the graph structure of relationships between accounts; fraud rings are defined by their structural pattern, not individual transactions",
                       c="GNNs use newer hardware that traditional ML cannot access",
                       d="Traditional ML always overfits on imbalanced classes"),
             answer="b"),
        dict(q="What is 'message passing' in a GNN?",
             opts=dict(a="A way for nodes to send each other email-like alerts about suspicious activity",
                       b="The core operation where each node updates its representation by aggregating (e.g., averaging) feature vectors from its neighbours; stacking k layers means each node sees information from k hops away",
                       c="A network protocol used by GraphSAGE to coordinate distributed training",
                       d="A debugging mechanism that prints intermediate node states"),
             answer="b"),
        dict(q="Why does Sneha choose GraphSAGE over GCN for production fraud detection?",
             opts=dict(a="GraphSAGE always achieves higher accuracy than GCN on every benchmark",
                       b="GraphSAGE samples a fixed-size neighbourhood per node, scales to millions of nodes via mini-batching, and is inductive — it can produce embeddings for brand-new accounts not seen during training",
                       c="GCN does not support PyTorch Geometric",
                       d="GraphSAGE was specifically designed for UPI fraud by NPCI"),
             answer="b"),
        dict(q="What does the class_weights = [1.0, 50.0] argument do?",
             opts=dict(a="It scales the learning rate differently for clean vs fraud nodes",
                       b="It makes the loss function penalise misclassifying rare fraud cases 50× more than misclassifying clean accounts, counteracting the severe class imbalance (~0.5% fraud rate)",
                       c="It normalises node degrees in the message-passing aggregation",
                       d="It controls the dropout rate for fraud vs clean predictions"),
             answer="b"),
        dict(q="What problem does NeighborLoader solve?",
             opts=dict(a="It encrypts neighbour data for privacy compliance",
                       b="A node's full k-hop neighbourhood can explode to millions of nodes (especially with high-degree hubs); NeighborLoader samples a fixed number of neighbours per hop, capping per-batch compute and enabling training on huge graphs",
                       c="It removes neighbours that have already been seen in previous batches",
                       d="It loads neighbour features from disk one at a time to save RAM"),
             answer="b"),
        dict(q="Why does Sneha need GNNExplainer in production?",
             opts=dict(a="To make the model run faster on CPU",
                       b="When the model flags an account as fraud, regulators and the fraud team need to know which neighbours and edges drove the prediction; GNNExplainer highlights the influential subgraph, supporting audit and appeal processes",
                       c="To convert the model into a decision tree for serving",
                       d="To compress the model for mobile deployment"),
             answer="b"),
        dict(q="What is the cold-start problem for GNN fraud detection?",
             opts=dict(a="The model fails when training data is older than 6 months",
                       b="Brand-new accounts have no transaction edges yet, so their k-hop neighbourhoods are empty and the GNN cannot generate meaningful embeddings — fallback to feature-only models is needed for the first few days",
                       c="GPUs need to warm up for 10 minutes before serving GNN models",
                       d="The first batch of every epoch always has anomalously high loss"),
             answer="b"),
        dict(q="Why does stacking 2 SAGEConv layers help catch fraud rings?",
             opts=dict(a="Two layers always produce more accurate predictions than one",
                       b="With 2 layers each node aggregates information from neighbours-of-neighbours (2-hop) — fraud rings often span exactly 2–3 hops (sender → mule → cash-out), so 2 hops capture the structural pattern",
                       c="PyTorch Geometric requires at least 2 layers per GNN",
                       d="One layer cannot be combined with dropout"),
             answer="b"),
    ],
    prev={"href": "lesson-03.html", "label": "Lesson 3: Distributed Training"},
    next_={"href": "lesson-05.html", "label": "Lesson 5: Diffusion Models"},
))


# ----------------- LESSON 05 -----------------
LESSONS.append(dict(
    num=5, title="Diffusion Models &amp; Image Generation", emoji="🎨",
    character="Tara", city="Goa",
    story_summary="Generates Konkani folk-art posters with Stable Diffusion + ControlNet for a heritage preservation project — and learns the ethics of image generation.",
    sections=[
        dict(label="Story", title="Tara's Konkani Heritage Posters",
             body='''<div class="story-card"><div class="story-who">👩‍🎨 Tara · Goa · Age 17</div>
<p>Tara's grandmother teaches Konkani folk-art workshops. She wanted to create posters in the traditional Warli + Goan style, but custom illustrations cost ₹2,000 each. Tara fine-tuned <strong>Stable Diffusion</strong> on 200 photos of her grandmother's paintings and used <strong>ControlNet</strong> to keep the composition under her control.</p>
<p>She also learned the hard truth: image generation can be misused. Her lesson includes the safety controls she added — content filters, watermarks, and a clear "AI-generated" credit on every poster.</p></div>'''),
        dict(label="Theory", title="How Diffusion Models Work",
             body='''<p>The big idea: instead of generating an image directly (hard), train a model to <strong>remove noise</strong> from a noisy image (easier). Then start from pure noise and gradually denoise.</p>
<p><strong>Forward process:</strong> add tiny amounts of Gaussian noise over T=1000 steps until the image is pure noise. This is just math — no neural network needed.</p>
<p><strong>Reverse process:</strong> train a neural network (typically a U-Net) to predict the noise that was added at each step. At inference, start from noise and call the network 1000 (or with DDIM, just 50) times to denoise back to a clean image.</p>
<div class="concept-grid">
<div class="concept-card"><h4>DDPM</h4><p>Original diffusion. 1000 denoising steps. Slow but high quality.</p></div>
<div class="concept-card"><h4>DDIM</h4><p>Same model, deterministic schedule, 50 steps. 20× faster.</p></div>
<div class="concept-card"><h4>Latent Diffusion (SD)</h4><p>Diffuse in compressed latent space (8× smaller). Stable Diffusion's secret sauce.</p></div>
<div class="concept-card"><h4>Classifier-Free Guidance</h4><p>Sample with both conditional and unconditional model, push toward conditional. Controls prompt strength.</p></div>
</div>'''),
        dict(label="Code", title="Generate with Stable Diffusion XL",
             body='''<pre><code>!pip install -q diffusers transformers accelerate

from diffusers import StableDiffusionXLPipeline
import torch

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
).to("cuda")

prompt = "Goan Warli folk art style poster, women dancing in coconut grove, white figures on terracotta background, traditional patterns, festive"
negative_prompt = "blurry, low quality, modern style, 3d render, photograph"

image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=30,
    guidance_scale=7.5,
    height=1024, width=1024,
).images[0]
image.save("warli_poster.png")</code></pre>
<p><strong>Guidance scale</strong> controls prompt adherence. Too low (&lt;5) ignores the prompt. Too high (&gt;15) creates over-saturated, deep-fried images. 7–9 is the sweet spot.</p>'''),
        dict(label="Code", title="ControlNet for Composition Control",
             body='''<p>Pure prompt generation is unpredictable. ControlNet adds a second image (edge map, pose skeleton, depth map) that the model must follow:</p>
<pre><code>from diffusers import StableDiffusionXLControlNetPipeline, ControlNetModel
from PIL import Image
import cv2, numpy as np

# Load Tara's pencil sketch and convert to edge map
sketch = np.array(Image.open("grandmother_sketch.jpg").convert("RGB"))
edges = cv2.Canny(sketch, 100, 200)
edge_image = Image.fromarray(np.stack([edges]*3, axis=-1))

controlnet = ControlNetModel.from_pretrained(
    "diffusers/controlnet-canny-sdxl-1.0", torch_dtype=torch.float16
)
pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    controlnet=controlnet, torch_dtype=torch.float16,
).to("cuda")

image = pipe(
    prompt="Warli folk art style, traditional Goan motifs, terracotta and white",
    image=edge_image,                  # composition controlled by edges
    controlnet_conditioning_scale=0.7,
    num_inference_steps=30,
).images[0]</code></pre>
<div class="callout indigo"><strong>Why ControlNet matters:</strong> Tara's grandmother sketched the layout she wanted. ControlNet preserves that sketch's composition while filling in the artistic style. This makes the AI a collaborator, not a replacement.</div>'''),
        dict(label="Ethics", title="Safety Controls Tara Added",
             body='''<p>Image generation is powerful and dangerous. The same Stable Diffusion that paints folk art can generate harmful content. Tara built these safeguards:</p>
<ol>
<li><strong>Negative prompts:</strong> Always include <code>"nsfw, nude, child, violence, gore"</code> in negative prompts.</li>
<li><strong>Safety checker:</strong> The Hugging Face <code>StableDiffusionSafetyChecker</code> blocks NSFW outputs. Don't disable it.</li>
<li><strong>Watermark:</strong> Add a visible "AI-generated · Mitra Heritage Project" watermark to every output.</li>
<li><strong>Invisible watermark:</strong> Use <code>imwatermark</code> or Stability AI's invisible watermark to mark AI provenance even after cropping.</li>
<li><strong>No real faces:</strong> Refuse to generate identifiable people without consent. Use generic figures only.</li>
<li><strong>Source credit:</strong> Always credit "Trained on grandmother's original paintings, with permission."</li>
</ol>
<div class="callout red"><strong>Indian law context:</strong> The IT Rules 2021 (amended 2023) require deepfake-style AI content to be clearly labelled. The DPDPA 2023 prohibits processing personal data (including likenesses) without consent. Generating images of identifiable people without consent is both unethical and likely illegal.</div>
<div class="callout green"><strong>Tara's outcome:</strong> 50 posters printed for her grandmother's heritage workshop. Zero NSFW incidents. The "AI-generated, original art trained on grandmother's permission" credit became the workshop's tagline.</div>'''),
    ],
    quiz_questions=[
        dict(q="What is the core insight that makes diffusion models work?",
             opts=dict(a="Images are easier to generate when broken into 8x8 pixel blocks",
                       b="Generating an image directly is hard, but predicting the noise added at each step of a noising process is much easier; train a network to denoise, then start from pure noise and iteratively denoise to get a generated image",
                       c="Random initialisation of pixel values produces realistic images after enough training epochs",
                       d="Diffusion models replace GANs because they have no discriminator"),
             answer="b"),
        dict(q="Why does Stable Diffusion use latent diffusion instead of pixel-space diffusion?",
             opts=dict(a="Latent space is required by the licensing agreement",
                       b="Diffusing in a compressed VAE latent space (8× smaller in each dimension) cuts compute by ~64×, enabling 1024×1024 generation on a single consumer GPU instead of an entire server cluster",
                       c="Latent diffusion produces strictly higher quality than pixel diffusion",
                       d="Pixel-space diffusion is unstable and never converges"),
             answer="b"),
        dict(q="What is the role of guidance_scale (CFG) in image generation?",
             opts=dict(a="It sets the maximum image dimensions the model can generate",
                       b="Classifier-Free Guidance — at each step, sample with and without the prompt and push toward the conditional direction; higher values force closer prompt adherence but oversaturate around 12+",
                       c="It controls how many GPUs are used in parallel",
                       d="It is the random seed for the noise schedule"),
             answer="b"),
        dict(q="Why does Tara use ControlNet with an edge map of her grandmother's sketch?",
             opts=dict(a="ControlNet is required for any non-English prompt",
                       b="ControlNet conditions the generation on the structural information in the edge map, preserving the composition Tara's grandmother sketched while letting the diffusion model fill in the Warli folk-art style",
                       c="ControlNet runs faster than vanilla Stable Diffusion",
                       d="It allows generating multiple images in parallel"),
             answer="b"),
        dict(q="Why should the StableDiffusionSafetyChecker generally not be disabled in user-facing apps?",
             opts=dict(a="Disabling it voids the Apache 2.0 licence",
                       b="It blocks the most obvious NSFW outputs; disabling it removes a safety layer that protects users (especially minors) from harmful content and protects the developer from legal liability",
                       c="It is required for the model to converge during inference",
                       d="It produces higher-resolution images when enabled"),
             answer="b"),
        dict(q="Why does Tara add a visible watermark and an invisible watermark to every generated poster?",
             opts=dict(a="Watermarks improve the model's training process",
                       b="Visible watermarks prevent casual misrepresentation as human-made art; invisible watermarks (steganographic) survive cropping/screenshots and prove AI provenance — both are best practice and increasingly required by India's IT Rules and EU AI Act",
                       c="Watermarks help search engines find the images",
                       d="Hugging Face's terms of service mandate watermarks"),
             answer="b"),
        dict(q="What is the legal context in India for AI-generated images of identifiable people?",
             opts=dict(a="There are no laws that apply to AI-generated images in India",
                       b="The DPDPA 2023 prohibits processing personal data (including likenesses) without consent, and the IT Rules 2021 (2023 amendment) require synthetic media to be clearly labelled — generating images of identifiable people without consent is unethical and likely illegal",
                       c="Only commercial use of AI-generated images is regulated",
                       d="Indian law allows any AI image generation as long as it is not commercial"),
             answer="b"),
        dict(q="What is the difference between DDPM (1000 steps) and DDIM (50 steps) at inference time?",
             opts=dict(a="DDIM uses a different and incompatible model architecture",
                       b="DDIM is a deterministic sampler that uses the same trained model but a non-Markovian schedule, achieving comparable quality in ~20× fewer steps — turning interactive prompting from minutes per image to seconds per image",
                       c="DDIM produces black-and-white images only",
                       d="DDIM requires 20× more GPU memory than DDPM"),
             answer="b"),
    ],
    prev={"href": "lesson-04.html", "label": "Lesson 4: GNNs"},
    next_={"href": "lesson-06.html", "label": "Lesson 6: Speech AI &amp; Ethics"},
))

# ----------------- LESSON 06 -----------------
LESSONS.append(dict(
    num=6, title="Speech AI: TTS &amp; Voice Cloning Ethics", emoji="🎙️",
    character="Manav", city="Lucknow",
    story_summary="Builds a Hindi-Urdu audiobook generator for visually impaired students — and refuses a tempting voice-cloning offer.",
    sections=[
        dict(label="Story", title="Manav's Audiobook Project (and the Offer He Refused)",
             body='''<div class="story-card"><div class="story-who">👨‍🎤 Manav · Lucknow · Age 17</div>
<p>Manav volunteered with a Lucknow school for visually impaired students. The school's textbooks weren't available as audiobooks in Hindi-Urdu mix. He used <strong>Coqui TTS</strong> with the IndicTTS Hindi voices to generate 80 hours of textbook audio over a weekend.</p>
<p>A YouTube creator then offered him ₹15,000 to clone a famous actress's voice from public interviews so the creator could "make her say whatever I want." Manav refused. The lesson covers both the technology and why he said no.</p></div>'''),
        dict(label="Tech", title="How Modern TTS Works",
             body='''<p>Modern TTS is two stages:</p>
<ol>
<li><strong>Text → Mel-spectrogram:</strong> A model (Tacotron2, FastSpeech2, or VITS encoder) converts text to a 2D representation of frequency over time.</li>
<li><strong>Spectrogram → Audio waveform:</strong> A vocoder (HiFi-GAN, WaveRNN, or VITS decoder) converts the spectrogram to actual sound samples (22050 Hz audio).</li>
</ol>
<p><strong>VITS</strong> combines both stages end-to-end — better quality, simpler pipeline. It's what most current open-source TTS uses.</p>
<table>
<thead><tr><th>System</th><th>Quality (MOS)</th><th>Latency</th><th>Indian Languages</th></tr></thead>
<tbody>
<tr><td>Coqui XTTS-v2</td><td>4.2 / 5</td><td>200ms</td><td>17 langs incl. Hindi</td></tr>
<tr><td>IndicTTS (AI4Bharat)</td><td>4.0 / 5</td><td>150ms</td><td>13 Indian langs</td></tr>
<tr><td>Bark</td><td>4.1 / 5</td><td>5–8s</td><td>Multi-lingual</td></tr>
<tr><td>Google Cloud TTS</td><td>4.4 / 5</td><td>100ms</td><td>14 Indian langs</td></tr>
<tr><td>ElevenLabs</td><td>4.6 / 5</td><td>250ms</td><td>Limited Indian</td></tr>
</tbody>
</table>'''),
        dict(label="Code", title="Generate Hindi Audiobook with Coqui XTTS",
             body='''<pre><code>!pip install -q TTS

from TTS.api import TTS
import os

# XTTS v2 — multilingual, supports Hindi
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

def text_to_audiobook(chapter_path: str, output_path: str, lang: str = "hi"):
    """Convert one chapter file to an MP3 audiobook segment."""
    with open(chapter_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Chunk by sentence to avoid memory blow-up on long text
    sentences = [s.strip() for s in text.split("।") if s.strip()]
    audio_segments = []
    for i, sentence in enumerate(sentences):
        wav = tts.tts(
            text=sentence,
            language=lang,
            speaker_wav="reference_voice.wav",  # 6-second clip of approved voice
        )
        audio_segments.append(wav)
        if i % 10 == 0:
            print(f"  {i}/{len(sentences)} sentences synthesised")

    # Concatenate and save
    import numpy as np
    full_audio = np.concatenate(audio_segments)
    tts.synthesizer.save_wav(full_audio, output_path)

# Generate the whole textbook
for chapter in os.listdir("./hindi_textbook/"):
    text_to_audiobook(
        chapter_path=f"./hindi_textbook/{chapter}",
        output_path=f"./audiobook/{chapter.replace('.txt', '.wav')}",
        lang="hi",
    )</code></pre>'''),
        dict(label="Ethics", title="The Voice-Cloning Refusal",
             body='''<p>The same XTTS model that read Manav's textbooks can clone any voice from a 6-second sample. That's the offer he received — clone a celebrity voice without consent. Why he refused:</p>
<div class="callout red"><strong>Legal risks (India):</strong>
<ul>
<li><strong>Personality rights:</strong> Indian courts (Anil Kapoor v. Simply Life India, 2023) recognise a celebrity's right to control their voice and likeness. Cloning without consent invites injunctions and damages.</li>
<li><strong>IT Rules 2021 + 2023 amendment:</strong> Synthetic media impersonating real people must be clearly labelled. Defamation via deepfake is criminal under IPC §499/500.</li>
<li><strong>DPDPA 2023:</strong> Voice is biometric/personal data. Processing it (training a clone) without consent violates the Act.</li>
</ul></div>
<div class="callout indigo"><strong>Manav's principles for voice synthesis:</strong>
<ol>
<li>Only synthesise voices with explicit, written consent of the speaker.</li>
<li>Never imitate a real, named person without their permission.</li>
<li>Always announce "This is an AI-generated voice" at the start of synthesised audio.</li>
<li>Add an inaudible watermark (e.g., AudioSeal) for provenance.</li>
<li>Reject any request that involves making someone "say something they didn't say".</li>
</ol></div>
<p>For the audiobook project, the school had a teacher record 30 minutes of speech and signed a consent form. Manav used that as the reference voice. The students and parents knew the voice was synthetic and consented to its use.</p>
<div class="callout green"><strong>Outcome:</strong> 80 hours of Hindi-Urdu audiobooks for 200+ visually impaired students. The teacher whose voice was used became a local celebrity. The YouTube creator went elsewhere — and Manav's principles became the school's official AI policy.</div>'''),
        dict(label="Detection", title="Detecting Voice Deepfakes",
             body='''<p>The other side of TTS is detection. Open-source detectors that work in 2026:</p>
<ul>
<li><strong>AASIST:</strong> Audio Anti-Spoofing using Integrated Spectro-Temporal graph attention. Best open-source detector.</li>
<li><strong>RawNet3:</strong> Lightweight detector that runs on CPU.</li>
<li><strong>AudioSeal (Meta):</strong> Watermark embedded in TTS output, recoverable even after re-recording.</li>
</ul>
<pre><code>from speechbrain.pretrained import SpeakerRecognition
verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

# Compare suspect audio to known real samples of the speaker
score, prediction = verification.verify_files(
    "real_speaker_sample.wav", "suspect_audio.wav"
)
print(f"Same speaker probability: {score.item():.3f}")</code></pre>
<p>Detection is an arms race. The right defence is provenance (watermarks + signed metadata) plus media literacy, not detection alone.</p>'''),
    ],
    quiz_questions=[
        dict(q="What are the two stages of modern TTS?",
             opts=dict(a="Recording and editing",
                       b="Text → Mel-spectrogram (acoustic model like Tacotron2/FastSpeech2/VITS-encoder), then spectrogram → audio waveform (vocoder like HiFi-GAN/WaveRNN/VITS-decoder)",
                       c="Translation and synthesis",
                       d="Compression and encryption"),
             answer="b"),
        dict(q="Why does Manav refuse the celebrity voice-cloning offer?",
             opts=dict(a="The technology is too difficult and would take months",
                       b="It violates Indian personality rights (Anil Kapoor v. Simply Life India, 2023), the IT Rules 2021 synthetic-media labelling requirement, the DPDPA 2023 (voice is biometric data), and basic ethics — making someone 'say what they didn't say' is impersonation",
                       c="The Coqui licence forbids any voice cloning",
                       d="The offered payment is too low"),
             answer="b"),
        dict(q="Why does the school audiobook project not raise the same ethical issues?",
             opts=dict(a="School projects are exempt from voice-cloning law",
                       b="The teacher whose voice was used gave written, informed consent; students and parents knew the voice was synthetic; and the use is for an accessibility purpose, not impersonation — these conditions make the use ethical and legal",
                       c="Audiobooks are exempt from the IT Rules synthetic media provisions",
                       d="The teacher does not have personality rights because she is not a celebrity"),
             answer="b"),
        dict(q="What does VITS do differently from a Tacotron2 + HiFi-GAN pipeline?",
             opts=dict(a="VITS only supports English",
                       b="VITS combines acoustic model and vocoder into a single end-to-end network trained jointly with a variational objective — simpler pipeline, fewer cascading errors, and typically higher quality",
                       c="VITS uses transformer-only architecture without convolutions",
                       d="VITS requires 10× more training data than Tacotron2"),
             answer="b"),
        dict(q="Why is detection alone an insufficient defence against voice deepfakes?",
             opts=dict(a="Detection models are illegal to deploy in India",
                       b="Detection is an arms race — every new detector quickly faces a generator that defeats it; the right defence stack is provenance (watermarks + signed metadata) + clear labelling + media literacy education, with detection as one layer",
                       c="Detection requires more GPU memory than generation",
                       d="Detection only works on English audio"),
             answer="b"),
        dict(q="What is AudioSeal and why does it matter?",
             opts=dict(a="It is a hardware device that physically marks audio recordings",
                       b="An open-source watermarking method by Meta that embeds an inaudible watermark in TTS output; the watermark is recoverable even after MP3 compression and re-recording, providing provenance proof that the audio was AI-generated",
                       c="It encrypts audio so only authorised users can play it",
                       d="It is the legal name of India's anti-deepfake law"),
             answer="b"),
        dict(q="Why does Manav chunk the textbook by sentence (split on '।') before synthesis?",
             opts=dict(a="The Coqui API rejects inputs longer than 100 characters",
                       b="Long text inputs cause GPU OOM and quality degradation in TTS models; chunking at sentence boundaries (the Devanagari full stop '।') gives natural prosody breaks and fits each chunk in memory",
                       c="It allows the audio to be played in parallel",
                       d="It is required to convert Devanagari to ASCII"),
             answer="b"),
        dict(q="What single principle from Manav's checklist should every student building voice-AI systems adopt?",
             opts=dict(a="Always use the highest-quality voice available",
                       b="Only synthesise voices with explicit, written consent from the speaker — and never imitate a real, named person without their permission. This single rule prevents almost every harmful voice-AI use case",
                       c="Always use a paid TTS service rather than open-source",
                       d="Always upload generated audio to a public server for transparency"),
             answer="b"),
    ],
    prev={"href": "lesson-05.html", "label": "Lesson 5: Diffusion Models"},
    next_={"href": "lesson-07.html", "label": "Lesson 7: Recommender Systems"},
))


# ----------------- LESSON 07 -----------------
LESSONS.append(dict(
    num=7, title="Recommender Systems at Scale", emoji="🎯",
    character="Priya", city="Hyderabad",
    story_summary="Builds a Telugu film recommender for a regional OTT startup using collaborative filtering and a two-tower neural model.",
    sections=[
        dict(label="Story", title="Priya's Telugu OTT Recommender",
             body='''<div class="story-card"><div class="story-who">👩‍💻 Priya · Hyderabad · Age 17</div>
<p>Priya interned at a Hyderabad startup building a Telugu-first OTT app. Their original "trending" feed showed everyone the same 20 films. Engagement was 4 minutes/day. After Priya built a personalised recommender, engagement grew to 19 minutes/day in 8 weeks.</p>
<p>She started with simple collaborative filtering, hit cold-start problems, then built a <strong>two-tower neural model</strong> that handled new users (cold-start) and scaled to 200K users + 8K films.</p></div>'''),
        dict(label="Concepts", title="The Recommender Toolbox",
             body='''<div class="concept-grid">
<div class="concept-card"><h4>Popularity</h4><p>Show the trending. No personalisation. The baseline. Beats nothing personalised.</p></div>
<div class="concept-card"><h4>Collaborative Filtering</h4><p>"Users who liked X also liked Y." Works when you have ratings. Cold-start fails.</p></div>
<div class="concept-card"><h4>Matrix Factorisation</h4><p>Decompose user-item matrix into latent factors. SVD/ALS/NMF. The classic.</p></div>
<div class="concept-card"><h4>Content-Based</h4><p>Recommend items similar in features (genre, cast, language). Works for new items.</p></div>
<div class="concept-card"><h4>Two-Tower Neural</h4><p>One tower encodes users, one encodes items. Both share an embedding space. Scales to billions.</p></div>
<div class="concept-card"><h4>Transformer-based</h4><p>Sequence of past interactions → next-item prediction. State of the art (SASRec, BERT4Rec).</p></div>
</div>'''),
        dict(label="Code", title="Two-Tower Neural Recommender",
             body='''<pre><code>import torch
import torch.nn as nn
import torch.nn.functional as F

class TwoTowerRecommender(nn.Module):
    """User tower + Item tower → cosine similarity in shared 64-dim space."""

    def __init__(self, num_users, num_items, num_genres, num_languages, dim=64):
        super().__init__()
        # User features: ID + age_bucket + city + watch_history (last 10 items)
        self.user_id_emb = nn.Embedding(num_users, 32)
        self.age_emb = nn.Embedding(8, 8)            # 8 age buckets
        self.city_emb = nn.Embedding(50, 16)         # 50 cities
        self.history_emb = nn.Embedding(num_items + 1, 32, padding_idx=0)
        self.user_mlp = nn.Sequential(
            nn.Linear(32 + 8 + 16 + 32, 128), nn.ReLU(),
            nn.Dropout(0.2), nn.Linear(128, dim),
        )
        # Item features: ID + genre + language + release_year_bucket
        self.item_id_emb = nn.Embedding(num_items, 32)
        self.genre_emb = nn.Embedding(num_genres, 16)
        self.lang_emb = nn.Embedding(num_languages, 8)
        self.year_emb = nn.Embedding(10, 8)
        self.item_mlp = nn.Sequential(
            nn.Linear(32 + 16 + 8 + 8, 128), nn.ReLU(),
            nn.Dropout(0.2), nn.Linear(128, dim),
        )

    def encode_user(self, user_id, age, city, history):
        history_avg = self.history_emb(history).mean(dim=1)  # avg of last 10 items
        x = torch.cat([self.user_id_emb(user_id), self.age_emb(age),
                       self.city_emb(city), history_avg], dim=-1)
        return F.normalize(self.user_mlp(x), dim=-1)

    def encode_item(self, item_id, genre, lang, year):
        x = torch.cat([self.item_id_emb(item_id), self.genre_emb(genre),
                       self.lang_emb(lang), self.year_emb(year)], dim=-1)
        return F.normalize(self.item_mlp(x), dim=-1)

    def forward(self, user_inputs, item_inputs):
        u = self.encode_user(*user_inputs)
        v = self.encode_item(*item_inputs)
        return (u * v).sum(dim=-1)  # cosine similarity (since both normalised)</code></pre>'''),
        dict(label="Code", title="Train with Sampled Softmax (Negative Sampling)",
             body='''<pre><code>def train_step(model, batch, num_negatives=4):
    """For each positive (user, item) pair, sample N random items as negatives."""
    user_inputs = batch["user"]   # (user_id, age, city, history)
    pos_item = batch["pos_item"]  # (item_id, genre, lang, year)

    # Sample negatives uniformly (or proportional to popularity^0.75)
    batch_size = pos_item[0].size(0)
    neg_ids = torch.randint(0, num_items, (batch_size, num_negatives))
    neg_items = (neg_ids,
                 item_genre_table[neg_ids],
                 item_lang_table[neg_ids],
                 item_year_table[neg_ids])

    pos_score = model(user_inputs, pos_item)  # (B,)
    # Encode all negatives in one go
    u = model.encode_user(*user_inputs).unsqueeze(1)         # (B, 1, dim)
    v_neg = model.encode_item(*neg_items)                    # (B, N, dim)
    neg_scores = (u * v_neg).sum(dim=-1)                     # (B, N)

    logits = torch.cat([pos_score.unsqueeze(1), neg_scores], dim=1)  # (B, 1+N)
    targets = torch.zeros(batch_size, dtype=torch.long, device=logits.device)
    return F.cross_entropy(logits, targets)</code></pre>
<p>At inference, encode all 8K films into a FAISS index once, then for each user encode the user vector and look up top-K nearest films in &lt;5ms.</p>'''),
        dict(label="Production", title="Cold Start, Diversity, and Filter Bubbles",
             body='''<ul>
<li><strong>Cold-start users:</strong> A new user has no history. Use age + city + onboarding genre selection. The two-tower model handles this naturally — user_id_emb with random init combined with strong age/city/genre signals.</li>
<li><strong>Cold-start items:</strong> A new film has no views. Use content features (genre, language, cast, plot embedding). Re-train item embeddings nightly.</li>
<li><strong>Diversity:</strong> Top-K by score gives 10 nearly identical action films. Use Maximal Marginal Relevance (MMR) or determinantal point processes to enforce variety.</li>
<li><strong>Filter bubbles:</strong> Always inject 1–2 random "exploration" items in every list of 10. Track engagement to learn from new patterns.</li>
<li><strong>Negative feedback:</strong> Track skips and "Not Interested" — these are stronger signals than weak positives like watch-1-minute.</li>
</ul>
<div class="callout indigo"><strong>Ethics for OTT recommenders:</strong>
<ul>
<li>Allow "show me everything chronologically" — let users opt out of personalisation.</li>
<li>Don't recommend extreme/harmful content even if engagement is high.</li>
<li>Make the "Why am I seeing this?" explanation accessible (e.g., "Because you watched X").</li>
</ul></div>
<div class="callout green"><strong>Priya's outcome:</strong> Engagement 4 → 19 min/day. The startup raised a Series A based on the engagement metric. Priya kept her summer internship and is now building the next iteration: a transformer-based sequential model (SASRec).</div>'''),
    ],
    quiz_questions=[
        dict(q="Why does popularity-based 'trending' work poorly for personalisation?",
             opts=dict(a="Trending lists are always wrong",
                       b="It shows everyone the same 20 items, so it cannot capture individual taste — a Telugu user who only watches romance gets the same feed as a comedy fan, hurting engagement and retention",
                       c="Trending requires expensive computation",
                       d="Trending lists violate privacy laws"),
             answer="b"),
        dict(q="What problem does collaborative filtering have that the two-tower model solves?",
             opts=dict(a="Collaborative filtering does not support GPU acceleration",
                       b="Collaborative filtering cannot handle cold-start (new users with no history); the two-tower model uses side features (age, city, genre preferences from onboarding) so it can produce reasonable recommendations on day 1",
                       c="Collaborative filtering only works for English content",
                       d="Collaborative filtering has been deprecated by FAISS"),
             answer="b"),
        dict(q="Why does the two-tower architecture put the user encoder and item encoder in separate towers?",
             opts=dict(a="It runs faster because the towers can be trained on different GPUs",
                       b="At serving time you precompute and FAISS-index all item embeddings once; for each query you only encode the user and do a fast nearest-neighbour search — this scales to billions of items, which a single combined model cannot",
                       c="Two-tower is required by the recommender system patent",
                       d="It allows the model to handle multiple languages"),
             answer="b"),
        dict(q="Why does training use negative sampling (sampled softmax) instead of computing softmax over all 8,000 films?",
             opts=dict(a="Negative sampling produces strictly higher accuracy",
                       b="Computing the full softmax over every item per batch is prohibitively expensive at scale; sampling 4–10 negatives per positive gives an unbiased gradient estimate at a fraction of the cost — the standard scaling trick from word2vec",
                       c="Negative sampling is required for cosine similarity to work",
                       d="The 8,000 films cannot fit in GPU memory simultaneously"),
             answer="b"),
        dict(q="Why does Priya inject 1–2 random 'exploration' items into every list of 10?",
             opts=dict(a="To slow down the algorithm and reduce server load",
                       b="To break filter bubbles and continually gather signal on items the user might like but the model doesn't yet know about; pure exploitation collapses the recommendation space and causes engagement decay over time",
                       c="To meet a regulatory requirement for randomness",
                       d="Because the model has bugs that random items mask"),
             answer="b"),
        dict(q="Why are explicit 'Not Interested' clicks more valuable than 1-minute watches?",
             opts=dict(a="Skip data is required by Indian law to be tracked",
                       b="A 'Not Interested' click is a clear, intentional negative signal; a 1-minute watch is ambiguous (interrupted? pre-roll? reading subtitles?) — clear labels train better models",
                       c="Skips happen more frequently than watches in the dataset",
                       d="The OTT platform pays content owners only on long watches"),
             answer="b"),
        dict(q="Why does Priya use F.normalize on both user and item embeddings before computing the dot product?",
             opts=dict(a="Normalisation is required by PyTorch when using two-tower models",
                       b="Normalising both vectors to unit length means the dot product equals cosine similarity, which is bounded in [-1, 1] and behaves well for ranking and FAISS retrieval; unnormalised dot products are dominated by vector magnitudes and skew rankings toward popular items",
                       c="It reduces GPU memory by half",
                       d="It is the only way to combine user and item features"),
             answer="b"),
        dict(q="What is the most important ethical principle Priya applies to her recommender?",
             opts=dict(a="Always recommend content with the highest predicted watch time",
                       b="Engagement optimisation has guardrails: allow users to opt out of personalisation, refuse to amplify extreme/harmful content even when engaging, and make 'Why am I seeing this?' easy to access — engagement at any cost causes long-term harm to users and to the business",
                       c="Always show items in alphabetical order to be fair",
                       d="Recommend only content from the user's home state"),
             answer="b"),
    ],
    prev={"href": "lesson-06.html", "label": "Lesson 6: Speech AI"},
    next_={"href": "lesson-08.html", "label": "Lesson 8: AI at Scale"},
))

# ----------------- LESSON 08 -----------------
LESSONS.append(dict(
    num=8, title="AI at Scale: Kubernetes + vLLM", emoji="🚢",
    character="Rohit", city="Mumbai",
    story_summary="Serves a 7B Llama-3 model to 50,000 daily users with vLLM on Kubernetes — at 1/8th the cost of OpenAI.",
    sections=[
        dict(label="Story", title="Rohit's ₹40,000/month LLM Service",
             body='''<div class="story-card"><div class="story-who">👨‍💻 Rohit · Mumbai · Age 17</div>
<p>Rohit's school built a Hindi study chatbot. Using OpenAI GPT-3.5 for 50,000 daily students cost ₹3.2 lakhs/month — unaffordable. Rohit migrated to a self-hosted Llama-3-8B served with <strong>vLLM</strong> on a single A10 GPU rented for ₹40,000/month from an Indian cloud provider (Yotta or E2E).</p>
<p>The service handles 50,000 daily users with P99 latency of 1.4 seconds. The trick: vLLM's <strong>PagedAttention</strong> + continuous batching gets 14× more throughput than naive HuggingFace serving.</p></div>'''),
        dict(label="Why vLLM", title="The Throughput Problem",
             body='''<p>Naive LLM serving allocates a contiguous KV-cache slot per request, sized for the worst case (max output length). Most requests use a fraction of it. Result: 60–80% of GPU memory is wasted, and you can only batch 8–16 concurrent requests on an A10 GPU.</p>
<p><strong>vLLM's two innovations:</strong></p>
<div class="concept-grid">
<div class="concept-card"><h4>PagedAttention</h4><p>Treats KV-cache like virtual memory pages. Allocates blocks on demand. Memory waste &lt; 4%. Supports 5–10× more concurrent requests.</p></div>
<div class="concept-card"><h4>Continuous Batching</h4><p>Doesn't wait for all requests in a batch to finish. As soon as one request completes, a new one slots in. GPU stays busy.</p></div>
</div>
<table>
<thead><tr><th>Server</th><th>Throughput (tok/s)</th><th>Concurrent Requests</th><th>Setup</th></tr></thead>
<tbody>
<tr><td>HF Transformers</td><td>~600</td><td>4–8</td><td>1 line</td></tr>
<tr><td>HF TGI</td><td>~3,500</td><td>32</td><td>Docker</td></tr>
<tr><td>vLLM</td><td>~9,000</td><td>128+</td><td>Docker + config</td></tr>
<tr><td>SGLang / TensorRT-LLM</td><td>~12,000</td><td>128+</td><td>Complex setup</td></tr>
</tbody>
</table>'''),
        dict(label="Code", title="Run vLLM in 3 Commands",
             body='''<pre><code># 1. Start vLLM server with Llama-3-8B
docker run --gpus all -p 8000:8000 \\
  -v ~/.cache/huggingface:/root/.cache/huggingface \\
  vllm/vllm-openai:latest \\
  --model meta-llama/Meta-Llama-3-8B-Instruct \\
  --max-model-len 4096 \\
  --gpu-memory-utilization 0.92</code></pre>
<p>vLLM exposes an OpenAI-compatible API. Existing OpenAI client code works with one line change:</p>
<pre><code>from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="dummy",  # vLLM doesn't check keys by default
)

response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    messages=[
        {"role": "system", "content": "You are a Hindi study tutor."},
        {"role": "user", "content": "प्रकाश संश्लेषण समझाइए"},
    ],
    temperature=0.7,
    max_tokens=400,
)
print(response.choices[0].message.content)</code></pre>'''),
        dict(label="Code", title="Kubernetes Deployment with Autoscaling",
             body='''<pre><code># vllm-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-llama3
spec:
  replicas: 2
  selector:
    matchLabels: {app: vllm}
  template:
    metadata:
      labels: {app: vllm}
    spec:
      nodeSelector:
        nvidia.com/gpu.product: NVIDIA-A10
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        args:
        - --model=meta-llama/Meta-Llama-3-8B-Instruct
        - --max-model-len=4096
        - --gpu-memory-utilization=0.92
        ports: [{containerPort: 8000}]
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: "32Gi"
        readinessProbe:
          httpGet: {path: /health, port: 8000}
          initialDelaySeconds: 120  # vLLM takes ~2 min to load 8B model
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vllm-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vllm-llama3
  minReplicas: 1
  maxReplicas: 4
  metrics:
  - type: Pods
    pods:
      metric: {name: vllm_requests_running}
      target: {type: AverageValue, averageValue: "60"}</code></pre>
<pre><code>kubectl apply -f vllm-deployment.yaml
kubectl get pods -l app=vllm
# vllm-llama3-7c6f4d89b8-x2k4p  Running</code></pre>
<div class="callout indigo"><strong>Indian cloud tip:</strong> Yotta, E2E, and Tata Cloud all offer A10/L40 GPUs at 30–50% lower price than AWS for Indian-hosted workloads. Data localisation under DPDPA 2023 also favours Indian infrastructure for student data.</div>'''),
        dict(label="Cost", title="The Economics — Why Self-Hosting Wins at Scale",
             body='''<table>
<thead><tr><th>Approach</th><th>Cost / Month</th><th>50K daily users</th></tr></thead>
<tbody>
<tr><td>OpenAI GPT-3.5</td><td>~₹3.2 lakh</td><td>Pay-per-token, scales linearly</td></tr>
<tr><td>OpenAI GPT-4o</td><td>~₹12 lakh</td><td>Higher quality, much higher cost</td></tr>
<tr><td>vLLM Llama-3-8B (1× A10)</td><td>~₹40,000</td><td>Self-hosted, fixed cost</td></tr>
<tr><td>vLLM Llama-3-70B (4× A100)</td><td>~₹3.5 lakh</td><td>GPT-4-class quality at GPT-3.5 price</td></tr>
</tbody>
</table>
<div class="callout green"><strong>Crossover point:</strong> Self-hosting wins when you have ~5,000+ daily active users. Below that, OpenAI / Anthropic / Google APIs are cheaper because the GPU sits idle most of the time. Don't self-host prematurely.</div>
<div class="callout red"><strong>Operational reality:</strong> Self-hosting requires DevOps capability — GPU monitoring, autoscaling, model upgrades, security patches. Budget 0.25 FTE engineering time. Below that, the API price is worth it.</div>'''),
    ],
    quiz_questions=[
        dict(q="What problem does PagedAttention solve in LLM serving?",
             opts=dict(a="It speeds up the matrix multiplications inside attention",
                       b="Naive serving allocates a worst-case-sized contiguous KV cache per request, wasting 60-80% of GPU memory; PagedAttention treats KV cache like virtual-memory pages allocated on demand, reducing waste to under 4% and enabling 5-10× more concurrent requests",
                       c="It removes the attention mechanism entirely",
                       d="It encrypts the KV cache for privacy"),
             answer="b"),
        dict(q="What is continuous batching in vLLM?",
             opts=dict(a="A scheduling policy that batches all requests every 10 milliseconds",
                       b="The scheduler doesn't wait for every request in a batch to finish — as soon as one completes, a new request slots into its place; the GPU stays continuously busy instead of idling on the slowest request",
                       c="A way to batch training and inference workloads on the same GPU",
                       d="A continuous integration test that runs each batch through CI"),
             answer="b"),
        dict(q="Why does Rohit use the OpenAI-compatible API exposed by vLLM?",
             opts=dict(a="It is the only API that vLLM supports",
                       b="OpenAI's chat completions API is the de-facto standard; vLLM exposing the same interface means the existing chatbot code works with a single base_url change — zero rewrite, easy migration back to OpenAI if needed",
                       c="OpenAI requires it for licensing reasons",
                       d="The OpenAI API is the only one that supports Hindi"),
             answer="b"),
        dict(q="Why does Rohit's HorizontalPodAutoscaler scale on vllm_requests_running rather than CPU usage?",
             opts=dict(a="CPU metrics are not exposed by Kubernetes for GPU pods",
                       b="LLM workloads are GPU-bound — CPU usage stays low even at full GPU saturation; vLLM exposes a queue-depth metric that actually tracks load and is the right scaling signal",
                       c="The pods do not have CPU limits set",
                       d="Memory is the only meaningful metric for LLMs"),
             answer="b"),
        dict(q="Why does the readiness probe have initialDelaySeconds: 120?",
             opts=dict(a="It is a Kubernetes-imposed minimum",
                       b="vLLM takes ~2 minutes to download (if not cached) and load the 8B-parameter model into GPU memory and warm up CUDA kernels; serving health checks before that period would mark the pod ready prematurely",
                       c="The Llama license requires a 2-minute waiting period",
                       d="Kubernetes garbage collection runs every 120 seconds"),
             answer="b"),
        dict(q="At what scale does self-hosting an LLM with vLLM become cheaper than OpenAI's API?",
             opts=dict(a="Self-hosting is always cheaper than any API",
                       b="Approximately 5,000+ daily active users — below that, the GPU sits idle most of the time and pay-per-token APIs win on cost; above that, fixed self-hosted infrastructure becomes much cheaper per query",
                       c="Self-hosting is never cheaper because of DevOps overhead",
                       d="At 100 users per day"),
             answer="b"),
        dict(q="Why is gpu-memory-utilization=0.92 a good default for vLLM?",
             opts=dict(a="0.92 is the maximum value vLLM accepts",
                       b="vLLM pre-allocates 92% of GPU memory for KV cache + model weights; leaving 8% headroom prevents OOM crashes from temporary spikes (long prompts, beam search) while maximising concurrent request capacity",
                       c="It matches the recommended ratio in NVIDIA's CUDA documentation",
                       d="92% is the average utilisation seen in production"),
             answer="b"),
        dict(q="What hidden cost does Rohit's lesson warn about with self-hosting?",
             opts=dict(a="Electricity bills become prohibitively expensive",
                       b="DevOps engineering time — GPU monitoring, autoscaling, model upgrades, security patches require ~0.25 FTE; teams without that capability should pay for the API even if the per-request cost is higher, because operational outages cost more than savings",
                       c="GPU drivers must be re-licensed monthly",
                       d="Indian cloud providers do not offer A10 GPUs"),
             answer="b"),
    ],
    prev={"href": "lesson-07.html", "label": "Lesson 7: Recommender Systems"},
    next_={"href": "lesson-09.html", "label": "Lesson 9: Time Series"},
))


# ----------------- LESSON 09 -----------------
LESSONS.append(dict(
    num=9, title="Time Series Forecasting", emoji="📈",
    character="Anjali", city="Delhi",
    story_summary="Forecasts demand for her family's Delhi sweet shop using Prophet and N-BEATS — and saves ₹3 lakh in wasted inventory.",
    sections=[
        dict(label="Story", title="Anjali's Mithai Shop Forecast",
             body='''<div class="story-card"><div class="story-who">👩‍💼 Anjali · Delhi · Age 17</div>
<p>Anjali's family runs a sweet shop in Karol Bagh. They threw away ₹40,000 of unsold mithai every month — and ran out of besan ladoo on Diwali two years running. Anjali built a forecasting system using <strong>Prophet</strong> (with Indian holidays) and <strong>N-BEATS</strong>.</p>
<p>Eight months later: waste down to ₹3,000/month, zero stockouts on festivals, and her father uses the dashboard daily. Total saving: ~₹3 lakhs/year.</p></div>'''),
        dict(label="Theory", title="Components of a Time Series",
             body='''<p>Every time series can be decomposed into three signals:</p>
<ol>
<li><strong>Trend:</strong> The long-term direction. Anjali's shop grew 8% YoY.</li>
<li><strong>Seasonality:</strong> Repeating patterns. Weekly (weekend spike), yearly (Diwali, Holi, Karva Chauth), and even hourly.</li>
<li><strong>Residual:</strong> What's left after removing trend + seasonality. Often modelled as noise or with autoregression.</li>
</ol>
<table>
<thead><tr><th>Method</th><th>When to Use</th><th>Pros</th><th>Cons</th></tr></thead>
<tbody>
<tr><td>ARIMA</td><td>Short series, simple seasonality</td><td>Interpretable, classic</td><td>Manual order tuning</td></tr>
<tr><td>Prophet</td><td>Daily data with holidays</td><td>Auto-tunes, handles holidays</td><td>Limited features</td></tr>
<tr><td>N-BEATS</td><td>Long series, complex patterns</td><td>SOTA accuracy, no feature engineering</td><td>Less interpretable</td></tr>
<tr><td>TFT (Temporal Fusion Transformer)</td><td>Multi-variate, multi-horizon</td><td>Handles many features + attention explanations</td><td>Compute heavy</td></tr>
<tr><td>Chronos / TimeGPT (foundation models)</td><td>Zero-shot forecasting</td><td>No training needed</td><td>Black box, costly API</td></tr>
</tbody>
</table>'''),
        dict(label="Code", title="Prophet with Indian Holidays",
             body='''<pre><code>!pip install -q prophet

import pandas as pd
from prophet import Prophet
from prophet.make_holidays import make_holidays_df

# Load 3 years of daily ladoo sales
df = pd.read_csv("ladoo_sales.csv")  # columns: ds, y
df["ds"] = pd.to_datetime(df["ds"])

# Indian holidays — built-in support
holidays = make_holidays_df(year_list=[2023, 2024, 2025, 2026], country="IN")

# Add custom mithai-relevant events
custom = pd.DataFrame({
    "holiday": "raksha_bandhan_week",
    "ds": pd.to_datetime(["2024-08-19", "2025-08-09", "2026-08-28"]),
    "lower_window": -3, "upper_window": 1,  # spike starts 3 days before
})
holidays = pd.concat([holidays, custom])

m = Prophet(
    holidays=holidays,
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    seasonality_mode="multiplicative",  # spikes scale with trend
    changepoint_prior_scale=0.05,       # default; raise to fit faster trend changes
)
m.fit(df)

future = m.make_future_dataframe(periods=60)        # 60-day forecast
forecast = m.predict(future)

# yhat = point estimate, yhat_lower / yhat_upper = 80% confidence interval
print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(10))
m.plot(forecast)
m.plot_components(forecast)  # trend / weekly / yearly / holidays</code></pre>'''),
        dict(label="Code", title="N-BEATS for Higher Accuracy",
             body='''<pre><code>!pip install -q neuralforecast

from neuralforecast import NeuralForecast
from neuralforecast.models import NBEATS

# Same dataframe but renamed to neuralforecast convention
df_nf = df.rename(columns={"ds": "ds", "y": "y"})
df_nf["unique_id"] = "ladoo"   # one series — could be many if multi-shop

model = NBEATS(
    h=60,                       # forecast horizon = 60 days
    input_size=180,             # use last 180 days as input
    max_steps=2000,
    stack_types=["trend", "seasonality"],
    n_blocks=[3, 3],
    mlp_units=[[256, 256], [256, 256]],
    learning_rate=1e-3,
    early_stop_patience_steps=20,
)
nf = NeuralForecast(models=[model], freq="D")
nf.fit(df_nf)

predictions = nf.predict()
print(predictions.head())</code></pre>
<p>N-BEATS often beats Prophet on long, noisy series because it learns trend and seasonality basis functions directly from data rather than assuming a fixed parametric form.</p>'''),
        dict(label="Production", title="Evaluation, Drift, and Inventory Decisions",
             body='''<p><strong>Right metrics:</strong></p>
<ul>
<li><strong>MAPE (Mean Absolute Percentage Error):</strong> Most intuitive. "Forecast was off by 12% on average."</li>
<li><strong>MASE (Mean Absolute Scaled Error):</strong> Compares to a naive baseline (yesterday=today). MASE &lt; 1 means you beat the baseline.</li>
<li><strong>Pinball loss (quantile loss):</strong> If you forecast a confidence interval, this scores it.</li>
</ul>
<p><strong>Drift handling:</strong> Retail patterns shift (new metro line opens, competitor closes). Anjali retrains weekly and runs a drift detector — if MAPE jumps 30% above baseline for 3 consecutive days, alert.</p>
<p><strong>From forecast to inventory:</strong> Raw forecasts mislead. Anjali uses the <strong>upper 80% confidence interval</strong> for perishable items (better to slightly over-stock than stockout) and the <strong>lower 60%</strong> for non-perishable packaging (cash-flow optimisation). The forecast is one input — final order quantity also factors in: shelf life, safety stock, supplier lead time, cash on hand.</p>
<div class="callout green"><strong>Anjali's outcome:</strong> ₹40,000 → ₹3,000/month waste. Zero Diwali stockouts. The dashboard runs on a ₹4,500 Raspberry Pi in the shop. Her father — who never used a computer — checks tomorrow's forecast every evening at 9 PM.</div>'''),
    ],
    quiz_questions=[
        dict(q="What are the three components of a classical time-series decomposition?",
             opts=dict(a="Mean, variance, and skewness",
                       b="Trend (long-term direction), seasonality (repeating patterns at fixed periods), and residual (everything left over after removing trend + seasonality)",
                       c="Past, present, and future",
                       d="X-axis, Y-axis, and Z-axis"),
             answer="b"),
        dict(q="Why does Anjali use Prophet's built-in Indian holiday list plus custom events?",
             opts=dict(a="Prophet refuses to fit data without a holiday parameter",
                       b="Mithai sales spike sharply on Diwali, Raksha Bandhan, Karva Chauth, etc.; without holidays, the model would treat these spikes as noise and over- or under-forecast around them. Custom 'lower_window=-3' captures the pre-festival ramp-up",
                       c="Indian holidays are required for Prophet to converge",
                       d="Prophet only supports holiday-based forecasts"),
             answer="b"),
        dict(q="What does seasonality_mode='multiplicative' mean in Prophet?",
             opts=dict(a="The model multiplies the data by 2 before fitting",
                       b="Seasonal effects scale proportionally with the trend — a 50% Diwali spike on a ₹10K baseline becomes a 50% spike on a ₹15K baseline next year, not a fixed ₹5K spike. Right for retail; wrong for stationary processes",
                       c="It enables multi-output forecasting",
                       d="It runs the model on multiple GPUs"),
             answer="b"),
        dict(q="Why does N-BEATS often outperform Prophet on long, noisy series?",
             opts=dict(a="N-BEATS uses GPU acceleration",
                       b="N-BEATS learns trend and seasonality basis functions directly from data via stacked residual blocks, instead of assuming a fixed parametric form (Fourier series + piecewise-linear trend). It captures patterns Prophet's prior assumptions miss",
                       c="N-BEATS does not need any training data",
                       d="N-BEATS only handles English text inputs"),
             answer="b"),
        dict(q="What does MASE < 1 indicate?",
             opts=dict(a="The model has overfit",
                       b="The model is more accurate than the naive baseline (predicting today's value will equal yesterday's). MASE >= 1 means you have not beaten the trivial 'no model' forecast and your model adds no value",
                       c="The model uses less than 1 GB of memory",
                       d="The data has fewer than 1,000 points"),
             answer="b"),
        dict(q="Why does Anjali order based on the upper 80% confidence interval for perishables but the lower 60% for packaging?",
             opts=dict(a="It is the only choice the Prophet API allows",
                       b="For perishables, the cost of stockout (lost sale + customer disappointment) is higher than the cost of slight overstock — so she orders for the optimistic case; for packaging (non-perishable), cash flow matters more, so she orders conservatively. The right quantile depends on cost asymmetry",
                       c="Higher percentiles use more memory",
                       d="80% is the default and 60% is the minimum"),
             answer="b"),
        dict(q="What is concept drift in time-series forecasting and why does it matter?",
             opts=dict(a="A bug in the Prophet library",
                       b="The underlying pattern changes (new metro station opens, competitor closes, pandemic) so the model trained on old data systematically errs; detect by monitoring MAPE vs baseline and trigger a retrain when drift exceeds a threshold for several consecutive days",
                       c="When the time-series data is shuffled accidentally",
                       d="It happens only in financial time series"),
             answer="b"),
        dict(q="Why is the forecast only one input to Anjali's final order quantity?",
             opts=dict(a="Because forecasts are always wrong",
                       b="A point forecast ignores shelf life, supplier lead time, safety stock policy, cash on hand, and the asymmetric cost of stockout vs waste — the final inventory decision combines forecast + business constraints + risk preference",
                       c="Because she does not trust her own model",
                       d="Because Prophet outputs are illegal in India"),
             answer="b"),
    ],
    prev={"href": "lesson-08.html", "label": "Lesson 8: AI at Scale"},
    next_={"href": "lesson-10.html", "label": "Lesson 10: AI Product Management"},
))

# ----------------- LESSON 10 -----------------
LESSONS.append(dict(
    num=10, title="AI Product Management", emoji="📋",
    character="Devansh", city="Ahmedabad",
    story_summary="Manages an AI feature for a fintech app — writes the PRD, runs an A/B test, and ships safely with shadow → canary → full rollout.",
    sections=[
        dict(label="Story", title="Devansh's First PM Role",
             body='''<div class="story-card"><div class="story-who">👨‍💼 Devansh · Ahmedabad · Age 17</div>
<p>Devansh interned at an Ahmedabad fintech startup. They wanted to add an "AI categorise my expenses" feature. He wasn't writing the model — he was the <strong>product manager</strong>: defining what success looks like, what could go wrong, and how to ship it without breaking the existing app.</p>
<p>The model was 84% accurate in offline testing. Six weeks later, after shadow deployment, A/B test, and gradual rollout, the feature reached 100% of users with 2.3% increase in 7-day retention. The PM craft mattered more than the model.</p></div>'''),
        dict(label="PRD", title="The AI PRD Template",
             body='''<p>An AI Product Requirements Document differs from a regular PRD in five sections:</p>
<ol>
<li><strong>Problem statement (1 paragraph):</strong> Who hurts, how badly, today. "Users spend 6 minutes/week categorising 80 expenses by hand. 40% give up after a month."</li>
<li><strong>Success metrics:</strong> Both <em>offline</em> (model accuracy ≥ 80%) and <em>online</em> (% of users who manually correct &lt; 15%, +2% week-2 retention).</li>
<li><strong>Failure modes:</strong> What happens when the model is wrong? Wrong category is reversible (1 tap to fix); wrong PIN-entry would not be. List the worst plausible failure and the mitigation.</li>
<li><strong>Data requirements:</strong> Source, labels, refresh cadence, privacy controls, DPDPA basis (consent? legitimate use?). Will we send transaction text to a third-party API? If yes, who and under what DPA?</li>
<li><strong>Rollout plan:</strong> Shadow → 1% canary → 10% → 50% → 100%. Kill switch at every stage. Define what triggers rollback.</li>
</ol>'''),
        dict(label="Metrics", title="Offline vs Online Metrics",
             body='''<div class="concept-grid">
<div class="concept-card"><h4>Offline Metrics (Model Quality)</h4><p>Accuracy, F1, AUC, MAPE on a held-out test set. Cheap to measure but doesn't predict business impact.</p></div>
<div class="concept-card"><h4>Online Metrics (Business Outcome)</h4><p>Retention, conversion, revenue per user, NPS. The metrics that actually matter — but only measurable in production via A/B test.</p></div>
<div class="concept-card"><h4>Guardrail Metrics</h4><p>Things that must not regress: latency P99, crash rate, support ticket volume. Catch bad releases that the success metric misses.</p></div>
<div class="concept-card"><h4>Counter Metrics</h4><p>Watch for unintended harm: complaint rate, accessibility breaks, demographic accuracy disparities.</p></div>
</div>
<div class="callout indigo"><strong>The PM trap:</strong> Optimising for offline accuracy alone often regresses business metrics — a 92%-accurate model that is slow or scary can lose more revenue than the 84% model that is fast and friendly.</div>'''),
        dict(label="Rollout", title="Shadow → Canary → Full",
             body='''<table>
<thead><tr><th>Stage</th><th>What Happens</th><th>Trigger to Advance</th></tr></thead>
<tbody>
<tr><td>1. Offline eval</td><td>Test model on held-out historical data</td><td>Beats baseline by ≥ 10% on F1</td></tr>
<tr><td>2. Shadow</td><td>Run model on 100% of live traffic but show old result; log both</td><td>Online metrics ≥ offline within 5%</td></tr>
<tr><td>3. 1% canary</td><td>1% of users see new feature</td><td>No regression in guardrails for 5 days</td></tr>
<tr><td>4. A/B test (50/50)</td><td>Random 50% see new, 50% see old; measure online metrics</td><td>p-value &lt; 0.05 on success metric, no guardrail regression</td></tr>
<tr><td>5. 100% rollout</td><td>Everyone gets the feature</td><td>—</td></tr>
<tr><td>6. Monitor + iterate</td><td>Dashboards, weekly review, retrain cadence</td><td>—</td></tr>
</tbody>
</table>
<div class="callout red"><strong>Always have a kill switch.</strong> A single feature flag that can disable the AI feature within 60 seconds. AI features have failure modes that traditional code does not — model decay, adversarial inputs, prompt injection. Without a kill switch you ship without insurance.</div>'''),
        dict(label="Stats", title="A/B Testing — Real Statistical Significance",
             body='''<p>The most common mistake junior PMs make: declaring a winner from a tiny sample because the average looks better. Real A/B testing:</p>
<pre><code>from scipy import stats

# Treatment: 4,832 users, 1,287 retained at day 7  → 26.6% retention
# Control:   4,801 users, 1,202 retained at day 7  → 25.0% retention

n_t, k_t = 4832, 1287
n_c, k_c = 4801, 1202

# Two-proportion z-test
p_pool = (k_t + k_c) / (n_t + n_c)
se = (p_pool * (1 - p_pool) * (1/n_t + 1/n_c)) ** 0.5
z = ((k_t/n_t) - (k_c/n_c)) / se
p_value = 2 * (1 - stats.norm.cdf(abs(z)))
print(f"Lift: {(k_t/n_t - k_c/n_c)*100:+.2f}pp, z={z:.2f}, p={p_value:.4f}")
# Lift: +1.65pp, z=2.04, p=0.0411 → significant at α=0.05</code></pre>
<p><strong>Sample size first:</strong> Use a power calculator before you start. To detect a 1.5pp lift with 80% power and α=0.05 you need ~5,000 users per arm. If your traffic can't deliver that in 2 weeks, the test is underpowered and shouldn't run.</p>
<div class="callout green"><strong>Devansh's outcome:</strong> Feature shipped to 100% of users with +2.3% retention (p=0.003). His PRD template is now the company's standard for every AI feature. He learned that the PM craft — clear metrics, safe rollout, honest measurement — multiplies the value of any model.</div>'''),
    ],
    quiz_questions=[
        dict(q="What is the difference between offline and online metrics?",
             opts=dict(a="Offline metrics are computed without internet; online metrics require internet",
                       b="Offline metrics measure model quality on held-out historical data (accuracy, F1, AUC) and are cheap; online metrics measure business outcomes (retention, revenue) only available from production A/B tests — and are the metrics that actually matter",
                       c="Offline metrics are for training, online metrics are for inference",
                       d="There is no meaningful difference"),
             answer="b"),
        dict(q="Why does Devansh include a 'failure modes' section in his PRD?",
             opts=dict(a="It is required by Indian fintech regulation",
                       b="AI features fail in ways traditional code does not — wrong predictions, drift, prompt injection. Listing the worst plausible failure and its mitigation forces the team to design for graceful degradation rather than discovering the failure in production",
                       c="It makes the PRD longer and more impressive",
                       d="Failure modes have no real impact on shipping"),
             answer="b"),
        dict(q="What is the purpose of shadow deployment?",
             opts=dict(a="To save GPU cost during development",
                       b="Run the new model on 100% of real traffic but do not show its output to users — log predictions side-by-side with the existing system. This validates online metrics, surfaces edge cases, and stress-tests infrastructure with zero user risk before any rollout",
                       c="To test the model on synthetic data",
                       d="To hide the model from competitors"),
             answer="b"),
        dict(q="What are guardrail metrics and why does Devansh track them in every A/B test?",
             opts=dict(a="They are metrics displayed on a literal guardrail",
                       b="Things that must NOT regress (P99 latency, crash rate, support ticket volume) — even when the success metric improves, regressions in guardrails can mean the feature is causing hidden harm; without them, a 'winning' test can ship a net-negative experience",
                       c="They measure how many guardrails are deployed",
                       d="They are a synonym for offline metrics"),
             answer="b"),
        dict(q="Why does Devansh do a power calculation before running the A/B test?",
             opts=dict(a="It is required by the company's CFO",
                       b="To know how many users per arm are needed to detect the expected lift with adequate statistical power (e.g., 80%) at α=0.05 — running an underpowered test wastes time and produces ambiguous results that cannot reject either hypothesis",
                       c="Power calculations make the test run faster",
                       d="It is the only way to compute p-values"),
             answer="b"),
        dict(q="Why is a kill switch (single feature flag with 60-second propagation) essential for AI features?",
             opts=dict(a="It is required by Kubernetes for any deployment",
                       b="AI features have failure modes traditional code lacks — model drift, adversarial inputs, prompt injection, sudden regression after a third-party API change. Without an instant kill switch, every release ships without insurance against catastrophic failures discovered post-launch",
                       c="It speeds up CI/CD pipelines",
                       d="It is required by the AI safety regulator"),
             answer="b"),
        dict(q="What DPDPA-related question must an AI PRD answer for any feature processing user data?",
             opts=dict(a="Whether the model is open-source or proprietary",
                       b="What is the lawful basis (consent or legitimate use), where is the data processed (in-country or cross-border), who is the data fiduciary, what data minimisation is applied, and is there a third-party processor agreement (DPA) — DPDPA 2023 requires this clarity before launch",
                       c="What programming language the model is written in",
                       d="Whether the model is bigger than 7 billion parameters"),
             answer="b"),
        dict(q="What is the central insight of Devansh's lesson about AI product management?",
             opts=dict(a="The most important PM skill is writing perfect specs",
                       b="The PM craft — clear success metrics, honest measurement, staged rollout with kill switches — multiplies (or destroys) the value of any AI model; an 84%-accurate model shipped well outperforms a 92%-accurate model shipped badly",
                       c="PMs should write the model code themselves",
                       d="AI features should always be shipped to 100% of users on day 1"),
             answer="b"),
    ],
    prev={"href": "lesson-09.html", "label": "Lesson 9: Time Series"},
    next_={"href": "lesson-11.html", "label": "Lesson 11: College &amp; Career"},
))


# ----------------- LESSON 11 -----------------
LESSONS.append(dict(
    num=11, title="College Admissions &amp; AI Career Path", emoji="🎓",
    character="Ananya", city="Coimbatore",
    story_summary="Maps the real path from Class 12 to an AI career — Indian colleges, global colleges, internships, and the GitHub portfolio that opens doors.",
    sections=[
        dict(label="Story", title="Ananya's Application Year",
             body='''<div class="story-card"><div class="story-who">👩‍🎓 Ananya · Coimbatore · Age 17</div>
<p>Ananya wanted to study AI but didn't know whether to aim for IIT, IIIT, BITS, or apply abroad. She had no PhD parent guiding her. So she made her own roadmap — three flagship GitHub projects, a Kaggle bronze, one Medium article series, and a clear pitch.</p>
<p>Result: BITS Pilani CSE (Pilani campus) admit + IIIT-Hyderabad CSD admit + an unpaid summer research internship with an IIT-Madras professor. Total prep cost: ₹0 beyond JEE coaching. Roadmap and templates here.</p></div>'''),
        dict(label="Portfolio", title="The GitHub Portfolio That Gets Reviewed",
             body='''<p>College admission committees and internship recruiters skim — they don't read. Your GitHub must pass the 30-second test:</p>
<div class="callout indigo"><strong>The 3-flagship rule:</strong> Pin three projects (not 30). Each should:
<ol>
<li>Solve a real, named problem (not "ML demo").</li>
<li>Have a README with: problem statement, dataset link, results table, deployed demo URL or video, lessons learned.</li>
<li>Show one technical depth (e.g., "I implemented PagedAttention from scratch" or "I built the eval harness for 8 Indian languages").</li>
</ol></div>
<p><strong>Example flagship from this course:</strong></p>
<ul>
<li>Class 11 L12 — Crop Disease Detection Web App (computer vision, deployed on Streamlit)</li>
<li>Class 12 L01 — Marathi Tutor with QLoRA (LLM fine-tuning, Hindi/Marathi eval)</li>
<li>Class 12 L08 — vLLM Deployment for 50K Users (production AI, k8s)</li>
</ul>
<p>That's already three flagships, all built across this course. Polish the READMEs and pin them.</p>'''),
        dict(label="Indian Colleges", title="AI-Strong Indian Colleges (2026)",
             body='''<table>
<thead><tr><th>Tier</th><th>Colleges</th><th>Entry Path</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>Tier 1 — IITs</td><td>IIT Bombay, Delhi, Madras, Kanpur, Kharagpur</td><td>JEE Advanced</td><td>Strong CS faculty; AI specialisation typically via electives + B.Tech project</td></tr>
<tr><td>Tier 1 — Specialised</td><td>IIIT Hyderabad (CSD/CLD), IIIT Delhi (CSAI), IISc UG (CS &amp; Data Science)</td><td>JEE Main, UGEE (IIIT-H), KVPY/IISc admission test</td><td>India's top dedicated AI/CS programs</td></tr>
<tr><td>Tier 1 — Private</td><td>BITS Pilani (Pilani/Goa/Hyd), Plaksha, Ashoka</td><td>BITSAT, own tests</td><td>BITS CS at Pilani is on par with IITs in AI hiring</td></tr>
<tr><td>Tier 2</td><td>NITs (Trichy, Surathkal, Warangal), VIT Vellore, IIIT Bangalore (PG only), Manipal</td><td>JEE Main, VITEEE</td><td>Solid CS, depends on student initiative</td></tr>
<tr><td>Specialised AI</td><td>IIT Hyderabad B.Tech AI, IIT Jodhpur AI &amp; DS, IIT Patna AI</td><td>JEE Advanced</td><td>Newer AI-named programs at IITs</td></tr>
</tbody>
</table>
<div class="callout indigo"><strong>Truth:</strong> Once you're at any tier-1 or strong tier-2 college, your portfolio + internships + GitHub matter more than your college name for AI roles. Colleges open the first door; your work keeps it open.</div>'''),
        dict(label="Global Colleges", title="If You're Considering Abroad",
             body='''<p>For undergrad AI/CS abroad, the typical strong options:</p>
<ul>
<li><strong>USA:</strong> CMU SCS, MIT EECS, Stanford CS, UC Berkeley EECS, Princeton CS, UIUC CS, Georgia Tech CS, UMich CS. Plus need-blind for Indian students: Harvard, Yale, MIT, Princeton (limited).</li>
<li><strong>UK:</strong> Cambridge (Computer Science), Oxford (CS or Maths &amp; CS), Imperial Computing, UCL CS, Edinburgh AI.</li>
<li><strong>Singapore:</strong> NUS CS, NTU CS — well-funded, strong AI faculty, Indian-friendly.</li>
<li><strong>Canada:</strong> University of Toronto (Geoffrey Hinton's home), University of Waterloo CS (great co-op), UBC CS.</li>
<li><strong>Europe:</strong> ETH Zurich CS, EPFL CS, TU Munich AI, KU Leuven AI.</li>
</ul>
<div class="callout red"><strong>Cost reality:</strong> US private undergrad ≈ ₹70 lakh/year all-in. UK ≈ ₹45 lakh/year. Singapore ≈ ₹25 lakh/year. Most need significant scholarship or family resources. Check need-based aid: MIT, Princeton, Yale offer it to international students; Stanford partial.</div>
<div class="callout green"><strong>Pragmatic path:</strong> B.Tech in India (IIT/IIIT/BITS) → MS in USA/UK with research-funded admission. This is how most successful Indian AI researchers got started — and you graduate with portable income, not portable debt.</div>'''),
        dict(label="Internships", title="The Internship Hunt — Cold Email Template",
             body='''<p>Cold email is the most under-used tool by Indian students. Here is what worked for Ananya:</p>
<pre><code>Subject: Class 12 student — your DDP paper inspired my IndicBERT pre-training run

Dear Prof. [Name],

I'm Ananya Krishnan, a Class 12 student in Coimbatore. After reading
your 2024 paper on efficient gradient compression for distributed
training, I implemented a small-scale reproduction on IndicBERT-base
across 8 GPUs and saw a 2.1x throughput improvement matching your
Table 3.

GitHub: github.com/ananyak/indicbert-ddp-repro
(Includes the modified all-reduce hook, training logs, and a write-up.)

I'd love to spend my summer (May-July 2026) helping with any
infrastructure or empirical-eval task in your lab — paid or unpaid,
remote or in-person. Even logging experiments would be a privilege.

Open to a 15-minute call any time that suits you.

Thank you for reading,
Ananya</code></pre>
<div class="callout indigo"><strong>Why this works:</strong> Specific paper + concrete reproduction + GitHub link + flexibility on terms + zero-pressure ask. 1 in 8 emails like this got a positive reply for Ananya.</div>
<div class="callout green"><strong>Other internship sources:</strong>
<ul>
<li><strong>Kaggle:</strong> A bronze medal is a real signal. Compete in Indic NLP / vision challenges.</li>
<li><strong>Open source:</strong> Contribute to AI4Bharat, Indic-NLP-Library, vLLM, transformers. A merged PR is a portfolio item.</li>
<li><strong>Smerc/RIA/IAS:</strong> Indian AI summer schools (often free for top applicants).</li>
<li><strong>Build-in-public:</strong> A working AI project with 100 real users beats most internships on a resume.</li>
</ul></div>'''),
        dict(label="Career", title="The First 5 Years — Realistic AI Career Path",
             body='''<table>
<thead><tr><th>Year</th><th>Role</th><th>Typical Compensation (India)</th><th>What to Build</th></tr></thead>
<tbody>
<tr><td>Year 0 (UG)</td><td>Student + Intern</td><td>Stipend ₹15K–60K/month</td><td>Portfolio + 2 internships + 1 paper if possible</td></tr>
<tr><td>Year 1–2</td><td>Junior ML Engineer / AI Engineer</td><td>₹15–35 LPA (tier 1) or ₹8–18 LPA (tier 2)</td><td>Ship 2 production models; learn one specialisation</td></tr>
<tr><td>Year 3–5</td><td>Senior ML / Research Engineer</td><td>₹30–80 LPA</td><td>Lead a model surface end-to-end; mentor 1–2 juniors</td></tr>
<tr><td>Year 5+</td><td>Staff / Principal / Founder / PhD</td><td>₹60 LPA – ₹2 Cr+ or research/founder route</td><td>Architect or research direction; or start your own</td></tr>
</tbody>
</table>
<p>Top employers in India for AI roles (2026): Google India, Microsoft IDC, Amazon (AWS / Alexa), Adobe, Uber India, Ola Krutrim, Sarvam AI, Haptik, Glance, Razorpay, Flipkart, Swiggy, Zomato, plus US companies hiring remotely (Anthropic, OpenAI, NVIDIA, Cohere). Indian foundation-model startups (Sarvam, Krutrim, TWO AI) are the highest-leverage early-career bets right now.</p>
<div class="callout green"><strong>Ananya's outcome:</strong> BITS Pilani CSE + IIIT-H CSD admits + IIT-Madras summer research. She picked BITS Pilani — closer family, strong AI alumni network, and the founder mindset she wants. Her GitHub now lists 5 flagship projects. She is on track to apply for an MS at CMU or Stanford in 4 years.</div>'''),
    ],
    quiz_questions=[
        dict(q="What is the '3-flagship rule' for an AI portfolio?",
             opts=dict(a="Build at least 30 small projects to show breadth",
                       b="Pin exactly three projects on GitHub, each solving a named real problem with a clear README (problem, dataset, results, demo URL, lessons), and each demonstrating one technical depth — admissions and recruiters skim in 30 seconds, so depth-on-three beats breadth-on-thirty",
                       c="Have one flagship for each of the three FAANG companies",
                       d="Have three flagships only if you are applying abroad"),
             answer="b"),
        dict(q="Which Indian colleges have dedicated UG AI/CS programs that rival the IITs?",
             opts=dict(a="Only the IITs offer real CS or AI programs",
                       b="IIIT Hyderabad (CSD/CLD), IIIT Delhi (CSAI), IISc UG (CS & Data Science), and BITS Pilani CSE — these have strong AI faculty, dedicated curriculum, and place graduates into AI roles on par with the top IITs",
                       c="Any private engineering college will do",
                       d="Only colleges with 'AI' in their name count"),
             answer="b"),
        dict(q="Why does Ananya's pragmatic path recommend B.Tech in India then MS abroad?",
             opts=dict(a="Indian degrees are not respected internationally",
                       b="A funded MS or PhD abroad (assistantship + tuition waiver) lets you study at top global universities without family debt; doing UG abroad costs ₹25-70 lakh/year out of pocket. Save the global move for graduate school where research funding is normal",
                       c="It is the only way to get a US visa",
                       d="MS is required to get any AI job"),
             answer="b"),
        dict(q="What makes a cold email to a researcher likely to get a reply?",
             opts=dict(a="Sending the same generic email to 500 professors",
                       b="A specific paper reference + concrete reproduction or extension + GitHub link with working code + flexibility on terms (paid/unpaid, remote/onsite) + a low-pressure ask. Demonstrating you have already done unpaid work in their domain is the strongest possible signal",
                       c="Mentioning your JEE rank in the first line",
                       d="Attaching your full CV as a 5-page PDF"),
             answer="b"),
        dict(q="Why is contributing a merged PR to AI4Bharat or vLLM a strong portfolio item?",
             opts=dict(a="Open-source contributions count as paid work experience",
                       b="A merged PR is independently verified evidence that maintainers (often senior engineers/researchers) judged your code production-worthy — a stronger signal than self-built projects which only you have evaluated",
                       c="It is the only path to a software job",
                       d="Open-source PRs guarantee an internship offer"),
             answer="b"),
        dict(q="What does Ananya's lesson say about college brand vs portfolio?",
             opts=dict(a="College brand always determines salary and role",
                       b="College opens the first door (campus placement, alumni network); after that, portfolio + internships + GitHub determine your trajectory in AI roles. Strong work from a tier-2 college consistently beats weak work from a tier-1 college",
                       c="Portfolio matters only at FAANG companies",
                       d="Brand doesn't matter at all in India"),
             answer="b"),
        dict(q="Which Indian foundation-model startups are highlighted as high-leverage early-career bets in 2026?",
             opts=dict(a="Only multinational companies hire AI talent in India",
                       b="Sarvam AI, Krutrim (Ola), TWO AI, and similar Indian foundation-model startups — small enough that you ship work that ships, large enough to have real GPU budgets, and building India-specific AI where domain knowledge gives an edge over global competitors",
                       c="Government PSUs are the only stable option",
                       d="Indian startups never hire freshers"),
             answer="b"),
        dict(q="What is the realistic compensation range for a Year 1-2 AI engineer at a tier-1 Indian campus in 2026?",
             opts=dict(a="₹4-6 lakh per annum",
                       b="Roughly ₹15-35 LPA at tier-1 campuses (IIT/IIIT/BITS), ₹8-18 LPA at tier-2 — actual numbers depend on company tier, internship conversions, and demonstrated AI specialisation; foundation-model startups and US-remote roles can pay higher",
                       c="₹2 crore per annum guaranteed",
                       d="Compensation does not vary by college"),
             answer="b"),
    ],
    prev={"href": "lesson-10.html", "label": "Lesson 10: AI Product Management"},
    next_={"href": "lesson-12.html", "label": "Lesson 12: Capstone"},
))


# Build all lessons
def main():
    print(f"Generating Class 12 lessons in {OUT_DIR}...")
    nav_chain = []
    for i, spec in enumerate(LESSONS):
        nav_chain.append((spec["num"], spec["title"]))

    for spec in LESSONS:
        page(**spec)
    print(f"\nDone. Generated {len(LESSONS)} lesson(s).")


if __name__ == "__main__":
    main()
