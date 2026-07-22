"""
Does the whole framework generalise from P(n,k) to arbitrary CYCLIC COVERS?

P(n,k) is a cyclic cover: take a two-vertex base graph B with a loop of
voltage 1 at u, a loop of voltage k at v, and an edge u-v of voltage 0; the
derived graph on V(B) x Z_n is exactly P(n,k).  Nothing in the reduction
argument used the specific voltages -- only that the Z_n action permutes the
fibres.  If that is right, then for ANY base graph B with voltages in Z_n:

  * a matrix carrying the derived graph's pattern and commuting with the
    Z_n action block-diagonalises into n blocks of size |V(B)|;
  * nullity = sum over m of nullity(M_m), where
        M_m[x][y] = sum over edges x->y of weight * omega^(m * voltage);
  * det M(zeta) is a Laurent polynomial whose degree span is determined by the
    voltages, giving a ceiling on the nullity exactly as 2k+2 did.

This script tests those claims on several base graphs, including the one that
reproduces P(n,k), by comparing the block computation against the full
derived-graph matrix built independently.
"""
import sys
import numpy as np


def derived_graph(base_edges, nV, n):
    """base_edges: list of (x, y, voltage).  Returns index maps for the cover
    on V(B) x Z_n, vertex (x,i) -> x*n + i."""
    edges = []
    for (x, y, v) in base_edges:
        for i in range(n):
            j = (i + v) % n
            edges.append((x * n + i, y * n + j))
    return edges, nV * n


def build_full(base_edges, nV, n, wts, diag):
    """Real symmetric matrix on the cover, with weight wts[e] on every lift of
    base edge e and diagonal diag[x] on every lift of base vertex x."""
    N = nV * n
    A = np.zeros((N, N))
    for e, (x, y, v) in enumerate(base_edges):
        for i in range(n):
            j = (i + v) % n
            p, q = x * n + i, y * n + j
            A[p, q] += wts[e]
            A[q, p] += wts[e]
    for x in range(nV):
        for i in range(n):
            A[x * n + i, x * n + i] = diag[x]
    return A


def blocks(base_edges, nV, n, wts, diag):
    out = []
    for m in range(n):
        w = np.exp(2j * np.pi * m / n)
        M = np.zeros((nV, nV), dtype=complex)
        for e, (x, y, v) in enumerate(base_edges):
            M[x, y] += wts[e] * w ** v
            M[y, x] += wts[e] * np.conj(w) ** v
        for x in range(nV):
            M[x, x] += diag[x]
        out.append(M)
    return out


def check(name, base_edges, nV, n, seed=0):
    rng = np.random.default_rng(seed)
    wts = rng.standard_normal(len(base_edges)) + 1.5
    diag = rng.standard_normal(nV)
    A = build_full(base_edges, nV, n, wts, diag)
    lam = np.sort(np.abs(np.linalg.eigvalsh(A)))
    nullA = int(np.sum(lam < 1e-9 * max(np.abs(A).max(), 1)))
    tot = 0
    for M in blocks(base_edges, nV, n, wts, diag):
        ev = np.abs(np.linalg.eigvalsh(M))
        tot += int(np.sum(ev < 1e-9 * max(np.abs(M).max(), 1)))
    # degree span of det M(zeta) as a Laurent polynomial -> the ceiling
    degs = []
    for _ in range(4):
        w2 = rng.standard_normal(len(base_edges)) + 1.5
        d2 = rng.standard_normal(nV)
        th = np.linspace(0.11, 2 * np.pi - 0.13, 60)
        vals = []
        for t in th:
            w = np.exp(1j * t)
            M = np.zeros((nV, nV), dtype=complex)
            for e, (x, y, v) in enumerate(base_edges):
                M[x, y] += w2[e] * w ** v
                M[y, x] += w2[e] * np.conj(w) ** v
            for x in range(nV):
                M[x, x] += d2[x]
            vals.append(np.linalg.det(M))
        vals = np.array(vals)
        # fit a Laurent polynomial sum_{j=-D}^{D} c_j zeta^j
        D = sum(abs(v) for (_, _, v) in base_edges) + nV
        Vm = np.stack([np.exp(1j * j * th) for j in range(-D, D + 1)], axis=1)
        c, *_ = np.linalg.lstsq(Vm, vals, rcond=None)
        nz = np.flatnonzero(np.abs(c) > 1e-8 * max(np.abs(c).max(), 1))
        degs.append((nz.max() - nz.min()) if len(nz) else 0)
    span = max(degs)
    ok = (nullA == tot) and (nullA <= span)
    print(f"  {name:<34} n={n:>3}  nullity(full)={nullA:>3}  "
          f"sum of block nullities={tot:>3}  deg span={span:>3}  "
          f"{'OK' if ok else 'MISMATCH'}")
    return ok, span


if __name__ == "__main__":
    print("Does the block reduction hold for arbitrary cyclic covers?\n")
    bad = 0
    for n in (12, 17, 20):
        for k in (2, 3, 5):
            # base graph reproducing P(n,k): loop voltage 1 at u, k at v, spoke 0
            be = [(0, 0, 1), (1, 1, k), (0, 1, 0)]
            ok, span = check(f"P(n,{k}) as a cyclic cover", be, 2, n)
            bad += (not ok)
    print()
    for n in (13, 16):
        for name, be, nV in [
            ("3-vertex, voltages 1,2,0,0", [(0,0,1),(1,1,2),(2,2,0),(0,1,0),(1,2,0)], 3),
            ("theta graph, voltages 0,1,4", [(0,1,0),(0,1,1),(0,1,4)], 2),
            ("4-vertex mixed voltages",
             [(0,0,1),(1,1,3),(2,2,2),(3,3,5),(0,1,0),(1,2,1),(2,3,0),(3,0,2)], 4),
        ]:
            ok, span = check(name, be, nV, n)
            bad += (not ok)
    print(f"\nblock reduction + ceiling for cyclic covers: "
          f"{'ALL PASS' if bad == 0 else f'{bad} FAILURES'}")
