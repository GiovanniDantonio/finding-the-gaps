# Key

`run_acceptance.py TASK FILE` runs the hidden checks for one task. Each check is tagged `hard` (any reasonable reading of the one sentence must pass) or `judgment` (the sentence does not decide it; the check passes for any of the listed reasonable behaviours and fails only on a crash or a nonsense result). The checks were written before any output was read and were sanity-checked against two 10-line reference implementations, which are not part of the probe.

Score reported as hard x/y, judgment x/y. The question the probe asks is whether the model fills in unstated requirements the way a careful engineer would, so the hard failures are the finding and the judgment column is context.

There is no `key.json`: the grader is the acceptance script, not an answer string. Example: `python key/run_acceptance.py t03 outputs/tools/t03/jsonflat.py`.
