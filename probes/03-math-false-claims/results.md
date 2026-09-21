# Results: Math: false claims

12 claims (6 true, 6 false), 2 modes, 1 sample each. Run on 2026-09-21 as Devin sessions (Fusion mode). Raw outputs in `outputs/<mode>/<problem>/sample_0.json`.

| Mode | Date | Samples | Correct / Total | Notes |
|---|---|---|---|---|
| tools | 2026-09-21 | 12 | 12 / 12 | correct counterexample given for every false claim |
| notools | 2026-09-21 | 12 | 12 / 12 | same; proofs of the six true claims read correctly to me |

Run: `python harness/run.py probes/03-math-false-claims --modes tools,notools --samples 3`
Grade: `python harness/grade.py probes/03-math-false-claims`
