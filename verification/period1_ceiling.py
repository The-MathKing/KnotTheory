"""The period-one ceiling: an exact upper bound on what one rotation can do.

A2/A4 context. Two places in the paper say "we have not found the matrix":
M(P(10,2)) was recorded as numerical, and M(P(24,4)) is the single value of
(n,k) at k<=4 where Z is known but no nullity certificate exists. In both the
honest statement was a failed search. This module replaces it with a reason.

THE BOUND. A period-one (rotation-invariant) symmetric matrix on the P(n,k)
pattern is five numbers: outer weight a, inner weight b, spoke c -- all
required nonzero -- and the two free diagonals d_out, d_in. Its Fourier block
at the n-th root of unity w^j is

        M_j = [[ d_out + a*x_j ,      c        ],
               [      c        , d_in + b*y_j  ]],

        x_j = 2 cos(2 pi j / n),     y_j = 2 cos(2 pi j k / n).

null M_j = 2 would force every entry to vanish, hence c = 0, so each block
contributes 0 or 1 and null A = #{j : det M_j = 0}.

Now suppose det M_j = det M_{j'} = 0 with y_j = y_{j'}. Since c != 0 neither
factor of (d_out + a x_j)(d_in + b y_j) = c^2 can vanish, so

        d_out + a x_j = c^2 / (d_in + b y_j) = d_out + a x_{j'},

and a != 0 gives x_j = x_{j'}, i.e. j' = +-j mod n. So:

        THE SINGULAR BLOCKS MUST HAVE PAIRWISE DISTINCT y VALUES,
        after identifying j with -j.

Hence, writing the +-classes of Z_n grouped by their common value of y,

        null A  <=  sum over distinct y-values of (largest class size in it),

each class having size 2, or 1 when 2j = 0 mod n. That sum is computable in
closed form for every (n,k), and it is an upper bound on every period-one
matrix at once -- not a search.

WHAT IT GIVES. At (10,2) the bound is 5, so no period-one matrix reaches 6:
this is the general form of what p10_2_exact.py established for that one case
by exhausting subsets symbolically, and it is why that search stalled at 5. At
(24,4) the bound is 8 against 2k+2 = 10, so the missing certificate at n=24 is
not a search failure -- no rotation-invariant matrix can attain the ceiling
there at all, and a higher restart budget would never have found one.

The bound is an upper bound only. Attaining it also needs the |J| determinant
equations to be solvable in the five parameters, which the bound does not
check, so a value BELOW the bound may still be unattainable.

CONTROL. The suite's authority here is the control, not the formula: wherever
the paper has a period-one certificate of nullity 2k+2, this bound must be at
least 2k+2. If it ever comes out smaller the argument above is wrong and the
run fails. We also cross-check (10,2) against the independent exhaustive
symbolic result in p10_2_exact.py.

Run: python3 verification/period1_ceiling.py
"""

import os
import sys
from collections import defaultdict
from fractions import Fraction

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def pm_classes(n):
    """The +-classes of Z_n, as (representative, size)."""
    out, seen = [], set()
    for j in range(n):
        if j in seen:
            continue
        cls = {j, (-j) % n}
        seen |= cls
        out.append((j, len(cls)))
    return out


def y_exact(j, k, n):
    """2 cos(2 pi j k / n), exactly, as an algebraic number."""
    return sp.nsimplify(2 * sp.cos(2 * sp.pi * sp.Rational(j * k, n)))


def period1_ceiling(n, k):
    """Exact upper bound on null A over all period-one A on the P(n,k) pattern."""
    groups = defaultdict(list)
    for j, size in pm_classes(n):
        # group by the exact value of y_j; sp.simplify gives a canonical key
        key = sp.simplify(y_exact(j, k, n))
        groups[key].append((j, size))
    total = 0
    detail = []
    for key, members in groups.items():
        best = max(s for _, s in members)
        total += best
        detail.append((key, [j for j, _ in members], best))
    return total, detail


def main():
    print("The period-one ceiling on P(n,k)")
    print("=" * 70)

    # ---- the two cases the paper leaves as failed searches -------------
    print("\n[1] The two open/numerical cases.")
    for n, k, Z in ((10, 2, 6), (24, 4, 10)):
        b, _ = period1_ceiling(n, k)
        verdict = ("period-one CANNOT reach it" if b < 2 * k + 2
                   else "period-one has room")
        print(f"    P({n},{k}): ceiling 2k+2 = {2*k+2}, Z = {Z}, "
              f"period-one bound = {b}   -> {verdict}")

    # cross-check against the independent exhaustive result
    b10, _ = period1_ceiling(10, 2)
    assert b10 == 5, f"(10,2) bound is {b10}, expected 5"
    print("    (10,2) bound 5 agrees with the exhaustive symbolic result in"
          " p10_2_exact.py")

    # ---- the control: never contradict an existing certificate ---------
    print("\n[2] CONTROL. Wherever the paper certifies nullity 2k+2 with a")
    print("    period-one matrix, the bound must be >= 2k+2.")
    # n divisible by lcm of the paper's period-one divisor classes, at small k
    CERTIFIED = [(17, 3), (20, 3), (24, 3), (29, 4), (25, 4), (26, 4),
                 (27, 4), (28, 4), (12, 2), (14, 2), (16, 2), (9, 2),
                 (11, 2), (13, 3), (18, 3), (19, 3)]
    bad = []
    print(f"    {'(n,k)':>9} {'2k+2':>5} {'bound':>6}  ok?")
    for n, k in CERTIFIED:
        b, _ = period1_ceiling(n, k)
        ok = b >= 2 * k + 2
        if not ok:
            bad.append((n, k, b))
        print(f"    {f'({n},{k})':>9} {2*k+2:>5} {b:>6}  {'yes' if ok else 'NO'}")
    if bad:
        print(f"\n    CONTROL FAILED on {bad}: the bound contradicts a")
        print("    certificate that exists, so the argument is wrong.")
        return 1
    print("    control passed: no contradiction with any existing certificate.")

    # ---- the shape of the obstruction ---------------------------------
    print("\n[3] Where period-one has room, for small k.")
    print(f"    {'k':>2} {'2k+2':>5}   n with bound < 2k+2 (period-one impossible)")
    for k in range(2, 6):
        blocked = [n for n in range(2 * k + 3, 61)
                   if period1_ceiling(n, k)[0] < 2 * k + 2]
        s = ", ".join(map(str, blocked[:18])) + ("..." if len(blocked) > 18 else "")
        print(f"    {k:>2} {2*k+2:>5}   {s if blocked else '(none)'}")

    print("\n" + "=" * 70)
    print("The bound depends only on how often y_j = 2cos(2 pi j k / n)")
    print("repeats on the +-classes of Z_n -- i.e. on gcd(k,n) and the")
    print("arithmetic of n, not on any search.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
