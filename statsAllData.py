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




restByZip = dict.fromkeys(irsData["postalCode"], 0)
for rest in list(yelpData.itertuples(index=False, name=None)):
    if rest[2] in list(restByZip.keys()):
        if rest[4] in ['1','2','3','4']:
            restByZip[rest[2]][rest[4]] = restByZip[rest[2]][rest[4]].append(rest[3])

print(len(restByZip[89156]['3']) == len(restByZip[89109]['3']))

# output = {}
# for zip in

# avg = dict.fromkeys(list(restByZip.keys()), [[],[],[],[]])
# print(avg)
#
#
# moo = list(avg.keys())
# print(moo)
# for item in avg[moo[0]]:
# avg[moo[0]][0] = sum(restByZip[moo[0]]['1'])
# avg[moo[0]][1] = sum(restByZip[moo[0]]['2'])
# avg[moo[0]][2] = sum(restByZip[moo[0]]['3'])
# print(avg)
# for zip in list(avg.keys()):
#     for price in list(avg[zip].keys()):
#         avg[zip][price] = sum(restByZip[zip][price])
#         #print(restByZip[zip][price])
