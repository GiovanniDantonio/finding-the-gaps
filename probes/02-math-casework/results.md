# Results: Math: heavy casework

12 counting problems, 2 modes, 1 sample each. Run on 2026-09-21 as Devin sessions (Fusion mode). Raw outputs in `outputs/<mode>/<problem>/sample_0.json`, each with a session link.

| Mode | Date | Samples | Correct / Total | Notes |
|---|---|---|---|---|
| tools | 2026-09-21 | 12 | 12 / 12 | wrote a brute-force script on every problem |
| notools | 2026-09-21 | 12 | 11 / 12 | p08 wrong: 5544 instead of 11880, dropped a factor of 3 in one case |

Run: `python harness/run.py probes/02-math-casework --modes tools,notools --samples 3`
Grade: `python harness/grade.py probes/02-math-casework`
