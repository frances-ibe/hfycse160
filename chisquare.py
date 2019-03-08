# Nathaniel Linden
# Parker Grosjean
# Frances Ingram-Bate
import preProcessIRS as ppi
import preProcessZillow as ppz
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

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
yzi = pd.merge(irsData, zillowData[['postalCode', 'zhvi']], on='postalCode')
yzi = pd.merge(yzi, yelpAvg[['postalCode', 'avgPrice']], on='postalCode')
yziFilt = yzi[["income", "zhvi", "avgPrice"]]

# # Compute Correlation Statistics Between household income and median home value
# # Will utilze the IRS dataset
corrDF = yziFilt.corr(method='pearson')
# print(corrDF)

# # ## Research Question 3
# # """ Does restaurant star rating across price point level vary for different zip code areas?
# # What are trends in such variance across zip code areas and how does it relate to
# # socioeconomic factors such as median house value and average household income? """
#
avgRatingByZip = []  # empty list to hold dictionaries of avg rating per price pnt for each zip code
numRestByZip = []  # empty list to hold dictionaries of num rest per price pnt for each zip code
numStars = [] # empty list to hold dictionaries of num stars per price point for each zip code

for zip in irsData["postalCode"]:  # loop through zip codes
    rests = yelpData[yelpData["postalCode"] == zip]  # get all rows such that the zip code is zip
    # temp dictionaries
    tempDictAvgs = {"postalCode":zip}
    tempDictCnts = {"postalCode":zip}
    tempDictStars = {"postalCode":zip}

    for priceLevel in [1, 2, 3, 4]:  # loop through possible price points
        restsPPnt = rests[rests["price"] == priceLevel]["stars"]  # filter by price level
        tempDictAvgs[priceLevel] = np.mean(np.array(restsPPnt))
        tempDictStars[priceLevel] = np.sum(np.array(restsPPnt))
        tempDictCnts[priceLevel] = len(restsPPnt)

    avgRatingByZip.append(tempDictAvgs)
    numRestByZip.append(tempDictCnts)
    numStars.append(tempDictStars)

avgRatingByZipDF = pd.DataFrame(avgRatingByZip)  # create dataframe
numRestByZipDF = pd.DataFrame(numRestByZip)  # create dataframe
starsZip = pd.DataFrame(numStars)

restRatio = []
for zip in irsData["postalCode"]:
    priceLevel = [1, 2, 3, 4]
    numData = numRestByZipDF[numRestByZipDF["postalCode"]==zip].values.tolist()[0][1:5]
    numRest= sum(numData)
    ratios = [x/numRest for x in numData]
    restRatio.append({"postalCode": zip, 1: ratios[0], 2: ratios[1],
                3: ratios[2], 4: ratios[3]})
restRatio = pd.DataFrame(restRatio)

## Calculate proption of restaurants within each price level for all zip codes

# calculate number restaurants within each price level bin
numRest1 = numRestByZipDF[1].sum()
numRest2 = numRestByZipDF[2].sum()
numRest3 = numRestByZipDF[3].sum()
numRest4 = numRestByZipDF[4].sum()

totalRest = numRest1 + numRest2 + numRest3 + numRest4

# calculate proportions
propRest1 = numRest1 / totalRest
propRest2 = numRest2 / totalRest
propRest3 = numRest3 / totalRest
propRest4 = numRest4 / totalRest
propRest = [propRest1, propRest2, propRest3, propRest4]

assert(propRest1 + propRest2 + propRest3 + propRest4 == 1)

### Chi-square test of independence ###

## Proportions of all restaurants per price level

# Number of restaurants
chiAvgRest = []
for zip in irsData["postalCode"]:
    obs = numRestByZipDF[numRestByZipDF["postalCode"]==zip].values.tolist()[0][1:5]
    numRest = sum(obs)
    exp = [numRest*propRest[x] for x in range(4)]
    result = stats.chisquare(obs, exp)
    chiAvgRest.append({"postalCode": zip, "chiSquared": result[0], "p-value": result[1], "number restaurants": numRest})
chiAvgRest = pd.DataFrame(chiAvgRest)
# print(chiAvgRest)

# Percentage
chiAvg100Rest = []
for zip in irsData["postalCode"]:
    obs = restRatio[restRatio["postalCode"]==zip].values.tolist()[0][1:5]
    obs = [x*100 for x in obs]
    numRest = sum(numRestByZipDF[numRestByZipDF["postalCode"]==zip].values.tolist()[0][1:5])
    exp = [x*100 for x in propRest]
    result = stats.chisquare(obs, exp)
    chiAvg100Rest.append({"postalCode": zip, "chiSquared": result[0], "p-value": result[1], "number restaurants": numRest})
chiAvg100Rest = pd.DataFrame(chiAvg100Rest)
# print(chiAvg100Rest)

## Proportion per zip code (assume equal distribution for each bin)

# Number of restaurants
chiZipRest = []
for zip in irsData["postalCode"]:
    obs = numRestByZipDF[numRestByZipDF["postalCode"]==zip].values.tolist()[0][1:5]
    numRest = sum(obs)
    exp = [np.mean(obs)] * 4
    result = stats.chisquare(obs, exp)
    chiZipRest.append({"postalCode": zip, "chiSquared": result[0], "p-value": result[1], "number restaurants": numRest})
chiZipRest = pd.DataFrame(chiZipRest)
# print(chiZipRest)

