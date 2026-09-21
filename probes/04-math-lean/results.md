# Results: Math: Lean 4 proofs

12 theorem statements, 2 modes, 1 sample each. Run 2026-09-21 as Devin sessions (Fusion mode). Raw outputs in `outputs/<mode>/<problem>/sample_0.json`. Every output was compiled afterwards by me in a Lean project I built for the purpose: Lean 4.35.0-rc2, mathlib4 at 0653561 (tag v4.35.0-rc2).

| Mode | Date | Samples | Compiles / Total | Notes |
|---|---|---|---|---|
| tools | 2026-09-21 | 12 | 10 / 12 | p03 and p05 fail to compile; 2 of the 12 sessions built Lean themselves |
| notools | 2026-09-21 | 12 | 11 / 12 | p02 fails: uses an identifier that does not exist |

No output used `sorry`, `admit`, `native_decide` or an added axiom, and no output altered the theorem statement. Compiling items depend only on `propext`, `Classical.choice` and `Quot.sound`.

Per item PASS/FAIL with the first compiler error verbatim: `lean_grade_report.txt`.

Grade: `python probes/04-math-lean/key/grade_lean.py /path/to/mathlib-project`
