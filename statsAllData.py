# Nathaniel Linden
# Parker Grosjean
# Frances Ingram-Bate
import preProcessIRS as ppi
import preProcessZillow as ppz
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Loading Preprocessed Data
# loading zillow data
zillowData = pd.read_csv("vegasHousing.csv")
zillowData.sort_values(by=["postalCode"])

# loading irs data
irsData = pd.read_csv("vegasIRS.csv")
irsData.sort_values(by=["postalCode"])

# loading yelp data
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

# merge yelp and zillow data
yzi = pd.merge(irsData, zillowData[['postalCode', 'zhvi']], on='postalCode')
yzi = pd.merge(yzi, yelpAvg[['postalCode', 'avgPrice']], on='postalCode')
yziFilt = yzi[["income", "zhvi", "avgPrice"]]

# Removing the Vegas Strip as it is an outlier in our data
yziNoOutlier = yzi[yzi["avgPrice"] != max(yzi["avgPrice"])]
yziNoOutlier.dropna()


#
# # ## Research Question 1
# # Does restaurant star rating across price point level vary for
# # different zip code  areas? What are trends in such variance across
# # zip code areas and how does it relate to socioeconomic factors
# # such as median house value and average household income?
#


## Compute Correlation Statistics Between household income and median home value
# no outlier removed
corrDF = yziFilt.corr(method='pearson')
# print(corrDF)


## Compute Correlation Statistics Between household income and median home value
# no outlier removed
corrDF2 = yziNoOutlier.corr(method='pearson')
# print(corrDF2)


## Plotting Grid of Scatter Plots for RQ1
figRQ1, axRq1 = plt.subplots(2, 3)
figRQ1.set_size_inches(12, 5)
plt.subplots_adjust(hspace=0.5, wspace=0.5)
axRq1[0,0].scatter(yzi["zhvi"], yzi["avgPrice"], s=10)
axRq1[0,2].scatter(yzi["zhvi"], yzi["income"], s=10)
axRq1[0,1].scatter(yzi["income"], yzi["avgPrice"], s=10)
axRq1[0,0].set_ylabel("Average \n Price Point", fontname="Arial", fontsize=12, fontweight='bold')
axRq1[0,0].set_xlabel("zhvi", fontname="Arial", fontsize=12, fontweight='bold')
axRq1[0,2].set_ylabel("Average Income", fontname="Arial", fontsize=12, fontweight='bold')
axRq1[0,2].set_xlabel("zhvi", fontname="Arial", fontsize=12, fontweight='bold')
axRq1[0,1].set_ylabel("Average \n Price Point", fontname="Arial", fontsize=12, fontweight='bold')
axRq1[0,1].set_xlabel("Average Income", fontname="Arial", fontsize=12, fontweight='bold')
axRq1[0,0].set_ylim((0,4))
axRq1[0,0].set_xlim(((150000,500000)))
axRq1[0,2].set_ylim((25000,225000))
axRq1[0,2].set_xlim(((150000,500000)))
axRq1[0,1].set_ylim((0,4))
axRq1[0,1].set_xlim(((25000,225000)))
axRq1[0,0].set_title('No Outlier Removed', fontname="Arial", fontsize=12, fontweight='bold')
axRq1[0,1].set_title('No Outlier Removed', fontname="Arial", fontsize=12, fontweight='bold')
axRq1[0,2].set_title('No Outlier Removed', fontname="Arial", fontsize=12, fontweight='bold')
axRq1[1,0].scatter(yziNoOutlier["zhvi"], yziNoOutlier["avgPrice"], s=10)
axRq1[1,2].scatter(yziNoOutlier["zhvi"], yziNoOutlier["income"], s=10)
axRq1[1,1].scatter(yziNoOutlier["income"], yziNoOutlier["avgPrice"], s=10)
axRq1[1,0].set_ylabel("Average \n Price Point", fontname="Arial", fontsize=12, fontweight='bold')
axRq1[1,0].set_xlabel("zhvi", fontname="Arial", fontsize=12, fontweight='bold')
axRq1[1,2].set_ylabel("Average Income", fontname="Arial", fontsize=12, fontweight='bold')
axRq1[1,2].set_xlabel("zhvi", fontname="Arial", fontsize=12, fontweight='bold')
axRq1[1,1].set_ylabel("Average \n Price Point", fontname="Arial", fontsize=12, fontweight='bold')
axRq1[1,1].set_xlabel("Average Income", fontname="Arial", fontsize=12, fontweight='bold')
axRq1[1,0].set_ylim((0,4))
axRq1[1,0].set_xlim(((150000,500000)))
axRq1[1,2].set_ylim((25000,225000))
axRq1[1,2].set_xlim(((150000,500000)))
axRq1[1,1].set_ylim((0,4))
axRq1[1,1].set_xlim(((25000,225000)))
axRq1[1,0].set_title('Outlier Removed', fontname="Arial", fontsize=12, fontweight='bold')
axRq1[1,1].set_title('Outlier Removed', fontname="Arial", fontsize=12, fontweight='bold')
axRq1[1,2].set_title('Outlier Removed', fontname="Arial", fontsize=12, fontweight='bold')
# plt.savefig('RQ1_scatters.png')

