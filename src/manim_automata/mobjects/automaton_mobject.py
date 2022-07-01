from cProfile import label
from manim import *
from src.manim_automata.automata import deterministic_finite_automaton

__all__ = ["State"]


class finite_automaton(VMobject):
    
    def __init__(self, automata_templete: dict):
        super().__init__()
        pass
        # deterministic_finite_automaton(template=automata_templete)


        

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