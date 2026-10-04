from lib import *
import numpy as np

def lam(t, k, sign):
    a, b = 2*np.cos(t), 2*np.cos(k*t)
    return (a+b)/2 + sign*np.sqrt(((a-b)/2)**2 + 1)

# ---------------------------------------------------------------- S01
class S01(BeatScene):
    SCENE_ID = 'S01'
    def construct(self):
        g, d = petersen(5, 2, R_out=2.4, R_in=1.1)
        self.beat(1, [Create(d['outer']), FadeIn(d['u'])], [Create(d['inner']), FadeIn(d['v'])],
                  [Create(d['spokes'])])
        # beat 2: morph to P(7,2) then P(9,3)
        g2, _ = petersen(7, 2, R_out=2.4, R_in=1.1)
        g3, _ = petersen(9, 3, R_out=2.4, R_in=1.1)
        lab = MathTex(r"P(n,k)", font_size=60).to_corner(UL).shift(RIGHT*0.5+DOWN*0.3)
        lab2 = MathTex(r"P(5,2)", font_size=40, color=MUTED).next_to(lab, DOWN, aligned_edge=LEFT)
        self.hold(2, ([Write(lab)], 1.5), ([Transform(g, g2)], 2.5), ([Transform(g, g3)], 2.5),
                  ([Transform(g, petersen(5,2,R_out=2.4,R_in=1.1)[0]), FadeIn(lab2)], 2.5))
        # beat 3: adjacency matrix sketch
        self.play(g.animate.scale(0.75).to_edge(LEFT, buff=1.0), FadeOut(lab2), run_time=1.5)
        A = IntegerMatrix([[0,1,0,0,1,1,0,0,0,0],[1,0,1,0,0,0,1,0,0,0],[0,1,0,1,0,0,0,1,0,0],
                           [0,0,1,0,1,0,0,0,1,0],[1,0,0,1,0,0,0,0,0,1],[1,0,0,0,0,0,0,1,1,0],
                           [0,1,0,0,0,0,0,0,1,1],[0,0,1,0,0,1,0,0,0,1],[0,0,0,1,0,1,1,0,0,0],
                           [0,0,0,0,1,0,1,1,0,0]], h_buff=0.75, v_buff=0.6).scale(0.5).to_edge(RIGHT, buff=0.8)
        q1 = clamp(Text("Q1: eigenvalues of the fixed matrix", font_size=30, color=YELLOW).next_to(A, UP, buff=0.4))
        self.hold(3, ([FadeIn(A)], 2), ([Write(q1)], 2))
        # beat 4: pattern with stars
        ents = A.get_entries()
        pattern = VGroup()
        for e in ents:
            if int(e.get_value()) == 1:
                pattern.add(MathTex(r"\ast", color=ORANGE, font_size=30).move_to(e))
            else:
                pattern.add(MathTex(r"0", color=MUTED, font_size=24).move_to(e))
        q2 = clamp(Text("Q2: every matrix with this pattern", font_size=30, color=TEAL).next_to(A, DOWN, buff=0.4))
        self.hold(4, ([Transform(ents, pattern)], 2.5), ([Write(q2)], 2))
        # beat 5: summary cards
        self.play(FadeOut(A), FadeOut(q1), FadeOut(q2), FadeOut(g), FadeOut(lab), run_time=1)
        c1 = VGroup(Text("Part I", font_size=40, weight=BOLD, color=YELLOW),
                    Text("Fixed matrix. Is the spectral gap optimal?", font_size=28),
                    Text("= the Riemann Hypothesis for the graph", font_size=28, color=MUTED)).arrange(DOWN, buff=0.25)
        c2 = VGroup(Text("Part II", font_size=40, weight=BOLD, color=TEAL),
                    Text("Ranging matrix. How degenerate can zero be?", font_size=28),
                    Text("= maximum nullity and zero forcing", font_size=28, color=MUTED)).arrange(DOWN, buff=0.25)
        cards = VGroup(c1, c2).arrange(DOWN, buff=1.0)
        self.hold(5, ([FadeIn(c1, shift=UP*0.3)], 1.5), ([], 4), ([FadeIn(c2, shift=UP*0.3)], 1.5))
        self.play(FadeOut(cards), run_time=0.8)

