from lib import *

# ---------------------------------------------------------------- E10S01  Fibonacci
class E10S01(BeatScene):
    SCENE_ID = 'E10S01'
    def construct(self):
        t = title_card("Episode 10", "Recurrences, and the exact ceiling on the matrix method")
        self.hold(1, ([FadeIn(t)], 1.5), ([FadeOut(t)], 0.5), ([FadeIn(header("Recurrences: Fibonacci first"))], 0.8),
                  ([Write(MathTex(r"1,\ 1,\ 2,\ 3,\ 5,\ 8,\ 13,\ \dots\qquad F_{i+1}=F_i+F_{i-1}", font_size=38).shift(UP*1.8))], 2.5),
                  ([FadeIn(defn("linear recurrence of order 2", "each term is determined by the two before it", width=50).shift(UP*0.6))], 2))
        fw = VGroup(MathTex(r"\text{forward: }F_{i+1}=F_i+F_{i-1};\qquad\text{backward: }F_{i-1}=F_{i+1}-F_i", font_size=30),
                    MathTex(r"\text{two consecutive values pin down the whole two-sided sequence}", font_size=28, color=YELLOW),
                    MathTex(r"\text{start }2,5:\quad 2,\ 5,\ 7,\ 12,\ 19,\ \dots\ \text{(same rule, different sequence)}", font_size=28, color=MUTED)).arrange(DOWN, buff=0.3).shift(DOWN*1.2)
        self.hold(2, ([Write(fw[0])], 3), ([FadeIn(fw[1])], 2), ([Write(fw[2])], 2.5))
        self.play(FadeOut(fw), run_time=0.4)
        dim = card("solution space", [MathTex(r"\text{order }2:\ \text{choose 2 numbers, the rest follows}\ \Rightarrow\ \text{2-dimensional}", font_size=28),
                                      MathTex(r"\text{order }m\ (\text{oldest coefficient}\ne0\text{ so it runs backward}):\ m\text{-dimensional}", font_size=28, color=GREEN)], color=GREEN, width=68).shift(DOWN*1.0)
        self.hold(3, ([FadeIn(dim)], 3.5))
        self.play(FadeOut(dim), run_time=0.4)
        circ = Circle(radius=1.3, color=MUTED).shift(LEFT*3.5+DOWN*1.2)
        pts = VGroup(*[Dot(circ.point_at_angle(PI/2 - 2*PI*i/10), color=INK, radius=0.07) for i in range(10)])
        per = VGroup(Text("positions on a circle of length n: position n is position 0 again", font_size=24),
                     Text("a solution must agree with itself after one full turn", font_size=24),
                     Text("those that do are the solutions with period n", font_size=26, color=YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(DOWN*1.2)
        self.hold(4, ([Create(circ), FadeIn(pts)], 1.5), ([FadeIn(per, lag_ratio=0.3)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E10S02  Kernel equations
class E10S02(BeatScene):
    SCENE_ID = 'E10S02'
    def construct(self):
        h = header("A matrix on P(n,k), and its kernel equations")
        k = 3; N = 11; dx = 1.15; x0 = -(N-1)/2*dx
        xp = [np.array([x0+i*dx, 1.5, 0]) for i in range(N)]; yp = [np.array([x0+i*dx, -0.3, 0]) for i in range(N)]
        outer = VGroup(*[Line(xp[i], xp[i+1], color=BLUE, stroke_width=3) for i in range(N-1)])
        spokes = VGroup(*[Line(xp[i], yp[i], color=MUTED, stroke_width=2) for i in range(N)])
        inner = VGroup(*[ArcBetweenPoints(yp[i], yp[i+k], angle=PI/2, color=ORANGE, stroke_width=2.5) for i in range(N-k)])
        xd = VGroup(*[Dot(p, radius=0.08, color=INK) for p in xp]); yd = VGroup(*[Dot(p, radius=0.08, color=INK) for p in yp])
        xl = VGroup(*[MathTex(f"x_{{i{i-5:+d}}}" if i != 5 else "x_i", font_size=20).next_to(xp[i], UP, buff=0.15) for i in range(N)])
        yl = VGroup(*[MathTex(f"y_{{i{i-5:+d}}}" if i != 5 else "y_i", font_size=20).next_to(yp[i], DOWN, buff=0.15) for i in range(N)])
        names = VGroup(MathTex(r"b_i\ (u_i\!\to\!u_{i+1}),\ b_i'\ \text{reverse}", font_size=24, color=BLUE), MathTex(r"c_i\ (u_i\!\to\!v_i),\ c_i'", font_size=24, color=MUTED),
                       MathTex(r"e_i\ (v_i\!\to\!v_{i+k}),\ e_i'", font_size=24, color=ORANGE), MathTex(r"a_i,\ d_i\ \text{diagonal (free)};\ \text{all }b,c,e\ne0", font_size=24)).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.4)
        self.hold(5, ([FadeIn(h), Create(outer), FadeIn(xd), FadeIn(xl)], 1.5), ([Create(spokes), FadeIn(yd), FadeIn(yl), Create(inner)], 1.5), ([FadeIn(names)], 3))
        self.play(FadeOut(names), run_time=0.4)
        rowu = MathTex(r"\text{row }u_i:\quad b'_{i-1}x_{i-1}+a_ix_i+b_ix_{i+1}+c_i\,y_i=0", font_size=32).to_edge(DOWN, buff=1.2)
        hi = VGroup(xd[4], xd[5], xd[6], yd[5]).copy().set_color(YELLOW)
        self.hold(6, ([Write(rowu)], 3), ([FadeIn(hi)], 1.5))
        solve = MathTex(r"\Rightarrow\quad y_i=-\frac{b'_{i-1}x_{i-1}+a_ix_i+b_ix_{i+1}}{c_i}\qquad(c_i\ne0)", font_size=32, color=GREEN).to_edge(DOWN, buff=0.35)
        self.hold(7, ([Write(solve)], 3), ([FadeIn(Text("every inner coordinate is determined by the outer ones", font_size=24, color=YELLOW).next_to(rowu, UP, buff=0.25))], 2))
        self.clear_all()

# ---------------------------------------------------------------- E10S03  Elimination
class E10S03(BeatScene):
    SCENE_ID = 'E10S03'
    def construct(self):
        h = header("Eliminating the inner coordinates")
        k = 3; N = 11; dx = 1.15; x0 = -(N-1)/2*dx
        xp = [np.array([x0+i*dx, 1.5, 0]) for i in range(N)]; yp = [np.array([x0+i*dx, -0.3, 0]) for i in range(N)]
        outer = VGroup(*[Line(xp[i], xp[i+1], color=BLUE, stroke_width=3) for i in range(N-1)])
        spokes = VGroup(*[Line(xp[i], yp[i], color=MUTED, stroke_width=2) for i in range(N)])
        inner = VGroup(*[ArcBetweenPoints(yp[i], yp[i+k], angle=PI/2, color=ORANGE, stroke_width=2.5) for i in range(N-k)])
        xd = VGroup(*[Dot(p, radius=0.08, color=INK) for p in xp]); yd = VGroup(*[Dot(p, radius=0.08, color=INK) for p in yp])
        self.add(h, outer, spokes, inner, xd, yd)
        rowv = MathTex(r"\text{row }v_i:\ e'_{i-k}y_{i-k}+d_iy_i+e_iy_{i+k}+c'_ix_i=0", font_size=30).to_edge(DOWN, buff=1.3)
        yh = VGroup(*[Circle(radius=0.17, color=ORANGE, stroke_width=3).move_to(yp[i]) for i in (5-k, 5, 5+k)])
        sub = Text("substitute the three-term expression for each y", font_size=24, color=MUTED).to_edge(DOWN, buff=0.5)
        self.hold(8, ([Write(rowv), FadeIn(yh)], 3), ([FadeIn(sub)], 2))
        nine = [5-k-1, 5-k, 5-k+1, 4, 5, 6, 5+k-1, 5+k, 5+k+1]
        hl = VGroup(*[Circle(radius=0.17, color=YELLOW, stroke_width=3).move_to(xp[i]) for i in nine])
        rec = MathTex(r"\sum_{p=-k-1}^{k+1}\gamma_{i,p}\,x_{i+p}=0\qquad\text{nine positions, window width }2k+3", font_size=30, color=GREEN).to_edge(DOWN, buff=0.5)
        self.hold(9, ([FadeOut(sub), FadeOut(rowv)], 0.3), ([FadeIn(hl, lag_ratio=0.1)], 2.5), ([Write(rec)], 3))
        self.play(FadeOut(rec), FadeOut(yh), run_time=0.4)
        ends = MathTex(r"\gamma_{i,k+1}=-\frac{e_i\,b_{i+k}}{c_{i+k}}\ne0,\qquad \gamma_{i,-k-1}=-\frac{e'_{i-k}\,b'_{i-k-1}}{c_{i-k}}\ne0", font_size=30).to_edge(DOWN, buff=1.1)
        self.hold(10, ([Write(ends)], 3), ([hl[0].animate.set_color(RED), hl[-1].animate.set_color(RED)], 1.5))
        ordr = Text("a linear recurrence of order exactly 2k+2 (coefficients vary with position)", font_size=26, color=YELLOW).to_edge(DOWN, buff=0.4)
        self.hold(11, ([FadeIn(ordr)], 2.5))
        self.clear_all()

# ---------------------------------------------------------------- E10S04  Monodromy
class E10S04(BeatScene):
    SCENE_ID = 'E10S04'
    def construct(self):
        h = header("Going once around: the monodromy")
        a = VGroup(MathTex(r"\text{order }2k+2\ \Rightarrow\ \text{on a line: solution space of dimension }2k+2", font_size=30),
                   Text("on the circle of length n: a kernel vector must agree with itself after one full turn", font_size=26, color=MUTED)).arrange(DOWN, buff=0.3).next_to(h, DOWN, buff=0.5)
        self.hold(12, ([FadeIn(h)], 0.8), ([Write(a[0])], 3), ([FadeIn(a[1])], 2.5))
        n = 14; R = 1.6; c = LEFT*3.8+DOWN*1.3
        ring = VGroup(*[Square(side_length=0.36, color=TEAL, fill_opacity=0.2).move_to(c + R*np.array([np.cos(PI/2-2*PI*i/n), np.sin(PI/2-2*PI*i/n), 0])).rotate(-2*PI*i/n) for i in range(n)])
        tl = VGroup(*[MathTex(f"T_{{{i}}}", font_size=16).move_to(ring[i]) for i in range(n)])
        d1 = defn("monodromy T", [MathTex(r"T=T_{n-1}\cdots T_1T_0:\ \text{run the recurrence }n\text{ steps}", font_size=26),
                                   MathTex(r"\text{a }(2k+2)\times(2k+2)\text{ matrix: block of starting values}\ \mapsto\ \text{block one turn later}", font_size=24)], width=44).to_edge(RIGHT, buff=0.4).shift(DOWN*1.0)
        self.hold(13, ([FadeIn(ring, lag_ratio=0.05), FadeIn(tl, lag_ratio=0.05)], 2.5), ([FadeIn(d1)], 3))
        self.play(FadeOut(a), run_time=0.4)
        fix = VGroup(MathTex(r"\text{period }n\iff Tv=v\iff(T-I)v=0", font_size=32),
                     MathTex(r"\ker A\ \cong\ \ker(T-I)", font_size=34, color=GREEN),
                     MathTex(r"\operatorname{null}A=\dim\ker(T-I)\ \le\ 2k+2,\quad\text{with equality}\iff T=I", font_size=30, color=YELLOW)).arrange(DOWN, buff=0.3).next_to(h, DOWN, buff=0.4)
        self.hold(14, ([Write(fix[0])], 2.5), ([Write(fix[1])], 2), ([Write(fix[2])], 3))
        self.play(FadeOut(ring), FadeOut(tl), FadeOut(d1), run_time=0.4)
        thm = card("the ceiling theorem", [MathTex(r"\text{every }A\text{ with the }P(n,k)\text{ pattern (symmetric or not):}", font_size=28),
                                           MathTex(r"\operatorname{null}A\le2k+2,\qquad \operatorname{null}A=2k+2\iff T=I", font_size=36, color=YELLOW)], color=YELLOW, width=66).shift(DOWN*1.3)
        self.hold(15, ([FadeIn(thm)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E10S05  Why it matters
class E10S05(BeatScene):
    SCENE_ID = 'E10S05'
    def construct(self):
        h = header("Why the ceiling matters")
        a = VGroup(Text("2k+2 is not new: it is the upper bound on Z.  New: the identification.", font_size=26),
                   Text("the ceiling of the matrix method = the bound it is trying to match", font_size=28, weight=BOLD),
                   Text("no slack on either side: either T = I proves Z = 2k+2, or nothing in this family of methods can", font_size=24, color=YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(h, DOWN, buff=0.5)
        self.hold(16, ([FadeIn(a, lag_ratio=0.3)], 5))
        n, k = 12, 2
        g, d = petersen(n, k, R_out=1.7, R_in=0.85, center=LEFT*4.2+DOWN*1.5, dot_r=0.09)
        for i in range(2*k+2): d['u'][i].set_color(BLUE)
        b = VGroup(Text("a nonzero kernel vector cannot vanish on 2k+2 consecutive outer vertices", font_size=24),
                   Text("= the forcing set of the 2020 bound", font_size=24),
                   MathTex(r"\text{order of the recurrence}=|S|=2k+2:\ \text{two views of one fact}", font_size=28, color=GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).shift(DOWN*1.2)
        self.hold(17, ([FadeIn(g)], 1.5), ([FadeIn(b, lag_ratio=0.3)], 4))
        self.play(FadeOut(b), FadeOut(g), FadeOut(a), run_time=0.4)
        c = card("a claim of ours, corrected", "An earlier version described the matrix method as capped near 6–8. That was a property of the constructions tried so far, not of the method. The cap is 2k+2 and nothing less.", color=RED, width=64).next_to(h, DOWN, buff=0.5)
        self.hold(18, ([FadeIn(c)], 3))
        dd = card("a bound a search cannot cross", "Twice a numerical search returned a nullity above 2k+2. Both times impossible by the theorem; both times a bug, found.\nWrapping a search inside a bound it cannot exceed is the only thing that tells you an answer is wrong when it looks right.", color=GREEN, width=64).next_to(c, DOWN, buff=0.4)
        self.hold(19, ([FadeIn(dd)], 3.5))
        self.clear_all()

# ---------------------------------------------------------------- E10S06  Recap
class E10S06(BeatScene):
    SCENE_ID = 'E10S06'
    def construct(self):
        h = header("Recap: what you can now do")
        b = bullets(["explain a linear recurrence of order m via Fibonacci; why its solution space is m-dimensional",
                     "name the entries of a matrix with the P(n,k) pattern",
                     "write the outer-vertex kernel equation and solve it for y_i",
                     "explain the nine-term relation with nonzero extreme coefficients: order 2k+2",
                     "define the monodromy T; kernel vectors ↔ vectors fixed by T",
                     "state the ceiling theorem and why it means no slack"], font_size=26, width=70).next_to(h, DOWN, buff=0.6)
        self.hold(20, ([FadeIn(h)], 0.8), ([FadeIn(b, lag_ratio=0.2)], 5))
        nxt = Text("Next: the first certificates — a nullity-6 matrix for P(12,2) by hand", font_size=28, color=YELLOW).to_edge(DOWN, buff=0.7)
        self.hold(21, ([FadeIn(nxt)], 1.5))
        self.clear_all()
