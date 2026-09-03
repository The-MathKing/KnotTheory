"""Certify identity tiles rigorously, upgrading the tiling result to a proof.

The tile condition T_tile = I is a rational map, so a Krawczyk bound on it would
need interval matrix products.  It is not necessary.  By cor:ceiling,
T_tile = I if and only if the CYCLIC matrix built from that single tile on
P(l,k) has nullity 2k+2 -- for a one-tile cycle the monodromy IS the tile
product.  So certifying the tile is certifying a nullity, which the bilinear
A(w)K(X) = 0 machinery already does with an affine Jacobian and a cheap
Lipschitz bound.

The one extra requirement is that the tiles still compose, which needs every
tile to carry the SAME docking pattern.  That is arranged by pinning the
docking weights -- the first and last k+1 positions of each of the five weight
sequences -- at their exact integer values (b = c = e = 1, a = d = 0) rather
than letting the solver move them.  Those entries go into the fixed set, so the
certified solution carries them exactly.

A certified tile of every length in [L, 2L) therefore proves, via
Theorem (tiling), that Z(P(n,k)) = M(P(n,k)) = 2k+2 for every n >= L.
"""
import glob
import os
import sys
from fractions import Fraction

import numpy as np
import scipy.linalg as sla
from mpmath import mp, mpf

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from certify_general import pattern_cells, assemble, graph_form, build_K, jac
from krawczyk import resid_mp, L_LIP
from tiles import dock_weights


def tile_to_full(w, l, k):
    """Interior tile weights -> the 5l vector in pattern_cells order (a,d,b,c,e),
    with the docking pattern written into the first and last k+1 positions."""
    m = k + 1
    nint = l - 2 * m
    D = dock_weights(k)
    seq = {}
    for idx, key in enumerate("bcead"):
        seq[key] = np.concatenate([D[key], w[idx * nint:(idx + 1) * nint], D[key]])
    return np.concatenate([seq["a"], seq["d"], seq["b"], seq["c"], seq["e"]])


def dock_indices(l, k):
    """Positions in the 5l weight vector that the docking pattern pins."""
    m = k + 1
    pos = list(range(m)) + list(range(l - m, l))
    return [blk * l + p for blk in range(5) for p in pos]


