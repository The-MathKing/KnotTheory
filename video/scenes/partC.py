from lib import *
import numpy as np

WHITE_V = "#2b2f3a"   # unfilled vertex fill
BLUE_V  = BLUE

def vdot(p, filled=False, r=0.13):
    return Dot(p, radius=r, color=BLUE_V if filled else WHITE_V, stroke_color=INK, stroke_width=2)

def force_seq(scene, dots, order, rt=0.5, extra=None):
    """Animate forcing: order is list of (from_idx, to_idx)."""
    for a, b in order:
        arr = Arrow(dots[a].get_center(), dots[b].get_center(), buff=0.15, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        scene.play(GrowArrow(arr), run_time=rt*0.5)
        scene.play(dots[b].animate.set_color(BLUE_V), FadeOut(arr), run_time=rt*0.5)

# ---------------------------------------------------------------- S17
class S17(BeatScene):
    SCENE_ID = 'S17'
    def construct(self):
        rule = VGroup(Text("Colour change rule", font_size=34, weight=BOLD, color=YELLOW),
                      Text("a blue vertex with exactly one white neighbour forces it blue", font_size=26)).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.5)
        # small star example
        c = DOWN*0.6
        pts = [c, c+UP*1.5, c+LEFT*1.5, c+RIGHT*1.5]
        ed = VGroup(*[Line(pts[0], p, color=MUTED, stroke_width=3) for p in pts[1:]])
        dd = [vdot(p) for p in pts]
        dd[0].set_color(BLUE_V); dd[1].set_color(BLUE_V); dd[2].set_color(BLUE_V)
        self.hold(1, ([Write(rule)], 2), ([Create(ed), *[FadeIn(d) for d in dd]], 1.5), ([], 1.0))
        force_seq(self, dd, [(0, 3)], rt=1.2)
        zdef = MathTex(r"Z(G)=\min\{|S|:\ S\ \text{forces everything}\}", font_size=40).next_to(rule, DOWN, buff=0.7)
        self.hold(2, ([FadeOut(ed), *[FadeOut(d) for d in dd]], 0.5), ([Write(zdef)], 2.5))
        # path
        pp = [LEFT*4 + RIGHT*1.6*i + DOWN*0.8 for i in range(6)]
        pe = VGroup(*[Line(pp[i], pp[i+1], color=MUTED, stroke_width=3) for i in range(5)])
        pd = [vdot(p) for p in pp]; pd[0].set_color(BLUE_V)
        pl = MathTex(r"Z(P_6)=1", font_size=36, color=GREEN).next_to(pe, DOWN, buff=0.6)
        self.hold(3, ([Create(pe), *[FadeIn(d) for d in pd]], 1.5))
        force_seq(self, pd, [(i, i+1) for i in range(5)], rt=0.7)
        self.play(Write(pl), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(pe), *[FadeOut(d) for d in pd], FadeOut(pl), run_time=0.6)
        # cycle
        cc = DOWN*0.9; R = 1.6; m = 8
        cp = [cc + R*np.array([np.cos(PI/2+2*PI*i/m), np.sin(PI/2+2*PI*i/m), 0]) for i in range(m)]
        ce = VGroup(*[Line(cp[i], cp[(i+1)%m], color=MUTED, stroke_width=3) for i in range(m)])
        cd = [vdot(p) for p in cp]; cd[0].set_color(BLUE_V)
        stuck = Text("stuck: two white neighbours", font_size=26, color=RED).next_to(ce, RIGHT, buff=0.8)
        self.hold(4, ([Create(ce), *[FadeIn(d) for d in cd]], 1.5), ([FadeIn(stuck)], 1.5), ([cd[1].animate.set_color(BLUE_V), FadeOut(stuck)], 1))
        force_seq(self, cd, [(1, 2), (0, 7), (2, 3), (7, 6), (3, 4), (6, 5)], rt=0.5)
        cl = MathTex(r"Z(C_8)=2", font_size=36, color=GREEN).next_to(ce, RIGHT, buff=0.8)
        self.play(Write(cl), run_time=1)
        self.hold(5, ([FadeOut(ce), *[FadeOut(d) for d in cd], FadeOut(cl)], 0.6),
                  ([FadeIn(VGroup(Text("quantum control: which spin systems can be steered from few sites", font_size=26),
                                  Text("power grids: fewest phasor measurement units that determine the state", font_size=26)).arrange(DOWN, buff=0.3).shift(DOWN*0.8))], 3))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S18
