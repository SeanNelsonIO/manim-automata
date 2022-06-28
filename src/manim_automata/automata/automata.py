from xmlrpc.client import boolean


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


class State:
    def __init__(self, name: str, x: int, y: int, initial: bool, final: bool):
        self.name = name
        self.x = x
        self.y = y
        self.initial = initial
        self.final = final
        #need some logic here for initial and final

class Transition:
    input_symbols = list[str]
    transition_link = tuple[int]

    def __init__(self, transition: transition_link, read: input_symbols):
        self.transition = transition
        self.read = read

    def transition(self):
        pass


class deterministic_finite_automaton():
    states = []
    transitions = []

    def __init__(self, template):

        pass

    def add_transition(self, transition: Transition):
        self.transitions.append(transition)

    def add_state(self, state: State):
        self.states.append(state)

    def run(self, input_string: list[str]):
        validation_response = self.validate_automaton() #returns tuple (bool, message)
        if validation_response[0] == False:
            return validation_response[1]
        
        for symbol in input_string:
            self.step(symbol)

        pass
    
    def step(self, input_sybol: str, transition: Transition):
        pass

    def validate_automaton(): #returns true if automaton is correct.
        #check only one initial state
        #check there is atleast one final state
        pass

class input_string():
    pass


class alphabet():
    pass





