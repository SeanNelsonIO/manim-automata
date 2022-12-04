from manim import *

from .manim_automaton import ManimAutomaton
# from .manim_state import ManimState, State
# from .manim_automaton_input import ManimAutomataInput
# from .manim_transition import ManimTransition

# from typing import Union

# import json
# import pprint

# import itertools

class ManimNonDeterminsticFiniteAutomaton(ManimAutomaton):

    nda_builder = False

    def __init__(self, json_template=None, xml_file=None, camera_follow=False, animation_style=None, cli=False, **kwargs) -> None:
        if animation_style is None:
            super().__init__(json_template, xml_file, camera_follow, cli=cli, **kwargs)
        else:
            super().__init__(json_template, xml_file, camera_follow, animation_style, cli=cli, **kwargs)

        if cli: #if cli exist display options to user
            self.cli.display_nda_options()
            if self.cli.nda_option == 0: #check the settings of the cli (what the user wants to do)
                self.nda_builder = True


#     def initialisation_animation(self, input: Union[str, "ManimAutomataInput"]) -> list:
#         """This method generates the animations that initialise the machine graphically.
#             The method specfically positions and animates the input string and highlights
#             the initial state"""

#         if type(input) is str:
#             #create mobject of input string
#             self.manim_automata_input = self.construct_automaton_input(input)
#             #position the mobject
#             self.set_default_position_of_input_string()
#             #display manim_automaton_input to the screen
#             list_of_animations.append(FadeIn(self.manim_automata_input))
#         else: self.manim_automata_input = input #if input is already an instance of ManimAutomataInput
        
#         #stores a list of animations that is returned to scene
#         list_of_animations = []
#         #Points to the current state
#         state_pointer = self.get_initial_state()
#         #Highlight current state with yellow
#         # list_of_animations.append([FadeToColor(state_pointer, color=YELLOW)])

#         return list_of_animations


#     def play_automaton_path(self, input, automaton_path: list[tuple]):
#         list_of_animations = self.initialisation_animation(input)

#         initial_state = self.get_initial_state()
        
#         if initial_state.name != automaton_path[0][0]: #check that the start of the path matches the initial state
#             pass #display erro

#         state_pointer = initial_state # Keeps track of all the states that are activated

#         for token, path_transition in zip(self.manim_automata_input.tokens, automaton_path):
#             current_state = state_pointer
#             current_state_transitions = current_state.transitions
#             if current_state.name == path_transition[0]: #if the current state matches the path_transition's from-state
#                 #check that the path_transition to-state exists and is valid
#                 for transition in current_state_transitions:
#                     if transition.transition_to.name == path_transition[1]:
#                         #check the transition has a read symbol that matches the input token
#                         if transition.check_transition_read_symbols(token):
#                             #generate animations
#                             # list_of_animations.append([FadeToColor(token, color=YELLOW)]) #highlights the current token
#                             state_pointer = self.play_predetermined_sequence(token, state_pointer, list_of_animations, predetermined_transition=transition)
#                             list_of_animations.append([token.animate.set_opacity(0.5)]) #animates that the token has been used
#                             break
#                         else:
#                             return False #transition does not have a matching read_symbol for the given token

#         #check if the language was accepted by the automaton
#         if self.check_automaton_result([state_pointer]): #if the automaton has an active accepting state
#             list_of_animations.append(self.generate_accept_animations())
#         else: #if there is no final state then the machine is not accepted.
#             list_of_animations.append(self.generate_reject_animations())

#         return list_of_animations
   

#     #Improving play string method
#     def play_predetermined_sequence(self, token, state_pointer, list_of_animations, predetermined_transition: "ManimTransition" = None) -> list[State]:
#         # step_result, next_neighbour_states, transition_ids = self.automaton_step(token, state_pointer, determinstic=False) #simulates the machine
#         step_result = True #determined by the calling function
#         list_of_animations.append(self.step(predetermined_transition, token, state_pointer, step_result))

