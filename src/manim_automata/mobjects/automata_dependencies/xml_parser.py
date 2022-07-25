import json
import xmltodict

def parse_xml_file(file_name):
    """
    Converts parses the xml from given file,
    then jsonify into a dictionary.
    """
    with open(file_name,'rb') as f:
        return xmltodict.parse(f)