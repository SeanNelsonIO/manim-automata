from enum import auto
from hmac import trans_36
from manim import *
from manim_automata.automata import Transition
# from manim_automata.automata import Automata
# from manim_automata.mobjects.automaton_mobject import ManimAutomaton
# from src.manim-automata import *
from src.manim_automata.mobjects import *
from src.manim_automata.mobjects.automaton_mobject import ManimAutomaton, ManimTransition

class CreateCircle(MovingCameraScene):
    def construct(self):
        # dot_grid = DotGrid()
        # circle = Circle()  # create a circle
        # circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        # self.play(Create(dot_grid))  # show the circle on screen
        # dot_grid.update_dot()
        # self.play(Create(dot_grid))  # show the circle on screen

        for x in range(-7, 8):
            for y in range(-4, 5):
                self.add(Dot(np.array([x, y, 0]), color=DARK_GREY))

        # self.camera_frame.save_state()

        # state = State()
        self.manim_automaton = ManimAutomaton()
        # self.play(Create(automaton))


        # automaton.play_string("1010010010")
        

            
        self.play(
            Create(self.manim_automaton), #vector that shifts automaton to centre of scene
            # self.camera.frame.animate.scale(.5)
        )
        
        
        # input_string = ["0", "1", "0", "0", "1", "0"]
        input_string = "010101010"
        if self.play_string(input_string) is False:
            self.play(Create(Text("REJECTED").shift((DOWN*3))))
        else:
            self.play(Create(Text("Accepted").shift((DOWN*3))))

        self.wait(1)

    def play_string(self, string: str):
        #create manim objects of tokens
        manim_tokens = []
        spacing = 0
        for token in string:
            manim_tokens.append(Text(token, font_size=40).shift((DOWN*2) + [spacing, 0, 0]))
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
            else:
                return False
            #if not then reject string

        return True


    def animate_step(self, manim_transition: ManimTransition, token: str, state_pointer, result: bool):

        if manim_transition == None: #there is no possible transition
            self.play(
                token.animate.set_color(RED) # create a custom animation to signify result
            )
        else:
            # first_transition.add_updater([1, 1, 0])
            # self.play()
            # d1 = Dot().set_color(ORANGE)
            # l1 = Line(LEFT, RIGHT)
            # l2 = VMobject()
            # self.add(d1, l1, l2)
            # l2.add_updater(lambda x: x.become(Arrow(LEFT, d1.get_center()).set_color(ORANGE)))
            # self.play(MoveAlongPath(d1, l1), rate_func=linear)

            # self.play(token.animate.)

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
            


