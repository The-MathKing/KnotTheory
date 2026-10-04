from lib import *

# ---------------------------------------------------------------- E04S01  Classical zeta
class E04S01(BeatScene):
    SCENE_ID = 'E04S01'
    def construct(self):
        t = title_card("Episode 4", "Why this is called a Riemann Hypothesis")
        self.hold(1, ([FadeIn(t)], 1.5))
        self.play(FadeOut(t), run_time=0.5)
        h = header("The classical zeta function in two minutes")
        z = MathTex(r"\zeta(s)=1+\frac1{2^s}+\frac1{3^s}+\frac1{4^s}+\cdots=\sum_{n\ge1}\frac1{n^s}", font_size=40).next_to(h, DOWN, buff=0.5)
        facts = VGroup(MathTex(r"\zeta(2)=\frac{\pi^2}{6},\qquad \zeta(1)=\infty", font_size=32),
                       wrap("Riemann Hypothesis (1859, open): every zero with 0 < Re s < 1 has Re s = 1/2.", 60, 26, YELLOW)).arrange(DOWN, buff=0.35).next_to(z, DOWN, buff=0.5)
        self.hold(2, ([FadeIn(h)], 0.8), ([Write(z)], 2.5), ([FadeIn(facts[0])], 1.5), ([FadeIn(facts[1])], 2.5))
        self.play(FadeOut(facts), run_time=0.4)
        e = MathTex(r"\zeta(s)=\prod_{p\ \mathrm{prime}}\frac1{1-p^{-s}}\qquad\text{(Euler product)}", font_size=36).next_to(z, DOWN, buff=0.5)
        pnt = wrap("Zeros of ζ control how primes are distributed: the prime number theorem (about x / log x primes below x) is a statement about where ζ is nonzero.", 64, 26, MUTED).next_to(e, DOWN, buff=0.4)
        self.hold(3, ([Write(e)], 2.5), ([FadeIn(pnt)], 3))
        self.clear_all()

