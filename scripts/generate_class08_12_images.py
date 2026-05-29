"""
Generate hero images for Class 8–12 using gpt-image-1.
Run:  .venv/bin/python scripts/generate_class08_12_images.py [--class 08]

- Reads OPENAI_API_KEY from .env
- Saves images to content/assets/students/class-NN/
- Skips files that already exist (safe to re-run)
- Pass --class 08 (or 09 10 11 12) to generate one class only
"""
import argparse
import base64
import os
import time
from pathlib import Path

from openai import OpenAI

# ── load .env ─────────────────────────────────────────────────────────────────
def load_env(path=".env"):
    env_path = Path(__file__).resolve().parents[1] / path
    if not env_path.exists():
        raise FileNotFoundError(f".env not found at {env_path}")
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())

load_env()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

BASE = Path(__file__).resolve().parents[1] / "content" / "assets" / "students"

# ── shared style suffix ────────────────────────────────────────────────────────
def style(palette: str) -> str:
    return (
        f"Vibrant cartoon illustration style, Indian cultural setting, bold black outlines, "
        f"{palette}, comic book aesthetic, expressive teenage faces, "
        f"clean flat design, family-friendly, 2D art. "
        f"No text, no letters, no numbers inside the image."
    )

# ── CLASS 08 — teal/emerald palette, age 13-14, conceptual AI ────────────────
CLASS08_STYLE = style("warm teal and emerald green colour palette")
CLASS08 = [
    ("lesson-01-hero.jpg", "Indian teenager age 13 at a school desk in Hyderabad studying how AI works. "
     "A transparent diagram of a simple neural network floats above an open textbook — three layers of "
     "glowing teal circles connected by arrows. The student points at the diagram with curiosity. "
     "Bright Indian classroom with posters on the wall."),
    ("lesson-02-hero.jpg", "A large glowing dataset visualised as hundreds of tiny colourful cards — "
     "photos, numbers, text snippets — streaming into a funnel shaped like a brain. "
     "An Indian student age 13 watches wide-eyed as the cards flow in. Teal and white tones. "
     "Clean educational infographic style set in an Indian classroom."),
    ("lesson-03-hero.jpg", "Indian teenager at a whiteboard drawing a decision tree that splits items "
     "into groups — apples vs oranges, spam vs not-spam, cats vs dogs. "
     "A glowing AI robot assistant beside the board points at correct classification nodes. "
     "Cheerful classroom setting, teal and gold accents."),
    ("lesson-04-hero.jpg", "A flowchart pipeline floating in the air: input box → AI process box → "
     "output box, connected by glowing teal arrows. An Indian student plugs different inputs "
     "(text, image, audio) into the first box. Factory-meets-classroom setting, clean and colourful."),
    ("lesson-05-hero.jpg", "Cartoon cross-section of a language model: words break into small tokens, "
     "tokens connect through glowing attention lines, and a new word appears at the output. "
     "An Indian teenager watches the process through a magnifying glass. Teal blue tones, "
     "clean flat educational diagram style."),
    ("lesson-06-hero.jpg", "An AI robot eye scanning a street scene in an Indian city — auto-rickshaws, "
     "a chai stall, a school. Colourful bounding boxes highlight each detected object. "
     "Indian teen watches the detection happen on a tablet screen. Teal and amber palette."),
    ("lesson-07-hero.jpg", "Two pans of a golden justice scale. One pan has a pile of Indian faces "
     "of different regions — North, South, East, West. The other pan has an AI output report. "
     "The scale tips slightly, showing imbalance. Indian student examines the scale thoughtfully. "
     "Teal and amber tones. Concept: fairness and bias."),
    ("lesson-08-hero.jpg", "Indian teenagers in a classroom discussion circle, one student at a board "
     "writing 'Should AI decide?' with three colourful thought-bubble options floating above. "
     "Each bubble shows a different ethical scenario — a medical decision, a school exam, a loan. "
     "Warm teal and cream tones. Thoughtful, discussion-oriented atmosphere."),
    ("lesson-09-hero.jpg", "Illustrated map of India with glowing teal hotspots in different states — "
     "DIKSHA logo over UP, Plantix over Andhra Pradesh, Aarogya Setu over Maharashtra, "
     "Bhashini over Tamil Nadu. Indian students wave flags of innovation. Bright celebratory scene."),
    ("lesson-10-hero.jpg", "Indian student age 13 at a computer, building a small AI project — "
     "a plant identifier app on screen. Around the desk: a notebook of ideas, a phone camera, "
     "sample leaf photos. A tiny glowing AI robot sits on the monitor helping. Teal accent colours."),
    ("lesson-11-hero.jpg", "Indian teenager's first Python script glowing on a laptop screen — "
     "clear colourful syntax highlighting, a simple print('Hello AI') visible. "
     "A cheerful robot hovers over the keyboard coaching the student. Bright home study setting. "
     "Teal and white palette."),
    ("lesson-12-hero.jpg", "Indian student proudly holding up a colourful portfolio folder labelled "
     "'My Class 8 AI Portfolio'. Around the student float 12 mini icons representing each lesson — "
     "a neural net, a dataset, a decision tree, a pipeline, a language token, an eye, "
     "a scale, an ethics symbol, India map, a project, Python code, a star. "
     "Teal graduation cap and sparkles. Celebratory warm scene."),
]

