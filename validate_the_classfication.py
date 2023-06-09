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
    image = cv2.imread('%s/%s' % (folder_path, file))
    # crop the image
    height, width,_ = image.shape
    crop_size = int(min(height, width) * 0.40)
    x = int((width - crop_size) / 2)
    y = int((height - crop_size) / 2)
    image = image[y:y+crop_size, x:x+crop_size]
    return image

def validate(image, data, crystals):
    if len(crystals) == 1:
        first_index = 0
    else:
        first_index = crystals[-2]
        
    last_index = crystals[-1]
    
    for i in range(first_index, last_index):
        '''
            first_index & last_index its necessary because the data update for each image in loop.
            So we need to cut the data in the range corresponding to each image.
        '''   
        df = data.iloc[first_index:(first_index + last_index), :]
        
        x = int(df['cx'][i])
        dx = int(df['major'][i])
        
        y = int(df['cy'][i])
        dy = int(df['minor'][i])
        
        angle = int(df['angle'][i])
       
        # print(i)
        # print(df)
        # print(int(dy*np.abs(np.sin(angle*np.pi/180))))
        # print(int(dy*np.abs(np.cos(angle*np.pi/180))))
        corr = 50
        # image_crystal = image[(y- int(dy*np.abs(np.sin(angle*np.pi/180)))):(y+ int(dy*np.abs(np.sin(angle*np.pi/180)))), (x- int(dy*np.abs(np.cos(angle*np.pi/180)))):(x+ int(dy*np.abs(np.cos(angle*np.pi/180))))]
        try:
            image_crystal = image[(y-(dy+corr)):(y+(dy+corr)), (x-(dx+corr)):(x+(dx+corr))]
            cv2.namedWindow('crystal', cv2.WINDOW_NORMAL)
            cv2.imshow('crystal', image_crystal)
            cv2.waitKey(0)
            
            while True:
                check = input()
                crystal = CrystalsClassification()
                
                if check == 'opa':
                    crystal.save()
                    break
                
                elif check == 1:
                    crystal.validate_the_crystal()
                    
                elif check == 2:
                    crystal.invalidate_the_crystal()
                    
        except:
            print('Crystal out of boundaries')
        
        









