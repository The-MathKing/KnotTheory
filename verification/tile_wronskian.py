"""The invariant skew form of a tile, EXACTLY, from the discrete Green identity.

For a symmetric matrix A on the infinite strip (the recurrence of thm:red) and
two kernel sequences z, z', the flux across the cut between positions j and j+1,

    J_j(z,z') = sum over edges (p,q) with p left of the cut and q right of it
                of A_pq (z_p z'_q - z'_p z_q),

is independent of j: J_{j+1} - J_j = sum over the vertices at position j+1 of
(z_p (A z')_p - z'_p (A z)_p) = 0.  Writing the flux through the state vector
Z_{j+1} = (x_{j-k-1}, ..., x_{j+k}) of 2k+2 consecutive outer coordinates (the
inner coordinates y_m being determined by x_{m-1}, x_m, x_{m+1}), it becomes
Z_{j+1}^T B_{j+1} Z'_{j+1} with B skew and depending only on the weights at
positions j-k-1 .. j+k.  Hence T_i^T B_{i+1} T_i = B_i for every step, and for a
tile whose two ends carry the same dock of k+1 positions, B_0 = B_l = B(dock):

    P^T B(dock) P = B(dock)   for every tile product P.

This file computes B(dock) exactly (Fractions) and decides whether it is
nondegenerate, i.e. whether tile products lie in Sp(2k+2) rather than in a
larger orthogonal-type group.  That is what lets a full-rank differential of
dimension (k+1)(2k+3) be a submersion onto the group.
"""
from fractions import Fraction
import sys


def wronskian_form(k, dock):
    """B (2k+2 x 2k+2, Fractions) for the state Z_0 = (x_{-k-1}, ..., x_k) at the
    cut between positions -1 and 0, with constant dock weights everywhere."""
    a0, c0, d0, e0 = (Fraction(v) for v in dock)
    b0 = Fraction(1)
    r = 2 * k + 2
    idx = {m: m + k + 1 for m in range(-k - 1, k + 1)}  # x_m -> coordinate

    def y_coeffs(m):
        """y_m as a linear form in the x's: -(b x_{m-1} + a x_m + b x_{m+1}) / c."""
        v = [Fraction(0)] * r
        for mm, coef in ((m - 1, b0), (m, a0), (m + 1, b0)):
            v[idx[mm]] += -coef / c0
        return v

    B = [[Fraction(0)] * r for _ in range(r)]

    def add_edge(wt, lp, lq):
        """edge with weight wt between linear forms lp (left) and lq (right):
        adds wt*(lp_i lq_j - lq_i lp_j) to B."""
        for i in range(r):
            if lp[i] == 0 and lq[i] == 0:
                continue
            for j in range(r):
                B[i][j] += wt * (lp[i] * lq[j] - lq[i] * lp[j])

    def x_form(m):
        v = [Fraction(0)] * r
        v[idx[m]] = Fraction(1)
        return v

    # outer edge u_{-1} u_0
    add_edge(b0, x_form(-1), x_form(0))
    # inner edges v_m v_{m+k} crossing the cut: m = -k .. -1 (left), m+k = 0 .. k-1 (right)
    for m in range(-k, 0):
        add_edge(e0, y_coeffs(m), y_coeffs(m + k))
    return B


def det_fraction(M):
    M = [row[:] for row in M]
    n = len(M)
    det = Fraction(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None:
            return Fraction(0)
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            det = -det
        det *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f:
                for j in range(c, n):
                    M[r][j] -= f * M[c][j]
    return det


def check_invariance(k, dock, l, seed=0):
    """Numerical sanity: P^T B P = B for a random tile."""
    import numpy as np
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    from tile_controllability import tile_product, dock_point
    B = np.array([[float(v) for v in row] for row in wronskian_form(k, dock)])
    rng = np.random.default_rng(seed)
    w = dock_point(l, k, tuple(float(x) for x in dock)) + 0.3 * rng.standard_normal(5 * (l - 2 * k - 2))
    P = tile_product(w, l, k, tuple(float(x) for x in dock))
    return np.abs(P.T @ B @ P - B).max() / np.abs(B).max()


if __name__ == "__main__":
    from tile_rank_exact import integer_elliptic_dock
    for k in range(2, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 10):
        dock = integer_elliptic_dock(k)
        B = wronskian_form(k, dock)
        d = det_fraction(B)
        skew = all(B[i][j] == -B[j][i] for i in range(len(B)) for j in range(len(B)))
        err = check_invariance(k, dock, 2 * k + 2 + 10)
        print(f"k={k}: dock {dock}: B skew={skew}, det B = {d} ({'nondegenerate' if d != 0 else 'DEGENERATE'}); invariance residual {err:.1e}")
