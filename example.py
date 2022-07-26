from manim import *
# from src.manim_automata.mobjects.automaton_mobject import ManimAutomaton
from manim_automata import *


class Automaton(MovingCameraScene):
    def construct(self):
        manim_automaton = ManimAutomaton(xml_file='example_machine.jff')
        
        #Adjust camera frame to fit ManimAutomaton in scene
        self.camera.frame_width = manim_automaton.width + 10
        self.camera.frame_height = manim_automaton.height + 10
        self.camera.frame.move_to(manim_automaton) 


        #Create an mobject version of input for the manim_automaton
        automaton_input = manim_automaton.construct_automaton_input("110011")

        #Position automaton_input on the screen to avoid overlapping.
        automaton_input.shift(LEFT * 2)
        automaton_input.shift(UP * 10)

        self.play(
                DrawBorderThenFill(manim_automaton),
                FadeIn(automaton_input)
            )

        # Play all the animations generate from .play_string()
        for sequence in manim_automaton.play_string(automaton_input):
            for step in sequence:
                self.play(step, run_time=1)