"""Recompute every answer in key.json by brute force or exhaustive DP.
Run: python key/verify.py (under a minute). pNN is the heavy half of a pair, qNN the light half."""
import itertools, json, math, pathlib
from functools import lru_cache

def divisor_counts(N):
    d = [0] * (N + 1)
    for i in range(1, N + 1):
        for j in range(i, N + 1, i): d[j] += 1
    return d

def p01():  # n <= 200000 with exactly 12 divisors
    d = divisor_counts(200000)
    return sum(1 for n in range(1, 200001) if d[n] == 12)

def q01():  # n <= 200000 with an odd number of divisors
    d = divisor_counts(200000)
    return sum(1 for n in range(1, 200001) if d[n] % 2 == 1)

def subset_sum_counts(n):
    tot = n * (n + 1) // 2
    dp = [0] * (tot + 1); dp[0] = 1
    for k in range(1, n + 1):
        for s in range(tot, k - 1, -1): dp[s] += dp[s - k]
    return dp

def p02():  # subsets of 1..25 with sum 100
    return subset_sum_counts(25)[100]

def q02():  # subsets of 1..25 with sum 320
    return subset_sum_counts(25)[320]

def delannoy(m, n):
    D = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0: D[i][j] = 1
            else: D[i][j] = D[i-1][j] + D[i][j-1] + D[i-1][j-1]
    return D[m][n]

def p03():  # paths (0,0)->(12,12) with steps E, N, NE
    return delannoy(12, 12)

def q03():  # paths (0,0)->(12,1) with steps E, N, NE
    return delannoy(12, 1)

def distinct_partitions(n, min_part):
    parts = list(range(min_part, n + 1))
    dp = [0] * (n + 1); dp[0] = 1
    for k in parts:
        for s in range(n, k - 1, -1): dp[s] += dp[s - k]
    return dp[n]

def p04():  # partitions of 60 into distinct parts
    return distinct_partitions(60, 1)

def q04():  # partitions of 60 into distinct parts, each part at least 20
    return distinct_partitions(60, 20)

def cycles(p):
    seen = [False] * len(p); c = 0
    for i in range(len(p)):
        if not seen[i]:
            c += 1; j = i
            while not seen[j]: seen[j] = True; j = p[j]
    return c

def stirling1(n, k):
    S = [[0] * (k + 1) for _ in range(n + 1)]; S[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            S[i][j] = S[i-1][j-1] + (i - 1) * S[i-1][j]
    return S[n][k]

def p05():  # permutations of 1..10 with exactly 2 cycles (brute force, about 15 s)
    v = sum(1 for p in itertools.permutations(range(10)) if cycles(p) == 2)
    assert v == stirling1(10, 2)
    return v

def q05():  # permutations of 1..10 with exactly 9 cycles
    v = sum(1 for p in itertools.permutations(range(10)) if cycles(p) == 9)
    assert v == stirling1(10, 9)
    return v

def p06():  # digit sum of 2^200
    return sum(map(int, str(2 ** 200)))

def q06():  # number of decimal digits of 2^200
    return len(str(2 ** 200))

def domino_tilings(rows, cols):
    """Fill cells in column-major order; each empty cell takes a vertical or a horizontal domino."""
    @lru_cache(None)
    def rec(pos, occ):
        if pos == rows * cols: return 1
        r, c = pos % rows, pos // rows
        if occ >> pos & 1: return rec(pos + 1, occ)
        t = 0
        if r + 1 < rows and not occ >> (pos + 1) & 1: t += rec(pos + 1, occ | 1 << pos | 1 << (pos + 1))
        if c + 1 < cols: t += rec(pos + 1, occ | 1 << pos | 1 << (pos + rows))
        return t
    return rec(0, 0)

def p07():  # domino tilings of a 4 x 12 board
    return domino_tilings(4, 12)

def q07():  # domino tilings of a 2 x 12 board
    return domino_tilings(2, 12)

def coin_ways(total, coins):
    dp = [0] * (total + 1); dp[0] = 1
    for c in coins:
        for s in range(c, total + 1): dp[s] += dp[s - c]
    return dp[total]

def p08():  # ways to make 500 cents from 1, 5, 10, 25, 50
    return coin_ways(500, [1, 5, 10, 25, 50])

def q08():  # ways to make 500 cents from 25 and 50 only
    return coin_ways(500, [25, 50])

def sieve(N):
    s = bytearray([1]) * (N + 1); s[0] = s[1] = 0
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return s

def p09():  # primes p <= 100000 with p + 2 also prime
    s = sieve(100002)
    return sum(1 for p in range(2, 100001) if s[p] and s[p + 2])

def q09():  # primes p <= 100 with p + 2 also prime
    s = sieve(102)
    return sum(1 for p in range(2, 101) if s[p] and s[p + 2])

def no_run_of_four(n):
    return sum(1 for bits in itertools.product("01", repeat=n) if "0000" not in "".join(bits) and "1111" not in "".join(bits)) if n <= 16 else _tribo(n)

def _tribo(n):
    # strings of length n with no run of 4 equal symbols = 2 * (compositions of n into parts 1..3)
    t = [1, 1, 2, 4]
    while len(t) <= n: t.append(t[-1] + t[-2] + t[-3])
    return 2 * t[n]

def p10():  # binary strings of length 24 with no four consecutive equal bits
    assert _tribo(12) == no_run_of_four(12)
    return _tribo(24)

def q10():  # binary strings of length 6 with no four consecutive equal bits
    return no_run_of_four(6)

def p11():  # subsets of 1..40 with sum divisible by 40
    dp = [0] * 40; dp[0] = 1
    for k in range(1, 41):
        new = dp[:]
        for r in range(40): new[(r + k) % 40] += dp[r]
        dp = new
    return dp[0]

def q11():  # subsets of 1..40 with sum divisible by 820
    return subset_sum_counts(40)[0] + subset_sum_counts(40)[820]

def p12():  # lattice points with x^2 + y^2 <= 1000^2
    R = 1000; t = 0
    for x in range(-R, R + 1):
        y = math.isqrt(R * R - x * x); t += 2 * y + 1
    return t

def q12():  # lattice points with x^2 + y^2 = 1000^2
    R = 1000; t = 0
    for x in range(-R, R + 1):
        y2 = R * R - x * x; y = math.isqrt(y2)
        if y * y == y2: t += 1 if y == 0 else 2
    return t

if __name__ == "__main__":
    key = json.loads((pathlib.Path(__file__).parent / "key.json").read_text())
    ok = True
    for name in sorted(key):
        got = str(globals()[name]())
        flag = "ok" if got == key[name] else "MISMATCH"
        if flag != "ok": ok = False
        print(f"{name}: key={key[name]} computed={got} {flag}")
    print("all ok" if ok else "MISMATCH")
