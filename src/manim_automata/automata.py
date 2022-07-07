from re import L
from xmlrpc.client import boolean
from .xml_parser import parse_xml_file

# class Automata:
#     """
#     Abstract class providing attributes and methods for automatas
#     ...

#     Attributes
#     ----------
#     states : float
#         States of automata.
#     transitions :
#         Transitions of between states
#     Methods
#     -------
#     colorspace(c='rgb')
#         Represent the photo in the given colorspace.
#     gamma(n=1.0)
#         Change the photo's gamma exposure.

#     """

#     def __init__(self) -> None:
#         """ """
#         pass

#     def __init__(self, states, transitions):
#         states = states
#         transitions = transitions




class State:
    def __init__(self, id: int, name: str, x: int, y: int, initial: bool = None, final: bool = None):
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.initial = initial
        self.final = final

        #list of transitions links this state to others
        self.links = []

    def add_transition(self, transition):
        self.links.append(transition)

    def get_transitions(self):
        return self.links

    def get_transition(self, index: int): #DEPRECATED
        return self.links[index]

    def __str__(self) -> str:
        return 'State id: {self.id}, name: {self.name}'.format(self=self)

class Transition:
    transition_counter = 0

    def __init__(self, transition_from: State, transition_to: State, input_symbol: str, transition_id: int):
        self.id = transition_id
        self.transition_from = transition_from
        self.transition_to = transition_to
        self.input_symbol = input_symbol

        #when creating a transition add the transition to the states

    def generate_id(self):
        self.transition_counter = self.transition_counter + 1
        return self.transition_counter
        



class deterministic_finite_automaton:
    states = []
    transitions = []
    
    transition_counter = 0

    def __init__(self, template=None, states=None, transitions=None, xml_file=None):
        if template:
            pass #extract states and transitions from template if valid
        elif xml_file:
            json_dictionary = parse_xml_file(xml_file)
            if not isinstance(json_dictionary, dict):
                exit()

            states = json_dictionary["structure"]["automaton"]["state"]
            transitions = json_dictionary["structure"]["automaton"]["transition"]

            for state in states: #create states
                self.add_state(state)

            self.add_transitions(transitions)

        elif states and transitions:
            for state in states: #create states
                self.add_state(state)

            self.add_transitions(transitions)
        
        else: return False
        

    def add_state(self, state: dict):
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
        self.states.append(State(state["@id"], state["@name"], state["x"], state["y"], initial=initial, final=final))

    def add_transitions(self, transitions: list[dict]): #function slow, REFACTOR!
        #go through each transition, fetch the corresponding state and add the transition to state
        for transition in transitions:
            #get states
            from_state = None
            to_state = None
            transition_symbols = transition['read']

            for state in self.states:
                if state.id == transition['from']:
                    from_state = state
                if state.id == transition['to']:
                    to_state = state

            if from_state and to_state: #if states exist create transition
                self.transition_counter = self.transition_counter + 1 #generates ids for transitions (REPLACE) TODO
                new_transition = Transition(from_state, to_state, transition_symbols, self.transition_counter)
                self.transitions.append(new_transition)
                print(new_transition.id)
                #add the transition to the from_states link list
                from_state.add_transition(new_transition)

    def run(self, input_string: str):
        current_state = self.get_initial_state() #initial state is the first state in sequence
        current_transitions = current_state.get_transitions()
        for transition in current_transitions:
            current_state = self.step(input_string, current_transitions, current_state)
        


        #need to define the branches and accept
        if current_state.final == True:
            return True
        return False #The last state was not a final state, therefore the string is rejected.


    def step(self, token: str, state_pointer: State):
        next_state = None
        state_transitions = state_pointer.get_transitions()
        #go through each transition of this state
        for transition in state_transitions:
            #check if any transition's symbols match the input token
            if transition.input_symbol == token.text: #currently we pick the first transition that matches if one exists, however this won't work for non-deterministic machines
                next_state = transition.transition_to
                return True, next_state, transition.id #the token matches the transition's input
                
            
            
        return False, next_state, None

    def get_initial_state(self):
        for state in self.states:
            if state.initial == True:
                return state

    def get_state(self, name):
        for state in self.states:
            if state.name == name:
                return state
        #create error message here - need to look up standard.

    # def generate_transition_branches(self): #this seams like a NFA
    #     #Some input_strings may create different branches as a state may have mulitple transitions
    #     #where the transitions consume variable lengths of the input string, resulting in branches
    #     #These branches will execute different paths, where the String is accepted.
    #     # do this count as non-determinism? ask Sam
    #     pass

    # def validate_automaton(self): #checks to see if automaton can run
    #     #check if there is an initial state
    #     response = []
    #     for state in self.states:
    #         if state.inital:
    #             break

    #     #check there is atleast one final state
    #     for state in self.states:
    #         if state.inital:
    #             break

    #     pass

