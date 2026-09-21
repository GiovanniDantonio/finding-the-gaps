# Math: heavy casework

**Area:** math

**Hypothesis.** Counting problems that split into many cases are where I lose points on paper, so I expected the model to lose them too when it cannot run code: skip a case, double count, or drop a factor. With code available the problems are trivial, so the interesting column is the no-tools one.

**Setup.** 12 counting problems with answers in the hundreds to tens of thousands, all with parameters I picked so the exact numbers are not in a textbook (digit sum 20 up to a million, four couples with exactly two adjacent, paths between two diagonal walls, and so on). `key/verify.py` recomputes each answer by brute force. Same two Devin modes as probe 01, one sample each.

**What happened.** With tools, 12 out of 12, and the model wrote a script every single time, usually a five line brute force, then reported the number. It did not try to reason any of them by hand.

Without tools, 11 out of 12. Several of the no-tools answers are real casework carried through correctly: p07 (three consecutive squarefree numbers up to 2000) went by inclusion and exclusion over residue classes mod 4p^2 for every prime p up to 43 and landed on 251. p12 (subsets of 1..15 summing to 60) went by size and used the complement symmetry. I would not have got either of those right in one pass.

The miss was p08, two pair hands containing the ace of spades. The case where the ace of spades is part of the ace pair needs a factor of 3 for which other ace joins it. The reasoning writes "12 times 6 times 11 times 4 = 3168" and never mentions the second ace's suit. The other case (ace of spades as the kicker, 2376) is right, so the total came out 5544 rather than 11880. This is exactly the kind of error I expected, it is just rarer than I expected.

**Gap or no gap.** Small gap, one in twelve, only without tools. The failure looks like a human one: an early case set up with one factor missing, then carried cleanly to a wrong total. Nothing in the write-up flags uncertainty. With tools the gap disappears entirely because the model does not trust its own casework either and just enumerates.

**What I would try next.** Three samples on p08 to see if the miss is stable or a coin flip. Push the case count up: problems where brute force also becomes awkward (say 10^9 range) so the tools mode has to think as well. Ask for the count per case in a fixed table format so I can see which case breaks rather than only the total.
