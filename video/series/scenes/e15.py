from lib import *

# ---------------------------------------------------------------- E15S01  One grid, two directions
class E15S01(BeatScene):
    SCENE_ID = 'E15S01'
    def construct(self):
        t = title_card("Episode 15", "What is proved, what is open, and how the numbers are trusted")
        n = 16; R = 1.6; c = LEFT*4.4+DOWN*0.5
        circ = Circle(radius=R, color=MUTED).move_to(c)
        pts = VGroup(*[Dot(c + R*np.array([np.cos(2*PI*m/n), np.sin(2*PI*m/n), 0]), radius=0.07, color=INK) for m in range(n)])
        gl = MathTex(r"\{\zeta_n^{\,m}\}", font_size=34).next_to(circ, DOWN, buff=0.3)
        p1 = VGroup(Text("Part One: matrix fixed", font_size=28, weight=BOLD, color=YELLOW), wrap("two fixed curves sampled on the grid", 44, 24),
                    wrap("must avoid a forbidden band: a fixed polynomial stays ≥ 0", 44, 24, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.5).shift(UP*1.4)
        p2 = VGroup(Text("Part Two: matrix ranging", font_size=28, weight=BOLD, color=TEAL), wrap("how many roots of a chosen polynomial land on the same grid", 44, 24),
                    wrap("then, symmetry broken: monodromy = I for every n", 44, 24, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.5).shift(DOWN*1.2)
        self.hold(1, ([FadeIn(t)], 1.5), ([FadeOut(t)], 0.5), ([FadeIn(header("One grid, two directions"))], 0.8),
                  ([Create(circ), FadeIn(pts), Write(gl)], 2), ([], 2), ([FadeIn(p1, lag_ratio=0.3)], 3), ([], 6), ([FadeIn(p2, lag_ratio=0.3)], 3))
        mid = wrap("Same object. Opposite direction. Same exact arithmetic: never trust a float where a float cannot decide.", 60, 24, YELLOW).to_edge(DOWN, buff=0.3)
        self.hold(2, ([Write(mid)], 3))
        self.clear_all()

# ---------------------------------------------------------------- E15S02  Four standards
class E15S02(BeatScene):
    SCENE_ID = 'E15S02'
    def construct(self):
        h = header("Four standards of evidence")
        rows = VGroup(VGroup(Text("1  proved", font_size=26, weight=BOLD, color=GREEN), wrap("a proof in the text, checkable line by line", 60, 22)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
                      VGroup(Text("2  exact certificate", font_size=26, weight=BOLD, color=TEAL), wrap("an explicit matrix / algebraic number, computed in whole-number arithmetic", 60, 22)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
                      VGroup(Text("3  exact certification", font_size=26, weight=BOLD, color=YELLOW), wrap("Krawczyk in exact fractions: a true solution exists in a box", 60, 22)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
                      VGroup(Text("4  proved finite", font_size=26, weight=BOLD, color=ORANGE), wrap("exhaustive search, validated against independent methods", 60, 22)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(h, DOWN, buff=0.3).to_edge(LEFT, buff=0.8)
        self.hold(3, ([FadeIn(h)], 0.8), ([FadeIn(rows, lag_ratio=0.3)], 6))
        more = VGroup(VGroup(Text("numerical only", font_size=26, weight=BOLD, color=MUTED), wrap("floating point never made exact: observations, never theorems", 60, 22)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
                      VGroup(Text("open", font_size=26, weight=BOLD, color=RED), Text("— not known", font_size=22)).arrange(RIGHT, buff=0.3),
                      wrap("the honesty is in the labels, and in the fact that they moved when the evidence changed", 60, 22, YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(rows, DOWN, buff=0.25).align_to(rows, LEFT)
        self.hold(4, ([FadeIn(more, lag_ratio=0.3)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E15S03  Results by standard
class E15S03(BeatScene):
    SCENE_ID = 'E15S03'
    def construct(self):
        h = header("The results, by standard")
        def block(head, items, col, width=74):
            return VGroup(Text(head, font_size=26, weight=BOLD, color=col), bullets(items, font_size=21, width=width, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        b1 = block("Proved", ["reduction + ceiling; symbol classification; realisability & antipodal obstruction; one divisibility class per symbol",
                              "tiling theorem; two-vertex-base reductions; K4 refutation",
                              "Part One: polynomial criterion, corner form, uniform bound, Dirichlet bound, parity law"], GREEN).next_to(h, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        self.hold(5, ([FadeIn(h)], 0.8), ([FadeIn(b1, lag_ratio=0.2)], 5))
        b2 = block("Proved by exact certificate", ["k=2: n ≥ 9 except 10 (rotation-invariant), n=10 by an integer matrix; k=3: 10 | n; k=4: 60, 70, 90 | n",
                                                    "k=5: 24 | n; k=7: 120 | n; the complete Ramanujan classification (460 pairs)"], TEAL).next_to(b1, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        self.hold(6, ([FadeIn(b2, lag_ratio=0.2)], 4))
        b3 = block("Proved by exact certification / proved finite", ["Z = M = 8 (k=3, n ≥ 17); 10 (k=4, n ≥ 29); 12 (k=5, n ≥ 162)",
                                                                       "every tabulated small value, including the complete rows for k = 2, 3, 4"], YELLOW).next_to(b2, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        self.hold(7, ([FadeIn(b3, lag_ratio=0.2)], 4))
        b4 = block("Numerical only, and said so", ["k=6 at seven values of n, one value at k=8: Newton solves never certified; observations"], ORANGE).next_to(b3, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        self.hold(8, ([FadeIn(b4, lag_ratio=0.2)], 3))
        self.play(FadeOut(b1), FadeOut(b2), FadeOut(b3), FadeOut(b4), run_time=0.5)
        b5 = block("Open", ["identity tiles for k ≥ 6 (parameter count says length 54; none found)",
                            "M(P(24,4)) = 10? Z is 10 there; no nullity-10 matrix found; no rotation-invariant matrix can reach it (proved late)",
                            "the exact maximum nullity of the K4 family: between n and n+2",
                            "the leading-coefficient conjecture"], RED).next_to(h, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        self.hold(9, ([FadeIn(b5, lag_ratio=0.2)], 5))
        b6 = block("Refuted (ours)", ["eight earlier claims, listed with dates, incl. the cubic gap conjecture and the regular-base ceiling",
                                     "one search withdrawn as unreliable: it collapsed onto degenerate configurations and reported plateaus that were not there"], MUTED).next_to(b5, DOWN, buff=0.5).to_edge(LEFT, buff=0.6)
        self.hold(10, ([FadeIn(b6, lag_ratio=0.2)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E15S04  Verification as method
class E15S04(BeatScene):
    SCENE_ID = 'E15S04'
    def construct(self):
        h = header("Verification as method")
        a = VGroup(Text("one script re-derives every computational claim from the certificates on disk", font_size=26),
                   MathTex(r"141\ \text{checks},\ \approx7\ \text{minutes}", font_size=38, color=GREEN),
                   wrap("every number in the paper is generated and read in automatically, never typed (the census drifted three times before that rule)", 80, 22, MUTED)).arrange(DOWN, buff=0.3).next_to(h, DOWN, buff=0.6)
        self.hold(11, ([FadeIn(h)], 0.8), ([FadeIn(a, lag_ratio=0.3)], 4))
        self.play(FadeOut(a), run_time=0.4)
        b = VGroup(Text("every search runs beside a control", font_size=30, weight=BOLD),
                   Text("exact Ramanujan classifier ‖ float64 classifier  →  the k = 1 bug", font_size=25),
                   Text("nullity searches ‖ the ceiling theorem  →  two impossible answers caught", font_size=25),
                   Text("forcing solver ‖ brute force + two independent formulations", font_size=25)).arrange(DOWN, buff=0.35).next_to(h, DOWN, buff=0.6)
        self.hold(12, ([FadeIn(b, lag_ratio=0.3)], 5))
        self.play(FadeOut(b), run_time=0.4)
        c = VGroup(Text("the dated log of wrong turns", font_size=30, weight=BOLD),
                   wrap("invalid Taylor derivation • a degree claimed as 2k that is 2k+2 • a misattributed citation • a separation guard that underflowed to 0 • pivoting that left 28 equations unproved • the cubic gap conjecture", 80, 22, MUTED),
                   VGroup(Text("A passing test is not a proof.", font_size=27, color=YELLOW), Text("A converged optimum is not a witness.", font_size=27, color=YELLOW),
                          Text("A failed search measures effort, not impossibility.", font_size=27, color=YELLOW)).arrange(DOWN, buff=0.12),
                   Text("each sentence was earned by a specific mistake", font_size=22, color=MUTED)).arrange(DOWN, buff=0.4).next_to(h, DOWN, buff=0.5)
        self.hold(13, ([FadeIn(c[0])], 1.5), ([FadeIn(c[1])], 3.5), ([FadeIn(c[2], lag_ratio=0.4)], 4), ([FadeIn(c[3])], 1.5))
        self.clear_all()

# ---------------------------------------------------------------- E15S05  In one breath
class E15S05(BeatScene):
    SCENE_ID = 'E15S05'
    def construct(self):
        h = header("What the project found, in one breath")
        found = VGroup(MathTex(r"460\ \text{Ramanujan }P(n,k);\ \text{none past }k=45;\ Q\text{ without }k;\ n\le230", font_size=30),
                       MathTex(r"Z=M=2k+2:\ n\ge17\ (k=3),\ n\ge29\ (k=4),\ n\ge162\ (k=5);\ Z\text{ determined }\forall n\text{ for }k=2,3,4", font_size=28),
                       MathTex(r"\text{Krishnan's Conjecture 5 proved, threshold }13\text{ (optimal)}", font_size=30),
                       Text("a ceiling theorem: the matrix method solves it completely or cannot touch it", font_size=26),
                       Text("a refuted conjecture, with the one-line reason why", font_size=26, color=RED)).arrange(DOWN, buff=0.35).next_to(h, DOWN, buff=0.6)
        self.hold(14, ([Write(found[0])], 3), ([Write(found[1])], 3.5), ([Write(found[2])], 2.5), ([FadeIn(found[3])], 2), ([FadeIn(found[4])], 2))
        self.play(FadeOut(found), run_time=0.5)
        nxt = VGroup(Text("Next", font_size=36, weight=BOLD),
                     bullets(["close M(P(24,4))", "identity tiles at k = 6, or a proof none exist below some length", "prove or refute the leading-coefficient criterion"], font_size=26, width=60),
                     Text("2 October 2026", font_size=26, color=MUTED)).arrange(DOWN, buff=0.5).next_to(h, DOWN, buff=0.8)
        self.hold(15, ([FadeIn(nxt, lag_ratio=0.4)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E15S06  How to use this series
class E15S06(BeatScene):
    SCENE_ID = 'E15S06'
    def construct(self):
        h = header("How to use this series")
        a = card("if you are the author: a drill", "Redo every worked example by hand: the Petersen blocks, D₂ at n = 5, Q at n = 24, the kernel of the 3-vertex path, the n = 12 certificate, Krawczyk on √2, the rank of the K4 matrix.\nIf you can do each on a whiteboard without notes, you can explain the project to anyone, including a judge who asks the one question you did not prepare for.", color=YELLOW, width=80, font_size=21, title_size=26).next_to(h, DOWN, buff=0.5)
        self.hold(16, ([FadeIn(h)], 0.8), ([FadeIn(a)], 4))
        b = card("if you are not: a map", "The paper is the territory. Every theorem named here is stated and proved there, with its status label. Where this series says a thing is true, the paper says how it is known. That difference is the point.", color=BLUE, width=80, font_size=21, title_size=26).next_to(a, DOWN, buff=0.3)
        self.hold(17, ([FadeIn(b)], 4))
        self.play(FadeOut(a), FadeOut(b), FadeOut(h), run_time=1.5)
