# Answer key

Twelve pairs. `pNN` is a counting question that needs a real computation (a sieve, a DP table, a long
sum). `qNN` is the same question with a parameter changed so the answer is short by hand (a
complement trick, a tiny case, a closed form). `verify.py` recomputes every answer by brute force
or exhaustive DP; run it before trusting `key.json`. `make_problems.py` regenerates `problems/`.

Why pairs: probe 10 suggested that no-tools misses come from computations the model describes but
does not do. If that is right, no-tools should miss the `p` half and get the `q` half, with tools
getting both. The last line of each reasoning field (EXACT / RECALLED / ESTIMATED) is the model's own
label for what it did; the grader records it next to correctness so the two can be compared.
