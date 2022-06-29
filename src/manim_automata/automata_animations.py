from manim import *
from manim.animation.animation import Animation
# from manim_automata.automata.xml_parser import parse_xml_file
# from manim_automata.automata.automata import deterministic_finite_automaton

# class CreateCircle(Scene):
#     def construct(self):
#         circle = Circle()  # create a circle
#         circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
#         self.play(Create(circle))  # show the circle on screen


# def initialise_automaton():
#     #testing functions
#     json_dictionary = parse_xml_file('testmachine.jff')
#     if not isinstance(json_dictionary, dict):
#         exit()


#     states = json_dictionary["structure"]["automaton"]["state"]
#     transitions = json_dictionary["structure"]["automaton"]["transition"]

#     # print(transitions)

#     deterministic_finite_automaton = deterministic_finite_automaton(states=states, transitions=transitions)




class AutomataRun(Animation):
    pass