"""Shared setup for every episode scene: TeX through tectonic, palette, beat
timing, and a few layout helpers for explanatory cards."""
import json, os, sys, textwrap
from manim import *
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)            # video/series
AUDIO = os.path.join(ROOT, 'audio')

os.environ['PATH'] = os.path.join(ROOT, 'bin') + os.pathsep + os.environ['PATH']
_PRE = r"""
\usepackage[english]{babel}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mathrsfs}
\usepackage{xcolor}
"""
config.tex_template = TexTemplate(tex_compiler="pdflatex", output_format=".pdf", preamble=_PRE)
# one TeX scratch directory per render process: parallel renders otherwise race on
# identical snippets (same hash) in the shared media/Tex directory
config.tex_dir = os.path.join(ROOT, 'media', 'Tex', f'p{os.getpid()}')
os.makedirs(config.tex_dir, exist_ok=True)

BG      = "#0f1117"
INK     = "#e8e8ec"
MUTED   = "#8b90a0"
BLUE    = "#58a6ff"
YELLOW  = "#f2cc60"
RED     = "#ff7b72"
GREEN   = "#56d364"
PURPLE  = "#bc8cff"
ORANGE  = "#ffa657"
TEAL    = "#39c5cf"
GRID    = "#2a2f3a"
PANEL   = "#181c26"

config.background_color = BG
Text.set_default(font="Helvetica Neue", color=INK)
MathTex.set_default(color=INK)
Tex.set_default(color=INK)

_DUR = json.load(open(os.path.join(AUDIO, 'durations.json'))) if os.path.exists(os.path.join(AUDIO, 'durations.json')) else {}

class BeatScene(Scene):
    """Each beat: start its narration clip, run the given animations, then hold
    until the clip ends."""
    SCENE_ID = None
    def _start(self, i):
        key = f"{self.SCENE_ID}_{i:02d}"
        dur = _DUR.get(key, {}).get('dur', 6.0)
        wav = os.path.join(AUDIO, key + '.wav')
        if os.path.exists(wav):
            self.add_sound(wav)
        return dur
    def beat(self, i, *anims, run_time=None, pad=0.5, lag_ratio=0.0):
        dur = self._start(i)
        t0 = self.renderer.time
        if anims:
            rt = run_time if run_time is not None else min(max(1.5, dur * 0.4), 5.0)
            self.play(*anims, run_time=rt, lag_ratio=lag_ratio)
        rest = dur + pad - (self.renderer.time - t0)
        if rest > 0:
            self.wait(rest)
        return dur
    def hold(self, i, *anim_groups, pad=0.5):
        """anim_groups: list of (animations, run_time) played in sequence inside
        the narration window; the remainder of the clip is held.  An empty
        animation list with a run_time is a pause."""
        dur = self._start(i)
        t0 = self.renderer.time
        for anims, rt in anim_groups:
            if anims:
                self.play(*anims, run_time=rt)
            else:
                self.wait(rt)
        rest = dur + pad - (self.renderer.time - t0)
        if rest > 0:
            self.wait(rest)
        return dur
    def clear_all(self, rt=0.7):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=rt)

# ---------------------------------------------------------------- layout helpers
def title_card(text, sub=None, size=54):
    t = Text(text, font_size=size, weight=BOLD)
    if sub:
        s = Text(sub, font_size=30, color=MUTED).next_to(t, DOWN, buff=0.4)
        return VGroup(t, s)
    return VGroup(t)

def wrap(text, width=48, font_size=28, color=INK, align=LEFT, line_spacing=1.0):
    """Multi-line Text wrapped at `width` characters."""
    lines = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, width) or [""])
    return Text("\n".join(lines), font_size=font_size, color=color, line_spacing=line_spacing)