#
# # ## Research Question 3
# # """ Does restaurant star rating across price point level vary for different zip code areas?
# # What are trends in such variance across zip code areas and how does it relate to
# # socioeconomic factors such as median house value and average household income? """
#

## Data preprocessing for RQ 3 analysis
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
for zip in irsData["postalCode"]:
    priceLevel = [1, 2, 3, 4]
    numData = numRestByZipDF[numRestByZipDF["postalCode"]==zip].values.tolist()[0][1:5]
    numRest = sum(numData)
    ratios = [x/numRest for x in numData]
    restRatio.append({"postalCode": zip, 1: ratios[0], 2: ratios[1],
                3: ratios[2], 4: ratios[3]})
restRatio = pd.DataFrame(restRatio)


## Calculating Correlation for avg rating yelp at different price points
# vs average income and for restaurant proportion at different price points
# vs average income
aRIncome = pd.merge(irsData, avgRatingByZipDF, on='postalCode')
rRIncome = pd.merge(irsData, restRatio, on='postalCode')
aRICorr = aRIncome[[1, 2, 3, 4, "income"]].corr(method='pearson')
# print(aRICorr)
rRICorr = rRIncome[[1, 2, 3, 4, "income"]].corr(method='pearson')
# print(rRICorr)


## Plotting avg rating yelp at different price points
# vs average income
figAvgI, axAvgI = plt.subplots(2, 2, sharex='col', sharey='row')
figAvgI.set_size_inches(8, 5)
plt.subplots_adjust(hspace=0.2, wspace=0.2)
axAvgI[0, 0].scatter(aRIncome["income"], aRIncome[1], s=10)
axAvgI[0, 1].scatter(aRIncome["income"], aRIncome[2], s=10)
axAvgI[1, 0].scatter(aRIncome["income"], aRIncome[3], s=10)
axAvgI[1, 1].scatter(aRIncome["income"], aRIncome[4], s=10)
axAvgI[0,0].set_ylim((0,5))
axAvgI[1,0].set_ylim((0,5))
axAvgI[0,1].set_ylim((0,5))
axAvgI[1,1].set_ylim((0,5))
axAvgI[0,0].set_xlim((25000,225000))
axAvgI[0,1].set_xlim((25000,225000))
axAvgI[1,0].set_xlim((25000,225000))
axAvgI[1,1].set_xlim((25000,225000))
axAvgI[0,0].set_title('Price Point 1', fontname="Arial", fontsize=12, fontweight='bold')
axAvgI[0,1].set_title('Price Point 2', fontname="Arial", fontsize=12, fontweight='bold')
axAvgI[1,0].set_title('Price Point 3', fontname="Arial", fontsize=12, fontweight='bold')
axAvgI[1,1].set_title('Price Point 4', fontname="Arial", fontsize=12, fontweight='bold')
axAvgI[0,0].set_ylabel('Average Rating', fontname="Arial", fontsize=12, fontweight='bold')
axAvgI[1,0].set_xlabel('Mean Income', fontname="Arial", fontsize=12, fontweight='bold')
axAvgI[1,0].set_ylabel('Average Rating', fontname="Arial", fontsize=12, fontweight='bold')
axAvgI[1,1].set_xlabel('Mean Income', fontname="Arial", fontsize=12, fontweight='bold')
# plt.savefig('scatter_income_avgrating_by_ppoint.png')


