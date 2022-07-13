from manim import *
from src.manim_automata.automata import deterministic_finite_automaton, Transition, State


__all__ = ["State"]

class ManimTransition(VMobject):
    def __init__(
        self,
        transition: Transition,
        start_state: State,
        end_state: State,
        label: str,
        **kwargs
    ) -> None:
        """A Manim Transition. A visual representation of a Transition

        Parameters
        ----------
        transition
            Positions of pendulum bobs.
        start_state
            state at which the transition sta
        end_state
            Parameters for ``Line``.
        label
            Parameters for ``Circle``.
        kwargs
            Additional parameters for ``VMobject``.
        Examples - do I need this.
        --------
        .. manim:: ManimTransitionExample

            from manim_physics import *
            class MultiPendulumExample(SpaceScene):
                def construct(self):
                    p = MultiPendulum(RIGHT, LEFT)
                    self.add(p)
                    self.make_rigid_body(p.bobs)
                    p.start_swinging()
                    self.add(TracedPath(p.bobs[-1].get_center, stroke_color=BLUE))
                    self.wait(10)
        """
        super().__init__()

        self.transition = transition

        if start_state == end_state: #create transition that points to itself
            self.arrow = Arrow([-1, 2, 0], start_state.manim_state, buff=0) #refactor this to look better
        else: #start_state ----> end_state
            self.arrow = Arrow(start_state.manim_state, end_state.manim_state, buff=0)
        
        if label: #if the tranistion is given a label (input symbols)
            self.text = Text(label, font_size=30)
            self.text.next_to(self.arrow, direction=UP, buff=0)
            self.edge = VGroup(self.arrow, self.text)

        self.add(self.edge)

class ManimState(VMobject):
    def __init__(self, state: State, initial: bool, final: bool):
        super().__init__()

        self.state = state

        self.circle = Circle(radius=0.5, color=BLUE)
        self.manim_state = VGroup(self.circle, Text(state.name, font_size=30))

        self.manim_state.set_x(float(state.x)/30)
        self.manim_state.set_y(float(state.y*-1)/30) # multiply y by -1 to flip the y axis, more similar to JFLAP

        if initial:
            self.set_to_initial_state()
        if final:
            self.set_to_final_state()

        self.add(self.manim_state)

    def set_to_final_state(self):
        state_outer = Circle(radius=self.manim_state.width*0.4, color=BLUE)
        #move x and y of outerloop to be in the same position as parameter:state
        state_outer.set_x(self.manim_state.get_x())
        state_outer.set_y(self.manim_state.get_y())
        self.manim_state = final_state = VGroup(self.manim_state, state_outer)
        self.add(self.manim_state)

    def set_to_initial_state(self):
        arrow = Arrow(buff=0, start=LEFT * 2, end=LEFT * 0.5, color=BLUE)
        self.manim_state = VGroup(arrow, self.manim_state)
        self.add(self.manim_state)