# ── CLASS 09 — orange/rust palette, age 14-15, first ML steps ────────────────
CLASS09_STYLE = style("warm orange, rust, and amber colour palette")
CLASS09 = [
    ("lesson-01-hero.jpg", "Glowing orange diagram of a neural network with labelled layers: "
     "Input Layer, Hidden Layer 1, Hidden Layer 2, Output Layer. Arrows show data flowing "
     "forward through circles. Indian teenager age 14 traces the connections with a finger. "
     "Clean educational illustration, orange and cream tones."),
    ("lesson-02-hero.jpg", "Indian student age 14 opens a CSV file on a laptop — rows and columns "
     "of structured data glow orange on screen. Beside the laptop: a small chart starting to form "
     "from the data. Clean flat illustration, organised and data-focused. Orange and white palette."),
    ("lesson-03-hero.jpg", "A messy table of data with missing cells, duplicate rows highlighted "
     "in red — and a glowing broom sweeping through it, leaving clean organised rows behind. "
     "Indian student at the keyboard pressing 'Clean'. Satisfying before/after visual. Orange tones."),
    ("lesson-04-hero.jpg", "A colourful scatter plot floats in the air above an Indian student's "
     "laptop. A glowing decision boundary line cuts through two clusters of dots. "
     "A small scikit-learn logo badge glows on the screen. Flat cartoon illustration. "
     "Orange and teal colour split across the two data classes."),
    ("lesson-05-hero.jpg", "A model report card floating in the air: Accuracy 87%, Precision 84%, "
     "Recall 91%, F1 Score 87% — each metric in a different coloured badge. "
     "Indian student reviews the report like a school exam result. Orange palette. "
     "Clean, informative illustration style."),
    ("lesson-06-hero.jpg", "A smooth prediction curve arching over a scatter plot of house price "
     "data points — Indian-style houses with prices labelled in rupees. A regression line fits "
     "through the points. Indian student draws the curve on a touchscreen. Orange and gold tones."),
    ("lesson-07-hero.jpg", "A glowing generative AI engine: noise particles on the left, a "
     "beautiful Indian landscape painting emerging on the right, transformation happening in "
     "the middle through a glowing diffusion process. Indian teenager watches in awe. "
     "Orange and golden tones."),
    ("lesson-08-hero.jpg", "A sentence in Hindi floats in the air, breaking into individual word "
     "tokens. Each token gets tagged — noun, verb, adjective — in colourful labels. "
     "An NLP pipeline diagram beneath shows tokenise → tag → embed. "
     "Indian student follows the pipeline. Orange and cream tones."),
    ("lesson-09-hero.jpg", "A vibrant dashboard of Indian data charts — a bar chart of state populations, "
     "a line graph of monsoon rainfall, a pie chart of crop types. "
     "An Indian student builds the dashboard in a Colab notebook visible on screen. "
     "Orange and data-viz rainbow tones."),
    ("lesson-10-hero.jpg", "Split workplace scene: left side shows an Indian professional doing "
     "tedious manual work (stacks of papers); right side the same professional uses an AI tool "
     "and the papers are organised instantly. Arrow between the two sides. Orange and green tones. "
     "Positive, empowering tone."),
    ("lesson-11-hero.jpg", "Indian student's laptop shows Python code calling a weather API — "
     "a JSON response floats out of the screen with temperature and city data. "
     "A small API connection diagram shows request → server → response. "
     "Orange and teal tones. Clean tech illustration."),
    ("lesson-12-hero.jpg", "Indian student holding a colourful project portfolio binder labelled "
     "'My Class 9 AI Project'. Around the student float 12 mini icons: neural net, CSV, "
     "broom, scatter plot, report card, regression curve, diffusion swirl, NLP tags, "
     "data dashboard, office, API call, a portfolio star. "
     "Orange graduation sparkles. Celebratory warm scene."),
]

