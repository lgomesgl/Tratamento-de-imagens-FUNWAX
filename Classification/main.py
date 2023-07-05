import pandas as pd
import os

from data import create_dataframes, row_to_append, separate_the_data_by_column, save_the_data, exclude_the_data
from classification_crystals import get_properties, get_image, crop_the_image, filter, classification
from pos_processing import graphics

FOLDER_PATH = '/home/lucas/FUNWAX/Images' ## linux path
# FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Images'
NAME_CSV_FILE = 'Results.csv'

data = create_dataframes(['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'cx', 'cy', 'major', 'minor', 'angle', 'kernel', 'AR'])
data_crystals = create_dataframes(['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'N_of_crystals'])

cnt_ellipse = 0
cnt_rect = 0
n_of_crystals_ = [0]
kernels = [(1, 1), (3, 3)]

exclude_the_data(FOLDER_PATH, NAME_CSV_FILE) # exclude the data to update the csv file
        
files = os.listdir(FOLDER_PATH) # list with all files in folder
for i, file in enumerate(files):
    properties = get_properties(file)
    image = get_image(FOLDER_PATH, file)
    
    if properties[1] == 'Macro':
        image = crop_the_image(image, 0.4)
    
    for kernel in kernels:
        contours = filter(image, properties, kernel)
        data, image, contours, n_of_crystals, cnt_ellipse, cnt_rect = classification(image, data, contours, properties, cnt_ellipse, cnt_rect, kernel)

    # n_of_crystals_.append(n_of_crystals)
    # row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'Time':properties[6], 'N_of_crystals': int(n_of_crystals-n_of_crystals_[i])}])
    # data_crystals = pd.concat([data_crystals, row_to_append], ignore_index=True)
    
    # data_crystals = row_to_append(data_crystals, ['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'N_of_crystals'],
    #                               [properties[1], properties[3], properties[4], properties[5], properties[6], (n_of_crystals - n_of_crystals_[i])])
    
    print('%s...Ok' % file)
    
save_the_data(data, NAME_CSV_FILE) # update the data

dataframes = separate_the_data_by_column(data, 'kernel')
'''
    dataframes name -> 'df_' + 'value filter'
    ex: by kernel -> df_(1, 1) & df_(3, 3)
'''

# print(data)
graphics(dataframes['df_(1, 1)'])
graphics(dataframes['df_(3, 3)'])

# print('AR calculate by ellipse: %s' % cnt_ellipse)
# print('AR calculate by rectangle: %s' % cnt_rect)
# print('Total: %s' % (cnt_ellipse + cnt_rect))
# print('Percentage of AR ellipse: %s' % (round((cnt_ellipse*100/(cnt_ellipse+cnt_rect)), 2)))