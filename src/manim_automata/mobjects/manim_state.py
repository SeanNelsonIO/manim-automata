from manim import *
from .automata_dependencies.automata import State



class ManimState(State, VGroup):
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
    def __init__(self, name: str, x: float, y: float, animation_style: dict, initial: bool = None, final: bool = None, scaling=10, id=None, **kwargs) -> None:
        State.__init__(self, name=name, initial=initial, final=final, id=id)

        #manim settings for animations and colors
        self.animation_style = animation_style
        
        self.text = Tex(name, font_size=100)
        self.circle = Circle(radius=2, color=BLUE)

        if True:
            self.initialise_subscript()
            VGroup.__init__(self, self.circle, self.text, self.subscript, name=name, **kwargs)
        
        else:
            VGroup.__init__(self, self.circle, self.text, name=name, **kwargs)
    
        self.set_x(x/scaling)
        self.set_y((y*-1)/scaling) # multiply y by -1 to flip the y axis, more similar to JFLAP


        if self.final:
            self.set_to_final_state()
        if self.initial:
            self.set_to_initial_state()

    def update_subscript(self, number):
        self.remove(self.subscript)
        self.subscript = self.subscript = Tex(number, font_size=50)
        self.subscript.set_x(self.text.get_x() + -0.5)
        self.subscript.set_y(self.text.get_y() + -0.5)
        self.add(self.subscript)

    def initialise_subscript(self):
        self.subscript = Tex(0, font_size=50)
        self.subscript.set_x(self.text.get_x() + -0.5)
        self.subscript.set_y(self.text.get_y() + -0.5)


    def set_to_final_state(self) -> None:
        state_outer = Circle(radius=self.width*0.4, color=BLUE)
        #move x and y of outerloop to be in the same position as parameter:state
        state_outer.set_x(self.circle.get_x())
        state_outer.set_y(self.circle.get_y())
        self.add(state_outer)

    def set_to_initial_state(self) -> None:
        arrow = Arrow(start=LEFT * 5, end=self, color=BLUE, buff=0.1, tip_style={'stroke_width': 5})
        # self.manim_state = VGroup(arrow, self.manim_state)
        self.add(arrow)


