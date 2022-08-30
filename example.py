from manim import *
# from src.manim_automata.mobjects.manim_determinstic_finite_state_automaton import ManimDeterminsticFiniteAutomaton
# from src.manim_automata.mobjects.manim_non_determinstic_finite_state_automaton import ManimNonDeterminsticFiniteAutomaton
# from manim_automata import *



from src.manim_automata.mobjects.manim_pushdown_automaton import ManimPushDownAutomaton

from src.manim_automata.mobjects.manim_non_determinstic_finite_state_automaton import ManimNonDeterminsticFiniteAutomaton
from src.manim_automata.mobjects.manim_determinstic_finite_state_automaton import ManimDeterminsticFiniteAutomaton

class Test(MovingCameraScene):
    def construct(self):
        
        manim_automaton = ManimNonDeterminsticFiniteAutomaton(xml_file='example_machine.jff', cli=False)
    
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

        # print(manim_automaton.play_string(automaton_input))


        # Play all the animations generate from .play_string()
        for sequence in manim_automaton.play_string(automaton_input):
            # break
            for step in sequence:
                self.play(step, run_time=0.5)
                print(step, len(self.get_mobject_family_members()))
        
                    



class PushDownTest(MovingCameraScene):
    def construct(self):
        manim_pushdown_automaton = ManimPushDownAutomaton(xml_file='pushdown_automaton.jff')
    
        #Adjust camera frame to fit ManimAutomaton in scene
        self.camera.frame_width = manim_pushdown_automaton.width + 10
        self.camera.frame_height = manim_pushdown_automaton.height + 10
        self.camera.frame.move_to(manim_pushdown_automaton)

        #Create an mobject version of input for the manim_automaton
        automaton_input = manim_pushdown_automaton.construct_automaton_input("110011")

        #Position automaton_input on the screen to avoid overlapping.
        automaton_input.shift(LEFT * 2)
        automaton_input.shift(UP * 10)

        self.play(
            DrawBorderThenFill(manim_pushdown_automaton),
            FadeIn(automaton_input)
        )