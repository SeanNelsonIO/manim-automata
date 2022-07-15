from curses.textpad import rectangle
from enum import auto
from manim import *
from manim_automata.automata import Transition
from src.manim_automata.mobjects import *
from src.manim_automata.mobjects.automaton_mobject import ManimAutomaton, ManimTransition, ManimAutomataInput
from src.manim_automata.mobjects.automaton_animation import AnimateStep





class Automata(MovingCameraScene):
    def construct(self):
        #need a way of specifying the automaton (build API??)
        manim_automaton = ManimAutomaton()


        
        


        width_of_scene = manim_automaton.width
        height = manim_automaton.height
        rectangle = Rectangle(width=width_of_scene, height=height, color=ORANGE)
        #set centre of rectangle to the centre of manim_automaton
        rectangle.set_x(manim_automaton.get_x())
        rectangle.set_y(manim_automaton.get_y())
        print("rectangle:", rectangle.get_x(), rectangle.get_y())
        
        # setup cameara
        self.play(
            self.camera.frame.animate.move_to(manim_automaton)
        )

        self.camera.frame.set_width(width_of_scene + 2)
        self.camera.frame.set_height(height + 10)
        # self.play(FadeIn(manim_automaton))
        self.play(DrawBorderThenFill(manim_automaton))
        self.play(DrawBorderThenFill(rectangle))
        # self.play(DrawBorderThenFill(manim_automata_input.scale(1)))
        

        # first_state = manim_automaton.manim_states[list(manim_automaton.manim_states.keys())[0]]
        # first_state.set_x(0)
        # first_state.set_y(0)
        # print(manim_automata_input.get_y(), first_state.get_y(), first_state.state.name)
        
        input_string = "010110"

        for sequence in manim_automaton.play_string("010110"):
            # self.play(*sequence)
            for step in sequence:
                self.play(step, run_time=0.5)