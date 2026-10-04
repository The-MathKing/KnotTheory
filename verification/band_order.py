"""The order of the kernel recurrence, computed without guessing a state.

For thm:red2 and thm:theta the transfer matrix was built by hand, which meant
choosing the state vector correctly for each shape of base.  On a base carrying
BOTH loops and several connecting edges the two eliminations compete -- the outer
row advances x by p, the inner advances y by q, and when the connecting voltages
reach further than p the orders interleave -- so hand-picking a state stops being
reliable.

This computes the order directly instead.  Solutions of the recurrence on Z,
restricted to a window of W consecutive fibres, satisfy exactly those equations
all of whose indices lie inside the window.  As W grows the nullity of that band
system grows by the ORDER of the recurrence per extra fibre... no: it becomes
CONSTANT, equal to the order, because each new fibre adds as many equations as
unknowns once the window is longer than the coupling width.  So

    order = nullity of the band system, for W large,

and the claim null A <= D is the claim that this constant is at most D.  Nothing
here optimises or samples weights for a purpose; the weights are generic, and a
generic value of a rank is an upper bound for every value of it.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import sys
import numpy as np

sys.path.insert(0, f"{_REPO}/verification")


def band_nullity(p, q, volts, W, seed=0, jitter=True):
    """Nullity of the equations fully inside a window of W fibres.

    Unknowns: x_0..x_{W-1}, y_0..y_{W-1}.  Rows included only when every index
    they touch lies in [0, W).
    """
    rng = np.random.default_rng(seed)
    a = rng.standard_normal(W + 40) + 1.7
    d = rng.standard_normal(W + 40) + 1.3
    b = rng.standard_normal(W + 40) + 1.9
    e = rng.standard_normal(W + 40) + 2.1
    ws = [rng.standard_normal(W + 40) + 1.5 + 0.3 * r for r in range(len(volts))]
    rows = []

    def X(i):
        return i
    def Y(i):
        return W + i

    for i in range(W):
        # row at u_i : a x_i + b' x_{i-p} + b x_{i+p} + sum_r w^r y_{i+t_r}
        idx = [i] + ([i - p, i + p] if p else []) + [i + t for t in volts]
        if all(0 <= u < W for u in idx):
            row = np.zeros(2 * W)
            row[X(i)] += a[i]
            if p:
                row[X(i - p)] += b[i - p]
                row[X(i + p)] += b[i]
            for r, t in enumerate(volts):
                row[Y(i + t)] += ws[r][i]
            rows.append(row)
        # row at v_j : d y_j + e' y_{j-q} + e y_{j+q} + sum_r w^r_{j-t_r} x_{j-t_r}
        j = i
        idx = [j] + ([j - q, j + q] if q else []) + [j - t for t in volts]
        if all(0 <= u < W for u in idx):
            row = np.zeros(2 * W)
            row[Y(j)] += d[j]
            if q:
                row[Y(j - q)] += e[j - q]
                row[Y(j + q)] += e[j]
            for r, t in enumerate(volts):
                row[X(j - t)] += ws[r][j - t]
            rows.append(row)
    if not rows:
        return 2 * W
    R = np.array(rows)
    s = np.linalg.svd(R, compute_uv=False)
    tol = max(R.shape) * s.max() * 1e-12 if s.size else 0.0
    return 2 * W - int(np.sum(s > tol))


def order(p, q, volts, seed=0):
    """The order: band nullity once it stops growing with W."""
    span = max([p, q] + [abs(t) for t in volts]) if volts else max(p, q)
    prev = None
    for W in range(4 * span + 6, 4 * span + 26, 2):
        nul = band_nullity(p, q, volts, W, seed=seed)
        if prev is not None and nul == prev:
            return nul
        prev = nul
    return prev


def span_D(p, q, volts):
    """Degree span of det M(zeta), computed numerically by interpolation."""
    V = max([p, q] + [abs(t) for t in volts]) * 2 + 4
    N = 8 * V
    rng = np.random.default_rng(1)
    a, d, b, e = rng.standard_normal(4) + 2.0
    w = rng.standard_normal(len(volts)) + 1.5
    vals = np.empty(N, dtype=complex)
    for k in range(N):
        z = np.exp(2j * np.pi * k / N)
        f = sum(w[r] * z ** t for r, t in enumerate(volts))
        M11 = a + (b * (z ** p + z ** -p) if p else 0)
        M22 = d + (e * (z ** q + z ** -q) if q else 0)
        vals[k] = M11 * M22 - f * np.conj(f if abs(abs(z) - 1) < 1e-12 else f)
    coef = np.fft.ifft(vals * np.exp(-2j * np.pi * V * np.arange(N) / N))
    nz = np.where(np.abs(coef) > 1e-8 * np.abs(coef).max())[0]
    return int(nz.max() - nz.min())
