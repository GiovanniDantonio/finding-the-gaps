# Results: Software: build a small CLI tool end to end

Task in `problems/task.md`, acceptance in `key/acceptance.md`. The 12 acceptance cases in `key/cases/` were written and frozen before either session ran. The 6 cases in `key/stress/` were written afterwards to look for a gap the first 12 missed (escaped commas, nested VALARM, quoted TZID, bare LF endings, empty file, duplicate UID). One Devin session per mode, 2026-09-21.

| Mode | Date | Interventions | Acceptance (12) | Stress (6) | Notes |
|---|---|---|---|---|---|
| tools | 2026-09-21 | 0 | 12 / 12 | 6 / 6 | Ran the tool itself on its own inputs before answering |
| notools | 2026-09-21 | 0 | 12 / 12 | 6 / 6 | Written in one pass, never executed by the session |

Not deployed (a CLI has nothing to deploy). Probe 08 carries the deployment requirement.

Run: `python key/run_acceptance.py outputs/<mode>/icsdiff.py`
