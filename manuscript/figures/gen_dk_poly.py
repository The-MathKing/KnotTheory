"""
Generate fig_dk_poly.pdf
Shows D_k(u) = (7 + 4u T_k(u))^2 - 8(2u + 2T_k(u))^2 for k=2,3,4.
Forbidden bands (D_k < 0) shaded red; grid sampling shown as dots.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def T(k, u):
    if k == 0: return np.ones_like(u)
    if k == 1: return u
    t0, t1 = np.ones_like(u), u
    for _ in range(k - 1):
        t0, t1 = t1, 2*u*t1 - t0
    return t1

def Dk(k, u):
    tk = T(k, u)
    return (7 + 4*u*tk)**2 - 8*(2*u + 2*tk)**2

fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.8), sharey=False)
fig.patch.set_facecolor('white')

BLUE, RED, GRID_C, BGRAY = '#1a3a6b', '#c0392b', '#27ae60', '#f7f9fc'
u = np.linspace(-1, 1, 6000)
rep_n = {2: 18, 3: 24, 4: 32}
poly_str = {
    2: r'$D_2(u)=64u^6-192u^4-16u^3+112u^2+8u+17$',
    3: r'$D_3(u)=256u^8-896u^6+880u^4-296u^2+49$',
    4: r'$D_4(u)$ — degree-10 integer polynomial',
}

for ax, k in zip(axes, [2, 3, 4]):
    y = Dk(k, u)
    ymax = max(abs(y.min()), y.max()) * 1.22
    ymin_ax = -ymax

    ax.set_facecolor(BGRAY)
    for sp in ax.spines.values():
        sp.set_color('#cccccc'); sp.set_linewidth(0.6)
    ax.axhline(0, color='#555', lw=0.9, zorder=2)
    ax.axvline(-1, color='#aaa', lw=0.7, ls='--', zorder=2)
    ax.axvline( 1, color='#aaa', lw=0.7, ls='--', zorder=2)

    # Forbidden band
    ax.fill_between(u, y, 0, where=(y < 0), color=RED, alpha=0.40,
                    zorder=3, label='Forbidden $(D_k<0)$')
    # D_k curve
    ax.plot(u, y, color=BLUE, lw=2.0, zorder=4, label=f'$D_{k}(u)$')

    # Endpoint annotations
    for uv in [1.0, -1.0]:
        dv = float(Dk(k, np.array([uv]))[0])
        col = RED if dv < 0 else BLUE
        ax.plot(uv, dv, 'o', color=col, ms=6, zorder=6, clip_on=False)
        xoff = -0.14 if uv > 0 else 0.14
        ax.annotate(f'$D_{k}({int(uv)})={int(round(dv))}$',
                    xy=(uv, dv), xytext=(uv + xoff, dv - ymax*0.09),
                    fontsize=6.5, color=col, ha='center', va='top',
                    arrowprops=dict(arrowstyle='-', color=col, lw=0.5))

    # Grid points
    n = rep_n[k]
    js = np.arange(1, n)
    if n % 2 == 0 and k % 2 == 1:
        js = js[js != n // 2]
    gu = np.unique(np.round(np.cos(2*np.pi*js/n), 10))
    gy = Dk(k, gu)
    good, bad = gy >= 0, gy < 0
    ax.scatter(gu[good], gy[good], c=GRID_C, edgecolors='#1a7a3a',
               s=30, zorder=7, label=f'Grid ($n={n}$, passes)')
    if bad.any():
        ax.scatter(gu[bad], gy[bad], c=RED, s=55, marker='x',
                   linewidths=2, zorder=8, label='In band (fails)')

    # Polynomial label at bottom
    ax.text(0, ymin_ax*0.96, poly_str[k], ha='center', va='bottom',
            fontsize=5.6, color='#444', style='italic', clip_on=False)

    ax.set_xlim(-1.08, 1.08)
    ax.set_ylim(ymin_ax, ymax)
    ax.set_xlabel(r'$u=\cos(2\pi j/n)$', fontsize=8.5)
    ax.set_title(f'$k={k}$', fontsize=12, fontweight='bold', color=BLUE, pad=5)
    ax.tick_params(labelsize=7.5, length=3)
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    step = max(10, int(ymax/5/10)*10)
    ax.yaxis.set_major_locator(MultipleLocator(step))
    if k == 2:
        ax.legend(loc='upper left', fontsize=6, framealpha=0.9,
                  ncol=1, borderpad=0.5, handlelength=1.2, edgecolor='#ccc')

fig.suptitle(
    r'$D_k(u)$: the integer polynomial whose nonnegativity decides the '
    r'Riemann Hypothesis for $P(n,k)$'
    '\n'
    r'$D_k(1)=-7$ always $\Rightarrow$ band at $u=1$;'
    r'  $D_k(-1)<0$ iff $k$ odd $\Rightarrow$ parity law',
    fontsize=8.5, y=1.04, color=BLUE, linespacing=1.6)

plt.tight_layout(rect=[0, 0.03, 1, 1])
for ext in ('pdf', 'png'):
    out = f'fig_dk_poly.{ext}'
    plt.savefig(out, bbox_inches='tight', dpi=200)
    print(f'Saved {out}')