# Percentage
chiZip100Rest = []
for zip in irsData["postalCode"]:
    obs = restRatio[restRatio["postalCode"]==zip].values.tolist()[0][1:5]
    obs = [x*100 for x in obs]
    numRest = sum(numRestByZipDF[numRestByZipDF["postalCode"]==zip].values.tolist()[0][1:5])
    exp = [25] * 4
    result = stats.chisquare(obs, exp)
    chiZip100Rest.append({"postalCode": zip, "chiSquared": result[0], "p-value": result[1], "number restaurants": numRest})
chiZip100Rest = pd.DataFrame(chiZip100Rest)
# print(chiZip100Rest)

## Proportion of all stars per price level

# calculate number stars within each price level bin
numStar1 = starsZip[1].sum()
numStar2 = starsZip[2].sum()
numStar3 = starsZip[3].sum()
numStar4 = starsZip[4].sum()

totalStar = numStar1 + numStar2 + numStar3 + numStar4

# calculate proportions
propStar1 = numStar1 / totalStar
propStar2 = numStar2 / totalStar
propStar3 = numStar3 / totalStar
propStar4 = numStar4 / totalStar
propStar = [propStar1, propStar2, propStar3, propStar4]

assert(propStar1 + propStar2 + propStar3 + propStar4 == 1)

# Number of stars
chiAvgStars = []
for zip in irsData["postalCode"]:
    obs = starsZip[starsZip["postalCode"]==zip].values.tolist()[0][1:5]
    numStars = sum(obs)
    numRest = sum(numRestByZipDF[numRestByZipDF["postalCode"]==zip].values.tolist()[0][1:5])
    exp = [numStars*propStar[x] for x in range(4)]
    result = stats.chisquare(obs, exp)
    chiAvgStars.append({"postalCode": zip, "chiSquared": result[0], "p-value": result[1], "number of stars": numStars, "number restaurants": numRest})
chiAvgStars = pd.DataFrame(chiAvgStars)
# print(chiAvgStars)

# Percentage
chiAvg100Stars = []
for zip in irsData["postalCode"]:
    obs = starsZip[starsZip["postalCode"]==zip].values.tolist()[0][1:5]
    numStars = sum(obs)
    obs = [x/numStars for x in obs]
    obs = [x*100 for x in obs]
    numRest = sum(numRestByZipDF[numRestByZipDF["postalCode"]==zip].values.tolist()[0][1:5])
    exp = [x*100 for x in propStar]
    result = stats.chisquare(obs, exp)
    chiAvg100Stars.append({"postalCode": zip, "chiSquared": result[0], "p-value": result[1], "number of stars": numStars, "number restaurants": numRest})
chiAvg100Stars = pd.DataFrame(chiAvg100Stars)
# print(chiAvg100Stars)

## Proportion of stars per zip code (assume equal distribution for each bin)

# Number of stars
chiZipStars = []
for zip in irsData["postalCode"]:
    obs = starsZip[starsZip["postalCode"]==zip].values.tolist()[0][1:5]
    numStars = sum(obs)
    numRest = sum(numRestByZipDF[numRestByZipDF["postalCode"]==zip].values.tolist()[0][1:5])
    exp = [np.mean(obs)] * 4
    result = stats.chisquare(obs, exp)
    chiZipStars.append({"postalCode": zip, "chiSquared": result[0], "p-value": result[1], "number of stars": numStars, "number restaurants": numRest})
chiZipStars = pd.DataFrame(chiZipStars)
# print(chiZipStars)

# Percentage
chiZip100Stars = []
for zip in irsData["postalCode"]:
    obs = starsZip[starsZip["postalCode"]==zip].values.tolist()[0][1:5]
    numStars = sum(obs)
    obs = [x/numStars for x in obs]
    obs = [x*100 for x in obs]
    numRest = sum(numRestByZipDF[numRestByZipDF["postalCode"]==zip].values.tolist()[0][1:5])
    exp = [25] * 4
    result = stats.chisquare(obs, exp)
    chiZip100Stars.append({"postalCode": zip, "chiSquared": result[0], "p-value": result[1], "number of stars": numStars, "number restaurants": numRest})
chiZip100Stars = pd.DataFrame(chiZip100Stars)
# print(chiZip100Stars)

## Number of stars, expected based off rest dist per zip
chiZipStarRest = []
for zip in irsData["postalCode"]:
    obs = starsZip[starsZip["postalCode"]==zip].values.tolist()[0][1:5]
    numStars = sum(obs)
    restProp = restRatio[restRatio["postalCode"]==zip].values.tolist()[0][1:5]
    exp = [numStars*restProp[x] for x in range(4)]
    result = stats.chisquare(obs, exp)
    chiZipStarRest.append({"postalCode": zip, "chiSquared": result[0], "p-value": result[1]})
chiZipStarRest = pd.DataFrame(chiZipStarRest)
# print(chiZipStarRest)

## Number of stars, expected based off total rest dist
chiAvgStarRest = []
for zip in irsData["postalCode"]:
    obs = starsZip[starsZip["postalCode"]==zip].values.tolist()[0][1:5]
    numStars = sum(obs)
    exp = [numStars*propStar[x] for x in range(4)]
    result = stats.chisquare(obs, exp)
    chiAvgStarRest.append({"postalCode": zip, "chiSquared": result[0], "p-value": result[1]})
chiAvgStarRest = pd.DataFrame(chiAvgStarRest)
print(chiAvgStarRest)
