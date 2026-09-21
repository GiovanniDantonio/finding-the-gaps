# Task: icsdiff

Write a command line tool that diffs two iCalendar files and prints what changed.

Usage: `python icsdiff.py OLD.ics NEW.ics`

Output, in this exact shape, sorted by start time within each section, sections in this order, and sections with no entries omitted:

```
ADDED
  2026-10-01 09:00 Standup
REMOVED
  2026-10-02 14:00 Budget review
CHANGED
  2026-10-03 10:00 Retro
    start: 2026-10-03 10:00 -> 2026-10-03 11:00
    summary: Retro -> Retrospective
```

Rules:

- Events are matched by UID. Same UID in both files means the event may be CHANGED; UID only in NEW is ADDED; UID only in OLD is REMOVED.
- An event with a RECURRENCE-ID is a single overridden occurrence and is matched by the pair (UID, RECURRENCE-ID), not by UID alone.
- Compare these fields only: start, end, summary, location. Report one indented line per changed field, in that field order.
- All times are printed in the calendar's local wall clock as given in the file. Times with a TZID are printed in that time zone. UTC times (trailing Z) are printed in UTC. All-day events (VALUE=DATE) print the date only, with no time.
- Exit 0 when there are no differences and print nothing. Exit 1 when there are differences. Exit 2 on a file that cannot be parsed, with the error on stderr.
- Standard library only. One file. Python 3.11.

Put the complete contents of `icsdiff.py` in the answer field, with no prose and no code fences. Put a short account of what you did in the reasoning field, including whether you ran it, on what inputs, and anything you know is unfinished.
