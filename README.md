# dots-pepe

Claude Code skill that remixes a pixel-art Pepe: the face shape, pose and framing stay fixed, and only the outfit, hand, background and expression change. Images are generated through the Codex CLI with `assets/pepe_base.png` as the reference.

## Install

```bash
git clone <this repo> ~/.claude/skills/dots-pepe
```

Needs the `codex` CLI (`npm i -g @openai/codex`) logged in. The reference image and prompt are sent to OpenAI when generating.

## Use

In Claude Code: `/dots-pepe 해적 페페 그려줘` (see `SKILL.md` for the four slots and expression options).
