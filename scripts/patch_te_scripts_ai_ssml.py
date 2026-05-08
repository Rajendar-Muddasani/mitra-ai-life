"""
Patch all 10 Telugu video scripts to fix AI pronunciation using SSML.
Handles two patterns:
  Pattern A (L1, L2): synthesis_input = gtts.SynthesisInput(text=text)
  Pattern B (L3-L10): input=gtts.SynthesisInput(text=text),

Run: python3 scripts/patch_te_scripts_ai_ssml.py
"""
import re
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent

# Pattern A (L1, L2)
PLAIN_A = "synthesis_input = gtts.SynthesisInput(text=text)"
SSML_A = (
    "# SSML fix: pronounce AI as individual letters (Ay + Eye)\n"
    "        _ssml = text.replace('ఏఐ', '<say-as interpret-as=\"characters\">AI</say-as>')\n"
    "        _ssml = re.sub(r'(?<![a-zA-Z])AI(?![a-zA-Z])', "
    "'<say-as interpret-as=\"characters\">AI</say-as>', _ssml)\n"
    "        synthesis_input = gtts.SynthesisInput(ssml=f'<speak>{_ssml}</speak>')"
)

# Pattern B (L3-L10): inline in synthesize_speech call
PLAIN_B = "input=gtts.SynthesisInput(text=text),"
SSML_B = (
    "input=gtts.SynthesisInput(ssml=(\n"
    "                '<speak>' +\n"
    "                re.sub(r'(?<![a-zA-Z])AI(?![a-zA-Z])',\n"
    "                    '<say-as interpret-as=\"characters\">AI</say-as>',\n"
    "                    text.replace('ఏఐ', '<say-as interpret-as=\"characters\">AI</say-as>')\n"
    "                ) + '</speak>'\n"
    "            )),"
)

te_scripts = sorted(SCRIPTS_DIR.glob("generate_level*_video_te.py"))
patched = 0

for script in te_scripts:
    content = script.read_text(encoding="utf-8")

    if "SynthesisInput(ssml=" in content:
        print(f"  [SKIP - already patched] {script.name}")
        continue

    changed = False
    if PLAIN_A in content:
        content = content.replace(PLAIN_A, SSML_A)
        changed = True
    elif PLAIN_B in content:
        content = content.replace(PLAIN_B, SSML_B)
        changed = True
    else:
        print(f"  [WARN - no pattern] {script.name}")
        continue

    # Ensure 're' is imported
    if "import re" not in content:
        content = content.replace("import os\n", "import os\nimport re\n", 1)

    script.write_text(content, encoding="utf-8")
    print(f"  [PATCHED] {script.name}")
    patched += 1

print(f"\nDone: {patched} scripts patched.")
