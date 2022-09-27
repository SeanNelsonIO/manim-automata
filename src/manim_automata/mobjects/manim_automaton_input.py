from manim import *

import itertools

class ManimAutomataInput(VGroup):
    """Class that describes the graphical representation of the input string,
    it is also used to simulate tautomata.

    Parameters
    ----------
    input_string
        Represents the
    font_size
        The class' position on the x-axis.
    **kwargs
        key words arguments for the VGroup

    Attributes
    ----------
    tokens
        list of text mobjects that represent the individual characters from input_string.
    x
        The value that represents the instance's position on the x-axis.
    y
        The value that represents the instance's position on the y-axis.
    initial
        If the instance is an initial state or not.
    final
        If the instance is a final state or not.
    """
    def __init__(self, input_string: str, animation_style: dict, font_size: int = 100, **kwargs) -> None:

        super().__init__(**kwargs)

        self.animation_style = animation_style

        #token creation
        self.tokens = []
        spacing = 0
        for token_symbol in input_string:
            token_mobject = Token(token_symbol, spacing, font_size)
            

            self.add(token_mobject)
            self.tokens.append(token_mobject)

            spacing = spacing + 1

        

    @staticmethod
    def highlight_token(token, animation_style):
        """animation function"""
        animation_function = animation_style["token_highlight"]["animation_function"]
        color = animation_style["token_highlight"]["color"]

        return animation_function(token, color=color)
    

class Token(MathTex):

    id_iter = itertools.count()

    def __init__(self, token_symbol, spacing, font_size: int = 100, **kwargs) -> None:

        super().__init__(token_symbol, font_size=font_size, **kwargs)

        self.id = next(self.id_iter)

        self.set_x(0 + spacing)
        self.set_y(0)

        # self.text




    