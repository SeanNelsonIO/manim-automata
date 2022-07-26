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

class ManimAutomaton(VGroup):
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

    manim_states = {}
    manim_transitions = []
    
    def __init__(self, automata_templete=None, xml_file=None, camera_follow=False, animation_style=default_animation_style, **kwargs) -> None:
        super().__init__(**kwargs)

        self.animation_style = animation_style
        self.camera_follow = camera_follow
        # default animation style
        # and allow users to pass in functions that replace some of the functionality such as play_accept..

        if automata_templete:
            pass
        #composite relationship
        self.automaton = FiniteStateAutomaton(xml_file=xml_file)
        
        self.construct_manim_states()
        self.construct_manim_transitions()
        

    def construct_manim_states(self):
        #calculate origin shift and normalise coordinates to manim coordinate system
        for state in self.automaton.states:
            #get the inital state (this should be set)
            if state.initial:
                self.initial_state = state
                #store original values, used to normalise coordinates
                self.origin_offset_x = float(state.x)
                self.origin_offset_y = float(state.y)
                break
        
        for state in self.automaton.states: #may need to take absolute values to prevent negative values (review)
            #normalise coordinates by subtracting offsets
            state.x = float(state.x) - self.origin_offset_x
            state.y = float(state.y) - self.origin_offset_y

        #build the visualisation of the automaton
        for state in self.automaton.states:
            # manim_state = self.create_manim_state(state)
            manim_state = ManimState(state, animation_style=self.animation_style)
            self.manim_states[state.name] = manim_state
            self.add(manim_state)

    def construct_manim_transitions(self):
        for transition in self.automaton.transitions:
            manim_state_from = self.manim_states[transition.transition_from.name] #lookup manim state using dict
            manim_state_to = self.manim_states[transition.transition_to.name] #lookup manim state using dict

            manim_transition = ManimTransition(transition, manim_state_from, manim_state_to, transition.read_symbols, animation_style=self.animation_style)
            self.manim_transitions.append(manim_transition)
        
        for manim_transition in self.manim_transitions:
            self.add(manim_transition)

    def create_manim_transition(self, start_state, end_state, label=None) -> "ManimTransition":
        if start_state == end_state: #create transition that points to itself
            transition = Arrow([-1, 2, 0], start_state, buff=0) #refactor this to look better
        else: #start_state ----> end_state
            transition = Arrow(start_state, end_state, buff=0)
        
        if label: #if the tranistion is given a label (input symbols)
            text = Tex(label, font_size=30)
            text.next_to(transition, direction=UP*CENTER, buff=0)
            transition = VGroup(transition, text)

        return transition

    def get_initial_state(self) -> "State":
        return self.automaton.get_initial_state()

    def get_manim_transition(self, transition_id: int) -> "ManimTransition": #incorrect solution TODO
        for manim_transition in self.manim_transitions:
            if manim_transition.transition.id == transition_id:
                return manim_transition

    def get_manim_state(self, state: State) -> "ManimState":
        return self.manim_states[state.name]
        
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
        list_of_animations.append([FadeToColor(self.manim_states[state_pointer.name], color=YELLOW)])

       
        #animate the automaton going through the sequence
        for i, token in enumerate(self.manim_automata_input.tokens):
            #check if it is last token
            if i == len(self.manim_automata_input.tokens)-1:
                #animate for the final state
                pass
            
            step_result, next_state, transition_id = self.automaton.step(token, state_pointer) #simulates the machine
            #get transition with transition id
            transition = self.get_manim_transition(transition_id)
            

            list_of_animations.append(self.step(transition, token, state_pointer, step_result)) # self.step returns a list of animations for that step

            #if successful point to the next state
            if step_result is True:
                #move state_pointer to next state
                if next_state:
                    list_of_animations.append([FadeToColor(self.manim_states[state_pointer.name], color=BLUE), FadeToColor(self.manim_states[next_state.name], color=YELLOW)])
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