#         next_neighbour_state = predetermined_transition.transition_to

#         list_of_animations.append([FadeToColor(state_pointer, color=BLUE)])
#         list_of_animations.append([FadeToColor(next_neighbour_state, color=YELLOW)])

#         next_state = next_neighbour_state

#         return next_state


#     def pick_transition(self, state_pointer, transitions):
#         path_options = self.generate_next_state_options(state_pointer, transitions)
#         user_choice = self.cli.display_dictionary_options(path_options)
#         transition = path_options[user_choice][1] #get transition given user choice

#         return [transition.transition_to], [transition]


#     #Implement branching in this method
#     def run_input_through_automaton(self, input: Union[str, "ManimAutomataInput"], automaton_path_name: str = None) -> list:
#         """
#         parameters:
#             automaton_path: provides a single path used to navigate through the nda, 
#             the purpose of this is to allow the user to animate a single path through
#             the nda instead of animating all of the branches that are created by the nda.
#         """
            
#         # example_structure = [("q0", "q1")]
#         # if this transition does not exist or the token does not match 
#         # then return error with the number of the tuple in the list
#         if automaton_path_name: # The nda will animate the predetermined path from the user
#             automaton_path = self.load_recorded_path_from_file(automaton_path_name)
#             return self.play_automaton_path(input, automaton_path) #create animations to do with given path
#         elif self.nda_builder: # Stores the path of of a single branch within the nda
#             self.recorded_path = []

#         #keeps track of what happend throughout each iteration
#         # global_history = {}

#         initial_state = self.get_initial_state()
#         # state_pointers = [initial_state] # Keeps track of all the states that are activated

#         initial_branch = Branch(initial_state)

#         self.all_branches = [initial_branch] #stores all the branches produced by non-determinism
#         #need a branch to start with
    
#         current_branches = self.all_branches

#         for i, token in enumerate(self.manim_automata_input.tokens):

#             current_branches = self.play_branches(token, current_branches)
           
        
#         #export the recorded path so the user can use it again without using nda builder
#         if self.nda_builder:
#             self.export_recorded_path_to_file()

#         #goes through each branch and records whether the branch is alive in the branche's history
#         for branch in self.all_branches:
#             branch.complete_branch()

#         #Resolve branches
#         chosen_branch_history = self.resolve_branches(self.all_branches, input) # picks a branch to generate an animation from

#         return chosen_branch_history

        
#     def play_branches(self, token, current_branches) -> list["Branch"]:
#         active_branches = []
#         for branch in current_branches: #loop though each branch and run one step
    
#             state_pointer = branch.state_pointer
#             result, next_states, transitions = self.automaton_step(token, state_pointer)

#             if self.nda_builder: #if nda_builder, only choose one path
#                 next_states, transitions = self.pick_transition(state_pointer, transitions)
           
#             # self.generate_animation_sequence(result, next_states, transitions, list_of_animations)
#             # self.play__sequence(token, result, state_pointer, next_states, transitions, list_of_animations) this generates the animations

#             # state_pointers = self.run_sequence(token, state_pointers, iteration_history) #goes through each state_pointer
            
#             new_branches = branch.step_through(result, next_states, transitions, token) #assign new state_pointer to current branch and create divergent branches(if any)

#             if result is False: #branch wasn't able to transition given a token, therefore language is rejected for branch.
#                 branch.reject()
            
#             active_branches = active_branches + new_branches # add any new branches to active branches

#             #add new branches to self.all_branches
#             for branch in new_branches:
#                 if branch not in self.all_branches:
#                     self.all_branches.append(branch)
            
#         return active_branches
    
#     #resolves all histories of each branch into one branch, display all branches
#     def resolve_branches(self, branches, input):
        
#         return self.merge_histories(branches, input)
    
#         for branch in branches:
#             if branch.alive == True and branch.state_pointer.final == True:
#                 pprint.pprint(branch.history)
#                 print("branch id:", branch.id, branch.alive)
#                 return branch.history

