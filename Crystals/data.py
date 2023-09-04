import pandas as pd
import numpy as np

def create_dataframes(columns):
    return pd.DataFrame(columns=columns)

def save_the_data(data, name_csv_file):
    return data.to_csv(name_csv_file, index=True)
        
def separate_the_data_by_column(data, column):
    '''
    dataframes name -> 'df_' + 'value filter'
    ex: by kernel -> df_(1, 1) & df_(3, 3)
    ''' 
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

def data_n_of_crystals(data_crystals, properties, n_of_crystals_,perct_parent, perct_child, perct_else ):
    n_of_crystals_per_image = np.diff(n_of_crystals_)
    
    row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'Time':properties[6], 'N_of_crystals': n_of_crystals_per_image[-1], 'Parent(%)':perct_parent, 'Child(%)':perct_child, 'No Parent/Child(%)':perct_else}])
    data_crystals = pd.concat([data_crystals, row_to_append], ignore_index=True)
    return data_crystals

