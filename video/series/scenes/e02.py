from lib import *

C4_PTS = [LEFT*1.2+UP*1.2, RIGHT*1.2+UP*1.2, RIGHT*1.2+DOWN*1.2, LEFT*1.2+DOWN*1.2]
C4_E = [(0,1),(1,2),(2,3),(3,0)]
C4_ROWS = [[0,1,0,1],[1,0,1,0],[0,1,0,1],[1,0,1,0]]
PET_ROWS = [[0,1,0,0,1,1,0,0,0,0],[1,0,1,0,0,0,1,0,0,0],[0,1,0,1,0,0,0,1,0,0],
            [0,0,1,0,1,0,0,0,1,0],[1,0,0,1,0,0,0,0,0,1],[1,0,0,0,0,0,0,1,1,0],
            [0,1,0,0,0,0,0,0,1,1],[0,0,1,0,0,1,0,0,0,1],[0,0,0,1,0,1,1,0,0,0],
            [0,0,0,0,1,0,1,1,0,0]]

def c4(center, labels=None, dot_r=0.12):
    pts = [center + p for p in C4_PTS]
    return simple_graph(pts, C4_E, dot_r=dot_r, labels=labels or ["0","1","2","3"], label_dir=[UL, UR, DR, DL])

def colvec(entries, color=INK, scale=0.8):
    return Matrix([[e] for e in entries], v_buff=0.6).scale(scale).set_color(color)

# ---------------------------------------------------------------- E02S01  Vectors
class E02S01(BeatScene):
    SCENE_ID = 'E02S01'
    def construct(self):
        h = header("Vectors: lists of numbers")
        d1 = defn("vector", "An ordered list of numbers, one per vertex. Written as a column x with entries x₀, x₁, x₂, x₃.", width=56).next_to(h, DOWN, buff=0.4)
        x = colvec([1, 2, 0, -1]).shift(RIGHT*3.5+DOWN*1.3)
        xl = MathTex(r"x=", font_size=40).next_to(x, LEFT)
        self.hold(1, ([FadeIn(h)], 0.8), ([FadeIn(d1)], 2), ([FadeIn(xl), FadeIn(x)], 1.5))
        g, dots, lines, labs = c4(LEFT*3.2+DOWN*1.3)
        vals = VGroup(*[MathTex(str(v), font_size=34, color=YELLOW).next_to(dots[i], [DL, DR, UR, UL][i]*0+[DOWN, DOWN, UP, UP][i], buff=0.35) for i, v in enumerate([1, 2, 0, -1])])
        for i, v in enumerate(vals):
            v.move_to(dots[i].get_center() + [DOWN*0.55+LEFT*0.55, DOWN*0.55+RIGHT*0.55, UP*0.55+RIGHT*0.55, UP*0.55+LEFT*0.55][i])
        self.hold(2, ([Create(lines), FadeIn(dots), FadeIn(labs)], 1.5), ([FadeIn(vals)], 1.5))
        self.play(FadeOut(d1), run_time=0.4)
        add = MathTex(r"\begin{pmatrix}1\\2\\0\\-1\end{pmatrix}+\begin{pmatrix}1\\1\\1\\1\end{pmatrix}=\begin{pmatrix}2\\3\\1\\0\end{pmatrix}", font_size=34).next_to(h, DOWN, buff=0.4).shift(LEFT*2.5)
        mul = MathTex(r"3\begin{pmatrix}1\\2\\0\\-1\end{pmatrix}=\begin{pmatrix}3\\6\\0\\-3\end{pmatrix}", font_size=34).next_to(add, RIGHT, buff=1.2)
        self.hold(3, ([Write(add)], 2), ([Write(mul)], 2))
        self.clear_all()