# ---------------------------------------------------------------- S02
class S02(BeatScene):
    SCENE_ID = 'S02'
    def construct(self):
        n, k = 8, 3
        g, d = petersen(n, k, R_out=2.7, R_in=1.3, center=LEFT*2.5)
        ulabels = VGroup(*[MathTex(f"u_{{{i}}}", font_size=28, color=BLUE).move_to(d['upos'][i]*1.13 + LEFT*2.5*(-0.13)) for i in range(n)])
        for i in range(n):
            p = d['upos'][i]; c = LEFT*2.5
            ulabels[i].move_to(c + (p-c)*1.14)
        rule1 = MathTex(r"u_i \sim u_{i+1}", font_size=44, color=BLUE).to_edge(RIGHT, buff=1.5).shift(UP*2)
        self.hold(1, ([Create(d['outer']), FadeIn(d['u'])], 2.5), ([FadeIn(ulabels)], 1.2), ([Write(rule1)], 1.2))
        rule2 = MathTex(r"v_i \sim v_{i+k}", font_size=44, color=ORANGE).next_to(rule1, DOWN, buff=0.6)
        vl = VGroup(*[MathTex(f"v_{{{i}}}", font_size=24, color=ORANGE).move_to(LEFT*2.5 + (d['vpos'][i]-LEFT*2.5)*0.72) for i in range(n)])
        # show k=1,2,3 inner patterns
        inner1 = petersen(n, 1, R_out=2.7, R_in=1.3, center=LEFT*2.5)[1]['inner']
        inner2 = petersen(n, 2, R_out=2.7, R_in=1.3, center=LEFT*2.5)[1]['inner']
        klab = MathTex("k=1", font_size=36, color=MUTED).next_to(rule2, DOWN, buff=0.5)
        self.hold(2, ([FadeIn(d['v']), FadeIn(vl), Write(rule2)], 1.5), ([Create(inner1), FadeIn(klab)], 1.5),
                  ([Transform(inner1, inner2), Transform(klab, MathTex("k=2", font_size=36, color=MUTED).move_to(klab))], 1.5),
                  ([Transform(inner1, d['inner']), Transform(klab, MathTex("k=3", font_size=36, color=MUTED).move_to(klab))], 1.5))
        rule3 = MathTex(r"u_i \sim v_i", font_size=44, color=MUTED).next_to(klab, DOWN, buff=0.5)
        cubic = Text("cubic: 2n vertices, 3n edges", font_size=28, color=INK).next_to(rule3, DOWN, buff=0.5)
        self.hold(3, ([Create(d['spokes']), Write(rule3)], 2), ([FadeIn(cubic)], 1.5))
        # beat 4: rotate
        whole = VGroup(d['outer'], inner1, d['spokes'], d['u'], d['v'], ulabels, vl)
        rot = MathTex(r"\rho: i \mapsto i+1", font_size=44, color=GREEN).to_edge(RIGHT, buff=1.5).shift(DOWN*2.8)
        self.hold(4, ([Rotate(whole, angle=2*PI/n, about_point=LEFT*2.5)], 2), ([Write(rot)], 1.2),
                  ([Rotate(whole, angle=2*PI/n, about_point=LEFT*2.5)], 2))
        self.play(FadeOut(VGroup(whole, rule1, rule2, rule3, klab, cubic, rot)), run_time=0.8)

