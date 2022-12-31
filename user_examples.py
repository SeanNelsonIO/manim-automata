from manim import *

from src.manim_automata.mobjects.manim_pushdown_automaton import ManimPushDownAutomaton
from src.manim_automata.mobjects.manim_determinstic_finite_state_automaton import ManimDeterminsticFiniteAutomaton

        

class FiniteStateAutomatonExample(MovingCameraScene):
    def construct(self):
        manim_automaton = ManimDeterminsticFiniteAutomaton(xml_file='manim_automata_examples/example_machine_files/finite_automaton.jff', cli=False)
        
        #Adjust camera frame to fit ManimAutomaton in scene
        self.camera.frame_width = manim_automaton.width + 10
        self.camera.frame_height = manim_automaton.height + 10
        self.camera.frame.move_to(manim_automaton)

        #Create an mobject version of input for the manim_automaton
        automaton_input = manim_automaton.construct_automaton_input("000001")

        #Position automaton_input on the screen to avoid overlapping.
        automaton_input.shift(LEFT * 2)
        automaton_input.shift(UP * 10)

        self.play(
            DrawBorderThenFill(manim_automaton),
            FadeIn(automaton_input)
        )

        for sequence in manim_automaton.play_string(automaton_input):
            self.play(*sequence, run_time=0.5)



class NonFiniteStateAutomatonExample(MovingCameraScene):
    def construct(self):
        manim_automaton = ManimDeterminsticFiniteAutomaton(xml_file='manim_automata_examples/example_machine_files/NFA.jff', cli=False)
        
    
        #Adjust camera frame to fit ManimAutomaton in scene
        self.camera.frame_width = manim_automaton.width + 10
        self.camera.frame_height = manim_automaton.height + 10
        self.camera.frame.move_to(manim_automaton)

        #Create an mobject version of input for the manim_automaton
        automaton_input = manim_automaton.construct_automaton_input("111011")

        #Position automaton_input on the screen to avoid overlapping.
        automaton_input.shift(LEFT * 2)
        automaton_input.shift(UP * 10)

        self.play(
            DrawBorderThenFill(manim_automaton),
            FadeIn(automaton_input)
        )

        for sequence in manim_automaton.play_string(automaton_input):
            self.play(*sequence, run_time=0.5)
