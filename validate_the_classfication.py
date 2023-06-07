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
from classification_crystals import database

# FOLDER_PATH = '/home/lucas/FUNWAX/Images'
# NAME_CSV_FILE = 'Results.csv' ## If don't need to atualize the DATA

def read_data(name_csv_file):
    return pd.read_csv(name_csv_file) 

def get_image(folder_path ,file):
    return cv2.imread('%s/%s' % (folder_path, file))

def validate(image, data):
    for i in range(data.shape[0]):
        img_crystal = image[int(data['cy'][i]): int(data['cy'][i]) + int(data['major'][i]), int(data['cx'][i]): int(data['cx'][i]) + int(data['minor'][i])]
        # print(img_crystal)
        cv2.imshow('Cristal', img_crystal)
        cv2.waitKey(0)
        
        print('1-Crystal \n 2-None')
        check = input()
        
        if check == ord('r'):
            CrystalsClassification.return_()
        
        while check == ord('\n'):
            if check == 1:
                CrystalsClassification.validate_the_crystal()
            elif check == 2:
                CrystalsClassification.invalidate_the_crystal()
                
        CrystalsClassification.save()








