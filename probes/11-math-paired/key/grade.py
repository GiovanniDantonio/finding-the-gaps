"""Grade probe 11: exact integer match, plus the model's own EXACT / RECALLED / ESTIMATED label.
Usage: python probes/11-math-paired/key/grade.py"""
import json, pathlib, re

here = pathlib.Path(__file__).parent; probe = here.parent
key = json.loads((here / "key.json").read_text())
LABEL = re.compile(r"\b(EXACT|RECALLED|ESTIMATED)\b")
rows = []
for f in sorted(probe.glob("outputs/*/*/sample_*.json")):
    d = json.loads(f.read_text()); mode, p = f.parts[-3], f.parts[-2]
    ans = d["text"].strip().replace(",", "")
    labels = LABEL.findall(d["reasoning"])
    rows.append({"problem": p, "mode": mode, "sample": f.stem, "answer": ans,
                 "correct": ans == key[p], "label": labels[-1] if labels else "none"})
(here / "grades.json").write_text(json.dumps(rows, indent=1) + "\n")
for half in "pq":
    for mode in sorted({r["mode"] for r in rows}):
        sub = [r for r in rows if r["mode"] == mode and r["problem"][0] == half]
        print(f"{half} {mode:8s} {sum(r['correct'] for r in sub)} / {len(sub)}")
print()
print("| item | key | " + " | ".join(sorted({r['mode'] for r in rows})) + " |")
for p in sorted(key):
    cells = []
    for mode in sorted({r["mode"] for r in rows}):
        rr = [r for r in rows if r["problem"] == p and r["mode"] == mode]
        cells.append(", ".join(("ok" if r["correct"] else r["answer"]) + " (" + r["label"] + ")" for r in rr) or "--")
    print(f"| {p} | {key[p]} | " + " | ".join(cells) + " |")
