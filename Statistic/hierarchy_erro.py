import numpy as np
import pandas as pd
from Statistic.datasets import separate_data_statistic, parameters_dataframe

data = pd.read_csv('D:\LUCAS\IC\FUNWAX\Results_number_of_crystals.csv')

dataframes = separate_data_statistic(data)
parameters = parameters_dataframe(dataframes)

def hierarchy_erro():
    count_erro = 0 
    for i in range(data.shape[0]):
        image_param = data.iloc[i,:]
        type = image_param['Type']
        reynold = image_param['Reynolds']
        n_crystals_image = image_param['N_of_crystals']
        parent_image = image_param['Parent(%)']
        child_image = image_param['Child(%)']
        else_image = image_param['No Parent/Child(%)']
        
        # take the parameters of the images groups to comapare
        conj = parameters[(parameters['Group'] == 'df_%s_%s' % (str(type).lower(), reynold))] 
        n_crystals_conj = conj['N crystal'].values[0]
        parent_conj = conj['Parent'].values[0]
        child_conj = conj['Child'].values[0]
        else_conj = conj['No parent/child'].values[0]
        
        if n_crystals_conj == 'nan+-nan':
            n_crystals_conj == 0.0
        if parent_conj == 'nan%+-nan':
            parent_conj == 0.0
        if child_conj == 'nan%+-nan':
            child_conj == 0.0
        if else_conj == 'nan%+-nan':
            else_conj == 0.0                
        
        ''' 
            Condition -> image_parameter < (mean of group that it belong - std)*0.95 or image_parameter > (mean of group that it belong + std)*1.05
        '''
        if parent_image < (float(parent_conj.split('%+-')[0]) - float(parent_conj.split('%+-')[1]))*0.95 or parent_image > (float(parent_conj.split('%+-')[0]) + float(parent_conj.split('%+-')[1]))*1.05:
            print(i, 'Parent')
            count_erro += 1
            continue
        elif child_image < (float(child_conj.split('%+-')[0]) - float(child_conj.split('%+-')[1]))*0.95 or child_image > (float(child_conj.split('%+-')[0]) + float(child_conj.split('%+-')[1]))*1.05:
            print(i, 'Child')
            count_erro += 1
            continue
        elif else_image < (float(else_conj.split('%+-')[0]) - float(else_conj.split('%+-')[1]))*0.95 or else_image > (float(else_conj.split('%+-')[0]) + float(else_conj.split('%+-')[1]))*1.05:
            print(i, 'No parent/child')
            count_erro += 1
            continue
        # elif n_crystals_image < (float(n_crystals_conj.split('+-')[0]) - float(n_crystals_conj.split('+-')[1]))*0.90 or n_crystals_image > (float(n_crystals_conj.split('+-')[0]) + float(n_crystals_conj.split('+-')[1]))*1.10:
        #     print(i, 'N of crystals')
        #     count_erro += 1
        #     continue
         
    erro = count_erro/data.shape[0]   
    return erro