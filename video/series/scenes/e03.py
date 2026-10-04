from lib import *

def pet_adj(n, k):
    A = np.zeros((2*n, 2*n))
    for i in range(n):
        A[i, (i+1) % n] = A[(i+1) % n, i] = 1
        A[n+i, n+(i+k) % n] = A[n+(i+k) % n, n+i] = 1
        A[i, n+i] = A[n+i, i] = 1
    return A

# ---------------------------------------------------------------- E03S01  Random walk
class E03S01(BeatScene):
    SCENE_ID = 'E03S01'
    def construct(self):
        h = header("A random walk on a graph")
        c = LEFT*3.5+DOWN*0.6
        g, d = petersen(5, 2, R_out=2.1, R_in=1.0, center=c, dot_r=0.1)
        tok = Dot(d['upos'][0], radius=0.18, color=YELLOW)
        rule = card("Rule", "Each second the token moves to one of its 3 neighbours, each with probability 1/3.", color=YELLOW, width=40, font_size=24).to_edge(RIGHT, buff=0.5).shift(UP*1.5)
        self.hold(1, ([FadeIn(h), FadeIn(g)], 1), ([FadeIn(tok)], 0.8), ([FadeIn(rule)], 1.5),
                  ([tok.animate.move_to(d['upos'][1])], 0.8), ([tok.animate.move_to(d['vpos'][1])], 0.8), ([tok.animate.move_to(d['vpos'][3])], 0.8), ([tok.animate.move_to(d['upos'][3])], 0.8))
        self.play(FadeOut(tok), run_time=0.4)
        p0 = MathTex(r"p=(1,0,0,0,0,0,0,0,0,0)", font_size=28).next_to(rule, DOWN, buff=0.5)
        p1 = MathTex(r"\text{after 1 step: }\tfrac13\text{ at }u_1,u_4,v_0", font_size=28).next_to(p0, DOWN, buff=0.3)
        labs = VGroup(*[MathTex(r"\tfrac13", font_size=24, color=YELLOW).next_to(d['u'][i], UP, buff=0.1) for i in (1, 4)], MathTex(r"\tfrac13", font_size=24, color=YELLOW).next_to(d['v'][0], DOWN, buff=0.1))
        self.hold(2, ([Write(p0)], 1.5), ([Write(p1), FadeIn(labs)], 2))
        e = MathTex(r"p_{\text{new}}(i)=\sum_{j\sim i}\frac{p_{\text{old}}(j)}{3}\quad\Rightarrow\quad p_{\text{new}}=\tfrac13A\,p_{\text{old}}", font_size=32, color=GREEN).next_to(p1, DOWN, buff=0.5)
        e2 = MathTex(r"p_t=\bigl(\tfrac13A\bigr)^t p_0", font_size=36, color=YELLOW).next_to(e, DOWN, buff=0.4)
        self.hold(3, ([FadeOut(labs)], 0.3), ([Write(e)], 3), ([Write(e2)], 2))
        self.clear_all()

