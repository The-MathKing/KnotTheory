"""Exact certification of the Ramanujan classification of P(n,k).

The float64 criterion G_k(t) <= 7 is not good enough to publish: the decision
turns on comparing algebraic numbers, and near a band edge the comparison is
exactly where floating point stops meaning anything.  This module removes the
floating point from the DECISION and leaves it only in a guarded estimate whose
error is bounded a priori.

Clearing the square root.  With alpha = 2 cos t, beta = 2 cos kt, A = alpha+beta
and Prod = alpha*beta, the criterion of ramanujan.py is 2 sqrt2 |A| - Prod <= 7,
i.e. 2 sqrt2 |A| <= 7 + Prod.  Both sides may be squared once the right side is
known nonnegative, so the criterion is EXACTLY the pair of conditions

        7 + Prod >= 0        and        8 A^2 <= (7 + Prod)^2 ,

with no radical anywhere.  Define

        D := (7 + Prod)^2 - 8 A^2 .

Ramanujan-ness of P(n,k) is then: at every nontrivial grid index j,
7 + Prod >= 0 and D >= 0.

Staying in the ring.  On the grid, with c_m := 2 cos(2 pi j m / n),
        A = c_1 + c_k,        Prod = c_{k+1} + c_{k-1},
because 4 cos a cos b = 2 cos(a+b) + 2 cos(a-b).  So A and Prod -- hence D --
are values at z = zeta_n^j of LAURENT POLYNOMIALS WITH INTEGER COEFFICIENTS:

        a(z)    = z + z^-1 + z^k + z^-k
        prod(z) = z^{k+1} + z^-{k+1} + z^{k-1} + z^-{k-1}
        d(z)    = (7 + prod(z))^2 - 8 a(z)^2

Since zeta_n^j is a primitive m-th root of unity for m = n/gcd(n,j), each value
d(zeta_n^j) is an algebraic integer of Z[zeta_m], and we reduce it to an exact
integer coordinate vector modulo the cyclotomic polynomial Phi_m.  That vector
is zero if and only if the value is exactly zero -- an EXACT test, pure integer
arithmetic, which is what decides the band-edge cases.

Sign, with a guard.  A nonzero algebraic integer cannot be arbitrarily small:
the product of its conjugates is a nonzero rational integer, so |d| >= 1 /
prod|conjugates| >= 1 / BOUND^(deg-1), with BOUND a crude a priori bound on
|d|.  We therefore evaluate at a precision set from that separation bound and
REFUSE to report a sign unless the computed value exceeds the guard -- so a
wrong sign is not merely unlikely, it is excluded.
"""

from math import gcd
import sympy
from sympy import Poly, Symbol, ZZ

x = Symbol("x")

# |c_m| <= 2, so |a| <= 4 and |prod| <= 4, giving |d| <= (7+4)^2 + 8*16 = 249.
VALUE_BOUND = 249


def _laurent_d(k):
    """d(z) as {exponent: integer coefficient}, exponents possibly negative."""
    def add(dst, src, scale=1):
        for e, c in src.items():
            dst[e] = dst.get(e, 0) + scale * c
        return dst

    def mul(u, v):
        out = {}
        for e1, c1 in u.items():
            for e2, c2 in v.items():
                out[e1 + e2] = out.get(e1 + e2, 0) + c1 * c2
        return out

    # NB: accumulate, never a dict literal.  At k=1 the exponents collide
    # (k == 1 and k-1 == -(k-1) == 0), and a literal would silently drop the
    # duplicate keys -- which is exactly the bug the float64 control caught.
    a, pr = {}, {}
    for e in (1, -1, k, -k):
        a[e] = a.get(e, 0) + 1
    for e in (k + 1, -(k + 1), k - 1, -(k - 1)):
        pr[e] = pr.get(e, 0) + 1
    seven_plus = add(dict(pr), {0: 7})
    d = mul(seven_plus, seven_plus)
    add(d, mul(a, a), -8)
    return {e: c for e, c in d.items() if c != 0}


def _laurent_prod_plus7(k):
    pr = {}
    for e in (k + 1, -(k + 1), k - 1, -(k - 1)):
        pr[e] = pr.get(e, 0) + 1
    pr[0] = pr.get(0, 0) + 7
    return {e: c for e, c in pr.items() if c != 0}


_PHI_CACHE = {}


def _phi(m):
    if m not in _PHI_CACHE:
        _PHI_CACHE[m] = Poly(sympy.cyclotomic_poly(m, x), x, domain=ZZ)
    return _PHI_CACHE[m]


