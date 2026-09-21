# Software: build a one-page web app end to end

**Area:** software

**Hypothesis.** Time zones are where I expected the no-tools version to break: half-hour offsets, a working day that ends after it starts, slots that land on a different calendar date for one participant. The spec named every one of those cases and asked for a single offline `index.html`. I expected the version written blind to fail two or three of the twelve checks and the version that could open a browser to pass most of them.

**Setup.** Two sessions, same task file. The tools session could open the page and poke at it; the no-tools session had to write the file in one pass and hand it over. I then ran both files through the same checks in Chrome, with Playwright doing the clicking and me reading the screens.

**What happened.** Same score for both: 11 of 11 checks that I could run, and the one I could not run (a DST change inside the seven-day window) was untestable for either, since nothing changes clocks between 21 and 28 September. Slot counts matched to the number (63 for London with Kolkata, 112 for New York with a Tokyo night shift), both encode the state in the hash, both work at phone width and by keyboard. The no-tools file even added a weekend toggle and dashed lines to mark DST shifts, neither of which I asked for. The two files differ in layout and in how they encode the hash, but they lean on the same primitive: `Intl.DateTimeFormat` with a `timeZone`, iterated over half-hour instants.

**Gap or no gap.** No gap. Small self-contained web pages with a precise spec are solved, with or without a browser to test in. The interesting thing is that having tools bought nothing measurable here: the tools session verified its work and the other one said it had not, but the outputs are equally correct.

**What I would try next.** Two directions. One, drop the spec down to a sentence and see what the model decides about the hard cases on its own. Two, add a requirement that needs the browser to get right, such as matching a screenshot pixel for pixel or handling a real DST week, where "wrote it and never ran it" should finally cost something.