class S18(BeatScene):
    SCENE_ID = 'S18'
    def construct(self):
        t = MathTex(r"A_{xy}\ne0\iff xy\in E\ (x\ne y),\qquad \text{diagonal free}", font_size=36).to_edge(UP, buff=0.6)
        e1 = MathTex(r"Ax=0,\qquad x|_B=0", font_size=40).next_to(t, DOWN, buff=0.6)
        self.hold(1, ([Write(t)], 2.5), ([Write(e2 := e1)], 2))
        # local picture
        c = DOWN*1.2 + LEFT*3.5
        pu = c; pw = c + RIGHT*2.0; pv1 = c + UP*1.4 + LEFT*1.0; pv2 = c + DOWN*1.4 + LEFT*1.0
        ed = VGroup(Line(pu, pw, color=MUTED, stroke_width=3), Line(pu, pv1, color=MUTED, stroke_width=3), Line(pu, pv2, color=MUTED, stroke_width=3))
        du = vdot(pu, True); dw = vdot(pw); dv1 = vdot(pv1, True); dv2 = vdot(pv2, True)
        lab = VGroup(MathTex("u", font_size=30).next_to(du, DOWN, buff=0.15), MathTex("w", font_size=30).next_to(dw, DOWN, buff=0.15))
        row = MathTex(r"A_{uu}x_u+\sum_{v\sim u}A_{uv}x_v=0", font_size=38).shift(RIGHT*2.5+DOWN*0.4)
        row2 = MathTex(r"\Rightarrow\ A_{uw}\,x_w=0,\quad A_{uw}\ne0\ \Rightarrow\ x_w=0", font_size=36, color=GREEN).next_to(row, DOWN, buff=0.5)
        self.hold(2, ([Create(ed), FadeIn(du), FadeIn(dw), FadeIn(dv1), FadeIn(dv2), FadeIn(lab)], 1.5), ([Write(row)], 2.5), ([Write(row2)], 3), ([dw.animate.set_color(BLUE_V)], 1))
        e3 = Text("blue = kernel vector known to vanish there", font_size=28, color=BLUE).next_to(row2, DOWN, buff=0.6)
        e4 = MathTex(r"S\ \text{zero forcing},\ x|_S=0\ \Rightarrow\ x=0", font_size=36).next_to(e3, DOWN, buff=0.4)
        self.hold(3, ([FadeIn(e3)], 2), ([Write(e4)], 2.5))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)
        big = MathTex(r"\operatorname{null}A\ \le\ Z(G)\quad\text{for every }A\text{ with the pattern}", font_size=44, color=YELLOW).shift(UP*1.5)
        mz = MathTex(r"M(G)=\max_{A\ \text{sym.}}\operatorname{null}A\ \le\ Z(G)", font_size=44).next_to(big, DOWN, buff=0.7)
        pay = VGroup(Text("upper bound on Z: exhibit one forcing set (easy)", font_size=28, color=MUTED),
                     Text("lower bound on Z: exclude every smaller set (brutal)", font_size=28, color=MUTED),
                     Text("…or exhibit one matrix of large nullity. A certificate.", font_size=30, color=GREEN)).arrange(DOWN, buff=0.3).next_to(mz, DOWN, buff=0.8)
        self.hold(4, ([Write(big)], 2.5), ([Write(mz)], 2.5), ([FadeIn(pay, lag_ratio=0.3)], 3))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S19
