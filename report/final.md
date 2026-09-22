# Finding the Gaps: Small Probes of Where Frontier AI Models Still Fail

CS 91r, Fall 2026. Supervisor: Christopher Thorpe.

Draft, revised after probes 09 to 11, the resampling pass and the Lean rerun. Section 7 will be filled as the semester goes.

## 1. What I set out to do

The public conversation about AI capability runs on two kinds of evidence: benchmark scores, and anecdotes. Benchmark scores are hard to argue with and hard to learn from, because a number like 87 percent on a suite tells you nothing about the 13 percent. Anecdotes are easy to learn from and easy to dismiss, because one screenshot of a wrong answer proves nothing about a rate.

I wanted something in between. Small probes, ten to twenty items each, that I could write in a day, run in an afternoon, grade by machine, and publish with every raw output attached. Each probe starts from a guess about where the model will break, and each ends with one of two verdicts: gap or no gap. A probe that finds no gap still counts, because it moves the boundary.

Eleven probes, three areas: math, biology, software. Eight were planned. Two more were added after the first eight came back, because two of the planned ones found nothing and I wanted to know whether that was the model or the probe. The eleventh was written to test a specific claim that came out of the tenth. After the first pass I went back and resampled, because one sample per item is not a rate, and I list the hypotheses I wrote down before each follow-up so the reader can see which ones held. This report says what I found, what I did not find, and what I now think the boundary looks like.

## 2. Setup

### 2.1 What was tested

Every item ran as its own Devin session, in two modes.

- **tools**: normal operation. The session can run code, open a browser, install software.
- **notools**: the prompt tells the session not to run code, browse, search, or use any tool, and to answer from reasoning alone.

So the comparison is not between three model vendors, which is what my petition originally proposed. It is between one agent with its hands tied and the same agent with its hands free. I made that change for cost and access reasons and I think it turned out to be the more interesting comparison. The `tools` column tells you what an agent can do for you today. The `notools` column tells you what the model underneath actually knows and can reason out. The difference between them is what tools are worth.

Every session returned a structured answer with two fields, `answer` and `reasoning`. The grader reads `answer`. I read `reasoning`. That split turned out to matter more than I expected; see section 4.

To be exact about the system under test: it is Devin, a coding agent, running in its default configuration on the dates given, not a bare model behind an API. The `notools` mode is a prompt instruction, not a sandbox; the agent can still see its own system prompt and whatever scaffolding the product adds. Every reasoning field in the no-tools math and Lean runs states that no code was run, and no session transcript I looked at shows tool use, but I did not audit all of them. Which underlying model the default tier uses is not something I control or can pin, so "the model" in this report means "whatever Devin's default tier was on 21 and 22 September 2026". I also ran two probes once on the Lite tier (section 3.15). That is one alternative configuration, one sample, two probes, and it is there as a data point, not a ranking.

### 2.2 How grading worked

- Math probes 01 to 03: every key is recomputed by a brute force script in `key/verify.py`. The grader compares the final integer or the TRUE/FALSE verdict. For probe 01 I also hand-checked five constructions.
- Probe 04: I compiled every returned proof myself against Lean 4.35.0-rc2 and Mathlib revision 0653561, rejected anything with `sorry`, `admit`, `native_decide`, extra axioms or an altered statement, and kept the first compiler error.
- Biology probes 05 and 06: every key cites the paper and quotes the sentence the number comes from. The grader separates three outcomes: correct, wrong, and abstained. Abstained means the answer field was empty or was some form of "I don't know".
- Software probes 07 and 08: acceptance checks written and frozen before the run. For 07 the checks are twelve fixture pairs and a runner script. For 08 they are twelve browser checks that I ran with Playwright driving Chrome and read myself.
- Probe 09: four one-sentence tasks, each with a frozen acceptance script that separates hard checks (the program must do this) from judgment checks (a reasonable reading of the sentence does this).
- Probe 10: same as 01 to 03, with harder problems and a brute force key for all twelve.
- Probe 11: same as 10, with a brute force key, a reproducible grader in `key/grade.py`, and the session's own EXACT / RECALLED / ESTIMATED label recorded next to each answer.

