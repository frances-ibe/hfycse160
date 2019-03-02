# Nathaniel Linden
# Parker Grosjean
# Frances Ingram-Bate
import preProcessIRS as ppi
import preProcessZillow as ppz
import pandas as pd

# Load Data
zillowData = pd.read_csv("vegasHousing.csv")
zillowData.sort_values(by=["postalCode"])
zillowZip = set(zillowData["postalCode"]) # 38 zip codes
print(len(zillowZip))

irsData = pd.read_csv("")

yelpData = pd.read_csv("vegasRest.csv")
yelpData.sort_values(by=["postal_code"])
yelpZip = set(yelpData["postal_code"]) # 80 zip codes
### Note: the yelp data with city="Las Vegas" appears to have some mislabeled
# data, some of the zip codes are in other cities such as 85705 in Tucson

yelpZilZip = zillowZip & yelpZip # 38 common zipcodes

# filtering yelp data for zipcodes present in the Yelp dataset


#merge yelp and zillow data
# yelpZil = zillowData.copy()
# yelpZil.merge(yelpData, how="left", left_on="postalCode", right_on="postal_code")
# print(yelpZil)

# Compute Correlation Statistics Between household income and median home value
# Will utilze the IRS dataset
