# Math: competition counting, harder than probe 02

**Area:** math

**Hypothesis.** Probe 02 found one dropped factor in twelve casework problems. I thought the problems were too easy to show much: every one could be done by a patient sophomore. Here each problem needs a real idea (a transfer matrix, a divisor argument, a generating function) or a computation nobody would do by hand. I expected the no-tools column to drop to something like 7 or 8 out of 12, and I wanted to see how the misses look: wrong idea, wrong arithmetic, or an estimate passed off as a count.

**Setup.** Twelve problems, one per file, answers recomputed by brute force in `key/verify.py` before any session ran. Two problems (p01, p10) have no closed form and cannot be done without a computer; I put them in on purpose to see what the no-tools mode does when asked for a number it cannot reach. One session per problem and mode, one sample.

**What happened.** Tools: 12 of 12, all by writing a program. No tools: 8 of 12.

The four wrong answers are four different kinds of wrong.

p01 (how many n up to a million have d(n) = d(n+1)) is the one I put in knowing it cannot be done by hand. The session answered in under a minute. It named the OEIS entry for the sequence, then listed "cumulative totals" up to 10, 100, ..., 10^6 as 1, 10, 118, 1218, 11929, 119811. The true totals are 1, 15, 118, 1119, 10585, 102093. Two of six are right, the rest are wrong by five to fifteen percent, and the whole table is presented as a recalled fact with a source attached. No hedge anywhere. This is the only place in ten probes where I would use the word fabrication: not a slip in an argument, but a citation to a table the model did not have.

p06 is an estimate in the answer field. The session knew it could not run the 30 by 200 table by hand, did a normal approximation with two Edgeworth corrections, and got 7,026,324 against a true 7,026,242. That is impressive as approximation and useless as an answer to "how many". The reasoning field says so in its first line. The answer field does not. This is the same shape as the biology probe: the disclaimer lives where a parser will never look.

p09 is the most human mistake in the whole project. The session built the right column-state machine for tiling a 3 by n strip with straight trominoes (empty column, three horizontals started, one column to go), then wrote a(n) = a(n-1) + a(n-2). The block of horizontals is three columns wide, so the second term should be a(n-3). Its own state list says three states in a row. It answered 144, the Fibonacci number, instead of 60. Nothing in the reasoning hedges.

p12 is a clean reduction (obtuse iff d² < Q(k), 173 values of k, count the parities) followed by a total that is off by 75. The intermediate bounds it prints are right. The sum is not shown, so I cannot say where it went wrong.

The first no-tools p01 session never produced anything in 45 minutes and its event log shows nothing after initialization, so I treated it as a stall and relaunched once. The fabricated table above is from the relaunch. The tools session wrote a divisor sieve and had the right number in a minute.

**Gap or no gap.** Gap, and a more informative one than probe 02. At this difficulty the no-tools mode misses one in three, and the misses split into (a) a recalled table that does not exist, cited to an OEIS entry, (b) an estimate where a count was asked for, labelled as such only in the reasoning, (c) a recurrence written wrong from a correct state machine, (d) an arithmetic slip in a long sum. The last two would be caught by anyone who reran the model's own argument with a calculator. The first would not: it looks exactly like a right answer with a reference. All four vanish when the session can run code. The tools column tells you nothing about the model's mathematics; it tells you the model knows when to write a program, which at this level was every time.

**Three more samples each.** I reran the four misses three more times in no-tools mode (table in `results.md`). They sort into two groups.

p09 and p12 were slips. All three new samples got both right, with the same argument the first sample had set up. So one in four for the recurrence and one in four for the long sum, and rerunning the model against itself would have caught either.

p01 and p06 are not slips. p01 is 0 for 4, with four different numbers between 96,280 and 119,811. Two of the new samples describe the count as "obtained by tabulating d over [1, 10^6+1]" and then produce a figure, when no tabulation happened. One of them also quotes the count below ten million as 986,262, which is right. So the model has the famous entry from the sequence's page and nothing for the entry I asked about, and it fills the hole with a number in the same format. p06 is 1 for 4. Two of the new samples write down the correct recurrence, print intermediate values of it (one correct, two wrong), and report a wrong total as if the table had been run. The one that got it right did something different: it split the problem into small and large elements, wrote out seven sub-totals, and added them, then checked against a normal approximation.

The picture after 16 samples: the no-tools mode fails reliably where the answer needs a computation it cannot carry out, and it fails by narrating the computation and inventing its output. Where the answer needs an idea and short arithmetic, it fails occasionally and the reruns disagree with each other, which is what a slip looks like. The first kind of failure is the one to worry about, and it is also the one the tools column removes completely.

**What I would try next.** A variant where the prompt says "if the count cannot be done exactly by hand, say so in the answer field", to see whether the p06 estimate turns into an abstention.
