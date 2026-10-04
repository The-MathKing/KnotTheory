"""The corner square, and the deficit design curve.

fig_corner consolidates what fig_bands, fig_dk_poly and fig_ramclass showed
separately.  Those three are per-k pictures: a polynomial for one k, its bands
for one k, a table of which n survive for each k.  The corner form removes k
from the geometry, so one picture now carries the whole criterion -- the four
forbidden lenses are the same for every k, and only the map into the square
changes.  Ramanujan becomes a visible question: does the orbit hit a corner?

fig_deficit answers the question the classification leaves an engineer with.
A no-go theorem says "you cannot have an optimal expander at this size"; the
deficit says how much is actually lost, which is a number you can design
against.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import math
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, f"{_REPO}")

OUT = f"{_REPO}/manuscript/figures"
SQRT2 = math.sqrt(2.0)
THR = 2 * SQRT2
TAU = 3 - 2 * SQRT2

BAD = "#c0503c"
GOOD = "#2a7a6b"
GRID = "#4b2a7b"


def Q(x, y):
    return 4 * x * x + 4 * y * y - 8 * SQRT2 * np.abs(x * y) + 3


def orbit(n, k):
    """The n-1 image points, and which index is the exempt trivial one.

    The criterion exempts the trivial eigenvalues, and the exemption is not
    cosmetic: at a bipartite cover the index j = n/2 lands exactly on the corner
    (-1,+1), inside a lens, and is forgiven.  That single exemption is the whole
    parity law -- it is why bipartiteness HELPS -- so the figure marks the point
    rather than deleting it.
    """
    j = np.arange(1, n)
    x = np.cos(np.pi * j * (k + 1) / n)
    y = np.cos(np.pi * j * (k - 1) / n)
    al = 2 * np.cos(2 * np.pi * j / n)
    be = 2 * np.cos(2 * np.pi * j * k / n)
    exempt = (np.abs(al + 2) < 1e-9) & (np.abs(be + 2) < 1e-9)
    return x, y, exempt


def _lenses(ax, lo=-1.02, hi=1.02, res=1400):
    g = np.linspace(lo, hi, res)
    X, Y = np.meshgrid(g, g)
    Z = Q(X, Y)
    ax.contourf(X, Y, Z, levels=[-10, 0], colors=[BAD], alpha=0.85, zorder=2)
    ax.contour(X, Y, Z, levels=[0], colors=[BAD], linewidths=0.9, zorder=3)


def fig_corner(cases=((112, 41, True), (113, 41, False)),
               path=f"{OUT}/fig_corner.pdf"):
    """The k-free criterion: one square, four lenses, the orbit on top.

    Two columns (a Ramanujan cover and one that just misses), two rows (the
    whole square, then the corner where the decision is actually made).  The
    zoom is a row rather than an inset because the orbit fills the square, so
    an inset necessarily covers data.
    """
    fig, axes = plt.subplots(2, 2, figsize=(9.6, 8.4),
                             gridspec_kw=dict(height_ratios=[1, 1]))
    for col, (n, k, expect) in enumerate(cases):
        ax, az = axes[0][col], axes[1][col]
        xs, ys, exempt = orbit(n, k)
        q = Q(xs, ys)
        inside = (q < 0) & ~exempt
        plain = ~inside & ~exempt

        _lenses(ax)
        ax.scatter(xs[plain], ys[plain], s=15, color=GRID, zorder=4,
                   linewidths=0, label="orbit point, admissible")
        if exempt.any():
            ax.scatter(xs[exempt], ys[exempt], s=70, facecolors="none",
                       edgecolors="#222222", linewidths=1.4, zorder=7,
                       label=r"exempt: the trivial $-3$")
        if inside.any():
            ax.scatter(xs[inside], ys[inside], s=95, color="#ffdd00",
                       edgecolors="#000000", linewidths=1.1, zorder=6,
                       marker="*", label="in a lens: not Ramanujan")
        ax.set_xlim(-1.04, 1.04)
        ax.set_ylim(-1.04, 1.04)
        ax.set_aspect("equal")
        ax.set_xlabel(r"$x=\cos\frac{\pi j(k+1)}{n}$", fontsize=11)
        ax.set_ylabel(r"$y=\cos\frac{\pi j(k-1)}{n}$", fontsize=11)
        verdict = "Ramanujan" if expect else "not Ramanujan"
        ax.set_title(r"$P(%d,%d)$: %s" % (n, k, verdict), fontsize=13,
                     color=GOOD if expect else BAD)
        ax.grid(alpha=0.18, lw=0.5, zorder=0)
        ax.legend(loc="lower left", fontsize=8.2, framealpha=0.93)

        # Which corner decides it, and a zoom there.  A small pad keeps a
        # marker sitting exactly on the corner from being clipped in half.
        cx, cy = 1.0, 1.0
        focus = inside if inside.any() else (exempt if exempt.any() else None)
        if focus is not None:
            i = int(np.argmax(focus))
            cx = float(np.sign(xs[i])) or 1.0
            cy = float(np.sign(ys[i])) or 1.0
        w, pad = 0.15, 0.012
        xlo, xhi = max(-1.0 - pad, cx - w), min(1.0 + pad, cx + w)
        ylo, yhi = max(-1.0 - pad, cy - w), min(1.0 + pad, cy + w)
        X, Y = np.meshgrid(np.linspace(xlo, xhi, 700),
                           np.linspace(ylo, yhi, 700))
        Z = Q(X, Y)
        az.contourf(X, Y, Z, levels=[-10, 0], colors=[BAD], alpha=0.85, zorder=2)
        az.contour(X, Y, Z, levels=[0], colors=[BAD], linewidths=1.1, zorder=3)
        sel = (xs >= xlo) & (xs <= xhi) & (ys >= ylo) & (ys <= yhi)
        az.scatter(xs[sel & plain], ys[sel & plain], s=34, color=GRID,
                   linewidths=0, zorder=4)
        if (sel & exempt).any():
            az.scatter(xs[sel & exempt], ys[sel & exempt], s=210,
                       facecolors="none", edgecolors="#222222",
                       linewidths=2.0, zorder=7)
        if (sel & inside).any():
            az.scatter(xs[sel & inside], ys[sel & inside], s=260,
                       color="#ffdd00", edgecolors="#000000", linewidths=1.3,
                       zorder=6, marker="*")
        az.set_xlim(xlo, xhi)
        az.set_ylim(ylo, yhi)
        az.set_aspect("equal")
        az.grid(alpha=0.18, lw=0.5, zorder=0)
        az.set_xlabel("$x$", fontsize=10)
        az.set_ylabel("$y$", fontsize=10)
        note = (r"the exempt point sits in the lens -- this is the parity law"
                if not inside.any() else
                r"%d orbit points land in a lens" % int(inside.sum()))
        az.set_title("zoom on the corner $(%+d,%+d)$" "\n" "%s"
                     % (cx, cy, note), fontsize=10.2)

    fig.suptitle(r"$Q(x,y)=4x^2+4y^2-8\sqrt{2}\,|xy|+3 \geq 0$"
                 "\n"
                 r"one criterion, four fixed lenses, the same for every $k$",
                 fontsize=13.4, y=0.985)
    fig.tight_layout(rect=[0, 0, 1, 0.935])
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def lam2(n, k):
    """The largest nontrivial |eigenvalue|, from the 2x2 character blocks."""
    worst = 0.0
    for j in range(n):
        al = 2 * math.cos(2 * math.pi * j / n)
        be = 2 * math.cos(2 * math.pi * j * k / n)
        d = math.sqrt((al - be) ** 2 + 4)
        for lam in ((al + be + d) / 2, (al + be - d) / 2):
            if abs(lam - 3) < 1e-9 or abs(lam + 3) < 1e-9:
                continue
            worst = max(worst, abs(lam))
    return worst


def deficit_curve(nmax=240):
    """delta*(n) = min over k of lambda_2(P(n,k)) - 2 sqrt2, and the argmin."""
    ns, ds, ks = [], [], []
    for n in range(3, nmax + 1):
        best = None
        for k in range(1, (n + 1) // 2):
            if 2 * k >= n:
                continue
            d = lam2(n, k) - THR
            if best is None or d < best[0]:
                best = (d, k)
        ns.append(n)
        ds.append(best[0])
        ks.append(best[1])
    return np.array(ns), np.array(ds), np.array(ks)


def fig_deficit(nmax=240, path=f"{OUT}/fig_deficit.pdf"):
    """What the no-go theorem costs, as a function of size."""
    ns, ds, ks = deficit_curve(nmax)
    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    neg = ds < 0
    ax.axhline(0, color=GOOD, lw=1.4, zorder=3)
    ax.axhline(TAU, color="#444444", lw=1.2, ls=":", zorder=3)
    # No connecting line: delta* alternates hard with the parity of n, so a
    # line reads as noise rather than as the trend it is drawn to show.
    ax.scatter(ns[neg], ds[neg], s=17, color=GOOD, zorder=5,
               label=r"optimal member exists ($\delta^*\leq 0$)")
    ax.scatter(ns[~neg], ds[~neg], s=17, color=BAD, zorder=5,
               label=r"no optimal member ($\delta^*>0$)")
    last = int(ns[neg].max())
    ax.axvline(last, color=GOOD, lw=0.9, ls="--", alpha=0.8, zorder=2)
    ax.annotate(r"last Ramanujan size, $n=%d$" % last,
                xy=(last, -0.012), xytext=(last + 14, -0.105), fontsize=10,
                color=GOOD,
                arrowprops=dict(arrowstyle="->", color=GOOD, lw=1.0))
    ax.text(6, TAU + 0.006,
            r"asymptote $3-2\sqrt{2}=%.4f$: the most that can be lost" % TAU,
            fontsize=9.8, color="#333333")
    ax.set_xlabel(r"$n$ (the cover has $2n$ vertices)", fontsize=11)
    ax.set_ylabel(r"$\delta^*(n)=\min_k\ \lambda_2(P(n,k))-2\sqrt{2}$", fontsize=11)
    ax.set_title("The deficit: what is lost by building at a size where no "
                 "optimal member exists", fontsize=12.3)
    ax.set_ylim(-0.30, TAU + 0.030)
    ax.set_xlim(0, nmax + 3)
    ax.grid(alpha=0.22, lw=0.5)
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path, last, float(ds.max()), int(neg.sum())


if __name__ == "__main__":
    print("wrote", fig_corner())
    p, last, mx, cnt = fig_deficit()
    print("wrote", p)
    print("  last Ramanujan size n = %d; %d sizes admit one; max deficit %.6f "
          "(< tau = %.6f)" % (last, cnt, mx, TAU))
