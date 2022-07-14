from enum import auto
from hmac import trans_36
from typing import Text
from manim import *
from manim_automata.automata import Transition
from src.manim_automata.mobjects import *
from src.manim_automata.mobjects.automaton_mobject import ManimAutomaton, ManimTransition, ManimAutomataInput
from src.manim_automata.mobjects.automaton_animation import AnimateStep





class Automata(MovingCameraScene):
    def construct(self):
        #need a way of specifying the automaton (build API??)
        manim_automaton = ManimAutomaton()
        manim_automata_input = ManimAutomataInput("010101")
        # setup cameara
        self.play(
            self.camera.frame.animate.move_to(manim_automaton)
        )

        # self.play(FadeIn(manim_automaton))
        self.play(DrawBorderThenFill(manim_automaton.scale(0.7)))
        self.play(DrawBorderThenFill(manim_automata_input.scale(0.9)))


    

        for sequence in manim_automaton.play_string(manim_automata_input):
            # self.play(*sequence)
            print(sequence)
            for step in sequence:
                self.play(step, run_time=0.5)