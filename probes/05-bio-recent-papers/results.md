# Results: Biology: questions from post-cutoff open access papers

12 questions from 8 open access bioRxiv preprints posted 14 August to 19 September 2026, sources and quotes in `key/key.json`. One Devin session per question per mode, 1 sample, 2026-09-21. "Abstained" means the answer field was empty or said some form of "I don't know"; "Answered" is everything else.

| Mode | Correct / Answered | Abstained | Total |
|---|---|---|---|
| tools | 12 / 12 | 0 | 12 |
| notools | 0 / 4 | 8 | 12 |

No-tools answered items: p01 (said 50, paper says 70), p04 (300 vs 500), p09 (100000 vs 698631), p12 (4.4 vs 3.1). Every one of the four reasoning fields says it did not read the paper and is guessing.

Grade: `python harness/grade.py probes/05-bio-recent-papers`

## Prompt variants, no tools (added 2026-09-22)

Same twelve questions, same no-tools instruction, one sample each. Only the last paragraph of the prompt changed. Raw outputs in `outputs/notools-guessok/` and `outputs/notools-penalty/`, with the exact prompt in each file.

| Variant | Last paragraph says | Answered | Correct | Abstained |
|---|---|---|---|---|
| original | answer exactly; in the reasoning, say if you did not read it | 4 | 0 | 8 |
| guessok | guessing is fine, give a confidence in the reasoning | 12 | 1 | 0 |
| penalty | a wrong answer costs more than no answer; write `abstain` if you have not read it | 0 | 0 | 12 |

Under guessok, the stated confidences run from 1 to 35 percent, median about 15. The one hit (p10, answered 7 for 7) came with 15 percent. Under penalty every answer field is the single word `abstain` and every reasoning field says the paper was not read. So the split behaviour in the original run (four guesses, eight abstentions) sits between two prompts that each move it all the way to one side.
