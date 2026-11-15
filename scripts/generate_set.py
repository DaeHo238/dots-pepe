#!/usr/bin/env python3
"""Generate several expressions in parallel from one base prompt and check the framing of each result.

Usage: generate_set.py <prompt file> <name> [expression key ...]
  Keys: smirk grin disappointed tears sob angry scream (all 7 if omitted)
  Output: <name>_<key>.png, <name>_<key>_512.png, <name>_<key>_prompt.txt
Only the `- Face:` line and the last line of the base prompt are swapped for each expression;
the rest (outfit, hand, background) is reused unchanged.
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))


def build(base_lines, face, face_end):
    out = list(base_lines)
    fi = next(i for i, l in enumerate(out) if l.startswith("- Face:"))
    out[fi] = "- Face: " + face
    ei = next(i for i, l in enumerate(out) if l.startswith("Do not add text"))
    out[ei] = "Do not add text, watermarks, extra characters, or extra hands. " + face_end
    return out


def run(job):
    key, prompt_path, out_name = job
    r = subprocess.run(["bash", os.path.join(HERE, "generate.sh"), prompt_path, out_name],
                       capture_output=True, text=True)
    return key, out_name, r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1:]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    prompt_file, name, *keys = sys.argv[1:]
    data = json.load(open(os.path.join(HERE, "expressions.json"), encoding="utf-8"))
    ex = data["expressions"]
    keys = keys or list(ex)
    unknown = [k for k in keys if k not in ex]
    if unknown:
        print("Unknown expression:", unknown, "| available:", list(ex))
        return 2

    base_lines = open(prompt_file, encoding="utf-8").read().split("\n")
    jobs = []
    for k in keys:
        out_name = f"{name}_{k}"
        path = f"{out_name}_prompt.txt"
        open(path, "w", encoding="utf-8").write("\n".join(build(base_lines, ex[k]["face"], data["face_end"])))
        jobs.append((k, path, out_name))

    print(f"Generating {len(jobs)} images in parallel ({', '.join(keys)}) ...", flush=True)
    with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
        results = list(pool.map(run, jobs))

    failed = 0
    for key, out_name, code, tail in results:
        if code != 0:
            failed += 1
            print(f"[FAILED] {key}: {tail}")
            continue
        chk = subprocess.run([sys.executable, os.path.join(HERE, "check_framing.py"), f"{out_name}_512.png", "--expr"],
                             capture_output=True, text=True)
        verdict = chk.stdout.strip().splitlines()[-1] if chk.stdout.strip() else "check unavailable"
        print(f"[done] {key:<13} {out_name}_512.png  | {verdict}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
