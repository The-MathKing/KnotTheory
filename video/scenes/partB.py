from lib import *
import numpy as np, json

def Dk_fn(k):
    T = np.polynomial.chebyshev.Chebyshev.basis(k)
    return lambda u: (7+4*u*T(u))**2 - 8*(2*u+2*T(u))**2

def largest_root_below_1(k):
    f = Dk_fn(k); us = np.linspace(0.5, 0.999999, 200001); v = f(us)
    idx = np.where(np.sign(v[:-1]) != np.sign(v[1:]))[0]
    return us[idx[-1]]

# ---------------------------------------------------------------- S09
class S09(BeatScene):
    SCENE_ID = 'S09'
    def construct(self):
        k = 3; f = Dk_fn(k)
        ax = Axes(x_range=[-1, 1, 0.5], y_range=[-20, 60, 20], x_length=10, y_length=3.6,
                  axis_config={"include_tip": False, "color": MUTED}, x_axis_config={"include_numbers": True}, y_axis_config={"include_numbers": True}).shift(DOWN*1.5)
        cur = ax.plot(f, x_range=[-1, 1, 0.005], color=BLUE)
        self.add(ax, cur)
        c1 = MathTex(r"D_k(1)=(7+4)^2-8(2+2)^2=121-128=-7", font_size=40).to_edge(UP, buff=0.6)
        p1 = Dot(ax.c2p(1, -7), color=RED, radius=0.1)
        self.hold(1, ([Write(c1)], 3), ([FadeIn(p1, scale=3)], 1))
        uk = largest_root_below_1(k)
        band = Rectangle(width=ax.c2p(1,0)[0]-ax.c2p(uk,0)[0], height=3.6, color=RED, fill_opacity=0.2, stroke_width=0).move_to(ax.c2p((1+uk)/2, 20))
        nt = ValueTracker(12)
        j1 = always_redraw(lambda: Dot(ax.c2p(np.cos(2*PI/nt.get_value()), f(np.cos(2*PI/nt.get_value()))), color=YELLOW, radius=0.1))
        j1l = always_redraw(lambda: MathTex(r"j=1,\ n=%d" % int(nt.get_value()), font_size=32, color=YELLOW).next_to(j1, UL, buff=0.2))
        self.hold(2, ([FadeIn(band)], 1.5), ([FadeIn(j1), FadeIn(j1l)], 1), ([nt.animate.set_value(40)], 6))
        bk = MathTex(r"n\le B_k=\frac{2\pi}{\arccos u_k}", font_size=40, color=YELLOW).next_to(c1, DOWN, buff=0.3).to_edge(LEFT, buff=1)
        tbl = MathTex(r"B_2=23,\quad B_3=32,\quad B_4=42\ \ \text{(all sharp)}", font_size=34).next_to(bk, DOWN, buff=0.3).to_edge(LEFT, buff=1)
        self.hold(3, ([FadeOut(c1)], 0.5), ([Write(bk)], 2.5), ([Write(tbl)], 2.5))
        c2 = MathTex(r"D_k(-1)=\begin{cases}-7 & k\ \text{odd}\\ +9 & k\ \text{even}\end{cases}", font_size=40).to_edge(RIGHT, buff=1).shift(UP*2.2)
        pm = Dot(ax.c2p(-1, -7), color=RED, radius=0.1)
        self.hold(4, ([Write(c2)], 2.5), ([FadeIn(pm, scale=3)], 1))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S10
