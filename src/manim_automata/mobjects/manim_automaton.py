from manim import *
from .automata_dependencies.automata import FiniteStateAutomaton
from .manim_state import ManimState, State
from .manim_automaton_input import ManimAutomataInput
from .manim_transition import ManimTransition
from .manim_animations import ManimAnimations

from .manim_cli import ManimAutomataCLI

from typing import Union

import abc

import json

__all__ = ["ManimAutomaton"]

default_animation_style = {
    "animate_transition": {
        "animation_function": FadeToColor,
        "accept_color": YELLOW,
        "reject_color": RED,
        "run_time": 0.5,
        "time_width": 2
    },
    "highlight_state": {
        "color": YELLOW
    },
    "token_highlight": {
        "animation_function": FadeToColor,
        "color": YELLOW
    }
}

class ManimAutomaton(FiniteStateAutomaton, VGroup, abc.ABC):
    """Class that describes the graphical representation of a State instance,
    it is also used to simulate automata.

    Parameters
    ----------
    automata_template
        State instance that the Mobject is modelled from.
    **kwargs
        Key words arguments for the VGroup.

    Attributes
    ----------
    automaton
        pass
    initial_state
        pass
    origin_offset_x
        pass
    origin_offset_y
        pass
    manim_states
        pass
    manim_transitions
        pass
    """

    def __init__(self, json_template=None, xml_file=None, camera_follow=False, animation_style=default_animation_style, manim_animations=None, cli=False, **kwargs) -> None:
        FiniteStateAutomaton.__init__(self)

        self.animation_style = animation_style
        self.camera_follow = camera_follow

        if manim_animations is None: #if user doesn't provide their own class set to default
            self.manim_animations = ManimAnimations()
        else:
            self.manim_animations = manim_animations

        self.cli = None
        if cli:
            self.cli = ManimAutomataCLI()
            self.nda_builder = True
        else: self.nda_builder = False
        # default animation style
        # and allow users to pass in functions that replace some of the functionality such as play_accept..
        
        VGroup.__init__(self, **kwargs)

        if json_template:
            self.automaton = FiniteStateAutomaton(json_template==json_template)
            self.construct_manim_states()
            self.construct_manim_transitions()
        elif xml_file:
            self.process_xml(xml_file)


        #add manim_states to screen/renderer
        self.add(*self.states)
        self.add(*self.transitions)


    def add_manim_state(self, manim_state: ManimState):
        #maybe need validation TODO
        #adds an already existing manim_state to automaton
        self.append(manim_state)
        
    def construct_state(self, state: dict) -> None: #creates a new manim_state instance
        #check if initial is set in state
        initial = False
        final = False
        if 'initial' in state.keys():
            initial = True 
            #check to see if there is already another initial state
            for state_object in self.states:
                if state_object.initial == True: #If there already exists an initial state set back to False and keep first initial state
                    initial = False
            
        if 'final' in state.keys():
            final = True

        new_x = float(state["x"]) - self.origin_offset_x
        new_y = float(state["y"]) - self.origin_offset_y
        #check if final exist in state
        self.states.append(ManimState(state["@name"], new_x, new_y, animation_style=self.animation_style, initial=initial, final=final, id=state["@id"]))

    def construct_states(self, states):
        #gets first initial state to calculate offset
        for state in states: 
            if 'initial' in state.keys():
                #store original values, used to normalise coordinates
                self.origin_offset_x = float(state["x"])
                self.origin_offset_y = float(state["y"])
                break
        
        for state in states:
            self.construct_state(state)
            
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
            if transition['read'] not in transition_group:
                if transition['read'] == None:
                    transition['read'] = r"\epsilon"
                transition_group.append(transition['read']) #append transition read value to transition[state_key]

        #avoids creating multiple manim_transitions.
        #Creates one manim_transition with multiple read values
        for state_key in transition_counter:
            read_values = transition_counter[state_key]

            transition_from = self.get_state_by_id(int(state_key[0]))
            transition_to = self.get_state_by_id(int(state_key[1])) #this is using the id from xml which will be different, can't use name either - has to be passed in

            self.construct_transition(transition_from, transition_to, read_values)

    def construct_transition(self, transition_from: ManimState, transition_to: ManimState, read_symbols: list):
        new_transition = ManimTransition(transition_from, transition_to, read_symbols, parent_automaton=self, animation_style=self.animation_style)
        self.transitions.append(new_transition)
        #add the transition to the from_states link list
        transition_from.add_transition_to_state(new_transition)
        
    def construct_automaton_input(self, input_string: str) -> "ManimAutomataInput":
        return ManimAutomataInput(input_string, animation_style=self.animation_style)

        
    def set_default_position_of_input_string(self):
        #get centre of self
        c1 = self.get_x()
        c2 = self.get_y()
        #set position of manim_automata_input relative to self
        self.manim_automata_input.set_x(c1)
        self.manim_automata_input.set_y(c2 + self.height/4)
        
    def check_automaton_result(self, state_pointers):
        for state in state_pointers:
            if state.final == True:
                return True
        return False

    def determine_input(self, input):
        """Checks to if input is a string or already an manim mobject,
            if it is type string then create manim_input instance using
            the input string.
        """
        if type(input) is str:
            #create mobject of input string
            self.manim_automata_input = self.construct_automaton_input(input)
            #position the mobject
            self.set_default_position_of_input_string()
        else: return input #if input is already an instance of ManimAutomataInput


    def run_sequence(self, token, state_pointers, iteration_history: list, predetermined_transition: "ManimTransition" = None) -> list[State]:
        next_states = []
        for state_pointer in state_pointers: #look at each state and calculate the steps that state can take.
            step_result, next_neighbour_states, transitions = self.automaton_step(token, state_pointer) #simulates the machine
            
            iteration_history.append({
                "state_pointer": state_pointer,
                "next_neighbour_states": next_neighbour_states,
                "transitions": transitions,
                "result": step_result,
                "token": token
            })

            if self.nda_builder:
                path_options = self.generate_next_state_options(state_pointer, transition_ids)
                user_choice = self.cli.display_dictionary_options(path_options)
                transition = path_options[user_choice][1] #get transition given user choice
                
                #record the transition choice
                self.recorded_path.append((transition.transition_from.name, transition.transition_to.name))

                transition_ids = [transition.id] #There is now only one transition that the state_pointer can take
                next_neighbour_states = [transition.transition_to] #There is now only one state that the state_pointer can go to

            #if step result is False then there are no more steps, check for final state and highlight state pointer as finished.
            # for transition in transitions:
            #     list_of_animations.append(self.step(transition, token, state_pointer, step_result)) # self.step returns a list of animations for that step
            
            #if successful point to the next state
            if step_result is True:
                if len(next_neighbour_states) > 0:
                    next_states = next_states + next_neighbour_states
            
            
        #if all state_pointers steps fail then automaton failed
        sequence_result = False
        for iteration in iteration_history:
            if iteration["result"] == True:
                sequence_result = True
                break

            # if len(next_neighbour_states) == 0: #if there are no more states or transitions left
            #     if self.check_automaton_result(state_pointers): #if the automaton has an active accepting state
            #         list_of_animations.append(self.generate_accept_animations())
            #     else: #if there is no final state then the machine is not accepted.
            #         list_of_animations.append(self.generate_reject_animations())

        return next_states, sequence_result
              

    def run_input_through_automaton(self, input: Union[str, "ManimAutomataInput"], automaton_path_name: str = None) -> list:
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

        #keeps track of what happend throughout each iteration
        global_history = {}

        initial_state = self.get_initial_state()
        state_pointers = [initial_state] # Keeps track of all the states that are activated

        # Animate the automaton going through the sequence
        for i, token in enumerate(input.tokens):
            iteration_history = []

            state_pointers, sequence_result = self.run_sequence(token, state_pointers, iteration_history) #goes through each state_pointer

            
            global_history[token.id] = {
                "token": token,
                "iteration_history": iteration_history
            }

            #if the input token failed then cancel input loop early
            if sequence_result == False:
                break
        
        #export the recorded path so the user can use it again without using nda builder
        if self.nda_builder:
            self.export_recorded_path_to_file()

        #add information about whether the input was accepted
        global_history["information"] = {
            "state_pointers": state_pointers,
            "automaton_result": self.check_automaton_result(state_pointers),
        }

        return global_history

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

    def play_string(self, input: Union[str, "ManimAutomataInput"]) -> list:
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

    def generate_history_animations(self, history):
        """Given a history of events of each iteration of the input ran through the manim automaton,
        generate all of the manim animations to visualise the process of the input going through the
        automaton"""

        list_of_animations = []

        #generate the pre-run animations
        state_pointer = self.get_initial_state()
        #Highlight current state with yellow
        list_of_animations.append(self.highlight_initial_state(state_pointer))
        for iteration_key in history:
            if iteration_key == "information": #provides information about the automaton and if it passed
                if history[iteration_key]["automaton_result"]: #if the automaton has an active accepting state
                    list_of_animations.append(self.generate_accept_animations()) #THIS IS GENERATED BEFORE ALL BRANCHES HAVE FINISHED
                else: #if there is no final state then the machine is not accepted.
                    list_of_animations.append(self.generate_reject_animations())
            else:
                token = history[iteration_key]["token"] #list of step histories
                iteration_history = history[iteration_key]["iteration_history"]

                #animate the token highlight
                list_of_animations.append(
                    [self.manim_animations.animate_highlight_input_token(token)]
                )

                for step_history in iteration_history:
                    list_of_animations = list_of_animations + self.animate_step_history(step_history) 

                   
                animate_subscripts = True #temp variable, TODO: intergrate into the api for user to choose
                if animate_subscripts == True:
                    list_of_animations.append(self.animate_subscripts(iteration_history))
                    
                
                #animate the token fades
                list_of_animations.append(
                    [self.manim_animations.animate_input_token_spent(token)]
                )

        #generate outcome animations
        return list_of_animations

    def animate_step_history(self, step_history) -> list:
        list_of_animations = []


        state_pointer = step_history["state_pointer"]
        next_neighbour_states = step_history["next_neighbour_states"]
        transitions = step_history["transitions"]
        step_result = step_history["result"]
        token = step_history["token"]


        #if step result is False then there are no more steps, check for final state and highlight state pointer as finished.
        step_animations = self.step(transitions, token, state_pointer, next_neighbour_states, step_result) # self.step returns a list of animations for that step
        
        if step_animations is not None:
            list_of_animations = list_of_animations + step_animations

        return list_of_animations

    def highlight_initial_state(self, initial_state):
        new_subscript_object = Tex(1, color=YELLOW)
        new_subscript_object.set_x(initial_state.subscript.get_x())
        new_subscript_object.set_y(initial_state.subscript.get_y())
        
        return [self.manim_animations.animate_highlight_state(initial_state),
                self.manim_animations.animate_transform_to_new_subscript_object(initial_state.subscript, new_subscript_object)]


    def generate_accept_animations(self):
        list_of_accept_animations = []

        text = Tex("ACCEPTED", color=GREEN, font_size=100)
        text.set_x(self.manim_automata_input.get_x())
        text.set_y(self.manim_automata_input.get_y())

        list_of_accept_animations.append(Transform(self.manim_automata_input, text))
        # list_of_accept_animations.append(FadeToColor(self, color=GREEN))

        return list_of_accept_animations

    def generate_reject_animations(self):
        list_of_reject_animations = []

        text = Tex("REJECTED", color=RED, font_size=100)
        text.set_x(self.manim_automata_input.get_x())
        text.set_y(self.manim_automata_input.get_y())

        list_of_reject_animations.append(Transform(self.manim_automata_input, text))
        # list_of_reject_animations.append(FadeToColor(self, color=RED))

        return list_of_reject_animations


    def step(self, manim_transitions: list[ManimTransition], token: "Tex", state_pointer: State, next_neighbour_states: list, step_result: bool) -> list:
        #creates a list of animations for the step
        list_of_step_animations = []

        if step_result is False: #if branch dies turn state red
            state_died_animation = []
            state_revert_back_to_default_animation = []

            # state_died_animation.append(FadeToColor(state_pointer, color=RED))
            state_died_animation.append(self.manim_animations.animate_dead_branch_state(state_pointer))

            state_revert_back_to_default_animation.append(self.manim_animations.animate_state_to_default_color(state_pointer))

            list_of_step_animations.append(
                state_died_animation
            )
            list_of_step_animations.append(
                state_revert_back_to_default_animation
            )


        else:
            activate_transition_animation = [self.manim_animations.animate_highlight_transition(x) for x in manim_transitions]

            #if successful point to the next state
            state_animations = []
            
            if step_result is True:
                
                if len(next_neighbour_states) > 0:
                    state_animations.append(self.manim_animations.animate_state_to_default_color(state_pointer))

                    state_animations = state_animations + [self.manim_animations.animate_highlight_state(x) for x in next_neighbour_states]
            

            deactivate_transition_animation = [self.manim_animations.animate_transition_to_default_color(x) for x in manim_transitions]
        
            #add the animations in the correct order
            list_of_step_animations.append(
                activate_transition_animation
            )

            list_of_step_animations.append(
                state_animations
            )
        
            list_of_step_animations.append(
                deactivate_transition_animation
            )
            
        return list_of_step_animations

    def animate_subscripts(self, iteration_history):
        animations = []
        #record the number of branches that end on each states
        state_counter = {}
        # for state in self.states:
        #     state_counter[state.id] = 0
            
        for step_history in iteration_history:
            next_neighbour_states = step_history["next_neighbour_states"]
            
            for state in next_neighbour_states:
                counter = state_counter.setdefault(state.id, 0) # key might exist already
                state_counter[state.id] = state_counter[state.id] + 1
                        
                # state_counter.setdefault(state.id, 1)
                # state_counter[state.id] = state_counter[state.id] + 1
        
        for state in self.states:
            if state.id in state_counter:
                new_subscript_object = Tex(state_counter[state.id], color=YELLOW)
                new_subscript_object.set_x(state.subscript.get_x())
                new_subscript_object.set_y(state.subscript.get_y())
                animations.append(self.manim_animations.animate_transform_to_new_subscript_object(state.subscript,  new_subscript_object))
            else: 
                new_subscript_object = Tex(0, color=BLUE)
                new_subscript_object.set_x(state.subscript.get_x())
                new_subscript_object.set_y(state.subscript.get_y())
                animations.append(self.manim_animations.animate_transform_to_new_subscript_object(state.subscript,  new_subscript_object))
        
        return animations

        