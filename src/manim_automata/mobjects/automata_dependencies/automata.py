from .xml_parser import parse_xml_file
import itertools

import gc #need a way of getting instances of class without gc TODO

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

    def add_transition_to_state(self, transition: "Transition") -> None:
        self.links.append(transition)

    def get_transitions(self) -> list["Transition"]:
        return self.links

    def get_transition(self, index: int) -> "Transition": #DEPRECATED
        return self.links[index]

    @staticmethod
    def get_state_by_id(id): #need a much faster function TODO
        for obj in gc.get_objects():
            if isinstance(obj, State):
                if obj.id == id:
                    return obj

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

    def __init__(self, transition_from: State, transition_to: State, read_symbols: list) -> None:
        self.id = next(self.id_iter)
        self.transition_from = transition_from
        self.transition_to = transition_to
        self.read_symbols = read_symbols

        #when creating a transition add the transition to the states TODO

        

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
            json_template #extract states and transitions from template if valid
            result = FiniteStateAutomaton.validate_json_template(json_template)
            if result == False:
                return "Error, json template was not valid, ensure the json object follows the correct structure."
        elif xml_file:
            json_dictionary = parse_xml_file(xml_file)
        else: return False

        states = json_dictionary["structure"]["automaton"]["state"]
        transitions = json_dictionary["structure"]["automaton"]["transition"]
        
        self.construct_states(states)
        self.construct_transitions(transitions)
        

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


    def construct_states(self, states):
        #sort states, just in case they are not in order TODO
        for state in states:
                self.add_state(state)

    def construct_transitions(self, transitions: list[dict]) -> None: #function slow, REFACTOR!

        #counts the number of transitions between two states
        transition_counter = {}
        # for transition in self.automaton.transitions:
        #if 2 or more transitions exist between states then this will merge them together in one transition.
        for transition in transitions:
            """put from and to states into tuple to be used as
            dictionary key."""
            state_key = (transition['from'], transition['to'])
            
            
            transition_group = transition_counter.setdefault(state_key, [])#if key doesn't exist then create new key list pair
            transition_group.append(transition['read']) #append transition read value to transition[state_key]


        for state_key in transition_counter:
            self.add_transition(state_key, transition_counter[state_key])


    def add_transition(self, state_key: tuple, read_values: list) -> None:
        
        from_state = State.get_state_by_id(int(state_key[0]))
        to_state = State.get_state_by_id(int(state_key[1]))

        new_transition = Transition(from_state, to_state, read_values)
        self.transitions.append(new_transition)

        #add the transition to the from_states link list
        from_state.add_transition_to_state(new_transition)





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
            for read_symbol in transition.read_symbols: #Iterate through the transtion's read options
                if read_symbol == token.text: #currently we pick the first transition that matches if one exists, however this won't work for non-deterministic machines
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

    @staticmethod
    def validate_json_template(json_template):

        

        stripped_json_template = {

        }
        
        #strip json object to bare components to see if it has everything
        #then create a hash of the object and compare it to the correct template's hash


        pass

    def strip_json_template(dictionary):

        if type(key) != dict:
            return {} # build the dictionary back up


        return strip_json_function(value)
        pass
        
        

automaton_json = {
    'structure': {
        'type': 'fa',
        'automaton': {
            'state': [
                {'@id': '0', '@name': 'q0', 'x': '84.0', 'y': '122.0', 'initial': None},
                {'@id': '1', '@name': 'q1', 'x': '218.0', 'y': '175.0'},
                {'@id': '2', '@name': 'q2', 'x': '386.0', 'y': '131.0', 'final': None},
                {'@id': '3', '@name': 'q3', 'x': '227.0', 'y': '36.0'}
            ],
            'transition': [
                {'from': '0', 'to': '1', 'read': '0'},
                {'from': '0', 'to': '1', 'read': '1'},
                {'from': '2', 'to': '3', 'read': '0'},
                {'from': '1', 'to': '2', 'read': '1'},
                {'from': '3', 'to': '0', 'read': '1'},
                {'from': '3', 'to': '0', 'read': '0'}
            ]
        }
    }
}
# class PushdownAutomaton(Automaton): TODO
#     def __init__(self) -> None:
#         pass

#create error message here - need to look up standard. TODO