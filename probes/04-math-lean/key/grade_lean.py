"""Compile every output in outputs/ inside a Mathlib project and report pass/fail.
Usage: python key/grade_lean.py /path/to/mathlib-project"""
import json, pathlib, re, subprocess, sys
proj = pathlib.Path(sys.argv[1]); here = pathlib.Path(__file__).parent; probe = here.parent
key = json.loads((here / "key.json").read_text())
rows = []
allowed = {"propext", "Classical.choice", "Quot.sound"}
for f in sorted(probe.glob("outputs/*/*/sample_*.json")):
    d = json.loads(f.read_text()); mode, p, sample = f.parts[-3], f.parts[-2], f.stem
    src = re.sub(r"^```(lean)?|```$", "", d["text"].strip(), flags=re.M).strip()
    note = []
    stmt_ok = key[p]["answer"] in src
    ok = stmt_ok and "sorry" not in src and "admit" not in src and "native_decide" not in src
    if ok:
        tmp = proj / f"FTG_{p}_{mode}_{sample}.lean"
        tmp.write_text(src + "\n\n#print axioms " + p + "\n")
        r = subprocess.run(["lake", "env", "lean", tmp.name], cwd=proj, capture_output=True, text=True, timeout=600)
        bad = re.findall(r"depends on axioms: \[(.*?)\]", r.stdout)
        ok = r.returncode == 0 and all(set(a.split(", ")) <= allowed for a in bad)
        if not ok:
            out = r.stdout + r.stderr
            errs = [l for l in out.splitlines() if re.search(r"\berror\b", l)]
            extra = [a for a in bad if not set(a.split(", ")) <= allowed]
            note = errs[:1] or ([f"extra axioms: {extra}"] if extra else out.strip().splitlines()[-1:])
    else:
        if not stmt_ok: note.append("statement altered (key statement not found verbatim)")
        if "sorry" in src: note.append("sorry present")
        if "admit" in src: note.append("admit present")
        if "native_decide" in src: note.append("native_decide present")
    note = " ".join(note)
    rows.append({"problem": p, "mode": mode, "sample": sample, "pass": ok, "note": note})
    print(p, mode, sample, "PASS" if ok else "FAIL", note[:120])
(here / "lean_grades.json").write_text(json.dumps(rows, indent=1) + "\n")
