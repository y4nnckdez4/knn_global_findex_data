import pandas as pd
import os
from preprocessing import preprocessing
from model import model
from chart_processing import chart_processing
from chart_processing import chart


def clustering():
    # Get the directory where the current script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the data.csv file
    data_path = os.path.join(current_dir, 'data.csv')
    # Read the CSV file
    raw_data = pd.read_csv(data_path)
    #Calling the 2 functions
    processed_data = preprocessing(raw_data)
    modeled_data = model(processed_data)

    return modeled_data


df = clustering()

# I return a first table with the clusters
df[['Country name', 'Cluster']].sort_values(by=['Cluster'], ascending=False)


# I return a graph with the column of interest
chart_data = chart_processing(df)
chart(chart_data, 4)
