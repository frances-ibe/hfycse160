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
# print(corrDF)

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
print(yziFiltNoOutlier)


## Research Question 2
""" Can we predict average resurante pricing?"""
## USE INCOME AS PREDICTOR  ##

# Select Training and Testing Data
# randomly select 4 indices for testing

np.random.seed(235)  # set numpy random number generator seed
# get four random idices
testIndices = np.random.randint(0, high=yziFiltNoOutlier["income"].count(), size=4)
trainIndices = set(np.arange(1,yziFiltNoOutlier["income"].count())+1) - set(testIndices)

# Select train and testing data
testIncome = np.array([[val] for val in yziFiltNoOutlier["income"][testIndices].dropna()])
testAvgPrice = np.array([[val] for val in yziFiltNoOutlier["avgPrice"][testIndices].dropna()])

print(testIncome)
print(testAvgPrice)
trainIncome = np.array([[val] for val in yziFiltNoOutlier["income"][trainIndices].dropna()])
trainAvgPrice = np.array([[val] for val in yziFiltNoOutlier["avgPrice"][trainIndices].dropna()])

print(trainAvgPrice)
print(trainIncome)
# create a linear regression object
regr = linear_model.LinearRegression()

# fit the model to the training data
regr.fit(trainIncome, trainAvgPrice)

# make predictions
predictedAvgPrice = regr.predict(testIncome)

# print the coeffs
print("Coefficients: ", regr.coef_)

print("score: ", regr.score(testIncome, testAvgPrice))


# calculate R-squared
print("R^2: ", pearsonr(testIncome, testAvgPrice)[0]**2)



# plot outputs
nl2 = plt.figure()
plt.scatter(testIncome, testAvgPrice, color="black")
plt.plot(testIncome, predictedAvgPrice, '.',color="blue")
plt.show()

# plot best fit line
nl3 = plt.figure()
plt.scatter(trainIncome, trainAvgPrice, color="black")
plt.plot(trainIncome, regr.predict(trainIncome), color="blue")
plt.show()




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
        tempDictAvgs[priceLevel] = np.mean(np.array(restsPPnt))
        tempDictCnts[priceLevel] = len(restsPPnt)

    avgRatingByZip.append(tempDictAvgs)
    numRestByZip.append(tempDictCnts)

avgRatingByZipDF = pd.DataFrame(avgRatingByZip)  # create dataframe
numRestByZipDF = pd.DataFrame(numRestByZip)  # create dataframe
