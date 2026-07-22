"""
Period-1 certificates, reformulated as a coplanarity problem in P^3.

The symbol is F(s) = (s + a) L_k(s) + alpha s + beta, and r is a root iff

    a L_k(r) + alpha r + beta + r L_k(r) = 0.

Define, for each grid value r in Gamma_n,

    w(r) = ( L_k(r),  r,  1,  r L_k(r) )  in R^4,
    p    = ( a, alpha, beta, 1 ).

Then r is a root of F exactly when w(r) . p = 0.  So:

    a period-1 certificate of nullity 2k+2 is a set of k+1 grid values whose
    w-vectors lie on a common hyperplane through the origin of R^4, with the
    hyperplane's normal having nonzero last coordinate.

Two consequences.

1. At most k+1 grid points can be coplanar in this sense (more would give F
   more than deg F roots), so a coplanar set of size k+1 is automatically
   maximal -- a useful self-check.

2. The search becomes O(|Gamma|^3) instead of the O(|Gamma|^4) of scanning
   triples and evaluating F on the whole grid for each.  Fix a PAIR w(i),
   w(j); the normals orthogonal to both form a 2-dimensional space with basis
   p1, p2; and for each further l the normal is pinned to the direction
   (lambda : mu) = ( -(p2.w(l)) : (p1.w(l)) ).  Grouping the l by that
   direction finds every coplanar set through the pair at once.

Candidates found in floating point are then re-verified exactly in Q(zeta_n)
by verification/exact_certifier.py, so tolerance here can only cost recall,
never correctness.
"""
import sys
from collections import defaultdict

import numpy as np


def lucas_poly(k):
    Lprev, Lcur = np.array([2.0]), np.array([1.0, 0.0])
    for _ in range(2, k + 1):
        Lprev, Lcur = Lcur, np.polysub(np.polymul([1.0, 0.0], Lcur), Lprev)
    return Lcur if k >= 1 else Lprev


