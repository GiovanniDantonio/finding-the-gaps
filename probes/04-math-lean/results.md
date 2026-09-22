# Results: Math: Lean 4 proofs

12 theorem statements, 2 modes, 1 sample each. Run 2026-09-21 as Devin sessions (Fusion mode). Raw outputs in `outputs/<mode>/<problem>/sample_0.json`. Every output was compiled afterwards by me in a Lean project I built for the purpose: Lean 4.35.0-rc2, mathlib4 at 0653561 (tag v4.35.0-rc2).

| Mode | Date | Samples | Compiles / Total | Notes |
|---|---|---|---|---|
| tools | 2026-09-21 | 12 | 10 / 12 | p03 and p05 fail to compile; 2 of the 12 sessions built Lean themselves |
| notools | 2026-09-21 | 12 | 11 / 12 | p02 fails: uses an identifier that does not exist |

No output used `sorry`, `admit`, `native_decide` or an added axiom, and no output altered the theorem statement. Compiling items depend only on `propext`, `Classical.choice` and `Quot.sound`.

Per item PASS/FAIL with the first compiler error verbatim: `lean_grade_report.txt`.

Grade: `python probes/04-math-lean/key/grade_lean.py /path/to/mathlib-project`

## Follow-up (2026-09-22): three more no-tools samples, and tools with an explicit compile instruction

Grader updated: `grade_lean.py` now names temp files by sample, rejects `admit` and `native_decide` alongside `sorry`, and writes `key/lean_grades.json` (72 rows). All 72 outputs recompiled in the same project (Lean 4.35.0-rc2, mathlib4 at v4.35.0-rc2).

| Mode | Samples | Compiles | Fails |
|---|---|---|---|
| notools s0 (original) | 12 | 11 | p02 |
| notools s1 | 12 | 9 | p05, p07, p09 |
| notools s2 | 12 | 9 | p04, p08, p09 |
| notools s3 | 12 | 11 | p09 |
| notools, all four | 48 | 40 | |
| tools s0 (original prompt) | 12 | 10 | p03, p05 |
| tools-lean s0 (told to install and compile) | 12 | 12 | |

The `tools-lean` prompt adds one paragraph: install Lean 4 and Mathlib with elan and `lake exe cache get`, compile before submitting, this takes about twenty minutes and is part of the task. All twelve sessions did it and all twelve say so in the reasoning field, with the toolchain named (nine on 4.35.0-rc2 or Mathlib master, three on 4.34.0). All twelve compile in my project too. Every no-tools reasoning field, all 48, states plainly that the proof was not compiled.

No-tools failure modes across the eight misses: four are identifiers that do not exist in Mathlib (`even_or_odd`, `Nat.sum_range_id`, `Nat.exists_prime_gt`, `nat_sub_dvd_pow_sub_pow`), two are `linarith` failing to close a goal, two are `positivity` applied to a goal it does not handle. p09 (a divisibility statement about powers) fails on three of four samples, each in a different way. No output in any mode used `sorry`, `admit`, `native_decide`, an extra axiom, or an altered statement.

The original tools-vs-notools comparison (10 vs 11) was a comparison between sessions that mostly did not have Lean and sessions that could not have it. With the checker actually installed, the comparison is 12 of 12 against 40 of 48.
