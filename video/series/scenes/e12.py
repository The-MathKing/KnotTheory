from lib import *

# ---------------------------------------------------------------- E12S01  Newton
class E12S01(BeatScene):
    SCENE_ID = 'E12S01'
    def construct(self):
        t = title_card("Episode 12", "Newton's method, interval arithmetic, and certified solutions")
        self.hold(1, ([FadeIn(t)], 1.5), ([FadeOut(t)], 0.5), ([FadeIn(header("Solving equations numerically: Newton on √2"))], 0.8),
                  ([FadeIn(wrap("Goal: entries varying around the ring with monodromy T = I. A polynomial system, solved numerically. Simplest possible version: x² = 2.", 70, 26).shift(UP*1.6))], 3))
        ax = Axes(x_range=[1.0, 1.8, 0.2], y_range=[-1, 1.5, 0.5], x_length=5.8, y_length=3.2, axis_config={"include_tip": False, "color": MUTED},
                  x_axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 1}}, y_axis_config={"include_numbers": True}).to_edge(LEFT, buff=0.6).shift(DOWN*1.5)
        cur = ax.plot(lambda x: x*x-2, x_range=[1.0, 1.8, 0.01], color=BLUE)
        x0 = 1.5
        p0 = Dot(ax.c2p(x0, x0*x0-2), color=YELLOW, radius=0.08)
        tang = ax.plot(lambda x: 2*x0*(x-x0) + (x0*x0-2), x_range=[1.3, 1.65, 0.01], color=YELLOW)
        x1 = x0 - (x0*x0-2)/(2*x0)
        p1 = Dot(ax.c2p(x1, 0), color=GREEN, radius=0.08)
        st = VGroup(MathTex(r"f(x)=x^2-2,\quad x_0=1.5:\ f=0.25,\ f'=2x=3", font_size=26),
                    MathTex(r"x_1=x_0-\frac{f(x_0)}{f'(x_0)}=1.5-\frac{0.25}{3}=1.4167", font_size=28, color=YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).shift(DOWN*0.6)
        self.hold(2, ([Create(ax), Create(cur)], 1.5), ([FadeIn(p0), Write(st[0])], 2), ([Create(tang), FadeIn(p1), Write(st[1])], 3))
        more = VGroup(MathTex(r"x_2=1.4167-\frac{0.0069}{2.833}=1.414216", font_size=26),
                      MathTex(r"x_3=1.414213562\ldots\ \text{(12 digits)}", font_size=26, color=GREEN),
                      Text("each step roughly doubles the correct digits", font_size=22, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(st, DOWN, buff=0.3).to_edge(RIGHT, buff=0.4)
        self.hold(3, ([Write(more[0])], 2.5), ([Write(more[1])], 2), ([FadeIn(more[2])], 1.5))
        self.play(FadeOut(ax), FadeOut(cur), FadeOut(p0), FadeOut(tang), FadeOut(p1), FadeOut(st), FadeOut(more), run_time=0.5)
        sysc = card("many unknowns", [MathTex(r"\text{slope}\to\text{Jacobian }J\ (\text{all partial derivatives});\quad\text{solve }J\,\delta=-f;\quad x\leftarrow x+\delta", font_size=26),
                                      Text("here: unknowns = the matrix entries around the ring; equations: T − I = 0 entry by entry", font_size=24, color=MUTED)], color=BLUE, width=70).shift(DOWN*1.0)
        self.hold(4, ([FadeIn(sysc)], 3.5))
        self.clear_all()

# ---------------------------------------------------------------- E12S02  Not a proof
class E12S02(BeatScene):
    SCENE_ID = 'E12S02'
    def construct(self):
        h = header("What Newton gives you, and what it does not")
        a = VGroup(MathTex(r"\text{Newton reports entries with }T-I=0\ \text{to 14 decimal places. Proved?}\quad\textbf{No.}", font_size=30),
                   Text("maybe a true solution sits a hair away and this is its rounded version", font_size=26, color=MUTED),
                   Text("or maybe no exact solution exists nearby: a small residual that is not zero", font_size=26, color=MUTED),
                   MathTex(r"\text{like }x^2=2\ \text{having no solution }\tfrac{m}{1000},\ \text{though }\tfrac{1414}{1000}\ \text{comes close}", font_size=26, color=ORANGE)).arrange(DOWN, buff=0.35).next_to(h, DOWN, buff=0.6)
        self.hold(5, ([FadeIn(h), Write(a[0])], 3), ([FadeIn(a[1])], 2), ([FadeIn(a[2])], 2), ([Write(a[3])], 3))
        b = card("what we need instead", "A statement about a region, not a measurement at a point: inside THIS box of numbers there exists an exact solution.\nThe tool: interval arithmetic.", color=YELLOW, width=64).next_to(a, DOWN, buff=0.5)
        self.hold(6, ([FadeIn(b)], 3))
        self.clear_all()

# ---------------------------------------------------------------- E12S03  Interval arithmetic
class E12S03(BeatScene):
    SCENE_ID = 'E12S03'
    def construct(self):
        h = header("Interval arithmetic in one minute")
        d1 = defn("interval", "A range of numbers, like [1.41, 1.42]. Add: add the ends. Multiply: take the smallest and largest of the four end-products.", width=70, font_size=24).next_to(h, DOWN, buff=0.35)
        ex = VGroup(MathTex(r"X=[1.41,1.42]:\ \text{end products }1.9881,\ 2.0022,\ 2.0164\ \Rightarrow\ X^2=[1.9881,\,2.0164]", font_size=28),
                    MathTex(r"X^2-2=[-0.0119,\,0.0164]", font_size=32, color=YELLOW)).arrange(DOWN, buff=0.3).next_to(d1, DOWN, buff=0.4)
        self.hold(7, ([FadeIn(h), FadeIn(d1)], 2.5), ([Write(ex[0])], 3), ([Write(ex[1])], 2))
        g = card("the point", "Whatever x is in the interval, x² − 2 really is in the computed range. Lower ends round down, upper ends round up, so the guarantee survives floating point.\nAn interval computation is a proof about every number in the range at once.", color=GREEN, width=76, font_size=22).next_to(ex, DOWN, buff=0.35)
        self.hold(8, ([FadeIn(g)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E12S04  Krawczyk
class E12S04(BeatScene):
    SCENE_ID = 'E12S04'
    def construct(self):
        h = header("Krawczyk's test, on √2")
        d1 = defn("Krawczyk operator (1969)", [MathTex(r"K(X)=x_0-Y\,f(x_0)+\bigl(1-Y\,f'(X)\bigr)\,(X-x_0)", font_size=32),
                                                 MathTex(r"X:\ \text{box};\ x_0\in X:\ \text{centre};\ Y\approx1/f'(x_0);\ f'(X):\ \text{slope over the whole box, as an interval}", font_size=24, color=MUTED),
                                                 MathTex(r"\textbf{Theorem: }K(X)\subset X\ \Rightarrow\ X\ \text{contains exactly one solution of }f=0", font_size=28, color=YELLOW)], width=72).next_to(h, DOWN, buff=0.4)
        self.hold(9, ([FadeIn(h), FadeIn(d1)], 4.5))
        why = idea("why", "x ↦ x − Y f(x) has the solutions as fixed points. K(X) contains everything this map does to X. If K(X) ⊂ X the map sends the box into itself ⇒ a fixed point exists inside (Brouwer). The small factor 1 − Y f′ makes it a contraction ⇒ unique.", width=72, font_size=22).next_to(d1, DOWN, buff=0.35)
        self.hold(10, ([FadeIn(why)], 4))
        self.play(FadeOut(why), d1.animate.scale(0.7).next_to(h, DOWN, buff=0.2), run_time=0.5)
        w = VGroup(MathTex(r"X=[1.41,1.42],\ x_0=1.415,\ f(x_0)=1.415^2-2=0.002225,\ Y=\tfrac1{2.83}=0.3534", font_size=26),
                   MathTex(r"x_0-Yf(x_0)=1.415-0.000786=1.414214", font_size=26),
                   MathTex(r"f'(X)=2X=[2.82,2.84];\ Yf'(X)=[0.9965,1.0035];\ 1-Yf'(X)=[-0.0035,0.0035]", font_size=26),
                   MathTex(r"(1-Yf'(X))(X-x_0)=[-0.0035,0.0035]\cdot[-0.005,0.005]=[-0.000018,0.000018]", font_size=26),
                   MathTex(r"K(X)=[1.414196,\ 1.414231]\ \subset\ [1.41,1.42]\ \checkmark", font_size=32, color=GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(d1, DOWN, buff=0.35)
        self.hold(11, ([Write(w[0])], 3.5), ([Write(w[1])], 2.5))
        self.hold(12, ([Write(w[2])], 3.5), ([Write(w[3])], 3.5))
        line = NumberLine(x_range=[1.41, 1.42, 0.005], length=8, include_numbers=True, color=MUTED, decimal_number_config={"num_decimal_places": 3}).to_edge(DOWN, buff=0.9)
        kbox = Rectangle(width=line.n2p(1.414231)[0]-line.n2p(1.414196)[0]+0.08, height=0.4, color=GREEN, fill_opacity=0.5).move_to(line.n2p(1.4142135))
        kl = MathTex("K(X)", font_size=24, color=GREEN).next_to(kbox, UP, buff=0.1)
        self.hold(13, ([Write(w[4])], 2.5), ([Create(line), FadeIn(kbox), FadeIn(kl)], 2),
                  ([FadeIn(wrap("√2 exists and lies in the box — proved, without computing it exactly. The shape of every certification in Part Two.", 80, 22, YELLOW).to_edge(DOWN, buff=0.15))], 2))
        self.clear_all()

# ---------------------------------------------------------------- E12S05  Which equations
class E12S05(BeatScene):
    SCENE_ID = 'E12S05'
    def construct(self):
        h = header("Which equations to certify")
        a = VGroup(MathTex(r"T\ \text{is a product of }n\text{ matrices of fractions of the unknowns: horrible for intervals}", font_size=26),
                   MathTex(r"k=3:\ \text{image of }w\mapsto T\text{ is 51-dimensional inside 64: degenerate; Krawczyk needs a square, nondegenerate system}", font_size=24, color=RED)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(h, DOWN, buff=0.5)
        self.hold(14, ([FadeIn(h), Write(a[0])], 3), ([Write(a[1])], 3.5))
        b = card("certify the nullity directly", [MathTex(r"\operatorname{null}A\ge r\iff\exists\,K\ (2n\times r,\ \text{full rank}):\ A\,K=0", font_size=28),
                                                   MathTex(r"K=\begin{pmatrix}I_r\\ X\end{pmatrix}\ \text{(rows permuted)}:\quad f(w,X)=A(w)\,K(X)=0", font_size=28),
                                                   wrap("bilinear: each term is (entry of w)·(entry of X) or an entry of w alone. Degree 2, whole-number coefficients, Jacobian linear in the unknowns: cheap, tight intervals.", 80, 22, MUTED)], color=GREEN, width=70).next_to(a, DOWN, buff=0.4)
        self.hold(15, ([FadeIn(b)], 5))
        self.play(FadeOut(a), b.animate.scale(0.6).next_to(h, DOWN, buff=0.15), run_time=0.5)
        trap = card("the trap that nearly broke it", [MathTex(r"A\text{ symmetric}\ \Rightarrow\ K^{\!\top}AK\text{ symmetric}\ \Rightarrow\ \binom r2\text{ equations are consequences of the others}", font_size=26),
                                                       wrap("choosing which to keep by numerical pivoting can silently leave r(r−1)/2 of them unproved — 28 at r = 8 — while the test passes", 90, 20, RED),
                                                       wrap("fix (structural): all equations on the non-pivot rows + the upper triangle of the r × r pivot block; symmetry forces the rest", 90, 20, GREEN),
                                                       wrap("A passing test is not a proof until you have checked that the test tests the right thing.", 90, 22, YELLOW)], color=RED, width=70, title_size=26).next_to(b, DOWN, buff=0.25)
        self.hold(16, ([FadeIn(trap)], 6))
        self.clear_all()

# ---------------------------------------------------------------- E12S06  Exact arithmetic, results
class E12S06(BeatScene):
    SCENE_ID = 'E12S06'
    def construct(self):
        h = header("Exact arithmetic, and the results")
        ex = bullets(["Krawczyk needs three bounds: residual at the centre, preconditioned Jacobian over the box, contraction constant α < 1",
                      "every float is a fraction with a power-of-two denominator ⇒ the centre is an exact fraction",
                      "bilinear with whole-number coefficients ⇒ residual and Jacobian at the centre are exact fractions",
                      "Y is arbitrary ⇒ round it to a fraction for free",
                      "α < 1 is a comparison of two whole numbers"], font_size=24, width=78).next_to(h, DOWN, buff=0.5)
        self.hold(17, ([FadeIn(h)], 0.8), ([FadeIn(ex, lag_ratio=0.25)], 6))
        sp = MathTex(r"\text{speed: huge integers in base }2^{20}\text{ with balanced digits; each digit product is exact in float64; fast matrix libraries do the rest}", font_size=24, color=MUTED).next_to(ex, DOWN, buff=0.4)
        self.hold(18, ([Write(sp)], 3.5))
        self.play(FadeOut(ex), FadeOut(sp), run_time=0.4)
        res = card("certified", [MathTex(r"Z(P(n,3))=M(P(n,3))=8\qquad n=17,18,\dots,33", font_size=36, color=GREEN),
                                  MathTex(r"\text{primes }17,19,23,29,31\ \text{included: unreachable by any rotation-invariant certificate}", font_size=26),
                                  Text("…but still one n at a time. Next: every n at once.", font_size=26, color=YELLOW)], color=GREEN, width=70).next_to(h, DOWN, buff=0.8)
        self.hold(19, ([FadeIn(res)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E12S07  Recap
class E12S07(BeatScene):
    SCENE_ID = 'E12S07'
    def construct(self):
        h = header("Recap: what you can now do")
        b = bullets(["carry out three Newton steps for x² = 2 by hand",
                     "explain why a numerical solution is not a proof",
                     "do interval arithmetic: x² − 2 for x ∈ [1.41, 1.42]",
                     "state Krawczyk's test and the fixed-point idea; run it for √2",
                     "explain why the project certifies A K = 0 rather than T = I",
                     "explain the pivoting trap and its fix; why the final test is in exact fractions"], font_size=26, width=70).next_to(h, DOWN, buff=0.6)
        self.hold(20, ([FadeIn(h)], 0.8), ([FadeIn(b, lag_ratio=0.2)], 5))
        self.clear_all()
