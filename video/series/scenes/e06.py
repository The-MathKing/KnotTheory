from lib import *

def Dk_fn(k):
    T = np.polynomial.chebyshev.Chebyshev.basis(k)
    return lambda u: (7+4*u*T(u))**2 - 8*(2*u+2*T(u))**2

def largest_root_below_1(k):
    f = Dk_fn(k); us = np.linspace(0.5, 0.999999, 200001); v = f(us)
    idx = np.where(np.sign(v[:-1]) != np.sign(v[1:]))[0]
    return us[idx[-1]]

# ---------------------------------------------------------------- E06S01  The condition
class E06S01(BeatScene):
    SCENE_ID = 'E06S01'
    def construct(self):
        t = title_card("Episode 6", "From an eigenvalue test to a polynomial: D_k")
        self.hold(1, ([FadeIn(t)], 1.5), ([FadeOut(t)], 0.5), ([FadeIn(header("The condition, written out"))], 0.8),
                  ([Write(MathTex(r"M_j=\begin{pmatrix}\alpha&1\\1&\beta\end{pmatrix},\quad \lambda_\pm=\frac{\alpha+\beta}{2}\pm\sqrt{\Bigl(\frac{\alpha-\beta}{2}\Bigr)^2+1},\qquad -2\sqrt2\le\lambda_-\le\lambda_+\le2\sqrt2\ ?", font_size=30).shift(UP*1.7))], 3))
        warn = wrap("Trouble: square roots on both sides. Deciding whether one square root is below another, when they are nearly equal, is where decimal computation starts guessing. Goal: no square roots, whole-number coefficients.", 70, 26, ORANGE).shift(UP*0.2)
        self.hold(2, ([FadeIn(warn)], 3))
        sh = card("shorthand", [MathTex(r"A=\alpha+\beta,\qquad P=\alpha\beta,\qquad \lambda_\pm=\tfrac A2\pm\tfrac12\sqrt{(\alpha-\beta)^2+4}", font_size=30),
                                MathTex(r"|\alpha|,|\beta|\le2\ \Rightarrow\ -4\le A\le4,\quad -4\le P\le4", font_size=28, color=MUTED)], color=BLUE, width=60).shift(DOWN*1.8)
        self.hold(3, ([FadeIn(sh)], 3))
        self.clear_all()

# ---------------------------------------------------------------- E06S02  Squaring warning
class E06S02(BeatScene):
    SCENE_ID = 'E06S02'
    def construct(self):
        h = header("A warning about squaring")
        ex = VGroup(MathTex(r"-3<2\qquad\text{but}\qquad 9\not<4", font_size=40, color=RED),
                    wrap("Squaring preserves an inequality only when both sides are nonnegative. Then the squared inequality is equivalent (you can go back), not merely implied.", 64, 26)).arrange(DOWN, buff=0.4).next_to(h, DOWN, buff=0.6)
        self.hold(4, ([FadeIn(h)], 0.8), ([Write(ex[0])], 2), ([FadeIn(ex[1])], 3))
        plan = idea("the plan", "Square twice. Before each squaring, check both sides ≥ 0 using −4 ≤ A, P ≤ 4. Those two checks are the entire rigour of the episode.", width=60).next_to(ex, DOWN, buff=0.5)
        self.hold(5, ([FadeIn(plan)], 2.5))
        self.clear_all()