# ---------------------------------------------------------------- E02S02  Adjacency matrix
class E02S02(BeatScene):
    SCENE_ID = 'E02S02'
    def construct(self):
        h = header("The adjacency matrix")
        d1 = defn("adjacency matrix A", "N rows, N columns. Row x, column y holds 1 if x and y are joined, else 0. Diagonal is 0.", width=56).next_to(h, DOWN, buff=0.4)
        self.hold(4, ([FadeIn(h)], 0.8), ([FadeIn(d1)], 2))
        self.play(d1.animate.scale(0.75).to_corner(UR, buff=0.4).shift(DOWN*0.9), run_time=0.7)
        g, dots, lines, labs = c4(LEFT*4+DOWN*1.2, dot_r=0.11)
        A = int_matrix(C4_ROWS, scale=0.8).shift(RIGHT*0.3+DOWN*1.2)
        Al = MathTex("A=", font_size=40).next_to(A, LEFT)
        self.hold(5, ([Create(lines), FadeIn(dots), FadeIn(labs)], 1.2), ([FadeIn(Al), FadeIn(A.get_brackets())], 0.5),
                  *[([FadeIn(VGroup(*A.get_rows()[r])), Indicate(dots[r], color=YELLOW)], 1.2) for r in range(4)],
                  ([Write(MathTex(r"8\ \text{ones}=2\times4\ \text{edges}", font_size=28, color=MUTED).next_to(A, DOWN, buff=0.4))], 1.5))
        sym = wrap("symmetric: entry (x,y) = entry (y,x). Flip across the diagonal: unchanged.", 26, 24, GREEN).next_to(A, RIGHT, buff=0.7).shift(UP*0.3)
        diag = Line(A.get_corner(UL)+0.2*DR, A.get_corner(DR)+0.2*UL, color=GREEN, stroke_width=2)
        self.hold(6, ([Create(diag)], 1), ([FadeIn(sym)], 1.5))
        self.play(*[FadeOut(m) for m in self.mobjects if m is not h], run_time=0.5)
        P = int_matrix(PET_ROWS, scale=0.5, h_buff=0.7, v_buff=0.55).shift(LEFT*2.2+DOWN*0.6)
        g2, d2 = petersen(5, 2, R_out=1.5, R_in=0.7, center=RIGHT*3.8+DOWN*0.6, dot_r=0.07)
        lab = Text("Petersen: 10 × 10, three 1s per row", font_size=24, color=MUTED).next_to(g2, DOWN, buff=0.3)
        self.hold(7, ([FadeIn(P), FadeIn(g2)], 2), ([Indicate(VGroup(*P.get_rows()[0]), color=YELLOW), Indicate(VGroup(d2['u'][0], d2['u'][1], d2['u'][4], d2['v'][0]), color=YELLOW)], 2), ([FadeIn(lab)], 1.5))
        self.clear_all()

# ---------------------------------------------------------------- E02S03  Multiplying
class E02S03(BeatScene):
    SCENE_ID = 'E02S03'
    def construct(self):
        h = header("Multiplying a matrix by a vector")
        rule = card("Rule", "Entry i of A x = row i of A, multiplied entry-by-entry against x, then summed.", color=YELLOW, width=56).next_to(h, DOWN, buff=0.4)
        self.hold(8, ([FadeIn(h)], 0.8), ([FadeIn(rule)], 2))
        self.play(rule.animate.scale(0.75).next_to(h, DOWN, buff=0.25), run_time=0.6)
        A = int_matrix(C4_ROWS, scale=0.75).shift(LEFT*4.6+DOWN*1.3)
        x = colvec([1, 2, 0, -1]).next_to(A, RIGHT, buff=0.4)
        eq = MathTex("=", font_size=40).next_to(x, RIGHT, buff=0.4)
        res = colvec(["?", "?", "?", "?"]).next_to(eq, RIGHT, buff=0.4)
        self.add(A, x, eq, res)
        work = VGroup()
        texts = [r"0{\cdot}1+1{\cdot}2+0{\cdot}0+1{\cdot}(-1)=1", r"1{\cdot}1+0{\cdot}2+1{\cdot}0+0{\cdot}(-1)=1",
                 r"0{\cdot}1+1{\cdot}2+0{\cdot}0+1{\cdot}(-1)=1", r"1{\cdot}1+0{\cdot}2+1{\cdot}0+0{\cdot}(-1)=1"]
        def step(r):
            row = SurroundingRectangle(VGroup(*A.get_rows()[r]), color=YELLOW, buff=0.08)
            t = MathTex(texts[r], font_size=28).move_to(RIGHT*3.0+UP*0.3+DOWN*0.55*r)
            newres = colvec([1 if i <= r else "?" for i in range(4)]).move_to(res)
            return row, t, newres
        r0, t0, n0 = step(0)
        self.hold(9, ([Create(r0)], 0.8), ([Write(t0)], 2.5), ([Transform(res, n0)], 0.8))
        self.play(FadeOut(r0), run_time=0.3)
        for r in (1, 2, 3):
            rr, tt, nn = step(r)
            if r == 1:
                self.hold(10, ([Create(rr)], 0.6), ([Write(tt)], 2), ([Transform(res, nn), FadeOut(rr)], 0.6))
            else:
                self.play(Create(rr), run_time=0.5); self.play(Write(tt), run_time=1.5); self.play(Transform(res, nn), FadeOut(rr), run_time=0.5)
        self.play(FadeOut(VGroup(t0)), *[FadeOut(m) for m in self.mobjects if isinstance(m, MathTex) and m is not eq and m.get_center()[0] > 1.5], run_time=0.5)
        mean = idea("what it means", "(A x) at vertex i = the sum of x over the neighbours of i.\nMultiplying by A replaces each vertex's number by the sum of its neighbours' numbers.", width=42, font_size=24).to_edge(RIGHT, buff=0.4).shift(DOWN*0.9)
        g, dots, lines, labs = c4(LEFT*4.2+DOWN*0.6, dot_r=0.1)
        self.hold(11, ([FadeOut(A), FadeOut(x), FadeOut(eq), FadeOut(res)], 0.5), ([Create(lines), FadeIn(dots), FadeIn(labs)], 1), ([FadeIn(mean)], 2),
                  ([Indicate(dots[1], color=YELLOW), Indicate(dots[3], color=YELLOW)], 1.5))
        keep = MathTex(r"(Ax)_i=\sum_{j\sim i}x_j", font_size=44, color=YELLOW).next_to(g, DOWN, buff=0.6)
        self.hold(12, ([Write(keep)], 2))
        self.clear_all()

