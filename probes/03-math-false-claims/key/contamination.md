# Contamination check

Date: 2026-09-22. Method: one web search per claim (claim text plus "counterexample" or the
famous counterexample), top four results recorded, then a check of whether the result page
states the claim and its truth value. Raw search dumps are not committed.

| Claim | Online status | Where |
|---|---|---|
| p01 n^2+n+41 prime | Famous (Euler's polynomial), n=40 counterexample on many pages | math.stackexchange 2535743, 495253 |
| p02 2^p-1 prime for prime p | Famous, 2^11-1 = 23*89 | math.stackexchange 1160699, 1870988 |
| p03 Fermat numbers prime | Famous, 641 divides F5 | Wikipedia "Fermat number" |
| p04 n divides 2^n-2 implies prime | Famous ("Chinese hypothesis"), 341 | Wikipedia "Chinese hypothesis" |
| p05 gcd(n^2+1,(n+1)^2+1)=1 | Textbook exercise, appears as an MSE question | math.stackexchange 3106694 |
| p06 Goldbach up to 1000 | Verified far beyond 1000 in the literature | Wikipedia "Goldbach's conjecture" |
| p07 42 divides n^7-n | Textbook exercise (Niven 2.1.20), MSE | math.stackexchange 22121 |
| p08 sum of cubes is a square | Textbook identity | Wikipedia "Squared triangular number" |
| p09 n!+1 never a square | Famous (Brocard), 4!+1 = 25 | Wikipedia "Brocard's problem" |
| p10 a^2 divides b^2 implies a divides b | Textbook exercise, MSE | math.stackexchange 182988 |
| p11 abc divisible by 60 | MathOverflow question with the same statement | mathoverflow 4318 |
| p12 five points in a unit square | Textbook pigeonhole exercise | math.stackexchange 952306 |

Verdict: all twelve claims, with their truth values, are on the open web with the same or nearly
the same wording. The 12/12 in both modes should be read as recall of well-known facts, not as
a test of finding counterexamples from scratch. A fresh version of this probe would need claims
written for it, ideally with a parameter changed so the famous counterexample no longer applies.