# ---------------------------------------------------------------- S03
class S03(BeatScene):
    SCENE_ID = 'S03'
    def construct(self):
        n = 5
        rows = [[0,1,0,0,1,1,0,0,0,0],[1,0,1,0,0,0,1,0,0,0],[0,1,0,1,0,0,0,1,0,0],
                [0,0,1,0,1,0,0,0,1,0],[1,0,0,1,0,0,0,0,0,1],[1,0,0,0,0,0,0,1,1,0],
                [0,1,0,0,0,0,0,0,1,1],[0,0,1,0,0,1,0,0,0,1],[0,0,0,1,0,1,1,0,0,0],
                [0,0,0,0,1,0,1,1,0,0]]
        A = IntegerMatrix(rows, h_buff=0.7, v_buff=0.55).scale(0.55).to_edge(LEFT, buff=0.8)
        lab = MathTex("A", font_size=48).next_to(A, UP)
        g, d = petersen(5, 2, R_out=1.5, R_in=0.7, center=RIGHT*3.5+UP*1.5)
        self.hold(1, ([FadeIn(g)], 1.5), ([Write(lab), FadeIn(A)], 2.5),
                  ([Indicate(VGroup(*A.get_rows()[0]), color=YELLOW)], 1.5))
        eq = MathTex(r"A\,\mathbf 1 = 3\,\mathbf 1", font_size=44).next_to(g, DOWN, buff=0.6)
        self.hold(2, ([Write(eq)], 2))
        # beat 3: number line of eigenvalues
        ax = NumberLine(x_range=[-3, 3, 1], length=6, include_numbers=True, color=MUTED).next_to(eq, DOWN, buff=0.8)
        gap = DoubleArrow(ax.n2p(1), ax.n2p(3), buff=0, color=YELLOW, stroke_width=3).shift(UP*0.5)
        gapl = Text("spectral gap", font_size=22, color=YELLOW).next_to(gap, UP, buff=0.1)
        self.hold(3, ([Create(ax)], 1.5), ([FadeIn(Dot(ax.n2p(3), color=GREEN, radius=0.1))], 1),
                  ([GrowArrow(gap), FadeIn(gapl)], 1.5))
        dots = VGroup(*[Dot(ax.n2p(1)+UP*0.12*i, color=BLUE, radius=0.07) for i in range(5)],
                      *[Dot(ax.n2p(-2)+UP*0.12*i, color=ORANGE, radius=0.07) for i in range(4)])
        spec = MathTex(r"\{3^{1},\ 1^{5},\ (-2)^{4}\}", font_size=40).next_to(ax, DOWN, buff=0.5)
        self.hold(4, ([FadeIn(dots, lag_ratio=0.1)], 2), ([Write(spec)], 1.5))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S04
class S04(BeatScene):
    SCENE_ID = 'S04'
    def construct(self):
        ax = NumberLine(x_range=[-3, 3, 1], length=9, include_numbers=True, color=MUTED).shift(DOWN*1.5)
        r = 2*np.sqrt(2)
        band = Rectangle(width=ax.n2p(r)[0]-ax.n2p(-r)[0], height=0.8, color=YELLOW, fill_opacity=0.15, stroke_width=1).move_to(ax.n2p(0)+UP*0.0)
        bl = MathTex(r"-2\sqrt2", font_size=36, color=YELLOW).next_to(ax.n2p(-r), UP, buff=0.6)
        br = MathTex(r"2\sqrt2\approx 2.828", font_size=36, color=YELLOW).next_to(ax.n2p(r), UP, buff=0.6)
        ab = Text("Alon–Boppana: no infinite cubic family beats this", font_size=30).to_edge(UP, buff=0.8)
        self.hold(1, ([Create(ax)], 1.5), ([FadeIn(band), Write(bl), Write(br)], 2), ([FadeIn(ab)], 1.5))
        # beat 2: tree
        tree = VGroup()
        def grow(p, ang, depth, L):
            if depth == 0: return
            for da in ([0, 2*PI/3, -2*PI/3] if depth == 3 else [PI/3, -PI/3]):
                a = ang + da
                q = p + L*np.array([np.cos(a), np.sin(a), 0])
                tree.add(Line(p, q, color=TEAL, stroke_width=2), Dot(q, radius=0.04, color=INK))
                grow(q, a, depth-1, L*0.55)
        tree.add(Dot(ORIGIN, radius=0.05, color=INK))
        grow(ORIGIN, PI/2, 3, 1.1)
        tree.move_to(UP*1.2 + LEFT*4)
        tl = Text("3-regular tree: spectrum = [−2√2, 2√2]", font_size=26, color=TEAL).next_to(tree, RIGHT, buff=0.6)
        self.hold(2, ([FadeOut(ab)], 0.5), ([Create(tree)], 3), ([FadeIn(tl)], 1.5))
        ram = Text("Ramanujan graph: all nontrivial |λ| ≤ 2√2", font_size=30, color=YELLOW).to_edge(UP, buff=0.8)
        self.hold(3, ([FadeOut(tree), FadeOut(tl)], 0.5), ([Write(ram)], 2))
        dots = VGroup(Dot(ax.n2p(3), color=GREEN, radius=0.1), Dot(ax.n2p(1), color=BLUE, radius=0.1), Dot(ax.n2p(-2), color=ORANGE, radius=0.1))
        q = Text("Which P(n,k) are Ramanujan?", font_size=36, weight=BOLD).next_to(ax, DOWN, buff=0.9)
        self.hold(4, ([FadeIn(dots)], 1.5), ([], 2), ([Write(q)], 2))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S05
