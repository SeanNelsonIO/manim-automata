class Automata:
    """
    Abstarct class providing attributes and methods for automatas

    ...

    Attributes
    ----------
    states : float
        States of automata.
    transitions :
        Transitions of between states
    Methods
    -------
    colorspace(c='rgb')
        Represent the photo in the given colorspace.
    gamma(n=1.0)
        Change the photo's gamma exposure.

    """

    def __init__(self) -> None:
        """ """
        pass

    def __init__(self, states, transitions):
        states = states
        transitions = transitions

    # def __setattr__(self, __name: str, __value: Any) -> None:
    #     self.__dict__[__name] = __value

    # def __getattribute__(self, __name: str) -> Any:
    #     return self.__dict__[__name]
    # look into these please.
