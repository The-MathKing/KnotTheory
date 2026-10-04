from lib import *

def Q(x, y): return 4*x*x+4*y*y-8*np.sqrt(2)*abs(x*y)+3

# ---------------------------------------------------------------- E07S01  Difference of squares
class E07S01(BeatScene):
    SCENE_ID = 'E07S01'
    def construct(self):
        t = title_card("Episode 7", "The corner criterion, and why the family is finite")
        self.hold(1, ([FadeIn(t)], 1.5), ([FadeOut(t)], 0.5), ([FadeIn(header("D_k is a difference of squares"))], 0.8),
                  ([Write(MathTex(r"D_k=(7+P)^2-(2\sqrt2A)^2=f_-\,f_+,\qquad f_\pm=7+P\pm2\sqrt2\,A", font_size=36).shift(UP*1.6))], 3),
                  ([FadeIn(Text("f₋ ≥ 0 is the upper-eigenvalue condition; f₊ ≥ 0 the lower one", font_size=26, color=MUTED).shift(UP*0.7))], 2))
        e = VGroup(MathTex(r"f_-+f_+=2(7+P)\ge6>0\ \Rightarrow\ \text{never both negative}", font_size=30, color=GREEN),
                   MathTex(r"D_k\ge0\iff\min(f_-,f_+)\ge0\iff 7+P-2\sqrt2\,|A|\ge0", font_size=32, color=YELLOW)).arrange(DOWN, buff=0.4).shift(DOWN*0.8)
        self.hold(2, ([Write(e[0])], 3), ([Write(e[1])], 3))
        self.clear_all()

