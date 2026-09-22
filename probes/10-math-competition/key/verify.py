"""Brute-force check of every answer in key.json. Run: python key/verify.py (about a minute)."""
import itertools, json, math, pathlib
from functools import lru_cache

def p01():  # n <= 10^6 with d(n) = d(n+1)
    N = 10**6 + 1; d = [0] * (N + 1)
    for i in range(1, N + 1):
        for j in range(i, N + 1, i): d[j] += 1
    return sum(1 for n in range(1, N) if d[n] == d[n + 1])

def p02():  # 1..2026 that are a sum of two squares (0 allowed)
    s = {a*a + b*b for a in range(46) for b in range(46)}
    return sum(1 for n in range(1, 2027) if n in s)

def p03():  # permutations of 1..10 with exactly 3 fixed points and no 2-cycles
    c = 0
    for p in itertools.permutations(range(10)):
        if sum(p[i] == i for i in range(10)) != 3: continue
        if any(p[i] != i and p[p[i]] == i for i in range(10)): continue
        c += 1
    return c

def p04():  # R/U paths (0,0)->(10,10) that touch y=x at exactly 3 interior points
    c = 0
    for bits in itertools.combinations(range(20), 10):
        x = y = 0; s = set(bits); t = 0
        for i in range(20):
            if i in s: x += 1
            else: y += 1
            if x == y and 0 < x < 10: t += 1
        if t == 3: c += 1
    return c

def p05():  # 8-digit numbers, nondecreasing digits, digit sum 40
    return sum(1 for d in itertools.combinations_with_replacement(range(1, 10), 8) if sum(d) == 40)

def p06():  # subsets of 1..30 with sum 200
    dp = [0] * 466; dp[0] = 1
    for k in range(1, 31):
        for s in range(465, k - 1, -1): dp[s] += dp[s - k]
    return dp[200]

def p07():  # ordered integer pairs (x,y) with x^2 - y^2 = 2026^2
    M = 2026 ** 2; pairs = set()
    for d in range(1, int(math.isqrt(M)) + 1):
        if M % d == 0:
            a, b = d, M // d
            if (a + b) % 2 == 0:
                x, y = (a + b) // 2, (b - a) // 2
                for sx in (1, -1):
                    for sy in (1, -1): pairs.add((sx*x, sy*y))
    return len(pairs)

def p08():  # k <= 10000 such that no n! has exactly k trailing zeros
    def z(n):
        t = 0
        while n: n //= 5; t += n
        return t
    seen = set(); n = 0
    while True:
        seen.add(z(n))
        if z(n) > 10000: break
        n += 1
    return sum(1 for k in range(1, 10001) if k not in seen)

def p09():  # tilings of 3x12 by straight 1x3 trominoes (either orientation)
    R, C = 3, 12
    @lru_cache(None)
    def f(mask):  # mask over R*C cells, bit set = filled
        if mask == (1 << (R*C)) - 1: return 1
        i = next(k for k in range(R*C) if not mask >> k & 1); r, c = divmod(i, C); t = 0
        if c + 2 < C and all(not mask >> (i + k) & 1 for k in range(3)): t += f(mask | 7 << i)
        if r + 2 < R and all(not mask >> (i + k*C) & 1 for k in range(3)): t += f(mask | (1 << i) | (1 << i + C) | (1 << i + 2*C))
        return t
    return f(0)

def p10():  # n <= 10^6 with more 1s than 0s in binary
    return sum(1 for n in range(1, 10**6 + 1) if (b := bin(n)[2:]).count("1") > b.count("0"))

def p11():  # 4x4 0/1 matrices, all row and column sums 2, zero diagonal
    c = 0
    for m in range(1 << 16):
        rows = [(m >> 4*i) & 15 for i in range(4)]
        if any(bin(r).count("1") != 2 for r in rows): continue
        if any(rows[i] >> (3 - i) & 1 for i in range(4)): continue
        if all(sum(rows[i] >> j & 1 for i in range(4)) == 2 for j in range(4)): c += 1
    return c

def p12():  # non-congruent obtuse integer triangles with perimeter 2026
    P = 2026; c = 0
    for a in range(1, P):
        for b in range(a, P):
            cc = P - a - b
            if cc < b or a + b <= cc: continue
            if a*a + b*b < cc*cc: c += 1
    return c

if __name__ == "__main__":
    key = json.loads((pathlib.Path(__file__).parent / "key.json").read_text())
    for name, fn in sorted(globals().items()):
        if name.startswith("p") and name[1:].isdigit():
            v = fn(); ok = str(v) == key.get(name, {}).get("answer")
            print(name, v, "OK" if ok else f"MISMATCH (key {key.get(name, {}).get('answer')})")
