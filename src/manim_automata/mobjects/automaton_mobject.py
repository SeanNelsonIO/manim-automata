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

        q1 = self.final_state(Text('q1')).shift(RIGHT * 2)

        self.add(q0, q1)
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

    def final_state(self, name):
        state = Circle(radius=0.7)
        state_outer = Circle(radius=0.9)
        final_state = VGroup(state, state_outer, name)
        return final_state

    def state(self, name):
        state = VGroup(Circle(radius=0.9), name)
        return state
        


    def transition():
        pass



        # dot1 = Circle().shift(LEFT)
        # dot2 = Circle()
        # dot3 = Circle().shift(RIGHT)
        # self.dotgrid = VGroup(dot1, dot2, dot3)
        # self.add(self.dotgrid)