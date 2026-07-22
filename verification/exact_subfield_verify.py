"""
Exact verification of a period-d certificate whose weights lie in a subfield.

If the weights lie in the fixed field K = Q(zeta_m)^H of a subgroup H, they are
rational combinations of the Gauss periods

    eta_a = sum over h in H of zeta_m^{h a},

which form a basis of K over Q.  So an exact certificate can be produced in two
steps, only the second of which needs to be rigorous:

  RECOGNISE (heuristic): fit the numerical weights against the eta basis and
  round the coefficients to rationals.  Any method is allowed here -- a wrong
  guess simply fails the next step.

  VERIFY (exact): rebuild the blocks M_l with those exact field elements and
  check det M_l = 0 exactly in Q(zeta_m), i.e. as a polynomial identity modulo
  the cyclotomic polynomial Phi_m.  No floating point.

That det M_l = 0 for the k+1 chosen l (each hit by two Fourier indices) gives
2k+2 singular blocks, and the ceiling forces the nullity to be exactly 2k+2.
The nullity is therefore a DISCRETE consequence of an exactly verified
equation, never a thresholded numerical rank.
"""
import sys
from fractions import Fraction
from math import gcd

import numpy as np

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from exact_certifier import Cyclo


def field_basis(K, m, H):
    """A genuine Q-basis of the fixed field of H inside Q(zeta_m).

    The Gauss periods eta_a = sum_{h in H} zeta^{h a} span the fixed field but
    need not be independent -- for m = 24 and H = {1,5} they satisfy
    eta_1 + eta_7 = 0, because the sum over all units is the Ramanujan sum,
    which vanishes.  So take {1} together with the periods and reduce to an
    independent set of the right size."""
    units = [j for j in range(1, m) if gcd(j, m) == 1]
    Hs = set()
    for h in H:
        Hs.add(h % m); Hs.add((-h) % m)
    seen, periods = set(), []
    for a in units:
        if a in seen:
            continue
        coset = {(h * a) % m for h in Hs}
        seen |= coset
        e = K.zero()
        for t in sorted(coset):
            e = K.add(e, K.xpow(t))
        periods.append(e)
    # The periods span the fixed field but need not be a BASIS: for m = 24,
    # H = {1,5} they satisfy eta_1 + eta_7 = 0 (the sum over all units is the
    # Ramanujan sum, which vanishes), and for H = {1} the four periods span only
    # a 3-dimensional space although the field has degree 4.  So determine the
    # degree first and build a power basis from a primitive element.
    deg = len([1 for _ in periods])          # number of cosets = [G' : H{+-1}]
    for prim in periods:
        basis, mat = [], []
        e = K.const(1)
        for _ in range(deg):
            row = [float(x) for x in e]
            if np.linalg.matrix_rank(np.array(mat + [row]), tol=1e-9) <= len(mat):
                break
            mat.append(row); basis.append(e)
            e = K.mul(e, prim)
        if len(basis) == deg:
            return basis
    # fall back: periods plus 1, reduced
    cand = [K.const(1)] + periods
    basis, mat = [], []
    for e in cand:
        row = [float(x) for x in e]
        if np.linalg.matrix_rank(np.array(mat + [row]), tol=1e-9) > len(mat):
            mat.append(row); basis.append(e)
    return basis


def recognise(vals, K, basis, prec=60, maxcoeff=10**6):
    """Express each numerical value in the basis, by integer-relation detection.

    Heuristic by design: PSLQ proposes exact coefficients, and a wrong guess is
    caught by the exact verification that follows.  Fitting a single real number
    against a D-dimensional basis by least squares is underdetermined and was
    an error in an earlier version of this file."""
    import mpmath as mp
    mp.mp.dps = prec
    # PSLQ needs its inputs at working precision; converting through a Python
    # float first caps everything at ~16 digits and the relation is missed.
    bvals = [K.to_complex(b, prec=prec).real for b in basis]
    out = []
    for v in vals:
        rel = mp.pslq([mp.mpf(v)] + bvals, maxcoeff=maxcoeff, maxsteps=20000)
        if rel is None or rel[0] == 0:
            out.append(None); continue
        out.append([Fraction(-int(rel[i + 1]), int(rel[0]))
                    for i in range(len(basis))])
    return out


def to_field(K, coeffs, basis):
    e = K.zero()
    for q, b in zip(coeffs, basis):
        e = K.add(e, K.smul(q, b))
    return e


def det_exact(K, M):
    """Determinant of a square matrix over Q(zeta_m), by cofactor expansion
    (no division, so it stays exact)."""
    n = len(M)
    if n == 1:
        return M[0][0]
    tot = K.zero()
    for j in range(n):
        if K.is_zero(M[0][j]):
            continue
        minor = [[M[i][c] for c in range(n) if c != j] for i in range(1, n)]
        sub = det_exact(K, minor)
        term = K.mul(M[0][j], sub)
        tot = K.add(tot, term) if j % 2 == 0 else K.sub(tot, term)
    return tot


def blocks_exact(K, w_field, n, k, d, ell):
    """M_ell with entries in Q(zeta_m); w_field are field elements."""
    m = n // d
    b = w_field[0:d]; c = w_field[d:2*d]; e = w_field[2*d:3*d]
    aO = w_field[3*d:4*d]; aI = w_field[4*d:5*d]
    # zeta_m = zeta_n^d, so use xpow(d * ell * <power>)
    def zpow(p):
        return K.xpow((d * ell * p) % n)
    N = 2 * d
    M = [[K.zero() for _ in range(N)] for _ in range(N)]
    for r in range(d):
        M[r][r] = K.add(M[r][r], aO[r])
        M[d+r][d+r] = K.add(M[d+r][d+r], aI[r])
        rp, delta = (r + 1) % d, (r + 1) // d
        M[r][rp] = K.add(M[r][rp], K.mul(b[r], zpow(delta)))
        M[rp][r] = K.add(M[rp][r], K.mul(b[r], zpow(-delta)))
        rq, dk = (r + k) % d, (r + k) // d
        M[d+r][d+rq] = K.add(M[d+r][d+rq], K.mul(e[r], zpow(dk)))
        M[d+rq][d+r] = K.add(M[d+rq][d+r], K.mul(e[r], zpow(-dk)))
        M[r][d+r] = K.add(M[r][d+r], c[r])
        M[d+r][r] = K.add(M[d+r][r], c[r])
    return M
