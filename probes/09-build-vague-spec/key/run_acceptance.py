"""Hidden acceptance checks for the one-sentence tasks.

Usage: python key/run_acceptance.py t01 path/to/dedupe.py

Each check is tagged:
  hard     any reasonable reading of the sentence has to pass this
  judgment the sentence does not decide it; passes if the behaviour is one of the listed reasonable ones
Checks were written before any output was read.
"""
import json, subprocess, sys, tempfile

def run(tool, args=(), stdin=""):
    r = subprocess.run([sys.executable, tool, *args], input=stdin, capture_output=True, text=True, timeout=30)
    return r.returncode, r.stdout, r.stderr

def lines(s): return [l for l in s.replace("\r\n", "\n").split("\n") if l != ""]

def t01(tool):
    c = []
    rc, out, _ = run(tool, stdin="a,b\n1,2\n1,2\n3,4\n")
    c.append(("hard", "exact duplicate row removed, order kept", rc == 0 and lines(out) == ["a,b", "1,2", "3,4"]))
    rc, out, _ = run(tool, stdin="a,b\n3,4\n1,2\n3,4\n1,2\n")
    c.append(("hard", "first occurrence kept", rc == 0 and lines(out) == ["a,b", "3,4", "1,2"]))
    rc, out, _ = run(tool, stdin="a,b\n\"x,y\",1\n\"x,y\",1\nx,\"y,1\"\n")
    c.append(("hard", "quoted commas: rows compared as fields, not text", rc == 0 and len(lines(out)) == 3))
    rc, out, _ = run(tool, stdin="a,b\r\n1,2\r\n1,2\r\n")
    c.append(("hard", "CRLF input dedupes", rc == 0 and len(lines(out)) == 2))
    rc, out, _ = run(tool, stdin="")
    c.append(("hard", "empty input: exit 0, no traceback", rc == 0 and "Traceback" not in _))
    rc, out, _ = run(tool, stdin="a,b\n")
    c.append(("hard", "header only: header preserved", rc == 0 and lines(out) == ["a,b"]))
    rc, out, _ = run(tool, stdin="a,b\n1,2\n1, 2\n")
    c.append(("judgment", "'1,2' vs '1, 2': either both kept (exact) or one kept (trimmed), not a crash", rc == 0 and len(lines(out)) in (2, 3)))
    rc, out, _ = run(tool, stdin="x\nx\nx\n")
    c.append(("judgment", "row equal to header: header kept once, data 'x' kept 0 or 1 times", rc == 0 and lines(out) in (["x"], ["x", "x"])))
    return c

def t02(tool):
    c = []
    def go(text, args=()):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write(text); p = f.name
        return run(tool, [p, *args])
    rc, out, _ = go("the cat the dog the bird cat")
    c.append(("hard", "counts right, most common first", rc == 0 and lines(out) and lines(out)[0].split()[0].strip(":,") == "the"))
    c.append(("hard", "output has one word per line with a count", rc == 0 and all(any(tok.isdigit() for tok in l.replace(":", " ").replace(",", " ").split()) for l in lines(out))))
    rc, out, _ = go("The the THE tHe")
    c.append(("judgment", "case: folded to one line, or four lines, not a crash", rc == 0 and len(lines(out)) in (1, 4)))
    rc, out, _ = go("dog. dog, dog! dog? (dog) \"dog\"")
    c.append(("hard", "punctuation next to a word does not make new words", rc == 0 and len(lines(out)) == 1 and "6" in lines(out)[0]))
    rc, out, _ = go("don't don't can't")
    c.append(("judgment", "apostrophes: either kept (2 words) or split (3 or 4 tokens), no crash", rc == 0 and 2 <= len(lines(out)) <= 4))
    rc, out, _ = go("a b c")
    c.append(("hard", "fewer than ten distinct words: prints what exists, no padding, no crash", rc == 0 and len(lines(out)) == 3))
    rc, out, _ = go("")
    c.append(("hard", "empty file: exit 0, no traceback", rc == 0 and "Traceback" not in _))
    rc, out, _ = go("naïve naïve café")
    c.append(("hard", "non-ascii letters stay inside words", rc == 0 and len(lines(out)) == 2))
    rc, out, err = run(tool, ["/nonexistent/file.txt"])
    c.append(("hard", "missing file: nonzero exit, message, no traceback", rc != 0 and "Traceback" not in err))
    return c

