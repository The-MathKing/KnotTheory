"""
Why is the rank of (weights -> symbol coefficients) equal to 2d+1?

The rank law rank = min(2d+1, k+1) is the load-bearing unproved observation
behind every k >= 6 result.  Proving it means identifying the (5d - (2d+1)) =
(3d-1)-dimensional nullspace of the Jacobian.  Two candidate sources of
degeneracy:

  GAUGE. Conjugating A by a positive diagonal matrix D (period d) preserves the
  pattern and the nullity, and multiplies det M_l by the constant det(D)^2,
  so it leaves the MONIC symbol unchanged.  D has 2d parameters, so this
  accounts for 2d dimensions.

  That leaves d-1 unexplained.  The natural guess is that the symbol sees the
  off-diagonal weights only through certain products: for a periodic Jacobi
  matrix the zeta-dependent part of the determinant enters only through the
  product of the off-diagonal entries.  If the symbol depends on (b_0..b_{d-1})
  only via prod b_r, and likewise for e, that is a further (d-1)+(d-1)
  directions -- but some overlap the gauge.

This script tests those hypotheses directly: it computes the Jacobian
nullspace, compares it with the explicit gauge directions, and checks whether
rescaling the b's (or e's) at fixed product leaves the symbol invariant.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import sys
import numpy as np

sys.path.insert(0, f"{_REPO}/verification")
from period_d_rank import G_coeffs


def gauge_directions(w, n, k, d):
    """Tangent directions of A -> D A D, D = diag(exp(t_x)) of period d.
    b_r -> b_r * exp(t^O_r + t^O_{r+1});  c_r -> c_r * exp(t^O_r + t^I_r);
    e_r -> e_r * exp(t^I_r + t^I_{r+k});  a_r -> a_r * exp(2 t^O_r);
    d_r -> d_r * exp(2 t^I_r)."""
    P = 5 * d
    dirs = []
    for which in ("O", "I"):
        for r0 in range(d):
            v = np.zeros(P)
            for r in range(d):
                b, c, e, aO, aI = (r, d + r, 2 * d + r, 3 * d + r, 4 * d + r)
                if which == "O":
                    if r == r0:            v[b] += w[b]
                    if (r + 1) % d == r0:  v[b] += w[b]
                    if r == r0:            v[c] += w[c]
                    if r == r0:            v[aO] += 2 * w[aO]
                else:
                    if r == r0:            v[c] += w[c]
                    if r == r0:            v[e] += w[e]
                    if (r + k) % d == r0:  v[e] += w[e]
                    if r == r0:            v[aI] += 2 * w[aI]
            dirs.append(v)
    return np.array(dirs)


def jacobian(w, n, k, d, h=1e-6):
    P = 5 * d
    J = np.zeros((k + 1, P))
    for j in range(P):
        wp, wm = w.copy(), w.copy()
        wp[j] += h; wm[j] -= h
        J[:, j] = (G_coeffs(wp, n, k, d)[1:] - G_coeffs(wm, n, k, d)[1:]) / (2 * h)
    return J


if __name__ == "__main__":
    print("Structure of the Jacobian nullspace of (weights -> symbol)\n")
    print(f"{'k':>3} {'d':>3} {'5d':>4} {'rank':>5} {'null dim':>9} "
          f"{'gauge dim':>10} {'gauge in null?':>15} {'unexplained':>12}")
    rng = np.random.default_rng(1)
    for k in (5, 6, 7, 8):
        for d in (1, 2, 3, 4):
            n = d * (2 * k + 12)
            w = rng.standard_normal(5 * d)
            w[:3 * d] += 1.4 * np.sign(w[:3 * d])
            J = jacobian(w, n, k, d)
            sv = np.linalg.svd(J, compute_uv=False)
            rank = int(np.sum(sv > 1e-7 * max(sv[0], 1.0)))
            U, s2, Vt = np.linalg.svd(J)
            null = Vt[rank:]
            Gd = gauge_directions(w, n, k, d)
            # is each gauge direction inside the nullspace?
            resid = np.linalg.norm(Gd @ J.T, axis=1) / (
                np.linalg.norm(Gd, axis=1) * max(np.abs(J).max(), 1e-12))
            gauge_ok = bool(np.all(resid < 1e-5))
            gdim = int(np.linalg.matrix_rank(Gd, tol=1e-8))
            print(f"{k:>3} {d:>3} {5*d:>4} {rank:>5} {5*d-rank:>9} {gdim:>10} "
                  f"{str(gauge_ok):>15} {5*d-rank-gdim:>12}")
