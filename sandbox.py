from enum import auto
from hmac import trans_36
from typing import Text
from manim import *
from manim_automata.automata import Transition
from src.manim_automata.mobjects import *
from src.manim_automata.mobjects.automaton_mobject import ManimAutomaton, ManimTransition

class CreateCircle(MovingCameraScene):
    def construct(self):

        for x in range(-7, 8):
            for y in range(-4, 5):
                self.add(Dot(np.array([x, y, 0]), color=DARK_GREY))


        self.manim_automaton = ManimAutomaton()
        

        self.play(
            Create(self.manim_automaton), #vector that shifts automaton to centre of scene
            # self.camera.frame.animate.scale(.5)
        )
        
        
        input_string = "010101010"
        if self.play_string(input_string) is False:
            self.play_rejected()
        else:
            self.play_accepted()

        self.wait(1)

    def play_string(self, string: str):
        #create manim objects of tokens
        manim_tokens = []
        spacing = 0
        for token in string:
            manim_tokens.append(Text(token, font_size=40).shift((DOWN*2) + [spacing, 0, 0] + (LEFT * 3)))
            spacing = spacing + 0.5

        #display string
        for token in manim_tokens:
            self.add(token)
            
        #Points to the current state
        state_pointer = self.manim_automaton.get_initial_state()
        #animate the automaton going through the sequence
        for i, token in enumerate(manim_tokens):
            #check if it is last token
            if i == len(manim_tokens)-1:
                #animate for the final state
                pass
            
            step_result, next_state, transition_id = self.manim_automaton.automaton.step(token, state_pointer)
            #get transition with transition id
            transition = self.manim_automaton.get_manim_transition(transition_id)

            self.animate_step(transition, token, state_pointer, step_result)
            
            #if successful point to the next state
            if step_result is True:
                #move state_pointer to next state
                if next_state:
                    state_pointer = next_state
            else: #if step fails then stop play process early as the string is not accepted
                return False
            
        
        #check that the current state_pointer is a final state
        if state_pointer.final:
            return True
        else:
            return False


    def animate_step(self, manim_transition: ManimTransition, token: str, state_pointer, result: bool):

        if manim_transition == None: #there is no possible transition
            self.play(
                token.animate.set_color(RED) # create a custom animation to signify result
            )
        else:
            self.play(
                Transform(token, manim_transition)
            )

            self.remove(token) # removes the token once it has transformed

            if result is True:
                self.play(
                    manim_transition.animate.set_color(GREEN) # create a custom animation to signify result
                )
            else:
                self.play(
                    manim_transition.animate.set_color(RED) # create a custom animation to signify result
                )
            
    def play_rejected(self):
        text = Text("REJECTED")
        self.play(
            Create(text.shift(DOWN*3)),
            text.animate.set_color(RED)
        )

        for manim_transition in self.manim_automaton.manim_transitions:
            self.add(manim_transition.set_color(RED))
            # self.play(manim_transition.animate.set_color(RED))
        
        for key in self.manim_automaton.manim_states:
            manim_state = self.manim_automaton.manim_states[key]
            self.add(manim_state.set_color(RED))
        

        

    def play_accepted(self):
        text = Text("Accepted")
        self.play(
            Create(text.shift(DOWN*3)),
            text.animate.set_color(GREEN)
        )

        for manim_state in self.manim_automaton.manim_states:
            self.add(manim_state.set_color(GREEN))

        for key in self.manim_automaton.manim_states:
            manim_state = self.manim_automaton.manim_states[key]
            self.add(manim_state.set_color(GREEN))


