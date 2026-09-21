# Acceptance criteria: icsdiff

Written before the runs. The CHANGED header line uses the old values, as in the example in task.md. Each check is a pair of .ics files and an expected stdout plus exit code. The tool must be a single file using only the standard library.

1. Identical files. Empty stdout, exit 0.
2. One event added, one removed. Both sections present, correct order, exit 1.
3. One event whose start moved by an hour. CHANGED with one `start:` line only.
4. One event with two changed fields (summary and location). Two indented lines, in field order start, end, summary, location.
5. Two added events out of order in the file. Printed sorted by start time.
6. A recurring event with one overridden occurrence changed. Only the overridden occurrence appears, matched on (UID, RECURRENCE-ID); the series itself is not reported as changed.
7. An event with `TZID=America/New_York`. Printed in New York wall clock, not shifted to UTC.
8. An event with a UTC stamp (`20261001T130000Z`). Printed as 13:00 UTC.
9. An all day event (`DTSTART;VALUE=DATE=20261001`). Date printed, no time.
10. A file with a truncated VEVENT. Exit 2, message on stderr, nothing on stdout.
11. Same event, same UID, but reordered properties and different line folding. Reported as unchanged.
12. Folded long SUMMARY line (RFC 5545 folding, continuation starting with a space). Unfolded before comparison.

Score = checks passed out of 12. An intervention is any time I have to tell the session something it should have got from the task file; interventions are logged in `outputs/interventions.md`.
