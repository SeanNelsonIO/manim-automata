import itertools

from .state import State

class Transition:
    """Class that represents transitions between states.

    Parameters
    ----------
    transition_from
        Json object that describes an automaton.
    transition_to
        Path of XML format file describing an automaton.
    input_symbol
        The class' input symbol.
    Attributes
    ----------
    id
        The instance's id.
    transition_from
        The state where the transition begins.
    transition_to
        The state where the transition ends.
    input_symbol
        The symbols that the transition requires.
    """
    id_iter = itertools.count()


    def __init__(self, transition_from: State, transition_to: State) -> None:
        self.id = next(self.id_iter)
        self.transition_from = transition_from
        self.transition_to = transition_to

        