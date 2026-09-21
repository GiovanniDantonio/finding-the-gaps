# Math: long constructions

**Area:** math

**Hypothesis.** Extremal problems ask for a number and a construction that reaches it. My guess was that the model would get the number right by recall and then produce a construction that does not actually work, because checking a construction takes patience and the model tends to assert instead of check. I expected the gap to be bigger with tools turned off.

**Setup.** 12 problems, each asking for a maximum, minimum or count on a small finite object (subsets of {1..50} with forbidden differences, tilings, queens, no three in a line on a 5x5 grid, Latin squares, and so on). Every answer is recomputed by brute force in `key/verify.py`. Each problem ran as its own Devin session in two modes: normal, and told in the prompt not to use any tool. One sample per cell so far. The grader checks the final integer. I checked the constructions by hand for five problems.

**What happened.** 24 out of 24 final answers were right. With tools on, the model wrote a brute force search for 5 of the 12 problems and reasoned the rest. With tools off it obeyed the instruction every time (no shell, file or browser events in any of the 12 sessions) and still got every number, including the 21 digit count for p07, which it got by spotting that the even terms of the recurrence are squares of Fibonacci numbers.

The one failure is the one I predicted. On p06 (10 points in a 5x5 grid, no three collinear) the no-tools run gave the right number and a set of 10 points that has two collinear triples: (1,0),(2,1),(3,2) and (0,1),(1,2),(2,3), both on lines of slope 1. The reasoning even lists the values of y minus x for the ten points, 1,-1,4,-4,-1,1,1,0,-1,0, and says each value appears at most twice. Both 1 and -1 appear three times in its own list. The run with tools on found a valid set by exhaustive search. The full text is in `outputs/notools/p06/sample_0.json`.

**Gap or no gap.** Small gap, and not where the grader looks. The numbers here were too well known: most of these are textbook results, so getting the integer says little. The gap shows up in the certificate. When the model cannot run code it will state that it verified something and be wrong about it, in a way that is visible in its own output. One instance out of five checked is not a rate, so this needs more samples before I call it more than an anecdote.

**What I would try next.** Three samples per cell, and check every construction with a script rather than by hand, since that is where the failure lives. Replace the well known problems with variants that have the same shape but numbers nobody has published (a 6x7 grid, forbidden differences 3 and 7, a 2x13 board). Add a grader that parses the construction, not just the integer.