One sample per item per mode in the first pass. After that pass I took three more no-tools samples on every item of probes 01, 02, 04 and 10 (four samples per cell, 48 per probe), reran probe 04's tools mode with an explicit instruction to install Lean and compile, reran probes 05 and 06 under two rewordings, ran probes 02 and 10 once on the Lite tier, and wrote probe 11. Tools mode stays at one sample per item except where noted, because it was at 12 of 12 nearly everywhere and the question was about the no-tools column. Sections 3.11 to 3.15 report the follow-ups. Where a probe has four samples I report a count out of 48; where it has one I say so. Neither is a capability rate for anything beyond these items on these days.

### 2.3 What is in the repository

`github.com/GiovanniDantonio/finding-the-gaps`. One folder per probe with `problems/`, `key/`, `outputs/`, `results.md`, `writeup.md`. Every raw output includes a link to the session that produced it, so any number in this report can be traced to a transcript.

## 3. Results by probe

| # | Probe | tools | notools | Verdict |
|---|---|---|---|---|
| 01 | Math: long constructions | 12/12 numbers, 5/5 constructions checked | 12/12 numbers, 4/5 constructions checked | small gap in the certificate |
| 02 | Math: heavy casework | 12/12 | 11/12 (44/48 with resampling) | small gap, two problems slip |
| 03 | Math: false claims | 12/12 | 12/12 | no gap; measures recall (all twelve claims are online) |
| 04 | Math: Lean 4 proofs | 10/12 compile; 12/12 when told to install and compile | 11/12 compile (40/48 with resampling) | gap, 8 of 48, closed by the checker |
| 05 | Bio: recent papers | 12/12 | 0 correct, 4 guessed, 8 abstained | gap, but in the answer slot |
| 06 | Bio: legends and traps | 12/12 incl. 4 traps | 0 correct, 3 false "not reported", 9 abstained; prompt variants move it to 12 guesses or 12 abstentions | same gap as 05 |
| 07 | Software: CLI tool | 18/18 | 18/18 | no gap |
| 08 | Software: web app | 11/11 checks, deployed | 11/11 checks | no gap |
| 09 | Software: one-sentence specs | 22/24 hard, 10/11 judgment | 22/24 hard, 10/11 judgment | gap, shared by both modes |
| 10 | Math: competition counting | 12/12 | 8/12 (35/48 with resampling) | gap, three kinds |
| 11 | Math: paired, computation needed vs not | 24/24 | 10/12 on the computation half, 12/12 on the short half | gap on the predicted side, smaller than predicted |

### 3.1 Probe 01: long constructions

Twelve extremal problems on small finite objects. Each asks for a number and a construction that reaches it. My guess was that the number would come from memory and the construction would be wrong, because checking a construction takes patience.

All 24 numbers were right. The failure showed up where I expected: on the no-three-in-a-line problem (10 points on a 5 by 5 grid), the no-tools run gave the right count and a point set with two collinear triples. Its reasoning listed the values of y minus x for its ten points and said each appeared at most twice. Both 1 and minus 1 appear three times in its own list. The tools run found a valid set by exhaustive search.

One bad certificate in five is an anecdote. The lesson I took is about grading, not about the model: if you only check the integer you will not see this.

### 3.2 Probe 02: heavy casework

Twelve counting problems with parameters chosen so the answers are not in a textbook. With tools the model wrote a brute force script every single time and got 12 of 12. Without tools it got 11 of 12, and several of the eleven are real casework I could not have done cleanly in one pass: inclusion and exclusion over residue classes mod 4p² for every prime up to 43, complement symmetry on subset sums.

