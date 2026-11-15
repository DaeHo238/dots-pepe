#!/bin/bash
# Codex CLI(GPT 이미지 생성)로 기준 Pepe를 편집해 이미지를 만든다.
# 사용법: generate.sh <프롬프트 파일> [출력 이름]
#   결과: <출력 이름>.png (원본 크기), <출력 이름>_512.png, <출력 이름>_codex.log
#   현재 디렉터리에 저장된다.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BASE="$SKILL_DIR/assets/pepe_base.png"
PROMPT_FILE="${1:?프롬프트 파일 경로가 필요합니다}"
OUT="${2:-pepe_remix}"

command -v codex >/dev/null || { echo "codex CLI가 없습니다. 'npm i -g @openai/codex' 로 설치하세요." >&2; exit 1; }
[ -f "$PROMPT_FILE" ] || { echo "프롬프트 파일이 없습니다: $PROMPT_FILE" >&2; exit 1; }

{
  echo "Use your built-in image generation tool to edit the attached reference image, then save the resulting PNG as ${OUT}.png in the current directory. Do not write code to draw it."
  echo
  cat "$PROMPT_FILE"
} | codex exec --skip-git-repo-check --sandbox workspace-write -i "$BASE" - > "${OUT}_codex.log" 2>&1

[ -f "${OUT}.png" ] || { echo "이미지가 만들어지지 않았습니다. 로그: ${OUT}_codex.log" >&2; tail -20 "${OUT}_codex.log" >&2; exit 1; }

# 512x512로 축소 (macOS 기본 sips 사용, 없으면 Pillow)
if command -v sips >/dev/null; then
  sips -z 512 512 "${OUT}.png" --out "${OUT}_512.png" >/dev/null
else
  python3 -c "from PIL import Image; Image.open('${OUT}.png').convert('RGB').resize((512,512),Image.BOX).save('${OUT}_512.png')"
fi

echo "완료: ${OUT}.png, ${OUT}_512.png"

# 구도 점검 (PIL이 있을 때만, 실패해도 생성은 성공으로 본다)
python3 "$SKILL_DIR/scripts/check_framing.py" "${OUT}_512.png" 2>/dev/null || true
