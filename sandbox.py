from enum import auto
from manim import *
# from manim_automata.automata import Automata
# from manim_automata.mobjects.automaton_mobject import ManimAutomaton
# from src.manim-automata import *
from src.manim_automata.mobjects import *
from src.manim_automata.mobjects.automaton_mobject import ManimAutomaton

class CreateCircle(MovingCameraScene):
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

        # self.camera_frame.save_state()

        # state = State()
        automaton = ManimAutomaton()
        # self.play(Create(automaton))

        self.play(
            Create(automaton.shift([-1, -1, 0])), #vector that shifts automaton to centre of scene
            self.camera.frame.animate.scale(.5)
        )

        self.wait()

        