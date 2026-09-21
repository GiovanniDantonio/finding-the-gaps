# Acceptance criteria: overlap

Written before the runs. Checked by me in a real browser, and one version is deployed.

1. Single `index.html`, no build step, opens from `file://` with no console errors.
2. No network requests after load (checked in the network panel).
3. Add and remove participants; working hours editable per participant.
4. Slots computed for 7 days in 30 minute steps, shown in the viewer's zone.
5. Each slot also shows each participant's local time.
6. Asia/Kolkata participant lines up at a :30 boundary, not rounded to the hour.
7. A participant in a zone where the working day crosses midnight in the viewer's zone still yields correct slots.
8. A DST transition inside the window shifts later slots by an hour, and the app does not produce a duplicated or missing hour.
9. Two participants with no overlap at all produce a clear empty state, not a blank page.
10. URL hash round trip: copy the URL, open in a new tab, same participants and hours.
11. Tab order reaches every control, and the slot list is readable at 390px wide.
12. Deployed and reachable at a public URL.

Score = checks passed out of 12. Interventions logged in `outputs/interventions.md`.
