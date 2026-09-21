"""Grade saved outputs against key/key.json and print a results table.

Usage: python harness/grade.py probes/<slug>
"""
import json, pathlib, re, sys, collections

ABSTAIN = re.compile(r"^\s*$|i don'?t know|unknown|not (?:read|have|know)|no (?:idea|memory)|cannot", re.I)

def norm(s: str) -> str:
    s = s.strip().split("\n")[0]
    s = re.sub(r"[,%]|\bug/mL\b|Å|angstroms?|\bbp\b|\bcells?\b", "", s, flags=re.I)
    return s.strip().strip(".").strip()

def grade(answer: str, text: str, grader: str) -> bool | None:
    if ABSTAIN.match(text.strip()): return None
    if grader == "exact": return norm(text).lower() == norm(answer).lower()
    if grader == "numeric":
        try: return abs(float(norm(text)) - float(answer)) < 1e-6
        except ValueError: return False
    return None  # lean / manual: graded by hand, fill results.md directly

def main():
    probe = pathlib.Path(sys.argv[1])
    key = json.loads((probe / "key" / "key.json").read_text())
    tally = collections.defaultdict(lambda: [0, 0, 0])  # correct, answered, abstained
    for f in (probe / "outputs").rglob("sample_*.json"):
        r = json.loads(f.read_text()); k = key[r["problem"]]
        if k["grader"] not in ("exact", "numeric"): continue
        ok = grade(k["answer"], r["text"], k["grader"])
        t = tally[r["model"]]
        if ok is None: t[2] += 1
        else: t[1] += 1; t[0] += ok
    print("| Model | Correct / Answered | Abstained |\n|---|---|---|")
    for m, (c, a, ab) in sorted(tally.items()): print(f"| {m} | {c} / {a} | {ab} |")

if __name__ == "__main__":
    main()