def card(title, body, color=YELLOW, width=48, font_size=26, title_size=30, bg=PANEL, pad=0.35):
    """A titled panel: definition / example / idea.  `body` is a string (wrapped)
    or a list of mobjects arranged vertically."""
    t = Text(title, font_size=title_size, weight=BOLD, color=color)
    if isinstance(body, str):
        b = wrap(body, width, font_size)
    else:
        b = VGroup(*body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    inner = VGroup(t, b).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    box = RoundedRectangle(corner_radius=0.15, width=inner.width + 2*pad, height=inner.height + 2*pad,
                           fill_color=bg, fill_opacity=1.0, stroke_color=color, stroke_width=2)
    box.move_to(inner)
    return VGroup(box, inner)

def defn(term, body, **kw):
    return card("Definition: " + term, body, color=BLUE, **kw)

def example(title, body, **kw):
    return card("Example: " + title, body, color=GREEN, **kw)

def idea(title, body, **kw):
    return card("Idea: " + title, body, color=YELLOW, **kw)

def bullets(items, font_size=26, color=INK, width=50, buff=0.18):
    g = VGroup()
    for it in items:
        if isinstance(it, str):
            g.add(wrap("•  " + it, width, font_size, color))
        else:
            g.add(it)
    return g.arrange(DOWN, aligned_edge=LEFT, buff=buff)

def header(text, size=36, color=INK):
    return Text(text, font_size=size, weight=BOLD, color=color).to_edge(UP, buff=0.45)

def clamp(m, margin=0.4):
    half = config.frame_width / 2 - margin
    if m.get_right()[0] > half: m.shift(LEFT * (m.get_right()[0] - half))
    if m.get_left()[0] < -half: m.shift(RIGHT * (-half - m.get_left()[0]))
    return m

def fit(m, max_w=12.8, max_h=7.0):
    if m.width > max_w: m.scale_to_fit_width(max_w)
    if m.height > max_h: m.scale_to_fit_height(max_h)
    return m

# ---------------------------------------------------------------- graphs
def petersen(n, k, R_out=2.6, R_in=1.35, center=ORIGIN, dot_r=0.07,
             outer_col=BLUE, inner_col=ORANGE, spoke_col=MUTED, edge_w=2.2):
    us, vs = [], []
    for i in range(n):
        th = PI/2 + 2*PI*i/n
        us.append(center + R_out*np.array([np.cos(th), np.sin(th), 0]))
        vs.append(center + R_in*np.array([np.cos(th), np.sin(th), 0]))
    outer = VGroup(*[Line(us[i], us[(i+1)%n], color=outer_col, stroke_width=edge_w) for i in range(n)])
    inner = VGroup(*[Line(vs[i], vs[(i+k)%n], color=inner_col, stroke_width=edge_w) for i in range(n)])
    spokes = VGroup(*[Line(us[i], vs[i], color=spoke_col, stroke_width=edge_w*0.8) for i in range(n)])
    ud = VGroup(*[Dot(p, radius=dot_r, color=INK) for p in us])
    vd = VGroup(*[Dot(p, radius=dot_r, color=INK) for p in vs])
    g = VGroup(outer, inner, spokes, ud, vd)
    return g, dict(u=ud, v=vd, outer=outer, inner=inner, spokes=spokes, upos=us, vpos=vs)

def simple_graph(points, edges, dot_r=0.12, edge_col=MUTED, edge_w=3, fill="#2b2f3a", labels=None, label_size=28, label_dir=None):
    """Points: list of np arrays. edges: list of (i,j). Returns (VGroup, dots, lines, labels)."""
    lines = VGroup(*[Line(points[a], points[b], color=edge_col, stroke_width=edge_w) for a, b in edges])
    dots = VGroup(*[Dot(p, radius=dot_r, color=fill, stroke_color=INK, stroke_width=2) for p in points])
    labs = VGroup()
    if labels:
        for i, (p, l) in enumerate(zip(points, labels)):
            d = label_dir[i] if label_dir else UP
            labs.add(MathTex(l, font_size=label_size).next_to(p, d, buff=0.15))
    return VGroup(lines, dots, labs), dots, lines, labs

def ring_points(m, R=1.6, center=ORIGIN, start=PI/2):
    return [center + R*np.array([np.cos(start+2*PI*i/m), np.sin(start+2*PI*i/m), 0]) for i in range(m)]

WHITE_V = "#2b2f3a"
def vdot(p, filled=False, r=0.13):
    return Dot(p, radius=r, color=BLUE if filled else WHITE_V, stroke_color=INK, stroke_width=2)

def force_seq(scene, dots, order, rt=0.5):
    for a, b in order:
        arr = Arrow(dots[a].get_center(), dots[b].get_center(), buff=0.15, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        scene.play(GrowArrow(arr), run_time=rt*0.5)
        scene.play(dots[b].animate.set_color(BLUE), FadeOut(arr), run_time=rt*0.5)

def int_matrix(rows, scale=0.6, h_buff=0.75, v_buff=0.6, **kw):
    return IntegerMatrix(rows, h_buff=h_buff, v_buff=v_buff, **kw).scale(scale)

def adjacency(n_vertices, edges):
    A = [[0]*n_vertices for _ in range(n_vertices)]
    for a, b in edges:
        A[a][b] = A[b][a] = 1
    return A

def ring_labels(d, which='u', center=ORIGIN, factor=1.15, tangent=0.0, font_size=22, color=None, prefix=None):
    """Labels u_i / v_i for a petersen() dict, placed at `factor` times the ring radius,
    shifted `tangent` units along the ring so they do not sit on a spoke."""
    pos = d['upos'] if which == 'u' else d['vpos']
    col = color or (BLUE if which == 'u' else ORANGE)
    pre = prefix or which
    g = VGroup()
    for i, p in enumerate(pos):
        r = p - center
        t = np.array([-r[1], r[0], 0]); t = t/np.linalg.norm(t) if np.linalg.norm(t) else t
        g.add(MathTex(f"{pre}_{{{i}}}", font_size=font_size, color=col).move_to(center + r*factor + t*tangent))
    return g