# ---------------------------------------------------------------- E02S04  Eigenvectors
class E02S04(BeatScene):
    SCENE_ID = 'E02S04'
    def construct(self):
        h = header("Eigenvectors: vectors the matrix only stretches")
        g, dots, lines, labs = c4(LEFT*4.2+DOWN*0.8, dot_r=0.11)
        def show_vals(vals, color=YELLOW):
            vg = VGroup()
            for i, v in enumerate(vals):
                vg.add(MathTex(str(v), font_size=32, color=color).move_to(dots[i].get_center() + [DOWN*0.55+LEFT*0.55, DOWN*0.55+RIGHT*0.55, UP*0.55+RIGHT*0.55, UP*0.55+LEFT*0.55][i]))
            return vg
        v1 = show_vals([1, 1, 1, 1])
        e1 = MathTex(r"A\begin{pmatrix}1\\1\\1\\1\end{pmatrix}=\begin{pmatrix}2\\2\\2\\2\end{pmatrix}=2\begin{pmatrix}1\\1\\1\\1\end{pmatrix}", font_size=34).shift(RIGHT*2.5+UP*1.2)
        self.hold(13, ([FadeIn(h), Create(lines), FadeIn(dots), FadeIn(labs)], 1.2), ([FadeIn(v1)], 1), ([Write(e1)], 2.5))
        d1 = defn("eigenvector, eigenvalue", "x ≠ 0 with A x = λ x. The matrix only stretches x, by the factor λ (the eigenvalue).", width=44, font_size=24).shift(RIGHT*2.5+DOWN*1.4)
        self.hold(14, ([FadeIn(d1)], 2))
        v2 = show_vals([1, -1, 1, -1], color=ORANGE)
        e2 = MathTex(r"A\begin{pmatrix}1\\-1\\1\\-1\end{pmatrix}=\begin{pmatrix}-2\\2\\-2\\2\end{pmatrix}=-2\begin{pmatrix}1\\-1\\1\\-1\end{pmatrix}", font_size=34).move_to(e1)
        self.hold(15, ([FadeOut(d1)], 0.3), ([Transform(v1, v2), Transform(e1, e2)], 1.5))
        v3 = show_vals([1, 0, -1, 0], color=TEAL)
        e3 = MathTex(r"A\begin{pmatrix}1\\0\\-1\\0\end{pmatrix}=\begin{pmatrix}0\\0\\0\\0\end{pmatrix}=0\begin{pmatrix}1\\0\\-1\\0\end{pmatrix}", font_size=34).move_to(e1)
        e3b = MathTex(r"\text{also }(0,1,0,-1):\ \text{eigenvalue }0", font_size=28, color=MUTED).next_to(e3, DOWN, buff=0.4)
        self.hold(16, ([Transform(v1, v3), Transform(e1, e3)], 1.5), ([FadeIn(e3b)], 1.5))
        spec = card("spectrum of C₄", [MathTex(r"\{\,2,\ 0,\ 0,\ -2\,\}", font_size=36, color=YELLOW),
                                      wrap("An N × N symmetric matrix has exactly N real eigenvalues, counted with repetition.", 40, 22, MUTED)], color=GREEN).move_to(RIGHT*2.5+DOWN*1.5)
        self.hold(17, ([FadeOut(e3b)], 0.3), ([FadeIn(spec)], 2))
        self.clear_all()