# Plotting restaurant proportion at different price points
# vs average income
figRestI, axRestI = plt.subplots(2, 2, sharex='col', sharey='row')
figRestI.set_size_inches(8, 5)
plt.subplots_adjust(hspace=0.2, wspace=0.2)
axRestI[0, 0].scatter(rRIncome["income"], rRIncome[1], s=10)
axRestI[0, 1].scatter(rRIncome["income"], rRIncome[2], s=10)
axRestI[1, 0].scatter(rRIncome["income"], rRIncome[3], s=10)
axRestI[1, 1].scatter(rRIncome["income"], rRIncome[4], s=10)
axRestI[0,0].set_ylim((0,0.8))
axRestI[0,1].set_ylim((0,0.8))
axRestI[1,0].set_ylim((0,0.8))
axRestI[1,1].set_ylim((0,0.8))
axRestI[0,0].set_xlim((25000,225000))
axRestI[0,1].set_xlim((25000,225000))
axRestI[1,0].set_xlim((25000,225000))
axRestI[1,1].set_xlim((25000,225000))
axRestI[0,0].set_title('Price Point 1', fontname="Arial", fontsize=12, fontweight='bold')
axRestI[0,1].set_title('Price Point 2', fontname="Arial", fontsize=12, fontweight='bold')
axRestI[1,0].set_title('Price Point 3', fontname="Arial", fontsize=12, fontweight='bold')
axRestI[1,1].set_title('Price Point 4', fontname="Arial", fontsize=12, fontweight='bold')
axRestI[0,0].set_ylabel('Restaurant Proportion', fontname="Arial", fontsize=12, fontweight='bold')
axRestI[1,0].set_xlabel('Mean Income', fontname="Arial", fontsize=12, fontweight='bold')
axRestI[1,0].set_ylabel('Restaurant Proportion', fontname="Arial", fontsize=12, fontweight='bold')
axRestI[1,1].set_xlabel('Mean Income', fontname="Arial", fontsize=12, fontweight='bold')
# plt.savefig('scatter_income_proprest_by_ppoint.png')


# Calculating Correlation
aRZil = pd.merge(zillowData, avgRatingByZipDF, on='postalCode')
rRZil = pd.merge(zillowData, restRatio, on='postalCode')
aRZCorr = aRZil[[1, 2, 3, 4, "zhvi"]].corr(method='pearson')
# print(aRZCorr)
rRZCorr = rRZil[[1, 2, 3, 4, "zhvi"]].corr(method='pearson')
# print(rRZCorr)


