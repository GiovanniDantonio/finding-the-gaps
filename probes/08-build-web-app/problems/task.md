# Task: overlap

Build a single page web app that finds meeting times that work for people in different cities.

Input: a list of participants, each with a city and working hours in their own local time. Output: for the next 7 days, every 30 minute slot where all participants are inside their working hours, shown in the viewer's own time zone and in each participant's local time.

Requirements:

- One file, `index.html`. No build step, no backend, no network requests, no npm packages. Vanilla JS and CSS inline.
- Time zones come from the browser's own IANA database. Do not hardcode offsets.
- Participants can be added and removed. Default working hours 09:00 to 17:00, editable per participant.
- Handle a participant whose working day, seen from the viewer's zone, crosses midnight.
- Handle time zones with a non hour offset, for example Asia/Kolkata at +05:30.
- Handle a daylight saving transition inside the 7 day window, so the same slot can shift by an hour partway through the week.
- The state is encoded in the URL hash so the page can be shared and reopened with the same participants.
- Works offline once loaded. Keyboard accessible. Readable on a phone.

Put the complete contents of `index.html` in the answer field, with no prose and no code fences. Put a short account of what you did in the reasoning field, including whether you opened it in a browser, and anything you know is broken.
