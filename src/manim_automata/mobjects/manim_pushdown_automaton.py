
from manim import *

from .manim_determinstic_finite_state_automaton import ManimDeterminsticFiniteAutomaton
from .manim_state import ManimState, State
from .manim_automaton_input import ManimAutomataInput
from .manim_transition import ManimTransition

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

class ManimPushDownAutomaton(ManimDeterminsticFiniteAutomaton):

    stack: list

    def __init__(self, json_template=None, xml_file=None, camera_follow=False, animation_style=None, **kwargs) -> None:
        super().__init__(json_template, xml_file, camera_follow, animation_style, **kwargs)
        #initialise stack
        self.stack = []

    #override ManimAutomaton method
    def construct_transitions(self, transitions):
        # counts the number of transitions between two states
        transition_counter = {}
        # for transition in self.automaton.transitions:
        #if 2 or more transitions exist between states then this will merge them together in one transition.
        for transition in transitions:
            """put from and to states into tuple to be used as
            dictionary key."""
            state_key = (transition['from'], transition['to'])
            
            transition_group = transition_counter.setdefault(state_key, [])#if key doesn't exist then create new key list pair

            #if symbol already exists then skip
            # if transition['read'] not in transition_group:
            #     transition_group.append(transition['read']) #append transition read value to transition[state_key]

            #create a pushdown automaton rule
            rule = PushDownAutomatonRule(transition['read'], transition['pop'], transition['push'])

            transition_group.append(rule)

        #avoids creating multiple manim_transitions.
        #Creates one manim_transition with multiple rules
        for state_key in transition_counter:
            rules = transition_counter[state_key]

            transition_from = self.get_state_by_id(int(state_key[0]))
            transition_to = self.get_state_by_id(int(state_key[1]))

            self.construct_transition(transition_from, transition_to, rules)

    def construct_transition(self, transition_from: ManimState, transition_to: ManimState, rules: list):
        new_transition = ManimTransition(transition_from, transition_to, rules, parent_automaton=self, animation_style=self.animation_style)
        self.transitions.append(new_transition)
        #add the transition to the from_states link list
        transition_from.add_transition_to_state(new_transition)

    def push(self, push_item):
        self.stack.push(push_item)
        return self.stack

    def pop(self):
        return self.stack.pop()



class PushDownAutomatonRule():

    read_symbol: str
    pop: str
    push: list[str]

    def __init__(self, read_symbol: str, pop: str, push: str) -> None:
        if read_symbol is None:
            self.read_symbol = r"\lambda"
        else:
            self.read_symbol = read_symbol

        self.pop = pop
        self.push = []

        if push is None:
            self.push = r"\lambda"
        else:
            for push_item in push:
                self.push.append(push_item)

    def __str__(self) -> str:

        formatted_push_string = ''.join(str(x) for x in self.push)
        return f'{self.read_symbol};{self.pop};{formatted_push_string}'





    #every transition we pop one item of the stack,

    #if there is an 'a' and we pop a Z then we push YZ, first the Z and then the Y
