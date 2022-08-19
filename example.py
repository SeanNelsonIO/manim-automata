from manim import *
# from src.manim_automata.mobjects.manim_determinstic_finite_state_automaton import ManimDeterminsticFiniteAutomaton
# from src.manim_automata.mobjects.manim_non_determinstic_finite_state_automaton import ManimNonDeterminsticFiniteAutomaton
from manim_automata import *



# from manim_automata import ManimNonDeterminsticFiniteAutomaton

class Automaton(MovingCameraScene):
    def construct(self):
        manim_automaton = ManimDeterminsticFiniteAutomaton(xml_file='example_machine.jff')
 
        
        manim_state1 = State(
                    "name", 0, 0, True, False,
                    transitions = {
                        "to_state": ["1", "0"],
                        "to_other_state": ["1"]
                    }
                )
        state2 = State(...)

        manim_state1.set_x()
        manim_state1.add_transition()
        manim_state1.remove_transition(state1.get_transition_to_state("to_state"), animate=True) #if animate is True then the method will return an animation sequence of this instruction


        manim_automaton.add_state(
            state1,
            transitions = {"to_state": ["1", "0"],
                        "to_other_state": ["1"]}
        
        )
        manim_automaton.remove_transition("from_state", "to_state")
        manim_automaton.add_transition("from_state", "to_state", ["1", "0"])


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


class Test(MovingCameraScene):
    def construct(self):
        # manim_automaton = ManimAutomaton()

        # self.play(FadeIn(manim_automaton))
        # manim_automaton = ManimNonDeterminsticFiniteAutomaton(xml_file='example_machine.jff', cli=True)
    
        manim_automaton = ManimNonDeterminsticFiniteAutomaton(xml_file='example_machine.jff')


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

        #  # Play all the animations generate from .play_string()
        for sequence in manim_automaton.play_string(automaton_input, automaton_path_name="recorded_path.txt"):
            
            for step in sequence:
                self.play(step, run_time=0.5)






        # self.play(self.camera.frame.animate.move_to(manim_automaton.get_initial_state().circle))
        

        # state1 = ManimState("q0", 0, 0, True, True)

        # self.play(FadeIn(state1))

        # manim_automaton.add_state(
        #     state1,
        #     transitions = {
        #         "to_state_name||id?": ["1", "0"],
        #         "another_to_state": ["0"]
        #     }
        # )

