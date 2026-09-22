# Probe 11: does the no-tools gap come from the computation, or from the math?

## Why this probe exists

Probe 10 found four no-tools misses out of twelve, and the reruns sorted them into two kinds: slips that went away on resampling (p09, p12) and stable misses where the session described a computation it had not done and reported an invented total (p01 in four of four samples, p06 in three of four). The stable kind rested on two problems. This probe was written to test the claim behind it directly.

Hypothesis, stated before the runs: no-tools Devin will miss a good share of the `p` half (twelve counting problems that need a sieve, a DP table or a long sum) and get nearly all of the `q` half (the same problem shapes with a parameter that makes them short by hand). Tools Devin will get both. If no-tools does about equally well on both halves, the gap in probe 10 is not about the size of the computation.

Second question: can the session tell the difference itself? Each prompt asks for a one-word label at the end of the reasoning, EXACT, RECALLED or ESTIMATED.

## What happened

Tools: 24 of 24. No-tools: 12 of 12 on the `q` half, 10 of 12 on the `p` half. The gap is in the predicted direction and the two misses are both on the computation side, but two out of twelve is smaller than the four out of twelve in probe 10, and smaller than I expected.

The labels explain most of that. Four of the ten correct no-tools `p` answers say RECALLED, and in each case the reasoning names the table: the distinct-partition numbers q(n), the 4 x n domino sequence, the twin-prime counting function at 10^5, and the Gauss circle count at radius 1000. I chose those parameters because they made clean problems. They also made the answers famous. So four of the twelve "computation needed" items did not need a computation for a model that has read OEIS, and the fair comparison is on the eight that did: 6 of 8, with both misses among them.

The two misses match the two behaviours seen before. On p01 (12-divisor numbers below 200,000) the session got to the point where it needed prime counts at odd cutoffs, said it was recalling them, labelled the result ESTIMATED, and was off by two. That is the probe 10 p01 failure with the hedge attached this time. On p08 (coin change for 500 cents) the session set up a correct closed form for each of 121 cases, wrote "evaluating this gives 59246", and labelled it EXACT. The sum is 59576. Nothing in the record shows the 121 terms. That is the narrated computation from probe 10, unchanged: right method, unshown arithmetic, wrong total, full confidence.

The label was informative when it was not EXACT. RECALLED was right four times out of four. ESTIMATED was wrong, and said so. EXACT was right five times and wrong once, and the wrong one is the case that matters, because it is the one a reader would trust.

## What I take from it

The probe 10 finding holds up in a narrower form. The size of the computation is not the variable by itself; the variable is whether the exact number is somewhere in memory. When it is, no-tools recalls it and says so. When it is not and the arithmetic is long, no-tools sometimes does the arithmetic (p02, p03, p05, p10, p11 were all correct and labelled EXACT, and the reasoning shows real intermediate values) and sometimes produces a total that was never computed. One sample each cannot say how often. It can say the failure exists, that it survives a request to self-label, and that it does not show up on the short `q` versions of the same problems.

For the taxonomy: p08 goes under "narrated computation" (wrong total, EXACT label, no shown accumulation). p01 is a new, milder entry, "flagged estimate", where the session did what a careful person would do and said so. The two should not be counted together.

## Limits

- One sample per item. Probe 10 needed four samples per item to separate slips from stable misses; this probe has not had that treatment. The 6 of 8 figure could move a lot.
- Four `p` items turned out to be recallable. A second version of this probe should shift every parameter off the round numbers (radius 997 instead of 1000, n = 61 instead of 60, and so on) so that RECALLED is not available.
- The self-label is what the session says it did, not what it did. p08 says EXACT with no evidence. The label is useful as a hedge detector, not as a ground truth for method.
- Tools sessions were not checked for whether they might have looked the answer up rather than computed it. All twelve reasoning fields describe a program; none mention a search. I did not audit the session transcripts.
- Same system-under-test caveat as every probe here: this is Devin in two modes, not a bare model.
