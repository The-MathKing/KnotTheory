"""
The adjacency matrix already certifies the lower bound.

Take A in S(P(n,k)) with ALL weights 1 and zero diagonal -- that is, the plain
adjacency matrix.  In the notation of the period-1 analysis
(verification/d1_ceiling.py) this is a = d = 0, b = e = c = 1, so the
2x2 Fourier blocks are

    M_m = [[s_m, 1],[1, t_m]],    s_m = 2cos(2 pi m/n),  t_m = 2cos(2 pi k m/n),

and det M_m = s_m t_m - 1.  Since t = L_k(s) exactly, the singularity condition
is the degree-(k+1) polynomial  s L_k(s) - 1 = 0, and equivalently, in terms of
the angle,

    4 cos(theta) cos(k theta) = 1,   i.e.   2cos((k+1)theta) + 2cos((k-1)theta) = 1,
    theta = 2 pi m / n.

So  nullity(Adj P(n,k)) = #{ m in Z_n : 2cos(2 pi (k+1) m/n) + 2cos(2 pi (k-1) m/n) = 1 }.

Because M(G) <= Z(G) for every matrix whose off-diagonal support is exactly
E(G) -- the adjacency matrix included -- every such count is a rigorous lower
bound on Z(P(n,k)), and it is verifiable in exact integer arithmetic: the
matrix is a 0/1 matrix, so its rank over Q is computable exactly.

Combined with Z(P(n,k)) <= 2k+2 (the rotation-bootstrap theorem), any (n,k)
with adjacency nullity 2k+2 gives Z(P(n,k)) = 2k+2 exactly.
"""
import numpy as np
from fractions import Fraction


def adjacency(n, k):
    N = 2 * n
    A = np.zeros((N, N), dtype=np.int64)
    for i in range(n):
        A[i, (i + 1) % n] = A[(i + 1) % n, i] = 1
        A[i, n + i] = A[n + i, i] = 1
        A[n + i, n + (i + k) % n] = A[n + (i + k) % n, n + i] = 1
    return A


def exact_nullity(A):
    """Rank over Q by fraction-free Gaussian elimination -- no floating point."""
    M = [[Fraction(int(v)) for v in row] for row in A]
    rows, cols = len(M), len(M[0])
    rank, piv = 0, 0
    for c in range(cols):
        sel = None
        for rr in range(rank, rows):
            if M[rr][c] != 0:
                sel = rr
                break
        if sel is None:
            continue
        M[rank], M[sel] = M[sel], M[rank]
        inv = Fraction(1) / M[rank][c]
        M[rank] = [x * inv for x in M[rank]]
        for rr in range(rows):
            if rr != rank and M[rr][c] != 0:
                f = M[rr][c]
                M[rr] = [x - f * y for x, y in zip(M[rr], M[rank])]
        rank += 1
        if rank == rows:
            break
    return cols - rank


def predicted_nullity(n, k):
    """The closed-form count, from 2cos((k+1)th) + 2cos((k-1)th) = 1."""
    m = np.arange(n)
    th = 2 * np.pi * m / n
    val = 2 * np.cos((k + 1) * th) + 2 * np.cos((k - 1) * th)
    return int(np.sum(np.abs(val - 1.0) < 1e-9))


if __name__ == "__main__":
    print("adjacency nullity of P(n,k)  (a rigorous lower bound on Z)")
    print("closed-form count cross-checked against exact rational rank\n")
    hits = []
    print(f"{'k':>3} {'n':>4} {'2k+2':>5} {'nullity':>8} {'exact':>6} {'=2k+2?':>7}")
    for k in range(2, 11):
        for n in range(2 * k + 3, 121):
            if 2 * k >= n:
                continue
            p = predicted_nullity(n, k)
            if p == 0:
                continue
            ex = exact_nullity(adjacency(n, k)) if n <= 60 else None
            if ex is not None and ex != p:
                print(f"  MISMATCH k={k} n={n}: closed form {p}, exact {ex}")
            if p >= 6:
                print(f"{k:>3} {n:>4} {2*k+2:>5} {p:>8} "
                      f"{str(ex) if ex is not None else '-':>6} "
                      f"{'YES' if p == 2*k+2 else '':>7}", flush=True)
            if p == 2 * k + 2:
                hits.append((n, k, p, ex))
    print("\n(n,k) with adjacency nullity exactly 2k+2, hence Z(P(n,k)) = 2k+2:")
    for (n, k, p, ex) in hits:
        print(f"   Z(P({n},{k})) = {p}"
              + (f"   [exact rational rank confirms nullity {ex}]"
                 if ex is not None else "   [closed form]"))
    print(f"\ntotal: {len(hits)} exact values")
