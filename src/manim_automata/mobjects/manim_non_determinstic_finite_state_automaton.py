
from manim import *

from .manim_automaton import ManimAutomaton
from .manim_state import ManimState, State
from .manim_automaton_input import ManimAutomataInput
from .manim_transition import ManimTransition

from typing import Union

import json

class ManimNonDeterminsticFiniteAutomaton(ManimAutomaton):

    nda_builder = False

    def __init__(self, json_template=None, xml_file=None, camera_follow=False, animation_style=None, cli=False, **kwargs) -> None:
        if animation_style is None:
            super().__init__(json_template, xml_file, camera_follow, cli=cli, **kwargs)
        else:
            super().__init__(json_template, xml_file, camera_follow, animation_style, cli=cli, **kwargs)

        
        if cli is True: #if cli exist display options to user
            self.cli.display_nda_options()
            if self.cli.nda_option == 0: #check the settings of the cli (what the user wants to do)
                self.nda_builder = True


    def initialisation_animation(self, input: Union[str, "ManimAutomataInput"]) -> list:
        """This method generates the animations that initialise the machine graphically.
            The method specfically positions and animates the input string and highlights
            the initial state"""

        if type(input) is str:
            #create mobject of input string
            self.manim_automata_input = self.construct_automaton_input(input_string)
            #position the mobject
            self.set_default_position_of_input_string()
            #display manim_automaton_input to the screen
            list_of_animations.append(FadeIn(self.manim_automata_input))
        else: self.manim_automata_input = input #if input is already an instance of ManimAutomataInput
        
        #stores a list of animations that is returned to scene
        list_of_animations = []
        #Points to the current state
        state_pointer = self.get_initial_state()
        #Highlight current state with yellow
        list_of_animations.append([FadeToColor(state_pointer, color=YELLOW)])

        return list_of_animations

    def step(self, manim_transition: ManimTransition, token: "Tex", state_pointer: State, result: bool) -> list:
        #creates a list of animations for the step
        list_of_step_animations = []
        if manim_transition == None: #there is no possible transition
            list_of_step_animations.append(
                token.animate.set_color(RED) # create a custom animation to signify result
            )
        else:
            #move camera with every state, using the state_pointer
            if self.camera_follow is True: #need someway to replace
                # list_of_step_animations.append(
                #     self.camera.frame.animate.move_to(self.get_manim_state(state_pointer)).scale(1)
                # )
                pass

            #Animation that highlights the transition - Green for True and red otherwise
            list_of_step_animations.append(
                manim_transition.animate_transition(result)
            )

        
        return list_of_step_animations


    def generate_next_state_options(self, state_pointer, transition_ids):
        options = {}
        for index, transition_id in enumerate(transition_ids):
            transition = self.get_transition_by_id(int(transition_id))
            next_state = transition.transition_to
            options[index] = (f"{state_pointer.name} --> {next_state.name}", transition)

        return options

    def export_recorded_path_to_file(self):
        with open("recorded_path.txt", "w") as fp:
            json.dump(self.recorded_path, fp)

    def load_recorded_path_from_file(self, file_name):
        with open(f"{file_name}", "r") as fp:
            path_list = json.load(fp)
            #check that the type is a list
            if type(path_list) is list:
                return path_list
        return None


    def play_sequence(self, token, state_pointers, list_of_animations, predetermined_transition: "ManimTransition" = None) -> list[State]:
        next_states = []
        for state_pointer in state_pointers: #look at each state and calculate the steps that state can take.

            step_result, next_neighbour_states, transition_ids = self.automaton_step(token, state_pointer, determinstic=False) #simulates the machine
            
            if self.nda_builder:
                path_options = self.generate_next_state_options(state_pointer, transition_ids)
                print(f"Token: {token.tex_string}")
                user_choice = self.cli.display_dictionary_options(path_options)
                transition = path_options[user_choice][1] #get transition given user choice
                
                #record the transition choice
                self.recorded_path.append((transition.transition_from.name, transition.transition_to.name))

                transition_ids = [transition.id] #There is now only one transition that the state_pointer can take
                next_neighbour_states = [transition.transition_to] #There is now only one state that the state_pointer can go to

            #if step result is False then there are no more steps, check for final state and highlight state pointer as finished.
            for transition_id in transition_ids:
                transition = self.get_transition_by_id(int(transition_id))
                list_of_animations.append(self.step(transition, token, state_pointer, step_result)) # self.step returns a list of animations for that step
            
            #if successful point to the next state
            if step_result is True:
                if len(next_neighbour_states) > 0:
                    list_of_animations.append([FadeToColor(state_pointer, color=BLUE)])
                    list_of_animations.append([FadeToColor(x, color=YELLOW) for x in next_neighbour_states])

                    next_states = next_states + next_neighbour_states

            if len(next_neighbour_states) == 0: #if there are no more states or transitions left
                if self.check_automaton_result(state_pointers): #if the automaton has an active accepting state
                    list_of_animations.append(self.generate_accept_animations())
                else: #if there is no final state then the machine is not accepted.
                    list_of_animations.append(self.generate_reject_animations())

        return next_states
              
   
    def play_string(self, input: Union[str, "ManimAutomataInput"], automaton_path_name: str = None) -> list:
        """
        parameters:
            automaton_path: provides a single path used to navigate through the nda, 
            the purpose of this is to allow the user to animate a single path through
            the nda instead of animating all of the branches that are created by the nda.
        """
            
        # example_structure = [("q0", "q1")]
        # if this transition does not exist or the token does not match 
        # then return error with the number of the tuple in the list
        if automaton_path_name: # The nda will animate the predetermined path from the user
            automaton_path = self.load_recorded_path_from_file(automaton_path_name)
            return self.play_automaton_path(input, automaton_path) #create animations to do with given path
        elif self.nda_builder: # Stores the path of of a single branch within the nda
            self.recorded_path = []

        list_of_animations = self.initialisation_animation(input)

        initial_state = self.get_initial_state()
        state_pointers = [initial_state] # Keeps track of all the states that are activated

        # Animate the automaton going through the sequence
        for i, token in enumerate(self.manim_automata_input.tokens):
            
            #check if it is last token
            if i == len(self.manim_automata_input.tokens)-1:
                #animate for the final state
                pass
                
            list_of_animations.append([FadeToColor(token, color=YELLOW)]) #highlights the current token

            state_pointers = self.play_sequence(token, state_pointers, list_of_animations) #generate the animations for this token sequence

            list_of_animations.append([token.animate.set_opacity(0.5)]) #animates that the token has been used
        
        #export the recorded path so the user can use it again without using nda builder
        if self.nda_builder:
            self.export_recorded_path_to_file()

        return list_of_animations

    def generate_accept_animations(self):
        list_of_accept_animations = []

        text = Tex("ACCEPTED", color=GREEN, font_size=100)
        text.set_x(self.manim_automata_input.get_x())
        text.set_y(self.manim_automata_input.get_y())

        list_of_accept_animations.append(Transform(self.manim_automata_input, text))
        list_of_accept_animations.append(FadeToColor(self, color=GREEN))

        return list_of_accept_animations

    def generate_reject_animations(self):
        list_of_reject_animations = []

        text = Tex("REJECTED", color=RED, font_size=100)
        text.set_x(self.manim_automata_input.get_x())
        text.set_y(self.manim_automata_input.get_y())

        list_of_reject_animations.append(Transform(self.manim_automata_input, text))
        list_of_reject_animations.append(FadeToColor(self, color=RED))

        return list_of_reject_animations


    def play_automaton_path(self, input, automaton_path: list[tuple]):
        list_of_animations = self.initialisation_animation(input)

        initial_state = self.get_initial_state()
        
        if initial_state.name != automaton_path[0][0]: #check that the start of the path matches the initial state
            pass #display erro

        state_pointer = initial_state # Keeps track of all the states that are activated

        for token, path_transition in zip(self.manim_automata_input.tokens, automaton_path):
            current_state = state_pointer
            current_state_transitions = current_state.transitions
            if current_state.name == path_transition[0]: #if the current state matches the path_transition's from-state
                #check that the path_transition to-state exists and is valid
                for transition in current_state_transitions:
                    if transition.transition_to.name == path_transition[1]:
                        #check the transition has a read symbol that matches the input token
                        if transition.check_transition_read_symbols(token):
                            #generate animations
                            list_of_animations.append([FadeToColor(token, color=YELLOW)]) #highlights the current token
                            state_pointer = self.play_predetermined_sequence(token, state_pointer, list_of_animations, predetermined_transition=transition)
                            list_of_animations.append([token.animate.set_opacity(0.5)]) #animates that the token has been used
                            break
                        else:
                            return False #transition does not have a matching read_symbol for the given token

        #check if the language was accepted by the automaton
        if self.check_automaton_result([state_pointer]): #if the automaton has an active accepting state
            list_of_animations.append(self.generate_accept_animations())
        else: #if there is no final state then the machine is not accepted.
            list_of_animations.append(self.generate_reject_animations())

        return list_of_animations
   

    #Improving play string method
    def play_predetermined_sequence(self, token, state_pointer, list_of_animations, predetermined_transition: "ManimTransition" = None) -> list[State]:
        # step_result, next_neighbour_states, transition_ids = self.automaton_step(token, state_pointer, determinstic=False) #simulates the machine
        step_result = True #determined by the calling function
        list_of_animations.append(self.step(predetermined_transition, token, state_pointer, step_result))

        next_neighbour_state = predetermined_transition.transition_to

        list_of_animations.append([FadeToColor(state_pointer, color=BLUE)])
        list_of_animations.append([FadeToColor(next_neighbour_state, color=YELLOW)])

        next_state = next_neighbour_state

        return next_state
            