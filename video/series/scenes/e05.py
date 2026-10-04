from lib import *

def lam(t, k, sign):
    a, b = 2*np.cos(t), 2*np.cos(k*t)
    return (a+b)/2 + sign*np.sqrt(((a-b)/2)**2 + 1)

def cplane(center, L=3.2, rng=2.2):
    pl = NumberPlane(x_range=[-rng, rng, 1], y_range=[-rng, rng, 1], x_length=L, y_length=L,
                     background_line_style={"stroke_color": GRID, "stroke_width": 1}, axis_config={"stroke_color": MUTED}).move_to(center)
    return pl

# ---------------------------------------------------------------- E05S01  Complex numbers
class E05S01(BeatScene):
    SCENE_ID = 'E05S01'
    def construct(self):
        t = title_card("Episode 5", "Complex numbers, roots of unity, and how symmetry splits the matrix")
        self.hold(1, ([FadeIn(t)], 1.5), ([FadeOut(t)], 0.5),
                  ([FadeIn(header("Complex numbers as points in the plane"))], 0.8))
        pl = cplane(LEFT*3.5+DOWN*0.6)
        d1 = defn("complex number", "A point (a, b) in the plane, written a + b i.  a = real part (horizontal), b = imaginary part (vertical).  i itself is the point (0, 1).", width=46, font_size=22, title_size=26).to_edge(RIGHT, buff=0.4).shift(UP*1.6)
        pt = Dot(pl.c2p(2, 1), color=YELLOW, radius=0.08); ptl = MathTex("2+i", font_size=28, color=YELLOW).next_to(pt, UR, buff=0.1)
        ii = Dot(pl.c2p(0, 1), color=BLUE, radius=0.08); il = MathTex("i", font_size=28, color=BLUE).next_to(ii, LEFT, buff=0.1)
        self.play(FadeIn(pl), run_time=1)
        self.play(FadeIn(d1), FadeIn(pt), FadeIn(ptl), FadeIn(ii), FadeIn(il), run_time=1.5)
        self.wait(1)
        ops = VGroup(MathTex(r"(2+i)+(1+3i)=3+4i", font_size=30),
                     MathTex(r"(2+i)(1+3i)=2+6i+i+3i^2=2+7i-3=-1+7i", font_size=30, color=GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(d1, DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        self.hold(2, ([Write(ops[0])], 2), ([Write(ops[1])], 3))
        self.play(FadeOut(ops), run_time=0.4)
        geo = idea("multiplication is rotation", "Each complex number has a distance from 0 and an angle. Multiplying multiplies distances and adds angles.\ni: distance 1, angle 90°.  i·i: angle 180° = the point −1.  So i² = −1.", width=46, font_size=21, title_size=26).next_to(d1, DOWN, buff=0.3).to_edge(RIGHT, buff=0.4)
        arc = Arc(radius=0.9, start_angle=0, angle=PI/2, color=BLUE, arc_center=pl.c2p(0, 0))
        m1 = Dot(pl.c2p(-1, 0), color=RED, radius=0.08); m1l = MathTex("i^2=-1", font_size=28, color=RED).next_to(m1, DL, buff=0.1)
        arc2 = Arc(radius=0.9, start_angle=PI/2, angle=PI/2, color=RED, arc_center=pl.c2p(0, 0))
        self.hold(3, ([FadeIn(geo)], 2), ([Create(arc)], 1), ([Create(arc2), FadeIn(m1), FadeIn(m1l)], 1.5))
        self.play(FadeOut(geo), FadeOut(pt), FadeOut(ptl), FadeOut(arc), FadeOut(arc2), FadeOut(m1), FadeOut(m1l), run_time=0.4)
        circ = Circle(radius=pl.c2p(1, 0)[0]-pl.c2p(0, 0)[0], color=YELLOW, stroke_width=2).move_to(pl.c2p(0, 0))
        th = 0.9
        p = Dot(pl.c2p(np.cos(th), np.sin(th)), color=YELLOW, radius=0.08)
        ln = Line(pl.c2p(0, 0), p.get_center(), color=YELLOW); al = Arc(radius=0.5, start_angle=0, angle=th, color=YELLOW, arc_center=pl.c2p(0, 0))
        tl = MathTex(r"\theta", font_size=26, color=YELLOW).move_to(pl.c2p(0.75*np.cos(th/2), 0.75*np.sin(th/2)))
        e = VGroup(MathTex(r"\cos\theta+i\sin\theta\ =:\ e^{i\theta}", font_size=34),
                   MathTex(r"\text{the point on the unit circle at angle }\theta", font_size=24, color=MUTED),
                   MathTex(r"e^{i\theta}e^{i\phi}=e^{i(\theta+\phi)}\quad(\text{angles add})", font_size=32, color=GREEN)).arrange(DOWN, buff=0.3).next_to(d1, DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        self.hold(4, ([Create(circ), FadeIn(p), Create(ln), Create(al), FadeIn(tl)], 1.5), ([Write(e[0]), FadeIn(e[1])], 2.5), ([Write(e[2])], 2))
        self.clear_all()

# ---------------------------------------------------------------- E05S02  Roots of unity
class E05S02(BeatScene):
    SCENE_ID = 'E05S02'
    def construct(self):
        h = header("Roots of unity")
        pl = cplane(LEFT*3.5+DOWN*0.6, rng=1.4)
        R = pl.c2p(1, 0)[0]-pl.c2p(0, 0)[0]; c = pl.c2p(0, 0)
        circ = Circle(radius=R, color=MUTED, stroke_width=2).move_to(c)
        def roots(n, col=YELLOW):
            return VGroup(*[Dot(c + R*np.array([np.cos(2*PI*j/n), np.sin(2*PI*j/n), 0]), color=col, radius=0.08) for j in range(n)])
        n = 8
        rt = roots(n)
        labs = VGroup(*[MathTex(f"\\zeta^{{{j}}}" if j else "1", font_size=24, color=YELLOW).move_to(c + 1.25*R*np.array([np.cos(2*PI*j/n), np.sin(2*PI*j/n), 0])) for j in range(n)])
        d1 = defn("n-th roots of unity", "Divide the unit circle into n equal arcs starting at 1. ζ = the point at angle 2π/n. The others are ζ², ζ³, …, and ζⁿ = 1.", width=46, font_size=22, title_size=26).to_corner(UR, buff=0.3).shift(DOWN*0.55)
        self.hold(5, ([FadeIn(h), FadeIn(pl), Create(circ)], 1), ([FadeIn(rt, lag_ratio=0.1), FadeIn(labs, lag_ratio=0.1)], 2.5), ([FadeIn(d1)], 2))
        ex = VGroup(MathTex(r"n=4:\ 1,\ i,\ -1,\ -i", font_size=28), MathTex(r"n=6:\ \text{hexagon corners}", font_size=28),
                    MathTex(r"n=5:\ \text{angles }0^\circ,72^\circ,144^\circ,216^\circ,288^\circ", font_size=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(d1, DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        r4 = roots(4, BLUE); r6 = roots(6, GREEN); r5 = roots(5, ORANGE)
        self.hold(6, ([FadeOut(labs), Transform(rt, r4), FadeIn(ex[0])], 1.5), ([Transform(rt, r6), FadeIn(ex[1])], 1.5), ([Transform(rt, r5), FadeIn(ex[2])], 1.5))
        self.play(FadeOut(ex), Transform(rt, roots(8)), run_time=0.8)
        j = 1
        pj = c + R*np.array([np.cos(2*PI*j/8), np.sin(2*PI*j/8), 0]); pm = c + R*np.array([np.cos(2*PI*j/8), -np.sin(2*PI*j/8), 0])
        dj = Dot(pj, color=TEAL, radius=0.1); dm = Dot(pm, color=TEAL, radius=0.1)
        lj = MathTex(r"\zeta^{j}", font_size=26, color=TEAL).next_to(dj, UR, buff=0.05); lm = MathTex(r"\zeta^{-j}", font_size=26, color=TEAL).next_to(dm, DR, buff=0.05)
        ds = Dot(c + np.array([2*R*np.cos(2*PI*j/8), 0, 0]), color=GREEN, radius=0.1); ls = MathTex(r"\zeta^{j}+\zeta^{-j}", font_size=24, color=GREEN).next_to(ds, DOWN, buff=0.1)
        v1 = Arrow(c, pj, buff=0, color=TEAL, stroke_width=3); v2 = Arrow(pj, ds.get_center(), buff=0, color=TEAL, stroke_width=3)
        key = card("the formula we use everywhere", [MathTex(r"\zeta^{\,j}+\zeta^{-j}=2\cos\tfrac{2\pi j}{n}", font_size=34, color=GREEN),
                                                   wrap("mirror images across the axis: imaginary parts cancel, real parts add", 44, 20, MUTED)], color=GREEN, width=44, title_size=26).next_to(d1, DOWN, buff=0.3).to_edge(RIGHT, buff=0.3)
        self.hold(7, ([FadeIn(dj), FadeIn(dm), FadeIn(lj), FadeIn(lm)], 1.5), ([GrowArrow(v1), GrowArrow(v2), FadeIn(ds), FadeIn(ls)], 2), ([FadeIn(key)], 2.5))
        chk = VGroup(MathTex(r"n=4,j=1:\ i+(-i)=0=2\cos90^\circ\ \checkmark", font_size=24), MathTex(r"n=6,j=1:\ 2\cos60^\circ=1\ \checkmark", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(key, DOWN, buff=0.2).to_edge(RIGHT, buff=0.4)
        self.hold(8, ([FadeIn(chk[0])], 1.5), ([FadeIn(chk[1])], 1.5))
        self.clear_all()

# ---------------------------------------------------------------- E05S03  Cycle eigenvectors
class E05S03(BeatScene):
    SCENE_ID = 'E05S03'
    def construct(self):
        h = header("The cycle: eigenvectors from roots of unity")
        n = 8; c = LEFT*3.6+DOWN*0.7
        pts = ring_points(n, R=1.9, center=c)
        g, dots, lines, labs = simple_graph(pts, [(i, (i+1) % n) for i in range(n)], dot_r=0.1, labels=[str(i) for i in range(n)],
                                           label_dir=[(p-c)/np.linalg.norm(p-c) for p in pts])
        rule = MathTex(r"(Ax)_i=x_{i-1}+x_{i+1}", font_size=32).to_edge(RIGHT, buff=0.6).shift(UP*2.2)
        self.hold(9, ([FadeIn(h), Create(lines), FadeIn(dots), FadeIn(labs)], 1.5), ([Write(rule)], 2))
        vec = MathTex(r"x_i=\zeta^{\,ij}\quad(1,\ \zeta^{j},\ \zeta^{2j},\ \dots)", font_size=30, color=YELLOW).next_to(rule, DOWN, buff=0.4)
        vl = VGroup(*[MathTex(f"\\zeta^{{{i}j}}" if i > 1 else ("\\zeta^{j}" if i == 1 else "1"), font_size=20, color=YELLOW).move_to(c + (p-c)*0.72) for i, p in enumerate(pts)])
        comp = VGroup(MathTex(r"(Ax)_i=\zeta^{(i-1)j}+\zeta^{(i+1)j}=\zeta^{ij}\bigl(\zeta^{-j}+\zeta^{j}\bigr)", font_size=28),
                      MathTex(r"=2\cos\tfrac{2\pi j}{n}\cdot\zeta^{ij}=2\cos\tfrac{2\pi j}{n}\cdot x_i", font_size=30, color=GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(vec, DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        self.hold(10, ([Write(vec), FadeIn(vl)], 2), ([Write(comp[0])], 3), ([Write(comp[1])], 2.5))
        self.play(FadeOut(comp), FadeOut(vec), FadeOut(vl), run_time=0.4)
        res = card("eigenvalues of the n-cycle", [MathTex(r"\lambda_j=2\cos\frac{2\pi j}{n},\quad j=0,\dots,n-1", font_size=34, color=GREEN),
                                                  MathTex(r"n=4:\ 2,\ 0,\ -2,\ 0\quad(\text{episode 2})", font_size=26),
                                                  MathTex(r"n=10:\ 2,\ 1.618,\ 0.618,\ -0.618,\ -1.618,\ -2,\ \dots", font_size=26)], color=GREEN, width=46).next_to(rule, DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        self.hold(11, ([FadeIn(res)], 3))
        why = idea("why it worked", "Shifting every index by one multiplies this vector by ζʲ. Shifting is the symmetry of the cycle. A vector the symmetry merely scales is well-behaved under every matrix that respects the symmetry.", width=46, font_size=22).next_to(res, DOWN, buff=0.3).to_edge(RIGHT, buff=0.4)
        why.move_to(res)
        self.hold(12, ([FadeOut(res), FadeIn(why)], 1.5), ([Rotate(VGroup(lines, dots), angle=2*PI/n, about_point=c)], 1.5))
        self.clear_all()

# ---------------------------------------------------------------- E05S04  Two rings, 2x2 blocks
class E05S04(BeatScene):
    SCENE_ID = 'E05S04'
    def construct(self):
        h = header("Two rings and the 2 × 2 blocks")
        n = 8; c = LEFT*3.6+DOWN*0.7
        g, d = petersen(n, 3, R_out=2.0, R_in=0.95, center=c, dot_r=0.08)
        ul = VGroup(MathTex(r"p\zeta^{(i-1)j}", font_size=20, color=BLUE).move_to(c + (d['upos'][7]-c)*1.22),
                    MathTex(r"p\zeta^{ij}", font_size=20, color=BLUE).move_to(c + (d['upos'][0]-c)*1.2),
                    MathTex(r"p\zeta^{(i+1)j}", font_size=20, color=BLUE).move_to(c + (d['upos'][1]-c)*1.22))
        vl = VGroup(MathTex(r"q\zeta^{ij}", font_size=18, color=ORANGE).move_to(c + (d['vpos'][0]-c)*1.0 + RIGHT*0.45),
                    MathTex(r"q\zeta^{(i+k)j}", font_size=18, color=ORANGE).move_to(c + (d['vpos'][3]-c)*1.0 + LEFT*0.7 + DOWN*0.15),
                    MathTex(r"q\zeta^{(i-k)j}", font_size=18, color=ORANGE).move_to(c + (d['vpos'][5]-c)*1.0 + RIGHT*0.7 + DOWN*0.15))
        ul0 = MathTex("u_i", font_size=18, color=MUTED).move_to(c + (d['upos'][0]-c)*1.0 + RIGHT*0.3 + DOWN*0.05)
        try_ = MathTex(r"\text{try: }x_{u_i}=p\,\zeta^{ij},\quad x_{v_i}=q\,\zeta^{ij}", font_size=30).to_edge(RIGHT, buff=0.4).shift(UP*2.2)
        self.hold(13, ([FadeIn(h), FadeIn(g)], 1), ([Write(try_), FadeIn(ul), FadeIn(vl)], 2))
        outer = VGroup(MathTex(r"\text{at }u_i:\ p\zeta^{(i-1)j}+p\zeta^{(i+1)j}+q\zeta^{ij}", font_size=26),
                       MathTex(r"=\zeta^{ij}\bigl(\alpha_j\,p+q\bigr),\quad \alpha_j=2\cos\tfrac{2\pi j}{n}", font_size=28, color=BLUE)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(try_, DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        self.hold(14, ([Indicate(VGroup(d['u'][0], d['u'][1], d['u'][7], d['v'][0]), color=YELLOW)], 1.5), ([Write(outer[0])], 2.5), ([Write(outer[1])], 2.5))
        inner = VGroup(MathTex(r"\text{at }v_i:\ q\zeta^{(i-k)j}+q\zeta^{(i+k)j}+p\zeta^{ij}", font_size=26),
                       MathTex(r"=\zeta^{ij}\bigl(p+\beta_j\,q\bigr),\quad \beta_j=2\cos\tfrac{2\pi jk}{n}", font_size=28, color=ORANGE)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(outer, DOWN, buff=0.35).to_edge(RIGHT, buff=0.4)
        self.hold(15, ([Indicate(VGroup(d['v'][0], d['v'][3], d['v'][5], d['u'][0]), color=YELLOW)], 1.5), ([Write(inner[0])], 2.5), ([Write(inner[1])], 2.5))
        self.play(FadeOut(outer), FadeOut(inner), FadeOut(try_), run_time=0.4)
        blk = card("the block M_j", [MathTex(r"\begin{pmatrix}p\\q\end{pmatrix}\ \mapsto\ \begin{pmatrix}\alpha_j p+q\\ p+\beta_j q\end{pmatrix}=\underbrace{\begin{pmatrix}\alpha_j&1\\1&\beta_j\end{pmatrix}}_{M_j}\begin{pmatrix}p\\q\end{pmatrix}", font_size=30),
                                     MathTex(r"M_j\binom pq=\lambda\binom pq\ \Rightarrow\ A\,x=\lambda\,x", font_size=28, color=GREEN)], color=GREEN, width=46).to_edge(RIGHT, buff=0.4).shift(UP*0.8)
        self.hold(16, ([FadeIn(blk)], 3.5))
        split = VGroup(MathTex(r"2n\times2n\ \longrightarrow\ n\ \text{blocks }2\times2", font_size=32, color=YELLOW),
                       MathTex(r"\alpha_j:\ \text{outer ring};\quad \beta_j:\ \text{inner ring (step }k);\quad 1:\ \text{spokes}", font_size=24, color=MUTED)).arrange(DOWN, buff=0.25).next_to(blk, DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        self.hold(17, ([Write(split[0])], 2), ([FadeIn(split[1])], 2))
        self.clear_all()

# ---------------------------------------------------------------- E05S05  Petersen from five blocks
class E05S05(BeatScene):
    SCENE_ID = 'E05S05'
    def construct(self):
        h = header("Worked example: the Petersen spectrum from five blocks")
        setup = MathTex(r"n=5,\ k=2:\quad \alpha_j=2\cos(72j)^\circ,\quad \beta_j=2\cos(144j)^\circ", font_size=32).next_to(h, DOWN, buff=0.4)
        self.hold(18, ([FadeIn(h)], 0.8), ([Write(setup)], 2.5))
        rows = VGroup()
        def row(j, a, b, tr, det, ev, col):
            return MathTex(rf"j={j}:\ \alpha={a},\ \beta={b};\quad \text{{tr}}={tr},\ \det={det}\ \Rightarrow\ \lambda={ev}", font_size=28, color=col)
        r0 = VGroup(row(0, "2", "2", "4", "3", r"3,\ 1", GREEN), MathTex(r"M_0=\begin{pmatrix}2&1\\1&2\end{pmatrix}\ \text{(episode 2)}", font_size=26, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(setup, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        self.hold(19, ([Write(r0[0])], 2.5), ([FadeIn(r0[1])], 1.5))
        r1 = VGroup(row(1, "0.618", "-1.618", "-1", "-2", r"1,\ -2", YELLOW),
                    MathTex(r"\lambda^2+\lambda-2=(\lambda-1)(\lambda+2)=0", font_size=26, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(r0, DOWN, buff=0.3).to_edge(LEFT, buff=0.6)
        self.hold(20, ([Write(r1[0])], 3), ([FadeIn(r1[1])], 2))
        gold = MathTex(r"2\cos72^\circ=\varphi-1,\quad 2\cos144^\circ=-\varphi,\quad (\varphi-1)(-\varphi)=-1", font_size=26, color=MUTED).next_to(r1, DOWN, buff=0.3).to_edge(LEFT, buff=0.6)
        self.hold(21, ([Write(gold)], 2.5))
        r2 = VGroup(row(2, "-1.618", "0.618", "-1", "-2", r"1,\ -2", YELLOW),
                    MathTex(r"j=3,4:\ \text{mirror images of }j=2,1\ \Rightarrow\ 1,-2\ \text{each}", font_size=26, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(gold, DOWN, buff=0.3).to_edge(LEFT, buff=0.6)
        self.hold(22, ([Write(r2[0])], 2.5), ([FadeIn(r2[1])], 2))
        tot = card("total", [MathTex(r"\{3,1\}\cup\{1,-2\}\times4\ =\ 3^{1},\ 1^{5},\ (-2)^{4}\ \checkmark", font_size=32, color=GREEN)], color=GREEN, width=50).next_to(r2, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        self.hold(23, ([FadeIn(tot)], 2.5))
        self.clear_all()

# ---------------------------------------------------------------- E05S06  Curves sampled
class E05S06(BeatScene):
    SCENE_ID = 'E05S06'
    def construct(self):
        h = header("Two curves, sampled")
        ev = MathTex(r"\lambda_\pm=\frac{\alpha+\beta}{2}\pm\sqrt{\Bigl(\frac{\alpha-\beta}{2}\Bigr)^2+1}\qquad(\text{quadratic formula on }\lambda^2-\text{tr}\,\lambda+\det)", font_size=30).next_to(h, DOWN, buff=0.4)
        self.hold(24, ([FadeIn(h)], 0.8), ([Write(ev)], 3))
        sub = MathTex(r"t\ \text{continuous}:\ \alpha=2\cos t,\ \beta=2\cos kt\ \Rightarrow\ \text{two curves in }t,\ \text{depending on }k\text{ only}", font_size=28, color=YELLOW).next_to(ev, DOWN, buff=0.3)
        self.hold(25, ([Write(sub)], 3))
        self.play(FadeOut(ev), sub.animate.next_to(h, DOWN, buff=0.3), run_time=0.6)
        k = 3
        ax = Axes(x_range=[0, 2*PI, PI/2], y_range=[-3.5, 3.5, 1], x_length=11, y_length=4.6,
                  axis_config={"include_tip": False, "color": MUTED}, y_axis_config={"include_numbers": True}).shift(DOWN*0.9)
        cp = ax.plot(lambda t: lam(t, k, 1), x_range=[0, 2*PI, 0.01], color=BLUE)
        cm = ax.plot(lambda t: lam(t, k, -1), x_range=[0, 2*PI, 0.01], color=ORANGE)
        r = 2*np.sqrt(2)
        hp = DashedLine(ax.c2p(0, r), ax.c2p(2*PI, r), color=YELLOW); hm = DashedLine(ax.c2p(0, -r), ax.c2p(2*PI, -r), color=YELLOW)
        klab = MathTex("k=3", font_size=32, color=MUTED).to_corner(UR).shift(LEFT*0.5+DOWN*1.0)
        nt = ValueTracker(10)
        def samples():
            nn = int(nt.get_value()); vg = VGroup()
            for j in range(nn):
                t = 2*PI*j/nn
                for s, col in ((1, BLUE), (-1, ORANGE)):
                    y = lam(t, k, s)
                    bad = abs(y) > r and j != 0 and not (nn % 2 == 0 and j == nn//2)
                    vg.add(Dot(ax.c2p(t, y), radius=0.06, color=RED if bad else col))
            return vg
        pts = always_redraw(samples)
        nlab = always_redraw(lambda: MathTex(f"n={int(nt.get_value())}", font_size=32).next_to(klab, DOWN))
        self.hold(26, ([Create(ax), FadeIn(klab)], 1.5), ([Create(cp), Create(cm)], 2.5), ([Create(hp), Create(hm)], 1),
                  ([FadeIn(pts), FadeIn(nlab)], 1), ([nt.animate.set_value(32)], 6), ([nt.animate.set_value(40)], 3))
        msg = Text("curves fixed by k; sampling finer with n; so for each k only finitely many n avoid the forbidden regions", font_size=22, color=YELLOW).to_edge(DOWN, buff=0.3)
        self.hold(27, ([FadeIn(msg)], 2))
        self.clear_all()

# ---------------------------------------------------------------- E05S07  Recap
class E05S07(BeatScene):
    SCENE_ID = 'E05S07'
    def construct(self):
        h = header("Recap: what you can now do")
        b = bullets(["add and multiply complex numbers; multiplication as rotation",
                     "define the n-th roots of unity; show ζʲ + ζ⁻ʲ = 2cos(2πj/n)",
                     "show ζ^{ij} is an eigenvector of the cycle with eigenvalue 2cos(2πj/n)",
                     "derive the block M_j for P(n,k) with α_j, β_j on the diagonal",
                     "recompute the Petersen spectrum from the five blocks",
                     "explain the picture: two fixed curves sampled at n points"], font_size=28, width=64).next_to(h, DOWN, buff=0.6)
        self.hold(28, ([FadeIn(h)], 0.8), ([FadeIn(b, lag_ratio=0.2)], 5))
        self.clear_all()
