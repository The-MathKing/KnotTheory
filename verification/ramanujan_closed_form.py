"""Towards a closed form: the classification is a condition on divisors.

The classification of `ramanujan_all_k` is a certified list, not a formula.
This module is the structure underneath it, which is what a formula would have
to be built from.  Four statements, in order of strength.

LOCALITY.  The grid points of `level m` -- those j with n/gcd(n,j) = m -- are
exactly the full conjugate set {cos(2 pi j/m) : gcd(j,m)=1}.  Since the
criterion is a condition on each grid point separately, and every grid point of
P(n,k) has some level m dividing n,

    P(n,k) is Ramanujan  <=>  no divisor m >= 3 of n is BAD for k,

where m is bad for k when some primitive level-m point violates Q >= 0.  The
levels m = 1 and m = 2 never obstruct: m = 1 is the trivial +3, and at m = 2 we
have D_k(-1) = 9 > 0 for even k while for odd k the cover is bipartite and the
point carries the exempt trivial -3.

Badness at level m depends on k only through k mod m, because the point
(cos(pi j(k+1)/m), cos(pi j(k-1)/m)) does.

DIVISOR CLOSURE.  Immediately: if d | n then the level set of d is contained in
that of n, so P(n,k) Ramanujan and d | n with d > 2k forces P(d,k) Ramanujan.
The Ramanujan set of each k is closed downwards under division.  So the whole
classification is determined by the MINIMAL bad divisors, and since nothing
above B_k survives anyway, by the finitely many minimal bad m <= B_k.

THE MINIMUM IS A GCD.  For m not dividing c,

    min { ||j c / m|| : gcd(j,m) = 1 }  =  gcd(c,m) / m,

with ||.|| the distance to the nearest integer.  (If m | c the minimum is 0.)

GCD SAFETY.  Corollary `cor:lens` says Q < 0 forces BOTH |x| and |y| to be at
least sqrt2 - 1/2, the point where the forbidden region meets the side of the
square.  Since |cos(pi t)| >= sqrt2 - 1/2 exactly when ||t|| <= gamma, where

    gamma = arccos(sqrt2 - 1/2) / pi = 0.1328095...,

a level m is SAFE as soon as one of the two coordinates cannot get close
enough.  By the gcd formula that is a divisibility statement, and because
1/gamma = 7.5295... while m/gcd(k+1,m) is an integer, it is a statement about
small integers:

    THEOREM.  If m/gcd(k+1,m) or m/gcd(k-1,m) lies in {2,...,7},
              then m is safe for k.

The excluded value 1 is not an oversight: m/gcd = 1 means m | k+1, the
coordinate is pinned at |x| = 1, and the level is as unsafe as it can be.

WHAT IS STILL MISSING.  The safety theorem is sufficient, not necessary, and it
is the safe side it describes; there is no matching criterion for badness.  A
closed form needs both.  For k <= 9 the two bounds already in the paper happen
to suffice, and `closed_form_small_k` states exactly that -- verified, but
verified case by case rather than derived, and it fails at k = 6, 8 and at every
odd k >= 11, where interior bands appear.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SQRT2 = math.sqrt(2.0)
#: the half-width, in units of pi, of the angular window a coordinate must hit
GAMMA = math.acos(SQRT2 - 0.5) / math.pi
#: 1/GAMMA = 7.5295..., so the integer form of the safety test is "<= 7"
SAFE_MAX = int(1.0 / GAMMA)


def Q(x, y):
    return 4 * x * x + 4 * y * y - 8 * SQRT2 * abs(x * y) + 3


# ---------------------------------------------------------------------------
# locality
# ---------------------------------------------------------------------------

def bad_level(m, k, tol=1e-11):
    """Does some PRIMITIVE level-m grid point violate the criterion?

    Depends on k only through k mod m.
    """
    for j in range(1, m):
        if math.gcd(j, m) != 1:
            continue
        x = math.cos(math.pi * j * (k + 1) / m)
        y = math.cos(math.pi * j * (k - 1) / m)
        if Q(x, y) < -tol:
            return True
    return False


def is_ramanujan_local(n, k):
    """The divisor form of the criterion: no bad divisor m >= 3 of n."""
    return not any(bad_level(m, k) for m in range(3, n + 1) if n % m == 0)


def minimal_bad_divisors(k, bound):
    """The minimal bad m <= bound, under divisibility.  These generate the answer."""
    bad = {m for m in range(3, bound + 1) if bad_level(m, k)}
    return [m for m in sorted(bad)
            if not any(m % d == 0 and d < m and d in bad for d in range(3, m))]


# ---------------------------------------------------------------------------
# the gcd formula, and the safety theorem it gives
# ---------------------------------------------------------------------------

def min_unit_norm(c, m):
    """min over j coprime to m of ||jc/m||, which equals gcd(c,m)/m."""
    if c % m == 0:
        return 0.0
    return math.gcd(c, m) / m


def gcd_safe(m, k):
    """The safety test, in its integer form."""
    if k >= 1:
        bp = m // math.gcd(k + 1, m)
        if 2 <= bp <= SAFE_MAX:
            return True
    if k - 1 != 0:
        bm = m // math.gcd(k - 1, m)
        if 2 <= bm <= SAFE_MAX:
            return True
    return False


# ---------------------------------------------------------------------------
# the closed form where one exists
# ---------------------------------------------------------------------------

def max_odd_divisor(n):
    while n % 2 == 0:
        n //= 2
    return n


def closed_form_small_k(n, k, B, P):
    """The closed form for k <= 9, given the paper's two bounds B_k and P_k.

    k = 2, 4 : every n in (2k, B_k].
    k odd    : every n in (2k, B_k] all of whose odd divisors are at most P_k.

    For even k the second clause is vacuous (P_k is not defined; there is no
    band at u = -1), which is exactly why k = 2 and k = 4 are solid runs.
    """
    if n <= 2 * k or n > B:
        return False
    if k % 2 == 0:
        return True
    return max_odd_divisor(n) <= P


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def check_locality(kmax=45, nmax=230):
    """The divisor form against the direct criterion."""
    from verification.ramanujan_all_k import is_ramanujan_corner
    bad, total = [], 0
    for k in range(1, kmax + 1):
        for n in range(2 * k + 1, nmax + 1):
            total += 1
            if is_ramanujan_corner(n, k)[0] != is_ramanujan_local(n, k):
                bad.append((n, k))
    return total, bad


def check_divisor_closure(kmax=45, nmax=230):
    """P(n,k) Ramanujan and d | n, d > 2k  ==>  P(d,k) Ramanujan."""
    from verification.ramanujan_all_k import is_ramanujan_corner
    bad, total = [], 0
    for k in range(1, kmax + 1):
        for n in range(2 * k + 1, nmax + 1):
            if not is_ramanujan_corner(n, k)[0]:
                continue
            for d in range(2 * k + 1, n):
                if n % d:
                    continue
                total += 1
                if not is_ramanujan_corner(d, k)[0]:
                    bad.append((n, k, d))
    return total, bad


def check_gcd_formula(mmax=120, cmax=200):
    """min over units of ||jc/m|| equals gcd(c,m)/m."""
    bad = []
    for m in range(3, mmax):
        units = [j for j in range(1, m + 1) if math.gcd(j, m) == 1]
        for c in range(0, cmax):
            got = min(min((j * c) % m, m - (j * c) % m) / m for j in units)
            if abs(got - min_unit_norm(c, m)) > 1e-12:
                bad.append((c, m))
    return bad


def check_gcd_safety(kmax=60, mmax=200):
    """The safety theorem: it must never call a bad level safe."""
    fired, total, bad = 0, 0, []
    for k in range(1, kmax + 1):
        for m in range(3, mmax):
            total += 1
            if gcd_safe(m, k):
                fired += 1
                if bad_level(m, k):
                    bad.append((m, k))
    return total, fired, bad


def check_closed_form_small_k(nmax=300):
    """Where the closed form is claimed, it must be exact; and it must fail
    where we say it fails, so the scope of the claim is checked too."""
    from verification.ramanujan_all_k import is_ramanujan_corner
    from verification.ramanujan_exact import finiteness_bound, odd_n_bound
    holds, fails = [], []
    for k in list(range(1, 14)):
        B = finiteness_bound(k)
        P = odd_n_bound(k) if k % 2 else 0
        bad = [n for n in range(2 * k + 1, nmax)
               if closed_form_small_k(n, k, B, P) != is_ramanujan_corner(n, k)[0]]
        (holds if not bad else fails).append(k)
    return holds, fails


if __name__ == "__main__":
    print("gamma = arccos(sqrt2 - 1/2)/pi = %.10f, 1/gamma = %.4f (so '<= %d')"
          % (GAMMA, 1 / GAMMA, SAFE_MAX))
    t, b = check_locality()
    print("locality:          %d cases, %d disagreements" % (t, len(b)))
    t, b = check_divisor_closure()
    print("divisor closure:   %d (n,d) pairs, %d violations" % (t, len(b)))
    b = check_gcd_formula()
    print("gcd formula:       %d counterexamples" % len(b))
    t, f, b = check_gcd_safety()
    print("gcd safety:        fired on %d of %d, %d counterexamples" % (f, t, len(b)))
    holds, fails = check_closed_form_small_k()
    print("closed form holds for k = %s" % holds)
    print("             fails for k = %s  (interior bands)" % fails)
