# Finding the Gaps: Small Probes of Where Frontier AI Models Still Fail

CS 91r, Fall 2026. Supervisor: Christopher Thorpe.

Draft, revised after probes 09 and 10 and the follow-up runs. Section 7 will be filled as the semester goes.

## 1. What I set out to do

The public conversation about AI capability runs on two kinds of evidence: benchmark scores, and anecdotes. Benchmark scores are hard to argue with and hard to learn from, because a number like 87 percent on a suite tells you nothing about the 13 percent. Anecdotes are easy to learn from and easy to dismiss, because one screenshot of a wrong answer proves nothing about a rate.

I wanted something in between. Small probes, ten to twenty items each, that I could write in a day, run in an afternoon, grade by machine, and publish with every raw output attached. Each probe starts from a guess about where the model will break, and each ends with one of two verdicts: gap or no gap. A probe that finds no gap still counts, because it moves the boundary.

Ten probes, three areas: math, biology, software. Eight were planned. Two more were added after the first eight came back, because two of the planned ones found nothing and I wanted to know whether that was the model or the probe. This report says what I found, what I did not find, and what I now think the boundary looks like.

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
- Probe 09: four one-sentence tasks, each with a frozen acceptance script that separates hard checks (the program must do this) from judgment checks (a reasonable reading of the sentence does this).
- Probe 10: same as 01 to 03, with harder problems and a brute force key for all twelve.

One sample per item per mode in the first pass. That is the biggest limit of this report. After the first pass I went back and took three more no-tools samples on every probe 10 miss and reran probe 05 under two rewordings, which is where sections 3.11 and 3.12 come from.

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
| 09 | Software: one-sentence specs | 22/24 hard, 10/11 judgment | 22/24 hard, 10/11 judgment | gap, shared by both modes |
| 10 | Math: competition counting | 12/12 | 8/12 (15/24 with reruns) | gap, two kinds |

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

### 3.9 Probe 09: software from one sentence

Probes 07 and 08 found no gap, and section 4.4 of the first draft said the spec probably did the work. So I cut the spec. Four tasks, each one sentence: remove duplicate rows from a CSV on stdin; print the ten most common words in a file; flatten a nested JSON object to dotted keys; print the number of days between two dates. Standard library, one file, no code fences. The prompt also asked, in the reasoning field, for a list of decisions the task did not specify and whether the code had been run.

Before looking at any output I wrote an acceptance script per task with two kinds of check. Hard checks are things any reading of the sentence has to satisfy: the happy path, an empty input, a missing file, Unicode. Judgment checks are things a reasonable engineer would do but the sentence does not require: a stable sort on ties, keeping the header row.

Both modes scored the same: 22 of 24 hard checks, 10 of 11 judgment checks, and the same two failures. The word counter crashes with a raw traceback when the file does not exist. The flattener turns `{}` into `{"": {}}`, and when a key that already contains a dot collides with a nested path it keeps the last value and drops the other. Every session listed that collision rule in its decisions, so by its own account it was a choice, not a bug. I disagree with the choice, and the acceptance script marks it, but I count it separately from the crashes.

The part that made this worth doing: the tools sessions ran their code. Every one of them wrote a small input, ran the program on it, and reported success. None of them tried an empty object, a missing file, or a colliding key. Running the code confirmed what the model had already thought of. It did not find what the model had not.

### 3.10 Probe 10: harder counting

Probe 02 found one dropped factor in twelve problems a patient sophomore could do. Probe 10 raises the difficulty to where each problem needs an idea (a transfer matrix, a divisor argument, a generating function) or a computation nobody does by hand. Two of the twelve, counting n up to a million with d(n) = d(n+1) and counting integers up to a million with more ones than zeros in binary, have no closed form and cannot be done without a computer. I put them in to see what the no-tools mode does when asked for a number it cannot reach.

Tools: 12 of 12, every one by writing a program. No tools: 8 of 12, and the four misses are four different things.

