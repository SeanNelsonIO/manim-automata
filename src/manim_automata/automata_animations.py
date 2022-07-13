from manim import VMobject, VGroup
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


# class AutomataStep(Animation):
#     def __init__(self, manim_automaton: VGroup, token: str, **kwargs):
#         self.token = token
#         super().__init__(manim_automaton, **kwargs)

#     def step(self):
#         Indicate(token)


# class AutomataRun(Animation): #for creating our own animations
#     pass




# class PlayString():

#     def __init__(self, mobject_automaton: VMObject, input_string: str) -> None:
#         manim_tokens = []
#         spacing = 0
#         for token in string:
#             manim_tokens.append(Text(token, font_size=40).shift((DOWN*2) + [spacing, 0, 0] + (LEFT * 3)))
#             spacing = spacing + 0.5

#         #display string
#         for token in manim_tokens:
#             self.add(token)
            
#         #Points to the current state
#         state_pointer = self.manim_automaton.get_initial_state()
#         #animate the automaton going through the sequence
#         for i, token in enumerate(manim_tokens):
#             #check if it is last token
#             if i == len(manim_tokens)-1:
#                 #animate for the final state
#                 pass
            
#             step_result, next_state, transition_id = self.manim_automaton.automaton.step(token, state_pointer)
#             #get transition with transition id
#             transition = self.manim_automaton.get_manim_transition(transition_id)

#             self.animate_step(transition, token, state_pointer, step_result)
            
#             #if successful point to the next state
#             if step_result is True:
#                 #move state_pointer to next state
#                 if next_state:
#                     state_pointer = next_state
#             else: #if step fails then stop play process early as the string is not accepted
#                 return False
            
        
#         #check that the current state_pointer is a final state
#         if state_pointer.final:
#             return True
#         else:
#             return False



# def play_string(self, string: str, **kwargs):
            
        
#         #create manim objects of tokens

#         # if len(string) > 5:
#         #     string = string + "..." #need to dramatically improve this
            
        
