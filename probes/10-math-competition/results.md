# Results: Math: competition counting, harder than probe 02

Twelve problems in `problems/`, every answer recomputed by `key/verify.py` (brute force or exhaustive DP, three seconds total). One Devin session per (problem, mode), one sample each, 2026-09-21 and 22. Raw outputs with session links in `outputs/`.

| Mode | Correct | Wrong |
|---|---|---|
| tools | 12 / 12 | 0 |
| notools | 8 / 12 | 4 |

Per problem (T = tools, N = no tools):

| | p01 | p02 | p03 | p04 | p05 | p06 | p07 | p08 | p09 | p10 | p11 | p12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| key | 102093 | 626 | 136800 | 32032 | 526 | 7026242 | 6 | 1998 | 60 | 516788 | 9 | 58120 |
| T | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok |
| N | 119811 | ok | ok | ok | ok | 7026324 | ok | ok | 144 | ok | ok | 58045 |

The four no-tools misses:

- p01 (d(n) = d(n+1) for n up to a million): the reasoning names the OEIS entry for this sequence and gives "cumulative totals up to 10^k for k = 1..6" as 1, 10, 118, 1218, 11929, 119811. The true totals, from the sieve in `key/verify.py`, are 1, 15, 118, 1119, 10585, 102093. Two of the six recalled values are right. The rest look like memory of a table that was never seen, dressed as a citation. Nothing in either field says it is uncertain.
- p06 (subsets of 1..30 with sum 200): answer field holds 7026324, an Edgeworth-expansion estimate that is off by 82. The reasoning field opens with "Caveat: this is an analytic estimate, not an exact enumeration."
- p09 (3 x 12 tiled by straight trominoes): the session set up the right column states (empty, three horizontals started, one column left) and then wrote the recurrence as a(n) = a(n-1) + a(n-2). The three-horizontal block is three columns wide, so the term is a(n-3). Its own state machine says so. 144 is the Fibonacci number; 60 is the right count.
- p12 (obtuse integer triangles, perimeter 2026): a correct reduction to a sum over 173 values of k, then a wrong total (58045 vs 58120). The intermediate bounds it reports are right; the accumulation is not shown and is not right.

The first no-tools p01 session (linked in the output file's `note`) sat for 45 minutes with no events after initialization and never produced output. I treated that as a harness stall, not a model behaviour, and launched one replacement with the identical prompt. Only the replacement is graded.

## Three more no-tools samples on the four misses (2026-09-22)

Same prompt, same mode, `sample_1` to `sample_3` in each folder. Sample 0 is the original.

| | s0 | s1 | s2 | s3 | correct |
|---|---|---|---|---|---|
| p01 (key 102093) | 119811 | 111192 | 96280 | 108231 | 0 / 4 |
| p06 (key 7026242) | 7026324 | 7031132 | 7029274 | ok | 1 / 4 |
| p09 (key 60) | 144 | ok | ok | ok | 3 / 4 |
| p12 (key 58120) | 58045 | ok | ok | ok | 3 / 4 |

p01: four different wrong numbers spread over a 24 percent range. s1 and s3 say the count "is obtained by tabulating d over [1, 10^6+1]" and then give a number, with no tabulation having happened. s1 adds "since no tools were used, the value is recalled rather than recomputed", which is the only hedge in the four. s3 also gives 986262 as the count below 10^7; that one is right (I checked with a sieve), so the recall is real for the famous value and wrong for the one I asked about.

p06: s1 states D(20,200) = 10 as an intermediate, which is correct, then reports a wrong final. s2 states D(20,200) = 155 and D(25,200) = 424296, both wrong (true 10 and 219087). s3 splits the set into small and large elements, sums seven per-size totals it writes out, and lands on the exact answer, then checks it against a normal approximation.

p09 and p12: the other three samples each got the right answer with the right argument. The s0 recurrence slip and the s0 sum slip did not recur.

Every tools session wrote a short program. On p01 and p10 there is no other way; on p07, p09 and p11 the program was a check on a hand argument that was already right.

## Three more no-tools samples on all twelve (2026-09-22)

The reruns above covered only the four misses. `sample_1` to `sample_3` now exist for every problem.

| | s0 | s1 | s2 | s3 | correct |
|---|---|---|---|---|---|
| p01 (key 102093) | 119811 | 111192 | 96280 | 108231 | 0 / 4 |
| p02 (key 626) | ok | ok | 617 | ok | 3 / 4 |
| p05 (key 526) | ok | 524 | 518 | 535 | 1 / 4 |
| p06 (key 7026242) | 7026324 | 7031132 | 7029274 | ok | 1 / 4 |
| p09 (key 60) | 144 | ok | ok | ok | 3 / 4 |
| p12 (key 58120) | 58045 | ok | ok | ok | 3 / 4 |
| other six | ok | ok | ok | ok | 24 / 24 |

35 of 48 overall; per sample 8, 9, 8, 10. Two problems that were right in the original sample turned out to be unstable: p02 missed once, and p05 (8-digit nondecreasing numbers with digit sum 40) was right only in the original and gave three different wrong totals afterwards, each from a correct reduction (partitions of 32 in an 8 x 8 box) followed by a long recursive breakdown with dozens of small partition counts written out. The breakdowns are shown, and they differ from each other; somewhere in each one a small count is wrong. That is a different failure from p01 and p06, where the arithmetic is not shown at all: here it is shown and slips, the way a person's would over a page of casework.

Majority vote over four samples: right on p02, p09, p12 (and the six that never miss); no majority at all on p01, p05, p06, where the four samples give four different numbers. So the vote fixes the slips and does nothing for the stable misses. p01 and p06 give scattered numbers because the totals are invented; p05 gives scattered numbers because a long shown computation slips in a different place each time. Same signature, different cause, and only reading the reasoning tells them apart.

## Lite tier, no tools, one sample (2026-09-22)

Same no-tools prompt as a Devin Lite session, `outputs/notools-lite/`. 7 of 12. Misses: p01 (105074), p02 (633), p05 (528), p06 (7029544), p12 (42756). The default tier's three stable misses (p01, p05, p06) are all misses here too, and p02 and p12, which the default tier slips on once in four, are missed once here. Every problem the default tier got right on all four samples, Lite got right. p05's 528 is two off the key, the same near-miss shape as the default tier's shown-and-slipped breakdowns; p12's 42756 comes from a recalled formula (floor(N^2/24)) applied to a problem it does not fit. One sample, one tier: a check that the hard problems are the same hard problems, not a ranking.

The first p11 Lite session sat at "working" for 35 minutes with no output and was replaced by an identical session (noted in the record); the replacement answered in a few minutes. Not counted as a model failure, same rule as the default-tier p01 stall.