# ---------------------------------------------------------------- E07S02  Two identities
class E07S02(BeatScene):
    SCENE_ID = 'E07S02'
    def construct(self):
        h = header("Two cosine identities")
        ids = VGroup(MathTex(r"\cos a\cos b=\tfrac12\bigl[\cos(a+b)+\cos(a-b)\bigr]\qquad\text{(product to sum)}", font_size=32),
                     MathTex(r"\cos a+\cos b=2\cos\tfrac{a+b}2\cos\tfrac{a-b}2\qquad\text{(sum to product)}", font_size=32)).arrange(DOWN, buff=0.4).next_to(h, DOWN, buff=0.5)
        self.hold(3, ([FadeIn(h)], 0.8), ([Write(ids[0])], 2.5), ([Write(ids[1])], 2.5))
        chk = VGroup(MathTex(r"a=b=60^\circ:\ \cos^260^\circ=\tfrac14;\ \tfrac12[\cos120^\circ+\cos0]=\tfrac12[-\tfrac12+1]=\tfrac14\ \checkmark", font_size=26, color=MUTED),
                     MathTex(r"a=60^\circ,b=0:\ \cos60^\circ+1=\tfrac32;\ 2\cos30^\circ\cos30^\circ=2\cdot\tfrac34=\tfrac32\ \checkmark", font_size=26, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ids, DOWN, buff=0.4)
        self.hold(4, ([Write(chk[0])], 3), ([Write(chk[1])], 3))
        self.play(FadeOut(chk), run_time=0.4)
        app = card("apply with a = t, b = kt", [MathTex(r"x:=\cos\tfrac{(k+1)t}{2},\qquad y:=\cos\tfrac{(k-1)t}{2}", font_size=32, color=YELLOW),
                                                 MathTex(r"A=2\cos t+2\cos kt=4xy", font_size=30),
                                                 MathTex(r"\cos t\cos kt=\tfrac12[(2x^2-1)+(2y^2-1)]\ \Rightarrow\ P=4x^2+4y^2-4", font_size=30)], color=YELLOW, width=66).next_to(ids, DOWN, buff=0.4)
        self.hold(5, ([FadeIn(app)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E07S03  Q
class E07S03(BeatScene):
    SCENE_ID = 'E07S03'
    def construct(self):
        h = header("The function Q: k has left the geometry")
        sub = MathTex(r"7+P-2\sqrt2|A|=7+4x^2+4y^2-4-8\sqrt2|xy|", font_size=32).next_to(h, DOWN, buff=0.5)
        Qd = MathTex(r"Q(x,y)=4x^2+4y^2-8\sqrt2\,|xy|+3\ \ge\ 0\quad\text{at }x=\cos\tfrac{\pi j(k+1)}{n},\ y=\cos\tfrac{\pi j(k-1)}{n}", font_size=32, color=YELLOW).next_to(sub, DOWN, buff=0.4)
        self.hold(6, ([FadeIn(h), Write(sub)], 2.5), ([Write(Qd)], 3.5))
        nok = idea("look", "Q contains no k. For every k the same test on the same two variables. k only decides which (x, y) pairs get tested, not what test is applied.", width=66).next_to(Qd, DOWN, buff=0.4)
        self.hold(7, ([FadeIn(nok)], 3))
        self.play(FadeOut(sub), FadeOut(nok), Qd.animate.scale(0.8).next_to(h, DOWN, buff=0.3), run_time=0.7)
        L = 4.6; c = DOWN*1.2 + LEFT*3.0
        sq = Square(side_length=L, color=MUTED).move_to(c)
        def ym(x): return np.sqrt(2)*x - 0.5*np.sqrt(max(4*x*x-3, 0))
        x0 = np.sqrt(2) - 0.5
        xs = np.linspace(x0, 1, 60)
        poly_pts = [np.array([x, ym(x), 0]) for x in xs] + [np.array([1, 1, 0])]
        regions = VGroup()
        for sx in (1, -1):
            for sy in (1, -1):
                pts = [c + (L/2)*np.array([sx*p[0], sy*p[1], 0]) for p in poly_pts]
                regions.add(Polygon(*pts, color=RED, fill_opacity=0.6, stroke_width=1))
        Z = 9.0; zc = RIGHT*3.4 + DOWN*0.9
        zpts = [zc + Z*(np.array([p[0], p[1], 0]) - np.array([1, 1, 0])) + np.array([0.9, 0.9, 0]) for p in poly_pts]
        zreg = Polygon(*zpts, color=RED, fill_opacity=0.5, stroke_width=1)
        zbox = Square(side_length=1.8, color=MUTED, stroke_width=1).move_to(zc)
        zl = Text("corner (1,1), ×9", font_size=20, color=MUTED).next_to(zbox, UP, buff=0.1)
        facts = VGroup(MathTex(r"Q=0:\ \text{a hyperbola}", font_size=26), MathTex(r"\text{side segments: }\tfrac32-\sqrt2=0.086", font_size=26),
                       MathTex(r"\text{total area: }0.43\%\text{ of the square}", font_size=26, color=YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(zbox, DOWN, buff=0.3)
        self.hold(8, ([Create(sq)], 1), ([FadeIn(regions)], 1.5), ([Create(zbox), FadeIn(zreg), FadeIn(zl)], 1.5), ([FadeIn(facts, lag_ratio=0.3)], 3))
        self.clear_all()

# ---------------------------------------------------------------- E07S04  Worked Q
class E07S04(BeatScene):
    SCENE_ID = 'E07S04'
    def construct(self):
        h = header("Worked example: Q on P(5,2) and P(24,2)")
        L = 4.4; c = DOWN*1.0 + LEFT*3.4
        sq = Square(side_length=L, color=MUTED).move_to(c)
        def ym(x): return np.sqrt(2)*x - 0.5*np.sqrt(max(4*x*x-3, 0))
        x0 = np.sqrt(2) - 0.5; xs = np.linspace(x0, 1, 60)
        poly_pts = [np.array([x, ym(x), 0]) for x in xs] + [np.array([1, 1, 0])]
        regions = VGroup(*[Polygon(*[c + (L/2)*np.array([sx*p[0], sy*p[1], 0]) for p in poly_pts], color=RED, fill_opacity=0.6, stroke_width=1) for sx in (1, -1) for sy in (1, -1)])
        self.add(h, sq, regions)
        def mk(n, k, j=1):
            x = np.cos(PI*j*(k+1)/n); y = np.cos(PI*j*(k-1)/n)
            return x, y, Dot(c + (L/2)*np.array([x, y, 0]), radius=0.09, color=YELLOW)
        x, y, d1 = mk(5, 2)
        w1 = VGroup(MathTex(r"P(5,2),\ j=1:\ x=\cos108^\circ=-0.309,\ y=\cos36^\circ=0.809", font_size=26),
                    MathTex(r"Q=4(0.0955)+4(0.6545)-8\sqrt2(0.250)+3", font_size=26),
                    MathTex(r"=0.382+2.618-2.828+3=3.172>0", font_size=28, color=GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP*1.6)
        self.hold(9, ([FadeIn(d1), Write(w1[0])], 2.5), ([Write(w1[1])], 3), ([Write(w1[2])], 2.5))
        x, y, d2 = mk(24, 2)
        w2 = VGroup(MathTex(r"P(24,2),\ j=1:\ x=\cos22.5^\circ=0.9239,\ y=\cos7.5^\circ=0.9914", font_size=26),
                    MathTex(r"Q=4(0.8536)+4(0.9830)-8\sqrt2(0.9160)+3", font_size=26),
                    MathTex(r"=3.414+3.932-10.363+3=-0.017<0\ \text{fails}", font_size=28, color=RED)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(w1, DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        self.hold(10, ([FadeIn(d2), Write(w2[0])], 2.5), ([Write(w2[1])], 3), ([Write(w2[2])], 2.5))
        x, y, d3 = mk(23, 2); d3.set_color(GREEN)
        w3 = MathTex(r"P(23,2):\ x=0.9172,\ y=0.9907,\ Q=+0.0105\quad\text{just outside}", font_size=26, color=GREEN).next_to(w2, DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        self.hold(11, ([FadeIn(d3), Write(w3)], 2.5), ([FadeIn(Text("a few hundredths decide it: exact arithmetic next episode", font_size=22, color=MUTED).to_edge(DOWN, buff=0.3))], 2))
        self.clear_all()

# ---------------------------------------------------------------- E07S05  AM-GM
class E07S05(BeatScene):
    SCENE_ID = 'E07S05'
    def construct(self):
        h = header("A bound for every k: the AM–GM argument")
        goal = Text("want: one bound on n valid for all k at once, from three elementary facts", font_size=26, color=MUTED).next_to(h, DOWN, buff=0.4)
        self.hold(12, ([FadeIn(h)], 0.8), ([FadeIn(goal)], 2))
        setup = VGroup(MathTex(r"x=\cos t,\ y=\cos kt,\ t=\tfrac{2\pi}{n};\quad a=1-x,\ b=1-y,\ s=a+b", font_size=28),
                       MathTex(r"\text{fail}\iff G:=4\sqrt2(x+y)-4xy>7", font_size=28),
                       MathTex(r"G=(8\sqrt2-4)-(4\sqrt2-4)s-4ab", font_size=30, color=YELLOW)).arrange(DOWN, buff=0.25).next_to(goal, DOWN, buff=0.4)
        self.hold(13, ([Write(setup[0])], 3), ([Write(setup[1])], 2.5), ([Write(setup[2])], 3))
        self.play(FadeOut(goal), setup.animate.scale(0.8).next_to(h, DOWN, buff=0.3), run_time=0.6)
        f1 = card("Fact 1: AM–GM", [MathTex(r"4ab\le(a+b)^2=s^2\quad\text{since }(a+b)^2-4ab=(a-b)^2\ge0;\quad a=1,b=3:\ 12\le16", font_size=26),
                                     MathTex(r"\Rightarrow\ \text{fail as soon as }s^2+(4\sqrt2-4)s<8\sqrt2-11", font_size=28, color=GREEN)], color=GREEN, width=70, font_size=24).next_to(setup, DOWN, buff=0.3)
        self.hold(14, ([FadeIn(f1)], 4))
        f2 = card("Fact 2", [MathTex(r"\text{LHS increasing in }s;\ \text{at }s=\tau:=3-2\sqrt2=0.1716\ \text{it equals }8\sqrt2-11\ \text{exactly}", font_size=26),
                              MathTex(r"\tau^2=17-12\sqrt2,\ (4\sqrt2-4)\tau=20\sqrt2-28;\ \text{sum}=8\sqrt2-11\ \checkmark\ \Rightarrow\ s<\tau\text{ forces failure}", font_size=24, color=MUTED)], color=GREEN, width=70, font_size=24).next_to(f1, DOWN, buff=0.25)
        self.hold(15, ([FadeIn(f2)], 4))
        self.play(FadeOut(f1), f2.animate.next_to(setup, DOWN, buff=0.3), run_time=0.5)
        f3 = card("Fact 3", [MathTex(r"1-\cos\theta\le\theta^2/2\quad(\theta=1:\ 0.46\le0.5)\ \Rightarrow\ a\le\tfrac{t^2}2,\ b\le\tfrac{k^2t^2}2,\ s\le\tfrac{(1+k^2)t^2}{2}", font_size=26)], color=GREEN, width=70, font_size=24).next_to(f2, DOWN, buff=0.25)
        self.hold(16, ([FadeIn(f3)], 4))
        self.play(FadeOut(f2), FadeOut(f3), FadeOut(setup), run_time=0.4)
        fin = VGroup(MathTex(r"\tfrac{(1+k^2)t^2}{2}<\tau\iff t<\frac{\sqrt{2\tau}}{\sqrt{k^2+1}}=\frac{2-\sqrt2}{\sqrt{k^2+1}}", font_size=30),
                     MathTex(r"\text{smallest grid angle }t=\tfrac{2\pi}{n}\ \Rightarrow\ \text{Ramanujan needs}", font_size=28),
                     MathTex(r"n\ \le\ \pi\,(2+\sqrt2)\sqrt{k^2+1}", font_size=44, color=YELLOW)).arrange(DOWN, buff=0.35).next_to(h, DOWN, buff=0.5)
        self.hold(17, ([Write(fin[0])], 3), ([Write(fin[1])], 2), ([Write(fin[2])], 2.5))
        num = MathTex(r"k=2:\ 23.98\ (\text{true }23.37);\qquad k=3:\ 33.9\ (\text{true }32.5)", font_size=28, color=MUTED).next_to(fin, DOWN, buff=0.4)
        self.hold(18, ([Write(num)], 2.5))
        self.play(FadeOut(fin), FadeOut(num), run_time=0.4)
        wrong = card("an honest correction", "An earlier draft got the same constant by Taylor expanding in t at fixed k. Invalid: the critical t is of size 1/k, so kt is of size 1, outside the expansion's range. Right constant, wrong argument. The proof above replaces it.", color=RED, width=64).next_to(h, DOWN, buff=0.6)
        self.hold(19, ([FadeIn(wrong)], 3))
        self.clear_all()

# ---------------------------------------------------------------- E07S06  Dirichlet
class E07S06(BeatScene):
    SCENE_ID = 'E07S06'
    def construct(self):
        h = header("Dirichlet's theorem closes the family")
        p = wrap("For each k, n is bounded, but the bound grows like k. Could there be Ramanujan graphs with enormous k and n? Use the failure condition with any j, not just j = 1.", 68, 26).next_to(h, DOWN, buff=0.4)
        e0 = MathTex(r"\text{fail}\Leftarrow\ \bigl(1-\cos\tfrac{2\pi j}{n}\bigr)+\bigl(1-\cos\tfrac{2\pi jk}{n}\bigr)<\tau\ \text{ for some nontrivial }j", font_size=28, color=YELLOW).next_to(p, DOWN, buff=0.3)
        self.hold(20, ([FadeIn(h), FadeIn(p)], 2.5), ([Write(e0)], 3))
        self.play(FadeOut(p), e0.animate.next_to(h, DOWN, buff=0.3), run_time=0.5)
        d1 = defn("‖θ‖", [MathTex(r"\|\theta\|=\text{distance from }\theta\text{ to the nearest whole number};\ \|2.9\|=0.1,\ \|0.4\|=0.4", font_size=26),
                           MathTex(r"1-\cos2\pi\theta\le2\pi^2\|\theta\|^2\ \Rightarrow\ \text{fail}\Leftarrow\ \Bigl\|\tfrac jn\Bigr\|^2+\Bigl\|\tfrac{jk}{n}\Bigr\|^2<\frac{\tau}{2\pi^2}=0.00869", font_size=26, color=YELLOW)], width=70).next_to(e0, DOWN, buff=0.4)
        self.hold(21, ([FadeIn(d1)], 4))
        need = wrap("Need a j with both j/n and jk/n nearly whole. j/n is small when j is small; jk/n needs jk ≈ a multiple of n: approximating the fraction k/n by fractions with small denominators j.", 70, 24, MUTED).next_to(d1, DOWN, buff=0.4)
        self.hold(22, ([FadeIn(need)], 3))
        self.play(FadeOut(d1), FadeOut(need), FadeOut(e0), run_time=0.4)
        thm = card("Dirichlet's approximation theorem", [MathTex(r"\text{for any real }r\text{ and whole }J:\ \exists\,j\in\{1,\dots,J\}\ \text{with }\|jr\|\le\tfrac1{J+1}", font_size=28)], color=YELLOW, width=66).next_to(h, DOWN, buff=0.4)
        pf = VGroup(Text("proof (pigeonhole): fractional parts of 0r, 1r, …, Jr are J+1 numbers in [0,1)", font_size=24),
                    Text("cut [0,1) into J+1 bins of width 1/(J+1)", font_size=24),
                    Text("two in one bin ⇒ their difference jr is within one bin of a whole number", font_size=24),
                    Text("else every bin has one ⇒ the last bin holds some mr, within one bin of the next whole number", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(thm, DOWN, buff=0.35)
        self.hold(23, ([FadeIn(thm)], 2.5), ([FadeIn(pf, lag_ratio=0.3)], 5))
        self.play(FadeOut(pf), run_time=0.4)
        # numeric example
        r = 0.414; J = 4
        line = NumberLine(x_range=[0, 1, 0.2], length=8, include_numbers=True, color=MUTED, decimal_number_config={"num_decimal_places": 1}).shift(DOWN*1.0)
        fr = [(j*r) % 1 for j in range(J+1)]
        dots = VGroup(*[Dot(line.n2p(v), color=YELLOW, radius=0.08) for v in fr])
        labs = VGroup(*[MathTex(f"{j}r", font_size=22, color=YELLOW).next_to(line.n2p(v), UP, buff=0.15) for j, v in enumerate(fr)])
        ex = VGroup(MathTex(r"r=0.414,\ J=4:\ \text{parts }0,\ 0.414,\ 0.828,\ 0.242,\ 0.656;\ \text{bins of width }0.2", font_size=26),
                    MathTex(r"\text{one per bin}\ \Rightarrow\ \text{last bin holds }0.828=2r:\ j=2,\ \|2r\|=0.172<\tfrac15\ \checkmark", font_size=26, color=GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(line, DOWN, buff=0.6)
        self.hold(24, ([Create(line), FadeIn(dots), FadeIn(labs)], 2), ([Write(ex[0])], 3), ([Write(ex[1])], 3))
        self.play(FadeOut(line), FadeOut(dots), FadeOut(labs), FadeOut(ex), run_time=0.4)
        ap = VGroup(MathTex(r"r=\tfrac kn,\ J=\lfloor\sqrt n\rfloor:\ \exists\,j\le\sqrt n\ \text{with }\Bigl\|\tfrac{jk}{n}\Bigr\|<\tfrac1{\sqrt n},\ \text{and }\Bigl\|\tfrac jn\Bigr\|\le\tfrac{j}{n}\le\tfrac1{\sqrt n}", font_size=28),
                    MathTex(r"\text{sum of squares}<\tfrac2n", font_size=32, color=YELLOW)).arrange(DOWN, buff=0.3).next_to(thm, DOWN, buff=0.4)
        self.hold(25, ([Write(ap[0])], 3.5), ([Write(ap[1])], 2))
        res = VGroup(MathTex(r"\tfrac2n<\tfrac{\tau}{2\pi^2}\iff n>\tfrac{4\pi^2}{\tau}=230.097\ldots", font_size=32, color=YELLOW),
                     wrap("n ≥ 231: not Ramanujan, for every k. The candidates live in a finite triangle: about 13,000 pairs.", 64, 26)).arrange(DOWN, buff=0.35).next_to(ap, DOWN, buff=0.4)
        self.hold(26, ([Write(res[0])], 3), ([FadeIn(res[1])], 3))
        self.clear_all()

# ---------------------------------------------------------------- E07S07  Parity, no-go
class E07S07(BeatScene):
    SCENE_ID = 'E07S07'
    def construct(self):
        h = header("The parity law, and no infinite family from any base")
        par = card("parity law", [MathTex(r"n\text{ even},\ k\text{ odd},\ j=\tfrac n2:\ x=\cos\tfrac{\pi(k+1)}2,\ y=\cos\tfrac{\pi(k-1)}2\in\{\pm1\}:\ \text{a corner}", font_size=26),
                                  Text("but that j carries the eigenvalue −3 of a bipartite graph: exempt", font_size=24),
                                  Text("odd n has no such j; its nearest point lands in the band at u = −1", font_size=24),
                                  MathTex(r"\Rightarrow\ \text{for odd }k,\ \text{odd }n\text{ is cut off at half the constant. Bipartite is worth a factor }2\text{ in }n.", font_size=26, color=YELLOW)], color=YELLOW, width=70, font_size=24).next_to(h, DOWN, buff=0.4)
        self.hold(27, ([FadeIn(par)], 5))
        self.play(FadeOut(par), run_time=0.4)
        u = Dot(LEFT*1.2, radius=0.12, color=BLUE); v = Dot(RIGHT*1.2, radius=0.12, color=ORANGE)
        lu = Arc(radius=0.5, start_angle=-PI/2+0.5, angle=2*PI-1.0, color=BLUE).move_to(LEFT*1.2+UP*0.6)
        lv = Arc(radius=0.5, start_angle=-PI/2+0.5, angle=2*PI-1.0, color=ORANGE).move_to(RIGHT*1.2+UP*0.6)
        e = Line(LEFT*1.2, RIGHT*1.2, color=MUTED)
        vol = VGroup(MathTex("1", font_size=28, color=BLUE).next_to(lu, UP, buff=0.1), MathTex("k", font_size=28, color=ORANGE).next_to(lv, UP, buff=0.1), MathTex("0", font_size=28, color=MUTED).next_to(e, DOWN, buff=0.1))
        base = VGroup(lu, lv, e, u, v, vol).scale(0.8).move_to(LEFT*4.6+UP*0.9)
        bl = wrap("P(n,k) = a two-vertex base, rotated n times (a cyclic cover: episode 14)", 30, 22, MUTED).next_to(base, DOWN, buff=0.4)
        nogo = VGroup(MathTex(r"M_1\xrightarrow{\ n\to\infty\ }M_0=\text{adjacency of the base},\ \lambda_{\max}(M_0)=3", font_size=26),
                      wrap("some nontrivial eigenvalue is dragged toward 3, past 2√2", 48, 24),
                      wrap("No infinite Ramanujan family comes from rotating a fixed base.", 48, 28, YELLOW),
                      wrap("known in spirit (why LPS used non-commutative groups); new: the constant and exact criteria", 48, 22, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP*0.3)
        self.hold(28, ([FadeIn(h), Create(base), FadeIn(bl)], 2.5), ([Write(nogo[0])], 3), ([FadeIn(nogo[1])], 2), ([FadeIn(nogo[2])], 2), ([FadeIn(nogo[3])], 2))
        self.clear_all()

# ---------------------------------------------------------------- E07S08  Recap
class E07S08(BeatScene):
    SCENE_ID = 'E07S08'
    def construct(self):
        h = header("Recap: what you can now do")
        b = bullets(["factor D_k = f₋f₊ and explain why both cannot be negative",
                     "state and check the two cosine identities; derive A = 4xy, P = 4x² + 4y² − 4",
                     "write Q(x,y) and explain why it has no k",
                     "evaluate Q on P(5,2) and P(24,2)",
                     "reproduce the AM–GM argument: n ≤ π(2+√2)√(k²+1)",
                     "state Dirichlet's theorem, prove it by pigeonhole, derive n ≤ 230"], font_size=27, width=66).next_to(h, DOWN, buff=0.6)
        self.hold(29, ([FadeIn(h)], 0.8), ([FadeIn(b, lag_ratio=0.2)], 5))
        self.clear_all()
