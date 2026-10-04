"""The classification of Ramanujan P(n,k) for EVERY k, not one k at a time.

The paper's finiteness theorem bounds n for each fixed k:

    P(n,k) Ramanujan  ==>  n <= pi(2 + sqrt2) sqrt(k^2 + 1),

which is finite for each k but grows with k, so it leaves the classification
open as a statement about the family.  The corner form closes it.

THE ARGUMENT.  The corner criterion says the whole question is whether the grid
avoids four fixed corner regions, and the sufficient failure condition behind
the uniform bound is local to a corner: if

    s := (1 - cos 2 pi j/n) + (1 - cos 2 pi jk/n)  <  tau := 3 - 2 sqrt2

for even one nontrivial j, then P(n,k) is not Ramanujan.  Since
1 - cos(2 pi t) = 2 sin^2(pi t) <= 2 pi^2 ||t||^2, where ||.|| is the distance to
the nearest integer, failure is forced as soon as

    ||j/n||^2 + ||jk/n||^2  <  tau / (2 pi^2)  =  0.00869198...

That is a SIMULTANEOUS DIOPHANTINE condition, and Dirichlet's approximation
theorem supplies the j unconditionally.  Taking J = floor(sqrt n), there is some
1 <= j <= J with ||jk/n|| <= 1/(J+1); that j has ||j/n|| = j/n <= J/n, so

    ||j/n||^2 + ||jk/n||^2  <=  (J/n)^2 + 1/(J+1)^2  <  1/n + 1/n  =  2/n.

Hence 2/n < tau/(2 pi^2) forces failure, i.e.

    THEOREM.  If n >= 231 then P(n,k) is not Ramanujan, for EVERY k.

The bound is uniform in k -- it is the statement the per-k bound could not
make -- and it is what turns the classification into a finite problem in BOTH
variables.  Since P(n,k) needs 1 <= k < n/2, the entire family reduces to
3 <= n <= 230, and that region is then decided exhaustively and exactly.

The threshold 231 is loose: no Ramanujan P(n,k) has n > 112.  It does not need
to be sharp, only uniform, and sharpening it would not change the answer.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SQRT2 = math.sqrt(2.0)
TAU = 3 - 2 * SQRT2
AREA = TAU / (2 * math.pi ** 2)          # 0.00869198...
NMAX = 231                               # the certified uniform threshold


def dirichlet_threshold():
    """The least N with 2/N < tau/(2 pi^2): beyond it nothing is Ramanujan."""
    return math.ceil(2 / AREA)


def frac_norm(p, q):
    """||p/q||, the distance from p/q to the nearest integer."""
    r = (p % q) / q
    return min(r, 1 - r)


def dirichlet_witness(n, k):
    """The j whose existence Dirichlet guarantees, and the value it achieves."""
    J = math.isqrt(n)
    best = min(range(1, J + 1), key=lambda j: frac_norm(j * k, n))
    return best, frac_norm(best, n) ** 2 + frac_norm(best * k, n) ** 2


def check_dirichlet_bound(nlo=None, nhi=400):
    """For every n in [threshold, nhi] and every k, the witness forces failure.

    Returns (worst value attained, the (n,k) attaining it, number of failures).
    A failure would mean the theorem's own argument does not close, so this is
    the check that the proof -- not the classification -- is right.
    """
    nlo = nlo or dirichlet_threshold()
    worst, arg, bad = 0.0, None, 0
    for n in range(nlo, nhi):
        for k in range(1, n // 2):
            _j, s = dirichlet_witness(n, k)
            if s > worst:
                worst, arg = s, (n, k)
            if s >= AREA:
                bad += 1
    return worst, arg, bad


# ---------------------------------------------------------------------------
# the classification over the finite region the theorem leaves
# ---------------------------------------------------------------------------

def Q(x, y):
    return 4 * x * x + 4 * y * y - 8 * SQRT2 * abs(x * y) + 3


def is_ramanujan_corner(n, k, tol=1e-11):
    """The corner criterion, floating point.  Returns (verdict, worst margin)."""
    worst = float("inf")
    for j in range(1, n):
        al = 2 * math.cos(2 * math.pi * j / n)
        be = 2 * math.cos(2 * math.pi * j * k / n)
        if abs(al + 2) < 1e-9 and abs(be + 2) < 1e-9:
            continue                        # the trivial -3 of a bipartite cover
        x = math.cos(math.pi * j * (k + 1) / n)
        y = math.cos(math.pi * j * (k - 1) / n)
        q = Q(x, y)
        worst = min(worst, q)
        if q < -tol:
            return False, worst
    return True, worst


def census(nmax=NMAX - 1):
    """Every (n,k) with 3 <= n <= nmax and 1 <= k < n/2, decided in float."""
    hits, margins = [], []
    for n in range(3, nmax + 1):
        for k in range(1, (n + 1) // 2):
            if 2 * k >= n:
                continue
            ok, m = is_ramanujan_corner(n, k)
            if ok:
                hits.append((n, k))
            margins.append((abs(m), n, k))
    margins.sort()
    return hits, margins[:12]


def iso_class(n, k):
    """P(n,k) = P(n,l) iff l = +-k^(+-1) mod n (Watkins; Steimle-Staton)."""
    s = set()
    cands = [k, n - k]
    try:
        ki = pow(k, -1, n)
        cands += [ki, n - ki]
    except ValueError:
        pass
    for v in cands:
        v %= n
        if v > n // 2:
            v = n - v
        if 1 <= v < n / 2:
            s.add((n, v))
    return frozenset(s) if s else frozenset({(n, k)})


# ---------------------------------------------------------------------------
# exact certification
# ---------------------------------------------------------------------------

def certify(hits, nmax=NMAX - 1, verbose=True):
    """Re-decide every case in exact arithmetic and compare with the float run.

    Negative cases exit at their first bad j, so they are cheap; the positives
    carry the cost, and there are only 460 of them with n <= 112.
    """
    from verification import ramanujan_exact as RX
    hitset = set(hits)
    cases = disagree = 0
    bad = []
    for n in range(3, nmax + 1):
        for k in range(1, (n + 1) // 2):
            if 2 * k >= n:
                continue
            want = (n, k) in hitset
            got, _why = RX.is_ramanujan_exact(n, k)
            cases += 1
            if got != want:
                disagree += 1
                bad.append((n, k, want, got))
        if verbose and n % 10 == 0:
            print("    ... n=%d, %d cases certified, %d disagreements"
                  % (n, cases, disagree), flush=True)
    return cases, bad


def main(nmax=NMAX - 1, do_exact=True):
    thr = dirichlet_threshold()
    print("THE UNIFORM THRESHOLD")
    print("  tau = 3 - 2 sqrt2            = %.10f" % TAU)
    print("  tau / (2 pi^2)               = %.10f" % AREA)
    print("  least N with 2/N < that      = %d" % thr)
    worst, arg, bad = check_dirichlet_bound(nhi=2 * thr)
    print("  Dirichlet witness, n >= %d: worst value %.8f at %s (< %.8f)"
          % (thr, worst, arg, AREA))
    print("  cases where the witness fails to force failure: %d" % bad)
    assert bad == 0 and worst < AREA

    print()
    print("THE CLASSIFICATION, over the finite region 3 <= n <= %d" % nmax)
    hits, tight = census(nmax)
    ks = sorted({k for _n, k in hits})
    iso = {iso_class(n, k) for n, k in hits}
    print("  Ramanujan parameter pairs    = %d" % len(hits))
    print("  isomorphism classes          = %d" % len(iso))
    print("  largest n                    = %d" % max(n for n, _k in hits))
    print("  largest k                    = %d" % max(k for _n, k in hits))
    print("  k values occurring           = %s" % ks)
    print("  smallest |margin| seen       = %.3e at (n,k)=(%d,%d)"
          % (tight[0][0], tight[0][1], tight[0][2]))
    byk = {}
    for n, k in hits:
        byk.setdefault(k, []).append(n)
    print()
    for k in sorted(byk):
        print("  k=%-3d count=%-3d n = %s" % (k, len(byk[k]), byk[k]))

    if do_exact:
        print()
        print("EXACT CERTIFICATION of every case in the region")
        cases, bad = certify(hits, nmax)
        print("  %d cases decided in exact arithmetic, %d disagreements"
              % (cases, len(bad)))
        if bad:
            print("  DISAGREEMENTS: %s" % bad[:10])
        assert not bad
    return hits


if __name__ == "__main__":
    main(do_exact="--fast" not in sys.argv)
