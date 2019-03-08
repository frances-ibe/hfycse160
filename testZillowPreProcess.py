# Testing ZillowPreProcess

import preProcessZillow as ppz
import preProcessIRS as ppi
import preProcess as ppy


ppz.zillPreProcess("Zip_Zhvi_Summary_AllHomes.csv", targetCity = "Las Vegas")
print(ppz.zipcodeList())
ppi.preProcess("16zp29nv.csv", ppz.zipcodeList())
ppy.preProcess()
