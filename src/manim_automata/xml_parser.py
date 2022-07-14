import json
import xmltodict

# from automata import deterministic_finite_automaton

def parse_xml_file(file_name):
    """
    Converts parses the xml from given file,
    then jsonify into a dictionary.
    """
    with open(file_name,'rb') as f:
        return xmltodict.parse(f)
 

#need some kind of validation of the dictionary
#Could build the automaton anyway and tell the user if it works or not.
def create_automaton_from_dictionary(dictionary):
    #create all the states
    #create all the transitions
    #create machine
    deterministic_finite_automaton = deterministic_finite_automaton(dictionary)



if __name__ == "__main__":

    #testing functions
    json_dictionary = parse_xml_file('testmachine.jff')
    if not isinstance(json_dictionary, dict):
        exit()


    states = json_dictionary["structure"]["automaton"]["state"]
    transitions = json_dictionary["structure"]["automaton"]["transition"]

    # print(transitions)

    deterministic_finite_automaton = deterministic_finite_automaton(states=states, transitions=transitions)

def initialise_automaton():
    #testing functions
    # json_dictionary = parse_xml_file('testmachine.jff')
    # if not isinstance(json_dictionary, dict):
    #     exit()


    # states = json_dictionary["structure"]["automaton"]["state"]
    # transitions = json_dictionary["structure"]["automaton"]["transition"]


    return deterministic_finite_automaton(xml_file='x_contains_a_1_in_third_final_position.jff')


    # print(states)
    # print(transitions)

    

    # print(list(find_key_in_dictionary(json_dictionary, "transition")))
    # print(list(gen_dict_extract("transition", json_dictionary)))


    

# def find_key_in_dictionary(dictionary, condition, path=None):

#     if path is None:
#         path = []    
#     # In case this is a dictionary
#     if isinstance(dictionary, dict):
#         for key, value in dictionary.items():
#             new_path = list(path)
#             new_path.append(key)
#             for result in find_key_in_dictionary(value, condition, path=new_path):
#                 yield result 

#             if condition == key:
#                 new_path = list(path)
#                 new_path.append(key)
#                 yield new_path 

#     # return path

# def gen_dict_extract(key, var):
#     if hasattr(var,'iteritems'):
#         for k, v in var.iteritems():
#             if k == key:
#                 yield v
#             if isinstance(v, dict):
#                 for result in gen_dict_extract(key, v):
#                     yield result
#             elif isinstance(v, list):
#                 for d in v:
#                     for result in gen_dict_extract(key, d):
#                         yield result