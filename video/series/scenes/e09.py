from lib import *

# ---------------------------------------------------------------- E09S01  Second question
class E09S01(BeatScene):
    SCENE_ID = 'E09S01'
    def construct(self):
        t = title_card("Episode 9", "Zero forcing: a colouring game, and why it bounds the nullity")
        self.hold(1, ([FadeIn(t)], 1.5), ([FadeOut(t)], 0.5), ([FadeIn(header("The second question"))], 0.8))
        rows = [[0,1,0,0,1,1,0,0,0,0],[1,0,1,0,0,0,1,0,0,0],[0,1,0,1,0,0,0,1,0,0],[0,0,1,0,1,0,0,0,1,0],[1,0,0,1,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,1,1,0],[0,1,0,0,0,0,0,0,1,1],[0,0,1,0,0,1,0,0,0,1],[0,0,0,1,0,1,1,0,0,0],[0,0,0,0,1,0,1,1,0,0]]
        A = int_matrix(rows, scale=0.48, h_buff=0.7, v_buff=0.55).shift(LEFT*3.3+DOWN*0.6)
        self.play(FadeIn(A), run_time=1)
        ents = A.get_entries(); pattern = VGroup()
        for i, e in enumerate(ents):
            r, c = divmod(i, 10)
            if rows[r][c] == 1: pattern.add(MathTex(r"\ast", color=ORANGE, font_size=26).move_to(e))
            elif r == c: pattern.add(MathTex(r"?", color=YELLOW, font_size=22).move_to(e))
            else: pattern.add(MathTex(r"0", color=MUTED, font_size=20).move_to(e))
        d1 = defn("matrix with the pattern of G", "Symmetric. Off the diagonal: nonzero exactly on the edges (∗). Diagonal: anything (?). The adjacency matrix is one of infinitely many.", width=42, font_size=24).to_edge(RIGHT, buff=0.4).shift(UP*1.2)
        self.play(Transform(ents, pattern), run_time=2)
        self.play(FadeIn(d1), run_time=1.5)
        self.wait(2)
        d2 = defn("maximum nullity M(G)", [MathTex(r"M(G)=\max\{\operatorname{null}A:\ A\ \text{symmetric with the pattern of }G\}", font_size=26),
                                           Text("how many times can 0 be made an eigenvalue, given only the connections?", font_size=22, color=MUTED)], width=42).next_to(d1, DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        self.hold(2, ([FadeIn(d2)], 3))
        why = wrap("Why: a molecule, a circuit, a spin chain is a symmetric matrix whose pattern is a graph; the values depend on details, the pattern on the connections. Computing M directly means searching infinitely many matrices. The tool: a colouring game.", 44, 22, INK).to_edge(RIGHT, buff=0.4).shift(DOWN*0.4)
        self.hold(3, ([FadeOut(d2), FadeOut(d1), FadeIn(why)], 3))
        self.clear_all()

# ---------------------------------------------------------------- E09S02  The game
class E09S02(BeatScene):
    SCENE_ID = 'E09S02'
    def construct(self):
        h = header("The game")
        rule = card("colour change rule", "Some vertices start blue, the rest white. Repeat: a blue vertex with exactly one white neighbour forces that neighbour blue.", color=YELLOW, width=60).next_to(h, DOWN, buff=0.4)
        self.hold(4, ([FadeIn(h)], 0.8), ([FadeIn(rule)], 3))
        self.play(rule.animate.scale(0.65).to_corner(UR, buff=0.3).shift(DOWN*0.8), run_time=0.6)
        d1 = defn("zero forcing set, Z(G)", "S is a zero forcing set if starting from S blue, everything ends blue. Z(G) = the smallest size of a zero forcing set.", width=40, font_size=20, title_size=24).next_to(rule, DOWN, buff=0.25).to_edge(RIGHT, buff=0.3)
        self.hold(5, ([FadeIn(d1)], 3))
        # path
        pp = [LEFT*5.5 + RIGHT*1.3*i + DOWN*0.3 for i in range(6)]
        pe = VGroup(*[Line(pp[i], pp[i+1], color=MUTED, stroke_width=3) for i in range(5)])
        pd = [vdot(p) for p in pp]; pd[0].set_color(BLUE)
        pl = MathTex(r"Z(\text{path})=1", font_size=32, color=GREEN).next_to(pe, DOWN, buff=0.5)
        self.hold(6, ([Create(pe), *[FadeIn(d) for d in pd]], 1.2))
        force_seq(self, pd, [(i, i+1) for i in range(5)], rt=0.7)
        self.play(Write(pl), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(pe), *[FadeOut(d) for d in pd], FadeOut(pl), run_time=0.5)
        # cycle
        cc = LEFT*3.2+DOWN*0.9; R = 1.7; m = 8
        cp = ring_points(m, R=R, center=cc)
        ce = VGroup(*[Line(cp[i], cp[(i+1) % m], color=MUTED, stroke_width=3) for i in range(m)])
        cd = [vdot(p) for p in cp]; cd[0].set_color(BLUE)
        stuck = Text("stuck: two white neighbours", font_size=24, color=RED).next_to(ce, DOWN, buff=0.3)
        self.hold(7, ([Create(ce), *[FadeIn(d) for d in cd]], 1.2), ([FadeIn(stuck)], 1.5), ([cd[1].animate.set_color(BLUE), FadeOut(stuck)], 1))
        force_seq(self, cd, [(1, 2), (0, 7), (2, 3), (7, 6), (3, 4), (6, 5)], rt=0.5)
        cl = MathTex(r"Z(\text{cycle})=2", font_size=32, color=GREEN).next_to(ce, DOWN, buff=0.3)
        self.play(Write(cl), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(ce), *[FadeOut(d) for d in cd], FadeOut(cl), run_time=0.5)
        g, d = petersen(5, 2, R_out=1.9, R_in=0.9, center=cc, dot_r=0.12)
        for i in range(5):
            d['u'][i].set_color(BLUE).set_stroke(INK, 2); d['v'][i].set_color(WHITE_V).set_stroke(INK, 2)
        self.hold(8, ([FadeIn(g)], 1.2), ([*[d['v'][i].animate.set_color(BLUE) for i in range(5)]], 1.5),
                  ([Write(MathTex(r"Z(\text{Petersen})=5\quad(\text{no 4-set works: checked})", font_size=26, color=GREEN).next_to(g, DOWN, buff=0.25))], 2))
        self.clear_all()

# ---------------------------------------------------------------- E09S03  Kernel tiny example
class E09S03(BeatScene):
    SCENE_ID = 'E09S03'
    def construct(self):
        h = header("The kernel, with a tiny example")
        pts = [LEFT*2+UP*1.5, UP*1.5, RIGHT*2+UP*1.5]
        g, dots, lines, labs = simple_graph(pts, [(0,1),(1,2)], labels=["0","1","2"], label_dir=[UP, UP, UP])
        A = MathTex(r"A=\begin{pmatrix}0&1&0\\1&0&1\\0&1&0\end{pmatrix}", font_size=34).next_to(g, DOWN, buff=0.4).shift(LEFT*3)
        eqs = VGroup(MathTex(r"\text{vertex }0:\ x_1=0", font_size=28), MathTex(r"\text{vertex }1:\ x_0+x_2=0", font_size=28), MathTex(r"\text{vertex }2:\ x_1=0", font_size=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(A, RIGHT, buff=1.0)
        self.hold(9, ([FadeIn(h), Create(lines), FadeIn(dots), FadeIn(labs)], 1.2), ([Write(A)], 2), ([FadeIn(eqs, lag_ratio=0.3)], 3))
        k1 = MathTex(r"\ker=\{\,c\,(1,0,-1)\,\}:\ \text{nullity }1", font_size=30, color=GREEN).next_to(A, DOWN, buff=0.7).shift(RIGHT*2.5)
        self.hold(10, ([Write(k1)], 2), ([Transform(A, MathTex(r"A=\begin{pmatrix}0&1&0\\1&7&1\\0&1&0\end{pmatrix}", font_size=34).move_to(A)), Transform(eqs[1], MathTex(r"\text{vertex }1:\ x_0+7x_1+x_2=0", font_size=28).move_to(eqs[1], aligned_edge=LEFT))], 1.5),
                  ([Transform(k1, MathTex(r"x_1=0\ \text{still}\ \Rightarrow\ \text{nullity }1", font_size=30, color=GREEN).move_to(k1, aligned_edge=LEFT))], 2),
                  ([Transform(A, MathTex(r"A=\begin{pmatrix}3&1&0\\1&7&1\\0&1&0\end{pmatrix}", font_size=34).move_to(A)), Transform(eqs[0], MathTex(r"\text{vertex }0:\ 3x_0+x_1=0", font_size=28).move_to(eqs[0], aligned_edge=LEFT))], 1.5),
                  ([Transform(k1, MathTex(r"x_1=0\Rightarrow x_0=0\Rightarrow x_2=0:\ \text{nullity }0", font_size=30, color=RED).move_to(k1, aligned_edge=LEFT))], 2),
                  ([FadeIn(Text("the diagonal matters", font_size=30, color=YELLOW).to_edge(DOWN, buff=0.8))], 1.5))
        self.clear_all()

# ---------------------------------------------------------------- E09S04  Why forcing bounds nullity
class E09S04(BeatScene):
    SCENE_ID = 'E09S04'
    def construct(self):
        h = header("Why forcing bounds the nullity")
        setup = MathTex(r"A\ \text{with the pattern of }G;\quad Ax=0;\quad x=0\ \text{on a set }B\ \text{(colour }B\text{ blue)}", font_size=30).next_to(h, DOWN, buff=0.4)
        self.hold(11, ([FadeIn(h), Write(setup)], 3), ([FadeIn(Text("blue = the kernel vector is known to vanish there", font_size=26, color=BLUE).next_to(setup, DOWN, buff=0.3))], 2))
        c = LEFT*3.8+DOWN*1.3
        pu = c; pw = c + RIGHT*2.0; pv1 = c + UP*1.3 + LEFT*1.1; pv2 = c + DOWN*1.3 + LEFT*1.1
        ed = VGroup(Line(pu, pw, color=MUTED, stroke_width=3), Line(pu, pv1, color=MUTED, stroke_width=3), Line(pu, pv2, color=MUTED, stroke_width=3))
        du = vdot(pu, True); dw = vdot(pw); dv1 = vdot(pv1, True); dv2 = vdot(pv2, True)
        lab = VGroup(MathTex("u", font_size=28).next_to(du, DOWN, buff=0.15), MathTex("w", font_size=28).next_to(dw, DOWN, buff=0.15))
        row = VGroup(MathTex(r"\text{row }u:\ A_{uu}x_u+\sum_{v\sim u}A_{uv}x_v=0", font_size=30),
                     MathTex(r"x_u=0;\ x_v=0\ \text{for the blue }v\ \Rightarrow\ A_{uw}\,x_w=0", font_size=28),
                     MathTex(r"A_{uw}\ne0\ (\text{edge})\ \Rightarrow\ x_w=0", font_size=32, color=GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(DOWN*1.0)
        self.hold(12, ([Create(ed), FadeIn(du), FadeIn(dw), FadeIn(dv1), FadeIn(dv2), FadeIn(lab)], 1.5), ([Write(row[0])], 3), ([Write(row[1])], 3), ([Write(row[2]), dw.animate.set_color(BLUE)], 2.5))
        self.play(FadeOut(row), FadeOut(ed), FadeOut(du), FadeOut(dw), FadeOut(dv1), FadeOut(dv2), FadeOut(lab), run_time=0.5)
        concl = VGroup(Text("that is exactly the colour change rule", font_size=28, color=YELLOW),
                       MathTex(r"S\ \text{zero forcing},\ x|_S=0\ \Rightarrow\ x=0\ \text{everywhere}", font_size=30),
                       MathTex(r"\Rightarrow\ \text{a kernel vector is determined by its values on }S\ \Rightarrow\ \operatorname{null}A\le|S|", font_size=28)).arrange(DOWN, buff=0.35).shift(DOWN*0.6)
        self.hold(13, ([FadeIn(concl[0])], 1.5), ([Write(concl[1])], 2.5), ([Write(concl[2])], 3))
        self.play(FadeOut(concl), run_time=0.4)
        big = card("the bridge (2008)", [MathTex(r"\operatorname{null}A\le Z(G)\ \text{ for every }A\text{ with the pattern (symmetric or not)}", font_size=30),
                                         MathTex(r"M(G)\ \le\ Z(G)", font_size=44, color=YELLOW)], color=YELLOW, width=66).shift(DOWN*0.6)
        self.hold(14, ([FadeIn(big)], 3.5))
        self.clear_all()

# ---------------------------------------------------------------- E09S05  Why useful
class E09S05(BeatScene):
    SCENE_ID = 'E09S05'
    def construct(self):
        h = header("Why the inequality is useful")
        a = VGroup(wrap("Z ≤ m:  exhibit one forcing set of size m and play the game.  Easy.", 66, 28, GREEN),
                   wrap("Z ≥ m:  show every set of size m − 1 fails.  50 vertices, size 8: hundreds of millions of sets.", 66, 28, RED)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(h, DOWN, buff=0.6)
        self.hold(15, ([FadeIn(a[0])], 2.5), ([FadeIn(a[1])], 3))
        b = card("the strategy of Part Two", [MathTex(r"\text{one matrix with nullity }8\ \Rightarrow\ M\ge8\ \Rightarrow\ Z\ge8", font_size=30),
                                               Text("a matrix is a certificate: anyone can verify its nullity by elimination in a minute", font_size=24),
                                               MathTex(r"\text{nullity}=\text{forcing-set size}\ \Rightarrow\ M=Z\ \text{exactly}", font_size=28, color=YELLOW)], color=YELLOW, width=66).next_to(a, DOWN, buff=0.6)
        self.hold(16, ([FadeIn(b)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E09S06  What was known
class E09S06(BeatScene):
    SCENE_ID = 'E09S06'
    def construct(self):
        h = header("What was known about P(n,k)")
        n, k = 12, 3
        g, d = petersen(n, k, R_out=2.1, R_in=1.0, center=LEFT*3.8+DOWN*0.8, dot_r=0.1)
        for i in range(2*k+2): d['u'][i].set_color(BLUE)
        ub = VGroup(MathTex(r"Z(P(n,k))\le2k+2", font_size=36), Text("Rashidi, Shajareh Poursalavati, Tavakkoli (2020):\n2k+2 consecutive outer vertices; the rotation sweeps it around", font_size=22, color=MUTED, line_spacing=1.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP*2.0)
        self.hold(17, ([FadeIn(h), FadeIn(g)], 1.5), ([Write(ub[0]), FadeIn(ub[1])], 3))
        k2 = MathTex(r"Z(P(n,2))=6\ \ (n\ge10)", font_size=30).next_to(ub, DOWN, buff=0.4, aligned_edge=LEFT)
        k3 = MathTex(r"\text{Thm 3.6: }Z(P(n,3))=8\ \ (n\ge12)", font_size=30).next_to(k2, DOWN, buff=0.25, aligned_edge=LEFT)
        self.hold(18, ([Write(k2)], 2), ([Write(k3)], 2))
        cross = Cross(k3, stroke_color=RED, stroke_width=5)
        kr = VGroup(Text("Krishnan, July 2026:", font_size=26, color=YELLOW), MathTex(r"Z(P(12,3))=7", font_size=32, color=YELLOW),
                    MathTex(r"\begin{array}{r|ccccccc} n & 7 & 8 & 9 & 10 & 11 & 12 & 13\text{--}20\\ \hline Z & 6 & 6 & 6 & 8 & 7 & 7 & 8\end{array}", font_size=28),
                    MathTex(r"\textbf{Conjecture 5: }Z(P(n,3))=8\ \ \forall n\ge13", font_size=28, color=YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(k3, DOWN, buff=0.35, aligned_edge=LEFT)
        self.hold(19, ([Create(cross)], 1), ([FadeIn(kr[0]), Write(kr[1])], 2), ([Write(kr[2])], 3), ([Write(kr[3])], 2.5))
        self.play(FadeOut(VGroup(k2, k3, cross, kr)), run_time=0.5)
        k4 = VGroup(MathTex(r"k\ge4:\ \text{only }Z(P(2k+1,k))=6\ \text{known},\ \ll2k+2", font_size=26),
                    wrap("open: the threshold at k = 3; any rigorous lower bound for k ≥ 4", 46, 24, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ub, DOWN, buff=0.5, aligned_edge=LEFT)
        self.hold(20, ([Write(k4[0])], 2.5), ([FadeIn(k4[1])], 2.5))
        self.clear_all()

# ---------------------------------------------------------------- E09S07  What a lower bound requires
class E09S07(BeatScene):
    SCENE_ID = 'E09S07'
    def construct(self):
        h = header("What a lower bound for all n requires")
        need = card("needed", [MathTex(r"\text{for every }n:\ \text{a matrix on the }P(n,k)\text{ pattern with nullity }2k+2", font_size=30),
                                Text("not one matrix per n found by search, forever", font_size=24, color=MUTED),
                                Text("a construction uniform in n, with a proof it works for all of them", font_size=28, color=YELLOW)], color=YELLOW, width=66).next_to(h, DOWN, buff=0.6)
        self.hold(21, ([FadeIn(need)], 4))
        road = bullets(["episode 10: how far any matrix on this pattern can go — an exact ceiling",
                        "episode 11: the first certificates, and why they cannot reach every n",
                        "episodes 12–13: break the symmetry and reach every n"], font_size=26, width=66).next_to(need, DOWN, buff=0.6)
        self.hold(22, ([FadeIn(road, lag_ratio=0.3)], 4))
        self.clear_all()

# ---------------------------------------------------------------- E09S08  Recap
class E09S08(BeatScene):
    SCENE_ID = 'E09S08'
    def construct(self):
        h = header("Recap: what you can now do")
        b = bullets(["define a matrix with the pattern of a graph, and M(G)",
                     "state the colour change rule; play it on a path, a cycle, the Petersen graph; define Z",
                     "compute the kernel of the 3-vertex path and see why the diagonal matters",
                     "reproduce the one-slide argument: kernel vector zero on a forcing set ⇒ zero; M ≤ Z",
                     "explain why a matrix is a certificate for a lower bound on Z",
                     "state what was known: 2k+2, k = 2, the false theorem, Krishnan's Conjecture 5"], font_size=26, width=70).next_to(h, DOWN, buff=0.6)
        self.hold(23, ([FadeIn(h)], 0.8), ([FadeIn(b, lag_ratio=0.2)], 5))
        self.clear_all()