def t03(tool):
    c = []
    def go(obj):
        rc, out, err = run(tool, stdin=json.dumps(obj))
        try: parsed = json.loads(out)
        except Exception: parsed = None
        return rc, out, err, parsed
    rc, out, err, p = go({"a": {"b": 1, "c": {"d": 2}}, "e": 3})
    c.append(("hard", "nested keys become dotted", rc == 0 and p == {"a.b": 1, "a.c.d": 2, "e": 3}))
    c.append(("hard", "output is valid JSON", p is not None))
    rc, out, err, p = go({"a": [1, {"b": 2}]})
    c.append(("judgment", "arrays: indexed (a.0, a.1.b) or left as values, not a crash", rc == 0 and p in ({"a.0": 1, "a.1.b": 2}, {"a[0]": 1, "a[1].b": 2}, {"a": [1, {"b": 2}]})))
    rc, out, err, p = go({"a": {}, "b": None, "c": ""})
    c.append(("hard", "null and empty string survive as values", rc == 0 and p is not None and p.get("b", "missing") is None and p.get("c") == ""))
    c.append(("judgment", "empty object: dropped or kept as {} , not a crash", rc == 0 and p is not None and p.get("a", "dropped") in ({}, "dropped")))
    rc, out, err, p = go({"a.b": 1, "a": {"b": 2}})
    c.append(("judgment", "key already containing a dot: any output, but both values present or a clear error", (rc == 0 and p is not None and sorted(p.values()) == [1, 2]) or (rc != 0 and "Traceback" not in err)))
    rc, out, err, p = go({})
    c.append(("hard", "empty object in: {} out", rc == 0 and p == {}))
    rc, out, err, p = go([1, 2])
    c.append(("judgment", "top-level array: indexed keys or a clean error, no traceback", (rc == 0 and p is not None) or (rc != 0 and "Traceback" not in err)))
    rc, out, err = run(tool, stdin="{not json")
    c.append(("hard", "malformed input: nonzero exit, message, no traceback", rc != 0 and "Traceback" not in err))
    return c

def t04(tool):
    c = []
    def go(*a):
        rc, out, err = run(tool, list(a)); return rc, out.strip(), err
    rc, out, _ = go("2026-01-01", "2026-01-11")
    c.append(("hard", "ISO dates, ten days", rc == 0 and out.lstrip("+") == "10"))
    rc, out, _ = go("2026-01-11", "2026-01-01")
    c.append(("judgment", "reversed order: 10 or -10", rc == 0 and out in ("10", "-10")))
    rc, out, _ = go("2024-02-28", "2024-03-01")
    c.append(("hard", "leap year counted", rc == 0 and out.lstrip("+") == "2"))
    rc, out, _ = go("2026-05-05", "2026-05-05")
    c.append(("hard", "same day: 0", rc == 0 and out == "0"))
    rc, out, _ = go("2026-03-01", "2026-03-31")
    c.append(("judgment", "output is a bare integer, or integer plus the word days", rc == 0 and out.split()[0].lstrip("+-").isdigit()))
    rc, out, err = go("2026-02-30", "2026-03-01")
    c.append(("hard", "invalid date: nonzero exit, message, no traceback", rc != 0 and "Traceback" not in err))
    rc, out, err = go("2026-01-01")
    c.append(("hard", "one argument: nonzero exit, usage, no traceback", rc != 0 and "Traceback" not in err))
    rc, out, _ = go("1900-01-01", "2100-01-01")
    c.append(("hard", "far apart dates", rc == 0 and out.lstrip("+") == "73049"))
    rc, out, err = go("01/02/2026", "01/03/2026")
    c.append(("judgment", "non-ISO format: accepted with a consistent reading, or rejected cleanly", (rc == 0 and out.lstrip("+-").isdigit()) or (rc != 0 and "Traceback" not in err)))
    return c

if __name__ == "__main__":
    task, tool = sys.argv[1], sys.argv[2]
    checks = globals()[task](tool)
    hp = sum(ok for kind, _, ok in checks if kind == "hard"); ht = sum(kind == "hard" for kind, _, _ in checks)
    jp = sum(ok for kind, _, ok in checks if kind == "judgment"); jt = sum(kind == "judgment" for kind, _, _ in checks)
    for kind, name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'} [{kind}] {name}")
    print(f"hard {hp}/{ht}  judgment {jp}/{jt}")
