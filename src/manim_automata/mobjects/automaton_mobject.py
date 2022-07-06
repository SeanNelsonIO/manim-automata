from manim import *
from src.manim_automata.automata import deterministic_finite_automaton, Transition, State

__all__ = ["State"]


class ManimTransition(VMobject):
    def __init__(self, transition: Transition, start_state, end_state, label=None):
        super().__init__()

        self.transition = transition

        if start_state == end_state: #create transition that points to itself
            self.arrow = Arrow([-1, 2, 0], start_state, buff=0) #refactor this to look better
        else: #start_state ----> end_state
            self.arrow = Arrow(start_state, end_state, buff=0)
        
        if label: #if the tranistion is given a label (input symbols)
            self.text = Text(label, font_size=30)
            self.text.next_to(self.arrow, direction=UP, buff=0)
            self.edge = VGroup(self.arrow, self.text)

        self.add(self.edge)

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
            manim_state = self.create_manim_state(state.name, state.x, state.y)
            if state.initial:
                manim_state = self.create_manim_initial_state(manim_state)
            if state.final:
                manim_state = self.create_manim_final_state(manim_state)

            self.manim_states[state.name] = manim_state
            self.add(manim_state)
    
        for transition in self.automaton.transitions:
            manim_state_from = self.manim_states[transition.transition_from.name] #lookup manim state using dict
            manim_state_to = self.manim_states[transition.transition_to.name] #lookup manim state using dict

            manim_transition = ManimTransition(transition, manim_state_from, manim_state_to, transition.input_symbol)
            self.manim_transitions.append(manim_transition)

        for manim_transition in self.manim_transitions:
            self.add(manim_transition)
        

    def create_manim_initial_state(self, state):
        arrow = Arrow(buff=0.5, start=4 * LEFT, end=LEFT * 0.5)
        initial_state = VGroup(arrow, state)
        return initial_state # need to fix arrow to state

    def create_manim_final_state(self, state):
        state_outer = Circle(radius=state.width*0.4)
        #move x and y of outerloop to be in the same position as parameter:state
        state_outer.set_x(state.get_x())
        state_outer.set_y(state.get_y())
        final_state = VGroup(state, state_outer)
        return final_state

    def create_manim_state(self, label: str, x: float, y: float):
        circle = Circle(radius=0.5)
        state = VGroup(circle, Text(label, font_size=30))

        state.set_x(float(x)/30)
        state.set_y(float(y)/30)

        return state

    def create_manim_transition(self, start_state, end_state, label=None):
        if start_state == end_state: #create transition that points to itself
            transition = Arrow([-1, 2, 0], start_state, buff=0) #refactor this to look better
        else: #start_state ----> end_state
            transition = Arrow(start_state, end_state, buff=0)
        
        if label: #if the tranistion is given a label (input symbols)
            text = Text(label, font_size=30)
            text.next_to(transition, direction=UP, buff=0)
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
        


    # def position_states(self, states): #algorithm to position states in scene
    #     for state in states: #find initial state
    #         if state.initial:
    #             initial_state = state
    #             #set position of initial state to origin
    #             initial_state.x = 0
    #             initial_state.y = 0
    #             break
        
    #     #create hiarchy of levels

    #     #create create hiarchy within levels (most valuable goes higher)

        


    
    def create_bezier(self):
        # bezier = CubicBezier(ORIGIN, UP, UP * RIGHT, DOWN * RIGHT)
        # arrow_tip = ArrowTip()
        # self.add(arrow_tip)
        # self.add(bezier)
        # self.add(CurvedArrow(ORIGIN, DOWN).shift(LEFT * 4))
        pass
    
    #need to create a transition function that transitions to itself
    def create_reflextive_transition(): #change name of this!
        pass

    def generate_manim_states():
        pass


    def generate_automaton(): 
        #creates a visual representation of automaton using template or automata object
        pass

    

        

class ManimState(VMobject):


    def __init__(self):
        super().__init__()
        # state = Circle().shift(LEFT)
        # state = Circle(radius=0.7)
        # state_outer = Circle(radius=0.9)

        # final_state = VGroup(state, state_outer)

        # state2 = Circle().shift(RIGHT)
        # id = 1
        # name = Text('q0')
       
        q0 = self.initial_state(self.state(Text('q0')))

        q1 = self.final_state(self.state(Text('q1'))).shift(RIGHT * 3)

        transition1 = self.transition(q0, q1, label="1")

        q2 = self.state(Text('q2')).shift(RIGHT  * 6)

        transition2 = self.transition(q1, q2, label="0")

        self.add(q0, transition1, q1, transition2, q2)
        # self.final_state(Text('q1'))
        # self.state_grid = VGroup(state, name)
        # arrow = Arrow(buff=0.5, start=4 * LEFT, end=LEFT * 0.5)
        # arrow = Arrow(start=LEFT*2, end=CENTRE)
        
        # initial_state = VGroup(final_state, arrow)

        # self.add(arrow, final_state, name)

    def initial_state(self, state):
        arrow = Arrow(buff=0.5, start=4 * LEFT, end=LEFT * 0.5)
        initial_state = VGroup(arrow, state)
        return initial_state

    def final_state(self, state):
        state_outer = Circle(radius=state.width*0.6)
        final_state = VGroup(state_outer, state)
        return final_state

    def state(self, name):
        state = VGroup(Circle(radius=0.9), name)
        return state

    def transition(self, start_state, end_state, label=None):
        transition = Arrow(start_state, end_state, buff=0)
        
        if label: #if the tranistion is given a label (input symbols)
            text = Text(label)
            text.next_to(transition, direction=UP, buff=0)
            transition = VGroup(transition, text)

        return transition

