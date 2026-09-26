"""Exact rational evaluation of the Krawczyk test.

WHY THIS FILE EXISTS.  The Krawczyk criterion is a theorem about real numbers;
evaluating it in float64 is not a proof of its hypotheses.  krawczyk.py and
certify_tiles.py compute the three norms

    ||Y||_inf,    alpha0 = ||I - Y J(z0)||_inf,    eta = ||Y f(z0)||_inf

in double precision with no directed rounding, and evaluate J and f at the
double-rounded point rather than at the 60-digit one.  The margins are enormous
(alpha0 ~ 1e-10 against 1, eta ~ 1e-61 against delta), so the conclusion was
surely true -- but "proved by interval certification" must not rest on that.

This module recomputes the entire test with NO ROUNDING ANYWHERE.  Three facts
make that possible.

  * z0 is exactly rational.  We snap the certificate to the dyadic grid
    2^-SNAP, so every coordinate is an exact rational with denominator 2^SNAP.
    The snap moves z0 by at most 2^-SNAP-1, which is irrelevant: z0 is only the
    CENTRE of the box, and the test re-measures f(z0) after the move.
  * f and J are polynomials with integer coefficients -- f(z) = A(w)K(X) is
    bilinear, so J is affine -- hence f(z0) and J(z0) are exactly rational, and
    are built here as integer matrices over a common denominator.
  * Y is ARBITRARY.  The Krawczyk test holds for any matrix Y; Y must only make
    alpha0 small, it need not be J(z0)^{-1}.  So we take the float64 inverse and
    read it as an exact dyadic rational, losing nothing at all.

Consequently alpha0, ||Y||_inf and eta computed below are exact rationals, the
comparisons alpha < 1 and eta + alpha*delta <= delta are exact integer
comparisons, and a PASS here is a proof.

THE ONE ENGINEERING PROBLEM IS SPEED.  alpha0 needs every entry of the rk x rk
product Y J(z0), with rk in the hundreds to low thousands, so a Fraction matmul
is hopeless.  Instead both factors are scaled to integer matrices and multiplied
by BALANCED LIMB DECOMPOSITION: each integer is written in base 2^BASE with
digits in [-2^(BASE-1), 2^(BASE-1)), each pair of digit matrices is multiplied
by BLAS in float64 -- the entries stay below 2^53, so those float products are
themselves exact integers -- and the limb products are recombined with Python
integers.  That yields the exact integer product at BLAS speed.  The guard
_exactness_guard() refuses to proceed if the limb bound is not met, so the
routine cannot silently return an inexact answer.
"""
import sys
from fractions import Fraction
from math import gcd

import numpy as np

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from certify_general import pattern_cells, assemble, graph_form, build_K, jac

BASE = 20    # limb width in bits
SNAP = 60    # z0 is snapped to the dyadic grid 2^-SNAP


# ---------------------------------------------------------------- exact matmul

def _signed_limbs(M):
    """Write an integer object-array in base 2^BASE with balanced digits."""
    half, full = 1 << (BASE - 1), 1 << BASE
    shape = M.shape
    flat = [int(x) for x in M.ravel().tolist()]
    limbs = []
    while any(flat):
        d, nxt = [], []
        for x in flat:
            t = x % full
            if t >= half:
                t -= full
            d.append(t)
            nxt.append((x - t) >> BASE)
        limbs.append(np.array(d, dtype=float).reshape(shape))
        flat = nxt
        if len(limbs) > 400:
            raise RuntimeError("limb decomposition failed to terminate")
    return limbs or [np.zeros(shape)]


def _exactness_guard(nla, nlb, inner):
    """Every float64 limb product must be an exact integer."""
    per = (1 << (BASE - 1)) ** 2 * inner
    worst = per * min(nla, nlb)
    if worst >= 2 ** 53:
        raise RuntimeError(
            f"limb products would not be exact in float64: {worst} >= 2^53; "
            f"lower BASE")
    return worst


def exact_int_matmul(A, B):
    """Exact product of two integer matrices held as object arrays."""
    la, lb = _signed_limbs(A), _signed_limbs(B)
    _exactness_guard(len(la), len(lb), A.shape[1])
    ns = len(la) + len(lb) - 1
    acc = [np.zeros((A.shape[0], B.shape[1])) for _ in range(ns)]
    for p, ap in enumerate(la):
        for q, bq in enumerate(lb):
            acc[p + q] += ap @ bq
    shift = 1 << BASE
    out = np.zeros(acc[0].shape, dtype=object)
    for s in range(ns - 1, -1, -1):
        blk = acc[s]
        if np.abs(blk).max() >= 2 ** 53:
            raise RuntimeError("limb accumulation left the exact float range")
        out = out * shift + blk.astype(np.int64).astype(object)
    return out


# ------------------------------------------------------- exact system at z0

def snap(zfloat, S=SNAP):
    """The certificate read as exact rationals on the dyadic grid 2^-S.

    Returns integer numerators over the common denominator 2^S.
    """
    D = 1 << S
    return [int(round(Fraction(float(v)) * D)) for v in zfloat], D


def _maps(cells, perm, r):
    r_of = {p: s for s, p in enumerate(perm[:r])}
    m_of = {p: m for m, p in enumerate(perm[r:])}
    rows = {}
    for j, (_, cl) in enumerate(cells):
        for (i, l) in cl:
            rows.setdefault(i, []).append((j, l))
    return r_of, m_of, rows


