from manim import *

from .manim_automaton import ManimAutomaton
from .manim_state import ManimState, State
from .manim_automaton_input import ManimAutomataInput
from .manim_transition import ManimTransition


from typing import Union

class ManimDeterminsticFiniteAutomaton(ManimAutomaton):

    def __init__(self, json_template=None, xml_file=None, camera_follow=False, animation_style=None, **kwargs) -> None:
        if animation_style is None:
            super().__init__(json_template, xml_file, camera_follow, **kwargs)
        else:
            super().__init__(json_template, xml_file, camera_follow, animation_style, **kwargs)

    #returns a list of animations to run through
    def play_string(self, input: Union[str, "ManimAutomataInput"]) -> list:
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
    
            step_result, next_states, transition_ids = self.automaton_step(token, state_pointer) #simulates the machine

            transition = self.get_transition_by_id(int(transition_ids[0]))

            list_of_animations.append(self.step(transition, token, state_pointer, step_result)) # self.step returns a list of animations for that step

            #if successful point to the next state
            if step_result is True:
                #move state_pointer to next state
                if len(next_states) > 0:
                    list_of_animations.append([FadeToColor(state_pointer, color=BLUE), FadeToColor(next_states[0], color=YELLOW)])
                    state_pointer = next_states[0]
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