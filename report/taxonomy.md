# Taxonomy of gaps (running)

| Category | Seen in probes | Example | Notes |
|---|---|---|---|
| Claims to have checked something it did not check | 01 | p06 no-tools: lists y-x values with 1 and -1 three times each, says "each at most twice" | Final number right, certificate wrong. Only visible if you grade the construction. |
| Well known answers by recall | 01 | 24/24 integers correct | Textbook problems measure memory, not reasoning. Use unpublished variants. |
| Dropped factor in one case of a case split | 02 | p08 no-tools: ace pair case has no factor for the other ace's suit, total 5544 not 11880 | Human-looking error, carried cleanly to a wrong total with no hedge. Disappears with tools. |
| Recall dressed as reasoning | 01, 03 | 03 no-tools names "Brocard's problem", "Fermat pseudoprime" | Famous problems test memory. Probes need unpublished variants to say anything about reasoning. |
| Writes code rather than reason, when allowed | 02 | tools mode scripted all 12 counting problems | Not a gap, but it means the tools column measures the harness, not the model's math. |
| Invented or misapplied Mathlib API | 04 | `even_or_odd` does not exist; `hcop.mul_dvd` taken from an `Eq` | Catches a checker instantly, reads fine to a person. 3 of 24 at easy difficulty. |
| Unverifiable because the tool was missing | 04 | 10 of 12 tools sessions had no Lean installed and said so; 2 installed it and compiled | The harness, not the model, decided whether the task was checkable. Self-reports were accurate either way. |
