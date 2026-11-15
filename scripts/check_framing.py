#!/usr/bin/env python3
"""Measure how far the head position and size in a generated image differ from the base image.

Usage: check_framing.py <image> [--base base_image] [--tol 0.04] [--expr]
Uses the position and width of the lips (orange-brown, #C8783A) to see whether the head moved or grew.
Hats, helmets and a green body do not affect it, so it is more reliable than looking at green pixels.
  mouth x / mouth y : center of the mouth (% of the image size)  -> WARN if off by more than tol (default 4 points)
  mouth width       : ratio to the base -> WARN outside 0.88-1.12x (0.65-1.30x with --expr)
Exit code 1 on WARN. SKIP (exit code 0) if no lips are found (full-face mask, mouth covered by a prop).
Expressions that change the mouth shape (wide open mouth, tears) can change the width, so also check by eye.
"""
import argparse
import os
import sys

from PIL import Image

DEFAULT_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "pepe_base.png")


def lips_component(img):
    """Return the bounding box (as ratios) of the largest connected blob of lip-colored (orange-brown) pixels."""
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
                    help="for images with a changed expression (the mouth shape differs), widen the allowed mouth width range")
    args = ap.parse_args()

    base = measure(args.base)
    cur = measure(args.image)
    if base is None:
        print("Could not measure the base image.", file=sys.stderr)
        return 2
    if cur is None:
        print("SKIP: no lips found (full-face mask, mouth covered by a prop, etc.). Check by eye.")
        return 0

    bad = []
    print(f"{'item':<12}{'base':>8}{'result':>8}{'diff':>9}")
    for k, label in (("cx", "mouth x"), ("cy", "mouth y")):
        d = cur[k] - base[k]
        flag = ""
        if abs(d) > args.tol:
            flag = "  <-- off"
            bad.append(k)
        print(f"{label:<12}{base[k]*100:>7.1f}%{cur[k]*100:>7.1f}%{d*100:>+7.1f}pt{flag}")
    ratio = cur["w"] / base["w"]
    flag = ""
    lo, hi = (0.65, 1.30) if args.expr else (0.88, 1.12)
    if not (lo <= ratio <= hi):
        flag = "  <-- off"
        bad.append("w")
    print(f"{'mouth width':<12}{base['w']*100:>7.1f}%{cur['w']*100:>7.1f}%{ratio:>8.2f}x{flag}")
    if bad:
        print("WARN: the head may have moved or grown from the base framing -> check the image by eye and consider regenerating.")
        return 1
    print("PASS: head position and size are within the base range.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
