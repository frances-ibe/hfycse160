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
# print(yelpData)
# yelpData = yelpData[yelpData.price.notnull()]
# print(yelpData)
for zip in irsData["postalCode"]:
    zipPrice = yelpData[yelpData["postalCode"] == zip]["price"]
    print(zipPrice)
    zipPrice.astype(int)
    d.append({"postalCode": zip, "averagePrice": np.mean(zipPrice)})
yelpAvg = pd.DataFrame(d)
# print(yelpAvg)

#merge yelp and zillow data
# yzi = zillowData.copy()
yzi = pd.merge(irsData, zillowData[['postalCode', 'zhvi']], on='postalCode')

# # Compute Correlation Statistics Between household income and median home value
# # Will utilze the IRS dataset
# corrDF = yzi.corr(method='pearson')
#
# print(corrDF)
#
# # Plot Grid of Scatter Plots
# fig1 = plt.figure()
# # WE NEED TO CHANGE THE NAMES HERE
# plt.plot(yzi["HOUSEING"], yzi["RESTPRICE"],'.')
# plt.plot(yzi["HOUSEING"], yzi["INCOME"],'.')
# plt.plot(yzi["income"], yzi["RESTPRICE"],'.')




# ## Research Question 3
# """ Does restaurant star rating across price point level vary for different zip code areas?
# What are trends in such variance across zip code areas and how does it relate to
# socioeconomic factors such as median house value and average household income? """
# for zip in irsData['postalCode']