def certify_tile(l, k, w_int, digits=6, verbose=True):
    r = 2 * k + 2
    N = 2 * l
    cells = pattern_cells(l, k)
    nw = len(cells)
    w = tile_to_full(w_int, l, k)
    A = assemble(w, cells, N)
    sv0 = np.linalg.svd(A, compute_uv=False)
    K0 = np.linalg.svd(A)[2][-r:].T
    perm, X = graph_form(K0, r)
    eqs = sorted([perm[r + i] * r + t for i in range(N - r) for t in range(r)]
                 + [perm[s] * r + t for s in range(r) for t in range(r) if s <= t])
    excess = sorted([perm[s] * r + t for s in range(r) for t in range(r) if s > t])
    z = np.concatenate([w, X.ravel()])
    rk = len(eqs)
    pinned = dock_indices(l, k)
    others = [i for i in range(len(z)) if i not in pinned]
    J = jac(z[:nw], z[nw:].reshape(N - r, r), cells, perm, N, r)
    _, _, Pc = sla.qr(J[np.ix_(eqs, others)], pivoting=True)
    free = sorted(others[i] for i in Pc[:rk])
    fixed = sorted(set(range(len(z))) - set(free))
    if verbose:
        print(f"  l={l}: {len(z)} unknowns, {N*r} equations, {rk} structural, "
              f"{len(excess)} dependent; {len(pinned)} docking pins, "
              f"{len(fixed)} fixed total")
    # damped Newton in double precision
    nu = 1e-3
    F = (assemble(z[:nw], cells, N)
         @ build_K(z[nw:].reshape(N - r, r), perm, N, r)).ravel()[eqs]
    for _ in range(200):
        J = jac(z[:nw], z[nw:].reshape(N - r, r), cells, perm, N, r)
        Js = J[np.ix_(eqs, free)]
        H = Js.T @ Js
        try:
            step = np.linalg.solve(H + nu * np.diag(np.diag(H) + 1e-12), -Js.T @ F)
        except np.linalg.LinAlgError:
            nu *= 10; continue
        zt = z.copy(); zt[free] += step
        Ft = (assemble(zt[:nw], cells, N)
              @ build_K(zt[nw:].reshape(N - r, r), perm, N, r)).ravel()[eqs]
        if np.all(np.isfinite(Ft)) and np.abs(Ft).max() < np.abs(F).max():
            z, F, nu = zt, Ft, max(nu * 0.3, 1e-14)
        else:
            nu *= 8
            if nu > 1e12: break
        if np.abs(F).max() < 1e-13:
            break
    if np.abs(F).max() > 1e-9:
        if verbose: print(f"    double Newton stalled at {np.abs(F).max():.2e}")
        return False, None
    # high precision, docking and the other fixed unknowns pinned to rationals
    mp.dps = 60
    zf = [Fraction(round(float(z[i]) * 10**digits), 10**digits) for i in fixed]
    zc = [mpf(float(v)) for v in z]
    for i, v in zip(fixed, zf):
        zc[i] = mpf(v.numerator) / mpf(v.denominator)
    for _ in range(60):
        Fm = resid_mp(zc, cells, perm, N, r, nw)
        zn = np.array([float(x) for x in zc])
        Jn = jac(zn[:nw], zn[nw:].reshape(N - r, r), cells, perm, N, r)
        Fs = np.array([float(Fm[i]) for i in eqs])
        try:
            step = np.linalg.solve(Jn[np.ix_(eqs, free)], -Fs)
        except np.linalg.LinAlgError:
            return False, None
        for idx, sv in zip(free, step):
            zc[idx] = zc[idx] + mpf(sv)
        if np.abs(Fs).max() < 1e-45:
            break
    Fm = resid_mp(zc, cells, perm, N, r, nw)
    fs = max(abs(Fm[i]) for i in eqs)
    fe = max(abs(Fm[i]) for i in excess)
    zn = np.array([float(x) for x in zc])
    Jn = jac(zn[:nw], zn[nw:].reshape(N - r, r), cells, perm, N, r)
    Js = Jn[np.ix_(eqs, free)]
    Y = np.linalg.inv(Js)
    Ynorm = np.abs(Y).sum(axis=1).max()
    eta = np.abs(Y @ np.array([float(Fm[i]) for i in eqs])).max()
    alpha0 = np.abs(np.eye(rk) - Y @ Js).sum(axis=1).max()
    ok = False
    for delta in [10.0**p for p in range(-14, 0)]:
        alpha = alpha0 + Ynorm * L_LIP * delta
        if alpha < 1 and eta + alpha * delta <= delta:
            ok = True; break
    A2 = assemble(zn[:nw], cells, N)
    sv2 = np.linalg.svd(A2, compute_uv=False)
    nul = int(np.sum(sv2 < 1e-9 * sv2.max()))
    # confirm the docking pattern survived exactly
    D = dock_weights(k)
    dock_ok = True
    m = k + 1
    for blk, key in enumerate("adbce"):
        for j, p in enumerate(list(range(m)) + list(range(l - m, l))):
            want = D[key][j % m]
            if abs(zn[blk * l + p] - want) > 1e-14:
                dock_ok = False
    edges = np.abs(zn[2*l:5*l]).min() / np.abs(zn[:nw]).max()
    good = ok and nul == r and dock_ok and edges > 1e-3
    if verbose:
        print(f"    structural {mp.nstr(fs,3)}, dependent {mp.nstr(fe,3)}, "
              f"||Y||={Ynorm:.2e}, alpha={alpha:.2e}, nullity {nul}, "
              f"docking exact {dock_ok}, min|edge| {edges:.4f}  "
              f"{'CERTIFIED' if good else 'not certified'}")
    return good, zn


def main():
    k = int(sys.argv[1])
    got, failed = [], []
    files = sorted(glob.glob(f"/Volumes/2TB/scifair/results/zero_forcing/tile_*_{k}.npy"),
                   key=lambda f: int(os.path.basename(f).split("_")[1]))
    print(f"certifying {len(files)} identity tiles at k={k}")
    for f in files:
        l = int(os.path.basename(f).split("_")[1])
        w = np.load(f)
        ok, zn = certify_tile(l, k, w)
        (got if ok else failed).append(l)
        if ok:
            np.save(f"/Volumes/2TB/scifair/results/zero_forcing/"
                    f"tilecert_{l}_{k}.npy", zn)
    print()
    print(f"CERTIFIED tile lengths: {got}")
    print(f"not certified: {failed}")
    if got and got == list(range(min(got), max(got)+1)) and max(got) >= 2*min(got)-1:
        print(f"=> the certified lengths cover [{min(got)}, {2*min(got)}), so "
              f"Z(P(n,{k})) = {2*k+2} is PROVED for every n >= {min(got)}")


if __name__ == "__main__":
    main()
