# from lxml import etree

# from io import StringIO, BytesIO

# # print("running with cElementTree")

# xml_test = """<structure>
# 	<type>fa</type>
# 	<automaton>
# 		<!--The list of states.-->
# 		<state id="0" name="q0">
# 			<x>24640.0</x>
# 			<y>21780.0</y>
# 		</state>
# 		<state id="1" name="q1">
# 			<x>92.0</x>
# 			<y>120.0</y>
# 			<initial/>
# 		</state>
# 		<state id="2" name="q2">
# 			<x>170.0</x>
# 			<y>134.0</y>
# 		</state>
# 		<state id="3" name="q3">
# 			<x>238.0</x>
# 			<y>142.0</y>
# 			<final/>
# 		</state>
# 		<!--The list of transitions.-->
# 		<transition>
# 			<from>1</from>
# 			<to>1</to>
# 			<read>0</read>
# 		</transition>
# 		<transition>
# 			<from>2</from>
# 			<to>3</to>
# 			<read>0</read>
# 		</transition>
# 		<transition>
# 			<from>1</from>
# 			<to>2</to>
# 			<read>1</read>
# 		</transition>
# 	</automaton>
# </structure>"""

# tree = etree.parse(StringIO(xml_test))
# print_tree = etree.tostring(tree.getroot())
# print(print_tree)
# # tree = etree.parse(StringIO("testmachine.jff"))

# # etree.tostring(tree.getroot())
import json
import xmltodict



def parse_xml_file(file_name):
    """
    Converts parses the xml from given file,
    then jsonify into a dictionary.
    """
    with open(file_name,'rb') as f:
        return json.dumps(xmltodict.parse(f))
 

if __name__ == "__main__":
    json_dictionary = parse_xml_file('testmachine.jff')