# ---------------------------------------------------------------- E03S02  Forgetting
class E03S02(BeatScene):
    SCENE_ID = 'E03S02'
    def construct(self):
        h = header("Watching the walk forget")
        A = pet_adj(5, 2); W = A/3; p = np.zeros(10); p[0] = 1
        c = LEFT*3.5+DOWN*0.7
        g, d = petersen(5, 2, R_out=2.1, R_in=1.0, center=c, dot_r=0.05)
        def bars(pv):
            vg = VGroup()
            for i in range(10):
                pos = d['upos'][i] if i < 5 else d['vpos'][i-5]
                vg.add(Circle(radius=0.08+0.9*pv[i], color=YELLOW, fill_opacity=0.5, stroke_width=1).move_to(pos))
            return vg
        tbl = VGroup(MathTex(r"t", font_size=28), MathTex(r"\max_i|p_t(i)-0.1|", font_size=28), MathTex(r"(2/3)^t", font_size=28)).arrange(RIGHT, buff=0.8).to_edge(RIGHT, buff=0.5).shift(UP*2.2)
        rows = VGroup()
        devs = []
        cur = bars(p)
        self.hold(4, ([FadeIn(h), FadeIn(g), FadeIn(cur), FadeIn(tbl)], 1))
        q = p.copy()
        for t in range(1, 8):
            q = W @ q
            dev = np.abs(q-0.1).max()
            r = VGroup(MathTex(str(t), font_size=26), MathTex(f"{dev:.3f}", font_size=26), MathTex(f"{(2/3)**t:.3f}", font_size=26, color=MUTED)).arrange(RIGHT, buff=1.2)
            r.next_to(tbl, DOWN, buff=0.25+0.42*(t-1)).align_to(tbl, LEFT)
            rows.add(r)
            self.play(Transform(cur, bars(q)), FadeIn(r), run_time=0.9)
        self.wait(1)
        unif = MathTex(r"\tfrac13A\cdot\tfrac1{10}\mathbf 1=\tfrac1{10}\mathbf 1\quad(\text{uniform is a fixed point})", font_size=28, color=GREEN).next_to(rows, DOWN, buff=0.4).align_to(tbl, LEFT)
        self.hold(5, ([Write(unif)], 2.5))
        self.play(FadeOut(rows), FadeOut(tbl), FadeOut(unif), FadeOut(g), FadeOut(cur), run_time=0.5)
        dec = idea("decompose along eigenvectors", [MathTex(r"p_0=c_3\mathbf 1+(\text{eigenvalue-1 pieces})+(\text{eigenvalue-}(-2)\text{ pieces})", font_size=28),
                                                   MathTex(r"\tfrac13A:\quad \mathbf 1\mapsto\tfrac33\mathbf 1=\mathbf 1,\qquad x_1\mapsto\tfrac13x_1,\qquad x_{-2}\mapsto-\tfrac23x_{-2}", font_size=28)], width=60).next_to(h, DOWN, buff=0.5)
        self.hold(6, ([FadeIn(dec)], 3))
        after = VGroup(MathTex(r"\bigl(\tfrac13A\bigr)^t p_0=c_3\mathbf 1+\bigl(\tfrac13\bigr)^t(\cdots)+\bigl(-\tfrac23\bigr)^t(\cdots)", font_size=30),
                       MathTex(r"(2/3)^7=0.059;\quad\text{measured deviation }0.023\ \text{(that factor times the piece's size)}", font_size=26, color=MUTED),
                       Text("the slowest-shrinking piece controls convergence: eigenvalue −2 here", font_size=26, color=YELLOW)).arrange(DOWN, buff=0.35).next_to(dec, DOWN, buff=0.5)
        self.hold(7, ([Write(after[0])], 2.5), ([FadeIn(after[1])], 2.5), ([FadeIn(after[2])], 2))
        self.clear_all()

