"""Independent verification of a period-d certificate on the FULL matrix.

Rebuilds the 2n x 2n real symmetric matrix from the period-d weights -- not
the Fourier blocks the search used -- and checks, independently:
  * the zero pattern is exactly E(P(n,k)): every vertex has exactly three
    off-diagonal nonzeros, and no required entry is near zero relative to the
    matrix scale;
  * the nullity is 2k+2, with a spectral gap;
  * the nullity does not exceed 2k+2 (the structural ceiling), which is an
    automatic correctness check on the whole pipeline.
"""
import sys
import numpy as np

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from prescribe_symbol import solve_for, grid_interior


def build_full(w, n, k, d):
    b, c, e, aO, aI = (w[j * d:(j + 1) * d] for j in range(5))
    N = 2 * n
    A = np.zeros((N, N))
    for i in range(n):
        r = i % d
        A[i, (i + 1) % n] += b[r]; A[(i + 1) % n, i] += b[r]
        A[i, n + i] += c[r];       A[n + i, i] += c[r]
        A[n + i, n + (i + k) % n] += e[r]; A[n + (i + k) % n, n + i] += e[r]
        A[i, i] = aO[r]; A[n + i, n + i] = aI[r]
    return A


def verify(w, n, k, d, verbose=True):
    A = build_full(w, n, k, d)
    sc = np.abs(A).max()
    lam = np.sort(np.abs(np.linalg.eigvalsh(A)))
    r = int(np.sum(lam < 1e-8 * sc))
    B = np.abs(A) > 1e-12
    np.fill_diagonal(B, False)
    deg = B.sum(axis=1)
    cubic = bool(np.all(deg == 3))
    minoff = np.abs(A[B]).min() / sc
    gap = lam[2 * k + 2] / sc if 2 * k + 2 < len(lam) else np.inf
    ok = (r == 2 * k + 2) and cubic and minoff > 1e-2 and gap > 1e-5
    if verbose:
        print(f"  full matrix {2*n}x{2*n}")
        print(f"  |eigenvalues| smallest {2*k+5}: "
              f"{np.array2string(lam[:2*k+5], precision=3)}")
        print(f"  nullity = {r}  (target 2k+2 = {2*k+2}; ceiling {2*k+2})")
        print(f"  every vertex has exactly 3 off-diagonal nonzeros: {cubic}")
        print(f"  min |required off-diagonal| / scale = {minoff:.6f}")
        print(f"  first nonzero eigenvalue / scale   = {gap:.3e}")
        assert r <= 2 * k + 2, "nullity exceeds the structural ceiling -- bug"
    return ok, r, gap, minoff


if __name__ == "__main__":
    k, d, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    want = tuple(int(v) for v in sys.argv[4].split(","))
    m = n // d
    G = grid_interior(m)
    roots = [s for (l, s) in G if l in want]
    print(f"k={k} d={d} n={n} m={m}; root set l={want}")
    assert len(roots) == k + 1, f"need {k+1} roots, got {len(roots)}"
    w, err, _ = solve_for(n, k, d, roots, tries=80, push=3.0)
    print(f"  symbol solve error {err:.3e}")
    lab = ([f"b{r}" for r in range(d)] + [f"c{r}" for r in range(d)]
           + [f"e{r}" for r in range(d)] + [f"aO{r}" for r in range(d)]
           + [f"aI{r}" for r in range(d)])
    ok, r, gap, minoff = verify(w, n, k, d)
    if ok:
        print(f"\n  *** VALID: Z(P({n},{k})) >= {r} ***")
        print(f"  with the bootstrap bound Z <= {2*k+2}:  "
              f"Z(P({n},{k})) = {2*k+2}")
        print("  weights:")
        for L, v in zip(lab, w):
            print(f"     {L:>4} = {v:+.12f}")
        np.save(f"/Volumes/2TB/scifair/results/zero_forcing/"
                f"cert_k{k}_d{d}_n{n}.npy", w)
    else:
        print(f"\n  not a valid certificate (nullity {r}, gap {gap:.2e}, "
              f"min off-diag {minoff:.4f})")
