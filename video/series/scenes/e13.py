from lib import *

def strip(n_cells, x0, y, w=0.42, h=0.55, dock=None, color=MUTED, interior_color=TEAL):
    g = VGroup()
    for i in range(n_cells):
        isd = dock and i in dock
        r = Rectangle(width=w, height=h, color=color if isd else interior_color, fill_opacity=0.35 if isd else 0.15, stroke_width=1.5).move_to([x0 + i*w, y, 0])
        g.add(r)
    return g

# ---------------------------------------------------------------- E13S01  One n at a time
class E13S01(BeatScene):
    SCENE_ID = 'E13S01'
    def construct(self):
        t = title_card("Episode 13", "Tiles: from each n to every n")
        self.hold(1, ([FadeIn(t)], 1.5), ([FadeOut(t)], 0.5), ([FadeIn(header("The problem with one n at a time"))], 0.8),
                  ([FadeIn(wrap("Episode 12: n = 17 … 33, each certified separately. Krishnan's conjecture: every n ≥ 13. Infinitely many n cannot be certified one at a time. We need finitely many certified pieces that produce a certificate for every n.", 70, 26).shift(UP*1.2))], 4))
        n = 16; R = 1.7; c = LEFT*3.8+DOWN*1.5
        ring = VGroup(*[Square(side_length=0.38, color=TEAL, fill_opacity=0.2).move_to(c + R*np.array([np.cos(PI/2-2*PI*i/n), np.sin(PI/2-2*PI*i/n), 0])).rotate(-2*PI*i/n) for i in range(n)])
        tl = VGroup(*[MathTex(f"T_{{{i}}}", font_size=16).move_to(ring[i]) for i in range(n)])
        clue = VGroup(MathTex(r"T=T_{n-1}\cdots T_1T_0", font_size=34),
                      Text("if the ring were assembled from pieces each contributing I,", font_size=24),
                      MathTex(r"I\cdot I\cdots I=I\quad\text{for any number of factors}", font_size=28, color=YELLOW),
                      Text("different combinations of pieces ⇒ different n", font_size=24, color=MUTED)).arrange(DOWN, buff=0.28).to_edge(RIGHT, buff=0.5).shift(DOWN*1.3)
        self.hold(2, ([FadeIn(ring, lag_ratio=0.05), FadeIn(tl, lag_ratio=0.05)], 2.5), ([FadeIn(clue, lag_ratio=0.3)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E13S02  Docking
class E13S02(BeatScene):
    SCENE_ID = 'E13S02'
    def construct(self):
        h = header("Why pieces interact, and the docking pattern")
        k = 3; L = 14; w = 0.55; x0 = -(L-1)/2*w
        row = strip(L, x0, 1.3, w=w, dock=set(range(k+1)) | set(range(L-k-1, L)))
        win = SurroundingRectangle(VGroup(*row[9:L]), color=YELLOW, buff=0.05)
        wl = Text("a step matrix sees a window of width ≈ 2k+2; near a boundary it straddles two pieces", font_size=22, color=YELLOW).next_to(row, UP, buff=0.3)
        self.hold(3, ([FadeIn(h), FadeIn(row)], 1.5), ([Create(win), FadeIn(wl)], 3))
        self.play(FadeOut(win), FadeOut(wl), run_time=0.4)
        d1 = defn("dock and tile", "Dock: fixed values of the five entries at k+1 consecutive positions, chosen once and for all. Tile: a stretch whose first k+1 and last k+1 positions carry the dock; interior free.\nTwo tiles side by side meet in 2k+2 dock positions, the same for any pair.", width=70, font_size=22).next_to(row, DOWN, buff=0.4)
        dl = Text("dock", font_size=20, color=MUTED).next_to(row[1], UP, buff=0.1); dr = Text("dock", font_size=20, color=MUTED).next_to(row[L-3], UP, buff=0.1); il = Text("interior (free)", font_size=20, color=TEAL).next_to(row[7], UP, buff=0.1)
        self.hold(4, ([FadeIn(dl), FadeIn(dr), FadeIn(il)], 1.5), ([FadeIn(d1)], 4))
        self.play(FadeOut(d1), FadeOut(dl), FadeOut(dr), FadeOut(il), run_time=0.4)
        row2 = strip(L, x0 + L*w, 1.3, w=w, dock=set(range(k+1)) | set(range(L-k-1, L)), interior_color=PURPLE)
        both = VGroup(row, row2)
        self.play(both.animate.scale(0.6).move_to(UP*1.3), run_time=1)
        win2 = SurroundingRectangle(VGroup(*row[L-4:L], *row2[0:4]), color=YELLOW, buff=0.05)
        lem = VGroup(Text("a straddling window sees only dock entries + one tile's interior: the dock is long enough", font_size=22),
                     MathTex(r"\Rightarrow\ \text{tile product depends only on its own interior}\ \Rightarrow\ T=\prod_{\text{tiles}}T_{\text{tile}}", font_size=30, color=GREEN),
                     Text("checked numerically before use: perturb one tile's interior, the others' products are unchanged to the last digit", font_size=20, color=MUTED)).arrange(DOWN, buff=0.3).next_to(both, DOWN, buff=0.6)
        self.hold(5, ([Create(win2)], 1.5), ([FadeIn(lem[0])], 2.5), ([Write(lem[1])], 3), ([FadeIn(lem[2])], 2.5))
        self.clear_all()

# ---------------------------------------------------------------- E13S03  Tiling theorem
class E13S03(BeatScene):
    SCENE_ID = 'E13S03'
    def construct(self):
        h = header("The tiling theorem, with a postage-stamp example")
        thm = card("tiling theorem", [Text("identity tile: product = I, all required entries nonzero", font_size=24, color=MUTED),
                                      MathTex(r"\text{identity tiles of every length in }[L,\,2L)\ \Rightarrow\ \text{for every }n\ge L:", font_size=28),
                                      MathTex(r"Z(P(n,k))=M(P(n,k))=2k+2", font_size=36, color=YELLOW)], color=YELLOW, width=66).next_to(h, DOWN, buff=0.4)
        self.hold(6, ([FadeIn(h), FadeIn(thm)], 4))
        self.play(thm.animate.scale(0.7).next_to(h, DOWN, buff=0.2), run_time=0.5)
        pf = VGroup(MathTex(r"n<2L:\ \text{one tile of length }n.\qquad n\ge2L:\ \text{peel off }L,\ \text{recurse on }n-L\ge L.", font_size=26)).next_to(thm, DOWN, buff=0.3)
        demos = VGroup()
        for i, (n, parts) in enumerate([(35, [35]), (55, [21, 34]), (100, [21, 21, 21, 37])]):
            x = -6.4; row = VGroup()
            for p in parts:
                row.add(strip(p, x + 0.0475, -0.3 - i*0.8, w=0.095, h=0.4, dock=set(range(4)) | set(range(p-4, p)), interior_color=[TEAL, PURPLE, GREEN, ORANGE][len(row) % 4]))
                x += p*0.095
            lab = MathTex(f"n={n}=" + "+".join(map(str, parts)), font_size=22).next_to(row, RIGHT, buff=0.25)
            demos.add(VGroup(row, lab))
        self.hold(7, ([Write(pf)], 3), ([FadeIn(demos[0])], 1.5), ([FadeIn(demos[1])], 1.5), ([FadeIn(demos[2])], 2),
                  ([FadeIn(Text("163 = 6 × 21 + 37. Every n ≥ 21, no gaps, no conditions on n.", font_size=24, color=GREEN).next_to(demos, DOWN, buff=0.35))], 2))
        self.play(FadeOut(demos), FadeOut(pf), *[FadeOut(m) for m in self.mobjects if isinstance(m, Text) and m is not h], run_time=0.5)
        why = card("why the whole interval", "Two coprime lengths, 21 and 22, generate all large n but miss many small ones: the largest unreachable n is 21·22 − 21 − 22 = 419. The interval guarantees nothing is missing from L onward.", color=BLUE, width=66).next_to(thm, DOWN, buff=0.5)
        self.hold(8, ([FadeIn(why)], 4))
        ach = wrap("“for every n ≥ L” has become a finite list: one identity tile per length in [L, 2L), each certified as in episode 12", 70, 24, YELLOW).next_to(why, DOWN, buff=0.5)
        self.hold(9, ([FadeIn(ach)], 3))
        self.clear_all()

# ---------------------------------------------------------------- E13S04  Parameter count
class E13S04(BeatScene):
    SCENE_ID = 'E13S04'
    def construct(self):
        h = header("Do identity tiles exist? Counting parameters")
        cnt = VGroup(MathTex(r"\text{tile of length }\ell:\ \ell-2(k+1)\ \text{interior positions}\times5\ \text{entries}=5(\ell-2k-2)\ \text{unknowns}", font_size=28),
                     MathTex(r"\text{identity condition: }(2k+2)^2\ \text{equations}=64\ \text{at }k=3", font_size=28),
                     MathTex(r"5(\ell-8)\ge64\iff\ell\ge21:\quad \ell=20:\ 60<64;\quad \ell=21:\ 65\ge64", font_size=30, color=YELLOW)).arrange(DOWN, buff=0.3).next_to(h, DOWN, buff=0.5)
        self.hold(10, ([FadeIn(h), Write(cnt[0])], 3.5), ([Write(cnt[1])], 2.5), ([Write(cnt[2])], 3))
        lens = list(range(16, 24)); res = [0.83, 0.78, 0.82, 0.14, 0.37, 1e-14, 1e-14, 1e-14]
        ax = Axes(x_range=[15, 24, 1], y_range=[-15, 1, 5], x_length=5.5, y_length=3.0, axis_config={"include_tip": False, "color": MUTED},
                  x_axis_config={"include_numbers": False}, y_axis_config={"include_numbers": True}).to_edge(LEFT, buff=0.8).shift(DOWN*1.6)
        xnums = VGroup(*[MathTex(str(l), font_size=20, color=MUTED).next_to(ax.c2p(l, -15), DOWN, buff=0.1) for l in (16, 18, 20, 22)])
        yl = MathTex(r"\log_{10}\text{residual}", font_size=22).next_to(ax.y_axis, UP, buff=0.1); xl = MathTex(r"\ell", font_size=26).next_to(ax.x_axis, RIGHT)
        bars = VGroup()
        for l, r in zip(lens, res):
            top = ax.c2p(l, np.log10(r))[1]; bot = ax.c2p(l, -15)[1]
            bars.add(Rectangle(width=0.4, height=top-bot, color=GREEN if r < 1e-10 else RED, fill_opacity=0.6, stroke_width=1).move_to([ax.c2p(l, 0)[0], (top+bot)/2, 0]))
        lab = VGroup(Text("ℓ < 21: Newton stalls, residual ≈ 0.4", font_size=22, color=RED), Text("ℓ ≥ 21: identity tiles found", font_size=22, color=GREEN),
                     Text("k = 3: every length 21 … 43, covering [21, 41] with room", font_size=22), Text("parameter counting predicted the threshold exactly", font_size=22, color=YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(DOWN*1.6)
        self.hold(11, ([Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(xnums)], 1.5), ([FadeIn(bars, lag_ratio=0.1)], 2.5), ([FadeIn(lab, lag_ratio=0.3)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E13S05  Certifying a tile
class E13S05(BeatScene):
    SCENE_ID = 'E13S05'
    def construct(self):
        h = header("Certifying a tile")
        gift = VGroup(MathTex(r"T_{\text{tile}}=I:\ \text{a rational equation, nasty to certify}", font_size=28),
                      MathTex(r"\text{one-tile ring: a single tile of length }\ell\text{ on }P(\ell,k);\ \text{its monodromy is exactly }T_{\text{tile}}", font_size=26),
                      MathTex(r"\Rightarrow\ T_{\text{tile}}=I\iff\operatorname{null}A_{\text{one tile}}=2k+2", font_size=36, color=YELLOW),
                      wrap("the bilinear nullity system of episode 12 again; dock entries pinned at exact whole numbers so certified tiles still fit", 80, 22, MUTED)).arrange(DOWN, buff=0.35).next_to(h, DOWN, buff=0.6)
        self.hold(12, ([FadeIn(h), Write(gift[0])], 2.5), ([Write(gift[1])], 3), ([Write(gift[2])], 2.5), ([FadeIn(gift[3])], 2.5))
        self.play(FadeOut(gift), run_time=0.4)
        tab = MathTex(r"\begin{array}{c|c|c|c} k & \text{tiles} & \text{lengths} & \alpha_{\max}\\ \hline 3 & 23 & 21\text{--}43 & 2.2\times10^{-10}\\ 4 & 33 & 29\text{--}61 & \le10^{-9}\\ 5 & 21 & 54\text{--}75\ (\text{two gaps}) & \le10^{-9}\end{array}", font_size=34).next_to(h, DOWN, buff=0.6)
        tot = VGroup(Text("k = 5: not a full interval, but the lengths still generate every n ≥ 162 as sums", font_size=22, color=MUTED),
                     Text("77 tile certifications + 17 single-n certifications, all in exact rational arithmetic", font_size=26, color=GREEN)).arrange(DOWN, buff=0.3).next_to(tab, DOWN, buff=0.6)
        self.hold(13, ([Write(tab)], 4), ([FadeIn(tot)], 3))
        self.clear_all()

# ---------------------------------------------------------------- E13S06  Theorems and rows
class E13S06(BeatScene):
    SCENE_ID = 'E13S06'
    def construct(self):
        h = header("The theorems, and the complete rows")
        th = VGroup(MathTex(r"Z(P(n,3))=M(P(n,3))=8\qquad n\ge17", font_size=38, color=YELLOW),
                    MathTex(r"Z(P(n,4))=M(P(n,4))=10\qquad n\ge29", font_size=38, color=YELLOW),
                    MathTex(r"Z(P(n,5))=M(P(n,5))=12\qquad n\ge162", font_size=38, color=YELLOW),
                    Text("no divisibility conditions. primes included.", font_size=26, color=MUTED)).arrange(DOWN, buff=0.35).next_to(h, DOWN, buff=0.6)
        self.hold(14, ([FadeIn(h)], 0.8), ([Write(th[0])], 2.5), ([Write(th[1])], 2.5), ([Write(th[2])], 2.5), ([FadeIn(th[3])], 1.5))
        self.play(th.animate.scale(0.5).next_to(h, DOWN, buff=0.1), run_time=0.7)
        srch = VGroup(Text("below the thresholds: exhaustive search, playing the game on every set of each size", font_size=24),
                      Text("the rotation lets a minimum set be assumed to contain a fixed vertex: n times less work, still exact", font_size=22, color=MUTED),
                      MathTex(r"P(28,4):\ \text{every 9-set excluded},\ \approx1.2\times10^{9}\ \text{candidates}", font_size=26),
                      Text("solver reproduced every published value first, including Krishnan's corrected table", font_size=22, color=GREEN)).arrange(DOWN, buff=0.25).next_to(th, DOWN, buff=0.4)
        self.hold(15, ([FadeIn(srch, lag_ratio=0.3)], 5))
        self.play(FadeOut(srch), run_time=0.4)
        ax = Axes(x_range=[4, 30, 2], y_range=[3, 11, 1], x_length=9.5, y_length=3.6, axis_config={"include_tip": False, "color": MUTED},
                  x_axis_config={"include_numbers": True}, y_axis_config={"include_numbers": True}).shift(DOWN*1.4)
        xl = MathTex("n", font_size=26).next_to(ax.x_axis, RIGHT); yl = MathTex("Z", font_size=26).next_to(ax.y_axis, UP)
        z2 = {5:5,6:4,7:6,8:5,9:6,10:6,11:6}; z2.update({n:6 for n in range(12,30)})
        z3 = {7:6,8:6,9:6,10:8,11:7,12:7}; z3.update({n:8 for n in range(13,30)})
        z4 = {9:6,10:6,11:7,12:6,13:8,14:8,15:9,16:8,17:9}; z4.update({n:10 for n in range(18,30)})
        def series(d, col):
            pts = sorted(d.items())
            return VGroup(VMobject(color=col, stroke_width=2).set_points_as_corners([ax.c2p(n, z) for n, z in pts]), VGroup(*[Dot(ax.c2p(n, z), radius=0.055, color=col) for n, z in pts]))
        s2, s3, s4 = series(z2, BLUE), series(z3, ORANGE), series(z4, GREEN)
        leg = VGroup(MathTex("k=2", color=BLUE, font_size=26), MathTex("k=3", color=ORANGE, font_size=26), MathTex("k=4", color=GREEN, font_size=26)).arrange(RIGHT, buff=0.6).next_to(ax, UP, buff=0.05).shift(RIGHT*3)
        self.hold(16, ([Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(leg)], 1.5), ([Create(s2)], 2.5), ([Create(s3)], 2.5), ([Create(s4)], 2.5),
                  ([Indicate(s3[1][3], color=YELLOW, scale_factor=2), Indicate(s4[1][3], color=YELLOW, scale_factor=2)], 1.5))
        self.play(FadeOut(s2), FadeOut(s4), FadeOut(ax), FadeOut(xl), FadeOut(yl), FadeOut(leg), FadeOut(s3), run_time=0.5)
        conj = card("Krishnan's Conjecture 5, proved", [MathTex(r"Z(P(n,3))=8\ \ \forall n\ge13,\qquad 13\ \text{optimal }(Z=7\text{ at }11,12)", font_size=28, color=YELLOW),
                                                        wrap("the missing ingredient he named — a lower bound for all large n — is the tiling theorem", 80, 21),
                                                        wrap("k = 4: first exact determination at all; first infinite family at any k ≥ 4", 80, 21, MUTED)], color=YELLOW, width=66, title_size=26).next_to(th, DOWN, buff=0.2)
        self.hold(17, ([FadeIn(conj)], 4))
        attr = card("attribution, precisely", "The correction of the published theorem (Z(P(12,3)) = 7) is Krishnan's. This project's contribution: the lower bound for all large n, hence the proof of his conjecture, and the k = 4, 5 results. Say exactly that, and no more.", color=RED, width=84, font_size=21, title_size=26).next_to(conj, DOWN, buff=0.25)
        self.hold(18, ([FadeIn(attr)], 3.5))
        self.clear_all()

# ---------------------------------------------------------------- E13S07  Recap
class E13S07(BeatScene):
    SCENE_ID = 'E13S07'
    def construct(self):
        h = header("Recap: what you can now do")
        b = bullets(["explain why the monodromy is a product and why that suggests pieces",
                     "explain why pieces interact and how the dock makes each tile's product depend only on its interior",
                     "state the tiling theorem and prove it by the postage-stamp recursion: 100 = 21 + 21 + 21 + 37",
                     "explain why the whole interval [L, 2L) is needed; count parameters: ℓ ≥ 21 at k = 3",
                     "explain why certifying a tile is a one-tile nullity certification",
                     "state the three theorems, the three complete rows, and the attribution"], font_size=25, width=74).next_to(h, DOWN, buff=0.6)
        self.hold(19, ([FadeIn(h)], 0.8), ([FadeIn(b, lag_ratio=0.2)], 5))
        self.clear_all()