def grid_indices(n):
    """Distinct grid values with a representative index m, 0 <= m <= n/2."""
    return list(range(0, n // 2 + 1))


def coplanar_sets(n, k, tol=1e-9, want=None, min_size=4):
    """Coplanar sets of grid indices.

    want=None  -> return the LARGEST coplanar sets found (of size >= min_size),
                  which is what determines the maximum attainable nullity:
                  a coplanar set of size j gives F exactly j grid roots, hence
                  nullity 2j when all of them are interior.
    want=j     -> return only sets of size exactly j."""
    ms = grid_indices(n)
    r = np.array([2 * np.cos(2 * np.pi * m / n) for m in ms])
    Lk = lucas_poly(k)
    Lr = np.polyval(Lk, r)
    W = np.column_stack([Lr, r, np.ones_like(r), r * Lr])      # |Gamma| x 4
    # scale rows so the grouping tolerance means the same thing everywhere
    W = W / np.linalg.norm(W, axis=1, keepdims=True)
    N = len(ms)
    found = set()
    best_size = [0]
    for i in range(N):
        for j in range(i + 1, N):
            M = np.vstack([W[i], W[j]])
            # 2-dimensional orthogonal complement of span{W[i], W[j]}
            _, sv, Vt = np.linalg.svd(M)
            if sv[-1] < 1e-12:               # degenerate pair, skip
                continue
            p1, p2 = Vt[2], Vt[3]
            d1 = W @ p1
            d2 = W @ p2
            # direction (lambda : mu) = (-d2 : d1), as a normalised 2-vector
            vec = np.column_stack([-d2, d1])
            nrm = np.linalg.norm(vec, axis=1)
            keep = nrm > 1e-12
            vec = vec / np.where(nrm[:, None] == 0, 1, nrm[:, None])
            # fix the projective sign
            flip = (vec[:, 0] < 0) | ((np.abs(vec[:, 0]) < 1e-14) & (vec[:, 1] < 0))
            vec[flip] *= -1
            key = np.round(vec / max(tol, 1e-12)).astype(np.int64)
            sel = keep.copy()
            sel[i] = sel[j] = False
            idxs = np.flatnonzero(sel)
            need = (want if want is not None else min_size) - 2
            if len(idxs) < need:
                continue
            # bucket by the projective direction, vectorised
            uniq, inv, cnt = np.unique(key[idxs], axis=0, return_inverse=True,
                                       return_counts=True)
            sizes = cnt + 2
            if want is not None:
                sel_b = np.flatnonzero(sizes == want)
            else:
                # keep only the best size seen so far, to bound memory
                hi = sizes.max(initial=0)
                if hi < max(min_size, best_size[0]):
                    continue
                if hi > best_size[0]:
                    best_size[0] = hi
                    found.clear()
                sel_b = np.flatnonzero(sizes == best_size[0])
            for b in sel_b:
                ls = idxs[np.flatnonzero(inv == b)]
                found.add(tuple(sorted([i, j] + ls.tolist())))
    return [tuple(ms[t] for t in f) for f in sorted(found)]


def evaluate(n, k, idx):
    """Recover (a, alpha, beta, c^2) from a coplanar set and score it."""
    r = np.array([2 * np.cos(2 * np.pi * m / n) for m in idx])
    Lk = lucas_poly(k)
    Lr = np.polyval(Lk, r)
    A = np.column_stack([Lr, r, np.ones_like(r)])
    rhs = -r * Lr
    sol, *_ = np.linalg.lstsq(A, rhs, rcond=None)
    resid = np.abs(A @ sol - rhs).max()
    a, alpha, beta = sol
    c2 = a * alpha - beta
    mult = sum(1 if (m == 0 or 2 * m == n) else 2 for m in idx)
    return dict(a=a, alpha=alpha, beta=beta, c2=c2, nullity=mult, resid=resid)


if __name__ == "__main__":
    k = int(sys.argv[1])
    if sys.argv[2] == "list":
        NS = [int(v) for v in sys.argv[3].split(",")]
        nlo, nhi = min(NS), max(NS)
    else:
        NS = None
        nlo, nhi = int(sys.argv[2]), int(sys.argv[3])
    print(f"period-1 coplanar search, k={k}, ceiling {2*k+2}, "
          f"n in [{nlo},{nhi}]", flush=True)
    best_overall, where = 0, []
    ns = NS if NS is not None else range(max(nlo, 2 * k + 3), nhi + 1)
    for n in ns:
        if 2 * k >= n:
            continue
        # fast path: one pass returning the LARGEST coplanar sets.  Only if
        # none of those is realisable (c^2 > 0) do we walk sizes downward.
        best_here = None
        cands = coplanar_sets(n, k)
        hits = [(idx, info) for idx in cands
                for info in [evaluate(n, k, idx)]
                if info["resid"] < 1e-7 and info["c2"] > 1e-9]
        if hits:
            best_here = max(hits, key=lambda h: h[1]["nullity"])
        else:
            top = max((len(c) for c in cands), default=0)
            for want in range(min(k + 1, top - 1), 3, -1):
                hits = [(idx, info) for idx in coplanar_sets(n, k, want=want)
                        for info in [evaluate(n, k, idx)]
                        if info["resid"] < 1e-7 and info["c2"] > 1e-9]
                if hits:
                    best_here = max(hits, key=lambda h: h[1]["nullity"])
                    break
        if best_here is None:
            continue
        idx, info = best_here
        nul = info["nullity"]
        if nul > best_overall:
            best_overall, where = nul, [(n, idx, info)]
        elif nul == best_overall:
            where.append((n, idx, info))
        tag = "   <== reaches 2k+2" if nul == 2 * k + 2 else ""
        print(f"  n={n:4d}: best nullity {nul:3d}{tag}", flush=True)
        if nul == 2 * k + 2:
            print(f"       roots m={idx}  a={info['a']:+.6f} "
                  f"d={info['alpha']:+.6f} c^2={info['c2']:.6f}", flush=True)
    print(f"\nBEST for k={k}: nullity {best_overall} (ceiling {2*k+2})")
    for (n, idx, info) in where[:8]:
        print(f"   n={n}  roots m={idx}  c^2={info['c2']:.6f}")
