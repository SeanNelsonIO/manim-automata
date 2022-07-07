from manim import *
from src.manim_automata.automata import deterministic_finite_automaton, Transition, State

__all__ = ["State"]


class ManimTransition(VMobject):
    def __init__(self, transition: Transition, start_state, end_state, label=None):
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
        self.manim_state.set_y(float(state.y)/30)

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


class ManimAutomaton(VMobject):

    manim_states = {}
    manim_transitions = []
    
    def __init__(self, automata_templete=None):
        super().__init__()
        if automata_templete:
            pass
        #composite relationship
        self.automaton = deterministic_finite_automaton(xml_file='testmachine.jff')
        
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
        pass
        

        


