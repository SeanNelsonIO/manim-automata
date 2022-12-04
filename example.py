from itertools import count
from manim import *
# from src.manim_automata.mobjects.manim_determinstic_finite_state_automaton import ManimDeterminsticFiniteAutomaton
# from src.manim_automata.mobjects.manim_non_determinstic_finite_state_automaton import ManimNonDeterminsticFiniteAutomaton
# from manim_automata import *

from manim import FadeToColor
from numpy import broadcast

from src.manim_automata.mobjects.manim_pushdown_automaton import ManimPushDownAutomaton

from src.manim_automata.mobjects.manim_non_determinstic_finite_state_automaton import ManimNonDeterminsticFiniteAutomaton
from src.manim_automata.mobjects.manim_determinstic_finite_state_automaton import ManimDeterminsticFiniteAutomaton

# import os, psutil
import gc

# class Test(MovingCameraScene):
#     def construct(self):
        
#         manim_automaton = ManimNonDeterminsticFiniteAutomaton(xml_file='example_machine.jff', cli=False)
        
    
#         #Adjust camera frame to fit ManimAutomaton in scene
#         self.camera.frame_width = manim_automaton.width + 10
#         self.camera.frame_height = manim_automaton.height + 10
#         self.camera.frame.move_to(manim_automaton)

#         #Create an mobject version of input for the manim_automaton
#         automaton_input = manim_automaton.construct_automaton_input("110011")

#         #Position automaton_input on the screen to avoid overlapping.
#         automaton_input.shift(LEFT * 2)
#         automaton_input.shift(UP * 10)

#         self.play(
#             DrawBorderThenFill(manim_automaton),
#             FadeIn(automaton_input)
#         )

        
#         broken_manim_automaton = ManimNonDeterminsticFiniteAutomaton(xml_file='example_machine.jff', cli=False)

#         # #Create an mobject version of input for the manim_automaton
#         broken_automaton_input = broken_manim_automaton.construct_automaton_input("110011")

        

        # #Position automaton_input on the screen to avoid overlapping.
        # broken_automaton_input.shift(LEFT * 2)
        # broken_automaton_input.shift(UP * 10)

        # self.play(
        #     DrawBorderThenFill(broken_manim_automaton),
        #     FadeIn(broken_automaton_input)
        # )

        # print(manim_automaton.play_string(automaton_input))
        # process = psutil.Process(os.getpid())

        # print(process.memory_info().rss)
        # Play all the animations generate from .play_string()
        
        


        # count1 = 0
        # interested1 = []
        # for list1 in manim_automaton.play_string(automaton_input):
        #     for element in list1:
        #         if isinstance(element, FadeToColor):
        #             count1 = count1 + 1
        #             interested1.append(element)
        

        # count2 = 0
        # interested2 = []
        # for list2 in broken_manim_automaton.play__string(broken_automaton_input):
        #     for element in list2:
        #         if isinstance(element, FadeToColor):
        #             count2 = count2 + 1
        #             interested2.append(element)

        # print("count: ", count1, count2)
        # print(len(gc.get_objects(generation=None)))
        # broken_manim_automaton.play__string(broken_automaton_input) #this is causing issue, even though it is not being played.
        #think it might be due to the size , or how many objects it is producing????
        # all_mobjects = [self] + list(it.chain(*sub_families))

        # for step in interested2:
        #     # print("broken", len(broken_manim_automaton.submobjects), len(self.get_mobject_family_members()))
        #     self.play(step, run_time=0.5)
        #     print("step: ", step)
        #     print("gc: ", len(gc.get_objects(generation=None)))



        # for sequence in manim_automaton.play_string(automaton_input):
        #     # break
        #     for step in sequence:
        #         # cal = process.memory_info().rss / 1000000
        #         # print("Mbytes: ", cal)
        #         print(step, len(self.mobjects))
        #         self.play(step, run_time=0.5)
                
        
                    
class PushDownTest(MovingCameraScene):
    def construct(self):
        manim_pushdown_automaton = ManimPushDownAutomaton(xml_file='example_machines/pushdown_automaton.jff')
    
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

        for sequence in manim_pushdown_automaton.play_string(automaton_input):
            # print(sequence)
            try:
                self.play(*sequence, run_time=0.5)
            except Exception as e:
                print(e)


class FiniteStateMachineTest(MovingCameraScene):
    def construct(self):
        manim_automaton = ManimDeterminsticFiniteAutomaton(xml_file='example_machines/NFA.jff', cli=False)
        
    
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
            try:
                self.play(*sequence, run_time=0.5)
            except Exception as e:
                print(e)

                

# class NonFiniteStateMachineTest(MovingCameraScene):
#     def construct(self):
#         manim_automaton = ManimNonDeterminsticFiniteAutomaton(xml_file='example_machine.jff', cli=False)
        
    
#         #Adjust camera frame to fit ManimAutomaton in scene
#         self.camera.frame_width = manim_automaton.width + 10
#         self.camera.frame_height = manim_automaton.height + 10
#         self.camera.frame.move_to(manim_automaton)

#         #Create an mobject version of input for the manim_automaton
#         automaton_input = manim_automaton.construct_automaton_input("110011")

#         #Position automaton_input on the screen to avoid overlapping.
#         automaton_input.shift(LEFT * 2)
#         automaton_input.shift(UP * 10)

#         self.play(
#             DrawBorderThenFill(manim_automaton),
#             FadeIn(automaton_input)
#         )

#         for sequence in manim_automaton.play_string(automaton_input):
#             # print(sequence)
#             self.play(*sequence, run_time=0.5)
#             for step in sequence:
#                 self.play(step, run_time=0.5)