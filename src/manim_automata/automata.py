from .xml_parser import parse_xml_file
import itertools

class State:
    """Class that represents states.

    Parameters
    ----------
    name
        The class' name.
    x
        The class' position on the x-axis.
    y
        The class' position on the x-axis.
    initial
        The class' state type, in terms of initial state.
    final
        the class' state type, in terms of final state.

    Attributes
    ----------
    id
        The instance's id.
    x
        The value that represents the instance's position on the x-axis.
    y
        The value that represents the instance's position on the y-axis.
    initial
        If the instance is an initial state or not.
    final
        If the instance is a final state or not.
    """

    id_iter = itertools.count()

    def __init__(self, name: str, x: int, y: int, initial: bool = None, final: bool = None) ->  None:
        self.id = next(self.id_iter)
        self.name = name
        self.x = x
        self.y = y
        self.initial = initial
        self.final = final

        #list of transitions links this state to others
        self.links = []

    def add_transition(self, transition: "Transition") -> None:
        self.links.append(transition)

    def get_transitions(self) -> list["Transition"]:
        return self.links

    def get_transition(self, index: int) -> "Transition": #DEPRECATED
        return self.links[index]

    def __str__(self) -> str:
        return 'State id: {self.id}, name: {self.name}'.format(self=self)

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

    def __init__(self, transition_from: State, transition_to: State, input_symbol: str) -> None:
        self.id = next(self.id_iter)
        self.transition_from = transition_from
        self.transition_to = transition_to
        self.input_symbol = input_symbol

        #when creating a transition add the transition to the states
        

class Automaton:
    def __init__(self) -> None:
        pass


class FiniteStateAutomaton(Automaton):
    """Class that represents finite state machines, including DFAs and NFAs.

    Parameters
    ----------
    json_template
        Json object that describes an automaton.
    xml_file
        Path of XML format file describing an automaton.
    Attributes
    ----------
    states
        List of State instances.
    transitions
        List of Transition instances.
    """
    states = []
    transitions = []

    def __init__(self, json_template=None, xml_file=None) -> None:
        if json_template:
            pass #extract states and transitions from template if valid
        elif xml_file:
            json_dictionary = parse_xml_file(xml_file)
            if not isinstance(json_dictionary, dict):
                exit()

            states = json_dictionary["structure"]["automaton"]["state"]
            transitions = json_dictionary["structure"]["automaton"]["transition"]
            
            #sort states, just in case they are not in order TODO

            for state in states: #create states
                self.add_state(state)

            self.add_transitions(transitions)
        
        else: return False
        

    def add_state(self, state: dict) -> None:
        #check if initial is set in state
        initial = False
        final = False
        if 'initial' in state.keys():
            initial = True 
            #check to see if there is already another initial state
            for state_object in self.states:
                if state_object.initial == True: #If there already exists an initial state set back to False and keep first initial state
                    initial = False
            
        if 'final' in state.keys():
            final = True

        #check if final exist in state
        self.states.append(State(state["@name"], state["x"], state["y"], initial=initial, final=final))

    def add_transitions(self, transitions: list[dict]) -> None: #function slow, REFACTOR!
        #go through each transition, fetch the corresponding state and add the transition to state
        for transition in transitions:
            #get states
            from_state = None
            to_state = None
            transition_symbols = transition['read']

            for state in self.states:
                if state.id == int(transition['from']):
                    from_state = state
                if state.id == int(transition['to']):
                    to_state = state

            if from_state and to_state: #if states exist create transition
                new_transition = Transition(from_state, to_state, transition_symbols)
                self.transitions.append(new_transition)
                #add the transition to the from_states link list
                from_state.add_transition(new_transition)

    def run(self, input_string: str) -> bool:
        current_state = self.get_initial_state() #initial state is the first state in sequence
        current_transitions = current_state.get_transitions()
        for transition in current_transitions:
            current_state = self.step(input_string, current_transitions, current_state)
        


        #need to define the branches and accept
        if current_state.final == True:
            return True
        return False #The last state was not a final state, therefore the string is rejected.


    def step(self, token: str, state_pointer: State) -> tuple:
        next_state = None
        state_transitions = state_pointer.get_transitions()
        #go through each transition of this state
        for transition in state_transitions:
            #check if any transition's symbols match the input token
            if transition.input_symbol == token.text: #currently we pick the first transition that matches if one exists, however this won't work for non-deterministic machines
                next_state = transition.transition_to
                return True, next_state, transition.id #the token matches the transition's input
                
        return False, next_state, None

    def get_initial_state(self) -> State:
        for state in self.states:
            if state.initial == True:
                return state

    def get_state(self, name) -> State:
        for state in self.states:
            if state.name == name:
                return state
        #create error message here - need to look up standard. TODO

# class PushdownAutomaton(Automaton): TODO
#     def __init__(self) -> None:
#         pass


