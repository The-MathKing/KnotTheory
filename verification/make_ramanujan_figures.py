"""Two figures for the board: the bad bands, and the classification."""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import sys
sys.path.insert(0, f"{_REPO}")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from verification.ramanujan import classify, is_ramanujan, G, bad_bands, SEVEN
from verification.ramanujan_exact import finiteness_bound

OUT = f"{_REPO}/manuscript/figures"
BAD = "#c0503c"
GOOD = "#2a7a6b"
GRID = "#4b2a7b"


def fig_bands(k=3, ns=(32, 33), path=f"{OUT}/fig_bands.pdf"):
    """G_k with its bad bands, then a zoom on where the decision is actually made."""
    fig = plt.figure(figsize=(7.2, 5.6))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.55, 1], hspace=0.42)
    t = np.linspace(0, np.pi, 6000)
    bands = bad_bands(k)

    ax = fig.add_subplot(gs[0])
    ax.plot(t, G(t, k), color="#222222", lw=1.8, zorder=3)
    ax.axhline(SEVEN, color=BAD, lw=1.3, ls="--", zorder=2)
    for a, b in bands:
        ax.axvspan(a, b, color=BAD, alpha=0.22, lw=0, zorder=1)
    ax.set_ylabel(r"$G_k(t)$", fontsize=12)
    ax.set_ylim(-1.5, 9.2)
    ax.set_xlim(0, np.pi)
    ax.set_xticks([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi])
    ax.set_xticklabels(["0", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"])
    ax.text(0.06, SEVEN + 0.35, r"$G_k=7$", color=BAD, fontsize=11)
    ax.set_title(r"$k=%d$: Ramanujan $\Leftrightarrow$ the grid $t=2\pi j/n$ misses every red band"
                 % k, fontsize=12.5)
    ax.grid(alpha=0.22, lw=0.5)

    # The bands are narrow, so the decision is invisible at full scale.  Zoom
    # on the band at pi -- the one that produces the parity law.
    lo = bands[-1][0] - 0.055
    ax2 = fig.add_subplot(gs[1])
    tz = np.linspace(lo, np.pi, 3000)
    ax2.plot(tz, G(tz, k), color="#222222", lw=1.8, zorder=3)
    ax2.axhline(SEVEN, color=BAD, lw=1.3, ls="--", zorder=2)
    for a, b in bands:
        ax2.axvspan(a, b, color=BAD, alpha=0.22, lw=0, zorder=1)
    for n in ns:
        ok = is_ramanujan(n, k)
        js = np.array([2 * np.pi * j / n for j in range(n)])
        js = js[(js >= lo) & (js <= np.pi + 1e-9)]
        col = GOOD if ok else BAD
        for tt in js:
            trivial = abs(tt - np.pi) < 1e-9        # the exempt sample
            ax2.plot([tt], [G(tt, k)], "o", ms=9 if trivial else 7,
                     mfc="white" if trivial else col, mec=col, mew=2.0, zorder=5)
    ax2.set_xlim(lo, np.pi + 0.004)
    ax2.set_ylim(6.55, 7.45)
    ax2.set_xticks([np.pi]); ax2.set_xticklabels([r"$\pi$"])
    ax2.set_ylabel(r"$G_k(t)$", fontsize=12)
    ax2.set_title(r"zoom on the band at $\pi$: $n=%d$ (even) lands ON $\pi$, where the"
                  "\n" r"sample is the trivial $-3$ and is exempt; $n=%d$ (odd) lands "
                  r"just inside" % (ns[0], ns[1]), fontsize=10.5)
    ax2.grid(alpha=0.22, lw=0.5)
    fig.savefig(path, bbox_inches="tight")
    print("wrote", path)


def fig_classification(path=f"{OUT}/fig_ramclass.pdf"):
    """The complete classification: every (n,k), both variables bounded.

    This used to stop at k=10, which was the range the exact certification
    then covered.  It now shows the whole family, because the family is
    finite: nothing survives past k=45, and the picture should say so rather
    than end where the old computation happened to end.
    """
    import numpy as np
    from verification.ramanujan_all_k import is_ramanujan_corner
    kmax, nmax = 48, 120
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    for k in range(1, kmax + 1):
        for n in range(2 * k + 1, nmax + 1):
            ok, _ = is_ramanujan_corner(n, k)
            ax.add_patch(plt.Rectangle((n - 0.5, k - 0.46), 1, 0.92,
                                       color=GOOD if ok else "#e9e9e9", lw=0))
    # The per-k bound B_k is nearly vacuous over this range -- at k=12 it is
    # already off the right edge -- which is precisely the gap the Diophantine
    # argument closes.  Drawing it here would suggest the bound is doing work
    # it is not, so the figure shows what actually bounds the family instead.
    ax.axhline(45.5, color="#a02a2a", lw=1.6, ls="--", zorder=6)
    ax.text(nmax * 0.33, 46.3, r"no $P(n,k)$ with $k>45$ is Ramanujan, for any $n$",
            fontsize=9.5, color="#a02a2a")
    ax.axvline(112.5, color=GRID, lw=1.6, ls="--", zorder=6)
    ax.text(113.5, 6, r"largest is $n=112$", fontsize=9.5, color=GRID,
            rotation=90, va="bottom")
    ax.set_xlim(2, nmax + 1)
    ax.set_ylim(0.3, kmax + 0.7)
    ax.set_yticks(list(range(5, kmax + 1, 5)))
    ax.set_xlabel(r"$n$", fontsize=12)
    ax.set_ylabel(r"$k$", fontsize=12)
    ax.set_title(r"The complete classification: all $460$ Ramanujan $P(n,k)$, "
                 r"decided exactly", fontsize=12.5)
    ax.legend(handles=[Patch(color=GOOD, label="satisfies the RH"),
                       Patch(color="#e9e9e9", label="does not")],
              loc="lower right", fontsize=9.5, framealpha=0.95)
    ax.grid(axis="x", alpha=0.25, lw=0.5)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    print("wrote", path)


if __name__ == "__main__":
    fig_bands()
    fig_classification()
