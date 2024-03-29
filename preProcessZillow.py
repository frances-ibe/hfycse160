""" The following code performs data preprocessing  of the zillow dataset
for the completion of our CSE 160 final project.
All supporting code and preprocessed data will be made available.

Authors: Frances Ingram-Bate, Parker Grosjean, Nathaniel Linden

Updated: March 8th 2019

Abbreviations (We will use these throughout the script):
-  zhvi - zillow homw value index
-  avgPrice - average restuarant price
-  yzi - yelp, zillow, IRS

 The following code reads the zillow housing data from its original
form to a new csv with only the attributes of interest for our analysis."""

"""


# importing neccessary modules
import pandas as pd
from pandas import DataFrame


def readInData(fileName):
    """ This function takes a csv filename and creates a dataframe containing columns
    for city, zhvi, and RegionName"""
    outputDF = pd.read_csv(fileName, usecols=["City","Zhvi","RegionName"], encoding='utf8')
    return outputDF


def usefulDict(zillowDF, targetCity):
    """This function takes the zillow data frame created using
    the readInData function and returns a dictionary with postal
    codes as keys and ZHVIs as values filtered only for a specified
    target city."""
    output_dict = {}  # creating dictionary
    if targetCity == None:
        for row in range(zillowDF.shape[0]):
            output_dict[zillowDF["RegionName"][row]] = zillowDF["Zhvi"][row]
    else:
        for row in range(zillowDF.shape[0]):
            if zillowDF["City"][row] == str(targetCity):
                output_dict[zillowDF["RegionName"][row]] = zillowDF["Zhvi"][row]
    return output_dict


def dictToCSVDF(zillow_dict, cols=("postalCode", "zhvi")):
    """This function takes in the dictionary with data of interest and generates
    a data frame with from the keys and values in the dictionary"""

    d = {}  # creating a dictioary to create dataframe
    postCodes = []  # These two lists are the columns of dataframe
    zhviList = []
    for key in zillow_dict.keys():
        # this for loop generates fills the dictionary to create the dataframe
        postCodes.append(key)
        zhviList.append(zillow_dict[key])

    d[cols[0]] = postCodes
    d[cols[1]] = zhviList
    zillowDF = pd.DataFrame(data=d)
    return zillowDF


def zillowCSVWrite(zillowDataFrame, fileName="vegasHousing"):
    """This function takes in the output from zillowForCSV and a filename without
    the CSV extention and writes a CSV file from the data frame with the postal
    codes and zhvi"""

    zillowDataFrame.to_csv(str(fileName) + '.csv')
    return None

def zillPreProcess(fileNameIn, fileNameOut="vegasHousing", targetCity="Las Vegas"):
    """This function takes in the filename of the csv with zillow data as fileNameIn
    and takes in a fileNameOut and then also takes in a targetCity that is default
    to Las Vegas

    Returns: the dataframe which is saved to the .csv
    """
    zillowDF1 = readInData(fileNameIn)
    zillowDict1 = usefulDict(zillowDF1, targetCity)
    zillowDF2 = dictToCSVDF(zillowDict1)
    zillowCSVWrite(zillowDF2, fileName=fileNameOut)
    return zillowDF2

def zipcodeList(fileNameIn="Zip_Zhvi_Summary_AllHomes.csv", targetCity="Las Vegas"):
    """This Function takes in the fileNameIn of the csv with the zillow data in it
    and the targetCity that is default set to Las Vegas and returns list of
    postal codes from the las vegas city that is used when generating the IRS data"""
    zillowDF1 = readInData(fileNameIn)
    zillowDict1 = usefulDict(zillowDF1, targetCity)
    outputList = list(zillowDict1.keys())
    return outputList