class S19(BeatScene):
    SCENE_ID = 'S19'
    def construct(self):
        n, k = 12, 3
        g, d = petersen(n, k, R_out=2.2, R_in=1.05, center=LEFT*3.8)
        for i in range(2*k+2):
            d['u'][i].set_color(BLUE_V).set(radius=0.1)
        ub = MathTex(r"Z(P(n,k))\le2k+2", font_size=40).shift(RIGHT*2.8+UP*2.3)
        ubl = Text("Rashidi et al. 2020: 2k+2 consecutive outer vertices", font_size=24, color=MUTED).next_to(ub, DOWN, buff=0.2)
        k2 = MathTex(r"Z(P(n,2))=6\ \ (n\ge10)", font_size=34).next_to(ubl, DOWN, buff=0.5)
        k3 = MathTex(r"\text{Thm 3.6: } Z(P(n,3))=8\ \ (n\ge12)", font_size=34).next_to(k2, DOWN, buff=0.3)
        self.hold(1, ([FadeIn(g)], 1.5), ([Write(ub), FadeIn(ubl)], 2.5), ([Write(k2)], 1.5), ([Write(k3)], 1.5))
        cross = Cross(k3, stroke_color=RED, stroke_width=5)
        kr = VGroup(Text("Krishnan, July 2026:", font_size=28, color=YELLOW),
                    MathTex(r"Z(P(12,3))=7", font_size=36, color=YELLOW),
                    MathTex(r"\begin{array}{r|ccccccc} n & 7 & 8 & 9 & 10 & 11 & 12 & 13\text{--}20\\ \hline Z & 6 & 6 & 6 & 8 & 7 & 7 & 8\end{array}", font_size=30),
                    MathTex(r"\textbf{Conjecture 5: } Z(P(n,3))=8\ \ \forall n\ge13", font_size=32, color=YELLOW)).arrange(DOWN, buff=0.3).next_to(k3, DOWN, buff=0.5)
        self.hold(2, ([Create(cross)], 1), ([FadeIn(kr[0]), Write(kr[1])], 2), ([Write(kr[2])], 3), ([Write(kr[3])], 2.5))
        self.play(FadeOut(VGroup(k2, k3, cross, kr, ubl)), run_time=0.8)
        k4 = VGroup(MathTex(r"k\ge4:\quad Z(P(2k+1,k))=6\ \text{ only}", font_size=34),
                    Text("open: threshold at k = 3;\nany rigorous lower bound for k ≥ 4", font_size=26, color=MUTED, line_spacing=1.1)).arrange(DOWN, buff=0.3).next_to(ub, DOWN, buff=0.8)
        self.hold(3, ([Write(k4[0])], 2.5), ([FadeIn(k4[1])], 2.5))
        need = VGroup(Text("Needed, for every n:", font_size=30, weight=BOLD),
                      MathTex(r"A\ \text{on the }P(n,k)\text{ pattern with }\operatorname{null}A=2k+2", font_size=34, color=GREEN),
                      Text("constructed uniformly in n", font_size=28, color=YELLOW)).arrange(DOWN, buff=0.3).next_to(k4, DOWN, buff=0.7)
        self.hold(4, ([FadeIn(need, lag_ratio=0.4)], 3.5))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S20
