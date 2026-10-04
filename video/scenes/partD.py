from lib import *
import numpy as np

def strip(n_cells, x0, y, w=0.42, h=0.55, dock=None, color=MUTED, interior_color=TEAL):
    """A row of n_cells boxes; dock = set of indices drawn in dock colour."""
    g = VGroup()
    for i in range(n_cells):
        col = color if (dock and i in dock) else interior_color
        r = Rectangle(width=w, height=h, color=col, fill_opacity=0.35 if (dock and i in dock) else 0.15, stroke_width=1.5).move_to([x0 + i*w, y, 0])
        g.add(r)
    return g

# ---------------------------------------------------------------- S25
class S25(BeatScene):
    SCENE_ID = 'S25'
    def construct(self):
        t = MathTex(r"T=T_{n-1}\cdots T_0=I\quad\text{is multiplicative along the cycle}", font_size=38).to_edge(UP, buff=0.6)
        # a ring of step boxes
        n = 16; R = 2.2; c = DOWN*0.6
        ring = VGroup(*[Square(side_length=0.45, color=TEAL, fill_opacity=0.2).move_to(c + R*np.array([np.cos(PI/2-2*PI*i/n), np.sin(PI/2-2*PI*i/n), 0])).rotate(-2*PI*i/n) for i in range(n)])
        tl = VGroup(*[MathTex(f"T_{{{i}}}", font_size=20).move_to(ring[i]) for i in range(n)])
        self.hold(1, ([Write(t)], 2.5), ([FadeIn(ring, lag_ratio=0.05), FadeIn(tl, lag_ratio=0.05)], 3))
        self.play(FadeOut(ring), FadeOut(tl), run_time=0.6)
        k = 3; L = 13
        x0 = -(L-1)/2*0.5
        row = strip(L, x0, 0.9, w=0.5, dock=set(range(k+1)) | set(range(L-k-1, L)))
        win = SurroundingRectangle(VGroup(*row[3:3+2*k+2]), color=YELLOW, buff=0.05)
        wl = Text("each step matrix sees a window of width ≈ 2k+2", font_size=24, color=YELLOW).next_to(win, UP, buff=0.2)
        dl = Text("docking pattern: fixed weights at k+1 positions, both ends", font_size=24, color=MUTED).next_to(row, DOWN, buff=0.3)
        il = Text("interior: free", font_size=24, color=TEAL).next_to(dl, DOWN, buff=0.15)
        self.hold(2, ([FadeIn(row)], 1.5), ([Create(win), FadeIn(wl)], 2), ([FadeOut(win), FadeOut(wl), FadeIn(dl), FadeIn(il)], 2.5))
        self.play(FadeOut(dl), FadeOut(il), run_time=0.5)
        # two tiles side by side sharing docking
        row2 = strip(L, x0 + L*0.5 - 0.5*0.0, 0.9, w=0.5, dock=set(range(k+1)) | set(range(L-k-1, L)))
        both = VGroup(row, row2)
        self.play(both.animate.scale(0.75).move_to(DOWN*0.2), run_time=1)
        win2 = SurroundingRectangle(VGroup(*row[L-4:L], *row2[0:4]), color=YELLOW, buff=0.05)
        lem = MathTex(r"\text{tile product depends only on its interior}\ \Rightarrow\ T=\prod_{\text{tiles}}T_{\text{tile}}", font_size=32, color=GREEN).next_to(both, DOWN, buff=0.6)
        self.hold(3, ([Create(win2)], 1.5), ([Write(lem)], 3))
        self.play(FadeOut(both), FadeOut(win2), FadeOut(lem), FadeOut(t), run_time=0.6)
        thm = VGroup(MathTex(r"\textbf{Tiling theorem.}\ \text{identity tiles of every length in }[L,2L)", font_size=34),
                     MathTex(r"\Rightarrow\ Z(P(n,k))=M(P(n,k))=2k+2\ \text{ for every }n\ge L", font_size=36, color=YELLOW),
                     MathTex(r"n<2L:\ \text{one tile};\qquad n\ge2L:\ \text{tile of length }L\ +\ \text{recurse on }n-L", font_size=28, color=MUTED)).arrange(DOWN, buff=0.45).shift(UP*1.2)
        # demonstrate: n = 55 with L=21 -> 21 + 34
        demo = VGroup(strip(21, -5.5, -1.3, w=0.2, dock=set(range(4))|set(range(17,21)), interior_color=TEAL), strip(34, -5.5+21*0.2, -1.3, w=0.2, dock=set(range(4))|set(range(30,34)), interior_color=PURPLE))
        dlab = MathTex(r"n=55=21+34", font_size=30).next_to(demo, DOWN, buff=0.3)
        self.hold(4, ([Write(thm[0])], 2.5), ([Write(thm[1])], 2.5), ([FadeIn(thm[2])], 2), ([FadeIn(demo), Write(dlab)], 2.5))
        self.play(FadeOut(demo), FadeOut(dlab), run_time=0.5)
        rem = VGroup(Text("an all-n statement = a finite list of finite problems", font_size=30, weight=BOLD, color=GREEN),
                     MathTex(r"\text{two coprime lengths }a,b\ \text{would miss every }n<(a-1)(b-1)\ \text{ (hundreds)}", font_size=28, color=MUTED)).arrange(DOWN, buff=0.4).shift(DOWN*1.5)
        self.hold(5, ([FadeIn(rem[0])], 2), ([Write(rem[1])], 3))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S26
