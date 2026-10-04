from lib import *

# ---------------------------------------------------------------- E11S01  Rotation-invariant matrices
class E11S01(BeatScene):
    SCENE_ID = 'E11S01'
    def construct(self):
        t = title_card("Episode 11", "Rotation-invariant certificates: roots on the grid, and where they run out")
        self.hold(1, ([FadeIn(t)], 1.5), ([FadeOut(t)], 0.5), ([FadeIn(header("The simplest matrices: the same weights everywhere"))], 0.8),
                  ([FadeIn(defn("rotation-invariant (period-one) matrix", "Outer edges 1, spokes c, inner edges e, outer diagonal a, inner diagonal d. Four numbers; symmetric; entries repeat with period one around the ring.", width=66, font_size=22, title_size=26).shift(UP*1.7))], 3))
        c = LEFT*4.6+DOWN*1.7
        g, d = petersen(8, 3, R_out=1.3, R_in=0.6, center=c, dot_r=0.06)
        lab = VGroup(MathTex("1", font_size=20, color=BLUE).next_to(d['outer'][0], UR, buff=0.05), MathTex("c", font_size=20, color=MUTED).next_to(d['spokes'][2], RIGHT, buff=0.05),
                     MathTex("e", font_size=20, color=ORANGE).next_to(d['inner'][0], RIGHT, buff=0.05), MathTex("a", font_size=20, color=BLUE).next_to(d['u'][4], DOWN, buff=0.1), MathTex("d", font_size=20, color=ORANGE).next_to(d['v'][0], UP, buff=0.05))
        blk = VGroup(MathTex(r"\text{outer: }(a+s_m)p+cq,\qquad \text{inner: }cp+(d+e\,t_m)q", font_size=28),
                     MathTex(r"s_m=2\cos\tfrac{2\pi m}{n},\qquad t_m=2\cos\tfrac{2\pi km}{n}", font_size=28),
                     MathTex(r"M_m=\begin{pmatrix}a+s_m&c\\ c&d+e\,t_m\end{pmatrix}", font_size=34, color=YELLOW)).arrange(DOWN, buff=0.25).to_edge(RIGHT, buff=0.5).shift(DOWN*1.3)
        self.hold(2, ([FadeIn(g), FadeIn(lab)], 1.5), ([Write(blk[0])], 3), ([Write(blk[1])], 2), ([Write(blk[2])], 2))
        self.play(FadeOut(blk), run_time=0.4)
        nul = card("nullity = number of singular blocks", [MathTex(r"\det M_m=0,\ c\ne0\ \Rightarrow\ \text{a one-dimensional kernel: contributes exactly }1", font_size=24),
                                                            MathTex(r"\operatorname{null}A=\#\{m:\ (a+s_m)(d+e\,t_m)-c^2=0\}", font_size=30, color=YELLOW)], color=YELLOW, width=54, title_size=26).to_edge(RIGHT, buff=0.4).shift(DOWN*1.5)
        self.hold(3, ([FadeIn(nul)], 3.5))
        self.clear_all()

# ---------------------------------------------------------------- E11S02  The symbol
class E11S02(BeatScene):
    SCENE_ID = 'E11S02'
    def construct(self):
        h = header("The symbol: a polynomial in s")
        t = VGroup(MathTex(r"2\cos2\theta=(2\cos\theta)^2-2\ \Rightarrow\ k=2:\ t=s^2-2;\qquad k=3:\ t=s^3-3s", font_size=30),
                   MathTex(r"\text{check: }s=2\cos60^\circ=1:\ t=2\cos120^\circ=-1=1-2\ \checkmark", font_size=26, color=MUTED)).arrange(DOWN, buff=0.25).next_to(h, DOWN, buff=0.5)
        self.hold(4, ([FadeIn(h), Write(t[0])], 3), ([Write(t[1])], 2.5))
        d1 = defn("symbol F(s)", [MathTex(r"F(s)=(a+s)\bigl(d+e\,t(s)\bigr)-c^2,\qquad \deg F=k+1", font_size=30),
                                   MathTex(r"\operatorname{null}A=\#\{m:\ F(s_m)=0\}=\text{number of grid points that are roots of }F", font_size=26, color=YELLOW)], width=70).next_to(t, DOWN, buff=0.4)
        self.hold(5, ([FadeIn(d1)], 4))
        n = 12; R = 1.4; c = LEFT*3.6+DOWN*2.0
        circ = Circle(radius=R, color=MUTED).move_to(c)
        pts = VGroup(*[Dot(c + R*np.array([np.cos(2*PI*m/n), np.sin(2*PI*m/n), 0]), radius=0.06, color=BLUE) for m in range(n)])
        proj = VGroup(*[DashedLine(p.get_center(), np.array([p.get_center()[0], c[1], 0]), color=GRID, stroke_width=1) for p in pts])
        line = Line(c + LEFT*R*1.1, c + RIGHT*R*1.1, color=MUTED)
        gp = VGroup(*[Dot(np.array([c[0] + R*np.cos(2*PI*m/n), c[1], 0]), radius=0.05, color=YELLOW) for m in range(n)])
        gl = MathTex(r"\text{grid: }s_m=2\cos\tfrac{2\pi m}{n}", font_size=24, color=YELLOW).next_to(circ, RIGHT, buff=0.5).shift(UP*0.6)
        note = wrap("s_m = s_{n−m} (cosine is even): every grid value except ±2 is hit twice. A root at a doubly-hit value contributes 2 to the nullity.", 40, 22, INK).next_to(gl, DOWN, buff=0.3, aligned_edge=LEFT)
        self.hold(6, ([FadeOut(t), d1.animate.scale(0.7).next_to(h, DOWN, buff=0.2)], 0.6), ([Create(circ), FadeIn(pts), Create(line)], 1.5), ([Create(proj), FadeIn(gp), FadeIn(gl)], 2), ([FadeIn(note)], 3))
        self.clear_all()