On d(n) = d(n+1) the session named the OEIS entry for the sequence and listed "cumulative totals" up to 10, 100, 1000 and so on: 1, 10, 118, 1218, 11929, 119811. The true totals from my sieve are 1, 15, 118, 1119, 10585, 102093. Two of six are right. The table is presented as a recalled fact with a source attached, and nothing in either field hedges. On subsets of 1 to 30 with sum 200 the session did a normal approximation with two correction terms, got 7,026,324 against a true 7,026,242, and wrote in the first line of the reasoning that this was an estimate and not a count. The answer field says nothing of the kind. On tiling a 3 by 12 strip with straight trominoes the session set up the right three column states and then wrote the recurrence as a(n) = a(n-1) + a(n-2) instead of a(n-3), answering 144 instead of 60. On obtuse integer triangles with perimeter 2026 it made a correct reduction to 173 terms and then a wrong total, 58,045 for 58,120.

### 3.11 Probe 10 reruns: slips versus stable failures

Three more no-tools samples on each of the four misses.

| | original | rerun 1 | rerun 2 | rerun 3 | right |
|---|---|---|---|---|---|
| d(n) = d(n+1), key 102093 | 119811 | 111192 | 96280 | 108231 | 0 of 4 |
| subset sum, key 7026242 | 7026324 | 7031132 | 7029274 | 7026242 | 1 of 4 |
| tromino tiling, key 60 | 144 | 60 | 60 | 60 | 3 of 4 |
| obtuse triangles, key 58120 | 58045 | 58120 | 58120 | 58120 | 3 of 4 |

The tiling and the triangles were slips. Three of three reruns got them right with the argument the first sample had set up and then fumbled. The divisor count and the subset sum were not. The divisor count went 0 for 4 with four different numbers spread over a 24 percent range. Two of the reruns say the count "is obtained by tabulating d over [1, 10^6+1]" and then give a figure, when no tabulation happened. One rerun also quotes the count below ten million as 986,262, which is correct; the model has the famous number from the sequence's page and nothing for the one I asked about, and fills the hole with a number in the same shape. The subset sum went 1 for 4. Two reruns wrote down the correct recurrence, printed intermediate values from it, one right and two wrong, and reported a total as if the table had been run. The one that got it right did something different: split the set into small and large elements, wrote out seven sub-totals, added them, and checked against the normal approximation.

### 3.12 Probe 05 reruns: what the prompt was for

The first run of probe 05 gave four guesses and eight abstentions in the no-tools column. I reran the same twelve items under two rewordings of the prompt's last paragraph. "Guessing is fine, put your best guess in the answer field and a confidence in the reasoning" gave twelve guesses, one of them right (a count of 7), with stated confidences between 1 and 35 percent. "A wrong answer counts against you more than no answer; if you have not read the paper, write abstain" gave twelve abstentions and no guesses.

| Prompt | Answered | Correct | Abstained |
|---|---|---|---|
| original | 4 | 0 | 8 |
| guessing allowed | 12 | 1 | 0 |
| wrong costs more than none | 0 | 0 | 12 |

So the four-and-eight split was not a property of the model. It was what the model does when the prompt does not say what the answer field is for. One sentence about the cost of a wrong answer moved the behaviour all the way to either side.

## 4. What the gaps have in common

Reading the ten write-ups together, the failures sort into four kinds. One of them is what I expected, one I did not expect, and one only appeared once I made the problems hard enough.

### 4.1 Reasoning slips (probes 01, 02, 04)

A missing factor in one branch of a case split. A construction asserted to satisfy a condition it does not. A lemma name that does not exist. A recurrence copied wrong from a correct state machine. These are the errors I set out to find. They exist, they are rare at this difficulty (roughly 1 in 12 per probe without tools, and 1 in 4 on the two probe 10 items where they appeared), and they share a signature: the error is local, the surrounding work is correct, nothing in the output flags uncertainty, and a second sample usually does not make the same mistake. They vanish when the model can run code, because it stops trusting its own casework and enumerates instead. They would also mostly vanish under self-consistency, running the same prompt a few times and taking the majority, which is cheap and which probe 10 suggests would have fixed two of four misses.

