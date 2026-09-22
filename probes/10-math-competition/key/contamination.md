# Contamination check

Date: 2026-09-22. Method: one web search per problem using its mathematical content (not the
exact wording), top four results recorded, then a check of whether the specific answer for the
specific parameter appears on the result page. Raw search dumps are not committed.

| Problem | Method online? | Exact answer online? | Notes |
|---|---|---|---|
| p01 d(n)=d(n+1), n<=10^6 | Yes (OEIS A005237, Erdős papers) | Not found for 10^6 | The count to 10^7 (986262) is quoted in the literature; the no-tools runs recalled it several times while getting 10^6 wrong |
| p02 sums of two squares <= 2026 | Yes (OEIS A102548) | Not found for 2026 | The b-file covers small n only |
| p03 permutations, 3 fixed points, no 2-cycles | Generic | No | Combination of two constraints, not a standard sequence |
| p04 paths touching y=x exactly 3 times | Generic | No | No page found with this exact question |
| p05 8-digit nondecreasing, digit sum 40 | Generic | No | A278971 counts all 8-digit numbers by digit sum, a different question |
| p06 subsets of 1..30 with sum 200 | Generic (subset-sum DP) | No | Would need a computer or a table |
| p07 x^2-y^2 = 2026^2 | Method common (divisor pairs) | No | Parameter chosen for this probe |
| p08 k with no n! ending in k zeros | Method common (MSE 4442948) | No | The 10,000 bound is specific to this probe |
| p09 3x12 by straight trominoes | Yes | Yes | The count is a(12)=60 of a standard recurrence a(n)=a(n-1)+a(n-3), on OEIS |
| p10 more 1s than 0s, n<=10^6 | Yes (OEIS A072603 is the complement) | Not found for 10^6 | |
| p11 4x4 0-1 matrices, row/col sum 2, zero diagonal | Generic | No | |
| p12 obtuse integer triangles, perimeter 2026 | Yes (OEIS A070101) | Not found for 2026 | The b-file stops well before 2026 |

Verdict: the methods for all twelve are standard and easy to find, which is expected for
competition-style counting. Only p09 has its exact answer on the web as a term of a named
sequence; p01's neighbouring value for 10^7 is also published. The specific parameters for the
other ten were chosen for this probe and no page with those answers turned up. This is a light
check (one query each), not a proof of absence.