class ManimAutomaton(VGroup):

    manim_states = {}
    manim_transitions = []
    
    def __init__(self, automata_templete=None, **kwargs):
        super().__init__(**kwargs)
        if automata_templete:
            pass
        #composite relationship
        self.automaton = deterministic_finite_automaton(xml_file='testmachine2.jff')
        
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
            manim_state = ManimState(state, state.initial, state.final)
            self.manim_states[state.name] = manim_state
            self.add(manim_state)
    
        for transition in self.automaton.transitions:
            manim_state_from = self.manim_states[transition.transition_from.name] #lookup manim state using dict
            manim_state_to = self.manim_states[transition.transition_to.name] #lookup manim state using dict

            manim_transition = ManimTransition(transition, manim_state_from, manim_state_to, transition.input_symbol)
            self.manim_transitions.append(manim_transition)
        
        for manim_transition in self.manim_transitions:
            self.add(manim_transition)
            # self.scene.scene.play(Create(manim_transition))

        
        # self.animate = ManimAutomataAnimation


    def create_manim_transition(self, start_state, end_state, label=None):
        if start_state == end_state: #create transition that points to itself
            transition = Arrow([-1, 2, 0], start_state, buff=0) #refactor this to look better
        else: #start_state ----> end_state
            transition = Arrow(start_state, end_state, buff=0)
        
        if label: #if the tranistion is given a label (input symbols)
            text = Text(label, font_size=30)
            text.next_to(transition, direction=UP*CENTER, buff=0)
            transition = VGroup(transition, text)

        return transition

    def get_initial_state(self):
        return self.automaton.get_initial_state()

    def get_manim_transition(self, transition_id: int): #incorrect solution TODO
        for manim_transition in self.manim_transitions:
            if manim_transition.transition.id == transition_id:
                return manim_transition

    def get_manim_state(self, state: State):
        return self.manim_states[state.name]
        

    #returns a list of animations to run through
    def play_string(self, input_string: str) -> None:
        list_of_animations = []
        
        #token creation
        manim_tokens = []
        spacing = 0
        for token in input_string:
            manim_tokens.append(Text(token, font_size=40).shift((DOWN*2) + [spacing, 0, 0] + (LEFT * 3)))
            spacing = spacing + 0.5

        
        #display tokens
        manim_tokens_group = VGroup(*manim_tokens)
        list_of_animations.append([FadeIn(manim_tokens_group)]) #put it inside list


        #Points to the current state
        state_pointer = self.get_initial_state()
        #animate the automaton going through the sequence
        for i, token in enumerate(manim_tokens):
            #check if it is last token
            if i == len(manim_tokens)-1:
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
                    state_pointer = next_state
            else: #if step fails then stop play process early as the string is not accepted
                # return False
                return list_of_animations


        # transition1 = self.get_manim_transition(1)
        # transition2 = self.get_manim_transition(2)

        # self.animate_step(transition, token, state_pointer, step_result)

        # list_of_animations.append(Transform(transition1, transition2))
        
        return list_of_animations


            
        
        #check that the current state_pointer is a final state
        if state_pointer.final:
            return True
        else:
            return False


    def step(self, manim_transition: ManimTransition, token: str, state_pointer, result: bool):
        #creates a list of animations for the step
        list_of_step_animations = []
        if manim_transition == None: #there is no possible transition
            list_of_step_animations.append(
                token.animate.set_color(RED) # create a custom animation to signify result
            )
        else:
            #move camera with every state, using the state_pointer
            # self. = manim_state
            # if self.camera_follow_state is True: #need someway to replace
            #     list_of_step_animations.append(
            #         self.camera.frame.animate.move_to(self.manim_automaton.get_manim_state(state_pointer)).scale(1)
            #     )

            list_of_step_animations.append(
                Indicate(token)
            )
            
            list_of_step_animations.append(
                Transform(token, manim_transition)
            )

            # self.remove(token) # removes the token once it has transformed
            if result is True:
                list_of_step_animations.append(
                    ShowPassingFlash(
                        manim_transition.arrow.copy().set_color(GREEN),
                        run_time=2,
                        time_width=2
                    )
                )
                list_of_step_animations.append(
                    Flash(manim_transition.text, color=GREEN)
                )


                list_of_step_animations.append(
                    ShowPassingFlash(token, color=GREEN)
                    # manim_transition.animate.set_color(GREEN) # create a custom animation to signify result
                )
            else:
                list_of_step_animations.append(
                    manim_transition.animate.set_color(RED) # create a custom animation to signify result
                )
        
        return list_of_step_animations


    def start_machine(self) -> None:
        """Start swinging."""
        spacescene: Scene = self.scene

        # pins = [self.pivot_point]
        # pins += self.bobs

        # for i in range(len(pins) - 1):
        #     self._make_joints(pins[i + 1], pins[i], spacescene)
        #     self.rods[i].add_updater(lambda mob, i=i: self._redraw_rods(mob, pins, i))

        


