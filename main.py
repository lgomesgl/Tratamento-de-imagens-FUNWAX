import pandas as pd
import os

from classification_crystals import exclude_the_data, save_the_data, database, graphics
from validate_the_classfication import validate, get_image

FOLDER_PATH = '/home/lucas/FUNWAX/Images'
# FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Images'
NAME_CSV_FILE = 'Results.csv'

data = pd.DataFrame(columns=['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'cx', 'cy', 'major', 'minor', 'angle', 'AR'])
data_crystals = pd.DataFrame(columns=['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'N_of_crystals'])

cnt_ellipse = 0
cnt_rect = 0
N_of_crystals_ = [0]

files = os.listdir(FOLDER_PATH) # list with all files in folder
exclude_the_data(FOLDER_PATH, NAME_CSV_FILE)
for i, file in enumerate(files):
    if file.endswith('.jpg'): # take just the images
        data, image, contours, properties, N_of_crystals, cnt_ellipse, cnt_rect = database(FOLDER_PATH, file, data, cnt_ellipse, cnt_rect)
        print('%s...OK' % file)
        
        # validate the classify
        # image = get_image(FOLDER_PATH, NAME_CSV_FILE)
        # validate(image, data)
        
        
        # N_of_crystals_.append(N_of_crystals)
        # row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'Time':properties[6], 'N_of_crystals': int(N_of_crystals-N_of_crystals_[i])}])
        # data_crystals = pd.concat([data_crystals, row_to_append], ignore_index=True)
save_the_data(data, NAME_CSV_FILE)
        
# print(data)
graphics(data, data_crystals)

print('AR calculate by ellipse: %s' % cnt_ellipse)
print('AR calculate by rectangle: %s' % cnt_rect)
print('Total: %s' % (cnt_ellipse + cnt_rect))
print('Percentage of AR ellipse: %s' % (round((cnt_ellipse*100/(cnt_ellipse+cnt_rect)), 2)))