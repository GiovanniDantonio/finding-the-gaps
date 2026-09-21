# Software: build a small CLI tool end to end

**Area:** software

**Hypothesis.** A file format with folding, escaping, parameters and nested components is the kind of thing that goes wrong at the edges. I wrote a spec for an iCalendar diff tool with the edges spelled out (recurrence overrides, TZID vs UTC vs all-day, exit codes, folding) and expected the version written without running any code to fail two or three of the twelve checks.

**Setup.** One task file, twelve acceptance cases frozen before the run, two sessions: one allowed to run code, one told to write the file in a single pass and not execute anything. I graded by running each output against the fixtures. After both passed, I wrote six more cases aimed at things the spec did not mention.

**What happened.** 12 of 12 for both, then 6 of 6 for both on the stress cases. The no-tools session said up front that it had not run the code and there might be bugs. There were none I could find. Both sessions built the same architecture: unfold lines, parse `name;params:value` with quoted parameters, keep a component stack so VALARM inside VEVENT is skipped, key events on `(UID, RECURRENCE-ID)`. Their code is structurally close enough that I suspect this is a well-trodden shape.

The one bug I hit during grading was mine: two stress fixtures were missing `END:VCALENDAR`, and both tools correctly rejected them with exit 2. I fixed the fixtures, not the tools.

**Gap or no gap.** No gap. A 300 line stdlib parser with a clear spec is inside what the model does without running anything. The result I actually care about is that a precise spec was enough: every rule I wrote down was honored, including the ones about output ordering and exit codes that people often get wrong.

**What I would try next.** Take the spec away. Give the RFC section and a sample file and ask for "a diff tool", then see whether the choices the model makes on its own (matching rule, time zone handling, exit codes) are sensible. The spec did a lot of work here and that is the part a real user often does not supply.
