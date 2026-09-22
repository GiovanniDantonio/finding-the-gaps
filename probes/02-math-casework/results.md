# Results: Math: heavy casework

12 counting problems, 2 modes, 1 sample each. Run on 2026-09-21 as Devin sessions (Fusion mode). Raw outputs in `outputs/<mode>/<problem>/sample_0.json`, each with a session link.

| Mode | Date | Samples | Correct / Total | Notes |
|---|---|---|---|---|
| tools | 2026-09-21 | 12 | 12 / 12 | wrote a brute-force script on every problem |
| notools | 2026-09-21 | 12 | 11 / 12 | p08 wrong: 5544 instead of 11880, dropped a factor of 3 in one case |

Run: `python harness/run.py probes/02-math-casework --modes tools,notools --samples 3`
Grade: `python harness/grade.py probes/02-math-casework`

## Three more no-tools samples (2026-09-22)

Same prompt, same mode, `sample_1` to `sample_3` for all twelve problems.

| | s0 | s1 | s2 | s3 | correct |
|---|---|---|---|---|---|
| p07 (key 251) | ok | ok | 254 | 267 | 2 / 4 |
| p08 (key 11880) | 5544 | 97416 | ok | ok | 2 / 4 |
| other ten | ok | ok | ok | ok | 40 / 40 |

44 of 48 overall, 11 of 12 on every sample, but not the same problem each time. Ten problems never miss. p07 and p08 each miss twice with three different wrong numbers between them. A majority vote over the four samples gets both right (251 has two votes against two singletons; 11880 likewise). The p08 wrong answers are each a different casework error: sample 0 dropped a factor of 3, sample 1 overcounted by a factor of about 8.

## Lite tier, no tools, one sample (2026-09-22)

Same no-tools prompt run as a Devin Lite session, `outputs/notools-lite/`. 8 of 12: p01 (3540), p05 (63), p07 (254), p12 (856) wrong. This is one sample of one alternative tier on one probe and is reported as a data point, not a ranking. The p07 miss repeats a number (254) that the default tier also produced once.
