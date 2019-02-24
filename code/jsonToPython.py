# Nathaniel Linden
# Feb 12th 2019
#  CSE 160
""" The following code reads in the a .json file. And returns a list
of dictionaries, where each dictionary corresponds to each object in the .json
data file"""

import json
import pandas as pd
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
    assert fileName[-5:] == ".json", "The file inputted is not .json" + fileName

    dictList = []  # create empty list to store object dictionaries
    jsonFile = open(fileName, "r", encoding="utf8")  # open json File
    for object in jsonFile:  # loop through .json objects
        objDict = json.loads(object)  # load on object from .json file as dict
        parsedObjDict = _parseDict(objDict, attributes)  # parse for attributes
        # parsedObjDict will  be none if objDict doesn not contain attributes
        if parsedObjDict is not None:
            dictList.append(parsedObjDict)  # update the dict list

    jsonFile.close()

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

    return dict(zip(attributes, valuesList))  # return a dictionary


dictForCSV = jsonToDictList(
    r"business.json", ("name", "city", "postal_code", "stars", "attributes"))


def filterBusinessCity(businessList):
    """ This funciton will filter restaurants from a list of businesses from
    the yelp data

    The elements of businessList MUST contain the followign keys:
     "name", "city","postal_code", "stars", "attributes"
    """
    restaurantsList = []  # list to hold all restaurants form business list

    for business in in businessList:  # loop through all restaurants
        # check for price range in attributes for restaurants only
        if "RestaurantsPriceRange2" in business[4].keys():
            # create a dicitonary with the desired attributes
            restAttr = {"name": business["name"], "city" : business["city"],
            "postal_code": business["postal_code"], "stars": business["stars"],
            "RestaurantsPriceRange2" : business["attribute"]["RestaurantsPriceRange2"]
            restaurantsList.append(restAttr)  # add business to rest list
    return restaurantsList


def restaurantsListToCSV(restaurantsList, filename):
    """ Creates a CSV file containing the data in restaurantsList with the
    name given from filename

    restaurantsList: a list of dictionaries which all contain the same keys
    filename: must be a string type
    """
    f = open(filename + ".csv", "w")  # create file

    for item in restaurantsList[0].keys():  # create a header line
        f.write(str(item) + ",")

    for restaurant in restaurantsList: # write csv from dict list
        for key in restaurantsList[0].keys():
            f.write(str(restaurant[key]) + ",")

    f.close() # close file


def CSVreader(filename):
    """Reads in filename and converts to pandas dataframe"""
    data = pd.read_csv(filename, delimiter=",")
    return data

def filterByCity(data, targetCity):
    """Filter restaurant data by city, returning df with only dat for one city"""

    if data["city"] == targetCity:


# dataFrameForCSV = pd.DataFrame.from_dict(dictForCSV)
# dataFrameForCSV2 = pd.DataFrame.from_dict(dictPricePoint)
# dataFrameForCSV.append(dataFrameForCSV2)
#
# writing CSV file with data from Yelp .json archive
# yelpBusinessData = dataFrameForCSV.to_csv(r"yelpBusinessData.csv", index = None, header = True)
#
# yelpData = open('yelpData.csv','w')
# for item in dictForCSV[0].keys():
#    yelpData.write(str(item))
#    yelpData.write(',')
# yelpData.write('\n')
# for ph in range(dictForCSV.keys()):
#    for dictionary in dictForExcel[ph].keys():
