# Nathaniel Linden
# Code to preprocess the IRS data
import pandas as pd


def preProcess(filename, zipList):
    """ Takes in a CSV of IRS SOI Tax Data and a list of zipcodes to analyze and
    returns a dicitonary mapping the zipcode to the average household income in
    that zipcode region """
    # read in CSV  # load data into dataframe only need columns 0, 2 and 16
    # column 0 - Zipcode, column 2 - number of tax returns, column 16 - AGI
    df = pd.read_csv(filename, usecols=[0,2,16], skiprows=3, skipfooter=17,engine='python')

    return _zipCodeIncmeAvg(zipList, df)


# get zip list
# get average income for zip code
def _zipCodeIncmeAvg(zipList, dfIRS):
    """ Computes average income per zipcode

    Returns a dictionary
    ziplist - list of zipcodes to ananlyze
    dfIRS - pandas dataframe of required IRS SOI data """
    zippedIncomes = {}  # empty dictionary to hold answers
    # convert df to list of tuples
    tupListIRS = list(dfIRS.itertuples(index=False, name=None))
    for zip in zipList:  # loop through all zipcodes
        # get list of all incomes for that zip code from all data
        # use strNumToInt to convert to ints from strings
        if zip in [zip for zip in tupListIRS[0]]:
            agiList = [[_strNumToInt(val[1]), _strNumToInt(val[2])]
                       for val in tupListIRS if val[0] == zip]
            print([val[0] for val in agiList if val is not []])
            avgAgi = sum([val[1] for val in agiList if val != []]) / sum([val[0] for val in agiList if val != []])
            # update dicitonary with zipcodes and avg income
            zippedIncomes[zip] = avgAgi * 1000  # account for fact that spreadsheet is in 1000s of dollars
    return zippedIncomes


def _strNumToInt(string):
    """ Private funciton to convet a string representaiton of a number to an int
    Removes commas associated with number places."""
    return int(string.replace(',', ''))  # return int of string number w/o comma

    # sort ziplist ascending
    # loop through all zipcodes in ziplist
    # start counting through the df with an interator
    # while current zip equals the zip from ziplist
# maybe use a while loop nested inside a for loop
# convert back to parsed csv
