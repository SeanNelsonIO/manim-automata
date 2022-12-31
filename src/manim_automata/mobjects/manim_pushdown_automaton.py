from manim import *

from .manim_non_determinstic_finite_state_automaton import ManimNonDeterminsticFiniteAutomaton
from .manim_state import ManimState, State
from .manim_automaton_input import ManimAutomataInput
from .manim_transition import ManimTransition, ManimPushDownAutomatonTransition

from typing import Union

class ManimPushDownAutomaton(ManimNonDeterminsticFiniteAutomaton):

    stack: list

    def __init__(self, json_template=None, xml_file=None, camera_follow=False, animation_style=None,  **kwargs) -> None:
        super().__init__(json_template, xml_file, camera_follow, animation_style, **kwargs)
        #initialise stack - Z is the bottom stack symbol
        self.stack = ["Z"]

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
        new_transition = ManimPushDownAutomatonTransition(transition_from, transition_to, rules, parent_automaton=self, animation_style=self.animation_style)
        self.transitions.append(new_transition)
        #add the transition to the from_states link list
        transition_from.add_transition_to_state(new_transition)

    def push(self, push_item):
        self.stack.push(push_item)
        return self.stack

    def pop(self):
        return self.stack.pop()

    #pushdown automata can accept if the stack is empty or if it falls on a final state TODO
    #overriden
    def play_string(self, input: Union[str, "ManimAutomataInput"], automaton_path_name: str = None, accept_on_final_state: bool = True) -> list:
        if type(input) is str:
            #create mobject of input string
            self.manim_automata_input = self.construct_automaton_input(input)
            #position the mobject
            self.set_default_position_of_input_string()
            #display manim_automaton_input to the screen
            list_of_animations.append(self.manim_animations.animate_display_input(self.manim_automata_input))
        else: self.manim_automata_input = input #if input is already an instance of ManimAutomataInput

        #run the input through the machine, returning a history of what happend
        history = self.run_input_through_automaton(input)

        list_of_animations = self.generate_history_animations(history)

                    # if self.check_automaton_result([state_pointer]): #if the automaton has an active accepting state
                    #     list_of_animations.append(self.generate_accept_animations()) #THIS IS GENERATED BEFORE ALL BRANCHES HAVE FINISHED
                    # else: #if there is no final state then the machine is not accepted.
                    #     list_of_animations.append(self.generate_reject_animations())

        return list_of_animations


    #overriden
    def automaton_step(self, token: str, state_pointer: State) -> tuple:
        next_states = [] #stores all of the next states that can be jumped to
        transitions = [] #store the transitions that transition from current to next states.
        
        #go through each transition of this state
        state_transitions = state_pointer.get_transitions()
        for transition in state_transitions:


            #check if any transition's rules match the input token
            for rule in transition.rules: #Iterate through the transtion's read options
                if rule.read_symbol == token.tex_string or rule.read_symbol == r"\epsilon":
                    next_states.append(transition.transition_to)
                    transitions.append(transition)

                    #some code for stack too - TODO


        if len(next_states) != 0:
            return True, next_states, transitions #the token matches the transition's input

        return False, next_states, transitions #There are no other transitions/ reachable next states given the token

    #nondeterministic pushdown automata have difference stacks - maybe a later requirement? Probably

    #the only difference in history is that we have a stack
    #check to see if the transition matches the input token
    #if not - fail
    #if true then execute the transition rule
    #update stack

    # transition.rules has each rule

    #change the way we generate animations / add the animations needed for stack, push and pop
    #need to probably animate which transition rule it takes too


    



class PushDownAutomatonRule():

    read_symbol: str
    pop: str
    push: list[str]

    def __init__(self, read_symbol: str, pop: str, push: str, empty_transition: str = r"\epsilon") -> None:
        if read_symbol is None:
            self.read_symbol = empty_transition
        else:
            self.read_symbol = read_symbol

        self.pop = pop
        self.push = []

        if push is None:
            self.push = empty_transition
        else:
            for push_item in push:
                self.push.append(push_item)

    def __str__(self) -> str:
        formatted_push_string = ''.join(str(x) for x in self.push)
        return f'{self.read_symbol},{self.pop};{formatted_push_string}'





    #every transition we pop one item of the stack,

    #if there is an 'a' and we pop a Z then we push YZ, first the Z and then the Y
