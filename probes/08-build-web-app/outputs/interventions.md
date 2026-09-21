# Interventions

Both sessions produced the file in one shot with zero follow-up messages from me.

Verification was done by me after the fact with Playwright driving Chrome against the two `index.html` files (script not part of the artifact). Nothing in either file was edited.

| Check | tools | notools |
|---|---|---|
| 1 loads with no console errors | pass | pass |
| 2 zero network requests | pass | pass |
| 3 add/remove participants, editable hours | pass | pass |
| 4 London 09-17 with Kolkata 09-18, viewer London: 09:00 to 13:30 shown, 63 slots over 7 days | pass | pass |
| 5 each slot shown in every participant's local time | pass | pass |
| 6 half-hour offset (Kolkata 13:30, GMT+5:30) | pass | pass |
| 7 shift across midnight (Tokyo 22:00 to 06:00 vs New York 09-17): 16 slots a day, 112 total | pass | pass |
| 8 DST transition inside the window | untested | untested |
| 9 empty state when nothing overlaps (Sydney 09-12 added) | pass | pass |
| 10 URL hash round trip in a fresh tab | pass | pass |
| 11 Tab reaches every control | pass | pass |
| 12 375px wide, no horizontal scroll | pass | pass |

Check 8 could not be run: the app fixes the window to the next 7 days from now (2026-09-21) and no zone I tried changes clocks in that window. To test it I would have to change the system clock. Noted as a limit of the acceptance list, not a failure.
