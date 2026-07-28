"""Full pipeline: reach the ceiling numerically, then certify it rigorously.

  stage 1  alternating minimisation on A(w)K = 0 with spokes fixed to 1 and a
           homotopy holding the other edges near +-1 (verification/
           reach_ceiling.py).  Cheap -- each half is a linear solve -- and gets
           within ~1e-4, but converges only linearly.
  stage 2  Newton on the SQUARE structural system (see verification/krawczyk.py
           for why those particular equations).  Quadratic convergence.
  stage 3  Krawczyk contraction test -> a proof that a true real solution exists.

Output: null A = 2k+2 proved, hence M(P(n,k)) = Z(P(n,k)) = 2k+2.
"""
import sys
from fractions import Fraction

import numpy as np
import scipy.linalg as sla
from mpmath import mp, mpf

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from certify_general import pattern_cells, assemble, graph_form, build_K, jac
from gauge_fixed import solve as gf_solve
from krawczyk import resid_mp, L_LIP


def to_full(w1, n, sign):
    """gauge-fixed (a, d, e [, b_0]) -> the (a,d,b,c,e) order of pattern_cells."""
    a, d, e = w1[:n], w1[n:2*n], w1[2*n:3*n]
    b = np.ones(n)
    b[0] = w1[3*n] if n % 2 == 0 else sign
    return np.concatenate([a, d, b, np.ones(n), e])


def certify(n, k, digits=4, tries=40, iters=400, seed=0, verbose=True,
            warm=None):
    """warm = (w_prev, n_prev, sign) from an earlier certified n, or None."""
    r = 2 * k + 2
    N = 2 * n
    if verbose:
        print(f"P({n},{k})   target nullity 2k+2 = {r}")
    from gauge_fixed import resample
    # Stage 1 yields CANDIDATES, and stage 2 is attempted on each in turn.  A
    # warm start that returns a mediocre point (say 1e-3) used to suppress the
    # cold solve and then fail stage 2, losing n that a cold solve certifies.
    cands = []
    if warm is not None:
        wp, npv, sp = warm
        try:
            obj0, me0, w1 = gf_solve(n, k, sign=sp, iters=iters, seed=seed,
                                     w0=resample(wp, npv, n))
            if np.isfinite(obj0):
                cands.append((obj0, me0, w1, sp, f"warm from n={npv}"))
        except Exception:
            pass
    for sign in (+1, -1):
        obj0, me0, w1 = gf_solve(n, k, sign=sign, tries=tries, iters=iters,
                                 seed=seed)
        if np.isfinite(obj0):
            cands.append((obj0, me0, w1, sign, f"cold, sign {sign:+d}"))
    cands.sort(key=lambda c: c[0])
    if not cands:
        if verbose: print("  stage 1 found nothing")
        return False, None, None
    for ci, (obj0, me0, w1, sign, tag) in enumerate(cands):
        if verbose:
            print(f"  stage 1 [{tag}]: r-th sv/scale = {obj0:.3e}, "
                  f"min|inner|/scale = {me0:.4f}")
        ok, info, zn = _finish(n, k, w1, sign, digits, verbose)
        if ok:
            return ok, info, zn
        if verbose and ci + 1 < len(cands):
            print("  -> stage 2/3 failed; trying the next stage-1 candidate")
    return False, None, None