def exact_vector(laurent, n, j):
    """The value of `laurent` at zeta_n^j, as an exact integer vector mod Phi_m.

    Returns (m, coeffs) where m = n/gcd(n,j) and coeffs are the coordinates in
    the power basis 1, zeta_m, ..., zeta_m^(deg Phi_m - 1).
    """
    g = gcd(n, j) if j else n
    m = n // g
    jp = (j // g) % m if m > 1 else 0
    if m == 1:                                   # zeta = 1
        return 1, [sum(laurent.values())]
    acc = {}
    for e, c in laurent.items():
        ee = (e * jp) % m
        acc[ee] = acc.get(ee, 0) + c
    deg = max(acc) if acc else 0
    poly = Poly([acc.get(i, 0) for i in range(deg, -1, -1)], x, domain=ZZ) \
        if acc else Poly(0, x, domain=ZZ)
    rem = poly.rem(_phi(m))
    coeffs = rem.all_coeffs()[::-1]
    coeffs += [0] * (_phi(m).degree() - len(coeffs))
    return m, [int(c) for c in coeffs]


def _value_and_guard(m, coeffs, prec_digits):
    """Numeric value of sum coeffs[i] zeta_m^i, and the guard it must clear.

    The value, the imaginary part and the guard all stay in mpmath.  They used
    to be handed back as float64, which silently broke the certification for
    every case with deg Phi_m >= 126: the guard 10^-(dps-15) is then below the
    smallest subnormal double, so float(guard) == 0.0, and the test
    `imag < guard` compares a non-negative number against zero and can never
    pass.  The symptom was a RuntimeError claiming the sign could not be
    separated on values of size 11 -- a guard bug wearing a precision bug's
    clothes.  Nothing outside the guard was wrong, and no published number
    moved: at k <= 10 the bound gives n <= 108, so deg Phi_m <= 108 and the
    underflow was never reached.  It appears as soon as n passes 126.
    """
    import mpmath
    with mpmath.workdps(prec_digits):
        z = mpmath.exp(2 * mpmath.pi * 1j / m)
        v = sum(c * z ** i for i, c in enumerate(coeffs))
        guard = mpmath.mpf(10) ** (-(prec_digits - 15))
        # The value is real by construction; the imaginary part is error only.
        return mpmath.re(v), abs(mpmath.im(v)), guard


def sign_exact(m, coeffs):
    """(sign, how) for sum coeffs[i] zeta_m^i.  sign in {-1,0,+1}.

    'how' records which test decided it: "exact-zero" (integer vector vanishes)
    or "separated@<digits>" (value exceeded the separation guard).
    """
    if all(c == 0 for c in coeffs):
        return 0, "exact-zero"
    deg = len(coeffs)
    # |value| >= 1 / BOUND^(deg-1); ask for comfortably more digits than that.
    import math as _m
    need = int((deg - 1) * _m.log10(VALUE_BOUND)) + 40
    for dps in (need, 2 * need, 4 * need):
        v, imag, guard = _value_and_guard(m, coeffs, dps)
        if abs(v) > guard and imag < guard:
            return (1 if v > 0 else -1), "separated@%d" % dps
    raise RuntimeError("could not separate sign; vector=%s" % coeffs)


def is_ramanujan_exact(n, k, trace=False):
    """Exact decision, with the reason recorded."""
    from verification.ramanujan import is_bipartite
    d = _laurent_d(k)
    p7 = _laurent_prod_plus7(k)
    for j in range(n):
        if j == 0:
            continue                                   # the trivial +3
        if is_bipartite(n, k) and 2 * j == n:
            continue                                   # the trivial -3
        m, cv = exact_vector(p7, n, j)
        s, how = sign_exact(m, cv)
        if s < 0:
            return False, ("j=%d: 7+prod < 0 (%s)" % (j, how))
        m, cv = exact_vector(d, n, j)
        s, how = sign_exact(m, cv)
        if s < 0:
            return False, ("j=%d: D < 0 (%s)" % (j, how))
        if trace and s == 0:
            print("      j=%d: D vanishes exactly -- |lambda| = 2 sqrt 2 on the nose" % j)
    return True, "all nontrivial j certified"


# ===========================================================================
# THE CRITERION AS ONE INTEGER POLYNOMIAL, AND A RIGOROUS FINITENESS BOUND
#
# Put u = cos t, so that cos kt = T_k(u) (the Chebyshev polynomial).  Then
#       A    = 2u + 2 T_k(u),        Prod = 4 u T_k(u),
#       D_k(u) = (7 + 4 u T_k(u))^2 - 32 (u + T_k(u))^2,
# an element of Z[u] of degree 2k.  The criterion becomes purely polynomial:
#
#       P(n,k) is Ramanujan  <=>  for every nontrivial j,
#           7 + 4 u T_k(u) >= 0   and   D_k(u) >= 0   at u = cos(2 pi j/n).
#
# FINITENESS.  D_k(1) = (7+4)^2 - 32*4 = -7 < 0, so u = 1 lies in the bad set,
# and by continuity so does an interval below it.  Let u_k be the LARGEST root
# of D_k in (-1,1) -- isolated below by Sturm sequences over the rationals, so
# the location is exact, not estimated.  Every t in (0, arccos(u_k)) then has
# D_k(cos t) < 0.  The grid's smallest nonzero angle is 2 pi/n, so
#
#       P(n,k) Ramanujan  =>  2 pi / n >= arccos(u_k)  =>  n <= 2 pi/arccos(u_k)
#
# which is the finiteness bound.  Only finitely many n per k, and the surviving
# range is then certified exhaustively by is_ramanujan_exact.
# ===========================================================================

u = Symbol("u")


def D_poly(k):
    """D_k(u) = (7 + 4u T_k)^2 - 8(2u + 2T_k)^2  in Z[u], of degree 2k."""
    Tk = Poly(sympy.chebyshevt(k, u), u, domain=ZZ)
    U = Poly(u, u, domain=ZZ)
    A = 2 * U + 2 * Tk
    prod = 4 * U * Tk
    return (prod + 7) ** 2 - 8 * A ** 2


def prod_plus_7_is_positive(k, samples=200001):
    """The side condition 7 + 4u T_k(u) >= 0 is never binding.

    For u in [-1,1] both |u| <= 1 and |T_k(u)| <= 1, so |4u T_k(u)| <= 4 and
    7 + 4u T_k(u) >= 3 > 0.  Hence the criterion is the single inequality
    D_k >= 0.  Checked numerically here as a guard on that reasoning.
    """
    import numpy as np
    uu = np.linspace(-1.0, 1.0, samples)
    return float(np.min(7.0 + 4.0 * uu * np.cos(k * np.arccos(np.clip(uu, -1, 1)))))


def largest_root_below_one(k, digits=40):
    """Exact rational bracket (lo, hi) around the largest root of D_k in (-1,1).

    sympy's real_roots are exact algebraic numbers; we narrow one to a rational
    interval and then VERIFY the bracket by an exact integer sign change, so a
    bad refinement cannot pass silently.
    """
    p = D_poly(k)
    inside = [r for r in p.real_roots()
              if r.is_real and sympy.Lt(r, 1) == sympy.true
              and sympy.Gt(r, -1) == sympy.true]
    if not inside:
        return None
    top = max(inside)
    scale = 10 ** digits
    approx = sympy.Rational(sympy.floor(top.evalf(digits + 10) * scale), scale)
    lo, hi = approx, approx + sympy.Rational(1, scale)
    for _ in range(60):
        if p.eval(lo) * p.eval(hi) <= 0:
            return lo, hi
        lo -= sympy.Rational(1, scale)
        hi += sympy.Rational(1, scale)
    raise RuntimeError("bracket failed for k=%d" % k)


def finiteness_bound(k):
    """The largest n permitted by the bad band at u = 1.

    D_k(1) = 11^2 - 8*16 = -7 < 0, so u=1 is inside the bad set; let u_k be the
    largest root of D_k below 1, so D_k < 0 on (u_k, 1).  Any Ramanujan n needs
    its smallest nonzero grid angle 2 pi/n to clear arccos(u_k), giving
    n <= 2 pi / arccos(u_k).  arccos is evaluated on the UPPER end of the exact
    bracket, which makes the angle smallest and the returned integer a genuine
    upper bound rather than a rounded estimate.
    """
    import mpmath
    br = largest_root_below_one(k)
    if br is None:
        return None
    lo, hi = br
    with mpmath.workdps(80):
        ang = mpmath.acos(mpmath.mpf(int(hi.p)) / int(hi.q))
        return int(mpmath.floor(2 * mpmath.pi / ang))


# ---------------------------------------------------------------------------
# THE PARITY LAW, as a second certified bound.
#
# D_k(-1) = (7 - 4 T_k(-1))^2 - 8(2 T_k(-1) - 2)^2 with T_k(-1) = (-1)^k, so
#       k even:  D_k(-1) = 9 > 0        k odd:  D_k(-1) = -7 < 0.
# For odd k, then, u = -1 (that is t = pi) also lies in the bad set.  The grid
# {2 pi j/n} contains t = pi exactly when n is EVEN, and there the sample is the
# trivial eigenvalue -3, which is exempt.  When n is ODD the nearest grid point
# sits at distance pi/n from pi, at u = -cos(pi/n), and it is not exempt.  With
# v_k the SMALLEST root of D_k in (-1,1), D_k < 0 on [-1, v_k), so a Ramanujan
# odd n needs -cos(pi/n) >= v_k, i.e.
#
#       n <= pi / arccos(-v_k)          (k odd, n odd).
#
# Existence of both roots is free: D_k(0) = 49 - 32 T_k(0)^2 and T_k(0) is 0 or
# +-1, so D_k(0) >= 17 > 0 for every k, giving a sign change on each side.
# ---------------------------------------------------------------------------


def smallest_root_above_minus_one(k, digits=40):
    """Exact rational bracket around the smallest root of D_k in (-1,1)."""
    p = D_poly(k)
    inside = [r for r in p.real_roots()
              if r.is_real and sympy.Lt(r, 1) == sympy.true
              and sympy.Gt(r, -1) == sympy.true]
    if not inside:
        return None
    bot = min(inside)
    scale = 10 ** digits
    approx = sympy.Rational(sympy.floor(bot.evalf(digits + 10) * scale), scale)
    lo, hi = approx, approx + sympy.Rational(1, scale)
    for _ in range(60):
        if p.eval(lo) * p.eval(hi) <= 0:
            return lo, hi
        lo -= sympy.Rational(1, scale)
        hi += sympy.Rational(1, scale)
    raise RuntimeError("bracket failed for k=%d" % k)


def odd_n_bound(k):
    """For odd k: the largest ODD n the band at u = -1 permits.  None if k even."""
    import mpmath
    if k % 2 == 0:
        return None
    br = smallest_root_above_minus_one(k)
    lo, hi = br
    with mpmath.workdps(80):
        # arccos(-v) grows with -v, so the SMALLEST arccos comes from the
        # smallest -v, i.e. from the LARGEST v: use the upper bracket end.
        ang = mpmath.acos(-mpmath.mpf(int(hi.p)) / int(hi.q))
        return int(mpmath.floor(mpmath.pi / ang))


# ===========================================================================
# A BOUND THAT HOLDS FOR EVERY k, NOT ONE k AT A TIME.
#
# finiteness_bound(k) is computed per k, from the roots of D_k.  That leaves
# the classification a table rather than a theorem: nothing is said about k
# beyond those computed.  The following closes that, with an elementary proof.
#
# Write x = cos t, y = cos kt, a = 1-x, b = 1-y, s = a+b.  On the region where
# x+y >= 0 the criterion function is
#
#   G = 4 sqrt2 (x+y) - 4xy = (8 sqrt2 - 4) - (4 sqrt2 - 4) s - 4ab .
#
# By AM-GM, 4ab <= s^2, so G > 7 is implied by  s^2 + (4 sqrt2 - 4) s < 8 sqrt2 - 11.
# The left side increases in s >= 0 and equals the right side EXACTLY at
# s = 3 - 2 sqrt2 = (sqrt2 - 1)^2 =: tau.  So
#
#       s < tau   =>   G > 7   =>   the sample is forbidden.
#
# Finally 1 - cos(theta) <= theta^2/2 for every real theta, so
# s <= (1 + k^2) t^2 / 2, and s < tau holds as soon as
#
#       t  <  sqrt(2 tau) / sqrt(k^2+1)  =  (2 - sqrt2)/sqrt(k^2+1).
#
# The grid's smallest nonzero angle is 2 pi/n, which gives the bound below.
# The same computation at t = pi (where x, y -> -1 for odd k, so x+y <= 0 and
# |x+y| = 2 - a' - b' with a' = 1+x, b' = 1+y -- the identical expression)
# gives the parity bound, with pi/n in place of 2 pi/n: exactly half.
#
# NOTE ON PROVENANCE.  An earlier draft stated this same constant from a Taylor
# expansion of lambda_+ in t at fixed k.  That derivation is INVALID: the
# critical t scales like 1/k, so kt is of order one and the expansion was used
# outside its domain.  The constant survived only because the bound is loose.
# The argument above uses no expansion in kt at all -- only monotonicity, AM-GM
# and 1 - cos theta <= theta^2/2 -- and is valid for every k.
# ===========================================================================

import math as _math

TAU = 3.0 - 2.0 * _math.sqrt(2.0)                  # (sqrt2 - 1)^2
C_UNIFORM = _math.pi * (2.0 + _math.sqrt(2.0))     # 2 pi / (2 - sqrt2)


def uniform_bound(k, n_odd=False):
    """n <= C sqrt(k^2+1), halved for the parity band (odd k, odd n)."""
    b = C_UNIFORM * _math.sqrt(k * k + 1.0)
    return b / 2.0 if (n_odd and k % 2 == 1) else b


def check_uniform_lemma(kmax=200, samples=4000):
    """The lemma the uniform bound rests on, checked against G itself.

    Returns (min G on the 0-band, min G on the pi-band over odd k).  Both must
    exceed 7 -- that is exactly the statement that the interval the proof
    claims is forbidden really is forbidden.
    """
    import numpy as np
    from verification.ramanujan import G as _G
    lo0 = lopi = float("inf")
    for k in range(1, kmax + 1):
        lim = (2.0 - _math.sqrt(2.0)) / _math.sqrt(k * k + 1.0)
        t = np.linspace(1e-12, lim * (1 - 1e-12), samples)
        lo0 = min(lo0, float(_G(t, k).min()))
        if k % 2 == 1:
            lopi = min(lopi, float(_G(np.pi - t, k).min()))
    return lo0, lopi


# ===========================================================================
# THE CORNER THEOREM: k leaves the region and enters the map.
#
# D_k = (7+Prod)^2 - 8A^2 is a difference of squares, so it FACTORS over
# Q(sqrt 2) into two polynomials of degree k+1:
#
#       D_k = P_-  *  P_+ ,      P_mp = 7 + 4u T_k(u) -+ 4 sqrt2 (u + T_k(u)).
#
# Their sum is 2(7 + Prod) >= 6 > 0, so they are never both negative; hence
#
#       D_k >= 0   <=>   P_- >= 0  AND  P_+ >= 0.
#
# Now set  x = cos((k+1)t/2),  y = cos((k-1)t/2).  Using
# cos t cos kt = (cos(k+1)t + cos(k-1)t)/2 and cos t + cos kt = 2 cos a cos b,
# both factors collapse to the SAME quadratic form:
#
#       P_mp = 3 + 4( x^2 + y^2 -+ 2 sqrt2 x y ),
#
# so the criterion of Theorem (Criterion) is exactly
#
#       Q(x,y) := 4x^2 + 4y^2 - 8 sqrt2 |x y| + 3   >=   0 .
#
# Q does not mention k.  Since
#   Q = 4(|x| - (sqrt2+1)|y|)(|x| - (sqrt2-1)|y|) + 3,
# the forbidden set {Q < 0} is four congruent lenses, one at each corner
# (+-1, +-1) of the square, together about 0.45% of its area -- ONE FIXED
# REGION, THE SAME FOR EVERY k.
#
# The whole Riemann Hypothesis for P(n,k) is therefore the statement that the
# n-1 points
#       ( cos(pi j (k+1)/n) ,  cos(pi j (k-1)/n) ),    j = 1..n-1
# avoid those four corners.  The k-dependence has moved out of the geometry and
# into the map -- which turns the classification into a simultaneous Diophantine
# question about j(k+1)/n and j(k-1)/n approaching integers together, and is the
# route to a statement valid for ALL k rather than the certified k <= 10.
# ===========================================================================


def Q_corner(x, y):
    """The k-free criterion form.  Ramanujan iff Q >= 0 at every image point."""
    import numpy as np
    return 4 * x * x + 4 * y * y - 8 * np.sqrt(2.0) * np.abs(x * y) + 3.0


def ramanujan_by_corner(n, k):
    """Decide via the corner criterion.  Equivalent to is_ramanujan; kept as an
    independent route so the two can be cross-checked against each other."""
    import numpy as np
    from verification.ramanujan import is_bipartite
    for j in range(1, n):
        if is_bipartite(n, k) and 2 * j == n:
            continue
        x = np.cos(np.pi * j * (k + 1) / n)
        y = np.cos(np.pi * j * (k - 1) / n)
        if Q_corner(x, y) < -1e-12:
            return False
    return True


def check_corner_identity(kmax=11, trials=300, seed=0):
    """The two factorizations, checked numerically against their definitions."""
    import numpy as np
    rng = np.random.default_rng(seed)
    worst = 0.0
    for k in range(1, kmax + 1):
        for _ in range(trials):
            t = rng.uniform(0, np.pi)
            u, Tk = np.cos(t), np.cos(k * t)
            A, Prod = 2 * u + 2 * Tk, 4 * u * Tk
            x = np.cos((k + 1) * t / 2)
            y = np.cos((k - 1) * t / 2)
            for sgn in (-1.0, 1.0):
                lhs = 7 + Prod + sgn * 2 * np.sqrt(2.0) * A
                rhs = 3 + 4 * (x * x + y * y + sgn * 2 * np.sqrt(2.0) * x * y)
                worst = max(worst, abs(lhs - rhs))
    return worst
