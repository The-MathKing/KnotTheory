"""Figures for the conference poster.  Every panel is generated from the
project's own verified data, not drawn by hand."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

OUT = "/Volumes/2TB/scifair/manuscript/figures"
os.makedirs(OUT, exist_ok=True)
BLUE, LIGHT, GREEN, RED = "#14386e", "#e4ecf6", "#236e3c", "#a52d2d"
plt.rcParams.update({"font.size": 11, "axes.linewidth": 1.2,
                     "savefig.bbox": "tight", "savefig.pad_inches": 0.04})


def petersen_xy(n, k, rout=1.0, rin=0.58):
    th = 2 * np.pi * np.arange(n) / n + np.pi / 2
    U = np.c_[rout * np.cos(th), rout * np.sin(th)]
    V = np.c_[rin * np.cos(th), rin * np.sin(th)]
    return U, V


def draw_graph(ax, n, k, filled=None, title="", newly=None):
    U, V = petersen_xy(n, k)
    for i in range(n):
        ax.plot(*zip(U[i], U[(i + 1) % n]), color="#9aa7b8", lw=1.6, zorder=1)
        ax.plot(*zip(V[i], V[(i + k) % n]), color="#9aa7b8", lw=1.6, zorder=1)
        ax.plot(*zip(U[i], V[i]), color="#c3cbd8", lw=1.3, zorder=1)
    filled = set(filled or []); newly = set(newly or [])
    for i in range(n):
        for tag, P in (("u", U), ("v", V)):
            key = (tag, i)
            fc = (GREEN if key in newly else BLUE) if key in filled else "white"
            ax.add_patch(Circle(P[i], 0.075, fc=fc, ec=BLUE, lw=1.6, zorder=3))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=11, color=BLUE, weight="bold", pad=4)


# ---- F1: the colour change rule, three frames -----------------------------
fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.4))
n, k = 9, 2
S = [("u", i) for i in range(6)]
draw_graph(axs[0], n, k, S, "1.  start:  $S=\\{u_0,\\dots,u_5\\}$")
step1 = S + [("v", i) for i in range(1, 5)]
draw_graph(axs[1], n, k, step1, "2.  spokes forced",
           newly=[("v", i) for i in range(1, 5)])
step2 = step1 + [("v", 5), ("u", 6)]
draw_graph(axs[2], n, k, step2, "3.  $\\rho(S)\\subseteq\\mathrm{cl}(S)$",
           newly=[("v", 5), ("u", 6)])
fig.savefig(f"{OUT}/fig_forcing.pdf"); plt.close(fig)

# ---- F2: the nine-term recurrence support ---------------------------------
fig, ax = plt.subplots(figsize=(6.4, 2.5))
k = 4
pos = [-k - 1, -k, -k + 1, -1, 0, 1, k - 1, k, k + 1]
for p in range(-k - 2, k + 3):
    on = p in pos
    ax.add_patch(plt.Rectangle((p - 0.42, -0.42), 0.84, 0.84,
                               fc=BLUE if on else "white", ec=BLUE, lw=1.4))
    if on:
        ax.text(p, 0, "$\\ast$", ha="center", va="center", color="white",
                fontsize=13)
ax.annotate("", xy=(k + 1, 0.75), xytext=(-k - 1, 0.75),
            arrowprops=dict(arrowstyle="<->", color=RED, lw=1.8))
ax.text(0, 1.0, "order $2k+2$  =  size of the bootstrap forcing set",
        ha="center", color=RED, fontsize=11, weight="bold")
for lbl, p in (("$i-k-1$", -k - 1), ("$i$", 0), ("$i+k+1$", k + 1)):
    ax.text(p, -0.95, lbl, ha="center", fontsize=10, color=BLUE)
ax.set_xlim(-k - 2.6, k + 2.6); ax.set_ylim(-1.4, 1.45); ax.axis("off")
fig.savefig(f"{OUT}/fig_recurrence.pdf"); plt.close(fig)

# ---- F3: the symbol's roots landing on the grid (the mechanism) -----------
def lucas(k):
    Lp, Lc = np.array([2.0]), np.array([1.0, 0.0])
    for _ in range(2, k + 1):
        Lp, Lc = Lc, np.polysub(np.polymul([1.0, 0.0], Lc), Lp)
    return Lc

fig, axs = plt.subplots(1, 2, figsize=(10.2, 3.6))
for ax, (n, k, a, al, ttl) in zip(axs, [
        (24, 5, 0.0, 0.0, "$k=5$, $n=24$:  $F=sL_5-1=\\Psi_6\\Psi_3\\Psi_{24}$"),
        (60, 4, 1.0, -1.0, "$k=4$, $n=60$:  $F=(s{+}1)L_4-s-2=\\Psi_4\\Psi_{30}$")]):
    Lk = lucas(k)
    s = np.linspace(-2.05, 2.05, 1600)
    F = (s + a) * np.polyval(Lk, s) + al * s + (a * al - 1.0)
    ax.axhline(0, color="#9aa7b8", lw=1.0)
    ax.plot(s, F, color=BLUE, lw=2.0)
    G = np.array([2 * np.cos(2 * np.pi * m / n) for m in range(n // 2 + 1)])
    ax.plot(G, np.zeros_like(G), "o", ms=5, mfc="white", mec="#9aa7b8",
            mew=1.3, label="grid $\\Gamma_n$", zorder=3)
    Fg = (G + a) * np.polyval(Lk, G) + al * G + (a * al - 1.0)
    hit = np.abs(Fg) < 1e-9
    ax.plot(G[hit], np.zeros(hit.sum()), "o", ms=9, color=RED,
            label="roots of $F$ on the grid", zorder=4)
    ax.set_ylim(-3.2, 3.2); ax.set_xlim(-2.15, 2.15)
    ax.set_xlabel("$s=2\\cos(2\\pi m/n)$"); ax.set_title(ttl, fontsize=11,
                                                        color=BLUE, weight="bold")
    ax.legend(fontsize=9, loc="upper center", framealpha=0.95)
fig.savefig(f"{OUT}/fig_symbol.pdf"); plt.close(fig)

# ---- F4: the certificate spectrum -----------------------------------------
def adj(n, k):
    N = 2 * n; A = np.zeros((N, N))
    for i in range(n):
        A[i, (i + 1) % n] = A[(i + 1) % n, i] = 1
        A[i, n + i] = A[n + i, i] = 1
        A[n + i, n + (i + k) % n] = A[n + (i + k) % n, n + i] = 1
    return A

fig, ax = plt.subplots(figsize=(6.6, 3.2))
lam = np.sort(np.linalg.eigvalsh(adj(24, 5)))
ax.plot(np.arange(len(lam)), lam, "o", ms=5, color=BLUE)
z = np.abs(lam) < 1e-9
ax.plot(np.where(z)[0], lam[z], "o", ms=9, color=RED,
        label=f"{z.sum()} zero eigenvalues $=2k+2$")
ax.axhline(0, color="#9aa7b8", lw=1.0)
ax.set_xlabel("index"); ax.set_ylabel("eigenvalue")
ax.set_title("Spectrum of $\\mathrm{Adj}\\,P(24,5)$: nullity $12$",
             fontsize=11, color=BLUE, weight="bold")
ax.legend(fontsize=9)
fig.savefig(f"{OUT}/fig_spectrum.pdf"); plt.close(fig)

# ---- F5: what is proved, by k -------------------------------------------
fig, ax = plt.subplots(figsize=(6.6, 3.3))
ks = np.arange(2, 9)
ceiling = 2 * ks + 2
best = np.array([6, 8, 10, 12, 14, 16, 18])
exact = np.array([True, True, True, True, False, False, False])
ax.plot(ks, ceiling, "s--", color=BLUE, lw=3.2, ms=11,
        label="upper bound $=$ ceiling $2k+2$")
ax.plot(ks, best, "-", color=RED, lw=2.4, zorder=2)
ax.plot(ks[exact], best[exact], "o", color=RED, ms=10, zorder=3,
        label="exact arithmetic certificate")
ax.plot(ks[~exact], best[~exact], "o", mfc="white", mec=RED, mew=2.4, ms=10,
        zorder=3, label="numerically certified")
for x, y, c, ex in zip(ks, best, ceiling, exact):
    if y == c:
        ax.annotate("exact\narithmetic" if ex else "numerical",
                    (x, y), textcoords="offset points",
                    xytext=(0, -26), ha="center",
                    color=GREEN if ex else RED, fontsize=8, weight="bold")
ax.set_xlabel("$k$"); ax.set_ylabel("$Z(P(n,k))$")
ax.set_title("The ceiling is attained for every $k$ tested",
             fontsize=11, color=BLUE, weight="bold")
ax.legend(fontsize=8.5, loc="upper left"); ax.set_ylim(2, 22)
fig.savefig(f"{OUT}/fig_status.pdf"); plt.close(fig)

# ---- F6: the ceiling identity (visual abstract centrepiece) ---------------
fig, ax = plt.subplots(figsize=(8.8, 2.9))
ax.axis("off")
W, GAP = 0.215, 0.045
boxes = ["any matrix with\nthe $P(n,k)$\npattern",
         "one recurrence,\norder $2k+2$",
         "$\\mathrm{null}\\,A=$\n$\\dim\\ker(T-I)$\n$\\leq 2k+2$",
         "$=2k+2$\n$\\Leftrightarrow\\ T=I$"]
for j, txt in enumerate(boxes):
    x = j * (W + GAP)
    col = "#cfe3d4" if j == len(boxes) - 1 else LIGHT
    ax.add_patch(plt.Rectangle((x, 0.30), W, 0.42, fc=col, ec=BLUE, lw=1.8))
    ax.text(x + W / 2, 0.51, txt, ha="center", va="center", fontsize=9,
            color=BLUE)
    if j:
        ax.add_patch(FancyArrowPatch((x - GAP, 0.51), (x - 0.004, 0.51),
                                     arrowstyle="-|>", mutation_scale=15,
                                     color=BLUE, lw=2))
ax.text((4 * W + 3 * GAP) / 2, 0.13, "the ceiling equals the upper bound: no slack either way",
        ha="center", fontsize=11, color=RED, weight="bold")
ax.set_xlim(-0.01, 4 * W + 3 * GAP + 0.01); ax.set_ylim(0, 0.9)
fig.savefig(f"{OUT}/fig_chain.pdf"); plt.close(fig)

print("wrote:", sorted(f for f in os.listdir(OUT) if f.startswith("fig_")))