def _finish(n, k, w1, sign, digits, verbose):
    r = 2 * k + 2
    N = 2 * n
    w = to_full(w1, n, sign)
    cells = pattern_cells(n, k)
    nw = len(cells)
    A = assemble(w, cells, N)
    K0 = np.linalg.svd(A)[2][-r:].T
    perm, X = graph_form(K0, r)
    eqs = sorted([perm[r + m] * r + t for m in range(N - r) for t in range(r)]
                 + [perm[s] * r + t for s in range(r) for t in range(r) if s <= t])
    excess = sorted([perm[s] * r + t for s in range(r) for t in range(r) if s > t])
    z = np.concatenate([w, X.ravel()])
    # stage 2: float Newton first, to get into the quadratic regime cheaply
    J = jac(z[:nw], z[nw:].reshape(N - r, r), cells, perm, N, r)
    rk = len(eqs)
    # the gauge fixing pins the outer weights (block b) and the spokes (block c)
    # pinned by the gauge fixing: the spoke block, and the outer block except
    # b_0 when n is even (where one outer weight has to stay free)
    gauge = list(range(3 * n, 4 * n))                      # spokes
    gauge += [i for i in range(2 * n, 3 * n) if not (n % 2 == 0 and i == 2 * n)]
    others = [i for i in range(len(z)) if i not in gauge]
    _, _, Pc = sla.qr(J[np.ix_(eqs, others)], pivoting=True)
    free = sorted(others[i] for i in Pc[:rk])
    fixed = sorted(set(range(len(z))) - set(free))
    assert len(free) == rk, (len(free), rk)
    if verbose:
        print(f"  {len(z)} unknowns, {N*r} equations, {rk} structural, "
              f"{len(excess)} dependent; fixing {len(fixed)} at rationals")
    # Levenberg-Marquardt: undamped Newton diverges from a 1e-3 start
    nu = 1e-3
    Fcur = (assemble(z[:nw], cells, N)
            @ build_K(z[nw:].reshape(N - r, r), perm, N, r)).ravel()[eqs]
    for it in range(300):
        J = jac(z[:nw], z[nw:].reshape(N - r, r), cells, perm, N, r)
        Js = J[np.ix_(eqs, free)]
        g = Js.T @ Fcur
        H = Js.T @ Js
        try:
            step = np.linalg.solve(H + nu * np.diag(np.diag(H) + 1e-12), -g)
        except np.linalg.LinAlgError:
            nu *= 10; continue
        ztry = z.copy(); ztry[free] += step
        Ftry = (assemble(ztry[:nw], cells, N)
                @ build_K(ztry[nw:].reshape(N - r, r), perm, N, r)).ravel()[eqs]
        if np.all(np.isfinite(Ftry)) and np.abs(Ftry).max() < np.abs(Fcur).max():
            z, Fcur, nu = ztry, Ftry, max(nu * 0.3, 1e-14)
        else:
            nu *= 8
            if nu > 1e12: break
        if np.abs(Fcur).max() < 1e-13:
            break
    F = (assemble(z[:nw], cells, N)
         @ build_K(z[nw:].reshape(N - r, r), perm, N, r)).ravel()
    if verbose:
        print(f"  stage 2 (double): max|f| structural = {np.abs(F[eqs]).max():.3e}"
              f", dependent = {np.abs(F[excess]).max():.3e}")
    if np.abs(F[eqs]).max() > 1e-8:
        if verbose: print("  did not converge; stopping")
        return False, None, z
    # stage 2b: high precision, with the fixed unknowns pinned to exact rationals
    mp.dps = 60
    zf = [Fraction(round(float(z[i]) * 10**digits), 10**digits) for i in fixed]
    zc = [mpf(float(v)) for v in z]
    for i, v in zip(fixed, zf):
        zc[i] = mpf(v.numerator) / mpf(v.denominator)
    for it in range(60):
        Fm = resid_mp(zc, cells, perm, N, r, nw)
        zn = np.array([float(x) for x in zc])
        Jn = jac(zn[:nw], zn[nw:].reshape(N - r, r), cells, perm, N, r)
        Fs = np.array([float(Fm[i]) for i in eqs])
        step = np.linalg.solve(Jn[np.ix_(eqs, free)], -Fs)
        for idx, sv in zip(free, step):
            zc[idx] = zc[idx] + mpf(sv)
        if np.abs(Fs).max() < 1e-45:
            break
    Fm = resid_mp(zc, cells, perm, N, r, nw)
    fs = max(abs(Fm[i]) for i in eqs); fe = max(abs(Fm[i]) for i in excess)
    zn = np.array([float(x) for x in zc])
    Jn = jac(zn[:nw], zn[nw:].reshape(N - r, r), cells, perm, N, r)
    Js = Jn[np.ix_(eqs, free)]
    Y = np.linalg.inv(Js)
    Ynorm = np.abs(Y).sum(axis=1).max()
    Fsv = np.array([float(Fm[i]) for i in eqs])
    eta = np.abs(Y @ Fsv).max()
    alpha0 = np.abs(np.eye(rk) - Y @ Js).sum(axis=1).max()
    if verbose:
        print(f"  stage 2b (60 digits): structural {mp.nstr(fs,4)}, "
              f"dependent {mp.nstr(fe,4)}")
        print(f"  ||Y||={Ynorm:.3e}  ||I-YJ||={alpha0:.3e}  ||Yf||={eta:.3e}")
    ok = False
    for delta in [10.0**p for p in range(-13, 0)]:
        alpha = alpha0 + Ynorm * L_LIP * delta
        if alpha < 1 and eta + alpha * delta <= delta:
            ok = True
            if verbose:
                print(f"  stage 3 KRAWCZYK PASSES at delta = {delta:g}: "
                      f"alpha = {alpha:.3e}")
            break
    A2 = assemble(zn[:nw], cells, N)
    sv2 = np.linalg.svd(A2, compute_uv=False)
    nul = int(np.sum(sv2 < 1e-9 * sv2.max()))
    edges = np.abs(np.concatenate([zn[2*n:3*n], zn[3*n:4*n], zn[4*n:5*n]]))
    if verbose:
        print(f"  certified matrix: nullity {nul}, gap "
              f"{sv2[-r-1]/sv2.max():.4f}, min|edge|/scale "
              f"{edges.min()/np.abs(zn[:nw]).max():.4f}")
        print(f"  VERDICT: {'PROVED null A = %d' % r if ok and nul == r else 'NOT proved'}")
    # hand back the gauge-fixed weights so the next n can warm-start from them
    wgf = np.concatenate([zn[:n], zn[n:2*n], zn[4*n:5*n]])
    if n % 2 == 0:
        wgf = np.concatenate([wgf, [zn[2*n]]])
    return ok and nul == r, (wgf, n, sign), zn


if __name__ == "__main__":
    k = int(sys.argv[1])
    for n in [int(x) for x in sys.argv[2:]]:
        certify(n, k)
        print()