# ---------------------------------------------------------------- E03S03  Spectral gap
class E03S03(BeatScene):
    SCENE_ID = 'E03S03'
    def construct(self):
        h = header("The spectral gap")
        d1 = defn("λ₂ and the spectral gap", "λ₂ = the largest |eigenvalue| other than 3. Non-uniform pieces shrink like (λ₂/3)ᵗ.\nSpectral gap = 3 − λ₂.", width=58).next_to(h, DOWN, buff=0.4)
        self.hold(8, ([FadeIn(h)], 0.8), ([FadeIn(d1)], 2.5))
        d2 = defn("expander", "A graph with a large spectral gap: fast mixing, no bottlenecks, every vertex set has many edges leaving it.", width=58).next_to(d1, DOWN, buff=0.3)
        self.hold(9, ([FadeIn(d2)], 2.5))
        self.play(FadeOut(d1), FadeOut(d2), run_time=0.4)
        # compare C10 and Petersen on number lines
        ax1 = NumberLine(x_range=[-3, 3, 1], length=6, include_numbers=True, color=MUTED).shift(LEFT*3.2+DOWN*0.3)
        ax2 = NumberLine(x_range=[-3, 3, 1], length=6, include_numbers=True, color=MUTED).shift(RIGHT*3.2+DOWN*0.3)
        c10 = [2*np.cos(2*PI*j/10) for j in range(10)]
        d10 = VGroup(*[Dot(ax1.n2p(v), color=BLUE, radius=0.07).shift(UP*0.12*(j//5)) for j, v in enumerate(c10)])
        dp = VGroup(Dot(ax2.n2p(3), color=GREEN, radius=0.08), *[Dot(ax2.n2p(1)+UP*0.12*i, color=BLUE, radius=0.06) for i in range(5)], *[Dot(ax2.n2p(-2)+UP*0.12*i, color=ORANGE, radius=0.06) for i in range(4)])
        l1 = VGroup(Text("10-cycle", font_size=26, weight=BOLD), MathTex(r"\lambda_2/\lambda_1=1.618/2=0.81", font_size=26, color=ORANGE)).arrange(DOWN, buff=0.15).next_to(ax1, DOWN, buff=0.5)
        l2 = VGroup(Text("Petersen", font_size=26, weight=BOLD), MathTex(r"\lambda_2/\lambda_1=2/3=0.67", font_size=26, color=GREEN)).arrange(DOWN, buff=0.15).next_to(ax2, DOWN, buff=0.5)
        note = Text("(degree 2 vs 3, so not quite a fair fight — but that is what the number means)", font_size=22, color=MUTED).to_edge(DOWN, buff=0.5)
        self.hold(10, ([Create(ax1), FadeIn(d10), FadeIn(l1)], 2), ([Create(ax2), FadeIn(dp), FadeIn(l2)], 2), ([FadeIn(note)], 1.5))
        self.clear_all()

# ---------------------------------------------------------------- E03S04  Alon-Boppana
class E03S04(BeatScene):
    SCENE_ID = 'E03S04'
    def construct(self):
        h = header("How small can λ₂ be?")
        q = Text("Can cubic graphs with more and more vertices keep λ₂ tiny?  No.", font_size=30).next_to(h, DOWN, buff=0.5)
        self.hold(11, ([FadeIn(h)], 0.8), ([FadeIn(q)], 2))
        ab = card("Alon–Boppana (1980s)", [MathTex(r"\text{for every }\varepsilon>0,\ \text{every large enough cubic graph has a nontrivial }\lambda>2\sqrt2-\varepsilon", font_size=26),
                                           MathTex(r"2\sqrt2\approx2.828", font_size=36, color=YELLOW)], color=YELLOW, width=60).next_to(q, DOWN, buff=0.4)
        self.hold(12, ([FadeIn(ab)], 3))
        self.play(FadeOut(q), ab.animate.scale(0.8).to_edge(RIGHT, buff=0.4).shift(DOWN*0.2), run_time=0.7)
        tree = VGroup()
        def grow(p, ang, depth, L):
            if depth == 0: return
            for da in ([0, 2*PI/3, -2*PI/3] if depth == 4 else [PI/3.2, -PI/3.2]):
                a = ang + da
                qq = p + L*np.array([np.cos(a), np.sin(a), 0])
                tree.add(Line(p, qq, color=TEAL, stroke_width=2), Dot(qq, radius=0.035, color=INK))
                grow(qq, a, depth-1, L*0.55)
        tree.add(Dot(ORIGIN, radius=0.05, color=INK)); grow(ORIGIN, PI/2, 4, 1.1)
        tree.scale(0.85).move_to(LEFT*4.3+DOWN*0.5)
        tl = Text("the 3-regular tree:\nevery cubic graph is a folded copy", font_size=20, color=TEAL, line_spacing=1.1).next_to(tree, DOWN, buff=0.15)
        self.hold(13, ([Create(tree)], 3), ([FadeIn(tl)], 1.5))
        cnt = VGroup(Text("closed walks of length 2t on the tree:", font_size=22),
                     MathTex(r"\text{pairings (Catalan)}\sim4^t\ \times\ \text{directions }2^t\ =\ 8^t", font_size=26),
                     MathTex(r"\text{per step: }\sqrt8=2\sqrt2", font_size=30, color=YELLOW),
                     wrap("a finite graph looks like the tree locally; the number leaks through", 40, 20, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(ab, DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        self.hold(14, ([FadeIn(cnt[0])], 1.5), ([Write(cnt[1])], 3), ([Write(cnt[2])], 2), ([FadeIn(cnt[3])], 2))
        self.clear_all()

# ---------------------------------------------------------------- E03S05  Ramanujan
class E03S05(BeatScene):
    SCENE_ID = 'E03S05'
    def construct(self):
        h = header("Ramanujan graphs")
        t = wrap("A cubic graph whose nontrivial eigenvalues all satisfy |λ| ≤ 2√2 is as well connected as any large cubic graph can be.  Lubotzky, Phillips, Sarnak (1988) named them Ramanujan graphs.", 70, 26).next_to(h, DOWN, buff=0.5)
        self.hold(15, ([FadeIn(h)], 0.8), ([FadeIn(t)], 3))
        triv = defn("trivial eigenvalues", "3 always (all-ones vector). And −3 when the graph is bipartite: +1 on one side, −1 on the other, each vertex sums three opposite signs. Neither counts.", width=60).next_to(t, DOWN, buff=0.4)
        self.hold(16, ([FadeIn(triv)], 3))
        self.play(FadeOut(t), FadeOut(triv), run_time=0.4)
        d1 = defn("Ramanujan graph (cubic)", [MathTex(r"|\lambda|\le2\sqrt2\quad\text{for every eigenvalue other than }3\ (\text{and }-3\text{ if bipartite})", font_size=30)], width=60).next_to(h, DOWN, buff=0.6)
        self.hold(17, ([FadeIn(d1)], 2.5))
        ax = NumberLine(x_range=[-3, 3, 1], length=9, include_numbers=True, color=MUTED).shift(DOWN*1.5)
        r = 2*np.sqrt(2)
        band = Rectangle(width=ax.n2p(r)[0]-ax.n2p(-r)[0], height=0.8, color=YELLOW, fill_opacity=0.15, stroke_width=1).move_to(ax.n2p(0))
        bl = MathTex(r"-2\sqrt2", font_size=30, color=YELLOW).next_to(ax.n2p(-r), UP, buff=0.5); br = MathTex(r"2\sqrt2", font_size=30, color=YELLOW).next_to(ax.n2p(r), UP, buff=0.5)
        dots = VGroup(Dot(ax.n2p(3), color=GREEN, radius=0.1), Dot(ax.n2p(1), color=BLUE, radius=0.1), Dot(ax.n2p(-2), color=ORANGE, radius=0.1))
        ok = Text("Petersen: 1 and −2 are inside. Ramanujan.", font_size=28, color=GREEN).next_to(ax, DOWN, buff=0.6)
        self.hold(18, ([Create(ax), FadeIn(band), FadeIn(bl), FadeIn(br)], 1.5), ([FadeIn(dots)], 1), ([FadeIn(ok)], 1.5))
        self.clear_all()

# ---------------------------------------------------------------- E03S06  First question
class E03S06(BeatScene):
    SCENE_ID = 'E03S06'
    def construct(self):
        h = header("The first question of the project")
        q = card("Question 1", [MathTex(r"\text{Which }P(n,k)\text{ are Ramanujan?}", font_size=40, color=YELLOW),
                                 wrap("compute all 2n eigenvalues, drop the trivial ones, test |λ| ≤ 2√2", 60, 24, MUTED)], color=YELLOW, width=60).next_to(h, DOWN, buff=0.6)
        self.hold(19, ([FadeIn(h)], 0.8), ([FadeIn(q)], 2.5))
        ans = VGroup(Text("First guess: lots of them, maybe all.", font_size=28, color=MUTED),
                     Text("Truth: for each k only finitely many n; only finitely many pairs in total.", font_size=28),
                     MathTex(r"\text{exactly }460\ \text{pairs},\ \text{none with }k>45", font_size=36, color=GREEN),
                     Text("road: complex numbers (ep. 5) → a polynomial (ep. 6) → fractions (ep. 7) → exact arithmetic (ep. 8)", font_size=22, color=MUTED)).arrange(DOWN, buff=0.35).next_to(q, DOWN, buff=0.6)
        self.hold(20, ([FadeIn(ans[0])], 1.5), ([FadeIn(ans[1])], 2), ([Write(ans[2])], 2), ([FadeIn(ans[3])], 2))
        nxt = Text("but first: why this is called a Riemann Hypothesis (episode 4)", font_size=26, color=YELLOW).to_edge(DOWN, buff=0.5)
        self.hold(21, ([FadeIn(nxt)], 1.5))
        self.clear_all()

# ---------------------------------------------------------------- E03S07  Recap
class E03S07(BeatScene):
    SCENE_ID = 'E03S07'
    def construct(self):
        h = header("Recap: what you can now do")
        b = bullets(["explain a random walk as repeated multiplication by A/3",
                     "explain why it converges to uniform and why λ₂ sets the speed",
                     "define spectral gap and expander",
                     "state the Alon–Boppana floor 2√2 and say where it comes from",
                     "state what a Ramanujan graph is, including the trivial eigenvalues",
                     "verify that the Petersen graph is Ramanujan"], font_size=28, width=60).next_to(h, DOWN, buff=0.6)
        self.hold(22, ([FadeIn(h)], 0.8), ([FadeIn(b, lag_ratio=0.2)], 5))
        self.clear_all()