The miss is a two-pair poker hand containing the ace of spades. In the case where the ace of spades is part of the ace pair, you need a factor of 3 for which other ace joins it. The reasoning writes "12 times 6 times 11 times 4" and never mentions the second ace. The other case is right, so the total is off by exactly that missing factor. No hedge, no flag. It reads like a good student's mistake.

### 3.3 Probe 03: false claims

Six true claims and six false ones phrased like homework. The false ones have well known smallest counterexamples that are not tiny: n = 40 for n² + n + 41, p = 11 for Mersenne primes, 341 for the Fermat test. Both modes got 24 of 24 with correct counterexamples and proofs I could not fault.

This probe failed as a probe. Every false claim is a famous false claim, and several no-tools answers named the result ("Brocard's problem"). It measured recall. I confirmed this after the fact with one web search per claim: all twelve, true and false, appear with their truth value on Wikipedia or Math StackExchange in the same or nearly the same wording (`key/contamination.md`). It is still worth keeping as a floor: the "confidently prove the false thing" failure does not show up on well known statements. To test it properly the claims have to be unpublished, and I list that under future work.

I ran the same check on probe 10. The methods are all standard, as they would be for any competition problem, but only one of the twelve exact answers is on the web as a term of a named sequence (p09, the tromino count). The other parameters were chosen for this probe and I found no page with those numbers. That is a light check and not a proof of absence.

### 3.4 Probe 04: Lean 4 proofs

Twelve first-year statements with the theorem given and `sorry` as the body. 21 of 24 compiled. The three failures are all of the kind a checker catches in a second and a reader does not: a lemma name that does not exist (`even_or_odd`), a field access on the wrong type (`.mul_dvd` on an equation), and `linarith` asked to close a goal it cannot.

The part I did not predict: ten of the twelve tools sessions had no Lean installed and said so, then answered without compiling. Two installed Lean and Mathlib themselves and compiled. Both of those compiled for me too. So the tools column here is mostly the no-tools experiment again, and the thing that determined whether a proof was checked was whether the session chose to spend twenty minutes building a toolchain. Nobody claimed a compile that had not happened.

I then reran the tools mode with one added paragraph telling the session to install Lean and Mathlib, compile before submitting, and treat the twenty minutes as part of the task. All twelve did it, all twelve say so and name the toolchain, and all twelve compile in my project. Against that, four no-tools samples per item give 40 of 48. The eight no-tools misses are four lemma names that do not exist in Mathlib, two `linarith` calls that do not close the goal, and two `positivity` calls on goals it does not handle; one statement (p09, a divisibility fact about powers) fails on three samples out of four, each differently. So the honest comparison is not 10 against 11. It is 12 of 12 with a checker against 40 of 48 without one, on statements where the proofs are short and the only thing that goes wrong is a name or a tactic the compiler would have flagged in a second.

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

### 3.11 Resampling: slips versus stable failures

Hypothesis, written before the runs: the misses in probes 02 and 10 split into slips (a second sample gets it right) and stable failures (every sample is wrong, and wrong differently), and the stable ones are the problems whose exact answer needs a computation the model cannot do in its head.

Three more no-tools samples on every item of probes 01, 02, 04 and 10. Probe 01: 48 of 48 on the final integer. Probe 02: 44 of 48, eleven of twelve on every sample but not the same eleven; p07 misses twice and p08 misses twice, with three different wrong numbers between them, and a majority vote over the four samples gets both right. Probe 04 is in 3.4. Probe 10:

| | original | rerun 1 | rerun 2 | rerun 3 | right |
|---|---|---|---|---|---|
| d(n) = d(n+1), key 102093 | 119811 | 111192 | 96280 | 108231 | 0 of 4 |
| sums of two squares, key 626 | 626 | 626 | 617 | 626 | 3 of 4 |
| 8-digit nondecreasing, digit sum 40, key 526 | 526 | 524 | 518 | 535 | 1 of 4 |
| subset sum, key 7026242 | 7026324 | 7031132 | 7029274 | 7026242 | 1 of 4 |
| tromino tiling, key 60 | 144 | 60 | 60 | 60 | 3 of 4 |
| obtuse triangles, key 58120 | 58045 | 58120 | 58120 | 58120 | 3 of 4 |
| other six | all right | | | | 24 of 24 |

