# Finding the Gaps: Small Probes of Where Frontier AI Models Still Fail

CS 91r, Fall 2026. Supervisor: Christopher Thorpe.

Draft. Sections marked [WEEK 7+] will be filled as the semester goes.

## 1. What I set out to do

The public conversation about AI capability runs on two kinds of evidence: benchmark scores, and anecdotes. Benchmark scores are hard to argue with and hard to learn from, because a number like 87 percent on a suite tells you nothing about the 13 percent. Anecdotes are easy to learn from and easy to dismiss, because one screenshot of a wrong answer proves nothing about a rate.

I wanted something in between. Small probes, ten to twenty items each, that I could write in a day, run in an afternoon, grade by machine, and publish with every raw output attached. Each probe starts from a guess about where the model will break, and each ends with one of two verdicts: gap or no gap. A probe that finds no gap still counts, because it moves the boundary.

Eight probes, three areas: math, biology, software. This report says what I found, what I did not find, and what I now think the boundary looks like.

## 2. Setup

### 2.1 What was tested

Every item ran as its own Devin session, in two modes.

- **tools**: normal operation. The session can run code, open a browser, install software.
- **notools**: the prompt tells the session not to run code, browse, search, or use any tool, and to answer from reasoning alone.

So the comparison is not between three model vendors, which is what my petition originally proposed. It is between one agent with its hands tied and the same agent with its hands free. I made that change for cost and access reasons and I think it turned out to be the more interesting comparison. The `tools` column tells you what an agent can do for you today. The `notools` column tells you what the model underneath actually knows and can reason out. The difference between them is what tools are worth.

Every session returned a structured answer with two fields, `answer` and `reasoning`. The grader reads `answer`. I read `reasoning`. That split turned out to matter more than I expected; see section 4.

### 2.2 How grading worked

- Math probes 01 to 03: every key is recomputed by a brute force script in `key/verify.py`. The grader compares the final integer or the TRUE/FALSE verdict. For probe 01 I also hand-checked five constructions.
- Probe 04: I compiled every returned proof myself against Lean 4.35.0-rc2 and Mathlib revision 0653561, rejected anything with `sorry`, `admit`, `native_decide`, extra axioms or an altered statement, and kept the first compiler error.
- Biology probes 05 and 06: every key cites the paper and quotes the sentence the number comes from. The grader separates three outcomes: correct, wrong, and abstained. Abstained means the answer field was empty or was some form of "I don't know".
- Software probes 07 and 08: acceptance checks written and frozen before the run. For 07 the checks are twelve fixture pairs and a runner script. For 08 they are twelve browser checks that I ran with Playwright driving Chrome and read myself.

One sample per item per mode. That is the biggest limit of this report and I return to it in section 6.

### 2.3 What is in the repository

`github.com/GiovanniDantonio/finding-the-gaps`. One folder per probe with `problems/`, `key/`, `outputs/`, `results.md`, `writeup.md`. Every raw output includes a link to the session that produced it, so any number in this report can be traced to a transcript.

## 3. Results by probe

| # | Probe | tools | notools | Verdict |
|---|---|---|---|---|
| 01 | Math: long constructions | 12/12 numbers, 5/5 constructions checked | 12/12 numbers, 4/5 constructions checked | small gap in the certificate |
| 02 | Math: heavy casework | 12/12 | 11/12 | small gap, one dropped factor |
| 03 | Math: false claims | 12/12 | 12/12 | no gap at this difficulty |
| 04 | Math: Lean 4 proofs | 10/12 compile | 11/12 compile | small gap, 3 of 24 |
| 05 | Bio: recent papers | 12/12 | 0 correct, 4 guessed, 8 abstained | gap, but in the answer slot |
| 06 | Bio: legends and traps | 12/12 incl. 4 traps | 0 correct, 3 false "not reported", 9 abstained | same gap as 05 |
| 07 | Software: CLI tool | 18/18 | 18/18 | no gap |
| 08 | Software: web app | 11/11 checks, deployed | 11/11 checks | no gap |

### 3.1 Probe 01: long constructions

Twelve extremal problems on small finite objects. Each asks for a number and a construction that reaches it. My guess was that the number would come from memory and the construction would be wrong, because checking a construction takes patience.

All 24 numbers were right. The failure showed up where I expected: on the no-three-in-a-line problem (10 points on a 5 by 5 grid), the no-tools run gave the right count and a point set with two collinear triples. Its reasoning listed the values of y minus x for its ten points and said each appeared at most twice. Both 1 and minus 1 appear three times in its own list. The tools run found a valid set by exhaustive search.

One bad certificate in five is an anecdote. The lesson I took is about grading, not about the model: if you only check the integer you will not see this.

