import pandas as pd
import numpy as np

def separate_data_statistic(data):
    types = data['Type'].unique()
    reynolds = data['Reynolds'].unique()
    
    dataframes = {}
    for type in types:
        for reynold in reynolds:
            dataframes['df_%s_%s' % (str(type).lower(), reynold)] = data[(data['Type'] == type) & (data['Reynolds'] == reynold)]
        
    return dataframes

def calculate_parameters(data):
    parameters = data.describe()
    mean_n_crystals = parameters['N_of_crystals']['mean']
    std_n_crystals = parameters['N_of_crystals']['std']
    mean_parent = parameters['Parent(%)']['mean']
    std_parent = parameters['Parent(%)']['std']
    mean_child = parameters['Child(%)']['mean']
    std_child = parameters['Child(%)']['std'] 
    mean_else = parameters['No Parent/Child(%)']['mean']
    std_else = parameters['No Parent/Child(%)']['std']     
    
    return mean_n_crystals,std_n_crystals,mean_parent,std_parent,mean_child,std_child,mean_else,std_else    

def parameters_dataframe(dataframes):
    '''
        Create a DF with the parameters about the hierarchy of func findCountours by Group
    '''
    parameters = pd.DataFrame(columns=['Data','N crystal','Parent', 'Child', 'No parent/child'])
    for datas in dataframes:
        mean_n_crystals,std_n_crystals,mean_parent,std_parent,mean_child,std_child,mean_else,std_else = calculate_parameters(dataframes[datas])
        row_to_append = pd.DataFrame([{'Group':datas, 'N crystal':'%s+-%s' %(round(mean_n_crystals, 2), round(std_n_crystals,2)), 'Parent':'%s%%+-%s' %(round(mean_parent, 2), round(std_parent,2)),
                                    'Child':'%s%%+-%s' %(round(mean_child, 2), round(std_child,2)), 'No parent/child':'%s%%+-%s' %(round(mean_else, 2), round(std_else,2))}])
        parameters = pd.concat([parameters, row_to_append], ignore_index=True)
    return parameters