35 of 48. The hypothesis held for the four original misses and missed something: p05 was right the first time and then wrong three times, with a long, fully shown breakdown into small partition counts that slips in a different place in each sample. That is a third kind: not a one-off slip, not an invented total, but a computation the model actually carries out on paper and gets wrong most of the time, the way a person would over a page of casework. Majority vote fixes the slips (p02, p09, p12) and does nothing for p01, p05 or p06, where the four samples are four different numbers.

The tiling and the triangles were slips. Three of three reruns got them right with the argument the first sample had set up and then fumbled. The divisor count and the subset sum were not. The divisor count went 0 for 4 with four different numbers spread over a 24 percent range. Two of the reruns say the count "is obtained by tabulating d over [1, 10^6+1]" and then give a figure, when no tabulation happened. One rerun also quotes the count below ten million as 986,262, which is correct; the model has the famous number from the sequence's page and nothing for the one I asked about, and fills the hole with a number in the same shape. The subset sum went 1 for 4. Two reruns wrote down the correct recurrence, printed intermediate values from it, one right and two wrong, and reported a total as if the table had been run. The one that got it right did something different: split the set into small and large elements, wrote out seven sub-totals, added them, and checked against the normal approximation.

### 3.12 Probe 05 reruns: what the prompt was for

The first run of probe 05 gave four guesses and eight abstentions in the no-tools column. I reran the same twelve items under two rewordings of the prompt's last paragraph. "Guessing is fine, put your best guess in the answer field and a confidence in the reasoning" gave twelve guesses, one of them right (a count of 7), with stated confidences between 1 and 35 percent. "A wrong answer counts against you more than no answer; if you have not read the paper, write abstain" gave twelve abstentions and no guesses.

| Prompt | Answered | Correct | Abstained |
|---|---|---|---|
| original | 4 | 0 | 8 |
| guessing allowed | 12 | 1 | 0 |
| wrong costs more than none | 0 | 0 | 12 |

So the four-and-eight split was not a property of the model. It was what the model does when the prompt does not say what the answer field is for. One sentence about the cost of a wrong answer moved the behaviour all the way to either side.

### 3.13 Probe 06 under the same two rewordings

Hypothesis: the same two sentences move probe 06 the same way, including the trap items where "not reported" is a valid answer the model could hide behind.

They did. Guessing allowed: twelve answers, no abstentions, two right. Wrong costs more than none: twelve abstentions. One of the two hits is worth a sentence. Asked for the mean uterine horn length in a human cohort, the guessing-mode session answered "not reported" and explained that humans do not have uterine horns. That is the correct answer reached by anatomy, not by reading, and it is the only no-tools biology answer in either probe that was right for a reason.

### 3.14 Probe 11: is it the computation or the math?

Probe 10's stable failures rested on two problems. Probe 11 was written to test the claim directly. Twelve pairs: a `p` item that needs a sieve, a DP table or a long sum, and a `q` item of the same shape with a parameter that makes it short by hand (the complement, a tiny case, a closed form). Each prompt also asks the session to end its reasoning with one word: EXACT, RECALLED or ESTIMATED.

Hypothesis: no-tools misses a good share of the `p` half and nearly none of the `q` half; tools gets both.

Tools: 24 of 24. No-tools: 12 of 12 on `q`, 10 of 12 on `p`. The direction is right and both misses are on the computation side, but the gap is smaller than probe 10 suggested, and the labels say why. Four of the ten correct `p` answers are labelled RECALLED, and in each case the reasoning names a table: distinct partitions of 60, domino tilings of a 4 by 12 board, twin primes below 10^5, lattice points in a circle of radius 1000. I picked round parameters and round parameters have published values. On the eight `p` items that were not recallable, no-tools got 6.

