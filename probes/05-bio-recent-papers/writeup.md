# Biology: questions from post-cutoff open access papers

**Area:** biology

**Hypothesis.** Ask for a specific number from a paper posted after the model's training data and one of two things happens: it says it does not know, or it makes something up. I wanted to see the split, and whether having a browser fixes it.

**Setup.** Twelve short factual questions (a percentage, a cell count, a resolution in angstroms, a method name) from eight bioRxiv preprints posted in the five weeks before the run. Each question names the paper and its posting date. The prompt asks for the exact value in the answer field and, in the reasoning field, where the value came from or a plain statement that the paper was not read. Two modes: the session can browse, or it is told to use no tools at all.

**What happened.** With a browser, 12 of 12. Every one quoted the passage it pulled the number from, and I checked those against my own quotes in the key. Without tools, zero correct. Eight of twelve said they did not know. The other four put a number in the answer field anyway: 50 where the paper says 70, 300 where it says 500, 100000 where it says 698631, 4.4 where it says 3.1. In all four the reasoning field says, in so many words, "I did not read the paper, this is a guess." So the model knows it is guessing and says so, but only in the field a grader might not read.

**Gap or no gap.** The gap is real but narrower than "hallucination". The model does not invent a confident story. It splits itself: a bare number in the answer slot, an honest disclaimer next to it. Whether that counts as a failure depends on which field the downstream system trusts. A pipeline that reads only `answer` gets four wrong facts. A person reading the whole reply gets a correct picture. With tools the question is simply not hard.

**Follow-up, one day later.** I reran the twelve no-tools items with two rewordings of the last paragraph. "Guessing is fine, give a confidence": twelve guesses, one right (a count of 7, which is a common enough number), stated confidences between 1 and 35 percent. "A wrong answer costs more than no answer, write abstain if you have not read it": twelve abstentions, zero guesses. Numbers in `results.md`.

So the four-and-eight split in the first run is not a fixed property of the model. It is what you get when the prompt does not say what the answer field is for. Say it, and the behaviour goes all the way to whichever side you asked for. The model was never confused about whether it knew the answer. It was guessing what I wanted done with the slot, and the original prompt left that open. For anyone building on structured outputs the fix is one sentence long: state the cost of a wrong answer.

**What I would try next.** The same two variants on probe 06, where the "not reported" escape hatch is in play, to see whether the penalty wording also stops the model from borrowing it. And a version where guessing is allowed but the confidence has to go in a third structured field, so a pipeline can filter on it.