class S20(BeatScene):
    SCENE_ID = 'S20'
    def construct(self):
        k = 3
        # linear strip: outer x_i on top row, inner y_i below
        N = 11; dx = 1.15; x0 = -(N-1)/2*dx
        xp = [np.array([x0+i*dx, 1.6, 0]) for i in range(N)]
        yp = [np.array([x0+i*dx, -0.2, 0]) for i in range(N)]
        outer = VGroup(*[Line(xp[i], xp[i+1], color=BLUE, stroke_width=3) for i in range(N-1)])
        spokes = VGroup(*[Line(xp[i], yp[i], color=MUTED, stroke_width=2) for i in range(N)])
        inner = VGroup(*[ArcBetweenPoints(yp[i], yp[i+k], angle=PI/2, color=ORANGE, stroke_width=2.5) for i in range(N-k)])
        xd = VGroup(*[Dot(p, radius=0.08, color=INK) for p in xp]); yd = VGroup(*[Dot(p, radius=0.08, color=INK) for p in yp])
        xl = VGroup(*[MathTex(f"x_{{{i-5:+d}}}" if i != 5 else "x_i", font_size=22).next_to(xp[i], UP, buff=0.15) for i in range(N)])
        yl = VGroup(*[MathTex(f"y_{{{i-5:+d}}}" if i != 5 else "y_i", font_size=22).next_to(yp[i], DOWN, buff=0.15) for i in range(N)])
        w = MathTex(r"b_i,\ c_i,\ e_i\ (\text{and primes})\ne0;\quad a_i,\ d_i\ \text{free}", font_size=30, color=MUTED).to_edge(UP, buff=0.4)
        self.hold(1, ([Create(outer), FadeIn(xd), FadeIn(xl)], 1.5), ([Create(spokes), FadeIn(yd), FadeIn(yl)], 1.5), ([Create(inner)], 1.5), ([Write(w)], 2))
        rowu = MathTex(r"\text{row }u_i:\ b'_{i-1}x_{i-1}+a_ix_i+b_ix_{i+1}+c_i\,y_i=0", font_size=32).shift(DOWN*2.3)
        solve = MathTex(r"\Rightarrow\ y_i=-\frac{b'_{i-1}x_{i-1}+a_ix_i+b_ix_{i+1}}{c_i}", font_size=34, color=GREEN).next_to(rowu, DOWN, buff=0.3)
        hi = VGroup(xd[4], xd[5], xd[6], yd[5]).copy().set_color(YELLOW)
        self.hold(2, ([Write(rowu)], 2.5), ([FadeIn(hi)], 1), ([Write(solve)], 2.5))
        self.play(FadeOut(hi), FadeOut(rowu), FadeOut(solve), run_time=0.6)
        rowv = MathTex(r"\text{row }v_i:\ e'_{i-k}y_{i-k}+d_iy_i+e_iy_{i+k}+c'_ix_i=0", font_size=32).shift(DOWN*2.3)
        self.play(Write(rowv), run_time=2)
        # highlight the nine positions
        nine = [5-k-1, 5-k, 5-k+1, 4, 5, 6, 5+k-1, 5+k, 5+k+1]
        hl = VGroup(*[Circle(radius=0.17, color=YELLOW, stroke_width=3).move_to(xp[i]) for i in nine])
        yh = VGroup(*[Circle(radius=0.17, color=ORANGE, stroke_width=3).move_to(yp[i]) for i in (5-k, 5, 5+k)])
        rec = MathTex(r"\sum_{p=-k-1}^{k+1}\gamma_{i,p}\,x_{i+p}=0\quad\text{(nine positions)}", font_size=34, color=GREEN).next_to(rowv, DOWN, buff=0.3)
        self.hold(3, ([FadeIn(yh)], 1), ([FadeIn(hl, lag_ratio=0.1)], 2), ([Write(rec)], 2.5))
        self.play(FadeOut(rowv), FadeOut(rec), FadeOut(yh), run_time=0.6)
        ends = MathTex(r"\gamma_{i,k+1}=-\frac{e_i\,b_{i+k}}{c_{i+k}}\ne0,\qquad \gamma_{i,-k-1}=-\frac{e'_{i-k}\,b'_{i-k-1}}{c_{i-k}}\ne0", font_size=32).shift(DOWN*2.3)
        ord_ = Text("a linear recurrence of order exactly 2k+2", font_size=30, color=YELLOW).next_to(ends, DOWN, buff=0.35)
        self.hold(4, ([Write(ends)], 3), ([hl[0].animate.set_color(RED), hl[-1].animate.set_color(RED)], 1), ([FadeIn(ord_)], 2))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)
        mono = VGroup(MathTex(r"\text{solutions on }\mathbb Z:\ \dim=2k+2", font_size=38),
                      MathTex(r"T=T_{n-1}\cdots T_0\in GL_{2k+2}(\mathbb R)\quad\text{(monodromy)}", font_size=38),
                      MathTex(r"\ker A\ \cong\ \{n\text{-periodic solutions}\}=\ker(T-I)", font_size=38),
                      MathTex(r"\operatorname{null}A=\dim\ker(T-I)\ \le\ 2k+2,\quad =\iff T=I", font_size=42, color=YELLOW)).arrange(DOWN, buff=0.5)
        self.hold(5, ([Write(mono[0])], 2), ([Write(mono[1])], 2.5), ([Write(mono[2])], 2.5), ([Write(mono[3])], 3))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S21