# ── CLASS 10 — deep emerald green palette, age 15-16, applied ML ─────────────
CLASS10_STYLE = style("deep emerald green and dark teal colour palette")
CLASS10 = [
    ("lesson-01-hero.jpg", "Diagram of a Convolutional Neural Network processing an image of an "
     "Indian tiger. Feature maps cascade through colourful filter layers — edges, textures, shapes. "
     "An Indian student age 15 examines the feature map grid on a monitor. "
     "Deep green and white tones. Technical but clear."),
    ("lesson-02-hero.jpg", "Transfer learning visualised: a large pre-trained MobileNetV2 tower "
     "on the left with frozen layers in grey, and a small new classification head in bright green "
     "added on top. Indian student connects the two blocks in a Colab notebook. "
     "Green and amber colour split."),
    ("lesson-03-hero.jpg", "A city street scene in India with bright bounding boxes drawn around "
     "every detected object — auto-rickshaw, pedestrian, traffic light, chai stall. "
     "YOLO detection confidence percentages float above each box. "
     "Indian student watches the real-time detection on a laptop. Emerald and orange tones."),
    ("lesson-04-hero.jpg", "Transformer attention visualised: a sentence in English splits into "
     "word tokens, and glowing attention lines of different strengths connect each word to every "
     "other word. A BERT/GPT architecture diagram sits below. "
     "Indian student traces attention weights on a screen. Green and gold tones."),
    ("lesson-05-hero.jpg", "Fine-tuning diagram: a large pre-trained model block in emerald green "
     "with most layers frozen, and a small IndicBERT or Indian-language fine-tune layer glowing "
     "amber on top. 'Before' shows generic output; 'After' shows Indian language-specific output. "
     "Indian student celebrates at the keyboard."),
    ("lesson-06-hero.jpg", "A RAG chatbot architecture: a document goes into a vector database "
     "(shown as a glowing grid of colourful embeddings), a query arrow retrieves the closest "
     "vectors, and a response emerges. Indian student chats with the bot about their own PDF. "
     "Emerald green and teal tones."),
    ("lesson-07-hero.jpg", "An MLflow experiment dashboard floating in the air: multiple model runs "
     "compared side by side with accuracy curves, parameter tables, and a winning model highlighted "
     "in green. Indian student reviews runs like a scientist. Clean data dashboard aesthetic. "
     "Deep green and white tones."),
    ("lesson-08-hero.jpg", "A FastAPI server diagram: a phone sends a POST request to a server, "
     "the server runs an ML model (shown as a brain icon), and returns a JSON prediction response. "
     "Indian student writes the API code in VS Code. Emerald green and cream tones."),
    ("lesson-09-hero.jpg", "A Streamlit web app running on a laptop: a slider on the left, "
     "a chart updating in real time on the right. Indian student demonstrates the app to a "
     "friend. Clean, modern UI visible on screen. Green and white colour scheme. Impressive demo feel."),
    ("lesson-10-hero.jpg", "Split-panel scene showing four Indian AI impact areas: top-left "
     "a farmer with Plantix plant diagnosis; top-right an eye doctor with AI diagnosis; "
     "bottom-left a student with DIKSHA; bottom-right a rural woman using a fintech app. "
     "Emerald green connectors link all panels."),
    ("lesson-11-hero.jpg", "A fairness audit dashboard with bias heatmaps, model cards, and "
     "a fairness metric comparison across different demographic groups. "
     "Indian student highlights a bias issue and marks it for correction. "
     "Emerald and amber tones. Responsible AI theme."),
    ("lesson-12-hero.jpg", "Indian student age 15 holding a phone showing a live deployed web app — "
     "their own AI product with a clean UI. Around the student: a dataset → model → API → "
     "Streamlit pipeline floating as a circular diagram. Graduation cap, stars. "
     "Emerald green celebratory scene."),
]

