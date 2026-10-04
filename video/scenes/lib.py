"""Shared setup for every scene: TeX through tectonic, palette, beat timing."""
import json, os, sys
from manim import *

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
AUDIO = os.path.join(ROOT, 'audio')

# --- TeX: this machine has only tectonic; bin/pdflatex is a wrapper around it.
os.environ['PATH'] = os.path.join(ROOT, 'bin') + os.pathsep + os.environ['PATH']
_PRE = r"""
\usepackage[english]{babel}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mathrsfs}
\usepackage{xcolor}
"""
config.tex_template = TexTemplate(tex_compiler="pdflatex", output_format=".pdf", preamble=_PRE)

# --- palette (dark, math-channel look)
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

config.background_color = BG
Text.set_default(font="Helvetica Neue", color=INK)
MathTex.set_default(color=INK)
Tex.set_default(color=INK)

_DUR = json.load(open(os.path.join(AUDIO, 'durations.json'))) if os.path.exists(os.path.join(AUDIO, 'durations.json')) else {}

class BeatScene(Scene):
    """Each beat: start its narration clip, run the given animations, then hold
    until the clip ends. `pad` seconds of silence are added after the clip."""
    SCENE_ID = None
    def beat(self, i, *anims, run_time=None, pad=0.6, lag_ratio=0.0):
        key = f"{self.SCENE_ID}_{i:02d}"
        dur = _DUR.get(key, {}).get('dur', 6.0)
        wav = os.path.join(AUDIO, key + '.wav')
        if os.path.exists(wav):
            self.add_sound(wav)
        t0 = self.renderer.time
        if anims:
            rt = run_time if run_time is not None else min(max(1.5, dur * 0.5), 6.0)
            self.play(*anims, run_time=rt, lag_ratio=lag_ratio)
        elapsed = self.renderer.time - t0
        rest = dur + pad - elapsed
        if rest > 0:
            self.wait(rest)
        return dur

    def hold(self, i, *anim_groups, pad=0.6):
        """Like beat, but anim_groups is a list of (animations, run_time) played
        in sequence inside the narration window; remainder is held."""
        key = f"{self.SCENE_ID}_{i:02d}"
        dur = _DUR.get(key, {}).get('dur', 6.0)
        wav = os.path.join(AUDIO, key + '.wav')
        if os.path.exists(wav):
            self.add_sound(wav)
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

def title_card(text, sub=None, size=54):
    t = Text(text, font_size=size, weight=BOLD)
    if sub:
        s = Text(sub, font_size=30, color=MUTED).next_to(t, DOWN, buff=0.4)
        return VGroup(t, s)
    return VGroup(t)

def petersen(n, k, R_out=2.6, R_in=1.35, center=ORIGIN, dot_r=0.07,
             outer_col=BLUE, inner_col=ORANGE, spoke_col=MUTED, edge_w=2.2):
    """Return (VGroup, dict) for P(n,k): dict has 'u','v' dot lists and edge lists."""
    import numpy as np
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

def clamp(m, margin=0.4):
    """Shift a mobject horizontally so it stays inside the 16:9 frame."""
    half = config.frame_width / 2 - margin
    if m.get_right()[0] > half: m.shift(LEFT * (m.get_right()[0] - half))
    if m.get_left()[0] < -half: m.shift(RIGHT * (-half - m.get_left()[0]))
    return m
