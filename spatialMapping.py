""" The following code performs choropleth map create for the visualization of
geographical data. Used  for the completion of our CSE 160 final project.
All supporting code and preprocessed data will be made available.

Authors: Frances Ingram-Bate, Parker Grosjean, Nathaniel Linden

Updated: March 8th 2019

Abbreviations (We will use these throughout the script):
-  zhvi - zillow homw value index
-  avgPrice - average restuarant price
-  yzi - yelp, zillow, IRS
"""

# imports
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl



# funcitons
def plot_spatialdata(file_name, zip_list_weighted, plot_title, geo_data_file='nevadaGeoData.min.json', filter_para='ZCTA5CE10'):
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
    fig, base = plt.subplots(1)
    ax = filtered_df.plot(ax=base, column=param_df[0], cmap='Oranges', edgecolor='black')
    plt.plot(-115.1728, 36.1147, 'b', markersize=10)
    ax.set_axis_off()

    label = [str(elm) for elm in np.linspace(min(list(zip_list_weighted.values())), max(list(zip_list_weighted.values())), num=7)]

    bins = np.arange(min(list(zip_list_weighted.values())), max(list(zip_list_weighted.values())), 23106)

    ax_legend = fig.add_axes([0.35, 0.06, 0.5, 0.03], zorder=3)
    cb = mpl.colorbar.ColorbarBase(ax_legend, cmap='Oranges', ticks=bins, orientation='horizontal')
    cb.ax.set_xticklabels([str(round(i, 1)) for i in bins], color='black')



    base.set_title(plot_title)
    fig.set_size_inches(8,8)
    plt.savefig(file_name + '.png')
# zippped = {'89108':[22750], '89121':[228200],'89123':[300100],'89110':[218000]}
# plot_spatialdata('moo.jpg',zippped)
