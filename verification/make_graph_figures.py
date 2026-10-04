"""A picture of the object: the two-vertex base, and the cover it lifts to.

The board carried no drawing of a generalized Petersen graph at all, which is
a strange thing for a board about them.  Worse, the unifying idea of the whole
project -- that P(n,k) is a CYCLIC COVER of a two-vertex base, which is why one
engine answers both halves -- was carried entirely in prose.  It is a picture.

Left panel: the base, two vertices with a loop of voltage 1, a loop of voltage
k and an edge of voltage 0.  Right panel: the lift, with the fibre over each
base vertex drawn in that vertex's colour, so the correspondence is visible.
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
from matplotlib.patches import FancyArrowPatch, Arc

sys.path.insert(0, f"{_REPO}")

OUT = f"{_REPO}/manuscript/figures"
OUTER = "#4b2a7b"      # the fibre over u -- the outer cycle
INNER = "#2a7a6b"      # the fibre over v -- the inner k-step cycle
SPOKE = "#b9b3c6"
BAD = "#c0503c"


def _base(ax, k=2):
    """The two-vertex base B(1,k,0), with its voltages."""
    u, v = (-0.75, 0.0), (0.75, 0.0)
    ax.plot([u[0], v[0]], [u[1], v[1]], color=SPOKE, lw=3.0, zorder=2)
    ax.text(0.0, 0.13, r"$0$", ha="center", fontsize=15, color="#555555")
    # the two loops
    for (cx, cy), col, lab, side in ((u, OUTER, r"$1$", -1), (v, INNER, r"$k$", +1)):
        ax.add_patch(Arc((cx + side * 0.42, cy), 0.84, 0.84, theta1=0, theta2=360,
                         color=col, lw=3.0, zorder=2))
        ax.text(cx + side * 0.95, cy + 0.02, lab, ha="center", va="center",
                fontsize=16, color=col)
    for (cx, cy), col in ((u, OUTER), (v, INNER)):
        ax.plot([cx], [cy], "o", ms=19, color=col, zorder=4)
    ax.text(u[0], u[1] - 0.42, r"$u$", ha="center", fontsize=15)
    ax.text(v[0], v[1] - 0.42, r"$v$", ha="center", fontsize=15)
    ax.set_xlim(-2.1, 2.1)
    ax.set_ylim(-1.15, 1.15)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("the base $B(1,k,0)$: two vertices, three edges,\n"
                 "voltages in $\\mathbb{Z}_n$", fontsize=12.5)


def _cover(ax, n=7, k=2):
    """The lift: outer n-cycle, inner k-step cycle, spokes between fibres."""
    R, r = 1.0, 0.52
    out = [(R * math.cos(2 * math.pi * i / n + math.pi / 2),
            R * math.sin(2 * math.pi * i / n + math.pi / 2)) for i in range(n)]
    inn = [(r * math.cos(2 * math.pi * i / n + math.pi / 2),
            r * math.sin(2 * math.pi * i / n + math.pi / 2)) for i in range(n)]
    for i in range(n):
        ax.plot(*zip(out[i], out[(i + 1) % n]), color=OUTER, lw=2.6, zorder=2)
        ax.plot(*zip(inn[i], inn[(i + k) % n]), color=INNER, lw=2.6, zorder=2)
        ax.plot(*zip(out[i], inn[i]), color=SPOKE, lw=2.0, zorder=1)
    for p in out:
        ax.plot([p[0]], [p[1]], "o", ms=11, color=OUTER, zorder=4)
    for p in inn:
        ax.plot([p[0]], [p[1]], "o", ms=11, color=INNER, zorder=4)
    ax.set_xlim(-1.32, 1.32)
    ax.set_ylim(-1.32, 1.32)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(r"the cover $P(%d,%d)$: each base vertex" "\n"
                 r"lifts to a fibre of $n=%d$" % (n, k, n), fontsize=12.5)


def fig_cover(path=f"{OUT}/fig_cover.pdf"):
    fig, axes = plt.subplots(1, 3, figsize=(11.6, 4.0),
                             gridspec_kw=dict(width_ratios=[1.15, 1, 1]))
    _base(axes[0])
    _cover(axes[1], 7, 2)
    _cover(axes[2], 5, 2)
    axes[2].set_title("$P(5,2)$: the Petersen graph,\none of the "
                      r"$\mathbf{460}$", fontsize=12.5, color=INNER)
    # No connecting arrow: at this aspect ratio it collides with the loop
    # labels, and the panel titles already say which way the lift goes.
    fig.suptitle(r"One engine, because one object: $P(n,k)$ is a cyclic cover "
                 r"of a two-vertex base", fontsize=13.5, y=1.0)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


if __name__ == "__main__":
    print("wrote", fig_cover())
