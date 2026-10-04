from lib import *

K4_VOLT = [((0,1),0),((0,2),1),((0,3),0),((1,2),2),((1,3),0),((2,3),1)]

def k4_base(center, scale=1.0):
    P = [center+UP*1.5*scale, center+LEFT*1.5*scale+DOWN*0.8*scale, center+RIGHT*1.5*scale+DOWN*0.8*scale, center+DOWN*0.3*scale]
    E = VGroup(); labs = VGroup()
    for (a, b), v in K4_VOLT:
        col = RED if v == 0 else MUTED
        E.add(Line(P[a], P[b], color=col, stroke_width=4 if v == 0 else 2.5))
        labs.add(MathTex(str(v), font_size=24, color=col).move_to((P[a]+P[b])/2 + 0.22*UP))
    V = VGroup(*[Dot(p, radius=0.1, color=INK) for p in P])
    vl = VGroup(*[MathTex(str(i), font_size=22).next_to(P[i], DOWN if i == 3 else UP, buff=0.12) for i in range(4)])
    return VGroup(E, V, labs, vl), P

def k4_cover(n, center, dx=1.3):
    """4n vertices drawn in n columns (fibre index i): the triangle {0_i,1_i,3_i} on top, 2_i below."""
    pos = {}
    for i in range(n):
        x = center[0] + (i - (n-1)/2)*dx
        pos[(0, i)] = np.array([x, center[1]+1.0, 0]); pos[(1, i)] = np.array([x-0.35, center[1]+0.3, 0])
        pos[(3, i)] = np.array([x+0.35, center[1]+0.3, 0]); pos[(2, i)] = np.array([x, center[1]-0.9, 0])
    E = VGroup()
    for (a, b), v in K4_VOLT:
        for i in range(n):
            p, q = pos[(a, i)], pos[(b, (i+v) % n)]
            if v and (i+v) >= n:
                E.add(ArcBetweenPoints(p, q, angle=-PI/2.5, color=MUTED, stroke_width=1.5))
            else:
                E.add(Line(p, q, color=RED if v == 0 else MUTED, stroke_width=3 if v == 0 else 1.5))
    V = VGroup(*[Dot(p, radius=0.06, color=INK) for p in pos.values()])
    labs = VGroup(*[MathTex(f"{b}_{{{i}}}", font_size=14, color=MUTED).next_to(pos[(b, i)], UP if b == 0 else (LEFT if b == 1 else (RIGHT if b == 3 else DOWN)), buff=0.05) for (b, i) in pos])
    return VGroup(E, V, labs), pos

# ---------------------------------------------------------------- E14S01  Voltage graphs
class E14S01(BeatScene):
    SCENE_ID = 'E14S01'
    def construct(self):
        t = title_card("Episode 14", "Covers, the K4 family, and a refutation")
        self.hold(1, ([FadeIn(t)], 1.5), ([FadeOut(t)], 0.5), ([FadeIn(header("Building big graphs from small ones: voltage graphs"))], 0.8))
        u = Dot(LEFT*1.2, radius=0.12, color=BLUE); v = Dot(RIGHT*1.2, radius=0.12, color=ORANGE)
        lu = Arc(radius=0.5, start_angle=-PI/2+0.5, angle=2*PI-1.0, color=BLUE).move_to(LEFT*1.2+UP*0.6)
        lv = Arc(radius=0.5, start_angle=-PI/2+0.5, angle=2*PI-1.0, color=ORANGE).move_to(RIGHT*1.2+UP*0.6)
        e = Line(LEFT*1.2, RIGHT*1.2, color=MUTED)
        vol = VGroup(MathTex("1", font_size=28, color=BLUE).next_to(lu, UP, buff=0.1), MathTex("k", font_size=28, color=ORANGE).next_to(lv, UP, buff=0.1), MathTex("0", font_size=28, color=MUTED).next_to(e, DOWN, buff=0.1))
        base = VGroup(lu, lv, e, u, v, vol).to_edge(LEFT, buff=1.5).shift(UP*0.8)
        d1 = defn("voltage graph (base)", "A small graph with a whole number (voltage) on each edge. Here: vertices u, v; a loop at u with voltage 1, a loop at v with voltage k, an edge u–v with voltage 0.", width=44, font_size=22).to_edge(RIGHT, buff=0.4).shift(UP*1.2)
        self.play(Create(base), run_time=2)
        self.play(FadeIn(d1), run_time=1.5)
        rule = card("unfolding for a chosen n", [MathTex(r"\text{make }n\text{ copies }x_0,\dots,x_{n-1}\ \text{of each base vertex }x", font_size=24),
                                                MathTex(r"\text{base edge }x\to y\text{ with voltage }g:\ \text{edges }x_i\to y_{i+g}\ (\text{mod }n)", font_size=24),
                                                MathTex(r"\text{loop}(u,1):\ u_iu_{i+1};\quad \text{loop}(v,k):\ v_iv_{i+k};\quad (u,v,0):\ u_iv_i", font_size=24, color=GREEN),
                                                MathTex(r"\Rightarrow\ P(n,k)", font_size=32, color=YELLOW)], color=GREEN, width=50).to_edge(RIGHT, buff=0.4).shift(DOWN*1.3)
        g, d = petersen(7, 2, R_out=1.25, R_in=0.6, center=LEFT*4.3+DOWN*1.5, dot_r=0.06)
        self.hold(2, ([FadeIn(rule)], 4), ([FadeIn(g)], 2))
        self.play(FadeOut(rule), FadeOut(d1), run_time=0.4)
        d2 = defn("cyclic cover, fibre", "The unfolded graph is the cyclic (n-fold) cover of the base; it always has the rotation i ↦ i+1. The n copies of a base vertex are its fibre.\nOne vertex with a loop of voltage 1 ⇒ the n-cycle. Two vertices with three parallel edges (0, 1, 2) ⇒ a bipartite cubic graph.", width=46, font_size=22).to_edge(RIGHT, buff=0.4).shift(UP*0.3)
        self.hold(3, ([FadeIn(d2)], 4))
        gen = wrap("the whole machinery (blocks, monodromy, ceiling) works for any base: the symbol M(ζ) is the base's adjacency with ζ^g on each edge", 95, 20, MUTED).to_edge(DOWN, buff=0.2)
        self.hold(4, ([FadeIn(gen)], 3))
        self.clear_all()

