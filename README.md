# Finding the Gaps

Small probes of where frontier AI models still fail. CS 91r, Harvard, Fall 2026. Supervisor: Christopher Thorpe.

Not a benchmark. Ten small experiments, each 10 to 25 hand-written problems or one build task, run as Devin sessions in two modes (with tools, and reasoning only), written up in one or two pages. The goal is a short, evidence-backed taxonomy of gaps in mathematics, biology, and software building.

## Probes

| Probe | Title | Area | Status |
|---|---|---|---|
| [01-math-constructions](probes/01-math-constructions) | Math: long constructions | math | run once, 24/24 numbers right, 1 bad construction |
| [02-math-casework](probes/02-math-casework) | Math: heavy casework | math | run once, 23/24, one dropped factor |
| [03-math-false-claims](probes/03-math-false-claims) | Math: prove-this claims that are actually false | math | run once, 24/24, no gap |
| [04-math-lean](probes/04-math-lean) | Math: statements to be checked in Lean 4 | math | run once, 21/24 compile |
| [05-bio-recent-papers](probes/05-bio-recent-papers) | Biology: questions from post-cutoff open access papers | biology | tools 12/12, no-tools 0/4 answered, 8 abstained; two prompt variants move it to 12 guesses or 12 abstentions |
| [06-bio-figure-reading](probes/06-bio-figure-reading) | Biology: figure and table reading | biology | run once, tools 12/12 incl. 4 traps, no-tools 0/3 answered |
| [07-build-cli-tool](probes/07-build-cli-tool) | Software: build a small CLI tool end to end | software | run once, 18/18 both modes, no gap |
| [08-build-web-app](probes/08-build-web-app) | Software: build and deploy a tiny web app | software | run once, 11/11 both modes, tools build deployed |
| [09-build-vague-spec](probes/09-build-vague-spec) | Software: four one-sentence specs | software | run once, 22/24 hard checks both modes, same two failures |
| [10-math-competition](probes/10-math-competition) | Math: competition counting | math | tools 12/12, no-tools 8/12; four misses rerun 3x: two slips, two stable |

## Layout

Each probe folder has the same shape:

```
probes/<slug>/
  problems/    what the model sees, one file per item (or task.md for build tasks)
  key/         answers and graders (key.json), Lean files, acceptance criteria
  outputs/     raw model outputs, never edited
  results.md   the numbers
  writeup.md   one to two pages: hypothesis, setup, what happened, gap or no gap
```

`harness/` runs and grades items. `run.py` opens one Devin session per (problem, mode, sample) through the Devin API and saves the structured answer plus a link to the session; set `DEVIN_API_KEY` first. `grade.py` scores the saved answers against `key/key.json`. `report/` holds the running taxonomy, the week 7 status report, and the final report.

## Rules I am holding myself to

- Every problem is written by me, after the models' training cutoffs where that matters.
- Several samples per problem. Mode, prompt, and a link to every session recorded.
- Raw outputs are committed as is.
- A probe that finds no gap still gets a writeup.
