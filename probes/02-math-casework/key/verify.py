"""Brute-force check of every answer in key.json. Run: python key/verify.py"""
import itertools, json, math, pathlib, collections
from functools import lru_cache

def p01():  # subsets of 1..20, no two consecutive, sum divisible by 5
    c = 0
    for m in range(1 << 20):
        if m & (m >> 1): continue
        if sum(i + 1 for i in range(20) if m >> i & 1) % 5 == 0: c += 1
    return c

def p02():  # integers 1..10^6 with digit sum 20
    return sum(1 for n in range(1, 10**6 + 1) if sum(map(int, str(n))) == 20)

def p03():  # permutations of 1..9 with no p(i)=i and no p(i)=i+1
    c = 0
    for p in itertools.permutations(range(1, 10)):
        if all(p[i-1] != i and p[i-1] != i + 1 for i in range(1, 10)): c += 1
    return c

def p04():  # proper 4-colorings of C7 using exactly 3 colors
    c = 0
    for col in itertools.product(range(4), repeat=7):
        if all(col[i] != col[(i+1) % 7] for i in range(7)) and len(set(col)) == 3: c += 1
    return c

def p05():  # 0<=a<=b<=c<=d<=12, a+b+c+d=30
    return sum(1 for a in range(13) for b in range(a, 13) for c in range(b, 13) for d in range(c, 13) if a+b+c+d == 30)

def p06():  # R/U paths (0,0)->(8,8) never touching y=x+3 or y=x-3
    @lru_cache(None)
    def f(x, y):
        if abs(y - x) >= 3: return 0
        if (x, y) == (8, 8): return 1
        return (f(x+1, y) if x < 8 else 0) + (f(x, y+1) if y < 8 else 0)
    return f(0, 0)

def p07():  # n<=2000 with n,n+1,n+2 all squarefree
    def sf(n): return all(n % (p*p) for p in range(2, int(n**0.5) + 1))
    return sum(1 for n in range(1, 2001) if sf(n) and sf(n+1) and sf(n+2))

def p08():  # 5-card hands: exactly two pairs, containing the ace of spades
    deck = [(r, s) for r in range(13) for s in range(4)]
    c = 0
    for h in itertools.combinations(deck, 5):
        if (12, 0) not in h: continue
        cnt = sorted(collections.Counter(r for r, s in h).values())
        if cnt == [1, 2, 2]: c += 1
    return c

def p09():  # x<y<z positive, xyz=7200
    N = 7200; c = 0
    for x in range(1, N + 1):
        if N % x: continue
        for y in range(x + 1, N // x + 1):
            if (N // x) % y == 0 and N // x // y > y: c += 1
    return c

def p10():  # binary strings length 14, exactly 6 ones, no run of ones longer than 2
    c = 0
    for pos in itertools.combinations(range(14), 6):
        s = ['0'] * 14
        for i in pos: s[i] = '1'
        if '111' not in ''.join(s): c += 1
    return c

def p11():  # 4 couples in a row of 8, exactly two couples adjacent
    c = 0
    for p in itertools.permutations(range(8)):
        together = sum(1 for k in range(4) if abs(p.index(2*k) - p.index(2*k+1)) == 1)
        if together == 2: c += 1
    return c

def p12():  # subsets of 1..15 with sum 60
    return sum(1 for m in range(1 << 15) if sum(i + 1 for i in range(15) if m >> i & 1) == 60)

if __name__ == "__main__":
    key = json.loads((pathlib.Path(__file__).parent / "key.json").read_text())
    for name, fn in sorted(globals().items()):
        if name.startswith("p") and name[1:].isdigit():
            got = str(fn()); exp = key[name]["answer"]
            print(name, "OK" if got == exp else f"MISMATCH got {got} expected {exp}")
