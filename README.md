# Finding the Gaps

Small probes of where frontier AI models still fail. CS 91r, Harvard, Fall 2026. Supervisor: Christopher Thorpe.

Not a benchmark. Eleven small experiments, each 10 to 25 hand-written problems or one build task, run as Devin sessions in two modes (with tools, and reasoning only), written up in one or two pages. The goal is a short, evidence-backed taxonomy of gaps in mathematics, biology, and software building.

## Probes

| Probe | Title | Area | Status |
|---|---|---|---|
| [01-math-constructions](probes/01-math-constructions) | Math: long constructions | math | 48/48 no-tools numbers over four samples, 12/12 tools, 1 bad construction in 5 checked |
| [02-math-casework](probes/02-math-casework) | Math: heavy casework | math | tools 12/12; no-tools 44/48 over four samples, two problems slip; Lite tier once, 8/12 |
| [03-math-false-claims](probes/03-math-false-claims) | Math: prove-this claims that are actually false | math | 24/24, no gap; all twelve claims are online, so this measures recall (`key/contamination.md`) |
| [04-math-lean](probes/04-math-lean) | Math: statements to be checked in Lean 4 | math | tools 10/12 compile, 12/12 when told to install Lean and compile; no-tools 40/48 over four samples |
| [05-bio-recent-papers](probes/05-bio-recent-papers) | Biology: questions from post-cutoff open access papers | biology | tools 12/12, no-tools 0/4 answered, 8 abstained; two prompt variants move it to 12 guesses or 12 abstentions |
| [06-bio-figure-reading](probes/06-bio-figure-reading) | Biology: figure and table reading | biology | tools 12/12 incl. 4 traps, no-tools 0/3 answered, 9 abstained; prompt variants move it to 12 guesses or 12 abstentions |
| [07-build-cli-tool](probes/07-build-cli-tool) | Software: build a small CLI tool end to end | software | run once, 18/18 both modes, no gap |
| [08-build-web-app](probes/08-build-web-app) | Software: build and deploy a tiny web app | software | run once, 11/11 both modes, tools build deployed |
| [09-build-vague-spec](probes/09-build-vague-spec) | Software: four one-sentence specs | software | run once, 22/24 hard checks both modes, same two failures |
| [10-math-competition](probes/10-math-competition) | Math: competition counting | math | tools 12/12; no-tools 35/48 over four samples: three slips, three stable; one exact answer online (`key/contamination.md`); Lite tier once, 7/12, misses only where the default tier also missed |
| [11-math-paired](probes/11-math-paired) | Math: paired problems, computation needed vs not | math | tools 24/24; no-tools 12/12 on the short half, 10/12 on the computation half, four of those recalled from tables |

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

`harness/` runs and grades items. `run.py` opens one Devin session per (problem, mode, sample) through the Devin API and saves the structured answer plus a link to the session; set `DEVIN_API_KEY` first. `grade.py` scores the saved answers against `key/key.json`. `report/` holds the running taxonomy, the week 7 status report, and the final report. `baseline/` is a protocol for a timed human run of probe 02, not yet done.

System under test: Devin child sessions, default tier, on 21 and 22 September 2026, not a bare model API. Two probes were also run once on the Lite tier as a data point.

## Rules I am holding myself to

- Every problem is written by me, after the models' training cutoffs where that matters.
- Several samples per problem. Mode, prompt, and a link to every session recorded.
- Raw outputs are committed as is.
- A probe that finds no gap still gets a writeup.
