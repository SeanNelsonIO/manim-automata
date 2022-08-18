from asyncio import constants
from .xml_parser import parse_xml_file


from .state import State
from .transitition import Transition

import gc #need a way of getting instances of class without gc TODO
        
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


#this class manages states and transitions, including simulation
class FiniteStateAutomaton():
    states = []
    transitions = []
    
    def __init__(self):
        pass
    
    def process_xml(self, xml_file: str) -> None:
        self.construct_from_json(parse_xml_file(xml_file))

    def construct_from_json(self, json_dictionary: dict) -> None:
        #validate json
        #Function HERE
        #construction
        states = json_dictionary["structure"]["automaton"]["state"]
        transitions = json_dictionary["structure"]["automaton"]["transition"]
        
        self.construct_states(states)
        self.construct_transitions(transitions)
        

    #State Methods
    def get_initial_state(self) -> State:
        for state in self.states:
            if state.initial == True:
                return state

    def get_state(self, name) -> State:
        for state in self.states:
            if state.name == name:
                return state

    def get_state_by_id(self, id: int) -> State:
        for state in self.states:
            if state.id == id:
                return state

    def automaton_step(self, token: str, state_pointer: State, determinstic: bool = True) -> tuple:
        next_states = [] #stores all of the next states that can be jumped to
        transition_ids = [] #store the ids of the transitions that transition from current to next states.
        
        #go through each transition of this state
        state_transitions = state_pointer.get_transitions()
        for transition in state_transitions:
            #check if any transition's symbols match the input token
            for read_symbol in transition.read_symbols: #Iterate through the transtion's read options
                if read_symbol.tex_string == token.tex_string:
                    next_states.append(transition.transition_to)
                    transition_ids.append(transition.id)
                    if determinstic: #pick the first valid transition and next state then returns.
                        return True, next_states, transition_ids #the token matches the transition's input

        if len(next_states) != 0:
            return True, next_states, transition_ids #the token matches the transition's input

        return False, next_states, transition_ids #There are no other transitions/ reachable next states given the token





    #Transition Methods
    def get_transition_by_id(self, id: int) -> Transition:
        for transition in self.transitions:
            if transition.id == id:
                return transition