The two misses are the two behaviours from probe 10, one of them improved. On the 12-divisor count the session reached the point where it needed prime counts at odd cutoffs, said it was recalling them, labelled the answer ESTIMATED, and was off by two. On the coin-change count it set up a correct closed form for each of 121 cases, wrote "evaluating this gives 59246", and labelled it EXACT. The sum is 59576 and the 121 terms are not in the record. The label was informative when it was not EXACT: RECALLED was right four of four, ESTIMATED was wrong and said so. EXACT was right five times and wrong once, and the wrong one is the one a reader would have trusted.

### 3.15 One pass on the Lite tier

Probes 02 and 10, no-tools prompt, one sample each, Devin Lite. Probe 02: 8 of 12 (the default tier: 11 of 12 on each of four samples). Probe 10: 7 of 12 (the default tier: 8 to 10 of 12 per sample). The five Lite misses on probe 10 are the default tier's three stable misses plus the two problems it slips on once in four; nothing the default tier always got right was missed. Two of the Lite misses repeat the shape of a default-tier error (254 on probe 02 p07, and a two-off total on probe 10 p05 at the end of a shown breakdown), which hints that the errors have shapes and are not noise, but two probes and one sample cannot carry more than a hint. This is not a comparison of models; it is a note that the no-tools numbers in this report depend on which tier was running, and would need to be re-collected for any other.

## 4. What the gaps have in common

Reading the eleven write-ups together, the failures sort into four kinds, with a fifth that the resampling separated out of the fourth. One of them is what I expected, one I did not expect, and two only appeared once I made the problems hard enough.

### 4.1 Reasoning slips (probes 01, 02, 04)

A missing factor in one branch of a case split. A construction asserted to satisfy a condition it does not. A lemma name that does not exist. A recurrence copied wrong from a correct state machine. These are the errors I set out to find. They exist, they are rare at this difficulty (4 of 48 on probe 02, 8 of 48 on probe 04, and on probe 10 the three slip items missed 3 times in 12), and they share a signature: the error is local, the surrounding work is correct, nothing in the output flags uncertainty, and a second sample usually does not make the same mistake. They vanish when the model can run code or compile, because it stops trusting its own casework and enumerates instead. They also mostly vanish under self-consistency: a majority over four samples fixes every slip in probes 02 and 10. It fixes nothing else, which is how I tell the slips from the next two kinds.

One item does not fit cleanly. Probe 10 p05 is a long computation the model does carry out, in full, on paper, and gets wrong three samples out of four in three different places. That is neither a local slip nor an invented number. It is what a person does with a page of casework and no calculator, and the fix is the same: do not do it by hand.

### 4.2 Field confusion (probes 05, 06)

This is the one I did not expect, and I think it is the most useful finding in the report. When the model does not know the answer, it does not invent a confident story. It splits itself. The `reasoning` field says "I did not read this paper, this is a guess" or "I cannot verify this." The `answer` field gets a bare number, or the phrase "not reported" borrowed from the prompt's own instructions.

To a person reading the whole reply, this is honest. To a pipeline reading only `answer`, it is four fabricated facts and three false claims about what a paper contains. Seven of twenty-four no-tools biology items behaved this way, and the probe 10 estimate is the same shape in a different subject: "this is an analytic estimate, not an exact enumeration" in the reasoning, a number to seven digits in the answer.

The rerun in 3.12 changes how I read this. I first wrote that the model treats the answer slot as a form that must be filled. That is half right. It treats the answer slot as a form whose purpose it has to infer, and when the prompt gives no hint it guesses, and different sessions guess differently. Tell it that a wrong answer costs more than no answer and it abstains twelve times out of twelve. Tell it guessing is fine and it guesses twelve times out of twelve, with a confidence number that in this case was honest (the one hit came with 15 percent). The model was never unsure whether it knew the answer. It was unsure what I wanted done with the slot, and I had not said. That makes this less a model failure and more a schema failure, and a cheap one to fix.