# ---------------------------------------------------------------- E02S05  2x2 solved
class E02S05(BeatScene):
    SCENE_ID = 'E02S05'
    def construct(self):
        h = header("A 2 × 2 example, solved completely")
        A = MathTex(r"A=\begin{pmatrix}2&1\\1&2\end{pmatrix},\qquad A\begin{pmatrix}x\\y\end{pmatrix}=\lambda\begin{pmatrix}x\\y\end{pmatrix}\ ?", font_size=38).next_to(h, DOWN, buff=0.5)
        self.hold(18, ([FadeIn(h)], 0.8), ([Write(A)], 2.5))
        eqs = VGroup(MathTex(r"2x+y=\lambda x,\qquad x+2y=\lambda y", font_size=34),
                     MathTex(r"(2-\lambda)x+y=0,\qquad x+(2-\lambda)y=0", font_size=34),
                     MathTex(r"\text{nonzero solution}\iff(2-\lambda)^2-1\cdot1=0", font_size=34, color=YELLOW)).arrange(DOWN, buff=0.3).next_to(A, DOWN, buff=0.5)
        self.hold(19, ([Write(eqs[0])], 2), ([Write(eqs[1])], 2), ([Write(eqs[2])], 2.5))
        self.play(FadeOut(eqs[0]), FadeOut(eqs[1]), eqs[2].animate.next_to(A, DOWN, buff=0.5), run_time=0.7)
        det = defn("determinant (2 × 2)", [MathTex(r"\det\begin{pmatrix}p&q\\r&s\end{pmatrix}=ps-qr", font_size=32),
                                            MathTex(r"\text{eigenvalues: }(p-\lambda)(s-\lambda)-qr=0\quad\text{(a quadratic in }\lambda)", font_size=28)], width=50).next_to(eqs[2], DOWN, buff=0.4)
        self.hold(20, ([FadeIn(det)], 2.5))
        self.play(FadeOut(det), run_time=0.4)
        sol = VGroup(MathTex(r"(2-\lambda)^2=1\ \Rightarrow\ 2-\lambda=\pm1\ \Rightarrow\ \lambda=3\ \text{or}\ 1", font_size=34),
                     MathTex(r"\lambda=3:\ -x+y=0\ \Rightarrow\ \begin{pmatrix}1\\1\end{pmatrix};\quad A\begin{pmatrix}1\\1\end{pmatrix}=\begin{pmatrix}3\\3\end{pmatrix}\ \checkmark", font_size=32, color=GREEN),
                     MathTex(r"\lambda=1:\ x+y=0\ \Rightarrow\ \begin{pmatrix}1\\-1\end{pmatrix};\quad A\begin{pmatrix}1\\-1\end{pmatrix}=\begin{pmatrix}1\\-1\end{pmatrix}\ \checkmark", font_size=32, color=GREEN)).arrange(DOWN, buff=0.3).next_to(eqs[2], DOWN, buff=0.4)
        self.hold(21, ([Write(sol[0])], 2), ([Write(sol[1])], 2.5), ([Write(sol[2])], 2.5))
        self.play(FadeOut(sol), FadeOut(eqs[2]), run_time=0.4)
        sc = idea("shortcut", [MathTex(r"\lambda_1+\lambda_2=\text{trace}=p+s,\qquad \lambda_1\lambda_2=\det=ps-qr", font_size=30),
                               MathTex(r"\text{here: }3+1=4=2+2,\quad 3\cdot1=3=2\cdot2-1\cdot1", font_size=28, color=MUTED),
                               MathTex(r"\lambda^2-(\text{trace})\lambda+\det=0", font_size=34, color=YELLOW)], width=50).next_to(A, DOWN, buff=0.5)
        self.hold(22, ([FadeIn(sc)], 2.5))
        self.clear_all()

