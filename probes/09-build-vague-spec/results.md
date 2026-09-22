# Results: Software: four one-sentence specs

Four tasks in `problems/`, one sentence each plus the output format rule. Hidden checks in `key/run_acceptance.py`, written before any session ran, tagged `hard` (any reading of the sentence must pass) or `judgment` (the sentence does not decide it; passes for any listed reasonable behaviour, fails only on a crash or nonsense). One Devin session per (task, mode), 2026-09-21. Raw outputs with session links in `outputs/`; the extracted `.py` files sit beside each `sample_0.json`.

| Task | Mode | Hard | Judgment | Hard failures |
|---|---|---|---|---|
| t01 dedupe.py | tools | 6 / 6 | 2 / 2 | |
| t01 dedupe.py | notools | 6 / 6 | 2 / 2 | |
| t02 wordfreq.py | tools | 6 / 7 | 2 / 2 | missing input file: raw traceback, exit 1 |
| t02 wordfreq.py | notools | 6 / 7 | 2 / 2 | missing input file: raw traceback, exit 1 |
| t03 jsonflat.py | tools | 4 / 5 | 3 / 4 | `{}` in gives `{"": {}}` out |
| t03 jsonflat.py | notools | 4 / 5 | 3 / 4 | `{}` in gives `{"": {}}` out |
| t04 datediff.py | tools | 6 / 6 | 3 / 3 | |
| t04 datediff.py | notools | 6 / 6 | 3 / 3 | |
| total | tools | 22 / 24 | 10 / 11 | |
| total | notools | 22 / 24 | 10 / 11 | |

The one judgment failure (both modes, t03) is a key that already contains a dot colliding with a flattened path: both scripts silently keep one value and drop the other. Both sessions named this in the reasoning field as a decision ("last write wins"), so it is a documented choice rather than an oversight, but the check asked for both values or a clear error and it delivered neither.

The tools sessions all report running their script on inputs they made up. None of those inputs was an empty object, a missing file, or a colliding key.

Run: `python key/run_acceptance.py t03 outputs/tools/t03/jsonflat.py`