### 4.2 Field confusion (probes 05, 06)

This is the one I did not expect, and I think it is the most useful finding in the report. When the model does not know the answer, it does not invent a confident story. It splits itself. The `reasoning` field says "I did not read this paper, this is a guess" or "I cannot verify this." The `answer` field gets a bare number, or the phrase "not reported" borrowed from the prompt's own instructions.

To a person reading the whole reply, this is honest. To a pipeline reading only `answer`, it is four fabricated facts and three false claims about what a paper contains. Seven of twenty-four no-tools biology items behaved this way, and the probe 10 estimate is the same shape in a different subject: "this is an analytic estimate, not an exact enumeration" in the reasoning, a number to seven digits in the answer.

The rerun in 3.12 changes how I read this. I first wrote that the model treats the answer slot as a form that must be filled. That is half right. It treats the answer slot as a form whose purpose it has to infer, and when the prompt gives no hint it guesses, and different sessions guess differently. Tell it that a wrong answer costs more than no answer and it abstains twelve times out of twelve. Tell it guessing is fine and it guesses twelve times out of twelve, with a confidence number that in this case was honest (the one hit came with 15 percent). The model was never unsure whether it knew the answer. It was unsure what I wanted done with the slot, and I had not said. That makes this less a model failure and more a schema failure, and a cheap one to fix.

### 4.3 Environment, not model (probe 04)

Ten of twelve tools sessions could not compile Lean because Lean was not installed. Two decided to install it. The proofs from all twelve were of similar quality, but only two were verified. Nothing about the model's ability changed between those sessions; what changed was a decision about whether to spend time on setup. In a real deployment this decision is made by whoever configures the environment, and it decides whether the task is checkable at all.

### 4.4 Narrated computation (probe 10)

This is the one that only showed up at the higher difficulty, and it is the one I would worry about. On the two problems that need a computer, the no-tools mode did not say so. It described the computation ("tabulate d over [1, 10^6+1]", "iterate the recurrence through n = 30") and then reported an output, and the output was wrong every time it did this, six sessions out of six across the two problems. The one rerun that got the subset sum right did not narrate; it did a different, smaller decomposition it could actually carry, and wrote out the pieces.

What distinguishes this from a slip is that it is stable. Four samples on the divisor count gave four wrong answers. Self-consistency does not help, because the samples disagree with each other and none is right. A reader checking the argument does not help either, because the argument is correct; what is missing is the arithmetic, and the arithmetic is a million-term sieve. And a source name is attached in most cases, which is where the word fabrication becomes fair. This failure is removed completely by letting the session run code, and I could find nothing else that removes it.

### 4.5 Where there was no gap, and what the spec was worth

Probe 03 (famous false claims), 07 and 08 (software from a precise spec). The common thread is that the task was fully specified or fully recalled. Every rule I wrote into the software specs was honored, including output ordering and exit codes, and running the code bought nothing measurable over writing it blind.

Probe 09 was the test of whether the spec did the work. The answer is partly. With a one-sentence spec the model still built the right thing, honored the obvious conventions, and listed its own assumptions on request. What it did not do is find the edges the sentence left out: the missing file, the empty object, the colliding key. And, the finding I did not expect, being able to run the code did not change that. The tools sessions tested the design they had in their head. A spec that names the edges buys you the edges. Execution buys you confidence in the happy path. Neither buys you the case nobody thought of, which is the same situation a human engineer is in, and which is what acceptance tests written by someone else are for.

## 5. What I would tell someone deciding how to use these systems

Each of these is earned by a specific probe.

**Grade the certificate, not the number.** Probe 01. If your task has a checkable artifact (a construction, a proof, a diff), check the artifact. The final answer being right is weak evidence that the work behind it is.

**Say what a wrong answer costs.** Probes 05, 06, 10. If you only consume a structured `answer` field, you will collect confident-looking guesses that the model itself labeled as guesses one field over. One sentence in the prompt about whether a wrong answer is worse than none moved the guess rate from a third to all or nothing. Write that sentence. Better, add an explicit abstain or confidence field so a pipeline can filter on it.

