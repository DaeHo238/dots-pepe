#!/bin/bash
# Edits the base Pepe with the Codex CLI (GPT image generation) and writes the image.
# Usage: generate.sh <prompt file> [output name]
#   Output: <name>.png (original size), <name>_512.png, <name>_codex.log
#   Files are written to the current directory.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BASE="$SKILL_DIR/assets/pepe_base.png"
PROMPT_FILE="${1:?A prompt file path is required}"
OUT="${2:-pepe_remix}"

command -v codex >/dev/null || { echo "codex CLI not found. Install it with: npm i -g @openai/codex" >&2; exit 1; }
[ -f "$PROMPT_FILE" ] || { echo "Prompt file not found: $PROMPT_FILE" >&2; exit 1; }

{
  echo "Use your built-in image generation tool to edit the attached reference image, then save the resulting PNG as ${OUT}.png in the current directory. Do not write code to draw it."
  echo
  cat "$PROMPT_FILE"
} | codex exec --skip-git-repo-check --sandbox workspace-write -i "$BASE" - > "${OUT}_codex.log" 2>&1

[ -f "${OUT}.png" ] || { echo "Image was not created. Log: ${OUT}_codex.log" >&2; tail -20 "${OUT}_codex.log" >&2; exit 1; }

# Scale down to 512x512 (macOS sips, or Pillow if sips is missing)
if command -v sips >/dev/null; then
  sips -z 512 512 "${OUT}.png" --out "${OUT}_512.png" >/dev/null
else
  python3 -c "from PIL import Image; Image.open('${OUT}.png').convert('RGB').resize((512,512),Image.BOX).save('${OUT}_512.png')"
fi

echo "Done: ${OUT}.png, ${OUT}_512.png"

# Framing check (only when PIL is available; a failure here does not fail the generation)
python3 "$SKILL_DIR/scripts/check_framing.py" "${OUT}_512.png" 2>/dev/null || true
