"""Compile every output in outputs/ inside a Mathlib project and report pass/fail.
Usage: python key/grade_lean.py /path/to/mathlib-project"""
import json, pathlib, re, subprocess, sys
proj = pathlib.Path(sys.argv[1]); here = pathlib.Path(__file__).parent; probe = here.parent
key = json.loads((here / "key.json").read_text())
rows = []
for f in sorted(probe.glob("outputs/*/*/sample_*.json")):
    d = json.loads(f.read_text()); mode, p = f.parts[-3], f.parts[-2]
    src = re.sub(r"^```(lean)?|```$", "", d["text"].strip(), flags=re.M).strip()
    ok = key[p]["answer"] in src and "sorry" not in src
    if ok:
        tmp = proj / f"FTG_{p}_{mode}.lean"
        tmp.write_text(src + "\n\n#print axioms " + p + "\n")
        r = subprocess.run(["lake", "env", "lean", tmp.name], cwd=proj, capture_output=True, text=True, timeout=600)
        bad = re.findall(r"depends on axioms: \[(.*?)\]", r.stdout)
        ok = r.returncode == 0 and all(set(a.split(", ")) <= {"propext", "Classical.choice", "Quot.sound"} for a in bad)
        note = (r.stdout + r.stderr).strip().splitlines()[-1:] if not ok else []
    else:
        note = ["statement changed or sorry present"]
    rows.append((p, mode, f.name, ok, " ".join(note)))
    print(p, mode, "PASS" if ok else "FAIL", " ".join(note)[:120])
