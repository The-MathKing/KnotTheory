from lib import *

# ---------------------------------------------------------------- E01S01  What this series is
class E01S01(BeatScene):
    SCENE_ID = 'E01S01'
    def construct(self):
        t = title_card("Episode 1", "Graphs, and the Petersen family")
        g, d = petersen(5, 2, R_out=1.6, R_in=0.75, center=DOWN*2.2)
        self.hold(1, ([FadeIn(t)], 1.5), ([Create(d['outer']), FadeIn(d['u'])], 1.5), ([Create(d['inner']), FadeIn(d['v']), Create(d['spokes'])], 1.5))
        self.play(FadeOut(t), FadeOut(g), run_time=0.6)
        plan = VGroup(
            Text("Episodes 1–3", font_size=30, weight=BOLD, color=BLUE), wrap("graphs, matrices and eigenvalues, what eigenvalues tell you", 60, 26, MUTED),
            Text("Episodes 4–8", font_size=30, weight=BOLD, color=YELLOW), wrap("Question 1: the fixed matrix — which P(n,k) are Ramanujan?", 60, 26, MUTED),
            Text("Episodes 9–14", font_size=30, weight=BOLD, color=TEAL), wrap("Question 2: every matrix with the graph's shape — maximum nullity", 60, 26, MUTED),
            Text("Episode 15", font_size=30, weight=BOLD, color=GREEN), wrap("what is proved, what is open, how the numbers are checked", 60, 26, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.hold(2, ([FadeIn(plan[0]), FadeIn(plan[1])], 1.5), ([], 3), ([FadeIn(plan[2]), FadeIn(plan[3])], 1.5), ([], 3), ([FadeIn(plan[4]), FadeIn(plan[5])], 1.5), ([], 3), ([FadeIn(plan[6]), FadeIn(plan[7])], 1.5))
        self.play(FadeOut(plan), run_time=0.6)
        c = idea("how to watch", "Every worked example uses real numbers you can redo on paper.\nPause. Redo it. Then trust the general statement.", width=52)
        self.hold(3, ([FadeIn(c)], 1.5))
        self.clear_all()

# ---------------------------------------------------------------- E01S02  What a graph is
class E01S02(BeatScene):
    SCENE_ID = 'E01S02'
    def construct(self):
        h = header("What a graph is")
        d1 = defn("graph", "A set of points (vertices) and a set of lines joining some pairs of them (edges).\nPositions and lengths do not matter. Only which pairs are joined.", width=56).next_to(h, DOWN, buff=0.5)
        self.hold(4, ([FadeIn(h)], 1), ([FadeIn(d1)], 2))
        self.play(d1.animate.scale(0.8).to_edge(LEFT, buff=0.5).shift(DOWN*0.3), run_time=0.8)
        # C4 drawn three ways
        sq = [LEFT*1.5+UP*1.5, RIGHT*1.5+UP*1.5, RIGHT*1.5+DOWN*1.5, LEFT*1.5+DOWN*1.5]
        base = RIGHT*3.3 + DOWN*0.4
        pts = [base + p*0.8 for p in sq]
        g, dots, lines, labs = simple_graph(pts, [(0,1),(1,2),(2,3),(3,0)], labels=["0","1","2","3"], label_dir=[UL, UR, DR, DL])
        name = MathTex(r"C_4", font_size=40, color=BLUE).next_to(g, UP, buff=0.3)
        self.hold(5, ([Create(lines), FadeIn(dots), FadeIn(labs)], 2), ([Write(name)], 1))
        dia = [base + np.array([0, 1.4, 0]), base + np.array([1.4, 0.2, 0]), base + np.array([-0.3, -1.3, 0]), base + np.array([-1.5, 0.4, 0])]
        g2, dots2, lines2, labs2 = simple_graph(dia, [(0,1),(1,2),(2,3),(3,0)], labels=["0","1","2","3"], label_dir=[UP, RIGHT, DOWN, LEFT])
        self.play(Transform(g, g2), run_time=1.5)
        self.wait(0.5)
        g3, *_ = simple_graph(pts, [(0,1),(1,2),(2,3),(3,0)], labels=["0","1","2","3"], label_dir=[UL, UR, DR, DL])
        self.play(Transform(g, g3), run_time=1.5)
        # degree
        d2 = VGroup(defn("neighbours", "Two vertices joined by an edge.", width=40, font_size=24, title_size=26),
                    defn("degree", "The number of neighbours a vertex has.", width=40, font_size=24, title_size=26),
                    defn("regular / cubic", "Every vertex has the same degree / that degree is 3.", width=40, font_size=24, title_size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).scale(0.85).to_edge(LEFT, buff=0.5).shift(DOWN*0.3)
        hl = VGroup(lines[0].copy().set_color(YELLOW).set_stroke(width=6), lines[3].copy().set_color(YELLOW).set_stroke(width=6))
        deg = Text("degree 2", font_size=26, color=YELLOW).next_to(g, DOWN, buff=0.3)
        self.hold(6, ([FadeOut(d1), FadeIn(d2[0])], 1.2), ([FadeIn(hl), FadeIn(deg)], 1.2), ([FadeIn(d2[1])], 1.2), ([FadeIn(d2[2])], 1.5))
        self.play(FadeOut(hl), FadeOut(deg), FadeOut(g), FadeOut(name), run_time=0.6)
        # cube and path
        cube_pts = [np.array([x, y, 0]) for x, y in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        cube_pts += [p*0.5 + np.array([0.35, 0.35, 0]) for p in cube_pts]
        cube_pts = [RIGHT*3.6 + UP*0.9 + p*0.9 for p in cube_pts]
        cube_e = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
        cg, cd, cl, _ = simple_graph(cube_pts, cube_e, dot_r=0.09)
        cl_t = Text("cube: cubic, 8 vertices, 12 edges", font_size=22, color=GREEN).next_to(cg, DOWN, buff=0.25)
        path_pts = [RIGHT*2.2 + DOWN*2.4 + RIGHT*0.9*i for i in range(4)]
        pg, pd, pl, _ = simple_graph(path_pts, [(0,1),(1,2),(2,3)], dot_r=0.09)
        pl_t = Text("path: degrees 1, 2, 2, 1 — not regular", font_size=22, color=ORANGE).next_to(pg, DOWN, buff=0.25)
        self.hold(7, ([Create(cl), FadeIn(cd), FadeIn(cl_t)], 2), ([Create(pl), FadeIn(pd), FadeIn(pl_t)], 2))
        self.clear_all()

# ---------------------------------------------------------------- E01S03  The Petersen graph
class E01S03(BeatScene):
    SCENE_ID = 'E01S03'
    def construct(self):
        h = header("The Petersen graph")
        g, d = petersen(5, 2, R_out=2.4, R_in=1.1, center=LEFT*3+DOWN*0.4, dot_r=0.09)
        ul = VGroup(*[MathTex(f"u_{i}", font_size=26, color=BLUE).move_to(LEFT*3+DOWN*0.4 + (d['upos'][i]-(LEFT*3+DOWN*0.4))*1.14) for i in range(5)])
        vl = ring_labels(d, 'v', center=LEFT*3+DOWN*0.4, factor=1.32, tangent=0.3, font_size=22)
        steps = VGroup(Text("outer ring: 5 vertices, join neighbours", font_size=26, color=BLUE),
                       Text("inner star: join two steps around", font_size=26, color=ORANGE),
                       Text("spokes: outer to inner, same index", font_size=26, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.6).shift(UP*1.2)
        self.hold(8, ([FadeIn(h)], 0.8), ([Create(d['outer']), FadeIn(d['u']), FadeIn(ul), FadeIn(steps[0])], 2.5),
                  ([Create(d['inner']), FadeIn(d['v']), FadeIn(vl), FadeIn(steps[1])], 2.5), ([Create(d['spokes']), FadeIn(steps[2])], 2))
        count = VGroup(MathTex(r"10\ \text{vertices}", font_size=30), MathTex(r"5+5+5=15\ \text{edges}", font_size=30),
                       MathTex(r"\text{every vertex: degree }3\ \Rightarrow\ \text{cubic}", font_size=30, color=GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(steps, DOWN, buff=0.6, aligned_edge=LEFT)
        hl = VGroup(d['outer'][0].copy(), d['outer'][4].copy(), d['spokes'][0].copy()).set_color(YELLOW).set_stroke(width=6)
        self.hold(9, ([FadeIn(count[0]), FadeIn(count[1])], 2), ([FadeIn(hl)], 1), ([FadeIn(count[2])], 1.5))
        self.play(FadeOut(hl), run_time=0.5)
        sym = wrap("the feature we care about: its symmetry (next)", 30, 26, YELLOW).next_to(count, DOWN, buff=0.6, aligned_edge=LEFT)
        self.hold(10, ([FadeIn(sym)], 1.5))
        self.clear_all()

# ---------------------------------------------------------------- E01S04  P(n,k)
class E01S04(BeatScene):
    SCENE_ID = 'E01S04'
    def construct(self):
        h = header("Generalized Petersen graphs P(n,k)")
        d1 = defn("P(n,k)", "n outer vertices in a ring; n inner vertices, each joined to the one k steps on; spokes between matching indices.", width=60).next_to(h, DOWN, buff=0.4)
        g, d = petersen(5, 2, R_out=1.7, R_in=0.8, center=LEFT*3.8+DOWN*1.6, dot_r=0.07)
        lab = MathTex(r"P(5,2)", font_size=34).next_to(g, DOWN, buff=0.2)
        self.hold(11, ([FadeIn(h)], 0.8), ([FadeIn(d1)], 2), ([FadeIn(g), FadeIn(lab)], 1.5))
        n = 8
        c = LEFT*3.2+DOWN*0.9
        g8, d8 = petersen(n, 3, R_out=2.1, R_in=1.0, center=c, dot_r=0.07)
        ul = ring_labels(d8, 'u', center=c, factor=1.15)
        r1 = MathTex(r"u_i \sim u_{i+1}\quad(\text{indices mod } n)", font_size=30, color=BLUE).move_to(RIGHT*3.2+UP*1.6)
        self.hold(12, ([FadeOut(d1), FadeOut(g), FadeOut(lab)], 0.5), ([Create(d8['outer']), FadeIn(d8['u']), FadeIn(ul)], 2), ([Write(r1)], 1.5))
        r2 = MathTex(r"v_i \sim v_{i+k}", font_size=30, color=ORANGE).next_to(r1, DOWN, buff=0.3, aligned_edge=LEFT)
        inner1 = petersen(n, 1, R_out=2.1, R_in=1.0, center=c)[1]['inner']
        inner2 = petersen(n, 2, R_out=2.1, R_in=1.0, center=c)[1]['inner']
        kl = MathTex("k=1", font_size=30, color=MUTED).next_to(r2, DOWN, buff=0.3, aligned_edge=LEFT)
        self.hold(13, ([FadeIn(d8['v']), Write(r2)], 1.2), ([Create(inner1), FadeIn(kl)], 1.5),
                  ([Transform(inner1, inner2), Transform(kl, MathTex("k=2", font_size=30, color=MUTED).move_to(kl))], 1.5),
                  ([Transform(inner1, d8['inner']), Transform(kl, MathTex("k=3", font_size=30, color=MUTED).move_to(kl))], 1.5))
        r3 = MathTex(r"u_i \sim v_i", font_size=30, color=MUTED).next_to(kl, DOWN, buff=0.3, aligned_edge=LEFT)
        cub = Text("cubic: 2n vertices, 3n edges", font_size=26, color=GREEN).next_to(r3, DOWN, buff=0.3, aligned_edge=LEFT)
        self.hold(14, ([Create(d8['spokes']), Write(r3)], 1.5), ([FadeIn(cub)], 1.5))
        rule = card("Rule", "Only k < n/2.  P(n,k) and P(n,n−k) are the same graph (step k forward = step n−k backward).\nn = 8: k = 1, 2, 3 only.", color=PURPLE, width=40, font_size=22).next_to(cub, DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        self.hold(15, ([FadeIn(rule)], 2))
        self.clear_all()

# ---------------------------------------------------------------- E01S05  P(7,2) by hand
class E01S05(BeatScene):
    SCENE_ID = 'E01S05'
    def construct(self):
        h = header("Worked example: P(7,2) by hand")
        n = 7; c = LEFT*3.4+DOWN*0.5
        g, d = petersen(n, 2, R_out=2.3, R_in=1.1, center=c, dot_r=0.08)
        ul = VGroup(*[MathTex(f"u_{i}", font_size=22, color=BLUE).move_to(c + (d['upos'][i]-c)*1.14) for i in range(n)])
        vl = ring_labels(d, 'v', center=c, factor=0.52, font_size=18)
        outer_list = MathTex(r"u_0u_1,\ u_1u_2,\ \dots,\ u_6u_0\quad(7)", font_size=28, color=BLUE).to_edge(RIGHT, buff=0.4).shift(UP*2.0)
        inner_list = VGroup(MathTex(r"v_0v_2,\ v_1v_3,\ v_2v_4,\ v_3v_5,", font_size=28, color=ORANGE),
                            MathTex(r"v_4v_6,\ v_5v_0,\ v_6v_1\quad(7)", font_size=28, color=ORANGE),
                            MathTex(r"6+2=8\equiv1\pmod 7", font_size=26, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(outer_list, DOWN, buff=0.4, aligned_edge=LEFT)
        self.hold(16, ([FadeIn(h)], 0.8), ([Create(d['outer']), FadeIn(d['u']), FadeIn(ul), Write(outer_list)], 2.5),
                  ([FadeIn(d['v']), FadeIn(vl)], 0.8), *[([Create(d['inner'][i])], 0.5) for i in range(n)], ([Write(inner_list)], 2))
        spk = MathTex(r"u_iv_i\quad(7)", font_size=28, color=MUTED).next_to(inner_list, DOWN, buff=0.4, aligned_edge=LEFT)
        tot = MathTex(r"21\ \text{edges},\ 14\ \text{vertices}", font_size=28).next_to(spk, DOWN, buff=0.3, aligned_edge=LEFT)
        hl = VGroup(d['inner'][3].copy(), d['inner'][1].copy(), d['spokes'][3].copy()).set_color(YELLOW).set_stroke(width=6)
        chk = MathTex(r"v_3:\ v_5,\ v_1,\ u_3\ \Rightarrow\ \text{degree }3", font_size=26, color=GREEN).next_to(tot, DOWN, buff=0.3, aligned_edge=LEFT)
        self.hold(17, ([Create(d['spokes']), Write(spk)], 1.5), ([Write(tot)], 1.2), ([FadeIn(hl), Write(chk)], 2))
        self.play(FadeOut(hl), run_time=0.4)
        # P(8,2): two 4-cycles
        g8, d8 = petersen(8, 2, R_out=2.3, R_in=1.1, center=c, dot_r=0.08)
        for i in range(8):
            d8['inner'][i].set_color(TEAL if i % 2 == 0 else PURPLE)
        note = wrap("P(7,2): one 7-pointed star (gcd(2,7)=1).\nP(8,2): two separate 4-cycles (2 divides 8). Both are fine.", 40, 24, INK).to_edge(RIGHT, buff=0.4).shift(DOWN*0.3)
        self.hold(18, ([Indicate(d['inner'], color=YELLOW)], 2), ([FadeOut(VGroup(outer_list, inner_list, spk, tot, chk, ul, vl))], 0.5),
                  ([Transform(g, g8)], 1.5), ([FadeIn(note)], 2))
        self.clear_all()

# ---------------------------------------------------------------- E01S06  Symmetry
class E01S06(BeatScene):
    SCENE_ID = 'E01S06'
    def construct(self):
        h = header("The symmetry")
        n = 8; c = LEFT*3.4+DOWN*0.5
        g, d = petersen(n, 3, R_out=2.3, R_in=1.1, center=c, dot_r=0.08)
        ul = ring_labels(d, 'u', center=c, factor=1.14)
        whole = g
        rot = MathTex(r"i\ \mapsto\ i+1", font_size=40, color=GREEN).move_to(RIGHT*3.2+UP*2.2)
        checks = VGroup(MathTex(r"u_iu_{i+1}\ \to\ u_{i+1}u_{i+2}\ \checkmark", font_size=28, color=BLUE),
                        MathTex(r"v_iv_{i+k}\ \to\ v_{i+1}v_{i+1+k}\ \checkmark", font_size=28, color=ORANGE),
                        MathTex(r"u_iv_i\ \to\ u_{i+1}v_{i+1}\ \checkmark", font_size=28, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(rot, DOWN, buff=0.5).shift(LEFT*0.3)
        self.hold(19, ([FadeIn(h), FadeIn(whole), FadeIn(ul)], 1.2), ([Write(rot)], 1), ([Rotate(whole, angle=2*PI/n, about_point=c)], 2),
                  ([FadeIn(checks[0])], 1.2), ([FadeIn(checks[1])], 1.2), ([FadeIn(checks[2])], 1.2))
        d1 = defn("automorphism", "A relabelling of the vertices that sends edges to edges. Rotating by one step is one; doing it n times is the identity: a cyclic symmetry of order n.", width=40, font_size=22).next_to(checks, DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        self.hold(20, ([Rotate(whole, angle=2*PI/n, about_point=c)], 2), ([FadeIn(d1)], 2))
        self.play(FadeOut(checks), FadeOut(d1), run_time=0.5)
        why = idea("why it matters", "A symmetry of the graph is a symmetry of every matrix built from it.\nA 2n × 2n matrix with this symmetry splits into n separate 2 × 2 pieces (episode 5).", width=40, font_size=22).next_to(rot, DOWN, buff=0.5).to_edge(RIGHT, buff=0.4)
        self.hold(21, ([FadeIn(why)], 2), ([Rotate(whole, angle=2*PI/n, about_point=c)], 2))
        self.clear_all()

# ---------------------------------------------------------------- E01S07  Recap
class E01S07(BeatScene):
    SCENE_ID = 'E01S07'
    def construct(self):
        h = header("Recap: what you can now do")
        b = bullets(["define a graph: vertices and edges; positions irrelevant",
                     "define degree, regular, cubic",
                     "draw the Petersen graph and explain why it is cubic",
                     "draw P(n,k): outer ring, inner step k, spokes",
                     "explain why k < n/2",
                     "explain why rotating every index by one is a symmetry"], font_size=28, width=60).next_to(h, DOWN, buff=0.6)
        self.hold(22, ([FadeIn(h)], 0.8), ([FadeIn(b, lag_ratio=0.2)], 5))
        nxt = Text("Next: matrices, and the eigenvalue", font_size=32, color=YELLOW).to_edge(DOWN, buff=0.8)
        self.hold(23, ([FadeIn(nxt)], 1.5))
        self.clear_all()
