# Nathaniel Linden, Parker Grosjean, Frances Ingram-Bate
# Feb 12th 2019
# CSE 160
""" The following code reads the zillow housing data from its original
form to a new csv with only the attributes of interest for our analysis."""

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


def dictToCSVDF(zillow_dict):
    """This function takes in the dictionary with data of interest and generates
    a data frame with from the keys and values in the dictionary"""

    d = {}  # creating a dictioary to create dataframe
    postCodes = []  # These two lists are the columns of dataframe
    zhviList = []
    for key in zillow_dict.keys():
        # this for loop generates fills the dictionary to create the dataframe
        postCodes.append(key)
        zhviList.append(zillow_dict[key])

    d["postalCode"] = postCodes
    d["zhvi"] = zhviList
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
    to Las Vegas"""
    zillowDF1 = readInData(fileNameIn)
    zillowDict1 = usefulDict(zillowDF1, targetCity)
    zillowDF2 = dictToCSVDF(zillowDict1)
    zillowCSVWrite(zillowDF2, fileName=fileNameOut)
    return None

def zipcodeList(fileNameIn="Zip_Zhvi_Summary_AllHomes.csv", targetCity="Las Vegas"):
    """This Function takes in the fileNameIn of the csv with the zillow data in it
    and the targetCity that is default set to Las Vegas and returns list of
    postal codes from the las vegas city that is used when generating the IRS data"""
    zillowDF1 = readInData(fileNameIn)
    zillowDict1 = usefulDict(zillowDF1, targetCity)
    outputList = list(zillowDict1.keys())
    return outputList