class S10(BeatScene):
    SCENE_ID = 'S10'
    def construct(self):
        t = Text("A bound for every k, with no expansion", font_size=36, weight=BOLD).to_edge(UP, buff=0.6)
        self.hold(1, ([Write(t)], 2))
        e1 = MathTex(r"x=\cos t,\ y=\cos kt,\quad a=1-x,\ b=1-y,\ s=a+b", font_size=36).next_to(t, DOWN, buff=0.6)
        e2 = MathTex(r"\text{fail}\iff G(t)=4\sqrt2\,(x+y)-4xy>7", font_size=36).next_to(e1, DOWN, buff=0.4)
        e3 = MathTex(r"G=(8\sqrt2-4)-(4\sqrt2-4)\,s-4ab", font_size=36).next_to(e2, DOWN, buff=0.4)
        self.hold(2, ([Write(e1)], 2), ([Write(e2)], 2.5), ([Write(e3)], 2.5))
        f1 = MathTex(r"\text{(1) AM--GM: } 4ab\le s^{2}", font_size=34, color=GREEN).next_to(e3, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        f2 = MathTex(r"\text{(2) } s^{2}+(4\sqrt2-4)s = 8\sqrt2-11 \text{ exactly at } s=\tau=3-2\sqrt2", font_size=34, color=GREEN).next_to(f1, DOWN, buff=0.3).to_edge(LEFT, buff=1)
        self.hold(3, ([Write(f1)], 2), ([Write(f2)], 3))
        f3 = MathTex(r"\text{(3) } 1-\cos\theta\le\theta^{2}/2 \ \Rightarrow\ s\le(1+k^{2})\,t^{2}/2", font_size=34, color=GREEN).next_to(f2, DOWN, buff=0.3).to_edge(LEFT, buff=1)
        res = MathTex(r"n\ \le\ \pi\,(2+\sqrt2)\,\sqrt{k^{2}+1}", font_size=48, color=YELLOW).next_to(f3, DOWN, buff=0.5)
        self.hold(4, ([Write(f3)], 2.5), ([Write(res)], 2.5))
        self.play(FadeOut(VGroup(e1, e2, e3, f1, f2, f3)), res.animate.next_to(t, DOWN, buff=0.6), run_time=1)
        wrong = VGroup(Text("Earlier draft: Taylor expansion in t at fixed k", font_size=30, color=RED),
                       MathTex(r"\text{critical } t\sim 1/k \ \Rightarrow\ kt\sim1:\ \text{outside the expansion's domain}", font_size=32),
                       Text("Right constant, wrong argument. Replaced.", font_size=30, color=MUTED)).arrange(DOWN, buff=0.4).next_to(res, DOWN, buff=1)
        self.hold(5, ([FadeIn(wrong[0])], 1.5), ([Write(wrong[1])], 2.5), ([FadeIn(wrong[2])], 1.5))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S11
class S11(BeatScene):
    SCENE_ID = 'S11'
    def construct(self):
        e1 = MathTex(r"\Bigl\|\tfrac jn\Bigr\|^{2}+\Bigl\|\tfrac{jk}{n}\Bigr\|^{2}\ <\ \frac{\tau}{2\pi^{2}}=0.00869\ldots\ \Rightarrow\ \text{fail}", font_size=40).to_edge(UP, buff=0.8)
        note = MathTex(r"\|\theta\| = \text{distance from }\theta\text{ to the nearest integer}", font_size=30, color=MUTED).next_to(e1, DOWN, buff=0.3)
        self.hold(1, ([Write(e1)], 3), ([FadeIn(note)], 1.5))
        # torus picture: points (j/n mod 1, jk/n mod 1)
        sq = Square(side_length=4, color=MUTED).shift(DOWN*0.9+LEFT*3)
        c = sq.get_center(); L = 4
        n, k = 40, 7
        pts = VGroup(*[Dot(c + L*np.array([((j/n+0.5)%1)-0.5, ((j*k/n+0.5)%1)-0.5, 0]), radius=0.05, color=BLUE) for j in range(1, n)])
        tgt = Circle(radius=L*np.sqrt(0.00869), color=RED, fill_opacity=0.25).move_to(c)
        dir = MathTex(r"\text{Dirichlet: } \exists\, j\le J:\ \Bigl\|\tfrac{jk}{n}\Bigr\|\le\frac1{J+1}", font_size=36, color=YELLOW).shift(RIGHT*3+DOWN*0.3)
        self.hold(2, ([Create(sq), FadeIn(pts, lag_ratio=0.03)], 2.5), ([FadeIn(tgt)], 1), ([Write(dir)], 2.5))
        e3 = MathTex(r"J=\lfloor\sqrt n\rfloor:\quad \Bigl\|\tfrac jn\Bigr\|^{2}<\frac1n,\ \ \Bigl\|\tfrac{jk}{n}\Bigr\|^{2}<\frac1n", font_size=34).next_to(dir, DOWN, buff=0.5)
        e4 = MathTex(r"\text{sum}<\frac2n", font_size=38).next_to(e3, DOWN, buff=0.4)
        self.hold(3, ([Write(e3)], 3), ([Write(e4)], 1.5))
        res = MathTex(r"\frac2n<\frac{\tau}{2\pi^{2}}\iff n>\frac{4\pi^{2}}{\tau}=230.097\ldots", font_size=38, color=YELLOW).move_to(e3).shift(DOWN*0.2)
        fin = clamp(Text("n ≥ 231: fails for every k.\nFinite in both variables.", font_size=28, weight=BOLD, line_spacing=1.1).next_to(res, DOWN, buff=0.5))
        self.hold(4, ([FadeOut(e3), FadeOut(e4), FadeOut(dir)], 0.5), ([Write(res)], 3), ([FadeIn(fin)], 2))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S12
class S12(BeatScene):
    SCENE_ID = 'S12'
    def construct(self):
        e1 = MathTex(r"D_k=f_-\,f_+,\qquad f_\pm=7+P\pm2\sqrt2\,A", font_size=42).to_edge(UP, buff=0.7)
        e2 = MathTex(r"f_-+f_+=2(7+P)\ge6>0\ \Rightarrow\ \text{never both negative}", font_size=34, color=GREEN).next_to(e1, DOWN, buff=0.4)
        self.hold(1, ([Write(e1)], 2.5), ([Write(e2)], 2.5))
        e3 = MathTex(r"x=\cos\frac{\pi j(k+1)}{n},\qquad y=\cos\frac{\pi j(k-1)}{n}", font_size=40).next_to(e2, DOWN, buff=0.6)
        e4 = MathTex(r"A=4xy,\qquad P=4x^{2}+4y^{2}-4", font_size=40).next_to(e3, DOWN, buff=0.5)
        self.hold(2, ([Write(e3)], 2.5), ([Write(e4)], 2.5))
        Q = MathTex(r"Q(x,y)=4x^{2}+4y^{2}-8\sqrt2\,|xy|+3\ \ge\ 0", font_size=48, color=YELLOW).next_to(e4, DOWN, buff=0.7)
        self.hold(3, ([Write(Q)], 3))
        nok = Text("Q does not contain k.", font_size=40, weight=BOLD, color=YELLOW).next_to(Q, DOWN, buff=0.6)
        self.hold(4, ([FadeIn(nok, scale=1.2)], 1.5))
        self.play(FadeOut(VGroup(e1, e2, e3, e4, nok)), Q.animate.scale(0.75).to_edge(UP, buff=0.5), run_time=1)
        # the square with corner regions
        L = 5.2; c = DOWN*0.6 + LEFT*2.5
        sq = Square(side_length=L, color=MUTED).move_to(c)
        def ym(x): return np.sqrt(2)*x - 0.5*np.sqrt(max(4*x*x-3, 0))
        x0 = np.sqrt(2) - 0.5
        xs = np.linspace(x0, 1, 60)
        poly_pts = [np.array([x, ym(x), 0]) for x in xs] + [np.array([1, 1, 0])]
        regions = VGroup()
        for sx in (1, -1):
            for sy in (1, -1):
                pts = [c + (L/2)*np.array([sx*p[0], sy*p[1], 0]) for p in poly_pts]
                regions.add(Polygon(*pts, color=RED, fill_opacity=0.5, stroke_width=1))
        # zoom inset of the (+1,+1) corner, magnified
        Z = 8.0; zc = RIGHT*3.4 + UP*1.1
        zpts = [zc + Z*(np.array([p[0], p[1], 0]) - np.array([1, 1, 0])) + np.array([0.9, 0.9, 0]) for p in poly_pts]
        zreg = Polygon(*zpts, color=RED, fill_opacity=0.5, stroke_width=1)
        zbox = Square(side_length=1.8, color=MUTED, stroke_width=1).move_to(zc)
        zcorner = Dot(zc + np.array([0.9, 0.9, 0]), radius=0.05, color=YELLOW)
        zl = MathTex(r"\text{corner }(1,1),\ \times8", font_size=24, color=MUTED).next_to(zbox, UP, buff=0.15)
        zoom = VGroup(zbox, zreg, zcorner, zl)
        area = MathTex(r"\text{area}=4\Bigl(\tfrac32-\sqrt2+\tfrac38\log\tfrac{1+\sqrt2}{3}\Bigr)=0.43\%", font_size=30).next_to(zoom, DOWN, buff=0.4)
        hyp = MathTex(r"Q=0:\ \text{hyperbola,}\\ \text{asymptotes } |x|=(\sqrt2\pm1)|y|", font_size=28, color=MUTED).next_to(area, DOWN, buff=0.4)
        self.hold(5, ([Create(sq)], 1), ([FadeIn(regions)], 1.5), ([FadeIn(zoom)], 1.5), ([Write(area)], 2.5), ([FadeIn(hyp)], 1.5))
        # map grid points for n,k
        def mapped(n, k):
            vg = VGroup()
            for j in range(1, n):
                if n % 2 == 0 and j == n//2: continue
                x = np.cos(PI*j*(k+1)/n); y = np.cos(PI*j*(k-1)/n)
                vg.add(Dot(c + (L/2)*np.array([x, y, 0]), radius=0.045, color=BLUE))
            return vg
        p1 = mapped(32, 3); l1 = MathTex(r"P(32,3)\ \checkmark", font_size=36, color=GREEN).next_to(hyp, DOWN, buff=0.6)
        p2 = mapped(33, 3); l2 = MathTex(r"P(33,3)\ \times", font_size=36, color=RED).move_to(l1)
        ex = Dot(c + (L/2)*np.array([-1, 1, 0]), radius=0.09, color=YELLOW)
        exl = Text("j = n/2: trivial −3, exempt", font_size=24, color=YELLOW).next_to(ex, DR, buff=0.15)
        self.hold(6, ([FadeIn(p1, lag_ratio=0.02), Write(l1)], 2.5), ([FadeIn(ex, scale=2), FadeIn(exl)], 2),
                  ([FadeOut(p1), FadeOut(l1), FadeOut(ex), FadeOut(exl), FadeIn(p2), Write(l2)], 2.5))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S13
class S13(BeatScene):
    SCENE_ID = 'S13'
    def construct(self):
        t = MathTex(r"3\le n\le230,\ 1\le k<n/2:\quad 13{,}110\ \text{cases}", font_size=40).to_edge(UP, buff=0.7)
        w = MathTex(r"D_k(u_j)\approx 0.000000\ldots?\qquad\text{sign?}", font_size=38, color=ORANGE).next_to(t, DOWN, buff=0.6)
        self.hold(1, ([Write(t)], 2.5), ([Write(w)], 2.5))
        e1 = MathTex(r"A,P\in\mathbb Z[\zeta_m+\zeta_m^{-1}]\ \Rightarrow\ D_k(u_j)\in\mathbb Z[\zeta_m]", font_size=36).next_to(w, DOWN, buff=0.6)
        e2 = MathTex(r"\text{reduce mod }\Phi_m(z):\ \text{exact integer vector, zero iff the value is zero}", font_size=32, color=GREEN).next_to(e1, DOWN, buff=0.4)
        self.hold(2, ([Write(e1)], 3), ([Write(e2)], 3))
        e3 = MathTex(r"\text{nonzero}\ \Rightarrow\ |D|\ \ge\ 249^{-(\deg-1)}\quad\text{(separation guard)}", font_size=34).next_to(e2, DOWN, buff=0.5)
        e4 = Text("13,110 cases, exact vs float64 control: 0 disagreements", font_size=28, color=MUTED).next_to(e3, DOWN, buff=0.4)
        self.hold(3, ([Write(e3)], 2.5), ([FadeIn(e4)], 2))
        self.play(FadeOut(VGroup(w, e1, e2, e3, e4)), run_time=0.8)
        bug = VGroup(Text("k = 1: exponents collide", font_size=32, color=RED),
                     MathTex(r"\{\,1{:}\,a,\ 1{:}\,b\,\}\ \to\ \text{dict literal keeps one}", font_size=34),
                     Text("exact classifier: every P(n,1) “Ramanujan” — incl. P(9,1), λ = −2.879", font_size=28),
                     Text("float64 control caught all four. Fixed.", font_size=30, color=GREEN)).arrange(DOWN, buff=0.45).next_to(t, DOWN, buff=0.8)
        self.hold(4, ([FadeIn(bug[0])], 1.5), ([Write(bug[1])], 2), ([FadeIn(bug[2])], 2.5), ([FadeIn(bug[3])], 1.5))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S14
class S14(BeatScene):
    SCENE_ID = 'S14'
    def construct(self):
        pairs = json.load(open(os.path.join(HERE, 'census.json')))
        ax = Axes(x_range=[0, 240, 40], y_range=[0, 50, 10], x_length=8.2, y_length=5.6,
                  axis_config={"include_tip": False, "color": MUTED}, x_axis_config={"include_numbers": True}, y_axis_config={"include_numbers": True}).shift(LEFT*2.3+DOWN*0.3)
        xl = MathTex("n", font_size=32).next_to(ax.x_axis, RIGHT); yl = MathTex("k", font_size=32).next_to(ax.y_axis, UP)
        dots = VGroup(*[Dot(ax.c2p(n, k), radius=0.035, color=BLUE if k % 2 == 0 else ORANGE) for n, k in pairs])
        head = VGroup(MathTex(r"460\ \text{pairs}\ (n,k)", font_size=36, color=YELLOW), MathTex(r"324\ \text{graphs}", font_size=32),
                      MathTex(r"n_{\max}=112\ (k=41)", font_size=32), MathTex(r"k_{\max}=45", font_size=32)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(UR, buff=0.5)
        self.hold(1, ([Create(ax), FadeIn(xl), FadeIn(yl)], 1.5), ([FadeIn(dots, lag_ratio=0.004)], 4), ([FadeIn(head)], 2))
        dl = DashedLine(ax.c2p(231, 0), ax.c2p(231, 50), color=RED); dll = MathTex("231", font_size=30, color=RED).next_to(dl, UP, buff=0.1)
        kl = Line(ax.c2p(0, 0), ax.c2p(100, 50), color=MUTED, stroke_width=1)
        run2 = SurroundingRectangle(VGroup(*[d for d, (n, k) in zip(dots, pairs) if k == 4]), color=BLUE, buff=0.05)
        self.hold(2, ([Create(dl), FadeIn(dll), Create(kl)], 2), ([Create(run2)], 1.5))
        run9 = SurroundingRectangle(VGroup(*[d for d, (n, k) in zip(dots, pairs) if k == 9]), color=ORANGE, buff=0.05)
        par = Text("odd k: even n only\nin the upper half\n(parity law)", font_size=24, color=ORANGE, line_spacing=1.1).next_to(head, DOWN, buff=0.5, aligned_edge=LEFT)
        self.hold(3, ([FadeOut(run2), Create(run9)], 1.5), ([FadeIn(par)], 2))
        top = SurroundingRectangle(VGroup(*[d for d, (n, k) in zip(dots, pairs) if k > 25]), color=YELLOW, buff=0.08)
        topl = Text("k > 25:\nno even k survives", font_size=24, color=YELLOW, line_spacing=1.1).next_to(par, DOWN, buff=0.4, aligned_edge=LEFT)
        self.hold(4, ([FadeOut(run9), Create(top)], 1.5), ([FadeIn(topl)], 2))
        nm = MathTex(r"k=8\to49\\ k=9\to90\\ k=10\to52", font_size=28).next_to(topl, DOWN, buff=0.4, aligned_edge=LEFT)
        self.hold(5, ([FadeOut(top), Write(nm)], 2.5))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S15
class S15(BeatScene):
    SCENE_ID = 'S15'
    def construct(self):
        # base graph: two vertices with loops and an edge
        u = Dot(LEFT*1.5, radius=0.12, color=BLUE); v = Dot(RIGHT*1.5, radius=0.12, color=ORANGE)
        lu = Arc(radius=0.6, start_angle=-PI/2+0.5, angle=2*PI-1.0, color=BLUE).move_to(LEFT*1.5+UP*0.75)
        lv = Arc(radius=0.6, start_angle=-PI/2+0.5, angle=2*PI-1.0, color=ORANGE).move_to(RIGHT*1.5+UP*0.75)
        e = Line(LEFT*1.5, RIGHT*1.5, color=MUTED)
        vol = VGroup(MathTex("1", font_size=32, color=BLUE).next_to(lu, UP, buff=0.1), MathTex("k", font_size=32, color=ORANGE).next_to(lv, UP, buff=0.1), MathTex("0", font_size=32, color=MUTED).next_to(e, DOWN, buff=0.1))
        base = VGroup(lu, lv, e, u, v, vol).shift(UP*1.5)
        bl = Text("two-vertex base, voltages (1, k, 0)", font_size=28, color=MUTED).next_to(base, DOWN, buff=0.4)
        g, d = petersen(9, 2, R_out=1.6, R_in=0.8, center=DOWN*1.8)
        self.hold(1, ([Create(base)], 2.5), ([FadeIn(bl)], 1.5), ([FadeIn(g)], 2))
        self.play(FadeOut(g), VGroup(base, bl).animate.to_edge(LEFT, buff=1).shift(DOWN*0.3), run_time=1)
        th = VGroup(Dot(LEFT*1, radius=0.12, color=BLUE), Dot(RIGHT*1, radius=0.12, color=ORANGE),
                    ArcBetweenPoints(LEFT*1, RIGHT*1, angle=-PI/2, color=MUTED), Line(LEFT*1, RIGHT*1, color=MUTED), ArcBetweenPoints(LEFT*1, RIGHT*1, angle=PI/2, color=MUTED)).to_edge(RIGHT, buff=2).shift(UP*1.3)
        thl = Text("theta base: bipartite Haar graphs", font_size=26, color=MUTED).next_to(th, DOWN, buff=0.3)
        crit = MathTex(r"Q\Bigl(\cos\tfrac{\pi j(a+b)}{n},\ \cos\tfrac{\pi j(a-b)}{n}\Bigr)\ge0", font_size=32, color=YELLOW).next_to(bl, DOWN, buff=0.6).to_edge(LEFT, buff=1)
        self.hold(2, ([Create(th), FadeIn(thl)], 2.5), ([Write(crit)], 3))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        e1 = MathTex(r"M_1\ \xrightarrow{\ n\to\infty\ }\ M_0=\text{adjacency of the base},\qquad \lambda_{\max}(M_0)=3", font_size=36).shift(UP*1.5)
        e2 = Text("No infinite family of Ramanujan graphs\nis a cyclic cover of a fixed base.", font_size=32, weight=BOLD, color=YELLOW, line_spacing=1.1).next_to(e1, DOWN, buff=0.8)
        self.hold(3, ([Write(e1)], 3), ([Write(e2)], 3))
        e3 = VGroup(Text("Known principle: abelian covers do not expand (why LPS used PGL₂)", font_size=28, color=MUTED),
                    Text("New here: the constant, and exact criteria for both bases", font_size=28),
                    MathTex(r"\text{deficit } \delta=\lambda_2-2\sqrt2\ \le\ 3-2\sqrt2", font_size=32)).arrange(DOWN, buff=0.4).next_to(e2, DOWN, buff=0.8)
        self.hold(4, ([FadeIn(e3[0])], 2), ([FadeIn(e3[1])], 2), ([Write(e3[2])], 2))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S16
class S16(BeatScene):
    SCENE_ID = 'S16'
    def construct(self):
        steps = ["zeta poles", "Ihara ⇒ eigenvalue bound", "symmetry ⇒ polynomial on a grid", "two squarings ⇒ D_k ∈ ℤ[u]",
                 "corner form ⇒ no k", "Dirichlet ⇒ finite in (n,k)", "cyclotomic arithmetic ⇒ certified"]
        chain = VGroup(*[Text(s, font_size=24) for s in steps]).arrange(DOWN, buff=0.28).to_edge(LEFT, buff=0.6)
        arrows = VGroup(*[Arrow(chain[i].get_bottom(), chain[i+1].get_top(), buff=0.05, color=MUTED, stroke_width=2, max_tip_length_to_length_ratio=0.3) for i in range(len(steps)-1)])
        self.hold(1, ([FadeIn(chain, lag_ratio=0.15), FadeIn(arrows, lag_ratio=0.15)], 6))
        r = VGroup(Text("A classification of a recognised kind", font_size=26, weight=BOLD),
                   Text("Droll; Le–Sander: same shape of answer", font_size=22, color=MUTED),
                   Text("Contribution: exactness and completeness,\nnot surprise", font_size=22, line_spacing=1.1),
                   MathTex(r"\text{which }460,\ \text{and nothing past }k=45", font_size=30, color=YELLOW)).arrange(DOWN, buff=0.35).to_edge(RIGHT, buff=0.5)
        self.hold(2, ([FadeIn(r, lag_ratio=0.3)], 4))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        t = VGroup(Text("Part II", font_size=56, weight=BOLD, color=TEAL), Text("Same graph. Same grid. The matrix is no longer fixed.", font_size=30, color=MUTED)).arrange(DOWN, buff=0.5)
        self.hold(3, ([FadeIn(t, scale=1.1)], 2))
        self.play(FadeOut(t), run_time=0.8)
