'''
    Take each crystal that the script crystal_images.py has classify and do the classify manually
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os

from cristal_class import CrystalsClassification
# from classification_crystals import FOLDER_PATH, NAME_CSV_FILE
from classification_crystals import classification

# FOLDER_PATH = '/home/lucas/FUNWAX/Images'
# NAME_CSV_FILE = 'Results.csv' ## If don't need to atualize the DATA

def read_data(name_csv_file):
    return pd.read_csv(name_csv_file) 

def get_image(folder_path ,file):
    return cv2.imread('%s/%s' % (folder_path, file))

def validate(image, data, crystals):
    if len(crystals) == 1:
        first_index = 0
    else:
        first_index = crystals[-2]
        
    last_index = crystals[-1]
        
    # for i in range(data.shape[0]):
        
    #     x = int(data['cx'][i])
    #     dx = int(data['major'][i])
        
    #     y = int(data['cy'][i])
    #     dy = int(data['minor'][i])
        
    #     img_crystal = image[(y-dy):(y+dy), (x-dx):(x+dx)]
    #     img_crystal = img_crystal.astype(np.unit8)
    #     # print(img_crystal)
    #     cv2.imshow('Cristal', img_crystal)
    #     cv2.waitKey(0)
        









