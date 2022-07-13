from manim import *
# from src.manim_automata.automata import deterministic_finite_automaton, Transition, State

# __all__ = ["State"]
# from src.manim_automata.mobjects.automaton_mobject import ManimTransition, ManimState
# import src.manim_automata.mobjects.automaton_mobject as a



class AnimateStep(Transform):
    def __init__(self, transition1, transition2) -> None:


        super().__init__(transition1, transition2)

# class TransitionStep(Animation):
#     def __init__(self, mobject_transition, token, **kwargs) -> None:
#         self.get


#         super().__init__(mobject, **kwargs)

    
# class PlayString():
#     def __init__(self) -> None:
#         pass