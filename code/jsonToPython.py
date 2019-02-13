# Nathaniel Linden
# Feb 12th 2019
#  CSE 160
""" The following code reads in the a .json file. And returns a list
of dictionaries, where each dictionary corresponds to each object in the .json
data file"""

import json
# take in attributes of interest form user
# create empty list to output
# loop through the .json file
# for each .json object query and create a ditionary with attributes of interest
# update list
# return list


def jsonToDict(fileName, attributes):
    """Converts .json file to python list of dictionaries.

    fileName - the .json file to be converted
    attributes - a tuple of attributes to include as key:value pairs

    Returns a list of dictionaries, where each dictionary corresponds to one
    onject in the .json file. The key:value pairs of the dictionary will
    be the attributes and corresponding values from the .json object
    """
    # check fileName is .json
    assert fileName[-5:] == '.json', 'The file inputted is not .json' + fileName

    jsonDict = {}
    for object in open(fileName, 'r'):
        objDict = json.loads(object)  # load on object from .json file as dict
        parsedObjDict = parseDict(objDict, attributes)


def parseDict(dictionary, attributes):
    

    return jsonDict