### 3.2 Probe 02: heavy casework

Twelve counting problems with parameters chosen so the answers are not in a textbook. With tools the model wrote a brute force script every single time and got 12 of 12. Without tools it got 11 of 12, and several of the eleven are real casework I could not have done cleanly in one pass: inclusion and exclusion over residue classes mod 4p² for every prime up to 43, complement symmetry on subset sums.

The miss is a two-pair poker hand containing the ace of spades. In the case where the ace of spades is part of the ace pair, you need a factor of 3 for which other ace joins it. The reasoning writes "12 times 6 times 11 times 4" and never mentions the second ace. The other case is right, so the total is off by exactly that missing factor. No hedge, no flag. It reads like a good student's mistake.

### 3.3 Probe 03: false claims

Six true claims and six false ones phrased like homework. The false ones have well known smallest counterexamples that are not tiny: n = 40 for n² + n + 41, p = 11 for Mersenne primes, 341 for the Fermat test. Both modes got 24 of 24 with correct counterexamples and proofs I could not fault.

This probe failed as a probe. Every false claim is a famous false claim, and several no-tools answers named the result ("Brocard's problem"). It measured recall. It is still worth keeping as a floor: the "confidently prove the false thing" failure does not show up on well known statements. To test it properly the claims have to be unpublished, and I list that under future work.

### 3.4 Probe 04: Lean 4 proofs

Twelve first-year statements with the theorem given and `sorry` as the body. 21 of 24 compiled. The three failures are all of the kind a checker catches in a second and a reader does not: a lemma name that does not exist (`even_or_odd`), a field access on the wrong type (`.mul_dvd` on an equation), and `linarith` asked to close a goal it cannot.

The part I did not predict: ten of the twelve tools sessions had no Lean installed and said so, then answered without compiling. Two installed Lean and Mathlib themselves and compiled. Both of those compiled for me too. So the tools column here is mostly the no-tools experiment again, and the thing that determined whether a proof was checked was whether the session chose to spend twenty minutes building a toolchain. Nobody claimed a compile that had not happened.

### 3.5 Probe 05: numbers from recent papers

Twelve factual questions from eight bioRxiv preprints posted in the five weeks before the run, so none of them can be in training data. With a browser: 12 of 12, every answer quoting the passage it came from, and I checked those quotes against mine. Without tools: zero correct. Eight said they did not know. Four put a number in the answer field: 50 where the paper says 70, 300 where it says 500, 100000 where it says 698631, 4.4 where it says 3.1. All four reasoning fields say, plainly, that the paper was not read and the number is a guess.

### 3.6 Probe 06: legends, methods and traps

Same design, harder questions: numbers that live in figure legends and methods paragraphs, plus four trap questions where the value is not in the paper and the right answer is "not reported". With tools: 12 of 12 including all four traps, and the trap reasoning names what the paper does report before saying what it does not ("Spearman and Pearson, not Kendall"). Without tools: zero correct, nine abstentions, and three answers of "not reported" on questions whose values are in the paper.

Nine tools sessions were re-run once because my first prompts referred to papers by shorthand and the sessions could not tell which paper was meant. That was my error, it is documented in the results file, and only the re-run outputs are graded.

### 3.7 Probe 07: a CLI tool from a spec

A one-file Python iCalendar diff tool, with the spec naming the edge cases: recurrence overrides, TZID versus UTC versus all-day, folded lines, exit codes. Twelve fixture pairs frozen before the run. Both modes: 12 of 12. I then wrote six more fixtures aimed at things the spec did not mention (escaped commas, a nested alarm, quoted parameters, bare line feeds, an empty file, a duplicate UID). Both modes: 6 of 6. The no-tools session said up front it had not run its code and there might be bugs. I could not find one.

### 3.8 Probe 08: a web app from a spec

A single offline `index.html` that finds thirty-minute meeting slots across time zones, with half-hour offsets, shifts that cross midnight, and state in the URL hash. Both modes passed every check I could run: 63 slots for London with Kolkata, 112 for New York with a Tokyo night shift, hash round trip, keyboard, phone width, zero network requests. The one check I could not run is a daylight-saving change inside the seven-day window, because no zone changes clocks between 21 and 28 September. The tools build is deployed unmodified at the URL in `probes/08-build-web-app/results.md`.

## 4. What the gaps have in common

Reading the eight write-ups together, the failures sort into three kinds, and only one of them is what I expected.

### 4.1 Reasoning slips (probes 01, 02, 04)

A missing factor in one branch of a case split. A construction asserted to satisfy a condition it does not. A lemma name that does not exist. These are the errors I set out to find. They exist, they are rare at this difficulty (roughly 1 in 12 per probe without tools), and they share a signature: the error is local, the surrounding work is correct, and nothing in the output flags uncertainty. They vanish when the model can run code, because it stops trusting its own casework and enumerates instead.

