# Nathaniel Linden
# Script to USE goepandas to create a geographical visualizaiton
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt


# funcitons
def plot_spatialdata(file_name, zip_list_weighted, geo_data_file='nevadaGeoData.min.json', filter_para='ZCTA5CE10'):
    """ The following function creates a choropleth map for the geo_data stored
    in the geo_data_frame. If zip_list is specefied the data will be filtered by
    this list of attributes. If weights is unspecified all objects will have the
    same coloring.

    geo_data_frame - a geopandas data frame
    file_name - name to save output graph in current working directory
    zip_list_weighted - maps from of values for one attribute in geo_data_frame
    to the weights associated with those values. The data will be
    filtered based on these values and the map will be colored according to the
    weights.
    filter_para - parameter corresponding to the values to be filtered by.
    Default to zip_codes in GeoJSON data for Nevada
    """
    #read in GeoJSON data
    # Data from: https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/nv_nevada_zip_codes_geo.min.json
    geo_data_frame = gpd.read_file(geo_data_file)

    # filter based on keys of zip_list_weighted
    filter_by = list(zip_list_weighted.keys())  # list of items to filter by
    # do the filtering
    filtered_df = geo_data_frame[geo_data_frame[filter_para].isin(filter_by)]
    # print(filtered_df[filter_para])
    param_df = pd.DataFrame.from_dict(zip_list_weighted, orient='index')
    print(param_df)

    filtered_df.plot(column=param_df[0], edgecolor='black')
    plt.show()
zippped = {'89108':[22750], '89121':[228200],'89123':[300100],'89110':[218000]}
plot_spatialdata('moo.jpg',zippped)
