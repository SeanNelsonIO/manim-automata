
from manim import *




# class ManimPushDownAutomaton(FiniteStateAutomaton, VGroup):

#     def __init__(self, json_template=None, xml_file=None, camera_follow=False, animation_style=default_animation_style, **kwargs) -> None:
#         super(FiniteStateAutomaton, self).__init__()

#         self.animation_style = animation_style
#         self.camera_follow = camera_follow
        
#         # default animation style
#         # and allow users to pass in functions that replace some of the functionality such as play_accept..
        
#         super(VGroup, self).__init__(**kwargs)

#         if json_template:
#             self.automaton = FiniteStateAutomaton(json_template==json_template)
#             self.construct_manim_states()
#             self.construct_manim_transitions()
#         elif xml_file:
#             self.process_xml(xml_file)


#         #add manim_states to screen/renderer
#         self.add(*self.states)
#         self.add(*self.transitions)

class ManimPushDownAutomaton(ManimAutomaton):
    def __init__(self, json_template=None, xml_file=None, camera_follow=False, animation_style=..., cli=False, **kwargs) -> None:
        super().__init__(json_template, xml_file, camera_follow, animation_style, cli, **kwargs)