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


def jsonToDictList(fileName, attributes):
    """Converts .json file to python list of dictionaries.

    fileName - the .json file to be converted
    attributes - a tuple of attributes to include as key:value pairs

    Returns a list of dictionaries, where each dictionary corresponds to one
    onject in the .json file. The key:value pairs of the dictionary will
    be the attributes and corresponding values from the .json object
    """
    # check fileName is .json
    assert fileName[-5:] == '.json', 'The file inputted is not .json' + fileName

    dictList = []  # create empty list to store object dictionaries
    for object in open(fileName, 'r'):  # loop through .json objects
        objDict = json.loads(object)  # load on object from .json file as dict
        parsedObjDict = _parseDict(objDict, attributes)  # parse for attributes
        # parsedObjDict will  be none if objDict doesn not contain attributes
        if parsedObjDict is not None:
            dictList.append(parsedObjDict)  # update the dict list

    return dictList


def _parseDict(dictionary, attributes):
    """ Private funciton which returns a dictionary containing the key values
    pairs from dictionary with keys corresponding to the items in attributes.

    Returns a dictionary if all of the attributes are keys in the dicitonary
    Returns None if an attribute is not contained in the dictionary

    To Do: fix conversion of attributes tuple to list 2/13/19
    """
    try:
        # use list comprehension to return list of values from the attributes
        valuesList = [dictionary[key] for key in attributes]
    except KeyError:  # if a given attribute not in the dictionary return None
        return None

    return dict(zip(keysList, valuesList))  # return a dictionary
