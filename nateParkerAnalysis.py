# Nathaniel Linden
# Parker Grosjean
# Frances Ingram-Bate
import preProcessIRS as ppi
import preProcessZillow as ppz
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score, mean_squared_error, explained_variance_score
from scipy.stats import pearsonr
from spatialMapping import plot_spatialdata

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
#
# # # Compute Correlation Statistics Between household income and median home value
# # # Will utilze the IRS dataset
# corrDF = yziFilt.corr(method='pearson')
# # print(corrDF)

# # Plot Grid of Scatter Plots
# fig1 = plt.figure()
# # plt.subplot(3,1,1)
# plt.plot(yzi["zhvi"], yzi["avgPrice"],'.')
# plt.title('zhvi vs avgPrice')
# # plt.subplot(3,1,2)
# fig2 = plt.figure()
# plt.plot(yzi["zhvi"], yzi["income"],'.')
# plt.title('zhvi vs income')
# # plt.subplot(3,1,3)
# fig3 = plt.figure()
# plt.plot(yzi["income"], yzi["avgPrice"],'.')
# plt.title('income vs avgPrice')
# plt.show()

# There is an outlier in the income vs. price data
# Need to find and remove that outlier from the data
#
yziNoOutlier = yzi[yzi["avgPrice"] != max(yzi["avgPrice"])]
yziNoOutlier.dropna()

#
# njl1 = plt.figure()
# plt.plot(yziNoOutlier["income"], yziNoOutlier["avgPrice"],'.')
# plt.show()
yziFiltNoOutlier = yziNoOutlier[["income", "zhvi", "avgPrice"]]

yziFiltNoOutlier.to_csv('try.csv')



## Research Question 2
""" Can we predict average resurante pricing?"""

trainIncome = np.array([[val] for val in yziFiltNoOutlier["income"].dropna()])
trainAvgPrice = np.array([[val] for val in yziFiltNoOutlier["avgPrice"].dropna()])
trainZHVI = np.array([[val] for val in yziFiltNoOutlier["zhvi"].dropna()])

## USE INCOME AS PREDICTOR  ##
# create a linear regression object
regr1 = linear_model.LinearRegression()
# fit the model to the training data
regr1.fit(trainIncome, trainAvgPrice)
# make predictions
predictedAvgPrice = regr1.predict(trainIncome)
rsquaredMetrics1 = pearsonr(predictedAvgPrice, trainAvgPrice)[0]**2
print(rsquaredMetrics1)

# plot best fit line
nl3 = plt.figure()
plt.scatter(trainIncome, trainAvgPrice, color="xkcd:black")
predictline, = plt.plot(trainIncome, regr1.predict(trainIncome), color="xkcd:aquamarine", linewidth=2)
plt.title('Linear Regression Based Prediciton of Average Restaurant Price by Average Income', \
          fontsize=14, fontname='Arial', fontweight='bold')
plt.xlabel('Income', fontsize=12, fontname='Arial', fontweight='bold')
plt.ylabel('Average Restaurant Price', fontsize=12, fontname='Arial', fontweight='bold')
leg = 'RSquared = ' + str(np.round(rsquaredMetrics1[0], 3))
print(leg)
plt.legend(handles=[predictline], labels=[leg], loc=4)
nl3.set_size_inches(11, 8)
plt.savefig('regr1priceincome.png')

## USE ZHVI AS PREDICTOR  ##
# create a linear regression object
regr2 = linear_model.LinearRegression()
# fit the model to the training data
regr2.fit(trainZHVI, trainAvgPrice)
# make predictions
predictedAvgPrice2 = regr2.predict(trainZHVI)
rsquaredMetrics2 = pearsonr(predictedAvgPrice, trainZHVI)[0]**2
print(rsquaredMetrics2)


# plot best fit line
nl4 = plt.figure()
plt.scatter(trainIncome, trainZHVI, color="xkcd:black")
predictline, = plt.plot(trainZHVI, regr1.predict(trainZHVI), color="xkcd:aquamarine", linewidth=2)
plt.title('Linear Regression Based Prediciton of Average Restaurant Price by Zillow Home Value Index', \
          fontsize=14, fontname='Arial', fontweight='bold')
plt.xlabel('Income', fontsize=12, fontname='Arial', fontweight='bold')
plt.ylabel('Zillow Home Value Index', fontsize=12, fontname='Arial', fontweight='bold')
leg = 'RSquared = ' + str(np.round(rsquaredMetrics1[0], 3))
print(leg)
plt.legend(handles=[predictline], labels=[leg], loc=4)
nl4.set_size_inches(11, 8)
plt.savefig('regr2priceZHVI.png')



## MAKE MAPS ##
# create a dictionary mapping zip codes to the number of restaurants in each zip
# code region
weightedZipsNumRest = {}
weightedZipsIncome = {}
weightedZipsPrice = {}

meanIncome = np.mean(yzi['income'])
for zip in irsData["postalCode"]:
    numRests = len(yelpData[yelpData["postalCode"] == zip]["price"])


    weightedZipsNumRest[str(zip)] = np.log(numRests)
    weightedZipsPrice[str(zip)] = np.max(yzi[yzi['postalCode'] == zip]['avgPrice'])
    weightedZipsIncome[str(zip)] = np.max(yzi[yzi['postalCode'] == zip]['income'])


# use spatialMapping to plot a choropleth map where colors correspond to number
# of restaurant in that zipcode

plot_spatialdata('numRest', weightedZipsNumRest, 'Number of Restaurants per Las Vegas Zip Code')
plot_spatialdata('Price', weightedZipsIncome, 'Mean Household Income per Las Vegas Zip Code')
plot_spatialdata('Income', weightedZipsPrice, 'Mean Restaurant Price per Las Vegas Zip Code')




# # ## Research Question 3
# # """ Does restaurant star rating across price point level vary for different zip code areas?
# # What are trends in such variance across zip code areas and how does it relate to
# # socioeconomic factors such as median house value and average household income? """
#
avgRatingByZip = []  # empty list to hold dictionaries of avg rating per price pnt for each zip code
numRestByZip = []  # empty list to hold dictionaries of num rest per price pnt for each zip code

for zip in irsData["postalCode"]:  # loop through zip codes
    rests = yelpData[yelpData["postalCode"] == zip]  # get all rows such that the zip code is zip
    # temp dictionaries
    tempDictAvgs = {"postalCode":zip}
    tempDictCnts = {"postalCode":zip}

    for priceLevel in [1, 2, 3, 4]:  # loop through possible price points
        restsPPnt = rests[rests["price"] == priceLevel]["stars"]  # filter by price level
        if len(restsPPnt) is not 0:
            tempDictAvgs[priceLevel] = np.mean(np.array(restsPPnt))
        else:
            tempDictAvgs[priceLevel] = 0
        tempDictCnts[priceLevel] = len(restsPPnt)

    avgRatingByZip.append(tempDictAvgs)
    numRestByZip.append(tempDictCnts)

avgRatingByZipDF = pd.DataFrame(avgRatingByZip)  # create dataframe
numRestByZipDF = pd.DataFrame(numRestByZip)  # create dataframe
