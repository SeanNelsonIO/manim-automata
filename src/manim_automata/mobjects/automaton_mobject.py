from manim import *
from src.manim_automata.automata import deterministic_finite_automaton

__all__ = ["State"]


class ManimAutomaton(VMobject):

    manim_states = {}
    manim_transitions = []
    
    def __init__(self, automata_templete=None):
        super().__init__()
        if automata_templete:
            pass
        #composite relationship
        automaton = deterministic_finite_automaton(xml_file='testmachine.jff')

        #build the visualisation of the automaton
        for state in automaton.states:
            manim_state = self.create_state(state.name)
            if state.initial:
                manim_state = self.create_initial_state(manim_state)
            if state.final:
                manim_state = self.create_final_state(manim_state)

            self.manim_states[state.name] = manim_state

    
        count = -6
        for key in self.manim_states:
            self.add(self.manim_states[key].shift(RIGHT * count))
            count = count + 4
            # self.add(state)

        for transition in automaton.transitions:
            manim_state_from = self.manim_states[transition.transition_from.name] #lookup manim state using dict
            manim_state_to = self.manim_states[transition.transition_to.name] #lookup manim state using dict

            manim_transition = self.create_transition(manim_state_from, manim_state_to, transition.input_symbol)

            self.manim_transitions.append(manim_transition)

        for transition in self.manim_transitions:
            self.add(transition)
        

    def create_initial_state(self, state):
        arrow = Arrow(buff=0.5, start=4 * LEFT, end=LEFT * 0.5)
        initial_state = VGroup(arrow, state)
        return state # need to fix arrow to state

    def create_final_state(self, state):
        state_outer = Circle(radius=state.width*0.6)
        final_state = VGroup(state_outer, state)
        return final_state

    def create_state(self, label):
        state = VGroup(Circle(radius=0.9), Text(label))
        return state

    def create_transition(self, start_state, end_state, label=None):
        if start_state == end_state: #create transition that points to itself
            transition = Arrow([-1, 2, 0], start_state, buff=0) #refactor this to look better
        else: #start_state ----> end_state
            transition = Arrow(start_state, end_state, buff=0)
        
        if label: #if the tranistion is given a label (input symbols)
            text = Text(label)
            text.next_to(transition, direction=UP, buff=0)
            transition = VGroup(transition, text)

        return transition
    
    def create_bezier(self):
           #     self.add(transition)
        pass
        # a = ArcPolygon(ORIGIN, RIGHT + 3, [0, 2, 0], radius=6)
        # a = Arc(angle=PI*1.9, radius=-1)
        # a.add_tip()
        # self.add(a)
        # vertices = [
        #     [0, 0, 0],
        #     [0, 1, 2],
        #     [1, 0, 1],
        #     [0, 0, 0]
        # ]
        # cubic_bezier = CubicBezier(points=vertices)
        # self.add(cubic_bezier)
        # p1 = np.array([-3, 1, 0])
        # p1b = p1 + [1, 0, 0]
        # d1 = Dot(point=p1).set_color(BLUE)
        # l1 = Line(p1, p1b)
        # p2 = np.array([3, -1, 0])
        # p2b = p2 - [1, 0, 0]
        # d2 = Dot(point=p2).set_color(RED)
        # l2 = Line(p2, p2b)
        # bezier = CubicBezier(ORIGIN, UP, UP * RIGHT, DOWN * RIGHT)


        # arrow_tip = ArrowTip()
        # self.add(arrow_tip)

        # self.add(bezier)

        # self.add(CurvedArrow(ORIGIN, DOWN).shift(LEFT * 4))
    
    
    #need to create a transition function that transitions to itself
    def create_reflextive_transition(): #change name of this!
        pass

    def generate_manim_states():
        pass


    def generate_automaton(): 
        #creates a visual representation of automaton using template or automata object
        pass

    

        

class State(VMobject):

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
        
    



        # dot1 = Circle().shift(LEFT)
        # dot2 = Circle()
        # dot3 = Circle().shift(RIGHT)
        # self.dotgrid = VGroup(dot1, dot2, dot3)
        # self.add(self.dotgrid)