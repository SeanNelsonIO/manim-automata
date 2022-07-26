from manim import *
from .automata_dependencies.automata import State



class ManimState(VGroup):
    """Class that describes the graphical representation of a State instance,
    it is also used to simulate tautomata.

    Parameters
    ----------
    state
        State instance that the Mobject is modelled from.
    **kwargs
        Key words arguments for the VGroup.

    Attributes
    ----------
    state
        Reference to a State instance.
    circle
        Circle Mobject
    text
        Text Mobject representation of the name from State instance.
    """
    def __init__(self, state: State, animation_style: dict, **kwargs) -> None:
        self.animation_style = animation_style
        self.state = state
        self.text = Tex(state.name, font_size=100)

        self.circle = Circle(radius=2, color=BLUE)
        # self.manim_state = VGroup(self.circle, self.text)
        super().__init__(self.circle, self.text, **kwargs)

        self.set_x(float(state.x)/10)
        self.set_y(float(state.y*-1)/10) # multiply y by -1 to flip the y axis, more similar to JFLAP
 
        if state.initial:
            self.set_to_initial_state()
        if state.final:
            self.set_to_final_state()


    def set_to_final_state(self) -> None:
        state_outer = Circle(radius=self.width*0.4, color=BLUE)
        #move x and y of outerloop to be in the same position as parameter:state
        state_outer.set_x(self.get_x())
        state_outer.set_y(self.get_y())
        self.add(state_outer)

    def set_to_initial_state(self) -> None:
        arrow = Arrow(start=LEFT * 5, end=self, color=BLUE, buff=0.1, tip_style={'stroke_width': 5})
        # self.manim_state = VGroup(arrow, self.manim_state)
        self.add(arrow)

    def highlight_state(self):
        pass