def exact_jac_and_f(zint, Dz, cells, perm, N, r, nw, eqs, free):
    """J(z0) as an integer matrix over Dz, and f(z0) over Dz^2.

    J's entries are, by construction, either 0, 1, or a single coordinate of z0:
    the w-columns carry entries of K and the X-columns carry entries of A.  That
    is why J(z0) is exactly rational with the SAME denominator as z0.
    """
    r_of, m_of, rows = _maps(cells, perm, r)
    colpos = {c: idx for idx, c in enumerate(free)}
    Js = np.zeros((len(eqs), len(free)), dtype=object)
    F = []
    for e_idx, e in enumerate(eqs):
        i, t = divmod(e, r)
        acc = 0
        for (j, l) in rows.get(i, []):
            if l in r_of:                       # K[l,t] is 1 or 0
                kv = Dz if r_of[l] == t else 0
            else:                               # K[l,t] = X[m,t]
                kv = zint[nw + m_of[l] * r + t]
            acc += zint[j] * kv                 # f gets w_j * K[l,t]
            if j in colpos:                     # d f / d w_j = K[l,t]
                Js[e_idx, colpos[j]] += kv
            if l in m_of:                        # d f / d X[m,t] = A[i,l]
                c = nw + m_of[l] * r + t
                if c in colpos:
                    Js[e_idx, colpos[c]] += zint[j]
        F.append(acc)
    return Js, F


# ------------------------------------------------------------- the exact test

def exact_krawczyk(zfloat, cells, perm, N, r, nw, eqs, free, L_lip,
                   deltas=None, verbose=True, tag=""):
    """Run the Krawczyk test in exact rational arithmetic.

    Returns (passed, info) with every number in info an exact Fraction.
    """
    if deltas is None:
        deltas = [Fraction(1, 10 ** p) for p in range(14, 3, -1)]
    zint, Dz = snap(zfloat)
    Js, F = exact_jac_and_f(zint, Dz, cells, perm, N, r, nw, eqs, free)
    rk = len(eqs)
    assert Js.shape == (rk, len(free)) and rk == len(free), (Js.shape, rk)

    # Y: the float64 inverse, read exactly.  Any Y is admissible.
    Jf = np.array([[float(Fraction(int(v), Dz)) for v in row] for row in Js])
    Yf = np.linalg.inv(Jf)
    Yfr = [[Fraction(float(v)) for v in row] for row in Yf]
    Dy = 1
    for row in Yfr:
        for v in row:
            Dy = Dy * v.denominator // gcd(Dy, v.denominator)
    Yint = np.array([[int(v * Dy) for v in row] for row in Yfr], dtype=object)

    # ||Y||_inf, exactly
    Ynorm = max(Fraction(sum(abs(int(v)) for v in row), Dy) for row in Yint)

    # alpha0 = ||I - Y J(z0)||_inf, exactly
    P = exact_int_matmul(Yint, Js)              # = Y J(z0) * (Dy*Dz)
    scale = Dy * Dz
    alpha0 = Fraction(0)
    for i in range(rk):
        s = 0
        row = P[i]
        for j in range(rk):
            v = int(row[j]) - (scale if i == j else 0)
            s += v if v >= 0 else -v
        a = Fraction(s, scale)
        if a > alpha0:
            alpha0 = a

    # eta = ||Y f(z0)||_inf, exactly
    eta = Fraction(0)
    dsq = Dz * Dz
    for i in range(rk):
        s = 0
        row = Yint[i]
        for j in range(rk):
            s += int(row[j]) * F[j]
        e = Fraction(abs(s), Dy * dsq)
        if e > eta:
            eta = e

    passed, used = False, None
    for delta in deltas:
        alpha = alpha0 + Ynorm * L_lip * delta
        if alpha < 1 and eta + alpha * delta <= delta:
            passed, used = True, (delta, alpha)
            break
    fnorm = max((Fraction(abs(v), Dz * Dz) for v in F), default=Fraction(0))
    info = dict(alpha0=alpha0, Ynorm=Ynorm, eta=eta, rk=rk, fnorm=fnorm,
                delta=used[0] if used else None,
                alpha=used[1] if used else None)
    if verbose:
        print(f"  EXACT{(' ' + tag) if tag else ''}: rk={rk}  "
              f"||Y||={float(Ynorm):.4e}  alpha0={float(alpha0):.4e}  "
              f"eta={float(eta):.4e}  ||f(z0)||={float(fnorm):.4e}")
        if passed:
            d, a = used
            print(f"  EXACT KRAWCZYK PASSES at delta={float(d):g}: "
                  f"alpha={float(a):.6e} < 1 and "
                  f"eta+alpha*delta={float(eta + a * d):.4e} <= {float(d):g}")
            print(f"        (all four quantities are exact rationals; the two "
                  f"comparisons are exact integer comparisons)")
        else:
            print("  EXACT test did not pass at any tested delta")
    return passed, info


def edge_bound(zfloat, n, k, delta):
    """R3: bound the edge weights over the WHOLE box, not just at the centre.

    Every edge weight of A(w) for w in the box differs from its value at z0 by
    at most delta, so min|edge| - delta is a lower bound valid for the certified
    w*, which is what cor:ceiling needs to apply to A(w*) as a matrix of P(n,k).
    """
    edges = [abs(Fraction(float(v))) for v in zfloat[2 * n:5 * n]]
    scale = max(abs(Fraction(float(v))) for v in zfloat[:5 * n])
    lo = min(edges) - Fraction(delta)
    return lo, scale, lo / scale
