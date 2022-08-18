from manim import *

from .manim_automaton import ManimAutomaton
from .manim_state import ManimState, State
from .manim_automaton_input import ManimAutomataInput
from .manim_transition import ManimTransition

from typing import Union


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

    def play_string(self, input: Union[str, "ManimAutomataInput"], automaton_path: list = None) -> list:
        """
        parameters:
            automaton_path: provides a single path used to navigate through the nda, 
            the purpose of this is to allow the user to animate a single path through
            the nda instead of animating all of the branches that are created by the nda.
        """
        #stores the path of of a single branch within the nda
        if self.nda_builder:
            self.recorded_path = []

        list_of_animations = self.initialisation_animation(input)

        initial_state = self.get_initial_state()
        state_pointers = [initial_state] #keeps track of all the states that are activated

        #animate the automaton going through the sequence
        for i, token in enumerate(self.manim_automata_input.tokens):
            
            #check if it is last token
            if i == len(self.manim_automata_input.tokens)-1:
                #animate for the final state
                pass
                
            next_states = []

            # [ManimAutomataInput.highlight_token(token, self.animation_style]
            list_of_animations.append([FadeToColor(token, color=YELLOW)]) #highlights the current token

            for state_pointer in state_pointers: #look at each state and calculate the steps that state can take.

                step_result, next_neighbour_states, transition_ids = self.automaton_step(token, state_pointer, determinstic=False) #simulates the machine
                
                if self.nda_builder:
                    path_options = self.generate_next_state_options(state_pointer, transition_ids)
                    print(f"Token #: {i}")
                    user_choice = self.cli.display_dictionary_options(path_options)
                    transition = path_options[user_choice][1] #get transition given user choice

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
                        text = Tex("ACCEPTED", color=GREEN, font_size=100)
                        text.set_x(token.get_x())
                        text.set_y(token.get_y())

                        list_of_animations.append([Transform(self.manim_automata_input, text)])
                        list_of_animations.append([FadeToColor(self, color=GREEN)])

                    else: #if there is no final state then the machine is not accepted.
                        text = Tex("REJECTED", color=RED, font_size=100)
                        text.set_x(token.get_x())
                        text.set_y(token.get_y())

                        list_of_animations.append([Transform(self.manim_automata_input, text)])
                        list_of_animations.append([FadeToColor(self, color=RED)])

                    return list_of_animations

            list_of_animations.append([token.animate.set_opacity(0.5)]) #animates that the token has been used

            state_pointers = next_states
        
        #export the recorded path so the user can use it again without using nda builder
        if self.nda_builder:
            self.export_recorded_path_to_file()

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
        pass