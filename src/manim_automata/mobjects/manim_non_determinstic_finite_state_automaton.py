
from manim import *

from .manim_automaton import ManimAutomaton
from .manim_state import ManimState, State
from .manim_automaton_input import ManimAutomataInput
from .manim_transition import ManimTransition

from typing import Union

import json

import itertools

class ManimNonDeterminsticFiniteAutomaton(ManimAutomaton):

    nda_builder = False

    def __init__(self, json_template=None, xml_file=None, camera_follow=False, animation_style=None, cli=False, **kwargs) -> None:
        if animation_style is None:
            super().__init__(json_template, xml_file, camera_follow, cli=cli, **kwargs)
        else:
            super().__init__(json_template, xml_file, camera_follow, animation_style, cli=cli, **kwargs)

        
        if cli: #if cli exist display options to user
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


    def generate_next_state_options(self, state_pointer, transitions):
        options = {}
        for index, transition in enumerate(transitions):
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


    #parent function that plays are the branches in "parallel"
    def play__refactor_string(self, input: Union[str, "ManimAutomataInput"], automaton_path_name: str = None) -> list:
        """
        parameters:
            automaton_path: provides a single path used to navigate through the nda, 
            the purpose of this is to allow the user to animate a single path through
            the nda instead of animating all of the branches that are created by the nda.
        """
        # if this transition does not exist or the token does not match 
        # then return error with the number of the tuple in the list
        if automaton_path_name: # The nda will animate the predetermined path from the user
            automaton_path = self.load_recorded_path_from_file(automaton_path_name)
            return self.play_automaton_path(input, automaton_path) #create animations to do with given path
        elif self.nda_builder: # Stores the path of of a single branch within the nda
            self.recorded_path = []

        self.list_of_animations = self.initialisation_animation(input)

        initial_state = self.get_initial_state()
        
        initial_branch = Branch(initial_state)

        self.all_branches = [initial_branch] #stores all the branches produced by non-determinism
        #need a branch to start with
        
        current_branches = self.all_branches
        # Animate the automaton going through the sequence
        for i, token in enumerate(self.manim_automata_input.tokens):
            self.list_of_animations.append([FadeToColor(token, color=YELLOW)]) #highlights the current token

            current_branches = self.play_branches(token, current_branches)
            
            self.list_of_animations.append([token.animate.set_opacity(0.5)]) #animates that the token has been used
        
        #once the tokens have ended, check to see if there are any alive branches
        #that end on a final state, if the nda accepts.
        accepted = False
        for branch in self.all_branches:
            if branch.alive is True:
                #check if the state_pointer is a final state
                if branch.state_pointer.final is True:
                    self.list_of_animations.append(self.generate_accept_animations())
                    accepted = True
                    break

        if accepted is False:
            self.list_of_animations.append(self.generate_reject_animations())
           

        #export the recorded path so the user can use it again without using nda builder
        if self.nda_builder:
            self.export_recorded_path_to_file()

        return self.list_of_animations

    def pick_transition(self, state_pointer, transitions):
        path_options = self.generate_next_state_options(state_pointer, transitions)
        user_choice = self.cli.display_dictionary_options(path_options)
        transition = path_options[user_choice][1] #get transition given user choice

        return [transition.transition_to], [transition]

    def play_branches(self, token, current_branches) -> list["Branch"]:
        active_branches = []
        for branch in current_branches: #loop though each branch and run one step
            state_pointer = branch.state_pointer

            result, next_states, transitions = self.automaton_step(token, state_pointer)

            if self.nda_builder: #if nda_builder, only choose one path
                next_states, transitions = self.pick_transition(state_pointer, transitions)
           
            # self.generate_animation_sequence(result, next_states, transitions, list_of_animations)
            self.play_sequence(token, result, state_pointer, next_states, transitions)

            if result is False: #branch wasn't able to transition given a token, therefore language is rejected for branch.
                branch.reject()
        
            new_branches = branch.step_through(transitions) #assign new state_pointer to current branch and create divergent branches(if any)
            active_branches = active_branches + new_branches # add any new branches to active branches
            self.all_branches = self.all_branches + new_branches

        return active_branches

    def play_refactor_sequence(self, token, result, state_pointer, next_states, transitions):
        #if step result is False then there are no more steps, check for final state and highlight state pointer as finished.
        for transition in transitions:
            self.list_of_animations.append(self.step(transition, token, state_pointer, result)) #self.step returns a list of animations for that step
        
        #if successful point to the next state
        if result is True:
            if len(next_states) > 0:
                #Broken TODO
                self.list_of_animations.append([state_pointer.animate.set_color(color=BLUE)])
                # print([FadeToColor(state_pointer, color=BLUE)])
                # self.list_of_animations.append([FadeToColor(next_states[0], color=YELLOW)]) 
                # self.list_of_animations.append([FadeToColor(x, color=YELLOW) for x in next_states])

    def play_sequence(self, token, state_pointers, list_of_animations, predetermined_transition: "ManimTransition" = None) -> list[State]:
        next_states = []
        for state_pointer in state_pointers: #look at each state and calculate the steps that state can take.

            step_result, next_neighbour_states, transitions = self.automaton_step(token, state_pointer) #simulates the machine
            
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
            for transition in transitions:
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
        

class Branch():

    id_iter = itertools.count()
    # recorded_path: list #records the path/history of the branch TODO
    # state_pointer: State #keeps track of the current state

    stack: list #pushdown automaton stack, each branch has its own stack

    def __init__(self, state_pointer, stack: list = None, recorded_path: list = None) -> None:
        self.id = next(self.id_iter)
        self.alive = True
        self.stack = stack

        if recorded_path is None:
            self.recorded_path = []
        else: self.recorded_path = recorded_path #the branch was a passed history from parent Branch

        self.state_pointer = state_pointer #stores the state that the branch is currently on

    
    def step_through(self, transitions) -> list["Branch"]: #checks to see if branch diverges
        new_branches = [] #stores the new divergent branches
        #pick a state to continue this branch
        if len(transitions) > 0:
            chosen_transition = transitions.pop()
            self.state_pointer = chosen_transition.transition_to
            self.recorded_path.append((chosen_transition.transition_from.name, chosen_transition.transition_to.name))
            new_branches.append(self)
        
        for transition in transitions:
            new_branches.append(self.diverge_branch(transition.transition_to)) # do we create two next branches or pick one to be branched?
        
        return new_branches

    def diverge_branch(self, next_state) -> "Branch": #creates another branch of current branch
        divergent = Branch(next_state, self.stack, self.recorded_path)
        return divergent

    def reject(self) -> None: #branch did not accept string.
        self.alive = False