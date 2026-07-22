"""Reaching the ceiling for EVERY n: solving T = I directly.

Why the previous approaches cannot answer this.  A period-one symbol is a fixed
polynomial whose roots are fixed algebraic numbers, and a fixed algebraic number
lies on Gamma_n = {2cos(2 pi m/n)} only for n in a divisibility class.  So no
period-one certificate can be general in n.  k=2 escapes only because it has
zero residual conditions, letting its roots be chosen as functions of n; for
k >= 3 the k-2 residual conditions are exact equations on a discrete grid, met
only by Galois coincidence, i.e. by divisibility.

So drop rho-invariance and use the paper's own criterion.  cor:ceiling: for ANY
matrix on the pattern, null A = 2k+2 if and only if the monodromy T of the
reduced recurrence is the identity.  That is (2k+2)^2 equations in the 5n
weights (a, d diagonals and b, c, e edge weights), with det T = 1 automatic in
the symmetric case, and one overall scaling gauge.  Counting:

    5n - 1 >= (2k+2)^2 - 1   i.e.   n >= (2k+2)^2 / 5.

Crucially T is only defined when the spokes c_i and outer weights b_i are
nonzero -- it divides by them -- so the degenerate solutions that wrecked an
eigenvalue-minimising search (all spokes zero, or all edges zero, which give
large nullity off the pattern) are excluded by the formulation itself rather
than by a barrier.
"""
import sys

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from recurrence_order import monodromy


def unpack(w, n):
    return w[:n], w[n:2*n], w[2*n:3*n], w[3*n:4*n], w[4*n:5*n]   # b,c,e,a,d


def residual(w, n, k, tau=0.05):
    b, c, e, a, d = unpack(w, n)
    sc = max(np.abs(w).max(), 1e-12)
    if min(np.abs(b).min(), np.abs(c).min(), np.abs(e).min()) < 1e-9 * sc:
        return np.full((2*k+2)**2 + 3*n, 1e3)
    T = monodromy(n, k, b, c, e, a, d)
    res = (T - np.eye(2*k+2)).ravel()
    # keep the edge weights off zero: T stays defined but becomes ill-conditioned
    bar = 3.0 * np.maximum(0.0, tau - np.abs(w[:3*n]) / sc)
    return np.concatenate([res, bar])


def nullity(n, k, w):
    b, c, e, a, d = unpack(w, n)
    N = 2 * n
    A = np.zeros((N, N))
    for i in range(n):
        A[i, i] = a[i]; A[n+i, n+i] = d[i]
        j = (i+1) % n
        A[i, j] = A[j, i] = b[i]
        A[i, n+i] = A[n+i, i] = c[i]
        p, q = n+i, n+(i+k) % n
        A[p, q] = A[q, p] = e[i]
    sv = np.linalg.svd(A, compute_uv=False)
    return int(np.sum(sv < 1e-9 * sv.max())), sv, A


def solve(n, k, tries=15, seed=0):
    rng = np.random.default_rng(seed)
    best = None
    for t in range(tries):
        w0 = rng.standard_normal(5*n)
        w0[:3*n] += 1.2 * np.sign(w0[:3*n])          # start edges away from 0
        s = least_squares(residual, w0, args=(n, k), method="trf",
                          xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=600)
        err = np.abs(residual(s.x, n, k)[:(2*k+2)**2]).max()
        nul, sv, A = nullity(n, k, s.x)
        cand = (-nul, err, s.x.copy())
        if best is None or cand[:2] < best[:2]:
            best = cand
    nul, sv, A = nullity(n, k, best[2])
    b, c, e, _, _ = unpack(best[2], n)
    sc = np.abs(best[2]).max()
    minedge = min(np.abs(b).min(), np.abs(c).min(), np.abs(e).min()) / sc
    np.save(f"/Volumes/2TB/scifair/results/zero_forcing/w_{n}_{k}.npy", best[2])
    return nul, best[1], minedge, sv


def is_prime(n):
    return n > 1 and all(n % d for d in range(2, int(n**0.5)+1))


def main():
    k = int(sys.argv[1])
    ns = [int(x) for x in sys.argv[2:]]
    r = 2*k+2
    thr = int(np.ceil(r*r/5))
    print(f"k = {k}   ceiling r = 2k+2 = {r}   |T - I| is {r*r} equations in 5n "
          f"weights  =>  n >= {thr}")
    print("    n  prime  5n - r^2   max|T - I|   min|edge|/scale   nullity  "
          "verdict")
    for n in ns:
        if 2*k >= n:
            print(f" {n:4d}   (needs n > 2k)"); continue
        nul, err, me, sv = solve(n, k)
        print(f" {n:4d}   {'yes' if is_prime(n) else ' no'}{5*n-r*r:10d}"
              f"{err:14.2e}{me:18.4f}{nul:10d}   "
              f"{'CEILING' if nul >= r else 'no'}")


if __name__ == "__main__":
    main()
