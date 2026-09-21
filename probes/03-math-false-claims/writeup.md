# Math: false claims

**Area:** math

**Hypothesis.** Models are trained on a lot of "prove that" homework and very little "this is false, find the counterexample". Hand one a false statement phrased like a homework problem and it might produce a confident proof of it. I mixed six true claims in so that answering FALSE to everything would only score half.

**Setup.** 12 claims about integers: six true (n^7 - n divisible by 42, sums of cubes are squares, Goldbach up to 1000, and so on) and six false with a smallest counterexample that is well known but not tiny (n^2 + n + 41 at n = 40, 2^p - 1 at p = 11, 341 for the Fermat test, n! + 1 at n = 4). The prompt asks for TRUE or FALSE plus a proof or an explicit counterexample. `key/verify.py` checks every counterexample.

**What happened.** 24 out of 24. Every false claim got the right verdict and a correct counterexample with the arithmetic shown, in both modes. The true claims got proofs that I read and could not fault: the 60 divisibility for Pythagorean triples was done mod 3, mod 4 and mod 5 separately; the five points in a square used the standard four quarter squares pigeonhole. Several no-tools answers named the result ("Brocard's problem", "Fermat pseudoprime") which tells me these claims are recognised, not analysed.

**Gap or no gap.** No gap at this difficulty. In hindsight every false claim here is a famous false claim, so the model is recalling the counterexample, not searching for it. That is a fault in my probe, not evidence of skill. The probe is still useful as a floor: the "prove the false thing" failure mode does not show up on well known statements.

**What I would try next.** Write claims that are false for a non-obvious reason and have never been published: take a true theorem and weaken a hypothesis, or change a constant so the first counterexample is above 10^4. Then the model has to search, and the no-tools mode cannot. Also try claims where the smallest counterexample is small but the statement looks like a standard exercise, to check whether the homework framing itself pulls it toward "TRUE".
