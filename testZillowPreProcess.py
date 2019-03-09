# Testing ZillowPreProcess

import preProcessZillow as ppz
import preProcessIRS as ppi
import preProcess as ppy
import pandas as pd


ppz.zillPreProcess("Zip_Zhvi_Summary_AllHomes.csv", targetCity = "Las Vegas")
irsDict = ppi.preProcess("16zp29nv.csv", ppz.zipcodeList())
df = ppz.dictToCSVDF(irsDict, cols=('postalCode', 'income'))
df.to_csv('vegasIRS.csv')
ppy.preProcess()