### 4.2 Field confusion (probes 05, 06)

This is the one I did not expect, and I think it is the most useful finding in the report. When the model does not know the answer, it does not invent a confident story. It splits itself. The `reasoning` field says "I did not read this paper, this is a guess" or "I cannot verify this." The `answer` field gets a bare number, or the phrase "not reported" borrowed from the prompt's own instructions.

To a person reading the whole reply, this is honest. To a pipeline reading only `answer`, it is four fabricated facts and three false claims about what a paper contains. Seven of twenty-four no-tools biology items behaved this way. The model appears to treat the answer slot as a form that must be filled, and the reasoning slot as the place where honesty lives. Whether that is a failure depends entirely on which field the downstream system trusts, which means it is a failure in every system that trusts the structured field, which is most of them.

### 4.3 Environment, not model (probe 04)

Ten of twelve tools sessions could not compile Lean because Lean was not installed. Two decided to install it. The proofs from all twelve were of similar quality, but only two were verified. Nothing about the model's ability changed between those sessions; what changed was a decision about whether to spend time on setup. In a real deployment this decision is made by whoever configures the environment, and it decides whether the task is checkable at all.

### 4.4 Where there was no gap

Probe 03 (famous false claims), 07 and 08 (software from a precise spec). The common thread is that the task was fully specified or fully recalled. Every rule I wrote into the software specs was honored, including output ordering and exit codes, and running the code bought nothing measurable over writing it blind. My reading is that the spec did the hard work. The untested question is what happens when the spec is one sentence.

## 5. What I would tell someone deciding how to use these systems

Three things, each earned by a specific probe.

**Grade the certificate, not the number.** Probe 01. If your task has a checkable artifact (a construction, a proof, a diff), check the artifact. The final answer being right is weak evidence that the work behind it is.

**Read the whole reply, or design the schema so you do not have to.** Probes 05 and 06. If you only consume a structured `answer` field, you will collect confident-looking guesses that the model itself labeled as guesses one field over. Either surface the reasoning or add an explicit confidence or abstain field and instruct the model to use it.

**Provision the checker.** Probe 04. If a task is verifiable in principle, make the verifier available in the environment. Otherwise verification depends on whether the agent decides to build one, and most of the time it will not.

And one thing that is not a warning: with a precise spec and a browser, every task in this suite that a competent person could do in an afternoon, the agent did in one pass. The boundary is not there.

## 6. Limits

- **One sample per cell.** Every rate in this report is an observation, not an estimate. A 1 in 12 miss could be 0 in 12 or 3 in 12 on the next run. Three to five samples on the probes that showed a gap is the first thing on the list.
- **One system, two modes.** I tested one agent. Another vendor's model might behave differently on field confusion in particular, since that is plausibly a training artifact.
- **Easy difficulty.** I kept the math at first-year level on purpose, to find the floor. The floor is high. The probes that found no gap need harder, unpublished items to say anything more.
- **Hand-checked constructions.** Only five of twenty-four probe 01 constructions were checked, by me, by hand. A script that parses and verifies constructions would let me check all of them.
- **Prompt engineering by me.** The probe 06 re-run shows that my prompt wording changed what the sessions could do. I documented it, but a different phrasing could shift other results too.

## 7. What changed since week 7

[WEEK 7+] Reserved for reruns on any model released mid-semester, additional samples, and the harder variants described below.

## 8. Next probes

In rough priority order.

1. Three to five samples on probe 01 constructions and probe 02 p08, to turn anecdotes into rates.
2. A construction grader for probe 01, so every certificate is checked.
3. Probe 03 with unpublished false claims: a true theorem with one hypothesis weakened, or a constant changed so the first counterexample is above 10⁴.
4. Probe 04 with a prebuilt Mathlib project in the environment, to separate proof ability from toolchain access. Then raise difficulty until compile failures return, and test whether the model repairs from the compiler message.
5. Probe 05 with the prompt reworded two ways: guessing explicitly allowed with a confidence number, and wrong answers explicitly penalized relative to abstention. The question is whether the four guessers become twelve or zero.
6. Probe 07 and 08 with the spec cut to one sentence, to measure what the spec was worth.
7. A probe where the number only exists in a plot, which needs image input and a different harness.

## Appendix A: taxonomy

See `report/taxonomy.md` for the running table, one row per failure type, with the probe and example for each.

## Appendix B: reproducing

Each `results.md` gives the grade command. Raw outputs are in `probes/*/outputs/`, unmodified except for two documented grader normalizations (word numbers to digits, "Unable to verify" counted as abstention). Every output links to its session.