**Provision the checker.** Probe 04. If a task is verifiable in principle, make the verifier available in the environment. Otherwise verification depends on whether the agent decides to build one, and most of the time it will not.

**Let it compute, or do not ask for a number it cannot reach.** Probe 10. When the answer needs a computation and the model cannot run one, it will narrate the computation and give you a figure anyway, with a citation. Nothing short of running the code fixed this. If the environment cannot run code, do not ask for exact counts over a million things.

**Write the edge cases yourself.** Probe 09. Running its own code did not lead the model to test inputs it had not thought of. Its tests cover its design. Acceptance tests have to come from someone who did not write the design, which for now means you.

**Take more than one sample when it is cheap.** Probe 10. Half the misses at the hard level were slips that three reruns did not repeat. Majority over a few samples would have caught them. It would not have caught the other half, so this is a complement to the checker, not a substitute.

And one thing that is not a warning: with a precise spec and a browser, every task in this suite that a competent person could do in an afternoon, the agent did in one pass. The boundary is not there.

## 6. Limits

- **Mostly one sample per cell.** Every rate in this report is an observation, not an estimate. A 1 in 12 miss could be 0 in 12 or 3 in 12 on the next run. Where I did take more samples (probe 10, four misses, four each) the picture changed for two of the four, which is the argument for doing it everywhere.
- **One system, two modes.** I tested one agent. Another vendor's model might behave differently on field confusion in particular, since that is plausibly a training artifact.
- **Two difficulty levels only.** Probes 01 to 03 are first-year level and found almost nothing. Probe 10 is competition level and found a third. There is a lot of room between them and I do not know where the curve bends.
- **Prompt variants were only tried on probe 05.** The finding that one sentence moves the guess rate to zero or all might not transfer to probe 06, where the "not reported" escape hatch is in play, or to the probe 10 estimate.
- **Probe 09 acceptance checks are mine.** What counts as a hard check versus a judgment check is my call, made before the run but still a call. Someone else might grade the collision behaviour as fine.
- **Hand-checked constructions.** Only five of twenty-four probe 01 constructions were checked, by me, by hand. A script that parses and verifies constructions would let me check all of them.
- **Prompt engineering by me.** The probe 06 re-run shows that my prompt wording changed what the sessions could do. I documented it, but a different phrasing could shift other results too.

## 7. What changed since week 7

Reserved for reruns on any model released mid-semester. Nothing to report yet.

## 8. Next probes

In rough priority order. Items 5 and 6 from the first draft became probes 09 and 10 and the reruns in 3.11 and 3.12.

1. Three to five samples on probe 01 constructions and probe 02 p08, to turn anecdotes into rates the way probe 10 did.
2. A construction grader for probe 01, so every certificate is checked.
3. Probe 03 with unpublished false claims: a true theorem with one hypothesis weakened, or a constant changed so the first counterexample is above 10⁴.
4. Probe 04 with a prebuilt Mathlib project in the environment, to separate proof ability from toolchain access. Then raise difficulty until compile failures return, and test whether the model repairs from the compiler message.
5. The probe 05 prompt variants on probe 06 and on the probe 10 estimate, to see whether "wrong costs more than none" also stops the borrowed "not reported" and turns the estimate into an abstention.
6. A probe 10 variant whose prompt says "if the count cannot be done exactly by hand, say so in the answer field", aimed at the narrated computation.
7. Probe 09 with the tools sessions told to write tests before code, to see whether the edges they miss change.
8. A probe where the number only exists in a plot, which needs image input and a different harness.

## Appendix A: taxonomy

See `report/taxonomy.md` for the running table, one row per failure type, with the probe and example for each.

## Appendix B: reproducing

Each `results.md` gives the grade command. Raw outputs are in `probes/*/outputs/`, unmodified except for three documented grader normalizations (word numbers to digits, "Unable to verify" and the bare word "abstain" counted as abstention). Every output links to its session. The probe 05 variant outputs are in `outputs/notools-guessok/` and `outputs/notools-penalty/`, with the variant prompt stored in each file.
