from lib import *
import json

# ---------------------------------------------------------------- E08S01  Finite computation
class E08S01(BeatScene):
    SCENE_ID = 'E08S01'
    def construct(self):
        t = title_card("Episode 8", "Deciding exactly, and the complete classification")
        self.hold(1, ([FadeIn(t)], 1.5), ([FadeOut(t)], 0.5), ([FadeIn(header("The finite computation"))], 0.8),
                  ([Write(MathTex(r"3\le n\le230,\ 1\le k<\tfrac n2:\quad 13{,}110\ \text{pairs};\ \text{each: is }D_k(u_j)\ge0\ \text{at every nontrivial }j?", font_size=30).shift(UP*1.5))], 3))
        w = VGroup(MathTex(r"P(23,2):\ D_2=+0.217\qquad P(24,2):\ D_2=-0.352\qquad\text{comfortable}", font_size=28),
                   MathTex(r"\text{large }k:\ \deg D_k=2k+2,\ \text{coefficients in the millions},\ D_k(u_j)=\pm0.000001\ ?", font_size=28, color=ORANGE),
                   Text("a finite computation is not yet a proof: can a computer tell the sign?", font_size=28, color=YELLOW)).arrange(DOWN, buff=0.4).shift(DOWN*0.6)
        self.hold(2, ([Write(w[0])], 2.5), ([Write(w[1])], 3), ([FadeIn(w[2])], 2))
        self.clear_all()

# ---------------------------------------------------------------- E08S02  Floating point
class E08S02(BeatScene):
    SCENE_ID = 'E08S02'
    def construct(self):
        h = header("How computers store numbers, and where they lie")
        d1 = defn("floating point", "sign + about 53 binary digits + exponent ≈ 16 decimal digits. Anything needing more is rounded.", width=60).next_to(h, DOWN, buff=0.4)
        ex = VGroup(MathTex(r"0.1\ \text{stored as}\ 0.1000000000000000055\ldots", font_size=28),
                    MathTex(r"0.1+0.2=0.30000000000000004\ \ne\ 0.3", font_size=32, color=RED),
                    Text("harmless — until the sign of a difference of nearly equal numbers is the answer", font_size=24, color=MUTED)).arrange(DOWN, buff=0.3).next_to(d1, DOWN, buff=0.4)
        self.hold(3, ([FadeIn(h), FadeIn(d1)], 2), ([Write(ex[0])], 2), ([Write(ex[1])], 2), ([FadeIn(ex[2])], 2))
        self.play(FadeOut(ex), FadeOut(d1), run_time=0.4)
        chain = VGroup(Text("cos → powers up to 2k+2 → × large coefficients → nearly cancelling sums", font_size=26),
                       MathTex(r"\text{each step rounds; error can reach }10^{-10}\text{ or worse}", font_size=28),
                       MathTex(r"\text{true value }10^{-12}\ \Rightarrow\ \text{computed sign is a coin flip}", font_size=30, color=RED),
                       Text("a classification that depends on coin flips is not a classification", font_size=28, color=YELLOW)).arrange(DOWN, buff=0.35).next_to(h, DOWN, buff=0.6)
        self.hold(4, ([FadeIn(chain, lag_ratio=0.3)], 5))
        fix = wrap("so: decide the sign in a way that cannot be wrong, by noticing what kind of number D_k(u_j) is", 70, 26, GREEN).to_edge(DOWN, buff=0.6)
        self.hold(5, ([FadeIn(fix)], 2))
        self.clear_all()