class S21(BeatScene):
    SCENE_ID = 'S21'
    def construct(self):
        t = MathTex(r"\operatorname{null}A\le2k+2\ \text{ for every }A\text{ on the pattern};\quad =2k+2\iff T=I", font_size=36, color=YELLOW).to_edge(UP, buff=0.6)
        self.hold(1, ([Write(t)], 3))
        n, k = 12, 2
        g, d = petersen(n, k, R_out=2.0, R_in=1.0, center=LEFT*3.8+DOWN*0.6)
        for i in range(2*k+2):
            d['u'][i].set_color(BLUE_V).set(radius=0.1)
        a = VGroup(Text("recurrence of order 2k+2", font_size=28),
                   Text("= a kernel vector can't vanish on\n2k+2 consecutive outer vertices", font_size=24, color=MUTED, line_spacing=1.1),
                   Text("= the forcing set of\nthe rotation bootstrap", font_size=28, line_spacing=1.1),
                   MathTex(r"\text{order of recurrence} = |S| = 2k+2", font_size=34, color=GREEN)).arrange(DOWN, buff=0.3).shift(RIGHT*2.9+DOWN*0.3)
        self.hold(2, ([FadeIn(g)], 1.5), ([FadeIn(a, lag_ratio=0.3)], 4))
        self.play(FadeOut(a), run_time=0.6)
        b = VGroup(Text("ceiling of the method\n= the bound it tries to match", font_size=28, weight=BOLD, line_spacing=1.1),
                   Text("no slack on either side", font_size=28, color=YELLOW),
                   Text("either the matrix method settles Z\ncompletely, or nothing does", font_size=24, color=MUTED, line_spacing=1.1),
                   Text("(earlier: “capped near 6–8” — a property\nof our constructions, not the method)", font_size=22, color=RED, line_spacing=1.1)).arrange(DOWN, buff=0.3).shift(RIGHT*2.9+DOWN*0.3)
        self.hold(3, ([FadeIn(b, lag_ratio=0.3)], 4.5))
        self.play(FadeOut(b), run_time=0.6)
        c = VGroup(Text("a bound a search\ncannot legally violate", font_size=30, weight=BOLD, line_spacing=1.1),
                   Text("twice, a numerical search returned\na nullity the theorem forbids", font_size=24, line_spacing=1.1),
                   Text("both times: a bug, caught", font_size=28, color=GREEN)).arrange(DOWN, buff=0.35).shift(RIGHT*2.9+DOWN*0.3)
        self.hold(4, ([FadeIn(c, lag_ratio=0.3)], 4))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S22
