"""
Period-d certificates for P(n,k): does enlarging the symmetry class help?

Period-1 (fully rotation-invariant) certificates are now completely understood:
the symbol carries exactly three free parameters for every k, the rational
search is finite and complete, and the ceiling 2k+2 is attained only for
k = 2, 4, 5.  The diagnosis (verification/cyclotomic_exhaustive.py) was that
the binding constraint is the k-2 linear membership conditions imposed on a
3-dimensional family.

A period-d matrix commutes with rho^d rather than rho: the weights repeat with
period d | n, giving 5d free parameters instead of 5.  By the same monodromy
argument the ceiling is unchanged at 2k+2, but the parameter count becomes
5d - 1 free ratios against the k+1 coefficients of the characteristic
polynomial, so d >= (k+2)/5 restores the count.  This script tests whether the
count being restored is enough -- the earlier period-2 work suggested that
realisability (c^2 > 0 in the period-1 language) becomes the new binding
constraint.

The search is only 5d-dimensional, so hundreds of random starts are cheap.
"""
import sys
import numpy as np
from scipy.optimize import minimize


def generators(n, k, d):
    """5d symmetric generators: outer edges, spokes, inner edges, and the two
    diagonals, each class split by residue mod d."""
    N = 2 * n
    gens, req = [], []
    for r in range(d):
        for kind in ("outer", "spoke", "inner", "diagO", "diagI"):
            pos = []
            for i in range(r, n, d):
                if kind == "outer":
                    pos += [(i, (i + 1) % n), ((i + 1) % n, i)]
                elif kind == "spoke":
                    pos += [(i, n + i), (n + i, i)]
                elif kind == "inner":
                    pos += [(n + i, n + (i + k) % n), (n + (i + k) % n, n + i)]
                elif kind == "diagO":
                    pos += [(i, i)]
                else:
                    pos += [(n + i, n + i)]
            gens.append(pos)
            req.append(kind in ("outer", "spoke", "inner"))
    rows = np.concatenate([[p for (p, q) in g] for g in gens])
    cols = np.concatenate([[q for (p, q) in g] for g in gens])
    owner = np.concatenate([[j] * len(g) for j, g in enumerate(gens)])
    return rows, cols, owner, N, np.array(req)


def assemble(w, rows, cols, owner, N):
    A = np.zeros((N, N))
    np.add.at(A, (rows, cols), w[owner])
    return A


def objective(w, rows, cols, owner, N, r, req, tau, mu):
    A = assemble(w, rows, cols, owner, N)
    lam, Q = np.linalg.eigh(A)
    idx = np.argsort(np.abs(lam))[:r]
    vals, V = lam[idx], Q[:, idx]
    scale = max(np.abs(A).max(), 1e-12)
    f = float(np.sum((vals / scale) ** 2))
    contrib = 2.0 * (vals / scale ** 2)[None, :] * (V[rows, :] * V[cols, :])
    g = np.zeros(len(req))
    np.add.at(g, owner, contrib.sum(axis=1))
    viol = np.maximum(0.0, tau - np.abs(w[req]) / scale)
    f += mu * float(np.sum(viol ** 2))
    gb = np.zeros(len(req))
    gb[req] = -2.0 * mu * viol * np.sign(w[req]) / scale
    P = len(req)
    f += 1e-3 * (w @ w / P - 1.0) ** 2
    g += gb + 4e-3 * (w @ w / P - 1.0) * w / P
    return f, g


def search(n, k, d, r, tries=400, seed=0, tau=0.06, mu=40.0):
    rows, cols, owner, N, req = generators(n, k, d)
    P = len(req)
    rng = np.random.default_rng(seed)
    best = None
    for t in range(tries):
        w0 = rng.standard_normal(P)
        w0 *= np.sqrt(P) / np.linalg.norm(w0)
        res = minimize(objective, w0, jac=True, method="L-BFGS-B",
                       args=(rows, cols, owner, N, r, req, tau, mu),
                       options=dict(maxiter=4000, ftol=1e-18, gtol=1e-14))
        A = assemble(res.x, rows, cols, owner, N)
        lam = np.sort(np.abs(np.linalg.eigvalsh(A)))
        scale = np.abs(A).max()
        small, gap = lam[r - 1] / scale, lam[r] / scale
        minnz = np.abs(res.x[req]).min() / scale
        if best is None or small < best[1]:
            best = (res.x.copy(), small, gap, minnz)
    return best


if __name__ == "__main__":
    k = int(sys.argv[1])
    ds = [int(v) for v in sys.argv[2].split(",")]
    ns = [int(v) for v in sys.argv[3].split(",")]
    tries = int(sys.argv[4]) if len(sys.argv) > 4 else 300
    r = 2 * k + 2
    print(f"period-d search, k={k}, target nullity r={r} (= 2k+2)")
    print(f"{'n':>5} {'d':>3} {'params':>7} {'lam_r/scale':>13} "
          f"{'gap':>10} {'min|wt|':>9}  verdict")
    for n in ns:
        for d in ds:
            if n % d or 2 * k >= n:
                continue
            w, small, gap, minnz = search(n, k, d, r, tries=tries)
            ok = small < 1e-9 and gap > 1e-3 and minnz > 1e-2
            print(f"{n:>5} {d:>3} {5*d:>7} {small:>13.2e} {gap:>10.2e} "
                  f"{minnz:>9.4f}  "
                  f"{'CERTIFICATE' if ok else 'none'}", flush=True)
