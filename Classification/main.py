import pandas as pd
import numpy as np
import os

from classification_crystals import get_properties, get_image, crop_the_image, filter, classification, exclude_the_data, save_the_data
from pos_processing import graphics

# FOLDER_PATH = '/home/lucas/FUNWAX/Images' ## linux path
FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Images'
NAME_CSV_FILE = 'Results.csv'

# DataFrames
data = pd.DataFrame(columns=['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'cx', 'cy', 'major', 'minor', 'angle', 'AR'])
data_crystals = pd.DataFrame(columns=['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'N_of_crystals'])

cnt_ellipse = 0
cnt_rect = 0
n_of_crystals_ = [0]

exclude_the_data(FOLDER_PATH, NAME_CSV_FILE) # exclude the data to update the csv file
        
files = os.listdir(FOLDER_PATH) # list with all files in folder
for i, file in enumerate(files):
    properties = get_properties(file)
    image = get_image(FOLDER_PATH, file)
    image = crop_the_image(image, 0.4)
    contours = filter(image, properties)
    data, image, contours, properties, n_of_crystals, cnt_ellipse, cnt_rect = classification(image, data, contours, properties, cnt_ellipse, cnt_rect)

    row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'Time':properties[6], 'N_of_crystals': int(n_of_crystals-n_of_crystals_[i])}])
    data_crystals = pd.concat([data_crystals, row_to_append], ignore_index=True)
    
    print('%s...Ok' % file)

# save_the_data(data, NAME_CSV_FILE)

# print(data)
graphics(data, data_crystals)

# print('AR calculate by ellipse: %s' % cnt_ellipse)
# print('AR calculate by rectangle: %s' % cnt_rect)
# print('Total: %s' % (cnt_ellipse + cnt_rect))
# print('Percentage of AR ellipse: %s' % (round((cnt_ellipse*100/(cnt_ellipse+cnt_rect)), 2)))