# ── CLASS 11 — amber/deep orange palette, age 16-17, advanced ────────────────
CLASS11_STYLE = style("deep amber, burnt orange, and golden colour palette")
CLASS11 = [
    ("lesson-01-hero.jpg", "Advanced Python code on a dark-themed editor: decorators, generators, "
     "type hints, and dataclasses visible with colourful syntax highlighting. "
     "Indian student age 16 at a mechanical keyboard in a focused evening study session. "
     "Amber glow from monitor. Technical but inspiring."),
    ("lesson-02-hero.jpg", "Deep learning backpropagation diagram: error signal flows backwards "
     "through a deep neural network, each layer's gradients shown as arrows of decreasing size. "
     "Loss curve graph nearby showing model improving. Indian student sketches the math "
     "on paper beside the laptop. Amber and deep blue tones."),
    ("lesson-03-hero.jpg", "A reinforcement learning grid world: an Indian student-character "
     "agent navigating a maze, collecting reward coins at goal states, avoiding penalty traps. "
     "State values (V numbers) shown in each grid cell. Q-table floating beside the maze. "
     "Amber and teal game-board style."),
    ("lesson-04-hero.jpg", "An AI agent learning to balance a cartpole — the classic RL problem — "
     "with a policy gradient graph showing reward climbing episode by episode. "
     "PPO algorithm flowchart with actor and critic networks. "
     "Indian student tracks reward curves on a monitor. Amber and green tones."),
    ("lesson-05-hero.jpg", "A Docker container visualised as a colourful shipping container "
     "with an ML model inside — Python logo, ML framework logos (PyTorch, sklearn) "
     "stacked like cargo. The container ships from laptop to a cloud server. "
     "Indian student watches the deployment. Amber and steel blue tones."),
    ("lesson-06-hero.jpg", "A production ML monitoring dashboard: accuracy over time, "
     "data drift alert (a red spike in the graph), model performance metrics. "
     "Alerts and notifications pop up. Indian data scientist reviews the drift warning. "
     "Amber and dark navy tones. Professional, real-world atmosphere."),
    ("lesson-07-hero.jpg", "Three AI modalities merging into one: an eye (vision), a speech bubble "
     "(language), and a sound wave (speech) flowing together into a central multimodal AI brain. "
     "Indian student demonstrates a multimodal query — an image + text question on screen. "
     "Amber, teal, and violet tones."),
    ("lesson-08-hero.jpg", "An AI agent with a tool belt — each tool a glowing icon: web search, "
     "calculator, code executor, file reader. The agent follows a ReAct loop diagram: "
     "Think → Act → Observe → Think. Indian student watches the agent solve a multi-step task. "
     "Amber and gold tones."),
    ("lesson-09-hero.jpg", "An academic AI research paper floating in the air — abstract, methods, "
     "results graph visible. The Indian student highlights key equations and sketches "
     "the architecture diagram from the paper in a notebook. "
     "Amber and cream tones. Library or study setting, focused atmosphere."),
    ("lesson-10-hero.jpg", "An AI alignment scale: on one side 'AI capabilities' rising like a "
     "rocket, on the other 'AI safety and human values' — shown as a heart and a shield. "
     "The scale is balanced carefully. Indian student thinks deeply, hand on chin. "
     "Amber and deep red tones. Serious, thoughtful scene."),
    ("lesson-11-hero.jpg", "An Indian student age 16 pitching an AI startup idea on a whiteboard "
     "to two investors. The whiteboard shows a product diagram with Indian users at the centre. "
     "Bangalore tech hub aesthetic — glass office, city skyline outside. "
     "Amber and gold tones. Energetic, entrepreneurial."),
    ("lesson-12-hero.jpg", "Indian student presenting an AI research project at a science fair "
     "— a large poster board behind them with models, graphs, and results. "
     "An audience of peers and a teacher listens. Around the scene float 12 mini icons "
     "representing each Class 11 lesson. Amber graduation sparkles and stars. Proud moment."),
]

