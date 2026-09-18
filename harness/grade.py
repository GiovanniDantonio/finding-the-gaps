"""Grade saved outputs against key/key.json and print a results table.

Usage: python harness/grade.py probes/<slug>
"""
import json, pathlib, sys, collections

def grade(answer: str, text: str, grader: str) -> bool | None:
    if grader == "exact": return text.strip().splitlines()[-1].strip() == answer.strip()
    if grader == "numeric":
        try: return abs(float(text.strip().splitlines()[-1]) - float(answer)) < 1e-6
        except ValueError: return False
    return None  # lean / manual: graded by hand, fill results.md directly

def main():
    probe = pathlib.Path(sys.argv[1])
    key = json.loads((probe / "key" / "key.json").read_text())
    tally = collections.defaultdict(lambda: [0, 0])
    for f in (probe / "outputs").rglob("sample_*.json"):
        r = json.loads(f.read_text()); k = key[r["problem"]]
        ok = grade(k["answer"], r["text"], k["grader"])
        if ok is None: continue
        tally[r["model"]][1] += 1; tally[r["model"]][0] += ok
    print("| Model | Correct / Total |\n|---|---|")
    for m, (c, t) in sorted(tally.items()): print(f"| {m} | {c} / {t} |")

if __name__ == "__main__":
    main()