# ---------------------------------------------------------------- E11S03  Worked P(12,2)
class E11S03(BeatScene):
    SCENE_ID = 'E11S03'
    def construct(self):
        h = header("Worked example: nullity 6 on P(12,2)")
        grid = MathTex(r"n=12:\ s_m=2\cos(30m)^\circ:\ \ 2,\ \sqrt3,\ 1,\ 0,\ -1,\ -\sqrt3,\ -2,\ \dots\quad\text{(each of }\pm\sqrt3,\pm1,0\text{ twice)}", font_size=28).next_to(h, DOWN, buff=0.4)
        goal = Text("degree 3 symbol; three roots at doubly-hit values ⇒ nullity 6 = 2k+2, the ceiling", font_size=26, color=YELLOW).next_to(grid, DOWN, buff=0.3)
        self.hold(7, ([FadeIn(h), Write(grid)], 3), ([FadeIn(goal)], 2.5))
        self.play(FadeOut(goal), grid.animate.scale(0.85), run_time=0.5)
        ch = VGroup(MathTex(r"\text{roots }0,\ -1,\ -\sqrt3:\quad F=e\,s(s+1)(s+\sqrt3)=e\bigl(s^3+(1+\sqrt3)s^2+\sqrt3\,s\bigr)", font_size=28),
                    MathTex(r"\text{general }(k=2):\ (a+s)(d+e(s^2-2))-c^2=e s^3+ae\,s^2+(d-2e)s+a(d-2e)-c^2", font_size=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(grid, DOWN, buff=0.4)
        self.hold(8, ([Write(ch[0])], 3.5), ([Write(ch[1])], 3.5))
        match = VGroup(MathTex(r"s^2:\ ae=e(1+\sqrt3)\ \Rightarrow\ a=1+\sqrt3=2.732", font_size=28),
                       MathTex(r"s:\ d-2e=\sqrt3e\ \Rightarrow\ d=(2+\sqrt3)e", font_size=28),
                       MathTex(r"1:\ a(d-2e)-c^2=0\ \Rightarrow\ c^2=a\sqrt3e=(3+\sqrt3)e", font_size=28),
                       MathTex(r"e=1:\quad a=2.732,\ d=3.732,\ c^2=4.732,\ c=2.175", font_size=30, color=GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(ch, DOWN, buff=0.35)
        self.hold(9, ([Write(match[0])], 2.5), ([Write(match[1])], 2.5), ([Write(match[2])], 3), ([Write(match[3])], 2.5))
        self.play(FadeOut(ch), FadeOut(match), FadeOut(grid), run_time=0.5)
        c = LEFT*3.6+DOWN*0.9
        g, d = petersen(12, 2, R_out=2.1, R_in=1.0, center=c, dot_r=0.07)
        res = card("the certificate", [MathTex(r"\text{outer diag }2.732,\ \text{inner diag }3.732,\ \text{outer edges }1,\ \text{inner edges }1,\ \text{spokes }2.175", font_size=24),
                                        MathTex(r"F(s_m)=0\ \text{at }s=0,-1,-\sqrt3,\ \text{each hit twice}\ \Rightarrow\ \text{nullity }6", font_size=26),
                                        MathTex(r"\text{numerically: exactly six zero eigenvalues}\ \checkmark", font_size=24, color=MUTED),
                                        MathTex(r"Z\le6\ (\text{forcing})\ \Rightarrow\ Z=M=6\ \text{for }P(12,2),\ \text{with one matrix}", font_size=28, color=GREEN)], color=GREEN, width=50, font_size=22).to_edge(RIGHT, buff=0.3).shift(DOWN*0.6)
        self.hold(10, ([FadeIn(g)], 1.5), ([FadeIn(res)], 4))
        self.hold(11, ([FadeIn(Text("why did c² come out positive? it did not have to…", font_size=26, color=YELLOW).to_edge(DOWN, buff=0.3))], 2))
        self.clear_all()

# ---------------------------------------------------------------- E11S04  Antipodal obstruction
class E11S04(BeatScene):
    SCENE_ID = 'E11S04'
    def construct(self):
        h = header("The antipodal obstruction")
        bad = VGroup(MathTex(r"\text{roots }1,0,-1:\quad F=e\,s(s-1)(s+1)=e s^3-e s", font_size=30),
                     MathTex(r"s^2:\ ae=0\Rightarrow a=0;\qquad s:\ d-2e=-e\Rightarrow d=e;\qquad 1:\ a(d-2e)-c^2=0\Rightarrow c^2=0", font_size=28),
                     MathTex(r"c=0:\ \text{the spoke entry must be nonzero. Not realisable by any matrix with the pattern.}", font_size=28, color=RED)).arrange(DOWN, buff=0.3).next_to(h, DOWN, buff=0.5)
        self.hold(12, ([FadeIn(h), Write(bad[0])], 2.5), ([Write(bad[1])], 4), ([Write(bad[2])], 3))
        self.play(FadeOut(bad), run_time=0.4)
        gen = card("k = 2 in closed form", [MathTex(r"c^2=-(s_1+s_2)(s_1+s_3)(s_2+s_3)", font_size=36, color=YELLOW),
                                            wrap("two roots that are negatives of each other (antipodal on the grid) ⇒ a factor vanishes ⇒ c² = 0", 70, 24),
                                            MathTex(r"\text{roots }0,-1,-\sqrt3:\ \text{pairwise sums }-1,\ -\sqrt3,\ -1-\sqrt3;\ \text{product }-3-\sqrt3;\ c^2=3+\sqrt3\ \checkmark", font_size=24, color=GREEN)], color=YELLOW, width=70).next_to(h, DOWN, buff=0.5)
        self.hold(13, ([FadeIn(gen)], 5))
        self.play(gen.animate.scale(0.75).next_to(h, DOWN, buff=0.2), run_time=0.5)
        n = 10; R = 1.3; c = LEFT*3.8+DOWN*1.7
        circ = Circle(radius=R, color=MUTED).move_to(c)
        pts = VGroup(*[Dot(c + R*np.array([np.cos(2*PI*m/n), np.sin(2*PI*m/n), 0]), radius=0.07, color=BLUE) for m in range(n)])
        anti = Line(pts[1].get_center(), pts[6].get_center(), color=RED, stroke_width=3)
        cnt = VGroup(MathTex(r"n\ge9,\ n\ne10:\ \text{three doubly-hit, non-antipodal values exist}\ \Rightarrow\ Z=M=6", font_size=26, color=GREEN),
                     MathTex(r"n=8:\ \text{values }\pm\sqrt2,0:\ \text{every triple antipodal; true }Z=5\ \text{(method right to fail)}", font_size=24),
                     MathTex(r"n=10:\ \pm1.618,\pm0.618:\ \text{every triple antipodal; true }Z=6\ \text{(method falls short)}", font_size=24),
                     Text("n = 10: a different, non-rotation-invariant integer matrix does the job", font_size=22, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3).shift(DOWN*1.5)
        self.hold(14, ([Create(circ), FadeIn(pts), Create(anti)], 2), ([FadeIn(cnt[0])], 2.5), ([FadeIn(cnt[1])], 2.5), ([FadeIn(cnt[2])], 2.5), ([FadeIn(cnt[3])], 2))
        self.clear_all()

# ---------------------------------------------------------------- E11S05  Galois conjugates
class E11S05(BeatScene):
    SCENE_ID = 'E11S05'
    def construct(self):
        h = header("Galois conjugates: roots that come in bundles")
        p = VGroup(MathTex(r"k\ge3:\ \deg F=k+1\ \text{but only three adjustable quantities }(a,d,c^2;\ e\text{ is the leading coefficient})", font_size=26),
                   MathTex(r"\Rightarrow\ \text{three prescribed roots, nullity }6<2k+2\ \ldots\ \text{unless the other roots land on the grid by themselves}", font_size=26, color=YELLOW)).arrange(DOWN, buff=0.3).next_to(h, DOWN, buff=0.4)
        self.hold(15, ([FadeIn(h), Write(p[0])], 3), ([Write(p[1])], 3))
        self.play(FadeOut(p), run_time=0.4)
        d1 = defn("conjugates", [MathTex(r"\sqrt2\ \text{is a root of }x^2-2;\ \text{so is }-\sqrt2", font_size=28),
                                  wrap("any polynomial with rational coefficients vanishing at one vanishes at the other (divide by x² − 2: no remainder). Algebraically indistinguishable.", 76, 22, MUTED)], width=66).next_to(h, DOWN, buff=0.4)
        self.hold(16, ([FadeIn(d1)], 4))
        ex = VGroup(MathTex(r"2\cos72^\circ=0.618:\ x^2+x-1;\ \text{other root }-1.618=2\cos144^\circ", font_size=26),
                    MathTex(r"2\cos\tfrac{2\pi}7=1.247:\ x^3+x^2-2x-1;\ \text{others }2\cos\tfrac{4\pi}7,\ 2\cos\tfrac{6\pi}7", font_size=26),
                    MathTex(r"\text{conjugates of }2\cos\tfrac{2\pi}{d}:\ \text{exactly }2\cos\tfrac{2\pi m}{d},\ \gcd(m,d)=1\quad\text{(a Galois orbit)}", font_size=26, color=YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(d1, DOWN, buff=0.4)
        self.hold(17, ([Write(ex[0])], 3), ([Write(ex[1])], 3), ([Write(ex[2])], 3))
        self.play(FadeOut(ex), FadeOut(d1), run_time=0.4)
        use = card("use it", [Text("build F as a product of such minimal polynomials, rational coefficients", font_size=24),
                              Text("prescribe one root 2cos(2π/d): the whole orbit comes free, on the grid whenever d | n", font_size=24),
                              MathTex(r"Z(P(n,4))=10\ \text{ for }60,70,90\mid n;\qquad Z(P(n,5))=12\ \text{ for }24\mid n", font_size=30, color=GREEN),
                              Text("first exact values at k = 4, 5 attaining 2k+2; first for infinitely many n", font_size=22, color=MUTED)], color=GREEN, width=68).next_to(h, DOWN, buff=0.5)
        self.hold(18, ([FadeIn(use)], 5))
        self.clear_all()

# ---------------------------------------------------------------- E11S06  Where it stops
class E11S06(BeatScene):
    SCENE_ID = 'E11S06'
    def construct(self):
        h = header("Where the method stops, exactly")
        lim = VGroup(Text("fixed rational symbol ⇒ fixed algebraic roots", font_size=28),
                     MathTex(r"2\cos\tfrac{2\pi}{d}\ \text{is on the grid}\iff d\mid n:\ \text{one divisibility class}", font_size=28),
                     Text("a divisibility class contains at most one prime", font_size=28),
                     Text("no rotation-invariant matrix can give a value for all large n", font_size=30, color=RED),
                     MathTex(r"\text{multiples of }10\ (k=3),\ 60\ (k=4)\ \text{yes};\quad n=17,19,23\ \text{never}", font_size=26, color=MUTED)).arrange(DOWN, buff=0.3).next_to(h, DOWN, buff=0.5)
        self.hold(19, ([FadeIn(lim, lag_ratio=0.25)], 6))
        self.play(FadeOut(lim), run_time=0.4)
        nxt = card("the route to all n", [wrap("Krishnan's conjecture asks for all n ≥ 13. Break the rotational symmetry: entries vary around the ring.", 70, 24),
                                          wrap("no blocks, no symbol — but the monodromy survives", 70, 24),
                                          MathTex(r"T=I:\ \text{no roots of unity, no divisibility; polynomial equations in the entries, any }n", font_size=26, color=YELLOW),
                                          wrap("next: solve it, and prove a computer's solution is real", 70, 24, MUTED)], color=YELLOW, width=68).next_to(h, DOWN, buff=0.5)
        self.hold(20, ([FadeIn(nxt)], 5))
        self.clear_all()

# ---------------------------------------------------------------- E11S07  Recap
class E11S07(BeatScene):
    SCENE_ID = 'E11S07'
    def construct(self):
        h = header("Recap: what you can now do")
        b = bullets(["write the 2 × 2 block of a rotation-invariant matrix on P(n,k)",
                     "explain why the nullity counts grid values that are roots of the symbol",
                     "reproduce the P(12,2) example: roots 0, −1, −√3 ⇒ a, d, c²",
                     "show roots 1, 0, −1 force c = 0; explain the antipodal obstruction",
                     "explain conjugates and Galois orbits via √2 and 2cos 72°",
                     "explain why a fixed symbol covers only one divisibility class of n"], font_size=26, width=70).next_to(h, DOWN, buff=0.6)
        self.hold(21, ([FadeIn(h)], 0.8), ([FadeIn(b, lag_ratio=0.2)], 5))
        self.clear_all()