# Plotting avg rating yelp at different price points
# vs Median household income
figAvgZ, axAvgZ = plt.subplots(2,2, sharex='col', sharey='row')
figAvgZ.set_size_inches(8, 5)
plt.subplots_adjust(hspace=0.2, wspace=0.2)
axAvgZ[0, 0].scatter(aRZil["zhvi"], aRZil[1], s=10)
axAvgZ[0, 1].scatter(aRZil["zhvi"], aRZil[2], s=10)
axAvgZ[1, 0].scatter(aRZil["zhvi"], aRZil[3], s=10)
axAvgZ[1, 1].scatter(aRZil["zhvi"], aRZil[4], s=10)
axAvgZ[0,0].set_ylim((0,5))
axAvgZ[1,0].set_ylim((0,5))
axAvgZ[0,1].set_ylim((0,5))
axAvgZ[1,1].set_ylim((0,5))
axAvgZ[0,0].set_xlim((150000,500000))
axAvgZ[0,1].set_xlim((150000,500000))
axAvgZ[1,0].set_xlim((150000,500000))
axAvgZ[1,1].set_xlim((150000,500000))
axAvgZ[0,0].set_title('Price Point 1', fontname="Arial", fontsize=12, fontweight='bold')
axAvgZ[0,1].set_title('Price Point 2', fontname="Arial", fontsize=12, fontweight='bold')
axAvgZ[1,0].set_title('Price Point 3', fontname="Arial", fontsize=12, fontweight='bold')
axAvgZ[1,1].set_title('Price Point 4', fontname="Arial", fontsize=12, fontweight='bold')
axAvgZ[0,0].set_ylabel('Average Rating', fontname="Arial", fontsize=12, fontweight='bold')
axAvgZ[1,0].set_xlabel('zhvi', fontname="Arial", fontsize=12, fontweight='bold')
axAvgZ[1,0].set_ylabel('Average Rating', fontname="Arial", fontsize=12, fontweight='bold')
axAvgZ[1,1].set_xlabel('zhvi', fontname="Arial", fontsize=12, fontweight='bold')
# plt.savefig('scatter_zhvi_avgrating_by_ppoint.png')

# Plotting restaurant proportion at different price points
# vs Median household income
figRestZ, axRestZ = plt.subplots(2, 2, sharex='col', sharey='row')
figRestZ.set_size_inches(8, 5)
plt.subplots_adjust(hspace=0.2, wspace=0.2)
axRestZ[0, 0].scatter(rRZil["zhvi"], rRZil[1], s=10)
axRestZ[0, 1].scatter(rRZil["zhvi"], rRZil[2], s=10)
axRestZ[1, 0].scatter(rRZil["zhvi"], rRZil[3], s=10)
axRestZ[1, 1].scatter(rRZil["zhvi"], rRZil[4], s=10)
axRestZ[0,0].set_ylim((0,0.8))
axRestZ[0,1].set_ylim((0,0.8))
axRestZ[1,0].set_ylim((0,0.8))
axRestZ[1,1].set_ylim((0,0.8))
axRestZ[0,0].set_xlim((150000,500000))
axRestZ[0,1].set_xlim((150000,500000))
axRestZ[1,0].set_xlim((150000,500000))
axRestZ[1,1].set_xlim((150000,500000))
axRestZ[0,0].set_title('Price Point 1', fontname="Arial", fontsize=12, fontweight='bold')
axRestZ[0,1].set_title('Price Point 2', fontname="Arial", fontsize=12, fontweight='bold')
axRestZ[1,0].set_title('Price Point 3', fontname="Arial", fontsize=12, fontweight='bold')
axRestZ[1,1].set_title('Price Point 4', fontname="Arial", fontsize=12, fontweight='bold')
axRestZ[0,0].set_ylabel('Restaurant Proportion', fontname="Arial", fontsize=12, fontweight='bold')
axRestZ[1,0].set_xlabel('zhvi', fontname="Arial", fontsize=12, fontweight='bold')
axRestZ[1,0].set_ylabel('Restaurant Proportion', fontname="Arial", fontsize=12, fontweight='bold')
axRestZ[1,1].set_xlabel('zhvi', fontname="Arial", fontsize=12, fontweight='bold')
# plt.savefig('scatter_zhvi_proprest_by_ppoint.png')


# generating comparative boxplots for average rating clustered by price point
avgRatingZhviDF = pd.merge(avgRatingByZipDF, yzi[["postalCode","zhvi"]], on="postalCode")
bxPlt_nw = plt.figure()
bxPlt1 = avgRatingZhviDF.boxplot(column=[1,2,3,4])
plt.ylabel('Average Rating', fontname="Arial", fontsize=12, fontweight='bold')
plt.xlabel('Price Point', fontname="Arial", fontsize=12, fontweight='bold')
# plt.savefig('comp_boxplot_ppoint_avgrating.png')
#plt.show()
