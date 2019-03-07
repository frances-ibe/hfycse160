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
# # plt.subplot(3,1,1)
# plt.plot(yzi["zhvi"], yzi["avgPrice"],'.')
# # plt.subplot(3,1,2)
# fig2 = plt.figure()
# plt.plot(yzi["zhvi"], yzi["income"],'.')
# # plt.subplot(3,1,3)
# fig3 = plt.figure()
# plt.plot(yzi["income"], yzi["avgPrice"],'.')
# plt.show()

#
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

restRatio = []
wRating = []
for zip in irsData["postalCode"]:
    priceLevel = [1, 2, 3, 4]
    numData = numRestByZipDF[numRestByZipDF["postalCode"]==zip].values.tolist()[0][1:5]
    ratingData = avgRatingByZipDF[avgRatingByZipDF["postalCode"]==zip].values.tolist()[0][1:5]
    numRest = sum(numData)
    ratios = [x/numRest for x in numData]
    restRatio.append({"postalCode": zip, 1: ratios[0], 2: ratios[1],
                3: ratios[2], 4: ratios[3]})
    wRating.append({"postalCode": zip, 1: ratingData[0]*ratios[0],
                2: ratingData[1]*ratios[1], 3: ratingData[2]*ratios[2],
                4: ratingData[3]*ratios[3]})
restRatio = pd.DataFrame(restRatio)
wRating = pd.DataFrame(wRating)
wRating.fillna(0)


# Plotting avg rating yelp at different price points
# vs Median household income
AvgVsZhvi = plt.figure()
plt.subplot(4,1,1)
plt.scatter(yzi["zhvi"], avgRatingByZipDF[1])
plt.title('Price Point 1', fontname="Arial", fontsize=12)
plt.ylabel('Average Rating', fontname="Arial", fontsize=12)
plt.xlabel('Median Estimated Home Value (zhvi)', fontname="Arial", fontsize=12)
plt.ylim((0,6))
plt.subplot(4,1,2)
plt.scatter(yzi["zhvi"], avgRatingByZipDF[2])
plt.title('Price Point 2', fontname="Arial", fontsize=12)
plt.ylabel('Average Rating', fontname="Arial", fontsize=12)
plt.xlabel('Median Estimated Home Value (zhvi)', fontname="Arial", fontsize=12)
plt.ylim((0,6))
plt.subplot(4,1,3)
plt.scatter(yzi["zhvi"], avgRatingByZipDF[3])
plt.title('Price Point 3', fontname="Arial", fontsize=12)
plt.ylabel('Average Rating', fontname="Arial", fontsize=12)
plt.xlabel('Median Estimated Home Value (zhvi)', fontname="Arial", fontsize=12)
plt.ylim((0,6))
plt.subplot(4,1,4)
plt.scatter(yzi["zhvi"], avgRatingByZipDF[4])
plt.title('Price Point 4', fontname="Arial", fontsize=12)
plt.ylabel('Average Rating', fontname="Arial", fontsize=12)
plt.xlabel('Median Estimated Home Value (zhvi)', fontname="Arial", fontsize=12)
plt.ylim((0,6))
plt.show()

avgRatingZhviDF = pd.merge(avgRatingByZipDF, yzi[["postalCode","zhvi"]], on="postalCode") # generating correlation matrix
corrRatingZhviDF = avgRatingZhviDF.corr(method='pearson')
print(corrRatingZhviDF) # printing correlation matrix

# Plotting avg weighted rating yelp at different price points
#vs Median household income
# The weight is the ratio of the number of restaurants per
#pricepoint per zipcode to the total number of resteraunts
#per zipcodeList
weightedAvgVsZhvi = plt.figure()
plt.subplot(4,1,1)
plt.scatter(yzi["zhvi"], wRating[1])
plt.title('Price Point 1', fontname="Arial", fontsize=12)
plt.ylabel('Weighted Average Rating', fontname="Arial", fontsize=12)
plt.xlabel('Median Estimated Home Value (zhvi)', fontname="Arial", fontsize=12)
plt.ylim((0,3))
plt.subplot(4,1,2)
plt.scatter(yzi["zhvi"], wRating[2])
plt.title('Price Point 1', fontname="Arial", fontsize=12)
plt.ylabel('Weighted Average Rating', fontname="Arial", fontsize=12)
plt.xlabel('Median Estimated Home Value (zhvi)', fontname="Arial", fontsize=12)
plt.ylim((0,3))
plt.subplot(4,1,3)
plt.scatter(yzi["zhvi"], wRating[3])
plt.title('Price Point 3', fontname="Arial", fontsize=12)
plt.ylabel('Weighted Average Rating', fontname="Arial", fontsize=12)
plt.xlabel('Median Estimated Home Value (zhvi)', fontname="Arial", fontsize=12)
plt.ylim((0,3))
plt.subplot(4,1,4)
plt.scatter(yzi["zhvi"], wRating[4])
plt.title('Price Point 4', fontname="Arial", fontsize=12)
plt.ylabel('Weighted Average Rating', fontname="Arial", fontsize=12)
plt.xlabel('Median Estimated Home Value (zhvi)', fontname="Arial", fontsize=12)
plt.ylim((0,3))
plt.show()

weightAvgZhvi = pd.merge(wRating, yzi[["postalCode","zhvi"]], on="postalCode") # generating correlation matrix
corrWeightAvgZhvi = weightAvgZhvi.corr(method='pearson')
print(corrWeightAvgZhvi) # printing correlation matrix
