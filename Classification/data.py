import pandas as pd
import numpy as np
import os

def create_dataframes(columns):
    return pd.DataFrame(columns=columns)

def save_the_data(data, name_csv_file):
    return data.to_csv(name_csv_file, index=True)

def exclude_the_data(folder_path, name_csv_file):
    if os.path.isfile(folder_path):
        os.remove('%s\%s' % (folder_path, name_csv_file))
        
def separate_the_data_by_column(data, column):
    values = data[column].unique()
    dataframes = {}
    for i in range(len(values)):
        dataframes['df_%s' % str(values[i])] = data[(data[column] == values[i])]
    return dataframes

def row_to_append(dataframe, columns, values):
    dict = {}
    for i, column in enumerate(columns):
        dict[column] = values[i]
    row_to_append = pd.DataFrame([dict])
    return pd.concat([dataframe, row_to_append], ignore_index=True)