# ---------------------------------------------------------------- E06S03  First squaring
class E06S03(BeatScene):
    SCENE_ID = 'E06S03'
    def construct(self):
        h = header("First squaring")
        e1 = MathTex(r"\tfrac A2+\tfrac12\sqrt{(\alpha-\beta)^2+4}\le2\sqrt2\quad\Longleftrightarrow\quad\sqrt{(\alpha-\beta)^2+4}\ \le\ 4\sqrt2-A", font_size=32).next_to(h, DOWN, buff=0.5)
        self.hold(6, ([FadeIn(h)], 0.8), ([Write(e1)], 3))
        chk = card("check before squaring", [MathTex(r"\text{LHS}\ge0\ \text{(a square root)};\quad \text{RHS}=4\sqrt2-A\ge5.66-4=1.66>0", font_size=28),
                                             Text("both sides nonnegative ⇒ squaring is an equivalence", font_size=26, color=GREEN)], color=GREEN, width=60).next_to(e1, DOWN, buff=0.4)
        self.hold(7, ([FadeIn(chk)], 3))
        self.play(chk.animate.scale(0.7).to_edge(RIGHT, buff=0.3).shift(DOWN*2.4), run_time=0.6)
        steps = VGroup(MathTex(r"(\alpha-\beta)^2+4\le32-8\sqrt2A+A^2", font_size=30),
                       MathTex(r"\text{identity: }A^2-(\alpha-\beta)^2=4\alpha\beta=4P\ \Rightarrow\ (\alpha-\beta)^2=A^2-4P", font_size=28, color=MUTED),
                       MathTex(r"A^2-4P+4\le32-8\sqrt2A+A^2\ \Rightarrow\ 8\sqrt2A-4P\le28", font_size=30),
                       MathTex(r"2\sqrt2\,A-P\le7", font_size=36, color=YELLOW)).arrange(DOWN, buff=0.28).next_to(e1, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        self.hold(8, ([Write(steps[0])], 2), ([Write(steps[1])], 3), ([Write(steps[2])], 3), ([Write(steps[3])], 2))
        mirror = VGroup(MathTex(r"\lambda_-\ge-2\sqrt2:\ \text{replace }A\to-A:\quad -2\sqrt2\,A-P\le7", font_size=30),
                        MathTex(r"\text{together: }2\sqrt2\,|A|\le7+P", font_size=38, color=YELLOW)).arrange(DOWN, buff=0.3).next_to(steps, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        self.hold(9, ([FadeOut(chk)], 0.3), ([Write(mirror[0])], 2.5), ([Write(mirror[1])], 2))
        self.clear_all()

# ---------------------------------------------------------------- E06S04  Second squaring
class E06S04(BeatScene):
    SCENE_ID = 'E06S04'
    def construct(self):
        h = header("Second squaring")
        e = MathTex(r"2\sqrt2\,|A|\le7+P", font_size=40, color=YELLOW).next_to(h, DOWN, buff=0.5)
        chk = card("check", [MathTex(r"\text{LHS}\ge0;\quad \text{RHS}=7+P\ge7-4=3>0\ \Rightarrow\ \text{squaring is an equivalence}", font_size=28, color=GREEN)], color=GREEN, width=64).next_to(e, DOWN, buff=0.4)
        self.hold(10, ([FadeIn(h), Write(e)], 1.5), ([FadeIn(chk)], 3))
        sq = VGroup(MathTex(r"8A^2\le(7+P)^2\quad\Longleftrightarrow\quad D:=(7+P)^2-8A^2\ \ge\ 0", font_size=36),
                    Text("no square roots anywhere", font_size=28, color=GREEN)).arrange(DOWN, buff=0.3).next_to(chk, DOWN, buff=0.5)
        self.hold(11, ([Write(sq[0])], 3), ([FadeIn(sq[1])], 1.5))
        pause = wrap("Two inequalities with nested radicals became one sign condition. The checks (RHS ≥ 1.66, RHS ≥ 3) are what guarantee nothing was lost or gained.", 66, 24, MUTED).next_to(sq, DOWN, buff=0.5)
        self.hold(12, ([FadeIn(pause)], 3))
        self.clear_all()

# ---------------------------------------------------------------- E06S05  Chebyshev
class E06S05(BeatScene):
    SCENE_ID = 'E06S05'
    def construct(self):
        h = header("Cosines become a polynomial: Chebyshev")
        s = MathTex(r"\alpha=2\cos t=2u,\qquad \beta=2\cos kt\ =\ ?\qquad(u:=\cos t)", font_size=34).next_to(h, DOWN, buff=0.5)
        key = Text("key fact: cos(kt) is a polynomial in cos(t) with whole-number coefficients", font_size=26, color=YELLOW).next_to(s, DOWN, buff=0.4)
        self.hold(13, ([FadeIn(h), Write(s)], 2), ([FadeIn(key)], 2))
        d1 = defn("Chebyshev polynomial T_k", [MathTex(r"\cos kt=T_k(\cos t)", font_size=30),
                                                MathTex(r"T_0=1,\ T_1=u,\ T_2=2u^2-1,\ T_3=4u^3-3u,\qquad T_{k+1}=2uT_k-T_{k-1}", font_size=28),
                                                MathTex(r"\text{check: }2u\cdot u-1=2u^2-1\ \checkmark", font_size=26, color=MUTED)], width=64).next_to(key, DOWN, buff=0.4)
        self.hold(14, ([FadeIn(d1)], 3.5))
        self.play(FadeOut(s), FadeOut(key), d1.animate.scale(0.62).next_to(h, DOWN, buff=0.2), run_time=0.6)
        sub = VGroup(MathTex(r"\beta=2T_k(u),\quad A=2u+2T_k(u),\quad P=4uT_k(u)", font_size=28),
                     MathTex(r"D_k(u)=\bigl(7+4u\,T_k(u)\bigr)^2-8\bigl(2u+2T_k(u)\bigr)^2\ \in\mathbb Z[u],\quad \deg D_k=2k+2", font_size=30, color=TEAL)).arrange(DOWN, buff=0.25).next_to(d1, DOWN, buff=0.3)
        self.hold(15, ([Write(sub[0])], 2.5), ([Write(sub[1])], 3.5))
        d2 = card("k = 2, expanded", [MathTex(r"T_2=2u^2-1:\ \ 7+4uT_2=8u^3-4u+7,\quad 2u+2T_2=4u^2+2u-2", font_size=26),
                                      MathTex(r"D_2(u)=64u^6-192u^4-16u^3+112u^2+8u+17", font_size=32, color=YELLOW),
                                      MathTex(r"\text{constant term: }7^2-8\cdot2^2=49-32=17\ \checkmark", font_size=26, color=MUTED)], color=YELLOW, width=66).to_edge(DOWN, buff=0.3)
        self.hold(16, ([FadeIn(d2)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E06S06  D_2 on three graphs
class E06S06(BeatScene):
    SCENE_ID = 'E06S06'
    def construct(self):
        h = header("Worked example: D₂ on three graphs")
        test = MathTex(r"P(n,k)\ \text{Ramanujan}\iff D_k\Bigl(\cos\tfrac{2\pi j}{n}\Bigr)\ge0\ \text{ for every nontrivial }j", font_size=30, color=YELLOW).next_to(h, DOWN, buff=0.4)
        f = Dk_fn(2)
        ax = Axes(x_range=[-1, 1, 0.5], y_range=[-20, 60, 20], x_length=7, y_length=3.6, axis_config={"include_tip": False, "color": MUTED},
                  x_axis_config={"include_numbers": True}, y_axis_config={"include_numbers": True}).to_edge(LEFT, buff=0.6).shift(DOWN*1.3)
        cur = ax.plot(f, x_range=[-1, 1, 0.005], color=BLUE)
        self.hold(17, ([FadeIn(h), Write(test)], 2.5), ([Create(ax), Create(cur)], 2))
        rows = VGroup(MathTex(r"P(5,2):\ u=\cos72^\circ=0.309,\quad D_2=28\ \ (>0)", font_size=28, color=GREEN),
                      MathTex(r"P(23,2):\ u=0.9629,\quad D_2=0.217\ \ (>0,\ \text{small})", font_size=28, color=GREEN),
                      MathTex(r"P(24,2):\ u=\cos15^\circ=0.9659,\quad D_2=-0.352\ \ (<0)\ \text{fails}", font_size=28, color=RED)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4).shift(DOWN*1.0)
        pts = [Dot(ax.c2p(np.cos(2*PI/n), f(np.cos(2*PI/n))), color=c, radius=0.09) for n, c in ((5, GREEN), (23, GREEN), (24, RED))]
        self.play(FadeIn(rows[0]), FadeIn(pts[0]), run_time=1.5)
        self.hold(18, ([FadeIn(rows[1]), FadeIn(pts[1])], 2), ([FadeIn(rows[2]), FadeIn(pts[2])], 2))
        zoom = MathTex(r"\text{between }n=23\text{ and }24\text{ the property switches off, and stays off (next)}", font_size=26, color=MUTED).to_edge(DOWN, buff=0.4)
        self.hold(19, ([FadeIn(zoom)], 2))
        self.clear_all()

# ---------------------------------------------------------------- E06S07  Band at u=1
class E06S07(BeatScene):
    SCENE_ID = 'E06S07'
    def construct(self):
        h = header("The band at u = 1")
        k = 2; f = Dk_fn(k)
        ax = Axes(x_range=[-1, 1, 0.5], y_range=[-20, 60, 20], x_length=8.5, y_length=3.4, axis_config={"include_tip": False, "color": MUTED},
                  x_axis_config={"include_numbers": True}, y_axis_config={"include_numbers": True}).shift(DOWN*1.7)
        cur = ax.plot(f, x_range=[-1, 1, 0.005], color=BLUE)
        c1 = MathTex(r"u=1:\ T_k(1)=1,\ A=4,\ P=4:\quad D_k(1)=(7+4)^2-8\cdot4^2=121-128=-7\ \ \text{for every }k", font_size=28).next_to(h, DOWN, buff=0.4)
        p1 = Dot(ax.c2p(1, -7), color=RED, radius=0.1)
        self.hold(20, ([FadeIn(h), Create(ax), Create(cur)], 1.5), ([Write(c1)], 3), ([FadeIn(p1, scale=3)], 1))
        uk = largest_root_below_1(k)
        band = Rectangle(width=ax.c2p(1, 0)[0]-ax.c2p(uk, 0)[0], height=3.4, color=RED, fill_opacity=0.2, stroke_width=0).move_to(ax.c2p((1+uk)/2, 20))
        nt = ValueTracker(8)
        j1 = always_redraw(lambda: Dot(ax.c2p(np.cos(2*PI/nt.get_value()), f(np.cos(2*PI/nt.get_value()))), color=YELLOW, radius=0.1))
        j1l = always_redraw(lambda: MathTex(r"j=1,\ n=%d" % int(nt.get_value()), font_size=28, color=YELLOW).next_to(j1, UL, buff=0.2))
        bl = MathTex(r"u_k=\text{largest root below }1;\ \text{band }[u_k,1]\text{ where }D_k<0", font_size=26, color=RED).next_to(c1, DOWN, buff=0.3)
        self.hold(21, ([FadeIn(band), FadeIn(bl)], 1.5), ([FadeIn(j1), FadeIn(j1l)], 1), ([nt.animate.set_value(30)], 6))
        self.play(FadeOut(bl), FadeOut(c1), run_time=0.4)
        bk = VGroup(MathTex(r"\text{fail}\iff\cos\tfrac{2\pi}{n}>u_k\iff n>B_k:=\frac{2\pi}{\arccos u_k}", font_size=30, color=YELLOW),
                    MathTex(r"k=2:\ u_2=0.9641,\ B_2=23.37\ \Rightarrow\ n\le23\ \checkmark", font_size=28),
                    MathTex(r"B_3=32.5,\quad B_4=42.0\quad(\text{all sharp: }23,32,42)", font_size=28)).arrange(DOWN, buff=0.25).next_to(h, DOWN, buff=0.35)
        self.hold(22, ([Write(bk[0])], 3), ([Write(bk[1])], 2.5), ([Write(bk[2])], 2.5))
        self.play(FadeOut(bk), FadeOut(j1), FadeOut(j1l), run_time=0.4)
        c2 = VGroup(MathTex(r"u=-1:\ \cos kt=(-1)^k", font_size=28),
                    MathTex(r"k\text{ odd}:\ A=-4,\ P=4:\ D=121-128=-7\quad\text{(second band)}", font_size=28, color=RED),
                    MathTex(r"k\text{ even}:\ A=0,\ P=-4:\ D=9-0=9\quad\text{(no band)}", font_size=28, color=GREEN)).arrange(DOWN, buff=0.25).next_to(h, DOWN, buff=0.35)
        pm = Dot(ax.c2p(-1, f(-1)), color=GREEN, radius=0.1)
        self.hold(23, ([Write(c2[0])], 2), ([Write(c2[1])], 2.5), ([Write(c2[2]), FadeIn(pm, scale=3)], 2.5))
        self.clear_all()

# ---------------------------------------------------------------- E06S08  Recap
class E06S08(BeatScene):
    SCENE_ID = 'E06S08'
    def construct(self):
        h = header("Recap: what you can now do")
        b = bullets(["explain when squaring an inequality is safe, and do the two checks",
                     "derive 2√2|A| ≤ 7 + P from the eigenvalue formula",
                     "explain why cos(kt) is a polynomial in cos(t); write T₂, T₃",
                     "define D_k(u), expand D₂, evaluate it at cos 72° to get 28",
                     "show D_k(1) = −7 and explain why that caps n for each k",
                     "compute D_k(−1) for odd and even k"], font_size=28, width=62).next_to(h, DOWN, buff=0.6)
        self.hold(24, ([FadeIn(h)], 0.8), ([FadeIn(b, lag_ratio=0.2)], 5))
        nxt = Text("Next: k leaves the geometry, and the family becomes finite", font_size=30, color=YELLOW).to_edge(DOWN, buff=0.8)
        self.hold(25, ([FadeIn(nxt)], 1.5))
        self.clear_all()
