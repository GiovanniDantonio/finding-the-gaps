# Results: Math: long constructions

12 problems, 2 modes, 1 sample each so far. Run on 2026-09-21 as Devin sessions (Fusion mode). Every output is in `outputs/<mode>/<problem>/sample_0.json` with a link to the session.

| Mode | Date | Samples | Final answer correct | Construction valid (where checked) | Notes |
|---|---|---|---|---|---|
| tools | 2026-09-21 | 12 | 12 / 12 | 5 / 5 | used the shell on 5 of 12 problems (p01, p05, p06, p07, p09) |
| notools | 2026-09-21 | 12 | 12 / 12 | 4 / 5 | no tool use in any session; p06 construction has two collinear triples |

Constructions were checked by hand (with a short script) for p01, p04, p06, p09, p11. The grader only checks the final integer, so the construction column is manual.

Run: `python harness/run.py probes/01-math-constructions --modes tools,notools --samples 3`
Grade: `python harness/grade.py probes/01-math-constructions`