# ── CLASS 12 — indigo/deep purple palette, age 17-18, cutting edge ────────────
CLASS12_STYLE = style("deep indigo, rich violet, and silver colour palette")
CLASS12 = [
    ("lesson-01-hero.jpg", "LoRA fine-tuning visualisation: a large frozen LLM tower in deep indigo "
     "with only tiny trainable rank-decomposition matrices (LoRA adapters) glowing in gold on the "
     "sides. A comparison: before fine-tuning shows generic text output, after shows "
     "domain-specific text. Indian student age 17 watches the training run. Indigo and gold tones."),
    ("lesson-02-hero.jpg", "A vector database visualised as a glowing grid of colourful embedding "
     "vectors. A query vector (bright gold arrow) zooms toward the nearest neighbours. "
     "A production RAG pipeline diagram beneath: Query → Retrieve → Augment → Generate. "
     "Indian student builds the pipeline on a laptop. Indigo and gold tones."),
    ("lesson-03-hero.jpg", "Multiple GPUs illustrated as glowing purple server racks connected "
     "by high-speed data arrows. PyTorch DDP logo floating above. A distributed training loss "
     "curve shows faster convergence with more GPUs. Indian student monitors the cluster. "
     "Indigo and electric blue tones."),
    ("lesson-04-hero.jpg", "A Graph Neural Network diagram: colourful nodes representing people "
     "in a social network, edges showing connections, and messages passing along the edges "
     "in glowing pulses. The GNN output — a node classification result — shown beside. "
     "Indian student sketches the graph. Indigo and teal tones."),
    ("lesson-05-hero.jpg", "Diffusion model forward and reverse process: an Indian landscape painting "
     "gradually turns to noise (left to right), then the reverse — noise gradually becomes "
     "a beautiful new painting (right to left). Gaussian noise cloud in the middle. "
     "Indian student generates art on a workstation. Indigo and violet tones."),
    ("lesson-06-hero.jpg", "A speech waveform on screen converting to text in multiple Indian languages — "
     "Hindi, Telugu, Tamil — shown as glowing text bubbles. TTS voice waves radiate outward. "
     "An ethics warning banner overlays voice cloning section. Indian student records a "
     "sample sentence. Indigo and teal tones."),
    ("lesson-07-hero.jpg", "A recommendation engine diagram: a user profile on the left, "
     "a collaborative filtering matrix in the middle (user-item grid with ratings), "
     "and recommended items floating on the right — movies, books, products. "
     "Indian e-commerce aesthetic. Indian student implements the system. Indigo and amber tones."),
    ("lesson-08-hero.jpg", "A Kubernetes cluster diagram: multiple pod icons orchestrated on "
     "a cloud platform. A vLLM inference server handles multiple incoming prompt requests "
     "efficiently. Indian student monitors the cluster dashboard. "
     "Indigo and electric blue tones. Scale and infrastructure feel."),
    ("lesson-09-hero.jpg", "A time series forecasting chart: historical stock or weather data "
     "in blue, then a dashed prediction line extending into the future in gold. "
     "Confidence intervals shown as shaded bands. Indian student annotates the forecast. "
     "Indigo and gold tones. Data science aesthetic."),
    ("lesson-10-hero.jpg", "An AI product roadmap on a whiteboard: discovery, prototyping, "
     "pilot, scale stages with colourful sticky notes. An Indian product manager age 17 "
     "presents to a small team. AI product metrics dashboard visible on a screen behind them. "
     "Indigo and cream tones. Professional strategy session."),
    ("lesson-11-hero.jpg", "An Indian student age 17 researching college admission options — "
     "IITs, IISc, international universities — on a laptop, with an AI assistant helping "
     "compare options on screen. A future career roadmap floats above: student → researcher → "
     "AI engineer → founder. Indigo and gold stars. Hopeful and aspirational scene."),
    ("lesson-12-hero.jpg", "Indian student age 17 at a graduation ceremony holding a laptop "
     "with their final AI portfolio website live on screen. "
     "Around the student float 12 glowing icons from each Class 12 lesson: "
     "LoRA adapter, vector grid, GPU rack, graph network, diffusion swirl, voice wave, "
     "recommendation grid, Kubernetes pod, forecast chart, roadmap, college buildings, portfolio star. "
     "Indigo graduation cap, confetti, gold sparkles. Triumphant ending."),
]