# ---------------------------------------------------------------- E14S02  General ceiling, the claim
class E14S02(BeatScene):
    SCENE_ID = 'E14S02'
    def construct(self):
        h = header("The general ceiling, and the regular-base claim")
        gen = VGroup(MathTex(r"\text{rotation-invariant }A\text{ on a cover of base }B:\quad \operatorname{null}A\le\text{degree span of }\det M(\zeta)", font_size=28, color=YELLOW),
                     MathTex(r"P(n,k):\ \text{span}=2k+2.\ \text{Read off the base and voltages, independent of }n.", font_size=26, color=MUTED)).arrange(DOWN, buff=0.3).next_to(h, DOWN, buff=0.5)
        self.hold(5, ([FadeIn(h), Write(gen[0])], 3.5), ([FadeIn(gen[1])], 2.5))
        story = wrap("The project went looking for a base where this ceiling is small but Z grows with n: a family with Z ≫ M, answering a survey question about cubic graphs. It found a candidate.", 70, 24).next_to(gen, DOWN, buff=0.4)
        self.hold(6, ([FadeIn(story)], 3.5))
        self.play(FadeOut(gen), FadeOut(story), run_time=0.4)
        base, P = k4_base(LEFT*3.8+DOWN*1.2)
        facts = VGroup(MathTex(r"B=K_4;\ \text{voltages }0\text{ on }01,03,13;", font_size=26), MathTex(r"1\text{ on }02,23;\ 2\text{ on }12", font_size=26),
                       MathTex(r"\text{cover: cubic, connected, }4n\text{ vertices}", font_size=26),
                       MathTex(r"\text{degree span}=6\text{ for every }n;", font_size=26), MathTex(r"\text{an integer matrix attains nullity }6", font_size=26),
                       MathTex(r"Z=n+2\ \text{for }n=4,\dots,8\ \text{(exact search)}", font_size=28, color=GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(DOWN*0.6)
        self.hold(7, ([Create(base)], 2.5), ([Write(facts[0]), Write(facts[1])], 2.5), ([FadeIn(facts[2]), FadeIn(facts[3]), FadeIn(facts[4])], 3), ([Write(facts[5])], 2))
        self.play(FadeOut(facts), run_time=0.4)
        claim = card("the cubic gap conjecture (ours)", [MathTex(r"M(B^n)=6\ \text{for all }n,\quad Z-M\to\infty\ \text{on cubic graphs}", font_size=24, color=RED),
                                                        wrap("on the poster, in the interview script, as the strongest result in the project", 44, 22, MUTED)], color=RED, width=44, title_size=26).to_edge(RIGHT, buff=0.4).shift(DOWN*0.6)
        self.hold(8, ([FadeIn(claim)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E14S03  Rank
class E14S03(BeatScene):
    SCENE_ID = 'E14S03'
    def construct(self):
        h = header("Rank, in one example")
        m = MathTex(r"u=\begin{pmatrix}1\\2\\3\end{pmatrix},\qquad uu^{\!\top}=\begin{pmatrix}1&2&3\\2&4&6\\3&6&9\end{pmatrix}", font_size=32).next_to(h, DOWN, buff=0.35)
        obs = wrap("every row is a multiple of the first; every column a multiple of the first: one independent row", 80, 22, MUTED).next_to(m, DOWN, buff=0.25)
        self.hold(9, ([FadeIn(h), Write(m)], 3), ([FadeIn(obs)], 2.5))
        d1 = defn("rank", [Text("number of independent rows (= independent columns)", font_size=22),
                           MathTex(r"\text{rank}+\text{nullity}=N\quad(\text{directions kept}+\text{directions killed}=\text{everything})", font_size=26, color=YELLOW),
                           MathTex(r"uu^{\!\top}:\ \text{rank }1\ \Rightarrow\ \text{nullity }2;\quad uu^{\!\top}\!\begin{pmatrix}2\\-1\\0\end{pmatrix}=0,\ uu^{\!\top}\!\begin{pmatrix}3\\0\\-1\end{pmatrix}=0\ \checkmark", font_size=24, color=GREEN)], width=70, title_size=26).next_to(obs, DOWN, buff=0.3)
        self.hold(10, ([FadeIn(d1)], 5))
        tri = card("a triangle can carry a rank-one block", "u uᵀ has every off-diagonal entry nonzero when every uᵢ is nonzero. On a triangle it is a legal matrix with the triangle's pattern (diagonal free), of rank 1, the smallest possible.", color=ORANGE, width=84, font_size=21, title_size=26).next_to(d1, DOWN, buff=0.25)
        d1.generate_target(); d1.target.next_to(h, DOWN, buff=0.4)
        tri.next_to(d1.target, DOWN, buff=0.3)
        self.hold(11, ([FadeOut(m), FadeOut(obs), MoveToTarget(d1)], 0.6), ([FadeIn(tri)], 3))
        self.clear_all()

# ---------------------------------------------------------------- E14S04  The refutation
class E14S04(BeatScene):
    SCENE_ID = 'E14S04'
    def construct(self):
        h = header("The refutation")
        base, P = k4_base(LEFT*5.2+UP*1.2, scale=0.7)
        tri = Polygon(P[0], P[1], P[3], color=YELLOW, fill_opacity=0.25, stroke_width=0)
        obs = VGroup(wrap("voltage-0 edges: 0–1, 0–3, 1–3: a triangle on base vertices 0, 1, 3", 48, 24, YELLOW),
                     MathTex(r"\text{voltage }0:\ x_i\text{–}y_i\ \Rightarrow\ \{0_i,1_i,3_i\}\text{ is a triangle for each }i", font_size=24),
                     wrap("n triangles; the only edges leaving one go to the fibre over vertex 2", 48, 24, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3).shift(UP*1.6)
        self.hold(12, ([FadeIn(h), Create(base)], 1.5), ([FadeIn(tri), FadeIn(obs[0])], 2.5), ([Write(obs[1])], 3), ([FadeIn(obs[2])], 2))
        cov, pos = k4_cover(4, LEFT*3.6+DOWN*1.9, dx=1.25)
        self.play(FadeIn(cov), run_time=2)
        self.wait(0.5)
        build = card("build a matrix", [MathTex(r"\text{each triangle: the block }uu^{\!\top},\ u=(1,2,3)", font_size=26),
                                        MathTex(r"\text{edges to fibre }2:\ 1;\ \text{diagonal there: }1", font_size=26),
                                        Text("legal: every edge nonzero, diagonal free", font_size=22, color=MUTED)], color=GREEN, width=46).next_to(obs, DOWN, buff=0.3).to_edge(RIGHT, buff=0.3)
        self.hold(13, ([FadeIn(build)], 4))
        self.play(FadeOut(build), FadeOut(obs), run_time=0.4)
        cnt = VGroup(MathTex(r"3n\text{ triangle rows: block-diag of }n\text{ rank-1 blocks }(\le n)", font_size=23),
                     MathTex(r"+\ n\text{ columns of fibre }2\ (\le n)\ \Rightarrow\ \text{rank}\le2n", font_size=23),
                     MathTex(r"n\text{ rows at fibre }2:\ \le n", font_size=23),
                     MathTex(r"\operatorname{rank}\le3n\ \Rightarrow\ \operatorname{null}\ge4n-3n=n", font_size=32, color=YELLOW),
                     MathTex(r"\text{exact over }\mathbb Q:\ \operatorname{null}=n\ \text{for }n=4,\dots,10", font_size=23, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3).shift(UP*1.2)
        self.hold(14, ([Write(cnt[0]), Write(cnt[1])], 4), ([Write(cnt[2])], 2), ([Write(cnt[3])], 2.5))
        self.hold(15, ([FadeIn(cnt[4])], 2), ([FadeIn(card("so", [MathTex(r"M(B^n)\ge n,\quad Z-M\le2.", font_size=26, color=RED), wrap("The conjecture is false; K4 is cubic, so the regular-base claim is false too.", 46, 22, RED)], color=RED, width=46, title_size=26).next_to(cnt, DOWN, buff=0.3).to_edge(RIGHT, buff=0.3))], 3))
        self.clear_all()

# ---------------------------------------------------------------- E14S05  What was wrong
class E14S05(BeatScene):
    SCENE_ID = 'E14S05'
    def construct(self):
        h = header("What was actually wrong")
        a = VGroup(Text("the rank-one matrix is rotation-invariant, so the ceiling theorem should apply…", font_size=26),
                   MathTex(r"\text{but }\det M(\zeta)\equiv0:\ \text{the zero polynomial; its degree span is undefined}", font_size=28, color=RED),
                   wrap("the proof silently assumed det M(ζ) ≢ 0: true for P(n,k) and every base tested, never written down", 80, 24),
                   Text("the theorem was true with the hypothesis and wrong without it", font_size=26, color=YELLOW)).arrange(DOWN, buff=0.3).next_to(h, DOWN, buff=0.5)
        self.hold(16, ([FadeIn(h), FadeIn(a[0])], 2), ([Write(a[1])], 3), ([FadeIn(a[2])], 3), ([FadeIn(a[3])], 2))
        self.play(FadeOut(a), run_time=0.4)
        b = card("the second lesson", "Two adversarial searches for high-nullity matrices on this family missed it: the matrix lives where three of the four fibre blocks are singular, and neither search goes there.\nIt was found by reading the voltages and noticing the triangle.\nA failed search measures the effort spent, not the impossibility of what it failed to find.", color=ORANGE, width=80, font_size=21, title_size=26).next_to(h, DOWN, buff=0.4)
        self.hold(17, ([FadeIn(b)], 4.5))
        c = card("what replaces it: a conjecture", "On every base where the ceiling holds, the top coefficient of det M(ζ) is a product of edge weights only; on every base where it fails, it involves a diagonal entry. Checked on all ten bases in the paper, proved on three families, stated as a conjecture. Honestly labelled open.", color=BLUE, width=80, font_size=21, title_size=26).next_to(b, DOWN, buff=0.25)
        self.hold(18, ([FadeIn(c)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E14S06  Why this episode exists
class E14S06(BeatScene):
    SCENE_ID = 'E14S06'
    def construct(self):
        h = header("Why this episode exists")
        t = wrap("The clearest thing a research record can show is a false claim caught and corrected by its author, in writing, with the reason.\n\n1 October 2026: poster, abstract and paper corrected the same day; the log records what the claim was, who found the problem, and why the proof had a hole.\n\nIf you remember one thing from Part Two: the headline claim was wrong, the reason was a triangle hiding in three zeros, and the fix was a hypothesis the theorem had needed all along.", 72, 26).next_to(h, DOWN, buff=0.6)
        self.hold(19, ([FadeIn(h)], 0.8), ([FadeIn(t)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E14S07  Recap
class E14S07(BeatScene):
    SCENE_ID = 'E14S07'
    def construct(self):
        h = header("Recap: what you can now do")
        b = bullets(["define a voltage graph and unfold it for a given n",
                     "show the base (1, k, 0) unfolds to P(n,k)",
                     "define rank; compute the rank of uuᵀ; rank + nullity = N",
                     "read the K4 voltages and find the triangle",
                     "build the rank-one matrix and count: nullity ≥ n",
                     "state the hypothesis the cover theorem was missing; explain why two searches missed it"], font_size=26, width=70).next_to(h, DOWN, buff=0.6)
        self.hold(20, ([FadeIn(h)], 0.8), ([FadeIn(b, lag_ratio=0.2)], 5))
        self.clear_all()
