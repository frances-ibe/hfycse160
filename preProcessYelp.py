""" The following code performs preprocessign of the yelp data used  for
the completion of our CSE 160 final project.
All supporting code and preprocessed data will be made available.

Authors: Frances Ingram-Bate, Parker Grosjean, Nathaniel Linden

Updated: March 8th 2019

Abbreviations (We will use these throughout the script):
-  zhvi - zillow homw value index
-  avgPrice - average restuarant price
-  yzi - yelp, zillow, IRS

The following code reads in the a .json file. And returns a list
of dictionaries, where each dictionary corresponds to each object in the .json
data file"""

import json
import pandas as pd
import os
# take in attributes of interest form user
# create empty list to output
# loop through the .json file
# for each .json object query and create a dictionary with attributes of interest
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


def filterBusinessCity(businessList, targetCity):
    """ This funciton will filter restaurants from a list of businesses from
    the yelp data

    The elements of businessList MUST contain the followign keys:
     "business_id", "city","postal_code", "stars", "attributes"
    """
    restaurantsList = []  # list to hold all restaurants from business list

    if targetCity == None:
        for business in businessList:  # loop through all restaurants
            # check for price range in attributes for restaurants only
            if business["attributes"] != None and business["postal_code"] is not "" and "RestaurantsPriceRange2" in business["attributes"].keys():
                # create a dicitonary with the desired attributes

                restAttr = {"business_id": business["business_id"], "city": business["city"],
                            "postalCode": business["postal_code"], "stars": business["stars"],
                            "price": business["attributes"]["RestaurantsPriceRange2"]}
                restaurantsList.append(restAttr)  # add business to rest list
    else:
        for business in businessList:  # loop through all restaurants
            # check for price range in attributes for restaurants only
            if business["attributes"] != None and business["postal_code"] is not "" and "RestaurantsPriceRange2" in business["attributes"].keys() and str(targetCity) == business["city"]:
                # create a dicitonary with the desired attributes
                restAttr = {"business_id": business["business_id"], "city": business["city"],
                            "postalCode": business["postal_code"], "stars": business["stars"],
                            "price": business["attributes"]["RestaurantsPriceRange2"]}
                # add business to rest list
                restaurantsList.append(restAttr)

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
    f.write("\n")

    for restaurant in restaurantsList:  # write csv from dict list
        for key in restaurantsList[0].keys():
            f.write(str(restaurant[key]) + ",")
        f.write("\n")

    f.close()  # close file

    return None


def CSVreader(filename):
    """Reads in filename and converts to pandas dataframe"""
    data = pd.read_csv(filename, delimiter=",")
    return data


def preProcess(filename="vegasRest", attributes_process=("business_id", "city", "postal_code", "stars", "attributes"), targetCity="Las Vegas"):
    """ Function to perform all desired preprocessing.
    """
    dictOfBussiness = jsonToDictList(r"business.json", attributes_process)
    restaurantFilteredDict = filterBusinessCity(dictOfBussiness, targetCity)
    restaurantsListToCSV(restaurantFilteredDict, filename)
    return None
