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

    def __init__(self, id: int, name: str, x: int, y: int, initial: bool = None, final: bool = None):
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.initial = initial
        self.final = final

        #list of states that this state is linked to
        self.links = []
        


        #need some logic here for initial and final

    def add_transition(self, transition_to, read_symbols):
        self.links.append((transition_to, read_symbols))
        pass

# class Transition:
#     # input_symbols = list[str]
#     # transition_link = tuple[int]
#     def __init__(self, transition_from: int, transition_to: int, input_symbols: str):
#         self.transition_from = transition_from
#         self.transition_to = transition_to
#         self.input_symbols = input_symbols

#     # def transition(self):
#     #     pass


class deterministic_finite_automaton:
    states = []
    # transitions = []

    def __init__(self, template=None, states=None, transitions=None):
        if template:
            pass
        else:
            for state in states: #create states
                self.add_state(state)

            self.add_transitions(transitions)


    def add_state(self, state: dict):
        #check if initial is set in state
        #check if final exist in state
        self.states.append(State(state["@id"], state["@name"], state["x"], state["y"]))

    def add_transitions(self, transitions: list[dict]): #function slow, REFACTOR!
        #go through each transition, fetch the corresponding state and add the transition to state
        for transition in transitions:
            # fetch from state
            for state in self.states:
                if state.id == transition['from']:
                    # create transition on state
                    state.add_transition(transition['to'], transition['read'])
                    break

    def run(self, input_string: list[str]):
        validation_response = self.validate_automaton() #returns tuple (bool, message)
        if validation_response[0] == False:
            return validation_response[1]
        
        for symbol in input_string:
            self.step(symbol)

    
    # def step(self, input_sybol: str, transition: Transition):
    #     pass

    def validate_automaton(self): #checks to see if automaton can run
        #check if there is an initial state
        response = []
        for state in self.states:
            if state.inital:
                break

        #check there is atleast one final state
        for state in self.states:
            if state.inital:
                break

        pass

class input_string():
    pass


class alphabet():
    pass





