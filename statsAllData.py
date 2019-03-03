# Nathaniel Linden
# Parker Grosjean
# Frances Ingram-Bate
import preProcessIRS as ppi
import preProcessZillow as ppz
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load Data
zillowData = pd.read_csv("vegasHousing.csv")
zillowData.sort_values(by=["postalCode"])

irsData = pd.read_csv("vegasIRS.csv")
irsData.sort_values(by=["postalCode"])

yelpData = pd.read_csv("vegasRest.csv")
yelpData.sort_values(by=["postalCode"])
### Note: the yelp data with city="Las Vegas" appears to have some mislabeled
# data, some of the zip codes are in other cities such as 85705 in Tucson

# average yelp rating
d = []
for zip in irsData["postalCode"]:
    zipPrice = yelpData[yelpData["postalCode"] == zip]["price"]
    zipPrice.astype(int)
    d.append({"postalCode": zip, "avgPrice": np.mean(zipPrice)})
yelpAvg = pd.DataFrame(d)

#merge yelp and zillow data
# yzi = zillowData.copy()
yzi = pd.merge(irsData, zillowData[['postalCode', 'zhvi']], on='postalCode')
yzi = pd.merge(yzi, yelpAvg[['postalCode', 'avgPrice']], on='postalCode')
yziFilt = yzi[["income", "zhvi", "avgPrice"]]

# # Compute Correlation Statistics Between household income and median home value
# # Will utilze the IRS dataset
corrDF = yziFilt.corr(method='pearson')
print(corrDF)

# # Plot Grid of Scatter Plots
# fig1 = plt.figure()
# # WE NEED TO CHANGE THE NAMES HERE
# plt.plot(yzi["zhvi"], yzi["avgPrice"],'.')
# plt.plot(yzi["HOUSEING"], yzi["INCOME"],'.')
# plt.plot(yzi["income"], yzi["RESTPRICE"],'.')



#
# # ## Research Question 3
# # """ Does restaurant star rating across price point level vary for different zip code areas?
# # What are trends in such variance across zip code areas and how does it relate to
# # socioeconomic factors such as median house value and average household income? """
#
# avgRatingByZip = []  # empty list to hold dictionaries of avg rating per price pnt for each zip code
# numRestByZip = []  # empty list to hold dictionaries of num rest per price pnt for each zip code
#
# for zip in irsData["postalCode"]:  # loop through zip codes
#     rests = yelpData[yelpData["postalCode"] == zip]  # get all rows such that the zip code is zip
#     # temp dictionaries
#     tempDictAvgs = {"postalCode":zip}
#     tempDictCnts = {"postalCode":zip}
#
#     for priceLevel in [1, 2, 3, 4]:  # loop through possible price points
#         restsPPnt = rests[rests["price"] == priceLevel]["stars"]  # filter by price level
#         tempDictAvgs[priceLevel] = np.mean(np.array(restsPPnt))
#         tempDictCnts[priceLevel] = len(restsPPnt)
#
#     avgRatingByZip.append(tempDictAvgs)
#     numRestByZip.append(tempDictCnts)
#
# avgRatingByZipDF = pd.DataFrame(avgRatingByZip)  # create dataframes
# numRestByZipDF = pd.DataFrame(numRestByZip)  # create dataframes
#
# print(avgRatingByZipDF)
# print(numRestByZipDF)
