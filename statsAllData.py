# Nathaniel Linden
# Parker Grosjean
# Frances Ingram-Bate
import preProcessIRS as ppi
import preProcessZillow as ppz
import pandas as pd

# Load Data
zillowData = pd.read_csv("vegasHousing.csv")
zillowData.sort_values(by=["postalCode"])

# Compute Correlation Statistics Between household income and median home value
# Will utilze the IRS dataset
