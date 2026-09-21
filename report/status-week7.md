# Status report, week 7

CS 91r, Fall 2026. Giovanni D'Antonio. Supervisor: Christopher Thorpe.

## Where things stand

Eight probes written, run once, graded and written up. Repository is public with every raw output and a link to the session that produced it. Running taxonomy has ten rows. The rest of the semester is reruns, more samples, and harder variants of the probes that came back empty.

## What was tested

Each item ran as its own Devin session in two modes: `tools` (normal, can run code and browse) and `notools` (told to answer from reasoning only). This replaces the three-vendor comparison in the petition. It is one system with and without its hands, and the gap between the two columns is what tools are worth.

Every math key is recomputed by brute force. Every Lean proof was compiled by me. Every biology key quotes the source sentence. Software acceptance checks were frozen before the runs.

## Results so far

| # | Probe | tools | notools | Verdict |
|---|---|---|---|---|
| 01 | Math: long constructions | 12/12, 5/5 constructions | 12/12, 4/5 constructions | small gap in the certificate |
| 02 | Math: heavy casework | 12/12 | 11/12 | one dropped factor |
| 03 | Math: false claims | 12/12 | 12/12 | no gap, claims too famous |
| 04 | Math: Lean 4 | 10/12 compile | 11/12 compile | 3 of 24, all invented API |
| 05 | Bio: recent papers | 11/11 | 0 correct, 4 guessed, 8 abstained | gap in the answer field |
| 06 | Bio: legends and traps | 12/12 | 0 correct, 3 false "not reported" | same |
| 07 | Software: CLI tool | 18/18 | 18/18 | no gap |
| 08 | Software: web app | 11/11, deployed | 11/11 | no gap |

## Three findings

**Reasoning slips are rare and local.** Without tools, roughly one item in twelve per math probe has an error: a missing factor in one branch, a construction that does not satisfy its own condition, a lemma that does not exist. The surrounding work is right and nothing flags uncertainty. With tools these vanish, because the model enumerates instead of reasoning.

**The model is honest in the wrong field.** On post-cutoff biology questions without a browser, seven of twenty-four items put a guess (or the phrase "not reported") in the `answer` field while the `reasoning` field says plainly that the paper was not read. To a reader this is honest. To any pipeline that consumes only the structured answer, it is fabrication. This was not something I set out to find and I think it is the most useful result so far.

**The environment decides what is checkable.** Ten of twelve Lean sessions had no Lean installed and said so. Two installed it and compiled. Proof quality did not differ; verification did.

## Where there was no gap

Famous false claims (recall), and software from a precise spec. Both software probes passed every check in both modes, including six stress fixtures I wrote after the run. The spec did the work; cutting it to one sentence is the obvious next experiment.

## Limits

One sample per cell, so every rate is an observation and not an estimate. One system. Easy difficulty on purpose. Five of twenty-four constructions hand-checked.

## Plan for weeks 8 to 13

1. Three to five samples on probe 01 constructions and probe 02 p08.
2. A construction grader for probe 01.
3. Probe 03 with unpublished false claims.
4. Probe 04 rerun with a prebuilt Mathlib project provided.
5. Probe 05 with the prompt reworded to allow, then to penalize, guessing.
6. Probes 07 and 08 with one-sentence specs.
7. Rerun everything on any model released mid-semester and post the diff.
8. Final report, 8 to 12 pages, draft already in `report/final.md`.