# ---------------------------------------------------------------- E08S03  Algebraic integers
class E08S03(BeatScene):
    SCENE_ID = 'E08S03'
    def construct(self):
        h = header("Algebraic integers, in one example")
        d1 = defn("algebraic integer", "A root of a polynomial with whole-number coefficients and leading coefficient 1.", width=60).next_to(h, DOWN, buff=0.4)
        exs = VGroup(MathTex(r"\sqrt2:\ x^2-2", font_size=28), MathTex(r"\varphi:\ x^2-x-1", font_size=28),
                     MathTex(r"2\cos72^\circ:\ x^2+x-1", font_size=28), MathTex(r"2\cos\tfrac{2\pi}{7}:\ x^3+x^2-2x-1", font_size=28),
                     MathTex(r"2\cos\tfrac{2\pi j}{n}=\zeta^j+\zeta^{-j},\quad \zeta:\ x^n-1", font_size=28, color=YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(d1, DOWN, buff=0.4)
        self.hold(6, ([FadeIn(h), FadeIn(d1)], 2), ([FadeIn(exs, lag_ratio=0.25)], 5))
        self.play(FadeOut(exs), run_time=0.4)
        cl = VGroup(Text("sums and products of algebraic integers are algebraic integers", font_size=26),
                    MathTex(r"D_k(u_j)\ \text{is built from }2\cos\text{ values by }+,\ \times,\ \text{whole numbers}\ \Rightarrow\ D_k(u_j)\in\mathbb Z[\zeta]", font_size=28, color=GREEN)).arrange(DOWN, buff=0.3).next_to(d1, DOWN, buff=0.5)
        self.hold(7, ([FadeIn(cl[0])], 2), ([Write(cl[1])], 3))
        key = card("exact representation", [MathTex(r"\text{every element of }\mathbb Z[\zeta]=c_0+c_1\zeta+c_2\zeta^2+\cdots\ \text{uniquely, }c_i\in\mathbb Z", font_size=26),
                                             Text("(ζ satisfies the n-th cyclotomic polynomial; reduce modulo it)", font_size=22, color=MUTED),
                                             Text("+ and × on these lists are exact. Zero exactly when every cᵢ = 0.", font_size=26, color=YELLOW)], color=YELLOW, width=66).next_to(cl, DOWN, buff=0.4)
        self.hold(8, ([FadeIn(key)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E08S04  Deciding the sign
class E08S04(BeatScene):
    SCENE_ID = 'E08S04'
    def construct(self):
        h = header("Deciding the sign exactly")
        s1 = bullets(["compute D_k(u_j) as an exact list of whole numbers in ℤ[ζ]",
                      "all zero ⇒ value exactly 0 ⇒ eigenvalue exactly 2√2 ⇒ passes (the condition is ≤)",
                      "nonzero ⇒ need its sign: how far from 0 can a nonzero element be?"], font_size=24, width=80).next_to(h, DOWN, buff=0.4)
        self.hold(9, ([FadeIn(s1, lag_ratio=0.3)], 4))
        sep = card("separation bound", [MathTex(r"\text{nonzero}\ \Rightarrow\ |D_k(u_j)|\ \ge\ 249^{-(\deg-1)}\quad\text{(tiny, but positive and computable)}", font_size=26),
                                        wrap("accept the floating-point sign only if |value| clears the bound by more than the error", 80, 22),
                                        wrap("otherwise refuse, and recompute with more precision", 80, 22, MUTED)], color=GREEN, width=68, title_size=26).next_to(s1, DOWN, buff=0.3)
        self.hold(10, ([FadeIn(sep)], 4))
        disc = VGroup(Text("floating point may propose a sign. It never decides one alone.", font_size=26, weight=BOLD, color=YELLOW),
                      wrap("13,110 cases decided this way, beside an independent float64 control: disagreements ⇒ go look", 80, 22, MUTED)).arrange(DOWN, buff=0.2).next_to(sep, DOWN, buff=0.3)
        self.hold(11, ([FadeIn(disc[0])], 2), ([FadeIn(disc[1])], 2))
        self.clear_all()

# ---------------------------------------------------------------- E08S05  The bug
class E08S05(BeatScene):
    SCENE_ID = 'E08S05'
    def construct(self):
        h = header("The bug the control caught")
        bug = VGroup(Text("k = 1: inner and outer rings step by the same amount ⇒ same power of ζ", font_size=26),
                     MathTex(r"\{\,1{:}\,a,\ 1{:}\,b\,\}\ \longrightarrow\ \text{a lookup table silently keeps one entry}", font_size=30, color=RED),
                     Text("half the terms vanished at k = 1", font_size=26, color=RED),
                     MathTex(r"\text{exact classifier: every }P(n,1)\ \text{``Ramanujan''},\ \text{incl. }P(9,1)\text{ with }\lambda=-2.879<-2\sqrt2", font_size=26)).arrange(DOWN, buff=0.35).next_to(h, DOWN, buff=0.6)
        self.hold(12, ([FadeIn(bug[0])], 2), ([Write(bug[1])], 2.5), ([FadeIn(bug[2])], 1.5), ([Write(bug[3])], 3))
        ctrl = card("the control", "Float64 control flagged four disagreements, all at k = 1. Found and fixed in an afternoon.\nTwo independent methods side by side is not redundancy. It is the only thing that tells you an answer is wrong when it looks right.", color=GREEN, width=64, font_size=24).next_to(bug, DOWN, buff=0.5)
        self.hold(13, ([FadeIn(ctrl)], 3))
        self.clear_all()

# ---------------------------------------------------------------- E08S06  Classification
class E08S06(BeatScene):
    SCENE_ID = 'E08S06'
    def construct(self):
        h = header("The classification")
        pairs = json.load(open(os.path.join(HERE, 'census.json')))
        head = VGroup(MathTex(r"460\ \text{pairs }(n,k)", font_size=34, color=YELLOW), MathTex(r"324\ \text{distinct graphs}", font_size=28),
                      MathTex(r"P(n,k)\cong P(n,l),\ l\equiv\pm k^{\pm1}", font_size=22, color=MUTED),
                      MathTex(r"n_{\max}=112\ (k=41),\quad k_{\max}=45", font_size=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.4).shift(DOWN*0.8)
        self.hold(14, ([FadeIn(h)], 0.8), ([FadeIn(head, lag_ratio=0.3)], 4))
        ax = Axes(x_range=[0, 240, 40], y_range=[0, 50, 10], x_length=8.0, y_length=5.2, axis_config={"include_tip": False, "color": MUTED},
                  x_axis_config={"include_numbers": True}, y_axis_config={"include_numbers": True}).to_edge(LEFT, buff=0.7).shift(DOWN*0.5)
        xl = MathTex("n", font_size=30).next_to(ax.x_axis, RIGHT); yl = MathTex("k", font_size=30).next_to(ax.y_axis, UP)
        dots = VGroup(*[Dot(ax.c2p(n, k), radius=0.035, color=BLUE if k % 2 == 0 else ORANGE) for n, k in pairs])
        dl = DashedLine(ax.c2p(231, 0), ax.c2p(231, 50), color=RED); dll = MathTex("231", font_size=26, color=RED).next_to(dl, UP, buff=0.1)
        run2 = SurroundingRectangle(VGroup(*[d for d, (n, k) in zip(dots, pairs) if k == 2]), color=BLUE, buff=0.05)
        run4 = SurroundingRectangle(VGroup(*[d for d, (n, k) in zip(dots, pairs) if k == 4]), color=BLUE, buff=0.05)
        rl = MathTex(r"k=2:\ 5..23;\ k=4:\ 9..42\ (=B_k)", font_size=22, color=BLUE).next_to(head, DOWN, buff=0.4, aligned_edge=LEFT)
        self.hold(15, ([Create(ax), FadeIn(xl), FadeIn(yl)], 1.5), ([FadeIn(dots, lag_ratio=0.004)], 4), ([Create(dl), FadeIn(dll)], 1.5), ([Create(run2), Create(run4), FadeIn(rl)], 2))
        run9 = SurroundingRectangle(VGroup(*[d for d, (n, k) in zip(dots, pairs) if k == 9]), color=ORANGE, buff=0.05)
        pl = wrap("odd k: even n only in the upper half (parity law). k = 9: 19..46, then even n to 90", 34, 20, ORANGE).next_to(rl, DOWN, buff=0.3, aligned_edge=LEFT)
        self.hold(16, ([FadeOut(run2), FadeOut(run4), Create(run9)], 1.5), ([FadeIn(pl)], 2.5))
        top = SurroundingRectangle(VGroup(*[d for d, (n, k) in zip(dots, pairs) if k > 25]), color=YELLOW, buff=0.08)
        tl = wrap("k > 25: no even k survives; only odd k, up to 45 (the −3 exemption)", 34, 20, YELLOW).next_to(pl, DOWN, buff=0.3, aligned_edge=LEFT)
        self.hold(17, ([FadeOut(run9), Create(top)], 1.5), ([FadeIn(tl)], 2.5))
        nm = wrap("k=8 → 49, k=9 → 90, k=10 → 52: not monotone in k", 34, 20, MUTED).next_to(tl, DOWN, buff=0.3, aligned_edge=LEFT)
        self.hold(18, ([FadeOut(top), Write(nm)], 2.5))
        self.clear_all()

# ---------------------------------------------------------------- E08S07  Part One honestly
class E08S07(BeatScene):
    SCENE_ID = 'E08S07'
    def construct(self):
        h = header("What Part One was, honestly")
        steps = ["poles of a zeta function", "Ihara ⇒ an eigenvalue bound", "rotation symmetry ⇒ sign of a polynomial on a grid",
                 "two justified squarings ⇒ D_k ∈ ℤ[u]", "change of variable ⇒ Q without k", "Dirichlet ⇒ finite in (n, k)", "exact arithmetic in ℤ[ζ] ⇒ certified"]
        chain = VGroup(*[Text(s, font_size=24) for s in steps]).arrange(DOWN, buff=0.22).to_edge(LEFT, buff=0.7).shift(DOWN*0.3)
        arrows = VGroup(*[Arrow(chain[i].get_bottom(), chain[i+1].get_top(), buff=0.04, color=MUTED, stroke_width=2, max_tip_length_to_length_ratio=0.3) for i in range(len(steps)-1)])
        self.hold(19, ([FadeIn(h)], 0.8), ([FadeIn(chain, lag_ratio=0.15), FadeIn(arrows, lag_ratio=0.15)], 6))
        r = VGroup(Text("contribution: exactness and completeness, not surprise", font_size=26, weight=BOLD),
                   Text("Droll (unitary Cayley), Le–Sander (integral circulants): same shape, finitely many", font_size=22, color=MUTED),
                   Text("predictable: the shape.  Not predictable: which 460, and nothing past k = 45.", font_size=24, color=YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(UP*0.5)
        self.hold(20, ([FadeIn(r, lag_ratio=0.3)], 4))
        p2 = VGroup(Text("Part Two", font_size=40, weight=BOLD, color=TEAL), Text("same graph, same symmetry, same grid. The matrix is no longer fixed.", font_size=24, color=MUTED)).arrange(DOWN, buff=0.3).next_to(r, DOWN, buff=0.8).to_edge(RIGHT, buff=0.5)
        self.hold(21, ([FadeIn(p2)], 2.5))
        self.clear_all()

# ---------------------------------------------------------------- E08S08  Recap
class E08S08(BeatScene):
    SCENE_ID = 'E08S08'
    def construct(self):
        h = header("Recap: what you can now do")
        b = bullets(["explain floating point and why 0.1 + 0.2 ≠ 0.3",
                     "explain why the sign of a tiny value cannot be trusted from floats alone",
                     "define an algebraic integer; give three examples",
                     "explain why D_k(u_j) is an exact list of whole numbers in ℤ[ζ]",
                     "explain the separation bound and the accept-or-refuse rule",
                     "tell the k = 1 bug story; state the classification (460 / 324 / 112 / 45)"], font_size=27, width=66).next_to(h, DOWN, buff=0.6)
        self.hold(22, ([FadeIn(h)], 0.8), ([FadeIn(b, lag_ratio=0.2)], 5))
        self.clear_all()