# ---------------------------------------------------------------- E02S06  Eigenvalue 3
class E02S06(BeatScene):
    SCENE_ID = 'E02S06'
    def construct(self):
        h = header("Why every cubic graph has eigenvalue 3")
        g, d = petersen(5, 2, R_out=1.7, R_in=0.8, center=LEFT*4+DOWN*0.8, dot_r=0.08)
        ones = VGroup(*[MathTex("1", font_size=22, color=YELLOW).move_to(LEFT*4+DOWN*0.8 + (p-(LEFT*4+DOWN*0.8))*1.18) for p in d['upos']])
        e = MathTex(r"A\,\mathbf 1=3\cdot\mathbf 1\qquad(\text{each vertex sums three 1s})", font_size=34).shift(RIGHT*2+UP*1.5)
        e2 = MathTex(r"d\text{-regular}\ \Rightarrow\ \text{eigenvalue } d", font_size=30, color=MUTED).next_to(e, DOWN, buff=0.3)
        self.hold(23, ([FadeIn(h), FadeIn(g), FadeIn(ones)], 1.2), ([Write(e)], 2), ([FadeIn(e2)], 1.5))
        pf = VGroup(MathTex(r"Ax=\lambda x,\quad m=\text{where }|x_m|\text{ is largest}", font_size=30),
                    MathTex(r"|\lambda x_m|=|(Ax)_m|=\Bigl|\sum_{3\text{ nbrs}}x_j\Bigr|\le3|x_m|", font_size=30),
                    MathTex(r"\Rightarrow\ |\lambda|\le3", font_size=36, color=GREEN)).arrange(DOWN, buff=0.3).next_to(e2, DOWN, buff=0.5)
        self.hold(24, ([Write(pf[0])], 2), ([Write(pf[1])], 3), ([Write(pf[2])], 1.5))
        self.clear_all()

