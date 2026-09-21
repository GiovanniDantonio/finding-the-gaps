"""Checks the counterexamples behind the FALSE items and spot-checks the TRUE ones. Run: python key/verify.py"""
import math
from sympy import isprime, gcd
assert not isprime(40*40+40+41), "p01: n=40"
assert not isprime(2**11-1), "p02: p=11, 2047=23*89"
assert not isprime(2**32+1), "p03: n=5, 641 divides"
assert pow(2,341,341)==2 and not isprime(341), "p04: 341=11*31"
assert gcd(2*2+1, 3*3+1)==5, "p05: n=2"
assert all(any(isprime(p) and isprime(n-p) for p in range(2,n//2+1)) for n in range(4,1001,2)), "p06"
assert all((n**7-n)%42==0 for n in range(1,5000)), "p07"
assert all(math.isqrt(s:=sum(k**3 for k in range(1,n+1)))**2==s for n in range(1,300)), "p08"
assert 4*3*2+1==25 and 5*4*3*2+1==121, "p09: n=4,5 (and 7)"
assert all(b%a==0 for a in range(1,300) for b in range(1,300) if (b*b)%(a*a)==0), "p10"
assert all((a*b*c)%60==0 for a in range(1,300) for b in range(a,300) for c in range(b,425) if a*a+b*b==c*c), "p11"
print("all checks pass")
