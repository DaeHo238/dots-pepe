#!/usr/bin/env python3
"""기본 프롬프트 한 개로 표정 여러 장을 병렬 생성하고, 각 결과의 구도를 점검한다.

사용법: generate_set.py <프롬프트 파일> <이름> [표정 키 ...]
  표정 키: smirk grin disappointed tears sob angry scream (생략하면 7개 전부)
  결과: <이름>_<표정>.png, <이름>_<표정>_512.png, <이름>_<표정>_prompt.txt
기본 프롬프트에서 `- Face:` 줄과 마지막 줄의 표정 문구만 바꾸고 나머지(옷, 손, 배경)는 그대로 쓴다.
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
        print("알 수 없는 표정:", unknown, "| 가능:", list(ex))
        return 2

    base_lines = open(prompt_file, encoding="utf-8").read().split("\n")
    jobs = []
    for k in keys:
        out_name = f"{name}_{k}"
        path = f"{out_name}_prompt.txt"
        open(path, "w", encoding="utf-8").write("\n".join(build(base_lines, ex[k]["face"], data["face_end"])))
        jobs.append((k, path, out_name))

    print(f"{len(jobs)}장을 병렬 생성합니다 ({', '.join(ex[k]['ko'] for k in keys)}) ...", flush=True)
    with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
        results = list(pool.map(run, jobs))

    failed = 0
    for key, out_name, code, tail in results:
        if code != 0:
            failed += 1
            print(f"[실패] {ex[key]['ko']}: {tail}")
            continue
        chk = subprocess.run([sys.executable, os.path.join(HERE, "check_framing.py"), f"{out_name}_512.png", "--expr"],
                             capture_output=True, text=True)
        verdict = chk.stdout.strip().splitlines()[-1] if chk.stdout.strip() else "점검 불가"
        print(f"[완료] {ex[key]['ko']:<4} {out_name}_512.png  | {verdict}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
