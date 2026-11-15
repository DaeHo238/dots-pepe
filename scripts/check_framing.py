#!/usr/bin/env python3
"""생성 이미지의 머리 위치·크기가 기준 이미지와 얼마나 다른지 잰다.

사용법: check_framing.py <이미지> [--base 기준이미지] [--tol 0.04]
입술(주황갈색, #C8783A)의 위치와 폭으로 머리가 움직이거나 커졌는지 본다.
모자·헬멧·초록 몸통에 영향받지 않아서 초록 픽셀 기준보다 믿을 만하다.
  입 가로 / 입 세로 : 입 중심 위치 (이미지 크기 대비 %)  -> tol(기본 4%p) 넘으면 WARN
  입 폭            : 기준 대비 비율 -> 0.88~1.12배 밖이면 WARN (--expr이면 0.65~1.30배)
WARN이면 종료 코드 1. 입을 찾지 못하면(전체 가면, 입을 크게 벌린 표정 등) SKIP, 종료 코드 0.
입을 크게 벌리거나 눈물 등으로 입 모양이 달라지는 표정은 폭이 달라질 수 있으니 눈으로 함께 확인한다.
"""
import argparse
import os
import sys

from PIL import Image

DEFAULT_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "pepe_base.png")


def lips_component(img):
    """입술 색(주황갈색)의 연결 덩어리 중 가장 큰 것의 경계 상자를 비율로 돌려준다."""
    w, h = img.size
    px = img.load()
    x0, x1, y0, y1 = int(w * 0.35), int(w * 0.95), int(h * 0.35), int(h * 0.68)

    def is_lip(x, y):
        r, g, b = px[x, y]
        return 165 <= r <= 255 and 90 <= g <= 170 and 25 <= b <= 95

    seen = set()
    best = None
    for y in range(y0, y1):
        for x in range(x0, x1):
            if (x, y) in seen or not is_lip(x, y):
                continue
            stack, comp = [(x, y)], []
            seen.add((x, y))
            while stack:
                cx, cy = stack.pop()
                comp.append((cx, cy))
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if x0 <= nx < x1 and y0 <= ny < y1 and (nx, ny) not in seen and is_lip(nx, ny):
                        seen.add((nx, ny))
                        stack.append((nx, ny))
            if best is None or len(comp) > len(best):
                best = comp
    if not best or len(best) < 150:
        return None
    xs = [c[0] for c in best]
    ys = [c[1] for c in best]
    return (min(xs) / w, max(xs) / w, min(ys) / h, max(ys) / h)


def measure(path):
    img = Image.open(path).convert("RGB").resize((512, 512), Image.NEAREST)
    box = lips_component(img)
    if box is None:
        return None
    l, r, t, b = box
    return {"cx": (l + r) / 2, "cy": (t + b) / 2, "w": r - l}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--tol", type=float, default=0.04)
    ap.add_argument("--expr", action="store_true",
                    help="표정을 바꾼 이미지(입 모양이 달라짐)면 입 폭 허용 범위를 넓힌다")
    args = ap.parse_args()

    base = measure(args.base)
    cur = measure(args.image)
    if base is None:
        print("기준 이미지를 측정하지 못했습니다.", file=sys.stderr)
        return 2
    if cur is None:
        print("SKIP: 입술을 찾지 못했습니다 (가면, 입을 가린 소품 등). 눈으로 확인하세요.")
        return 0

    bad = []
    print(f"{'항목':<8}{'기준':>8}{'결과':>8}{'차이':>9}")
    for k, label in (("cx", "입 가로"), ("cy", "입 세로")):
        d = cur[k] - base[k]
        flag = ""
        if abs(d) > args.tol:
            flag = "  <-- 벗어남"
            bad.append(k)
        print(f"{label:<8}{base[k]*100:>7.1f}%{cur[k]*100:>7.1f}%{d*100:>+8.1f}%p{flag}")
    ratio = cur["w"] / base["w"]
    flag = ""
    lo, hi = (0.65, 1.30) if args.expr else (0.88, 1.12)
    if not (lo <= ratio <= hi):
        flag = "  <-- 벗어남"
        bad.append("w")
    print(f"{'입 폭':<8}{base['w']*100:>7.1f}%{cur['w']*100:>7.1f}%{ratio:>8.2f}배{flag}")
    if bad:
        print("WARN: 머리가 기준 구도에서 벗어났을 수 있습니다 -> 이미지를 눈으로 확인하고 재생성을 고려하세요.")
        return 1
    print("PASS: 머리 위치와 크기가 기준 범위 안입니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
