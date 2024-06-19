import pandas as pd
import numpy as np
import os


def preprocessing(data):

    # I filter the dataframe only for African countries
    data_subset = data[data['Region'] == 'Sub-Saharan Africa (excluding high income)']
    countries_list = list(data_subset['Country name'].unique())
    africa = data[data['Country name'].isin(countries_list)]
    africa.reset_index(inplace=True, drop=True)

    # I remove the sub-region aggregated info
    africa = africa[:141]

    # The data contains info on several years (2014, 2017 and 2021)
    # If I try to select only the year 2021, I'll lose a lot of information.
    # I'll try to drop everything and only keep the last record

    africa = africa.drop_duplicates(subset=['Country name'], keep='last')
    africa.reset_index(inplace=True, drop=True)

    # In this way I managed to keep the majority of the countries I am interested in.

    # Now I want to drop the columns for which there are too many Null values.

    af = africa.copy()
    nulls = pd.DataFrame(af.isnull().sum().sort_values(ascending=False), columns=['n_nulls'])
    cols_to_drop_complete = list(nulls[nulls['n_nulls'] != 42].index)

    # I decide an arbitrary tolerance threshold: 10
    # This means that I drop all columns that have more than 10 countries having no record

    cols_to_drop = list(nulls[nulls['n_nulls'] > 10].index)
    af.drop(columns=cols_to_drop, inplace=True)

    # I am left with 875 columns. This is a first filtering.


    # 875 columns is still a lot. I need some type of manual selection of the most important columns for our use case

    from manual_selection import manual_selection


    # I drop the ones not included in the list
    af.drop(columns=[col for col in list(af.columns) if col not in manual_selection], inplace=True)
    af.columns

    # I have reduced the total amount of columns to 141


    # I transform all the percentages in float values (after removing the %)

    af[af.columns[6:]] = af[af.columns[6:]].apply(lambda x: x.str.strip('%'))
    af[af.columns[6:]] = af[af.columns[6:]].astype('float64')

    # I set a max threshold of Null values in a country record
    threshold = af.shape[1]/3

    # I notice that I might remove countries where Null values for more than haf of the variables

    c = af.isnull().sum(axis=1).sort_values(ascending=False)

    rows_to_drop = []
    for index, value in c.items():
        if value > threshold:
            rows_to_drop.append(index)

    # I create a memory of the countries dropped
    countries_dropped = af.iloc[rows_to_drop]['Country name']

    # And I remove them from the dataframe
    af.drop(index=rows_to_drop, axis=1, inplace=True)
    af.reset_index(inplace=True, drop=True)


    # I can now return my results
    return af