# ── class registry ─────────────────────────────────────────────────────────────
CLASSES = {
    "08": ("class-08", CLASS08_STYLE, CLASS08),
    "09": ("class-09", CLASS09_STYLE, CLASS09),
    "10": ("class-10", CLASS10_STYLE, CLASS10),
    "11": ("class-11", CLASS11_STYLE, CLASS11),
    "12": ("class-12", CLASS12_STYLE, CLASS12),
}


def generate(out_dir: Path, filename: str, style_suffix: str, prompt: str) -> None:
    out_path = out_dir / filename
    if out_path.exists():
        print(f"  SKIP  {filename}  (already exists)")
        return

    full_prompt = f"{prompt}  {style_suffix}"
    print(f"  GEN   {filename} ...", end="", flush=True)
    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=full_prompt,
            size="1536x1024",
            quality="medium",
            n=1,
        )
        img_bytes = base64.b64decode(response.data[0].b64_json)
        out_path.write_bytes(img_bytes)
        print(f" saved ({out_path.stat().st_size // 1024} KB)")
    except Exception as exc:
        print(f" ERROR: {exc}")
    time.sleep(1)  # rate-limit pause


def run_class(class_id: str) -> None:
    folder, style_suffix, images = CLASSES[class_id]
    out_dir = BASE / folder
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n{'='*60}")
    print(f"  Class {class_id}  →  {out_dir}")
    print(f"  Images: {len(images)}")
    print(f"{'='*60}")
    for filename, prompt in images:
        generate(out_dir, filename, style_suffix, prompt)
    print(f"  Class {class_id} done.\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--class", dest="cls", default=None,
                        help="Generate only this class (08, 09, 10, 11, 12)")
    args = parser.parse_args()

    targets = [args.cls] if args.cls else list(CLASSES.keys())
    total = sum(len(CLASSES[c][2]) for c in targets)
    print(f"Generating {total} images for classes: {', '.join(targets)}")

    for cls in targets:
        run_class(cls)

    cost_per_img = 0.011  # gpt-image-1 medium 1536x1024
    print(f"\nEstimated cost: ${total * cost_per_img:.2f} USD")


if __name__ == "__main__":
    main()
