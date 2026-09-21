import json, pathlib, subprocess, sys
tool = sys.argv[1]; d = pathlib.Path(__file__).parent / "cases"; passed = 0
for e in sorted(d.glob("*_expected.json")):
    k = e.name[:2]; exp = json.loads(e.read_text())
    r = subprocess.run([sys.executable, tool, d/f"{k}_old.ics", d/f"{k}_new.ics"], capture_output=True, text=True, timeout=30)
    ok = r.returncode == exp["exit"] and (exp["stdout"] is None and r.stdout == "" and r.stderr.strip() != "" or r.stdout == exp["stdout"])
    passed += ok
    print(k, "PASS" if ok else "FAIL", "" if ok else f"exit={r.returncode} stdout={r.stdout!r} stderr={r.stderr.strip()[:100]!r}")
print(f"{passed} / 12")
