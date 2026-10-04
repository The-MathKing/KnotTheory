"""
An EXACT k=6 certificate over a quadratic field.

The H-stable root sets found by verification/subfield_certificates.py are
realisable, and H-stability means the variety

    V = { w : det M_l(w) = 0 for l in S }

is defined over K = Q(zeta_m)^H, because sigma in H permutes the equations
among themselves.  So we look for K-rational points of V.

Pipeline:
  1. fix 5d-(k+1) weights at chosen RATIONALS (which lie in K), leaving a
     square system of k+1 equations in k+1 unknowns -- a 0-dimensional
     K-variety;
  2. solve it to 60 digits with mpmath Newton (double precision is nowhere
     near enough for step 3);
  3. propose exact values by integer-relation detection against a Q-basis of K
     (heuristic -- a wrong guess fails step 4);
  4. rebuild the blocks over Q(zeta_m) with those exact values and check
     det M_l = 0 EXACTLY, as an identity modulo Phi_m.

Step 4 is the only one that has to be right.  Given it, the k+1 chosen roots
are each hit by two Fourier indices, so 2k+2 blocks are singular, and the
ceiling forces the nullity to be exactly 2k+2 -- a discrete consequence of an
exactly verified equation, not a thresholded rank.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import sys
from fractions import Fraction

import mpmath as mp
import numpy as np

sys.path.insert(0, f"{_REPO}/verification")
from exact_certifier import Cyclo
from exact_subfield_verify import field_basis, recognise, to_field, \
    det_exact, blocks_exact
from prescribe_symbol import grid_interior
from verify_period_d_cert import verify


def M_mp(w, n, k, d, ell):
    """Block M_ell with mpmath complex entries."""
    m = n // d
    b, c, e, aO, aI = (w[j * d:(j + 1) * d] for j in range(5))
    z = mp.expjpi(2 * mp.mpf(ell) / m)
    N = 2 * d
    M = mp.zeros(N, N)
    for r in range(d):
        M[r, r] += aO[r]
        M[d + r, d + r] += aI[r]
        rp, delta = (r + 1) % d, (r + 1) // d
        M[r, rp] += b[r] * z ** delta
        M[rp, r] += b[r] * mp.conj(z) ** delta
        rq, dk = (r + k) % d, (r + k) // d
        M[d + r, d + rq] += e[r] * z ** dk
        M[d + rq, d + r] += e[r] * mp.conj(z) ** dk
        M[r, d + r] += c[r]
        M[d + r, r] += c[r]
    return M


def solve_hp(w0, n, k, d, S, free_idx, prec=60):
    mp.mp.dps = prec
    fixed = [mp.mpf(float(x)) for x in w0]

    def F(*xs):
        w = list(fixed)
        for j, x in zip(free_idx, xs):
            w[j] = x
        return [mp.re(mp.det(M_mp(w, n, k, d, l))) for l in S]

    x0 = [mp.mpf(float(w0[j])) for j in free_idx]
    sol = mp.findroot(F, x0, tol=mp.mpf(10) ** (-(prec - 8)))
    w = list(fixed)
    for j, x in zip(free_idx, [sol[i] for i in range(len(free_idx))]):
        w[j] = x
    return w


if __name__ == "__main__":
    k, d, n = 6, 3, 72
    m = n // d
    H = [int(v) for v in sys.argv[1].split(",")] if len(sys.argv) > 1 else [1, 7]
    S = tuple(int(v) for v in sys.argv[2].split(",")) if len(sys.argv) > 2 \
        else (1, 2, 3, 6, 7, 9, 10)
    prec = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    K = Cyclo(m)
    basis = field_basis(K, m, H)
    print(f"k={k} d={d} n={n} m={m}; H={H}; root set l={S}")
    print(f"fixed field of H has degree {len(basis)} over Q; basis values "
          f"{[float(K.to_complex(b, prec=30).real) for b in basis]}")

    G0 = grid_interior(m)
    roots = [s for (l, s) in G0 if l in S]
    from prescribe_symbol import solve_for
    w0, err, _ = solve_for(n, k, d, roots, tries=30, push=3.0)
    ok, nul, gap, minoff = verify(w0, n, k, d, verbose=False)
    print(f"double-precision seed: symbol err {err:.2e}, nullity {nul}, "
          f"min|req| {minoff:.4f}, {'realisable' if ok else 'DEGENERATE'}")
    if not ok:
        print("seed not realisable; aborting"); raise SystemExit

    free_idx = list(range(3 * d, 3 * d + k + 1))[:k + 1]
    if len(free_idx) < k + 1:
        free_idx = list(range(5 * d))[-(k + 1):]
    print(f"refining coordinates {free_idx} to {prec} digits ...")
    w = solve_hp(w0, n, k, d, S, free_idx, prec=prec)
    res = max(abs(mp.re(mp.det(M_mp(w, n, k, d, l)))) for l in S)
    print(f"  high-precision residual: {mp.nstr(res, 5)}")
    print("\nrecognising weights in the fixed field:")
    rec = recognise([w[j] for j in range(5 * d)], K, basis, prec=prec)
    lab = ([f"b{r}" for r in range(d)] + [f"c{r}" for r in range(d)]
           + [f"e{r}" for r in range(d)] + [f"aO{r}" for r in range(d)]
           + [f"aI{r}" for r in range(d)])
    good = True
    for L, v, r in zip(lab, w, rec):
        print(f"   {L:>4} = {mp.nstr(v, 22):>26}  ->  "
              + (str(r) if r is not None else "NOT RECOGNISED"))
        good &= r is not None
    if not good:
        print("\nnot all weights lie in this field at this height.")
        raise SystemExit
    wf = [to_field(K, r, basis) for r in rec]
    print("\nEXACT check: det M_l = 0 in Q(zeta_m)?")
    allz = True
    for l in S:
        M = blocks_exact(K, wf, n, k, d, l)
        dd = det_exact(K, M)
        z = K.is_zero(dd)
        allz &= z
        print(f"   l={l:>3}: {'ZERO (exact)' if z else 'NONZERO'}")
    print(f"\n{'*** EXACT CERTIFICATE ***' if allz else 'exact check failed'}")
