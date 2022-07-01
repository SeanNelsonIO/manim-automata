from manim import *
# from src.manim-automata import *
from src.manim_automata.mobjects import *

class CreateCircle(Scene):
    def construct(self):
        # dot_grid = DotGrid()
        # circle = Circle()  # create a circle
        # circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        # self.play(Create(dot_grid))  # show the circle on screen
        # dot_grid.update_dot()
        # self.play(Create(dot_grid))  # show the circle on screen

        for x in range(-7, 8):
            for y in range(-4, 5):
                self.add(Dot(np.array([x, y, 0]), color=DARK_GREY))


        state = State()
        self.play(Create(state))
        self.wait()