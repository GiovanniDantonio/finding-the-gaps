# Human baseline

One person, probe 02 (twelve casework counting problems), timed, pen and paper only. This anchors
the no-tools numbers in the report: it says what a careful human with the same constraints does
on the same items. It is not filled in yet. Nothing in `report/` cites it until it is.

## Protocol

- Solver: the author (or one other named person; record who).
- Materials: pen, paper, a printout of the twelve statements below. No calculator, no computer,
  no phone, no reference books.
- Time: 90 minutes total, self-timed, one sitting. Write the time you finish each problem.
- Answer: one integer per problem. Blank counts as an abstention, not a wrong answer.
- Grading: afterwards, against `probes/02-math-casework/key/key.json`. Do not look at the key
  before you finish.
- Report: fill the table, then the two paragraphs. Commit as-is; do not fix answers after
  grading.

## Table

| Problem | Statement | Answer | Minutes at finish | Correct? |
|---|---|---|---|---|
| p01 | How many subsets of {1, 2, ..., 20} (including the empty set) contain no two consecutive integers and have a sum of elements divisible by 5? | | | |
| p02 | How many integers between 1 and 1,000,000 inclusive have digit sum exactly 20? | | | |
| p03 | How many permutations p of {1, 2, ..., 9} satisfy p(i) != i and p(i) != i + 1 for every i from 1 to 9? | | | |
| p04 | The vertices of a 7-cycle are colored with colors from a palette of 4 colors so that adjacent vertices get different colors. How many such colorings use exactly 3 of the 4 colors? Vertices are labeled, so rotations and reflections count as different colorings. | | | |
| p05 | How many quadruples of integers (a, b, c, d) satisfy 0 <= a <= b <= c <= d <= 12 and a + b + c + d = 30? | | | |
| p06 | How many lattice paths from (0, 0) to (8, 8) using unit steps right or up never touch the line y = x + 3 and never touch the line y = x - 3? | | | |
| p07 | How many positive integers n <= 2000 have the property that n, n + 1, and n + 2 are all squarefree? | | | |
| p08 | How many 5-card hands from a standard 52-card deck are exactly two pair (two cards of one rank, two of a second rank, one of a third rank) and contain the ace of spades? | | | |
| p09 | How many ordered triples of positive integers (x, y, z) satisfy x < y < z and xyz = 7200? | | | |
| p10 | How many binary strings of length 14 contain exactly six 1s and no three consecutive 1s? | | | |
| p11 | Four married couples sit in a row of 8 chairs. How many seatings have exactly two of the four couples sitting in adjacent chairs? People are distinguishable. | | | |
| p12 | How many subsets of {1, 2, ..., 15} have elements summing to exactly 60? | | | |

Score: __ / 12 answered, __ correct, __ blank. Total time: __ minutes.

## What was hard

(Two or three sentences. Which problems needed the most casework? Where did you make an
arithmetic slip, if any? Did you check anything twice?)

## Comparison to the no-tools runs

(Fill after grading. The no-tools Devin runs on this probe are in
`probes/02-math-casework/results.md`. Note which items both got wrong, which only one side got
wrong, and whether the human error looks like the model's.)
