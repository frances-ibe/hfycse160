# Testing ZillowPreProcess

import preProcessZillow as ppz

ppz.zillPreProcess("Zip_Zhvi_Summary_AllHomes.csv", targetCity = "Las Vegas")
zcList = ppz.zipcodeList()
print(zcList)
