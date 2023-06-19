import pandas as pd
import numpy as np
import os

def create_dataframes(columns):
    return pd.DataFrame(columns=columns)

def save_the_data(data, name_csv_file):
    return data.to_csv('Results' % name_csv_file, index=True)

def exclude_the_data(folder_path, name_csv_file):
    if os.path.isfile(folder_path):
        os.remove('%s\%s' %(folder_path, name_csv_file))