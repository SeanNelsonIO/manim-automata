import itertools

class State:
    """Class that represents states.

    Parameters
    ----------
    name
        The class' name.
    initial
        The class' state type, in terms of initial state.
    final
        the class' state type, in terms of final state.

    Attributes
    ----------
    id
        The instance's id.
    name
        The class' name.
    initial
        If the instance is an initial state or not.
    final
        If the instance is a final state or not.
    """

    id_iter = itertools.count()

    def __init__(self, name: str, initial: bool = None, final: bool = None) ->  None:
        self.id = next(self.id_iter)
        self.name = name
        self.initial = initial
        self.final = final

        #list of transitions links this state to others
        self.links = []

    def add_transition_to_state(self, transition: "Transition") -> None:
        self.links.append(transition)

    def get_transitions(self) -> list["Transition"]:
        return self.links

    def get_transition(self, index: int) -> "Transition": #DEPRECATED
        return self.links[index]

    def __str__(self) -> str:
        return 'State id: {self.id}, name: {self.name}'.format(self=self)