class S26(BeatScene):
    SCENE_ID = 'S26'
    def construct(self):
        cnt = MathTex(r"5(\ell-2(k+1))\ \text{unknowns}\quad\text{vs}\quad(2k+2)^{2}=64\ \text{equations}\ (k=3)", font_size=34).to_edge(UP, buff=0.6)
        # residual bar chart by length
        lens = list(range(16, 24)); res = [0.83, 0.78, 0.82, 0.14, 0.37, 1e-14, 1e-14, 1e-14]
        ax = Axes(x_range=[15, 24, 1], y_range=[-15, 1, 5], x_length=7.5, y_length=3.5, axis_config={"include_tip": False, "color": MUTED},
                  x_axis_config={"include_numbers": True, "numbers_to_include": [16, 18, 20, 22]}, y_axis_config={"include_numbers": True}).shift(DOWN*1.0+LEFT*2.2)
        yl = MathTex(r"\log_{10}\text{ residual}", font_size=26).next_to(ax.y_axis, UP, buff=0.1); xl = MathTex(r"\ell", font_size=28).next_to(ax.x_axis, RIGHT)
        bars = VGroup()
        for l, r in zip(lens, res):
            top = ax.c2p(l, np.log10(r))[1]; bot = ax.c2p(l, -15)[1]
            bars.add(Rectangle(width=0.45, height=top-bot, color=GREEN if r < 1e-10 else RED, fill_opacity=0.6, stroke_width=1).move_to([ax.c2p(l, 0)[0], (top+bot)/2, 0]))
        lab = VGroup(Text("ℓ < 21: Newton stalls", font_size=24, color=RED), Text("ℓ ≥ 21: identity tiles found,\nevery length 21…43", font_size=24, color=GREEN, line_spacing=1.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(DOWN*0.8)
        self.hold(1, ([Write(cnt)], 3), ([Create(ax), FadeIn(yl), FadeIn(xl)], 1.5), ([FadeIn(bars, lag_ratio=0.1)], 2.5), ([FadeIn(lab)], 2))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.6)
        gift = VGroup(MathTex(r"T_{\text{tile}}=I\quad\text{(rational equation: nasty to certify)}", font_size=34),
                      MathTex(r"\text{monodromy of the one-tile cyclic matrix on }P(\ell,k)\ =\ T_{\text{tile}}", font_size=32),
                      MathTex(r"\Rightarrow\ T_{\text{tile}}=I\iff\operatorname{null}A_{\text{one tile}}=2k+2", font_size=40, color=YELLOW),
                      Text("the bilinear nullity system again; docking weights pinned at b = c = e = 1, a = d = 0", font_size=24, color=MUTED)).arrange(DOWN, buff=0.45).shift(UP*0.5)
        self.hold(2, ([Write(gift[0])], 2.5), ([Write(gift[1])], 3), ([Write(gift[2])], 2.5), ([FadeIn(gift[3])], 2))
        self.play(FadeOut(gift), run_time=0.5)
        ex = VGroup(Text("exact, not floating point", font_size=32, weight=BOLD, color=GREEN),
                    Text("every float64 is a dyadic rational ⇒ the box centre is exact", font_size=26),
                    Text("bilinear with integer coefficients ⇒ residual and Jacobian exactly rational", font_size=26),
                    Text("the preconditioner Y is arbitrary ⇒ round it to rationals for free", font_size=26),
                    MathTex(r"\text{speed: base-}2^{20}\text{ balanced digits, products exact in float64, BLAS does the work}", font_size=26, color=MUTED),
                    MathTex(r"\alpha<1\ \text{ is an exact integer comparison}", font_size=32, color=YELLOW)).arrange(DOWN, buff=0.3).shift(UP*0.2)
        self.hold(3, ([FadeIn(ex[0])], 1.5), ([FadeIn(ex[1])], 2), ([FadeIn(ex[2])], 2), ([FadeIn(ex[3])], 2), ([Write(ex[4])], 2.5), ([Write(ex[5])], 2))
        self.play(FadeOut(ex), run_time=0.5)
        tab = MathTex(r"\begin{array}{c|c|c|c} k & \text{tiles} & \text{lengths} & \alpha_{\max}\\ \hline 3 & 23 & 21\text{--}43 & 2.2\times10^{-10}\\ 4 & 33 & 29\text{--}61 & \le10^{-9}\\ 5 & 21 & 54\text{--}75\ (\text{two gaps}) & \le10^{-9}\end{array}", font_size=36).shift(UP*0.6)
        tot = Text("77 tile certifications + 17 per-n certifications, all in exact rational arithmetic", font_size=26, color=GREEN).next_to(tab, DOWN, buff=0.7)
        self.hold(4, ([Write(tab)], 4), ([FadeIn(tot)], 2.5))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S27
class S27(BeatScene):
    SCENE_ID = 'S27'
    def construct(self):
        th = VGroup(MathTex(r"Z(P(n,3))=M(P(n,3))=8\qquad n\ge17", font_size=42, color=YELLOW),
                    MathTex(r"Z(P(n,4))=M(P(n,4))=10\qquad n\ge29", font_size=42, color=YELLOW),
                    MathTex(r"Z(P(n,5))=M(P(n,5))=12\qquad n\ge162", font_size=42, color=YELLOW),
                    Text("no congruence conditions. primes included.", font_size=28, color=MUTED)).arrange(DOWN, buff=0.45)
        self.hold(1, ([Write(th[0])], 2.5), ([Write(th[1])], 2.5), ([Write(th[2])], 2.5), ([FadeIn(th[3])], 1.5))
        self.play(th.animate.scale(0.7).to_edge(UP, buff=0.4), run_time=0.8)
        srch = VGroup(Text("below the thresholds: exhaustive search over vertex subsets", font_size=28),
                      Text("rotation ⇒ a minimum forcing set contains a fixed representative: exact up to symmetry", font_size=24, color=MUTED),
                      MathTex(r"P(28,4):\ \text{every 9-set excluded, }\approx1.2\times10^{9}\text{ candidates}", font_size=28),
                      Text("solver reproduced every published value first, incl. Krishnan's corrected table", font_size=24, color=GREEN)).arrange(DOWN, buff=0.3).next_to(th, DOWN, buff=0.6)
        self.hold(2, ([FadeIn(srch, lag_ratio=0.3)], 5))
        self.play(FadeOut(srch), run_time=0.5)
        ax = Axes(x_range=[4, 30, 2], y_range=[3, 11, 1], x_length=10, y_length=4, axis_config={"include_tip": False, "color": MUTED},
                  x_axis_config={"include_numbers": True}, y_axis_config={"include_numbers": True}).shift(DOWN*1.1)
        xl = MathTex("n", font_size=28).next_to(ax.x_axis, RIGHT); yl = MathTex("Z", font_size=28).next_to(ax.y_axis, UP)
        z2 = {5:5,6:4,7:6,8:5,9:6,10:6,11:6}; z2.update({n:6 for n in range(12,30)})
        z3 = {7:6,8:6,9:6,10:8,11:7,12:7}; z3.update({n:8 for n in range(13,30)})
        z4 = {9:6,10:6,11:7,12:6,13:8,14:8,15:9,16:8,17:9}; z4.update({n:10 for n in range(18,30)})
        def series(d, col):
            pts = sorted(d.items())
            dots = VGroup(*[Dot(ax.c2p(n, z), radius=0.06, color=col) for n, z in pts])
            line = VMobject(color=col, stroke_width=2).set_points_as_corners([ax.c2p(n, z) for n, z in pts])
            return VGroup(line, dots)
        s2, s3, s4 = series(z2, BLUE), series(z3, ORANGE), series(z4, GREEN)
        leg = VGroup(MathTex("k=2", color=BLUE, font_size=28), MathTex("k=3", color=ORANGE, font_size=28), MathTex("k=4", color=GREEN, font_size=28)).arrange(RIGHT, buff=0.6).next_to(ax, UP, buff=0.1).shift(RIGHT*3)
        self.hold(3, ([Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(leg)], 1.5), ([Create(s2)], 2.5), ([Create(s3)], 2.5), ([Create(s4)], 2.5),
                  ([Indicate(s3[1][3], color=YELLOW, scale_factor=2), Indicate(s4[1][3], color=YELLOW, scale_factor=2)], 1.5))
        conj = VGroup(MathTex(r"Z(P(n,3))=8\ \ \forall n\ge13,\quad 13\ \text{optimal}", font_size=34, color=YELLOW),
                      Text("= Krishnan's Conjecture 5, proved. Threshold: 13.", font_size=28),
                      Text("k = 4: first exact determination at all;\nfirst infinite family at any k ≥ 4", font_size=24, color=MUTED, line_spacing=1.1)).arrange(DOWN, buff=0.35).next_to(th, DOWN, buff=1.0)
        self.hold(4, ([FadeOut(s2), FadeOut(s4), FadeOut(leg)], 0.8), ([FadeOut(VGroup(ax, xl, yl, s3))], 0.6), ([Write(conj[0])], 2.5), ([FadeIn(conj[1])], 2), ([FadeIn(conj[2])], 2))
        self.play(FadeOut(conj), run_time=0.6)
        attr = VGroup(Text("Attribution, exactly:", font_size=30, weight=BOLD),
                      Text("the correction to the published theorem is Krishnan's", font_size=28),
                      Text("the lower bound for all large n,\nand so the proof of his conjecture, is this project's", font_size=28, color=YELLOW, line_spacing=1.1)).arrange(DOWN, buff=0.4).next_to(th, DOWN, buff=1.2)
        self.hold(5, ([FadeIn(attr, lag_ratio=0.4)], 4))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S28
class S28(BeatScene):
    SCENE_ID = 'S28'
    def construct(self):
        t = Text("A conjecture, and its refutation", font_size=40, weight=BOLD).to_edge(UP, buff=0.6)
        self.hold(1, ([Write(t)], 2.5))
        gen = VGroup(MathTex(r"\text{cyclic cover of any base }B\text{ with voltages in }\mathbb Z_n", font_size=32),
                     MathTex(r"\text{equivariant }A:\quad \operatorname{null}A\ \le\ D=\text{degree span of }\det M(\zeta)", font_size=34, color=YELLOW),
                     MathTex(r"P(n,k):\ D=2k+2.\quad\text{read off the base, independent of }n", font_size=30, color=MUTED)).arrange(DOWN, buff=0.4).next_to(t, DOWN, buff=0.6)
        self.hold(2, ([Write(gen[0])], 2.5), ([Write(gen[1])], 3), ([FadeIn(gen[2])], 2))
        self.play(FadeOut(gen), run_time=0.5)
        # K4 with voltages
        c = LEFT*3.5 + DOWN*0.8
        P = [c+UP*1.6, c+LEFT*1.6+DOWN*0.8, c+RIGHT*1.6+DOWN*0.8, c+DOWN*0.3]
        edges = [((0,1),0),((0,2),1),((0,3),0),((1,2),2),((1,3),0),((2,3),1)]
        E = VGroup(); labs = VGroup()
        for (a,b),v in edges:
            col = RED if v == 0 else MUTED
            E.add(Line(P[a], P[b], color=col, stroke_width=4 if v == 0 else 2.5))
            labs.add(MathTex(str(v), font_size=26, color=col).move_to((P[a]+P[b])/2 + 0.25*UP))
        V = VGroup(*[Dot(p, radius=0.1, color=INK) for p in P])
        vl = VGroup(*[MathTex(str(i), font_size=24).next_to(P[i], DOWN if i == 3 else UP, buff=0.12) for i in range(4)])
        base = VGroup(E, V, labs, vl)
        facts = VGroup(MathTex(r"B=K_4,\quad B^{n}:\ \text{cubic, }4n\text{ vertices}", font_size=30),
                       MathTex(r"D=6\ \text{ for every }n;\ \text{attained by an integer matrix}", font_size=28),
                       MathTex(r"Z(B^{n})=n+2\quad(n=4,\dots,8,\ \text{CP-SAT, optimality proved})", font_size=28, color=GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5).shift(DOWN*0.6)
        self.hold(3, ([Create(E), FadeIn(V), FadeIn(labs), FadeIn(vl)], 2.5), ([Write(facts[0])], 2), ([Write(facts[1])], 2), ([Write(facts[2])], 2.5))
        self.play(FadeOut(facts), run_time=0.4)
        claim = VGroup(MathTex(r"\text{claimed: } M(B^{n})=6,\\ Z-M\to\infty\ \text{on cubic graphs}", font_size=30, color=RED),
                       Text("on the poster, in the interview script,\nas the strongest result", font_size=24, color=MUTED, line_spacing=1.1)).arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.5).shift(DOWN*0.6)
        self.hold(4, ([Write(claim[0])], 3), ([FadeIn(claim[1])], 2))
        self.play(FadeOut(claim), run_time=0.4)
        tri = Polygon(P[0], P[1], P[3], color=YELLOW, fill_opacity=0.25, stroke_width=0)
        proof = VGroup(Text("voltage-0 edges form a triangle", font_size=26, color=YELLOW),
                       MathTex(r"\text{each fibre carries a triangle; put }uu^{\!\top}\text{ on it}\\ \text{(legal: off-diagonal}\ne0\text{, diagonal free)}", font_size=24),
                       MathTex(r"\operatorname{rank}A\le 2n+n=3n\ \Rightarrow\ \operatorname{null}A\ge n", font_size=32, color=GREEN),
                       MathTex(r"\text{exact over }\mathbb Q:\ \operatorname{null}=n,\ n=4,\dots,10", font_size=26, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(DOWN*0.6)
        self.hold(5, ([FadeIn(tri)], 1.5), ([FadeIn(proof[0])], 1.5), ([Write(proof[1])], 3), ([Write(proof[2])], 2.5), ([FadeIn(proof[3])], 2))
        self.play(FadeOut(proof), FadeOut(base), FadeOut(tri), run_time=0.5)
        after = VGroup(MathTex(r"M(B^{n})\ge n,\quad Z-M\le2.\quad\text{The regular-base ceiling is false: }K_4\text{ is cubic.}", font_size=30),
                       MathTex(r"\det M(\zeta)\equiv0:\ \text{a hypothesis the cover theorem needed and had not stated}", font_size=28, color=RED),
                       Text("both adversarial searches missed it:\nthe matrix lives where three fibre blocks are singular", font_size=24, color=MUTED, line_spacing=1.1),
                       Text("found by reading the voltages, not by searching", font_size=28, color=YELLOW),
                       MathTex(r"\text{what survives: the leading-coefficient criterion (conjecture, proved on 3 base types)}", font_size=26, color=MUTED)).arrange(DOWN, buff=0.35).next_to(t, DOWN, buff=0.6)
        self.hold(6, ([Write(after[0])], 3), ([Write(after[1])], 3), ([FadeIn(after[2])], 2.5), ([FadeIn(after[3])], 2), ([Write(after[4])], 3))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S29
class S29(BeatScene):
    SCENE_ID = 'S29'
    def construct(self):
        t = Text("Status of the claims", font_size=40, weight=BOLD).to_edge(UP, buff=0.5)
        self.hold(1, ([Write(t)], 2))
        def block(head, items, col):
            h = Text(head, font_size=28, weight=BOLD, color=col)
            its = VGroup(*[Text("• " + x, font_size=22) for x in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            return VGroup(h, its).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        b1 = block("Proved", ["reduction + ceiling; symbol classification; realisability & antipodal obstruction",
                              "congruence-class theorem; two-vertex-base reductions; K4 refutation",
                              "Part I: criterion, corner form, uniform bound, Dirichlet bound, parity law"], GREEN).next_to(t, DOWN, buff=0.5).to_edge(LEFT, buff=0.7)
        self.hold(2, ([FadeIn(b1, lag_ratio=0.2)], 4))
        b2 = block("Proved by exact certificate", ["k=2: n ≥ 9, n ≠ 10   •   k=3: 10 | n   •   k=4: 60, 70, 90 | n",
                                                    "k=5: 24 | n   •   k=7: 120 | n"], TEAL).next_to(b1, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
        self.hold(3, ([FadeIn(b2, lag_ratio=0.2)], 3.5))
        b3 = block("Proved by exact certification (Krawczyk, rational arithmetic)", ["k=3: n ≥ 17   •   k=4: n ≥ 29   •   k=5: n ≥ 162"], YELLOW).next_to(b2, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
        b4 = block("Numerical only, and said so", ["k=6 at seven n; P(96,8)"], ORANGE).next_to(b3, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
        self.hold(4, ([FadeIn(b3, lag_ratio=0.2)], 3), ([FadeIn(b4, lag_ratio=0.2)], 2.5))
        self.play(FadeOut(b1), FadeOut(b2), FadeOut(b3), FadeOut(b4), run_time=0.5)
        b5 = block("Open", ["tiles for k ≥ 6 (count says ℓ ≥ 54; none found)", "M(P(24,4)) = 10 ?", "M(K4 family): between n and n+2", "the leading-coefficient criterion"], RED).next_to(t, DOWN, buff=0.5).to_edge(LEFT, buff=0.7)
        b6 = block("Refuted (ours)", ["8 earlier claims, listed; one search withdrawn as unreliable"], MUTED).next_to(b5, DOWN, buff=0.5).to_edge(LEFT, buff=0.7)
        self.hold(5, ([FadeIn(b5, lag_ratio=0.2)], 4), ([FadeIn(b6, lag_ratio=0.2)], 2.5))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S30
class S30(BeatScene):
    SCENE_ID = 'S30'
    def construct(self):
        t = Text("Verification as method", font_size=40, weight=BOLD).to_edge(UP, buff=0.5)
        a = VGroup(Text("one script re-derives every computational claim from the certificates on disk", font_size=26),
                   MathTex(r"141\ \text{checks}", font_size=40, color=GREEN),
                   Text("every number in the paper is generated, never typed (the census drifted three times before that rule)", font_size=22, color=MUTED)).arrange(DOWN, buff=0.35).next_to(t, DOWN, buff=0.6)
        self.hold(1, ([Write(t)], 1.5), ([FadeIn(a, lag_ratio=0.3)], 4))
        self.play(FadeOut(a), run_time=0.5)
        b = VGroup(Text("every search runs beside a control", font_size=30, weight=BOLD),
                   Text("exact Ramanujan classifier ‖ float64 classifier → the dictionary bug", font_size=26),
                   Text("nullity searches ‖ the ceiling theorem → two impossible answers caught", font_size=26),
                   Text("forcing solver ‖ brute force + two exact solver formulations", font_size=26)).arrange(DOWN, buff=0.35).next_to(t, DOWN, buff=0.6)
        self.hold(2, ([FadeIn(b, lag_ratio=0.3)], 5))
        self.play(FadeOut(b), run_time=0.5)
        c = VGroup(Text("the dated log of wrong turns", font_size=30, weight=BOLD),
                   Text("invalid Taylor derivation • degree 2k that is 2k+2 • misattributed citation", font_size=24, color=MUTED),
                   Text("a separation guard that underflowed to 0.0 • pivoting that left 28 equations unproved\nthe K4 conjecture", font_size=24, color=MUTED, line_spacing=1.1),
                   VGroup(Text("A passing test is not a proof.", font_size=28, color=YELLOW), Text("A converged optimum is not a witness.", font_size=28, color=YELLOW),
                          Text("A failed search measures effort, not impossibility.", font_size=28, color=YELLOW)).arrange(DOWN, buff=0.15)).arrange(DOWN, buff=0.4).next_to(t, DOWN, buff=0.6)
        self.hold(3, ([FadeIn(c[0])], 1.5), ([FadeIn(c[1]), FadeIn(c[2])], 3), ([FadeIn(c[3], lag_ratio=0.4)], 4))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.8)

# ---------------------------------------------------------------- S31
class S31(BeatScene):
    SCENE_ID = 'S31'
    def construct(self):
        n = 16; R = 2.0; c = LEFT*3.5 + DOWN*0.3
        circ = Circle(radius=R, color=MUTED).move_to(c)
        pts = VGroup(*[Dot(c + R*np.array([np.cos(2*PI*m/n), np.sin(2*PI*m/n), 0]), radius=0.07, color=INK) for m in range(n)])
        gl = MathTex(r"\{\zeta_n^{\,m}\}", font_size=36).next_to(circ, DOWN, buff=0.3)
        p1 = VGroup(Text("Part I: matrix fixed", font_size=30, weight=BOLD, color=YELLOW),
                    Text("a fixed curve sampled on the grid", font_size=26), Text("must avoid a forbidden band", font_size=26),
                    Text("fixed polynomial, no sign change", font_size=26, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.6).shift(UP*1.6)
        p2 = VGroup(Text("Part II: matrix ranging", font_size=30, weight=BOLD, color=TEAL),
                    Text("how many roots of a chosen polynomial", font_size=26), Text("can be forced onto the same grid", font_size=26),
                    Text("then: monodromy = I for every period", font_size=26, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.6).shift(DOWN*1.4)
        self.hold(1, ([Create(circ), FadeIn(pts), Write(gl)], 2), ([FadeIn(p1, lag_ratio=0.3)], 4), ([FadeIn(p2, lag_ratio=0.3)], 4))
        mid = Text("Same object. Opposite direction. Same exact arithmetic.", font_size=30, weight=BOLD).to_edge(DOWN, buff=0.4)
        self.hold(2, ([Write(mid)], 3))
        self.play(*[FadeOut(mm) for mm in self.mobjects], run_time=0.6)
        found = VGroup(MathTex(r"460\ \text{Ramanujan }P(n,k);\ \text{none past }k=45;\ Q\text{ without }k;\ n\le230", font_size=32),
                       MathTex(r"Z=M=2k+2:\ n\ge17\ (k=3),\ n\ge29\ (k=4);\ Z\text{ determined }\forall n,\ k=2,3,4", font_size=32),
                       MathTex(r"\text{Krishnan's Conjecture 5 proved; threshold }13", font_size=32),
                       Text("a ceiling theorem: the matrix method solves it or cannot touch it", font_size=28),
                       Text("a refuted conjecture, with the one-line reason", font_size=28, color=RED)).arrange(DOWN, buff=0.4).shift(UP*0.3)
        self.hold(3, ([Write(found[0])], 3), ([Write(found[1])], 3.5), ([Write(found[2])], 2.5), ([FadeIn(found[3])], 2), ([FadeIn(found[4])], 2))
        self.play(FadeOut(found), run_time=0.6)
        nxt = VGroup(Text("Next", font_size=36, weight=BOLD),
                     Text("close M(P(24,4))  •  tiles at k = 5, 6  •  prove or refute the leading-coefficient criterion", font_size=26),
                     Text("1 October 2026", font_size=28, color=MUTED)).arrange(DOWN, buff=0.5)
        self.hold(4, ([FadeIn(nxt, lag_ratio=0.4)], 4))
        self.play(FadeOut(nxt), run_time=1.5)
