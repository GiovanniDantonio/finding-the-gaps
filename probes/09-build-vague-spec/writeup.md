# Software: four one-sentence specs

**Area:** software

**Hypothesis.** Probes 07 and 08 found no gap, and I think the spec did the work: I had named every edge case. Here the spec is one sentence ("remove duplicate rows from a CSV on stdin", "print the ten most common words in a file", "flatten a nested JSON object to dotted keys", "print the days between two dates"). The checks are the things a careful engineer fills in without being asked: headers, quoting, empty input, bad input, a missing file. I expected the no-tools mode to miss more of these than the tools mode, since running the code is how you usually find out that `{}` does something odd.

**Setup.** Four tasks, hidden checks written first. Each check is tagged hard or judgment. Hard means any reasonable reading of the sentence has to pass (empty input should not crash, a missing file should not print a traceback). Judgment means the sentence does not decide it (case folding in word counts, sign of a reversed date difference) and the check passes for any of the reasonable behaviours. I also asked every session to list, in the reasoning field, the decisions the sentence left open, and to say whether it ran the code.

**What happened.** The two modes produced the same score on every task, and failed the same checks: 22 of 24 hard, 10 of 11 judgment, each.

Both `wordfreq.py` scripts print a Python traceback when the file does not exist. Both `jsonflat.py` scripts turn `{}` into `{"": {}}`, because they keep empty objects as leaf values and the top-level object has no key. Both flatteners let a literal key `a.b` collide with a flattened path `a.b` and keep whichever came last; both sessions wrote that down as a decision, so it is a choice I disagree with rather than a bug they missed. Everything else passed: CSV quoting, CRLF, header-only input, first-occurrence order, Unicode words, leap years, invalid dates, wrong argument counts.

The decision lists are good. Every session named the header question, the case question, the sign question, the format question, and picked a defensible answer. The tools sessions ran their scripts on inputs they wrote themselves, and those inputs were all happy paths plus one deliberately bad input. Nobody tried the empty object or the missing file.

**Gap or no gap.** A small gap, and not where I expected it. I thought the difference between the modes would show up once the spec stopped naming the edges. It did not: the model's picture of what a one-sentence spec implies is the same whether or not it can execute, and its tests exercise that picture rather than probe outside it. So running the code confirmed the design and could not have found the two hard failures, because the design did not include them. The two failures are both "the boring degenerate input": nothing in, file not there. Those are exactly the cases a code reviewer asks about first.

**What I would try next.** Same four tasks, prompt adds one line: "before you answer, write down the five inputs most likely to break this and run them". If the empty object and the missing file show up in that list, the gap is in what the model chooses to test, not in what it can write. If they do not, the gap is in its model of what breaks programs.
