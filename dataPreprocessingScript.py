""" The following code performs data preprocessing for the completion of
our CSE 160 final project. All supporting code and preprocessed data will be
made available.

Authors: Frances Ingram-Bate, Parker Grosjean, Nathaniel Linden

Updated: March 8th 2019

Abbreviations (We will use these throughout the script):
-  zhvi - zillow homw value index
-  avgPrice - average restuarant price
-  yzi - yelp, zillow, IRS

Note: This code is requrires the preprocessed data files, alongside the geoJSON
file in the same directory in order to compile.
"""

import preProcessZillow as ppz
import preProcessIRS as ppi
import preProcessYelp as ppy
import pandas as pd

# preProcess zillow - saves a csv of preProcess data to cwd
ppz.zillPreProcess("Zip_Zhvi_Summary_AllHomes.csv", targetCity = "Las Vegas")

# preProcess IRS - saves a csv of preProcess data to cwd
irsDict = ppi.preProcess("16zp29nv.csv", ppz.zipcodeList())
df = ppz.dictToCSVDF(irsDict, cols=('postalCode', 'income'))
df.to_csv('vegasIRS.csv')

# preProcess yelp - saves a csv of preProcess data to cwd
ppy.preProcess()