class S05(BeatScene):
    SCENE_ID = 'S05'
    def construct(self):
        z1 = MathTex(r"\zeta(s)=\prod_{p\ \mathrm{prime}}\bigl(1-p^{-s}\bigr)^{-1}", font_size=44).shift(UP*1.8)
        z2 = MathTex(r"\zeta_X(u)=\prod_{[C]\ \mathrm{prime\ cycle}}\bigl(1-u^{\ell(C)}\bigr)^{-1}", font_size=44).next_to(z1, DOWN, buff=0.8)
        l1 = Text("Riemann", font_size=26, color=MUTED).next_to(z1, LEFT, buff=0.6)
        l2 = Text("Ihara", font_size=26, color=MUTED).next_to(z2, LEFT, buff=0.6)
        self.hold(1, ([Write(z1), FadeIn(l1)], 2), ([Write(z2), FadeIn(l2)], 2.5))
        props = VGroup(Text("Euler product", font_size=28), Text("functional equation", font_size=28),
                       Text("prime number theorem for closed geodesics", font_size=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(z2, DOWN, buff=0.7)
        rh = MathTex(r"u=q^{-s}:\quad \text{poles in }0<\mathrm{Re}\,s<1\ \text{lie on}\ \mathrm{Re}\,s=\tfrac12\,?", font_size=36, color=YELLOW).next_to(props, DOWN, buff=0.5)
        self.hold(2, ([FadeIn(props, lag_ratio=0.3)], 2.5), ([Write(rh)], 2.5))
        rh_top = rh.copy().scale(0.85).to_edge(UP, buff=0.5)
        self.play(FadeOut(props), FadeOut(z1), FadeOut(l1), FadeOut(l2), FadeOut(z2), Transform(rh, rh_top), run_time=1)
        det = MathTex(r"\zeta_X(u)^{-1}=(1-u^2)^{|E|-|V|}\det\bigl(I-uA+qu^2I\bigr)", font_size=38).shift(UP*1.0)
        iff = MathTex(r"\text{RH for }X\iff X\text{ is Ramanujan}", font_size=44, color=GREEN).next_to(det, DOWN, buff=0.7)
        cub = MathTex(r"q=2:\quad |\lambda|\le 2\sqrt2\ \text{ for every nontrivial }\lambda", font_size=38).next_to(iff, DOWN, buff=0.5)
        self.hold(3, ([Write(det)], 2.5), ([Write(iff)], 2), ([Write(cub)], 2))
        q = Text("For which n, k does P(n,k) satisfy the Riemann Hypothesis?", font_size=32, weight=BOLD, color=YELLOW).to_edge(DOWN, buff=0.8)
        self.hold(4, ([Write(q)], 2.5))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S06
class S06(BeatScene):
    SCENE_ID = 'S06'
    def construct(self):
        gs = Text("Gera & Stănică (2011): every eigenvalue of P(n,k) in closed form", font_size=30).to_edge(UP, buff=0.8)
        f = MathTex(r"\lambda_\pm(j)=\frac{\alpha_j+\beta_j}{2}\pm\sqrt{\Bigl(\frac{\alpha_j-\beta_j}{2}\Bigr)^{2}+1}", font_size=42).shift(UP*1.3)
        miss = VGroup(Text("“Ramanujan”", font_size=30, color=RED), Text("“expander”", font_size=30, color=RED), Text("“spectral gap”", font_size=30, color=RED)).arrange(RIGHT, buff=0.8).next_to(f, DOWN, buff=0.8)
        zero = Text("0 occurrences", font_size=26, color=MUTED).next_to(miss, DOWN, buff=0.2)
        self.hold(1, ([FadeIn(gs)], 1.5), ([Write(f)], 2.5), ([FadeIn(miss), FadeIn(zero)], 2))
        prior = VGroup(Text("Droll — unitary Cayley graphs: finitely many", font_size=26),
                       Text("Le–Sander — integral circulants: finitely many", font_size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(zero, DOWN, buff=0.45)
        warn = MathTex(r"\sqrt{\;\cdot\;}\ \ \overset{?}{\lessgtr}\ \ 2\sqrt2 \qquad\text{(near equality: floating point guesses)}", font_size=32, color=ORANGE).next_to(prior, DOWN, buff=0.5)
        self.hold(2, ([FadeIn(prior, lag_ratio=0.3)], 2.5), ([Write(warn)], 2.5))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S07
class S07(BeatScene):
    SCENE_ID = 'S07'
    def construct(self):
        n = 8
        g, d = petersen(n, 3, R_out=1.8, R_in=0.85, center=LEFT*4.2+UP*0.6)
        rot = MathTex(r"\rho A = A\rho", font_size=40, color=GREEN).next_to(g, DOWN, buff=0.4)
        big = MathTex(r"A \;\xrightarrow{\ \text{Fourier over }\mathbb Z_n\ }\; M_0\oplus M_1\oplus\cdots\oplus M_{n-1}", font_size=40).shift(RIGHT*1.5+UP*2.2)
        self.hold(1, ([FadeIn(g)], 1.5), ([Rotate(g, 2*PI/n, about_point=LEFT*4.2+UP*0.6), Write(rot)], 2), ([Write(big)], 2.5))
        Mj = MathTex(r"M_j=\begin{pmatrix}\alpha_j & 1\\ 1 & \beta_j\end{pmatrix}", font_size=46).shift(RIGHT*1.5+UP*0.5)
        ab = MathTex(r"\alpha_j=2\cos\frac{2\pi j}{n},\qquad \beta_j=2\cos\frac{2\pi jk}{n}", font_size=38).next_to(Mj, DOWN, buff=0.5)
        self.hold(2, ([Write(Mj)], 2), ([Write(ab)], 2.5))
        why = VGroup(MathTex(r"\text{outer: }\ \zeta^{\,j}+\zeta^{-j}=\alpha_j", font_size=32, color=BLUE),
                     MathTex(r"\text{inner: }\ \zeta^{\,jk}+\zeta^{-jk}=\beta_j", font_size=32, color=ORANGE),
                     MathTex(r"\text{spoke: }\ 1", font_size=32, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ab, DOWN, buff=0.5)
        self.hold(3, ([Indicate(d['outer'], color=BLUE), FadeIn(why[0])], 2), ([Indicate(d['inner'], color=ORANGE), FadeIn(why[1])], 2), ([Indicate(d['spokes']), FadeIn(why[2])], 2))
        ev = MathTex(r"\lambda_\pm=\frac{\alpha+\beta}{2}\pm\sqrt{\Bigl(\frac{\alpha-\beta}{2}\Bigr)^2+1}", font_size=38, color=YELLOW).move_to(why)
        self.hold(4, ([FadeOut(why)], 0.5), ([Write(ev)], 2.5))
        # beat 5: curves sampled
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        k = 3
        ax = Axes(x_range=[0, 2*PI, PI/2], y_range=[-3.5, 3.5, 1], x_length=11, y_length=5.5,
                  axis_config={"include_tip": False, "color": MUTED}, y_axis_config={"include_numbers": True})
        xl = MathTex(r"t", font_size=30).next_to(ax.x_axis, RIGHT)
        cp = ax.plot(lambda t: lam(t, k, 1), x_range=[0, 2*PI, 0.01], color=BLUE)
        cm = ax.plot(lambda t: lam(t, k, -1), x_range=[0, 2*PI, 0.01], color=ORANGE)
        r = 2*np.sqrt(2)
        hp = DashedLine(ax.c2p(0, r), ax.c2p(2*PI, r), color=YELLOW); hm = DashedLine(ax.c2p(0, -r), ax.c2p(2*PI, -r), color=YELLOW)
        klab = MathTex("k=3", font_size=36, color=MUTED).to_corner(UR).shift(LEFT*0.5)
        nt = ValueTracker(10)
        def samples():
            nn = int(nt.get_value()); vg = VGroup()
            for j in range(nn):
                t = 2*PI*j/nn
                for s, col in ((1, BLUE), (-1, ORANGE)):
                    y = lam(t, k, s)
                    bad = abs(y) > r and j != 0 and not (nn % 2 == 0 and j == nn//2)
                    vg.add(Dot(ax.c2p(t, y), radius=0.06, color=RED if bad else col))
            return vg
        pts = always_redraw(samples)
        nlab = always_redraw(lambda: MathTex(f"n={int(nt.get_value())}", font_size=36).next_to(klab, DOWN))
        self.hold(5, ([Create(ax), FadeIn(xl), FadeIn(klab)], 1.5), ([Create(cp), Create(cm)], 2.5), ([Create(hp), Create(hm)], 1),
                  ([FadeIn(pts), FadeIn(nlab)], 1), ([nt.animate.set_value(32)], 5), ([nt.animate.set_value(40)], 2))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S08
class S08(BeatScene):
    SCENE_ID = 'S08'
    def construct(self):
        goal = MathTex(r"-2\sqrt2\ \le\ \lambda_-\ \le\ \lambda_+\ \le\ 2\sqrt2 \quad ?", font_size=44).to_edge(UP, buff=0.7)
        self.hold(1, ([Write(goal)], 2.5))
        e1 = MathTex(r"A=\alpha+\beta,\quad P=\alpha\beta", font_size=38).next_to(goal, DOWN, buff=0.6)
        e2 = MathTex(r"\lambda_+\le2\sqrt2 \iff \sqrt{(\alpha-\beta)^2+4}\ \le\ 4\sqrt2-A", font_size=38).next_to(e1, DOWN, buff=0.5)
        e3 = MathTex(r"|A|\le4<4\sqrt2\ \Rightarrow\ \text{RHS}>0\ \Rightarrow\ \text{squaring is an equivalence}", font_size=32, color=GREEN).next_to(e2, DOWN, buff=0.4)
        self.hold(2, ([Write(e1)], 1.5), ([Write(e2)], 2.5), ([Write(e3)], 2.5))
        e4 = MathTex(r"2\sqrt2\,A-P\le7,\qquad -2\sqrt2\,A-P\le7", font_size=38).next_to(e3, DOWN, buff=0.5)
        e5 = MathTex(r"2\sqrt2\,|A|\ \le\ 7+P", font_size=44, color=YELLOW).next_to(e4, DOWN, buff=0.5)
        self.hold(3, ([Write(e4)], 2.5), ([Write(e5)], 2))
        self.play(FadeOut(e1), FadeOut(e2), FadeOut(e3), FadeOut(e4), e5.animate.next_to(goal, DOWN, buff=0.6), run_time=1)
        e6 = MathTex(r"|P|\le4\ \Rightarrow\ 7+P\ge3>0\ \Rightarrow\ \text{square again}", font_size=32, color=GREEN).next_to(e5, DOWN, buff=0.5)
        e7 = MathTex(r"8A^{2}\ \le\ (7+P)^{2}", font_size=44, color=YELLOW).next_to(e6, DOWN, buff=0.5)
        self.hold(4, ([Write(e6)], 2.5), ([Write(e7)], 2))
        e8 = MathTex(r"\alpha=2u,\quad \beta=2T_k(u),\quad u=\cos\tfrac{2\pi j}{n}", font_size=36).next_to(e7, DOWN, buff=0.5)
        e9 = MathTex(r"D_k(u)=\bigl(7+4u\,T_k(u)\bigr)^{2}-8\bigl(2u+2T_k(u)\bigr)^{2}\ \in\ \mathbb Z[u],\qquad \deg D_k=2k+2", font_size=36, color=TEAL).next_to(e8, DOWN, buff=0.5)
        self.hold(5, ([Write(e8)], 2.5), ([Write(e9)], 3))
        self.play(FadeOut(goal), FadeOut(e5), FadeOut(e6), FadeOut(e7), FadeOut(e8), e9.animate.to_edge(UP, buff=0.7), run_time=1)
        k = 3
        T = np.polynomial.chebyshev.Chebyshev.basis(k)
        def Dk(u): return (7+4*u*T(u))**2 - 8*(2*u+2*T(u))**2
        ax = Axes(x_range=[-1, 1, 0.5], y_range=[-20, 60, 20], x_length=10, y_length=3.8,
                  axis_config={"include_tip": False, "color": MUTED}, x_axis_config={"include_numbers": True}, y_axis_config={"include_numbers": True}).shift(DOWN*0.6)
        cur = ax.plot(Dk, x_range=[-1, 1, 0.005], color=BLUE)
        nn = 20
        pts = VGroup(*[Dot(ax.c2p(np.cos(2*PI*j/nn), Dk(np.cos(2*PI*j/nn))), radius=0.07, color=RED if Dk(np.cos(2*PI*j/nn)) < 0 else GREEN) for j in range(1, nn) if j != nn//2])
        cap = MathTex(r"\text{Ramanujan}\iff D_k(u_j)\ge0\ \text{ at every nontrivial grid point}", font_size=32).to_edge(DOWN, buff=0.35)
        self.hold(6, ([Create(ax)], 1.5), ([Create(cur)], 2), ([FadeIn(pts, lag_ratio=0.05)], 2), ([Write(cap)], 2))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
