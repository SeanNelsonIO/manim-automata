from manim import *

from .manim_automaton import ManimAutomaton
from .manim_state import ManimState, State
from .manim_automaton_input import ManimAutomataInput
from .manim_transition import ManimTransition


from typing import Union

class ManimDeterminsticFiniteAutomaton(ManimAutomaton):

    def __init__(self, json_template=None, xml_file=None, camera_follow=False, animation_style=None, cli=False, **kwargs) -> None:
        if animation_style is None:
            super().__init__(json_template, xml_file, camera_follow, cli=cli, **kwargs)
        else:
            super().__init__(json_template, xml_file, camera_follow,  animation_style, cli=cli, **kwargs)

        if cli: #if cli exist display options to user
            self.cli.display_nda_options()
            if self.cli.nda_option == 0: #check the settings of the cli (what the user wants to do)
                self.nda_builder = True