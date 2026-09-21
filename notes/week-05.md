# Week 5: Probe 04, Lean

To: Christopher Thorpe

Probe 04: 21 of 24 compile. Three failures, all invented or misapplied Mathlib API: a lemma that does not exist, a field taken from an equation as if it were a coprimality proof, and linarith asked to close a goal it cannot. All caught by the compiler in a second.

The surprise: ten of twelve tools sessions had no Lean installed, said so, and answered without compiling. Two installed it themselves and their compiles were real. So whether a proof got checked depended on whether the session felt like spending twenty minutes on setup.

Question: for the rerun, should I provide a prebuilt Mathlib project so every session can compile, or is the current result (environment decides checkability) the more interesting one to keep?