### 4.3 Environment, not model (probe 04)

Ten of twelve tools sessions could not compile Lean because Lean was not installed. Two decided to install it. The proofs from all twelve were of similar quality, but only two were verified. Nothing about the model's ability changed between those sessions; what changed was a decision about whether to spend time on setup. In a real deployment this decision is made by whoever configures the environment, and it decides whether the task is checkable at all.

The rerun settles what the checker is worth here. Told to install and compile, twelve of twelve sessions did, and twelve of twelve proofs compile. Without the checker, 40 of 48. Every one of the eight misses is a thing the compiler names on the first try: a lemma that does not exist, a tactic that does not close the goal. None of them is a wrong proof idea. So on statements at this level the model's Lean ability is not the limit; whether anyone pointed it at a compiler is.

### 4.4 Narrated computation (probe 10)

This is the one that only showed up at the higher difficulty, and it is the one I would worry about. On the two problems that need a computer, the no-tools mode did not say so. It described the computation ("tabulate d over [1, 10^6+1]", "iterate the recurrence through n = 30") and then reported an output, and the output was wrong every time it did this, six sessions out of six across the two problems. The one rerun that got the subset sum right did not narrate; it did a different, smaller decomposition it could actually carry, and wrote out the pieces.

What distinguishes this from a slip is that it is stable. Four samples on the divisor count gave four wrong answers. Self-consistency does not help, because the samples disagree with each other and none is right. A reader checking the argument does not help either, because the argument is correct; what is missing is the arithmetic, and the arithmetic is a million-term sieve. And a source name is attached in most cases, which is where the word fabrication becomes fair. This failure is removed completely by letting the session run code, and I could find nothing else that removes it.

Probe 11 narrows the claim. The variable is not the size of the computation by itself; it is whether the exact number is somewhere in memory. When it is, the model recalls it and, asked to label what it did, says RECALLED, and it was right every time it said so. When the number is not in memory and the arithmetic is long, the model sometimes does the arithmetic (five of the eight non-recallable `p` items, with intermediate values shown) and sometimes writes down a total that was never computed and calls it EXACT (one of eight). Asking for the label did not stop the one narrated total. It did produce one honest ESTIMATED on the item where probe 10 had produced four confident wrong numbers, which I count as a small win for asking.

The practical difference between the invented total and the shown-but-wrong computation (probe 10 p05) matters for a reader: the second can be checked line by line and the first cannot, because there are no lines. Both give scattered numbers across samples. Only reading the reasoning tells them apart.

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

**Take more than one sample when it is cheap.** Probes 02, 04, 10. Every slip in this suite is fixed by a majority over four samples. None of the stable failures is; on those the four samples are four different numbers and the vote has no winner. So the vote is also a diagnostic: if there is no majority, do not trust any of them.

**Ask the model what it did, and read the answer.** Probe 11. A one-word label (EXACT, RECALLED, ESTIMATED) at the end of the reasoning was right every time it said RECALLED or ESTIMATED. It was wrong once when it said EXACT. That makes it useful as a filter for the honest cases and useless as a guarantee, which is still better than nothing.

**Do not trust round parameters.** Probe 11. Four of my twelve "needs a computation" items had published answers because I chose n = 60, radius 1000, primes below 10^5. The model knew the tables. Anyone writing a probe like this should nudge every parameter off the round number.

And one thing that is not a warning: with a precise spec and a browser, every task in this suite that a competent person could do in an afternoon, the agent did in one pass. The boundary is not there.

## 6. Limits

