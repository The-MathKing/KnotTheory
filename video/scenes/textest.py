from lib import *
class TexTest(Scene):
    def construct(self):
        t = MathTex(r"D_k(u)=\bigl(7+4u\,T_k(u)\bigr)^2-8\bigl(2u+2T_k(u)\bigr)^2", font_size=48)
        s = Text("Where Optimal Networks Stop Existing", font_size=40, weight=BOLD).next_to(t, UP, buff=1)
        g, _ = petersen(5, 2, R_out=1.6, R_in=0.8, center=DOWN*2)
        self.add(t, s, g)