# ---------------------------------------------------------------- E04S02  Prime cycles
class E04S02(BeatScene):
    SCENE_ID = 'E04S02'
    def construct(self):
        h = header("Prime cycles in a graph")
        d1 = defn("prime cycle", "A closed walk with no backtracking (never step along an edge and straight back) and no repetition (not a shorter closed walk traced several times), up to starting point.", width=62).next_to(h, DOWN, buff=0.4)
        self.hold(4, ([FadeIn(h)], 0.8), ([FadeIn(d1)], 3))
        self.play(d1.animate.scale(0.7).to_corner(UR, buff=0.4).shift(DOWN*0.9), run_time=0.6)
        c = LEFT*3.5+DOWN*0.9
        pts = ring_points(3, R=1.4, center=c)
        g, dots, lines, labs = simple_graph(pts, [(0,1),(1,2),(2,0)], labels=["0","1","2"], label_dir=[UP, DL, DR])
        self.play(Create(lines), FadeIn(dots), FadeIn(labs), run_time=1)
        arr1 = VGroup(*[Arrow(pts[i], pts[(i+1)%3], buff=0.2, color=GREEN, stroke_width=4) for i in range(3)])
        arr2 = VGroup(*[Arrow(pts[i], pts[(i-1)%3], buff=0.2, color=TEAL, stroke_width=4) for i in range(3)]).shift(RIGHT*0.0)
        items = VGroup(MathTex(r"0\to1\to2\to0:\ \text{prime, length }3", font_size=28, color=GREEN),
                       MathTex(r"0\to2\to1\to0:\ \text{a different prime cycle}", font_size=28, color=TEAL),
                       MathTex(r"\text{twice around (length 6): not prime}", font_size=28, color=RED),
                       MathTex(r"0\to1\to0:\ \text{backtracking, not allowed}", font_size=28, color=RED)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(DOWN*1.0)
        self.hold(5, ([FadeIn(arr1), FadeIn(items[0])], 2), ([FadeOut(arr1), FadeIn(arr2), FadeIn(items[1])], 2), ([FadeOut(arr2), FadeIn(items[2])], 2), ([FadeIn(items[3])], 2))
        self.play(FadeOut(items), FadeOut(g), run_time=0.5)
        pts4 = [c + p for p in [LEFT*1.1+UP*1.1, RIGHT*1.1+UP*1.1, RIGHT*1.1+DOWN*1.1, LEFT*1.1+DOWN*1.1]]
        g4, *_ = simple_graph(pts4, [(0,1),(1,2),(2,3),(3,0)], dot_r=0.1)
        more = VGroup(MathTex(r"C_4:\ \text{two prime cycles of length }4,\ \text{nothing shorter}", font_size=28),
                      MathTex(r"\text{Petersen: }12\ \text{five-cycles}\times2\ \text{directions}=24\ \text{prime cycles of length }5", font_size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5).shift(DOWN*1.0)
        self.hold(6, ([FadeIn(g4), FadeIn(more[0])], 2), ([FadeIn(more[1])], 2.5))
        self.clear_all()

# ---------------------------------------------------------------- E04S03  Ihara zeta
class E04S03(BeatScene):
    SCENE_ID = 'E04S03'
    def construct(self):
        h = header("The Ihara zeta function")
        z = MathTex(r"\zeta_X(u)=\prod_{[C]\ \text{prime cycle}}\frac{1}{1-u^{\ell(C)}}\qquad u\leftrightarrow p^{-s},\ \ q=\text{degree}-1=2", font_size=34).next_to(h, DOWN, buff=0.5)
        self.hold(7, ([FadeIn(h)], 0.8), ([Write(z)], 3))
        props = VGroup(Text("Euler product (by definition)", font_size=26), Text("functional equation  u ↔ 1/(q u)", font_size=26),
                       Text("prime number theorem for prime cycles", font_size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(z, DOWN, buff=0.5)
        rh = card("graph Riemann Hypothesis", [MathTex(r"u=q^{-s}:\ \text{do all poles with }0<\mathrm{Re}\,s<1\ \text{lie on }\mathrm{Re}\,s=\tfrac12\,?", font_size=30)], color=YELLOW, width=60).next_to(props, DOWN, buff=0.5)
        self.hold(8, ([FadeIn(props, lag_ratio=0.3)], 2.5), ([FadeIn(rh)], 3))
        note = wrap("Classical ζ: zeros. Graph ζ: poles (it is a product of reciprocals). Same shape: everything interesting on one vertical line.", 84, 22, MUTED).next_to(rh, DOWN, buff=0.3)
        self.hold(9, ([FadeIn(note)], 2.5))
        self.clear_all()

# ---------------------------------------------------------------- E04S04  Determinant formula
class E04S04(BeatScene):
    SCENE_ID = 'E04S04'
    def construct(self):
        h = header("Ihara's determinant formula")
        det = MathTex(r"\zeta_X(u)^{-1}=(1-u^2)^{|E|-|V|}\,\det\bigl(I-uA+2u^2I\bigr)\qquad(\text{cubic }X)", font_size=36).next_to(h, DOWN, buff=0.5)
        self.hold(10, ([FadeIn(h)], 0.8), ([Write(det)], 3))
        s1 = VGroup(Text("pole of ζ = zero of the reciprocal", font_size=28),
                    MathTex(r"(1-u^2)=0\ \text{at }u=\pm1:\ \text{outside the strip, ignore}", font_size=28, color=MUTED),
                    MathTex(r"\det(\cdots)=0\iff I-uA+2u^2I\ \text{is singular}", font_size=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(det, DOWN, buff=0.5)
        self.hold(11, ([FadeIn(s1[0])], 1.5), ([FadeIn(s1[1])], 2), ([Write(s1[2])], 2))
        s2 = VGroup(MathTex(r"Ax=\lambda x\ \Rightarrow\ (I-uA+2u^2I)\,x=(1-\lambda u+2u^2)\,x", font_size=32),
                    MathTex(r"\text{poles of }\zeta_X\ =\ \text{roots of }\ 2u^2-\lambda u+1=0,\ \text{ one quadratic per eigenvalue }\lambda", font_size=30, color=YELLOW)).arrange(DOWN, buff=0.35).next_to(s1, DOWN, buff=0.5)
        self.hold(12, ([Write(s2[0])], 3), ([Write(s2[1])], 3))
        self.clear_all()

# ---------------------------------------------------------------- E04S05  Two-line computation
class E04S05(BeatScene):
    SCENE_ID = 'E04S05'
    def construct(self):
        h = header("The two-line computation")
        q = MathTex(r"2u^2-\lambda u+1=0\quad\Rightarrow\quad u=\frac{\lambda\pm\sqrt{\lambda^2-8}}{4}", font_size=40).next_to(h, DOWN, buff=0.5)
        self.hold(13, ([FadeIn(h)], 0.8), ([Write(q)], 3))
        c1 = card("Case 1: λ² < 8, i.e. |λ| < 2√2", [MathTex(r"\sqrt{\lambda^2-8}\ \text{imaginary}\ \Rightarrow\ \text{conjugate roots } u,\bar u", font_size=28),
                                                      MathTex(r"u\bar u=\tfrac12\ \Rightarrow\ |u|^2=\tfrac12\ \Rightarrow\ |u|=\tfrac1{\sqrt2}", font_size=30, color=GREEN)], color=GREEN, width=56).next_to(q, DOWN, buff=0.4)
        self.hold(14, ([FadeIn(c1)], 3.5))
        tr = VGroup(MathTex(r"u=2^{-s}:\quad |u|=2^{-\mathrm{Re}\,s}=2^{-1/2}\ \Rightarrow\ \mathrm{Re}\,s=\tfrac12\ \ \text{on the line}", font_size=30, color=GREEN),
                    MathTex(r"\text{Case 2: }\lambda^2>8:\ \text{two different real roots with product }\tfrac12\ \Rightarrow\ \text{off the line}", font_size=28, color=RED)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(c1, DOWN, buff=0.4)
        self.hold(15, ([Write(tr[0])], 3), ([Write(tr[1])], 3))
        self.play(FadeOut(c1), FadeOut(tr), run_time=0.4)
        tab = MathTex(r"\begin{array}{c|c|c}\lambda & u & |u|\\ \hline 1 & 0.25\pm0.661i & 0.707\\ -2 & -0.5\pm0.5i & 0.707\\ 2.9 & 0.885,\ 0.565 & \text{different}\end{array}", font_size=32).next_to(q, DOWN, buff=0.5)
        # complex plane picture
        pl = NumberPlane(x_range=[-1.2, 1.2, 0.5], y_range=[-1.0, 1.0, 0.5], x_length=3.6, y_length=3.0, background_line_style={"stroke_color": GRID, "stroke_width": 1}).to_edge(RIGHT, buff=0.6).shift(DOWN*1.2)
        circ = Circle(radius=pl.c2p(1/np.sqrt(2), 0)[0]-pl.c2p(0, 0)[0], color=YELLOW, stroke_width=2).move_to(pl.c2p(0, 0))
        pts = VGroup(Dot(pl.c2p(0.25, 0.661), color=BLUE, radius=0.06), Dot(pl.c2p(0.25, -0.661), color=BLUE, radius=0.06),
                     Dot(pl.c2p(-0.5, 0.5), color=ORANGE, radius=0.06), Dot(pl.c2p(-0.5, -0.5), color=ORANGE, radius=0.06),
                     Dot(pl.c2p(0.885, 0), color=RED, radius=0.06), Dot(pl.c2p(0.565, 0), color=RED, radius=0.06))
        cl = MathTex(r"|u|=1/\sqrt2", font_size=24, color=YELLOW).next_to(pl, DOWN, buff=0.1)
        self.hold(16, ([Write(tab.shift(LEFT*2.5))], 3), ([FadeIn(pl), Create(circ), FadeIn(cl)], 1.5), ([FadeIn(pts, lag_ratio=0.2)], 2))
        self.play(FadeOut(tab), FadeOut(pl), FadeOut(circ), FadeOut(cl), FadeOut(pts), run_time=0.4)
        concl = card("Conclusion", [MathTex(r"\text{poles from }\lambda\text{ lie on }\mathrm{Re}\,s=\tfrac12\iff|\lambda|\le2\sqrt2", font_size=30),
                                     MathTex(r"\text{(trivial }\pm3\text{ give }u=1,\tfrac12:\ \text{edges of the strip, excluded)}", font_size=24, color=MUTED),
                                     MathTex(r"\textbf{RH for }X\iff X\textbf{ is Ramanujan}", font_size=36, color=YELLOW)], color=YELLOW, width=60).next_to(q, DOWN, buff=0.5)
        self.hold(17, ([FadeIn(concl)], 3))
        self.clear_all()

# ---------------------------------------------------------------- E04S06  What the name means
class E04S06(BeatScene):
    SCENE_ID = 'E04S06'
    def construct(self):
        h = header("What the name does and does not mean")
        a = bullets(["the graph RH is a theorem away from a finite eigenvalue check: decidable for a given graph",
                     "the analogy lives in the zeta function (Euler product, functional equation, prime cycle theorem), not in the difficulty",
                     "nobody is claiming anything about the Riemann Hypothesis for the integers"], font_size=26, width=70).next_to(h, DOWN, buff=0.5)
        self.hold(18, ([FadeIn(a, lag_ratio=0.3)], 4))
        q = MathTex(r"\text{Question 1: for which }n,k\text{ does }P(n,k)\text{ satisfy the RH }(=\text{ is Ramanujan})?", font_size=30, color=YELLOW).next_to(a, DOWN, buff=0.5)
        self.hold(19, ([Write(q)], 2.5))
        self.play(FadeOut(a), q.animate.next_to(h, DOWN, buff=0.5), run_time=0.6)
        gs = VGroup(Text("Gera & Stănică (2011): every eigenvalue of P(n,k) in closed form", font_size=26),
                    VGroup(Text("“Ramanujan”", font_size=26, color=RED), Text("“expander”", font_size=26, color=RED), Text("“spectral gap”", font_size=26, color=RED)).arrange(RIGHT, buff=0.6),
                    Text("0 occurrences. The formula and the number 2√2 were never put side by side.", font_size=24, color=MUTED),
                    MathTex(r"\sqrt{\;\cdots\sqrt{\cdots}\;}\ \overset{?}{<}\ 2\sqrt2\quad\text{near equality: computers guess (episode 8)}", font_size=28, color=ORANGE)).arrange(DOWN, buff=0.35).next_to(q, DOWN, buff=0.6)
        self.hold(20, ([FadeIn(gs[0])], 1.5), ([FadeIn(gs[1]), FadeIn(gs[2])], 2.5), ([Write(gs[3])], 2.5))
        self.clear_all()

# ---------------------------------------------------------------- E04S07  Recap
class E04S07(BeatScene):
    SCENE_ID = 'E04S07'
    def construct(self):
        h = header("Recap: what you can now do")
        b = bullets(["state the Riemann zeta function and its Euler product",
                     "define a prime cycle and count them in a triangle",
                     "state the Ihara zeta function",
                     "explain, via eigenvectors, why its poles come from 2u² − λu + 1 = 0",
                     "show |u| = 1/√2 exactly when λ² ≤ 8",
                     "say in one sentence what the graph RH is and is not"], font_size=28, width=62).next_to(h, DOWN, buff=0.6)
        self.hold(21, ([FadeIn(h)], 0.8), ([FadeIn(b, lag_ratio=0.2)], 5))
        nxt = Text("Next: complex numbers, roots of unity, and the 2 × 2 blocks", font_size=30, color=YELLOW).to_edge(DOWN, buff=0.8)
        self.hold(22, ([FadeIn(nxt)], 1.5))
        self.clear_all()
