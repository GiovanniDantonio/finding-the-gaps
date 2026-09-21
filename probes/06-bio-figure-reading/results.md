# Results: Biology: reading numbers off figures and legends

12 questions from 3 open access bioRxiv preprints posted 4 to 14 September 2026, sources and quotes in `key/key.json`. Eight questions have a value in the paper; four are traps where the value is not reported and the right answer is "not reported". One Devin session per question per mode, 1 sample, 2026-09-21.

Nine of the tools sessions were re-run once: the first prompts referred to the paper by a shorthand ("the same uterus preprint") and several sessions said they could not tell which paper was meant. The re-run prompts name the paper and date in full. Only the re-run outputs are in `outputs/`.

| Mode | Correct / Answered | Abstained | Total |
|---|---|---|---|
| tools | 12 / 12 | 0 | 12 |
| notools | 0 / 3 | 9 | 12 |

Tools got all four traps right ("not reported") and all eight values right. No-tools answered "not reported" on three questions whose values are in the paper (p02, p06, p07); the reasoning says in each case that it had not read the paper.

Grader notes: "four" is normalized to 4, and an answer starting "Unable to verify" is counted as an abstention. Both changes are in `harness/grade.py`; the raw outputs are untouched.

Grade: `python harness/grade.py probes/06-bio-figure-reading`
