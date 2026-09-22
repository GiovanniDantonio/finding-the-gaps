# Week 8: Probe 09, software from one sentence

To: Christopher Thorpe

Probes 07 and 08 found nothing, and I suspected the spec was doing the work. So probe 09 cuts the spec to one sentence: dedupe a CSV, top ten words in a file, flatten JSON to dotted keys, days between two dates. Acceptance scripts written before the run, split into hard checks and judgment calls.

Both modes came out identical: 22 of 24 hard, 10 of 11 judgment, same two failures (missing file gives a traceback, empty object flattens to `{"": {}}`). The part I want to talk about: the tools sessions ran their code and still missed those, because they only tested inputs they had thought of. Running code confirmed the design. It did not find the edge.

Writeup in probes/09-build-vague-spec.
