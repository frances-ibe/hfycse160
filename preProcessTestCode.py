""" The following code tests basic preprocessing functions we forstatistical
testing for the completion of our CSE 160 final project.
All supporting code and preprocessed data will be made available.

Authors: Frances Ingram-Bate, Nathaniel Linden, Parker Grossjean

Updated: March 7th 2019

Abbreviations (We will use these throughout the script):
-  zhvi - zillow homw value index
-  avgPrice - average restuarant price
-  yzi - yelp, zillow, IRS

Note: This code is requrires the preprocessed data files, alongside the geoJSON
file in the same directory in order to compile.
"""
# imports
import numpy as np
import preProcessIRS as ppI
import preProcess as ppY
import preProcessZillow as ppZ
import pandas as pd

### Test Yelp Preprocessing ###
# We created a mini yelp dataset containing one yelp data objects. The
# code should filter for resturantes and return the exact info in the tester data.
#
# There tester file is called: testYelp.json

testDictList = ppY.jsonToDictList('testerYelp.json', ("business_id", "city", "postal_code", "stars", "attributes"))
expectedDictList = [{"business_id":"6fPQJq4f_yiq1NHn0fd11Q","city":"Las Vegas","postal_code":"89109","stars":3.5,"attributes":{"RestaurantsTakeOut":"True","RestaurantsDelivery":"False","RestaurantsGoodForGroups":"True","RestaurantsAttire":"'casual'","Ambience":"{'romantic': False, 'intimate': False, 'touristy': False, 'hipster': False, 'divey': False, 'classy': False, 'trendy': False, 'upscale': False, 'casual': True}","OutdoorSeating":"False","BYOBCorkage":"'yes_free'","Caters":"False","GoodForKids":"True","RestaurantsPriceRange2":"2","Corkage":"False","WiFi":"'no'","NoiseLevel":"u'average'","Alcohol":"'none'","RestaurantsReservations":"False","BusinessParking":"{'garage': True, 'street': False, 'validated': False, 'lot': False, 'valet': False}","HasTV":"False","BikeParking":"False","GoodForMeal":"{'dessert': True, 'latenight': False, 'lunch': True, 'dinner': False, 'brunch': False, 'breakfast': True}","BusinessAcceptsCreditCards":"True"}}]


testDictListCompare = [list(dict.items()) for dict in testDictList]
expectedDictListCompare = [list(dict.items()) for dict in expectedDictList]

# test if the preProcessing code correctly grabs desired attributes
assert(testDictListCompare == expectedDictListCompare)

# ensure that we can filter based on city
assert(ppY.filterBusinessCity(testDictList, "Moo Town") == [])


### Test IRS PreProcessing ###
# We created a mini IRS dataset containing one IRS zipcode entry.
# The average income in that zip code was manuallt coputed and compared to our
# algorithm to ensure algorithm precision

preProcessVal = ppI.preProcess('16zp29nv.csv',[89109])
expectedVal = {89109:np.round((1387614*1000)/7140, 10)}

assert(list(preProcessVal.values()) == list(expectedVal.values()))
assert(list(preProcessVal.keys()) == list(expectedVal.keys()))

### Test Zillow Preprocessing ###
# We created a mini zillow dataset containing one zillow entries.
# We compared the output to expected outputs

df = ppZ.zillPreProcess('testerZillow.csv', fileNameOut='testOut')

# check postal codes are correct
assert(sorted(list(df["postalCode"])) == [89117, 89121, 89147])

# check zhvi are correct
assert(sorted(list(df["zhvi"])) == [228200, 279000, 333600])