- **Small samples.** Four no-tools samples per item on probes 01, 02, 04 and 10; one everywhere else, including every tools cell and all of probe 11. Every number here is a count of what happened, not an estimate of a rate. Where I went from one sample to four, the story changed on two probe 10 items (p02 and p05 turned out to be unstable), which is the argument for doing it everywhere and for not trusting the one-sample cells more than I do.
- **One system, one default tier, two modes.** The system under test is Devin on two days in September 2026. I cannot name the model underneath or hold it fixed. One pass on the Lite tier gave lower no-tools numbers on both probes tried, and that is all it can say. Another vendor's model might behave differently on field confusion in particular, since that is plausibly a training artifact.
- **No human baseline yet.** `baseline/README.md` is a protocol for one person to do probe 02 timed, on paper, with no tools. It has not been run. Until it is, "a patient sophomore could do this" in section 3.10 is my guess.
- **Contamination.** Probe 03 is fully contaminated by design and should be read as a recall test. Probe 10 has one exact answer online out of twelve. Probe 11 has four of twelve `p` answers in published tables, which the model used. The checks were one search per item, run after the experiment; they say what is findable, not what any session saw.
- **Probe 11 is one sample.** Its 10 of 12 could be 8 or 12 on the next run. Probe 10 needed four samples per item before the pattern was clear and probe 11 has not had that treatment.
- **Two difficulty levels only.** Probes 01 to 03 are first-year level and found almost nothing. Probe 10 is competition level and found a third. There is a lot of room between them and I do not know where the curve bends.
- **Prompt variants were tried on probes 05 and 06 only.** They transferred from 05 to 06 completely. Whether "wrong costs more than none" would also turn the probe 10 estimate into an abstention is untested.
- **Probe 09 acceptance checks are mine.** What counts as a hard check versus a judgment check is my call, made before the run but still a call. Someone else might grade the collision behaviour as fine.
- **Hand-checked constructions.** Only five of twenty-four probe 01 constructions were checked, by me, by hand. A script that parses and verifies constructions would let me check all of them.
- **Prompt engineering by me.** The probe 06 re-run shows that my prompt wording changed what the sessions could do. I documented it, but a different phrasing could shift other results too.

## 7. What changed since week 7

Reserved for reruns on any model released mid-semester. Nothing to report yet.

## 8. Next probes

In rough priority order. Items 5 and 6 from the first draft became probes 09 and 10 and the reruns in 3.11 and 3.12.

1. Run the human baseline in `baseline/`.
2. Probe 11 again with every parameter off its round number, and four samples per item, so RECALLED is not available and the `p` versus `q` gap is measured rather than glimpsed.
3. A construction grader for probe 01, so every certificate is checked; the other 43 no-tools constructions are graded on the integer only.
4. Probe 03 with unpublished false claims: a true theorem with one hypothesis weakened, or a constant changed so the first counterexample is above 10⁴.
5. Probe 04 at a difficulty where compile failures return even with the checker, and a test of whether the model repairs from the compiler message.
6. The "wrong costs more than none" sentence on the probe 10 estimate, to see whether it turns into an abstention.
7. Probe 09 with the tools sessions told to write tests before code, to see whether the edges they miss change.
8. A probe where the number only exists in a plot, which needs image input and a different harness.

## Appendix A: taxonomy

See `report/taxonomy.md` for the running table, one row per failure type, with the probe and example for each.

## Appendix B: reproducing

Each `results.md` gives the grade command. Raw outputs are in `probes/*/outputs/`, unmodified except for three documented grader normalizations (word numbers to digits, "Unable to verify" and the bare word "abstain" counted as abstention). Every output links to its session and stores the exact prompt it was given. Resampled outputs are `sample_1` to `sample_3` next to the original `sample_0`. Variant runs are in their own mode folders: `notools-guessok/` and `notools-penalty/` (probes 05, 06), `tools-lean/` (probe 04), `notools-lite/` (probes 02, 10). Probe 04 grades are in `key/lean_grades.json`, probe 11 grades in `key/grades.json`, and the contamination notes in `key/contamination.md` for probes 03 and 10.
