from manim import *
# from src.manim-automata import *
from src.manim_automata.mobjects import *

class CreateCircle(Scene):
    def construct(self):
        dot_grid = DotGrid()
        # circle = Circle()  # create a circle
        # circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(dot_grid))  # show the circle on screen
        dot_grid.update_dot()
        self.play(Create(dot_grid))  # show the circle on screen