class S22(BeatScene):
    SCENE_ID = 'S22'
    def construct(self):
        inv = MathTex(r"A=\begin{pmatrix} aI+(P+P^{-1}) & cI\\ cI & dI+e(P^{k}+P^{-k})\end{pmatrix}\quad\text{(rotation-invariant)}", font_size=36).to_edge(UP, buff=0.6)
        self.hold(1, ([Write(inv)], 3))
        blk = MathTex(r"M_m=\begin{pmatrix} a+s_m & c\\ c & d+e\,t_m\end{pmatrix},\quad s_m=2\cos\tfrac{2\pi m}{n},\ t_m=2\cos\tfrac{2\pi km}{n}", font_size=34).next_to(inv, DOWN, buff=0.6)
        nul = MathTex(r"\operatorname{null}A=\#\{m:\ \det M_m=0\}", font_size=38, color=YELLOW).next_to(blk, DOWN, buff=0.5)
        self.hold(2, ([Write(blk)], 3), ([Write(nul)], 2))
        self.play(FadeOut(inv), VGroup(blk, nul).animate.to_edge(UP, buff=0.5), run_time=0.8)
        # symbol plot: a polynomial in s with roots at grid values
        n = 14; k = 3
        grid = sorted(set(round(2*np.cos(2*PI*m/n), 6) for m in range(n)))
        ax = Axes(x_range=[-2.2, 2.2, 1], y_range=[-3, 3, 1], x_length=6.5, y_length=3.0, axis_config={"include_tip": False, "color": MUTED}).shift(DOWN*1.5+LEFT*3.2)
        sl = MathTex("s", font_size=28).next_to(ax.x_axis, RIGHT)
        gd = VGroup(*[Dot(ax.c2p(s, 0), radius=0.06, color=MUTED) for s in grid])
        roots = [grid[0], grid[1], grid[2]]
        def sym(s):
            v = 0.35*(s-roots[0])*(s-roots[1])*(s-roots[2])*(s-1.3)
            return max(min(v, 3), -3)
        cur = ax.plot(sym, x_range=[-2.2, 2.2, 0.01], color=TEAL)
        syml = Text("symbol: det M as a polynomial in s, degree k+1", font_size=22, color=TEAL).next_to(ax, DOWN, buff=0.15)
        self.hold(3, ([Create(ax), FadeIn(sl), FadeIn(gd)], 1.5), ([Create(cur)], 2), ([FadeIn(syml)], 1.5))
        rd = VGroup(*[Dot(ax.c2p(r, 0), radius=0.09, color=YELLOW) for r in roots])
        par = VGroup(MathTex(r"\text{free: }a,\ d,\ e,\ c^{2}", font_size=30), MathTex(r"\Rightarrow\ 3\ \text{roots prescribed, no more}", font_size=30),
                     MathTex(r"k=2:\ \text{nullity }6=2k+2\ \checkmark", font_size=30, color=GREEN), MathTex(r"k\ge3:\ 6<2k+2", font_size=30, color=RED)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).shift(DOWN*1.2)
        self.hold(4, ([FadeIn(rd, lag_ratio=0.3)], 1.5), ([FadeIn(par, lag_ratio=0.3)], 4))
        self.play(FadeOut(par), run_time=0.5)
        gal = VGroup(MathTex(r"\text{rational symbol}\ni2\cos\tfrac{2\pi}{d}\\ \Rightarrow\ \text{all }2\cos\tfrac{2\pi m}{d}", font_size=28),
                     Text("Galois orbits land on the grid for free", font_size=26, color=YELLOW),
                     MathTex(r"Z(P(n,4))=10\ \ (60,70,90\mid n)", font_size=28, color=GREEN),
                     MathTex(r"Z(P(n,5))=12\ \ (24\mid n)", font_size=28, color=GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).shift(DOWN*1.2)
        more = VGroup(*[Dot(ax.c2p(s, 0), radius=0.09, color=PURPLE) for s in grid[3:7]])
        self.hold(5, ([Write(gal[0])], 2.5), ([FadeIn(more, lag_ratio=0.3), FadeIn(gal[1])], 2), ([Write(gal[2]), Write(gal[3])], 3))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S23
class S23(BeatScene):
    SCENE_ID = 'S23'
    def construct(self):
        t = Text("Two limitations, both intrinsic", font_size=36, weight=BOLD).to_edge(UP, buff=0.6)
        self.hold(1, ([Write(t)], 2))
        r1 = VGroup(MathTex(r"\text{realisability: } c^{2}=a\alpha-\beta\ \ne\ 0\quad(>0\ \text{for symmetric})", font_size=32),
                    MathTex(r"k\ \text{even},\ \text{roots }y,-y\ \Rightarrow\ c^{2}\equiv0", font_size=32, color=RED),
                    MathTex(r"k=2:\quad c^{2}=-(s_1+s_2)(s_1+s_3)(s_2+s_3)", font_size=36, color=YELLOW)).arrange(DOWN, buff=0.35).next_to(t, DOWN, buff=0.6)
        self.hold(2, ([Write(r1[0])], 3), ([Write(r1[1])], 2.5), ([Write(r1[2])], 3))
        # antipodal grid on a circle
        self.play(FadeOut(r1), run_time=0.5)
        n = 10; R = 1.5; c = LEFT*3.5+DOWN*1.0
        circ = Circle(radius=R, color=MUTED).move_to(c)
        pts = VGroup(*[Dot(c + R*np.array([np.cos(2*PI*m/n), np.sin(2*PI*m/n), 0]), radius=0.07, color=BLUE) for m in range(n)])
        anti = Line(pts[1].get_center(), pts[6].get_center(), color=RED, stroke_width=3)
        k2 = VGroup(MathTex(r"Z(P(n,2))=M(P(n,2))=6\\ (n\ge9,\ n\ne10)", font_size=32, color=GREEN),
                    MathTex(r"n=8:\ Z=5\ \text{(method right to fail)}", font_size=26),
                    MathTex(r"n=10:\ Z=6\ \text{(method falls short;}\\ \text{non-symmetric integer matrix)}", font_size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(circ, RIGHT, buff=0.8)
        self.hold(3, ([Create(circ), FadeIn(pts)], 1.5), ([Create(anti)], 1), ([Write(k2[0])], 2.5), ([FadeIn(k2[1]), FadeIn(k2[2])], 3))
        self.play(FadeOut(circ), FadeOut(pts), FadeOut(anti), FadeOut(k2), run_time=0.6)
        r2 = VGroup(Text("fixed rational symbol ⇒ fixed algebraic roots", font_size=30),
                    Text("⇒ on the grid only for n in one divisibility class", font_size=30),
                    Text("⇒ at most one prime. Never “all large n”.", font_size=30, color=RED),
                    Text("The route to all n must break the rotational symmetry.", font_size=30, color=YELLOW)).arrange(DOWN, buff=0.4).next_to(t, DOWN, buff=0.8)
        self.hold(4, ([FadeIn(r2, lag_ratio=0.35)], 5))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S24
class S24(BeatScene):
    SCENE_ID = 'S24'
    def construct(self):
        t = MathTex(r"\operatorname{null}A=2k+2\iff T(w)=I\qquad\text{no roots of unity, no divisibility}", font_size=36, color=YELLOW).to_edge(UP, buff=0.6)
        self.hold(1, ([Write(t)], 3))
        kr = VGroup(Text("Newton ⇒ weights to 14 digits. Not a proof.", font_size=28),
                    MathTex(r"\text{Krawczyk: } K(X)\subset X\ \Rightarrow\ \exists\ \text{true zero in }X", font_size=34, color=GREEN),
                    Text("a theorem of interval analysis, not a measurement", font_size=26, color=MUTED)).arrange(DOWN, buff=0.35).next_to(t, DOWN, buff=0.6)
        self.hold(2, ([FadeIn(kr[0])], 2), ([Write(kr[1])], 2.5), ([FadeIn(kr[2])], 1.5))
        self.play(FadeOut(kr), run_time=0.5)
        bil = VGroup(MathTex(r"T\text{ rational in }w;\ \text{image dim }51\subset64\ (k=3):\ \text{degenerate}", font_size=30, color=RED),
                     MathTex(r"\text{instead: } \operatorname{null}A\ge r\iff \exists K=P\binom{I_r}{X}:\ A(w)K(X)=0", font_size=32),
                     MathTex(r"f(w,X)=A(w)K(X)\ \text{ bilinear, integer coefficients, affine Jacobian}", font_size=30, color=GREEN)).arrange(DOWN, buff=0.4).next_to(t, DOWN, buff=0.6)
        self.hold(3, ([Write(bil[0])], 3), ([Write(bil[1])], 3), ([Write(bil[2])], 3))
        self.play(FadeOut(bil), run_time=0.5)
        dep = VGroup(MathTex(r"K^{\!\top}AK\ \text{symmetric}\ \Rightarrow\ \binom r2\ \text{equations dependent}", font_size=32),
                     Text("pivoting silently leaves them unproved (28 at k = 3)", font_size=28, color=RED),
                     MathTex(r"\text{fix: all non-pivot rows}\ +\ \text{upper triangle of the }r\times r\text{ block}", font_size=30, color=GREEN),
                     Text("A passing test is not a proof.", font_size=30, weight=BOLD, color=YELLOW)).arrange(DOWN, buff=0.35).next_to(t, DOWN, buff=0.6)
        self.hold(4, ([Write(dep[0])], 3), ([FadeIn(dep[1])], 2), ([Write(dep[2])], 3), ([FadeIn(dep[3])], 1.5))
        self.play(FadeOut(dep), run_time=0.5)
        res = VGroup(MathTex(r"Z(P(n,3))=M(P(n,3))=8\quad n=17,\dots,33", font_size=40, color=GREEN),
                     MathTex(r"\text{primes }17,19,23,29,31\ \text{included}", font_size=32),
                     Text("…but still one n at a time", font_size=28, color=MUTED)).arrange(DOWN, buff=0.4).next_to(t, DOWN, buff=1.0)
        self.hold(5, ([Write(res[0])], 2.5), ([FadeIn(res[1])], 2), ([FadeIn(res[2])], 1.5))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)
