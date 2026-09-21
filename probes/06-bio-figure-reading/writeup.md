# Biology: reading numbers off figures and legends

**Area:** biology

**Hypothesis.** Probe 05 showed a browser makes recent-paper questions easy. This probe adds the harder half: questions where the number is only in a figure legend or a methods paragraph, and four trap questions where the number does not exist in the paper at all. I expected the tools mode to read a nearby number and report it for at least one trap.

**Setup.** Three September 2026 bioRxiv preprints (a single-cell isoform atlas, a mouse uterus remodeling time course, a single-nucleus Alzheimer's atlas). Eight questions with an answer, four without. Same two modes as before. A first attempt used shorthand paper references and confused the tools sessions, so nine of them were re-run with the full title and date in the prompt; that is the version graded here.

**What happened.** Tools: 12 of 12, including all four traps. The reasoning for the traps is what I was hoping to see fail: "the paper reports Spearman and Pearson, not Kendall", "the time course goes to PPD90 with no PPD60 point", "the cohort is described as sporadic AD, no Down syndrome subgroup". Each one names what the paper does report before saying what it does not. No-tools: zero correct, nine abstentions, and three answers of "not reported" on questions whose values are in the paper.

Those three are the interesting failure. "Not reported" is a factual claim about the paper. The model had not read the paper and said so in the reasoning, yet in the answer field it used the same phrase the trap questions were fishing for. I think it borrowed the phrasing from the prompt's own instructions, which mention "not reported" as an allowed answer. It is a cousin of the probe 05 behavior: a disclaimer in one field, a confident-looking token in the other.

**Gap or no gap.** No gap in reading. A model with the paper open reads legends, methods and tables correctly and knows when a value is missing, at least at twelve questions. The gap is in what happens without the paper, and it is the same gap as probe 05: the answer field gets filled with something that looks like an answer.

**What I would try next.** Real figure reading, where the number is only in the plot and not in any text. That needs image input and a different harness. And a bigger trap set, since 4 of 4 is not enough to say the tools mode never fabricates.
