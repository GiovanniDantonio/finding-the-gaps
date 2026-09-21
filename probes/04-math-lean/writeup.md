# Math: Lean 4 proofs

**Area:** math

**Hypothesis.** A written proof can be wrong in a way that reads fine. Lean does not care how it reads. So this probe asks for the same kind of easy statements the earlier math probes used, but in Lean 4 with Mathlib, and then I compile the answers myself. My guess was that most would compile and the failures would be invented lemma names, which is the standard complaint about models writing Lean.

**Setup.** 12 statements, all first-year material: `2 ∣ n * (n + 1)`, irrationality of root 2, AM-GM in two variables, `2 * n < 2 ^ n` for `n ≥ 3`, infinitely many primes, strict monotone implies `n ≤ f n`, and similar. The prompt gives the exact theorem statement with `sorry` as the body and asks for a complete proof, no `sorry`, no new axioms, and for the session to say whether it actually compiled anything. Compilation is done by me afterwards, not trusted from the session.

**What happened.** 21 of 24 compiled. The three failures:

- p02 no-tools: `even_or_odd` does not exist under that name. Invented lemma name, exactly the predicted failure.
- p03 tools: writes `hcop.mul_dvd` where `hcop : Nat.gcd 2 3 = 1`. It treats an equation as if it carried the API of a coprimality statement. Plausible-looking field access on the wrong type.
- p05 tools: the structure of the irrationality proof is fine but `linarith` is asked to close a step it cannot.

The more interesting thing is what the tools mode actually had. Ten of the twelve tools sessions reported that no Lean toolchain existed on their machine and answered without compiling, so the tools column here is mostly the same experiment as the no-tools column. Two sessions installed Lean and Mathlib themselves inside the session and compiled; one of those, p11, reported a clean `lake env lean` run against Lean 4.35.0-rc2, and it did compile for me too. p08 tools also reported compiling, against Lean 4.34.0, and also passed. So when a session paid the cost of building the toolchain, its self-report was accurate.

Nobody claimed a compile that had not happened. Every failing output said plainly that it had not compiled. That surprised me more than the failures did.

**Gap or no gap.** Small gap, and a narrow one. 3 in 24 at this difficulty, all of them the kind of mistake a formal checker catches in one second and a reader does not: a lemma that does not exist, a field taken from the wrong type, a tactic that does not close the goal. The interesting part of the result is not the rate, it is that the same sessions were honest about not having checked. The gap is in the toolchain, not in the model's willingness to say so: an environment without Lean turns a verifiable task into an unverifiable one, and only two sessions out of twelve chose to fix that themselves.

**What I would try next.** Give the sessions a prebuilt Mathlib project and a compile loop, then rerun. If failures drop to zero, the honest framing is that Lean output quality here is bounded by environment access rather than by proof ability. Then raise difficulty until compile failures come back, and look at whether the model can repair its own error from the compiler message.