#         #merge all branches to display all branches
#         #use a super script or subscript to show how many branches are on a state
#         #if any branch passes then the machine passes
        
        

#     def merge_histories(self, branches, input):
#         #merge all the branch histories into an iteration history
#         automaton_result = False

#         global_history = {}
#         for token in input:
#             iteration_history = global_history.setdefault(token.id, {
#                 'iteration_history': [],
#                 'token': token
#                 })

#             for branch in branches:
#                 if token.id in branch.history:
#                     # print("THIS:::", branch.history[token.id])
#                     iteration_history["iteration_history"].append(branch.history[token.id]["iteration_history"][0])
#                     if branch.history["information"]["automaton_result"] == True:
#                         automaton_result = True


#         global_history["information"] = {
#             "automaton_result": automaton_result
#         }
                
        
#         #DEBUG
#         # pprint.pprint(branches[0].history)
#         # pprint.pprint(global_history)

#         return global_history


# class Branch():

#     id_iter = itertools.count()
#     # recorded_path: list #records the path/history of the branch TODO
#     # state_pointer: State #keeps track of the current state
#     # stack: list #pushdown automaton stack, each branch has its own stack
#     # history: list

#     def __init__(self, state_pointer, stack: list = None, history: dict = None, divergent: bool = False, branch_transition = None, result = None, token = None) -> None:
#         self.id = next(self.id_iter)
#         self.alive = True
#         # self.stack = stack
#         self.stack = []
#         if stack is not None:
#             self.stack = stack

#         self.history = {}
#         if history is not None:
#             self.history = history

#         self.state_pointer = state_pointer #stores the state that the branch is currently on

#         if divergent == True:
#             self.step_through(result, [branch_transition.transition_to], [branch_transition], token)
    
#     def step_through(self, result, next_states, transitions, token) -> list["Branch"]: #checks to see if branch diverges
#         new_branches = [] #stores the new divergent branches
#         #pick a state to continue this branch
#         if len(transitions) > 0:
#             chosen_transition = transitions.pop() #pops the last item in the list and continues the branch with this.


#             #every other possible path diverges into a new branch
#             for transition in transitions: #create branch for every other path
#                 new_branches.append(self.diverge_branch(transition, result, token)) # do we create two next branches or pick one to be branched?
            
            
#             #record the path of the current branch
#             self.record_history(result, [chosen_transition.transition_to], [chosen_transition], token)

#             #move the state_pointer to the next state
#             self.state_pointer = chosen_transition.transition_to

#             new_branches.append(self)

#         return new_branches

#     def diverge_branch(self, branch_transition, result, token) -> "Branch": #creates another branch of current branch
#         divergent = Branch(self.state_pointer, self.stack.copy(), self.history.copy(), divergent=True, branch_transition=branch_transition, result=result, token=token)
#         # divergent = Branch(next_state, self.stack.copy(), self.history.copy(), divergent=True)
#         return divergent

#     def reject(self) -> None: #branch did not accept string.
#         self.alive = False

#     def record_history(self, result, next_states, transitions, token) -> None:

#         # print(self.id, token.id, transitions)
#         iteraction_history = [{
#             "state_pointer": self.state_pointer,
#             "next_neighbour_states": next_states,
#             "transitions": transitions,
#             "result": result,
#             "token": token,
#             "branch_id": self.id
#         }]


#         self.history[token.id] = {
#             "token": token,
#             "iteration_history": iteraction_history
#         }

#     def __str__(self) -> str:
#         return 'Branch id: {self.id}'.format(self=self)

#     def complete_branch(self):
#         self.history["information"] = {
#             "alive": self.alive,
#             "automaton_result": self.check_branch_result()
#         }
        
#     def check_branch_result(self):
#         if self.alive == True and self.state_pointer.final == True:
#             return True
#         return False



