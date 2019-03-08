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

        ############ Produces a run-time error ###############
        tempDictAvgs[priceLevel] = np.mean(np.array(restsPPnt))
        #######################################################

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

def chiDict(zip, obs, exp,  alpha=0.01):
    """Create dictionary containing zip code, number of stars per zip code,
    number of restaurants per zip code, chi-squared value and p-value result
    of chi-square test, as well as whether or not the p-value is less than alpha.
    Calculates chi-square value from observed and expected lists"""
    result = stats.chisquare(obs, exp)
    return {"postalCode":zip, "chi-squared":result[0], "p-value":result[1],
    "less than alpha":(result[1] < alpha)}


zipList = irsData["postalCode"].tolist()

### Chi Square Tests ###

# Restaurant Number and Price Level
chiTotRest = [] #obs: rest per price level, exp: total rest prop
chiZipRest = [] #obs: rest per price level, exp: mean number for zip

# Number of Stars and Price Level
chiTotStars = [] #obs: stars per price level, exp: total star prop
chiZipStars = [] #obs: stars per price level, exp: mean number for zip

# Restaurant Number and Number of Stars
chiTotStarRest = [] #obs: stars per price level, exp: total rest prop

for zip in zipList:

    # Observed Values
    restLevel = numRestByZipDF[numRestByZipDF["postalCode"]==zip].values.tolist()[0][1:5]
    numRest = sum(restLevel)
    restPropLevel = [x/numRest for x in restLevel]

    starLevel = starsZip[starsZip["postalCode"]==zip].values.tolist()[0][1:5]
    numStars = sum(starLevel)

    # Expected Values
    restTot = [numRest*x for x in propRest]
    restZip = [np.mean(restLevel)] * 4

    starTot = [numStars*x for x in propStar]
    starZipNum = [np.mean(starLevel)] * 4
    starAvgRest = [numStars*x for x in propRest]

    # Compute Chi-Square Test and Append Results to List
    chiTotRest.append(chiDict(zip,restLevel, restTot))
    chiZipRest.append(chiDict(zip,restLevel, restZip))

    chiTotStars.append(chiDict(zip,starLevel, starTot))
    chiZipStars.append(chiDict(zip,starLevel, starZipNum))
    chiTotStarRest.append(chiDict(zip,starLevel, starAvgRest))

# Convert List of Dictionaries to DataFrame
chiTotRest = pd.DataFrame(chiTotRest)
chiZipRest = pd.DataFrame(chiZipRest)

chiTotStars = pd.DataFrame(chiTotStars)
chiZipStars = pd.DataFrame(chiZipStars)
chiTotStarRest = pd.DataFrame(chiTotStarRest)

# Print Data Frames
# print(chiTotRest)
# print(chiZipRest)

# print(chiTotStars)
# print(chiZipStars)
# print(chiTotStarRest)

### Filter Data for Zips for which
# (1) number of restaurants per price level is independent of price level
# (2) number of stars per price level is independent of price level
# (3) number of stars per price level is independent of number of restaurants per price level

zipTest = []
for zip in zipList:
    zipRest = chiZipRest[chiZipRest["postalCode"]==zip].iloc[0]["less than alpha"]
    zipStars = chiZipStars[chiZipStars["postalCode"]==zip].iloc[0]["less than alpha"]
    starRest = chiTotStarRest[chiTotStarRest["postalCode"]==zip].iloc[0]["less than alpha"]
    zipTest.append({"postalCode": zip, "independent": (zipRest & zipStars & starRest)})
zipTest = pd.DataFrame(zipTest)
# print(zipTest)

zipPassTests = zipTest[zipTest["independent"]].drop(columns=["independent"])
