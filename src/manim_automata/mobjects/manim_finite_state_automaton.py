from manim import *
from .automata_dependencies.automata import FiniteStateAutomaton
from .manim_state import ManimState, State
from .manim_automaton_input import ManimAutomataInput
from .manim_transition import ManimTransition

from typing import Union

__all__ = ["ManimAutomaton"]

default_animation_style = {
    "animate_transition": {
        "animation_function": ShowPassingFlash,
        "accept_color": GREEN,
        "reject_color": RED,
        "run_time": 0.5,
        "time_width": 2
    },
    "highlight_state": {
        "color": YELLOW
    },
    "token_highlight": {
        "animation_function": Indicate,
        "color": YELLOW
    }
}

class ManimAutomaton(FiniteStateAutomaton, VGroup):
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

    def __init__(self, json_template=None, xml_file=None, camera_follow=False, animation_style=default_animation_style, **kwargs) -> None:
        super(FiniteStateAutomaton, self).__init__()

        self.animation_style = animation_style
        self.camera_follow = camera_follow
        
        # default animation style
        # and allow users to pass in functions that replace some of the functionality such as play_accept..
        
        super(VGroup, self).__init__(**kwargs)

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
        self.states.append(ManimState(state["@name"], new_x, new_y, animation_style=self.animation_style, initial=initial, final=final))

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
                transition_group.append(transition['read']) #append transition read value to transition[state_key]

        #avoids creating multiple manim_transitions.
        #Creates one manim_transition with multiple read values
        for state_key in transition_counter:
            read_values = transition_counter[state_key]

            transition_from = self.get_state_by_id(int(state_key[0]))
            transition_to = self.get_state_by_id(int(state_key[1]))

            self.construct_transition(transition_from, transition_to, read_values)

    def construct_transition(self, transition_from: ManimState, transition_to: ManimState, read_symbols: list):
        new_transition = ManimTransition(transition_from, transition_to, read_symbols, animation_style=self.animation_style)
        self.transitions.append(new_transition)
        #add the transition to the from_states link list
        transition_from.add_transition_to_state(new_transition)
        
    def construct_automaton_input(self, input_string: str) -> "ManimAutomataInput":
        return ManimAutomataInput(input_string, animation_style=self.animation_style)
        
    #returns a list of animations to run through
    def play_string(self, input: Union[str,"ManimAutomataInput"]) -> list:
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

       
        #animate the automaton going through the sequence
        for i, token in enumerate(self.manim_automata_input.tokens):
            #check if it is last token
            if i == len(self.manim_automata_input.tokens)-1:
                #animate for the final state
                pass
    
            step_result, next_state, transition_id = self.automaton_step(token, state_pointer) #simulates the machine

            #get transition with transition id
            transition = self.get_transition_by_id(int(transition_id))
            
            

            list_of_animations.append(self.step(transition, token, state_pointer, step_result)) # self.step returns a list of animations for that step

            #if successful point to the next state
            if step_result is True:
                #move state_pointer to next state
                if next_state:
                    list_of_animations.append([FadeToColor(state_pointer, color=BLUE), FadeToColor(next_state, color=YELLOW)])
                    state_pointer = next_state
            else: #if step fails then stop play process early as the string is not accepted
                text = Tex("REJECTED", color=RED, font_size=100)
                text.set_x(token.get_x())
                text.set_y(token.get_y())

                
                list_of_animations.append([Transform(self.manim_automata_input, text)])
                list_of_animations.append([FadeToColor(self, color=RED)])

                return list_of_animations

        #check that the current state_pointer is a final state
        if state_pointer.final:
            text = Tex("ACCEPTED", color=GREEN, font_size=100)
            text.set_x(token.get_x())
            text.set_y(token.get_y())

            list_of_animations.append([Transform(self.manim_automata_input, text)])
            list_of_animations.append([FadeToColor(self, color=GREEN)])
        else:
            text = Tex("REJECTED", color=RED, font_size=100)
            text.set_x(token.get_x())
            text.set_y(token.get_y())
            
            list_of_animations.append([Transform(self.manim_automata_input, text)])
            list_of_animations.append([FadeToColor(self, color=RED)])
           
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

            list_of_step_animations.append(
                ManimAutomataInput.highlight_token(token, self.animation_style)
            )

            #Animation that highlights the transition - Green for True and red otherwise
            list_of_step_animations.append(
                manim_transition.animate_transition(result)
            )

            list_of_step_animations.append(
                token.animate.set_opacity(0.5)
            )
        
        return list_of_step_animations


    def set_default_position_of_input_string(self):
        list_of_input_string_animations = []
        #get centre of self
        c1 = self.get_x()
        c2 = self.get_y()
        #set position of manim_automata_input relative to self
        self.manim_automata_input.set_x(c1)
        self.manim_automata_input.set_y(c2 + self.height/4)
        
        

    def parse_animation_style(self):
        pass


    def build_animation(self, animation_function, color, subject, **kwargs):
        """Build and returns line of animation code"""
        animation_function()

        return animation_function


    def move_camera(self):

        # self.camera.frame.animate.move_to(self.get_manim_state(state_pointer)).scale(1)
        pass