# ---------------------------------------------------------------- E02S07  Petersen spectrum
class E02S07(BeatScene):
    SCENE_ID = 'E02S07'
    def construct(self):
        h = header("The spectrum of the Petersen graph")
        ax = NumberLine(x_range=[-3, 3, 1], length=8, include_numbers=True, color=MUTED).shift(DOWN*2.2)
        dots = VGroup(Dot(ax.n2p(3), color=GREEN, radius=0.1), *[Dot(ax.n2p(1)+UP*0.14*i, color=BLUE, radius=0.07) for i in range(5)],
                      *[Dot(ax.n2p(-2)+UP*0.14*i, color=ORANGE, radius=0.07) for i in range(4)])
        spec = MathTex(r"\{\,3^{1},\ 1^{5},\ (-2)^{4}\,\}\qquad 1+5+4=10", font_size=40).next_to(h, DOWN, buff=0.5)
        d1 = defn("multiplicity", "How many times an eigenvalue appears; written as an exponent.", width=50, font_size=24).next_to(spec, DOWN, buff=0.3)
        self.hold(25, ([FadeIn(h), Create(ax)], 1), ([Write(spec)], 2), ([FadeIn(dots, lag_ratio=0.1)], 1.5), ([FadeIn(d1)], 1.5))
        self.play(FadeOut(d1), FadeOut(ax), FadeOut(dots), spec.animate.scale(0.8).to_corner(UR, buff=0.4).shift(DOWN*0.8), run_time=0.6)
        c = LEFT*3.6+DOWN*0.7
        g, d = petersen(5, 2, R_out=2.0, R_in=0.95, center=c, dot_r=0.09)
        vals = {('u', 3): 1, ('u', 4): 1, ('v', 0): -1, ('v', 2): -1}
        labs = VGroup()
        for i in range(5):
            for kind in ('u', 'v'):
                v = vals.get((kind, i), 0)
                p = d['upos'][i] if kind == 'u' else d['vpos'][i]
                f = 1.17 if kind == 'u' else 0.62
                labs.add(MathTex(str(v), font_size=24, color=YELLOW if v else MUTED).move_to(c + (p-c)*f))
        ul = ring_labels(d, 'u', center=c, factor=0.84, tangent=0.32, font_size=18)
        vl = ring_labels(d, 'v', center=c, factor=1.45, tangent=0.3, font_size=16)
        checks = VGroup(MathTex(r"u_3:\ u_2,u_4,v_3\to 0+1+0=1=1\cdot x_{u_3}\ \checkmark", font_size=26, color=GREEN),
                        MathTex(r"v_0:\ v_2,v_3,u_0\to -1+0+0=-1=1\cdot x_{v_0}\ \checkmark", font_size=26, color=GREEN),
                        MathTex(r"u_0:\ u_1,u_4,v_0\to 0+1-1=0=1\cdot x_{u_0}\ \checkmark", font_size=26, color=GREEN),
                        Text("eigenvalue 1 (do the other seven yourself)", font_size=24, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).shift(DOWN*0.6)
        self.hold(26, ([FadeIn(g), FadeIn(labs), FadeIn(ul), FadeIn(vl)], 1.5), ([Indicate(d['u'][3], color=YELLOW), FadeIn(checks[0])], 2.5),
                  ([Indicate(d['v'][0], color=YELLOW), FadeIn(checks[1])], 2.5), ([Indicate(d['u'][0], color=YELLOW), FadeIn(checks[2])], 2.5), ([FadeIn(checks[3])], 1.5))
        self.play(FadeOut(checks), FadeOut(labs), FadeOut(ul), FadeOut(vl), run_time=0.4)
        ax2 = NumberLine(x_range=[-3, 3, 1], length=6, include_numbers=True, color=MUTED).to_edge(RIGHT, buff=1.0).shift(DOWN*1.2)
        gap = DoubleArrow(ax2.n2p(1), ax2.n2p(3), buff=0, color=YELLOW, stroke_width=3).shift(UP*0.5)
        gl = Text("spectral gap = 3 − 1 = 2", font_size=24, color=YELLOW).next_to(gap, UP, buff=0.1).shift(LEFT*0.8)
        dd = VGroup(Dot(ax2.n2p(3), color=GREEN, radius=0.1), Dot(ax2.n2p(1), color=BLUE, radius=0.1), Dot(ax2.n2p(-2), color=ORANGE, radius=0.1))
        self.hold(27, ([Create(ax2), FadeIn(dd)], 1.5), ([GrowArrow(gap), FadeIn(gl)], 1.5))
        self.clear_all()

# ---------------------------------------------------------------- E02S08  Kernel and nullity
class E02S08(BeatScene):
    SCENE_ID = 'E02S08'
    def construct(self):
        h = header("The kernel and the nullity")
        d1 = defn("kernel (null space)", "All vectors x with A x = 0. Always contains the zero vector; the question is what else.", width=56).next_to(h, DOWN, buff=0.4)
        self.hold(28, ([FadeIn(h)], 0.8), ([FadeIn(d1)], 2))
        ex = example("C₄", [MathTex(r"(1,0,-1,0),\ (0,1,0,-1)\ \text{ are in the kernel}", font_size=30),
                            MathTex(r"2(1,0,-1,0)+3(0,1,0,-1)=(2,3,-2,-3)", font_size=30),
                            MathTex(r"\text{vertex }0:\ 3+(-3)=0\ \checkmark", font_size=28, color=MUTED),
                            MathTex(r"\text{two independent directions}\ \Rightarrow\ \text{nullity }2", font_size=30, color=YELLOW)], width=56).next_to(d1, DOWN, buff=0.4)
        self.hold(29, ([FadeIn(ex)], 3))
        d2 = defn("nullity", "Number of independent kernel directions = number of times 0 is an eigenvalue.\nC₄: 2.  Petersen: 0 (no zero in {3, 1, −2}).", width=56).next_to(h, DOWN, buff=0.4)
        self.hold(30, ([FadeOut(d1), ex.animate.to_edge(DOWN, buff=0.5)], 0.6), ([FadeIn(d2)], 2.5))
        self.clear_all()

# ---------------------------------------------------------------- E02S09  Recap
class E02S09(BeatScene):
    SCENE_ID = 'E02S09'
    def construct(self):
        h = header("Recap: what you can now do")
        b = bullets(["write the adjacency matrix of a small graph",
                     "multiply it by a vector: sum over neighbours",
                     "define eigenvector / eigenvalue and verify one by hand",
                     "find 2 × 2 eigenvalues from trace and determinant",
                     "explain why 3 is the largest eigenvalue of a cubic graph",
                     "define kernel and nullity"], font_size=28, width=60).next_to(h, DOWN, buff=0.6)
        self.hold(31, ([FadeIn(h)], 0.8), ([FadeIn(b, lag_ratio=0.2)], 5))
        nxt = Text("Next: random walks, the spectral gap, and 2√2", font_size=32, color=YELLOW).to_edge(DOWN, buff=0.8)
        self.hold(32, ([FadeIn(nxt)], 1.5))
        self.clear_all()
