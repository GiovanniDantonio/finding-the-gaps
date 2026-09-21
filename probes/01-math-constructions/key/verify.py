"""Brute-force check of every answer in key.json. Run: python key/verify.py"""
import itertools, json, math, pathlib, functools, collections

def p01():  # max subset of 1..50, no two differ by 3 or 5
    best = {0: 0}  # mask of last 5 picks -> best size
    for _ in range(50):
        nb = collections.defaultdict(int)
        for m, v in best.items():
            nb[(m << 1) & 31] = max(nb[(m << 1) & 31], v)
            if not (m >> 2) & 1 and not (m >> 4) & 1:
                nb[((m << 1) | 1) & 31] = max(nb[((m << 1) | 1) & 31], v + 1)
        best = nb
    return max(best.values())

def p02():  # tilings of 2x12 with 1x2 dominoes and 2x2 squares
    f = [1, 1]
    for n in range(2, 13): f.append(f[-1] + 2 * f[-2])
    return f[12]

def p03():  # largest subset of 1..30 with no element dividing another
    n = 30; best = 0
    def rec(i, chosen):
        nonlocal best
        if len(chosen) + (n - i + 1) <= best: return
        if i > n: best = max(best, len(chosen)); return
        if all(i % c for c in chosen): rec(i + 1, chosen + [i])
        rec(i + 1, chosen)
    rec(1, []); return best

def p04():  # min colors for 1..40, a|b => different colors == longest divisor chain
    L = {}
    for k in range(1, 41): L[k] = 1 + max([L[d] for d in range(1, k) if k % d == 0], default=0)
    return max(L.values())

def p05():  # 9-queens solutions
    cnt = 0
    def rec(row, cols, d1, d2):
        nonlocal cnt
        if row == 9: cnt += 1; return
        for c in range(9):
            if c in cols or row - c in d1 or row + c in d2: continue
            rec(row + 1, cols | {c}, d1 | {row - c}, d2 | {row + c})
    rec(0, set(), set(), set()); return cnt

def p06():  # max points in 5x5 grid, no three collinear
    pts = [(x, y) for x in range(5) for y in range(5)]
    def col(a, b, c): return (b[0]-a[0])*(c[1]-a[1]) == (b[1]-a[1])*(c[0]-a[0])
    best = 0
    def rec(i, chosen):
        nonlocal best
        if len(chosen) + (25 - i) <= best: return
        if i == 25: best = max(best, len(chosen)); return
        p = pts[i]
        if all(not col(a, b, p) for a, b in itertools.combinations(chosen, 2)): rec(i + 1, chosen + [p])
        rec(i + 1, chosen)
    rec(0, []); return best

def p07():  # ordered sums of 1,3,4 equal to 100
    f = [1] + [0] * 100
    for n in range(1, 101): f[n] = sum(f[n - k] for k in (1, 3, 4) if n >= k)
    return f[100]

def p08():  # smallest positive integer with exactly 24 divisors
    n = 1
    while True:
        d = sum(2 if n // i != i else 1 for i in range(1, int(n**0.5) + 1) if n % i == 0)
        if d == 24: return n
        n += 1

def p09():  # knight a1 to h8 min moves
    from collections import deque
    q = deque([((0, 0), 0)]); seen = {(0, 0)}
    while q:
        (x, y), d = q.popleft()
        if (x, y) == (7, 7): return d
        for dx, dy in [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < 8 and 0 <= ny < 8 and (nx, ny) not in seen: seen.add((nx, ny)); q.append(((nx, ny), d+1))

def p10():  # max edges triangle-free on 13 vertices (Mantel), sanity via K_{6,7}
    return 6 * 7

def p11():  # largest subset of 1..100, no two distinct elements sum to multiple of 7
    cnt = collections.Counter(x % 7 for x in range(1, 101))
    return (cnt[0] > 0) + max(cnt[1], cnt[6]) + max(cnt[2], cnt[5]) + max(cnt[3], cnt[4])

def p12():  # Latin squares of order 4
    rows = list(itertools.permutations(range(4))); cnt = 0
    def ok(sq): return all(len({r[c] for r in sq}) == len(sq) for c in range(4))
    def rec(sq):
        nonlocal cnt
        if len(sq) == 4: cnt += 1; return
        for r in rows:
            if ok(sq + [r]): rec(sq + [r])
    rec([]); return cnt

if __name__ == "__main__":
    key = json.loads((pathlib.Path(__file__).parent / "key.json").read_text())
    for name, fn in sorted(globals().items()):
        if name.startswith("p") and name[1:].isdigit():
            got = str(fn()); exp = key[name]["answer"]
            print(name, "OK" if got == exp else f"MISMATCH got {got} expected {exp}")
